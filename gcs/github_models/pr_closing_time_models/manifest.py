from datetime import timedelta

import twirl

twirl.manifest(
    twirl.FileCollection(
        inputs=[
            twirl.Input("bigquery/github_models/pull_request_features"),
            twirl.Input("bigquery/github_models/pr_closing_time_outcomes"),
            twirl.Input("bigquery/github_models/repository_features"),
            twirl.Input("bigquery/github_models/user_features"),
        ],
        job=twirl.PythonJob(
            update_method=twirl.UpdateMethod.MERGE,
            resource_config=twirl.CloudRunResourceConfig(cpu_count=1, memory="1Gi"),
        ),
        trigger_conditions=twirl.TriggerWhenAllInputsUpdated(at_most_every=timedelta(days=7)),
        freshness=twirl.Freshness(
            check_at="0 0 * * *",
            max_age=timedelta(days=8),
        ),
        tags=["engineering", "github_predictions"],
    )
)
