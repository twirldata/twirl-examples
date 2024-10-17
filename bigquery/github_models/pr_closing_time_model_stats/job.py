import io
from typing import BinaryIO

import pandas as pd

from ..model_utils import latest_model_metadata


def job(input_file_collections: dict[str, dict[str, BinaryIO]]) -> pd.DataFrame:
    _, metadata_filehandle = latest_model_metadata(input_file_collections["gcs/github_models/pr_closing_time_models"])

    metadata_raw = metadata_filehandle.read()
    metadata = pd.read_json(io.BytesIO(metadata_raw))
    metadata["train_test_split_timestamp"] = pd.to_datetime(metadata["train_test_split_timestamp"])

    return metadata
