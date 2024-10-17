import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("user", twirl.String()),
                twirl.Column("user_average_pr_closing_time", twirl.Float()),
            ]
        ),
        inputs=[
            twirl.Input("bigquery/clean/pull_requests"),
        ],
        job=twirl.BigQueryJob(update_method=twirl.UpdateMethod.REPLACE),
        tags=["engineering", "github_predictions"],
    )
)
