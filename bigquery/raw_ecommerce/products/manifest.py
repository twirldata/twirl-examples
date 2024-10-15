from datetime import timedelta

import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column(name="product_id", type=twirl.String(), is_primary_key=True),
                twirl.Column(name="name", type=twirl.String()),
                twirl.Column(name="category", type=twirl.String()),
                twirl.Column(name="price", type=twirl.Float()),
            ]
        ),
        job=twirl.PythonJob(update_method=twirl.UpdateMethod.MERGE, secrets=[twirl.SecretId("mock-db-url")]),
        tags=["ecommerce"],
        trigger_conditions=twirl.TriggerWithoutInputs(once_every=timedelta(hours=1)),
    )
)
