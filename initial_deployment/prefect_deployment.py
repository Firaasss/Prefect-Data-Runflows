from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/Firaasss/Prefect-Data-Runflows.git",
        entrypoint="initial_deployment/echo.py:echo",
    ).deploy(
        name="my-first-deployment",
        work_pool_name="my-managed-pool",
        cron="0 1 * * *",
    )