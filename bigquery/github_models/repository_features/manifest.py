import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("repository", twirl.String()),
                twirl.Column("repository_average_pr_closing_time", twirl.Float()),
            ]
        ),
        inputs=[
            twirl.Input("bigquery/clean/pull_requests"),
        ],
        job=twirl.BigQueryJob(update_method=twirl.UpdateMethod.REPLACE),
        tags=["engineering", "github_predictions"],
    )
)
