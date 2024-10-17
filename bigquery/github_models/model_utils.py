from typing import Any


def latest_model(file_collection: dict[str, Any]) -> tuple[str, object]:
    model_files = {k: v for k, v in file_collection.items() if k.startswith("model-")}
    if not model_files:
        raise ValueError("No model files found in input")

    model_file_name, model = sorted(model_files.items())[-1]

    return model_file_name, model


def latest_model_metadata(file_collection: dict[str, Any]) -> tuple[str, object]:
    metadata_files = {k: v for k, v in file_collection.items() if k.startswith("metadata-")}
    if not metadata_files:
        raise ValueError("No model metadata files found in input")

    metadata_file_name, metadata = sorted(metadata_files.items())[-1]

    return metadata_file_name, metadata
