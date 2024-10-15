from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, text


def job(state: dict[str, str], secrets: dict[str, str]) -> pd.DataFrame:
    # Create a connection to the PostgreSQL database
    engine = create_engine(secrets["mock-db-url"])
    last_updated_at = state.get("last_updated_at", datetime(2024, 1, 1).isoformat())
    # Determine the time range for incremental loading
    query = f"""
    SELECT * FROM users
    WHERE registration_date > '{last_updated_at}'
    """

    # Execute the query and load the results into a DataFrame
    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection)
        df["fetched_at"] = datetime.now()
        df["registration_date"] = df["registration_date"].astype("datetime64[us]")
        last_updated_at = df.registration_date.max().isoformat() if len(df) > 0 else last_updated_at
        return df, {"last_updated_at": last_updated_at}
