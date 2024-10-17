import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("pull_request_id", twirl.String(), is_primary_key=True),
                twirl.Column("predicted_closing_time_hours", twirl.Float()),
                twirl.Column("model_file_name", twirl.String()),
            ]
        ),
        inputs=[
            twirl.Input("gcs/github_models/pr_closing_time_models"),
            twirl.Input("bigquery/github_models/pull_request_features"),
            twirl.Input("bigquery/github_models/user_features"),
            twirl.Input("bigquery/github_models/repository_features"),
        ],
        job=twirl.PythonJob(update_method=twirl.UpdateMethod.REPLACE),
        tags=["engineering", "github_predictions"],
    )
)
