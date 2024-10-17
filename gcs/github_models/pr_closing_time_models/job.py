import codecs
import pickle
from datetime import UTC, datetime

import pandas as pd
from sklearn.metrics import mean_absolute_error
from xgboost.sklearn import XGBRegressor

FEATURES = [
    "title_n_characters",
    "body_n_characters",
    "n_labels",
    "repository_average_pr_closing_time",
    "user_average_pr_closing_time",
]
LABEL = "closing_time_hours"


def job(input_tables: dict[str, pd.DataFrame]) -> dict[str, bytes]:
    pull_request_features = input_tables["bigquery/github_models/pull_request_features"]
    repository_features = input_tables["bigquery/github_models/repository_features"]
    user_features = input_tables["bigquery/github_models/user_features"]
    pr_closing_time_outcomes = input_tables["bigquery/github_models/pr_closing_time_outcomes"]

    # Merge the feature vectors
    df_features = pull_request_features
    df_features = df_features.merge(repository_features, on="repository")
    df_features = df_features.merge(user_features, left_on="login", right_on="user")

    # Generate training and test datasets - use most recent data for testing
    df_full = pr_closing_time_outcomes.merge(df_features, how="left")
    train_test_split_timestamp = df_full["created_at"].quantile(0.9)
    df_test = df_full[df_full["created_at"] >= train_test_split_timestamp].reset_index().copy()
    df_train = df_full[df_full["created_at"] < train_test_split_timestamp].reset_index().copy()

    # Train model
    model = XGBRegressor()
    model = model.fit(df_train[FEATURES], df_train[LABEL])

    # Evaluate
    df_test["predicted_closing_time_hours"] = model.predict(df_test[FEATURES])
    mae = mean_absolute_error(df_test["closing_time_hours"], df_test["predicted_closing_time_hours"])

    # Construct training metadata output
    metadata = pd.DataFrame(
        data={
            "mean_absolute_error": [mae],
            "train_test_split_timestamp": [train_test_split_timestamp],
        }
    )

    # Serialize metadata to JSON and encode to utf-8
    encoded_metadata = metadata.to_json(orient="records", date_format="iso").encode()

    # Serialize model and encode to base64
    encoded_model = codecs.encode(pickle.dumps(model), "base64")

    model_version_id = datetime.now(UTC).isoformat().removesuffix("+00:00").replace(":", "-").replace(".", "-")
    model_file_name = f"model-{model_version_id}.pkl"
    metadata_file_name = f"metadata-{model_version_id}.json"

    return {
        model_file_name: encoded_model,
        metadata_file_name: encoded_metadata,
    }
