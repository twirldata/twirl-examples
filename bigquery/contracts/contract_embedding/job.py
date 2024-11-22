from collections.abc import Iterable

from sentence_transformers import SentenceTransformer


def job(rows: list[dict]) -> Iterable[dict]:
    model = SentenceTransformer("all-MiniLM-L6-v2")

    output = []
    for row in rows:
        page_text = row["page_text"]
        embedding = model.encode(
            page_text,
            show_progress_bar=False,
            convert_to_tensor=True,
        )
        row["page_embedding"] = embedding.tolist()
        output.append(row)

    return output
