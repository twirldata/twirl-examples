import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("file_name", twirl.String(), is_primary_key=True),
                twirl.Column("page_num", twirl.Integer(), is_primary_key=True),
                twirl.Column("page_text", twirl.String()),
            ]
        ),
        inputs=[
            twirl.Input("gcs/contracts"),
        ],
        job=twirl.PythonJob(update_method=twirl.UpdateMethod.REPLACE),
        tags=["legal"],
    )
)
