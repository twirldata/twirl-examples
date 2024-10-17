import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("mean_absolute_error", twirl.Float()),
                twirl.Column("train_test_split_timestamp", twirl.Timestamp(unit="us", tz="UTC")),
            ]
        ),
        inputs=[
            twirl.Input("gcs/github_models/pr_closing_time_models"),
        ],
        job=twirl.PythonJob(
            update_method=twirl.UpdateMethod.REPLACE,
            resource_config=twirl.CloudRunResourceConfig(cpu_count=1, memory="2G"),
        ),
        tags=["engineering", "github_predictions"],
    )
)
