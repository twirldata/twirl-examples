import codecs
import pickle
from typing import BinaryIO

import pandas as pd

from ..model_utils import latest_model


def job(input_tables: dict[str, pd.DataFrame], input_file_collections: dict[str, BinaryIO]) -> pd.DataFrame:
    pull_request_features = input_tables["bigquery/github_models/pull_request_features"]
    repository_features = input_tables["bigquery/github_models/repository_features"]
    user_features = input_tables["bigquery/github_models/user_features"]
    pr_closing_time_models = input_file_collections["gcs/github_models/pr_closing_time_models"]

    # Merge the feature vectors
    df_features = pull_request_features
    df_features = df_features.merge(repository_features, on="repository")
    df_features = df_features.merge(user_features, left_on="login", right_on="user")
    df_features = df_features[
        [
            "pull_request_id",
            "title_n_characters",
            "body_n_characters",
            "n_labels",
            "repository_average_pr_closing_time",
            "user_average_pr_closing_time",
        ]
    ]

    # Load the pickled previously trained prediction model
    model_file_name, model_filehandle = latest_model(pr_closing_time_models)
    model = pickle.loads(codecs.decode(model_filehandle.read(), "base64"))

    # Make the predictions
    df_out = df_features[["pull_request_id"]].copy()
    df_out["predicted_closing_time_hours"] = model.predict(df_features.drop(columns=["pull_request_id"]))
    df_out["model_file_name"] = model_file_name

    return df_out
