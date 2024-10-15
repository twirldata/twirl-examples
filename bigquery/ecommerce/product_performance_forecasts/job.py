import pandas as pd
from prophet import Prophet


def reshape(df: pd.DataFrame) -> pd.DataFrame:
    """Reshape the dataframe to be in the format that Prophet expects."""
    return pd.DataFrame(dict(ds=df.date, y=df.daily_orders.fillna(0)))


def job(input_tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Forecast product performance for the next 30 days."""
    df = input_tables["fct_product_performance"]

    forecasts = []
    g = df.groupby("product_id")
    for product_id, frame in g:
        prophet_model = Prophet()
        prophet_model.fit(reshape(frame))
        future = prophet_model.make_future_dataframe(periods=30)
        forecast = prophet_model.predict(future)
        forecast = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(30)
        forecast["product_id"] = product_id
    forecasts.append(forecast)

    ret = pd.concat(forecasts)
    ret["ds"] = ret.ds.dt.as_unit("us")

    return ret
