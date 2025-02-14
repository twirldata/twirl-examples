import twirl

twirl.manifest(
    twirl.Action(
        job=twirl.ContainerJob(), # Using a container job to simplify dependency handling
        trigger_conditions=twirl.TriggerAt(cron_string="0 0 * * MON"),
        tags=["vertex"],
    )
)
