from datetime import timedelta

import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("ds", twirl.Date()),
                twirl.Column("yhat", twirl.Float()),
                twirl.Column("yhat_lower", twirl.Float()),
                twirl.Column("yhat_upper", twirl.Float()),
                twirl.Column("product_id", twirl.String()),
            ]
        ),
        job=twirl.PythonJob(twirl.UpdateMethod.REPLACE),
        trigger_conditions=twirl.TriggerWhenAllInputsUpdated(at_most_every=timedelta(hours=12)),
        inputs=[twirl.Input("fct_product_performance")],
        tags=['ecommerce']
    )
)
