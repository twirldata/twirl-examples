import twirl

twirl.manifest(
    twirl.Action(
        job=twirl.PythonJob(twirl.UpdateMethod.NONE),
        trigger_conditions=twirl.TriggerAt(cron_string="0 0 * * MON-FRI"),
        inputs=[
            twirl.Input("dim_customers"),
            twirl.Input("dim_products"),
            twirl.Input("fct_product_performance"),
        ],
        tags=["ecommerce"],
    )
)
