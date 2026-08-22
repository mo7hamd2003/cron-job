import inngest
import logging


inngest_client = inngest.Inngest(
    app_id="report_api",
    logger=logging.getLogger("uvicorn"),
)