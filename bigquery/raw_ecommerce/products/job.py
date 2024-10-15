import pandas as pd
from sqlalchemy import create_engine, text


def job(secrets: dict[str, str]) -> pd.DataFrame:
    engine = create_engine(secrets["mock-db-url"])
    query = "SELECT * FROM products"

    with engine.connect() as connection:
        return pd.read_sql(text(query), connection)
