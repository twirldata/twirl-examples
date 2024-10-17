import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("pull_request_id", twirl.String()),
                twirl.Column("created_at", twirl.Timestamp(unit="us", tz="UTC"), is_event_time=True),
                twirl.Column("title_n_characters", twirl.Integer()),
                twirl.Column("body_n_characters", twirl.Integer()),
                twirl.Column("n_labels", twirl.Integer()),
                twirl.Column("repository", twirl.String()),
                twirl.Column("login", twirl.String()),
            ]
        ),
        inputs=[
            twirl.Input("bigquery/clean/pull_requests"),
        ],
        job=twirl.BigQueryJob(update_method=twirl.UpdateMethod.REPLACE),
        tags=["engineering", "github_predictions"],
    )
)
