from datetime import timedelta

import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("event_id", twirl.String()),
                twirl.Column("user_id", twirl.String()),
                twirl.Column("product_id", twirl.String()),
                twirl.Column("event_type", twirl.String()),
                twirl.Column("timestamp", twirl.Timestamp(unit="us", tz="UTC")),
                twirl.Column("fetched_at", twirl.Timestamp(unit="us", tz="UTC")),
            ]
        ),
        job=twirl.PythonJob(update_method=twirl.UpdateMethod.APPEND, secrets=[twirl.SecretId("mock-db-url")]),
        tags=["ecommerce"],
        trigger_conditions=twirl.TriggerWithoutInputs(once_every=timedelta(hours=1)),
    )
)
