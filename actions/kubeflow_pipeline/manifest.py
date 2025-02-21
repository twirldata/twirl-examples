import twirl

twirl.manifest(
    twirl.Action(
        job=twirl.KubeflowJob(pipeline_name="census_pipeline"),
        trigger_conditions=twirl.TriggerAt(cron_string="0 0 * * MON"),
        tags=["vertex"],
    )
)
