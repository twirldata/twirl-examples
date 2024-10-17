import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("pull_request_id", twirl.String(), validations=[twirl.NotNull()]),
                twirl.Column("created_at", twirl.Timestamp(unit="us", tz="UTC"), is_event_time=True),
                twirl.Column("closing_time_hours", twirl.Float()),
            ]
        ),
        inputs=[
            twirl.Input("bigquery/clean/pull_requests"),
        ],
        job=twirl.BigQueryJob(update_method=twirl.UpdateMethod.REPLACE),
        tags=["engineering", "github_predictions"],
    )
)
