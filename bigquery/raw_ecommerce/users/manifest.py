from datetime import timedelta

import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("user_id", twirl.String()),
                twirl.Column("name", twirl.String()),
                twirl.Column("email", twirl.String()),
                twirl.Column("registration_date", twirl.Timestamp(unit="us", tz="UTC")),
                twirl.Column("fetched_at", twirl.Timestamp(unit="us", tz="UTC")),
            ]
        ),
        job=twirl.PythonJob(update_method=twirl.UpdateMethod.APPEND, secrets=[twirl.SecretId("mock-db-url")]),
        tags=["ecommerce"],
        trigger_conditions=twirl.TriggerWithoutInputs(once_every=timedelta(hours=1)),
    )
)
