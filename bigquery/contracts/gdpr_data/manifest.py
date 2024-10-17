from datetime import timedelta

import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("file_name", twirl.String(), is_primary_key=True),
                twirl.Column("gdpr_pages", twirl.Array(value_type=twirl.Integer())),
            ]
        ),
        inputs=[
            twirl.Input("bigquery/contracts/contract_text"),
        ],
        job=twirl.BigQueryJob(update_method=twirl.UpdateMethod.REPLACE),
        tags=["legal"],
        freshness=twirl.Freshness(
            check_at="0 15 * * *",
            max_age=timedelta(minutes=10),
        ),
    )
)
