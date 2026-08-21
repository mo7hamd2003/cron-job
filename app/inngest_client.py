import inngest
import logging

# Create an Inngest client
inngest_client = inngest.Inngest(
    app_id="report_api",
    logger=logging.getLogger("uvicorn"),
)