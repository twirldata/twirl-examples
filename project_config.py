import twirl

twirl.project_config(
    project_name="twirl-demo",
    secrets=[
        twirl.EnvironmentSecrets(),
        twirl.GcpSecrets(gcp_project="twirldata-demo"),
    ],
    datastores=[
        twirl.BigQueryDatastore(
            name="bigquery",
            gcp_project_id="twirldata-demo",
            gcp_location="europe-west1",
        ),
        twirl.GcsDatastore(
            name="gcs",
            gcp_project_id="twirldata-demo",
            gcs_bucket_name="twirldata-demo",
        ),
    ],
    container_registry=twirl.GcpContainerRegistry(
        gcp_region="europe-west1",
        registry_host="europe-west1-docker.pkg.dev",
        gcp_project="twirldata-demo",
        registry_path="twirl",
    ),
    cloud_runtime=twirl.GcpCloudRuntime(
        project="twirldata-demo",
        location="europe-west1",
        job_runner_account="twirl-runner@twirldata-demo.iam.gserviceaccount.com",
        job_manager_account="twirl-job-manager@twirldata-demo.iam.gserviceaccount.com",
        default_job_resource_config=twirl.CloudRunResourceConfig(memory="1Gi", cpu_count=1),
    ),
    notify_on_failure=True,
    notify_on_success=False,
    dbt=twirl.DbtConfig(project_dir="dbt"),
)
