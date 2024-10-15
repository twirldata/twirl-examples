from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, text


def job(state: dict[str, str], secrets: dict[str, str]) -> pd.DataFrame:
    engine = create_engine(secrets["mock-db-url"])
    last_updated_at = state.get("last_updated_at", datetime(2024, 1, 1).isoformat())

    query = f"""
    SELECT * FROM events
    WHERE timestamp > '{last_updated_at}'
    """

    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection)
        df["fetched_at"] = datetime.now()
        df["timestamp"] = df["timestamp"].astype("datetime64[us]")
        last_updated_at = df.timestamp.max().isoformat() if len(df) > 0 else last_updated_at
        return df, {"last_updated_at": last_updated_at}
