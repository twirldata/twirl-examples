from typing import Any, BinaryIO

import pandas as pd
from pypdf import PdfReader


def job(input_file_collections: dict[str, dict[str, BinaryIO]]) -> dict[str, Any]:
    df = pd.DataFrame(columns=["file_name", "page_num", "page_text"])

    for file_name, file_contents in input_file_collections["gcs/contracts"].items():
        reader = PdfReader(file_contents)
        for page in reader.pages:
            page_num = page.page_number
            page_text = page.extract_text()
            df = pd.concat(
                (
                    df,
                    pd.DataFrame(
                        {
                            "file_name": file_name,
                            "page_num": page_num,
                            "page_text": page_text,
                        },
                        index=[0],
                    ),
                )
            )

    return df
