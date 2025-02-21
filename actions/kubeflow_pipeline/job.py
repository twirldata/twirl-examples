import google.cloud.aiplatform as aiplatform
import google.cloud.aiplatform_v1 as aiplatform_v1

from kfp import compiler, dsl
from kfp.dsl import Artifact, Dataset, Input, Metrics, Model, Output, component

# Adapted from https://github.com/GoogleCloudPlatform/vertex-ai-samples/blob/0cf6d0235ed09f891ebb70310a3ce35235032544/notebooks/official/pipelines/kfp2_pipeline.ipynb
# See https://docs.twirldata.com/concepts/jobs#kubeflowjob-gcp for information on what permissions are required etc.

@component(
    base_image="python:3.12",
    packages_to_install=["google-cloud-bigquery==3.10.0"],
)
def create_census_view(
    project_id: str,
    dataset_id: str,
    view_name: str,
):
    """Creates a BigQuery view on `bigquery-public-data.ml_datasets.census_adult_income`.

    Args:
        project_id: The Project ID.
        dataset_id: The BigQuery Dataset ID. Must be pre-created in the project.
        view_name: The BigQuery view name.
    """
    from google.cloud import bigquery

    client = bigquery.Client(project=project_id)

    create_or_replace_view = """
        CREATE OR REPLACE VIEW
        `{dataset_id}`.`{view_name}` AS
        SELECT
          age,
          workclass,
          education,
          education_num,
          marital_status,
          occupation,
          relationship,
          race,
          sex,
          capital_gain,
          capital_loss,
          hours_per_week,
          native_country,
          income_bracket,
        FROM
          `bigquery-public-data.ml_datasets.census_adult_income`
    """.format(dataset_id=dataset_id, view_name=view_name)

    job_config = bigquery.QueryJobConfig()
    query_job = client.query(query=create_or_replace_view, job_config=job_config)
    query_job.result()


@component(
    base_image="python:3.12",
    packages_to_install=["google-cloud-bigquery[pandas]==3.10.0"],
)
def export_dataset(
    project_id: str,
    dataset_id: str,
    view_name: str,
    dataset: Output[Dataset],
):
    """Exports from BigQuery to a CSV file.

    Args:
        project_id: The Project ID.
        dataset_id: The BigQuery Dataset ID. Must be pre-created in the project.
        view_name: The BigQuery view name.

    Returns:
        dataset: The Dataset artifact with exported CSV file.
    """
    from google.cloud import bigquery

    client = bigquery.Client(project=project_id)

    table_name = f"{project_id}.{dataset_id}.{view_name}"
    query = """
    SELECT
      *
    FROM
      `{table_name}`
    """.format(table_name=table_name)

    job_config = bigquery.QueryJobConfig()
    query_job = client.query(query=query, job_config=job_config)
    df = query_job.result().to_dataframe()
    df.to_csv(dataset.path, index=False)


@component(
    base_image="python:3.12",
    packages_to_install=[
        "numpy==1.26.0",
        "xgboost==1.7.6",
        "pandas==1.5.3",
        "joblib==1.4.2",
        "scikit-learn==1.5.2",
    ],
)
def xgboost_training(
    dataset: Input[Dataset],
    model: Output[Model],
    metrics: Output[Metrics],
):
    """Trains an XGBoost classifier.

    Args:
        dataset: The training dataset.

    Returns:
        model: The model artifact stores the model.joblib file.
        metrics: The metrics of the trained model.
    """
    import os

    import joblib
    import pandas as pd
    import xgboost as xgb
    from sklearn.metrics import accuracy_score, precision_recall_curve, roc_auc_score
    from sklearn.model_selection import (
        RandomizedSearchCV,
        StratifiedKFold,
        train_test_split,
    )
    from sklearn.preprocessing import LabelEncoder

    # Load the training census dataset
    with open(dataset.path, "r") as train_data:
        raw_data = pd.read_csv(train_data)

    CATEGORICAL_COLUMNS = (
        "workclass",
        "education",
        "marital_status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "native_country",
    )
    LABEL_COLUMN = "income_bracket"
    POSITIVE_VALUE = " >50K"

    # Convert data in categorical columns to numerical values
    encoders = {col: LabelEncoder() for col in CATEGORICAL_COLUMNS}
    for col in CATEGORICAL_COLUMNS:
        raw_data[col] = encoders[col].fit_transform(raw_data[col])

    X = raw_data.drop([LABEL_COLUMN], axis=1).values
    y = raw_data[LABEL_COLUMN] == POSITIVE_VALUE

    X_train, X_test, y_train, y_test = train_test_split(X, y)
    _ = xgb.DMatrix(X_train, label=y_train)
    _ = xgb.DMatrix(X_test, label=y_test)

    params = {
        "reg_lambda": [0, 1],
        "gamma": [1, 1.5, 2, 2.5, 3],
        "max_depth": [2, 3, 4, 5, 10, 20],
        "learning_rate": [0.1, 0.01],
    }

    xgb_model = xgb.XGBClassifier(
        n_estimators=50,
        objective="binary:hinge",
        silent=True,
        nthread=1,
        eval_metric="auc",
    )

    folds = 5
    param_comb = 20

    skf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=42)

    random_search = RandomizedSearchCV(
        xgb_model,
        param_distributions=params,
        n_iter=param_comb,
        scoring="precision",
        n_jobs=4,
        cv=skf.split(X_train, y_train),
        verbose=4,
        random_state=42,
    )

    random_search.fit(X_train, y_train)
    xgb_model_best = random_search.best_estimator_
    predictions = xgb_model_best.predict(X_test)
    score = accuracy_score(y_test, predictions)
    auc = roc_auc_score(y_test, predictions)
    _ = precision_recall_curve(y_test, predictions)

    metrics.log_metric("accuracy", (score * 100.0))
    metrics.log_metric("framework", "xgboost")
    metrics.log_metric("dataset_size", len(raw_data))
    metrics.log_metric("AUC", auc)

    # Export the model to a file
    os.makedirs(model.path, exist_ok=True)
    joblib.dump(xgb_model_best, os.path.join(model.path, "model.joblib"))

PROJECT_ID = "twirldata-demo"

@dsl.pipeline(
    name="census-demo-pipeline",
)
def pipeline():
    """A demo pipeline."""

    dataset_id = "vertex_ai_test"  # The BigQuery Data Set ID for the view
    view_name = "census_data"  # BigQuery view for input data
    create_input_view_task = create_census_view(
        project_id=PROJECT_ID,
        dataset_id=dataset_id,
        view_name=view_name,
    )

    export_dataset_task = (
        export_dataset(
            project_id=PROJECT_ID,
            dataset_id=dataset_id,
            view_name=view_name,
        )
        .after(create_input_view_task)
        .set_caching_options(False)
    )

    training_task = xgboost_training(
        dataset=export_dataset_task.outputs["dataset"],
    )
