import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("file_name", twirl.String(), is_primary_key=True),
                twirl.Column("page_num", twirl.Integer(), is_primary_key=True),
                twirl.Column("page_text", twirl.String()),
                twirl.Column("page_embedding", twirl.Array(value_type=twirl.Float())),
            ]
        ),
        inputs=[
            twirl.Input("bigquery/contracts/contract_text"),
        ],
        job=twirl.DataflowGroupByJob(
            update_method=twirl.UpdateMethod.REPLACE,
            group_by_key=["file_name"],
            order_by_key=["page_num"],
            resource_config=twirl.GcpBeamResourceConfig(
                worker_machine_type="n1-standard-2",
                worker_count=2,
                worker_max_count=4,
                autoscaling_algorithm="THROUGHPUT_BASED",
            )
        ),
        tags=["legal"],
    )
)
