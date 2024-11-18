import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("date", twirl.TimestampWithoutZone(unit="us")),
                twirl.Column("sends", twirl.Integer()),
            ]
        ),
        job=twirl.PythonJob(twirl.UpdateMethod.APPEND),
        trigger_conditions=twirl.TriggerAt(cron_string="0 0 * * MON-FRI"),
        inputs=[
            twirl.Input("dim_customers"),
            twirl.Input("dim_products"),
            twirl.Input("fct_product_performance"),
        ],
        tags=["ecommerce"],
    )
)
