from datetime import timedelta

import twirl

twirl.manifest(
    twirl.FileCollection(
        job=twirl.External(),
        trigger_conditions=twirl.TriggerWithoutInputs(once_every=timedelta(hours=1)),
        tags=["legal"],
    )
)
