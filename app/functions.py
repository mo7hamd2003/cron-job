import datetime
import inngest

from app.routes.client import inngest_client
from app.storage import load_report, save_report


@inngest_client.create_function(
    fn_id="make-report",
    trigger=inngest.TriggerEvent(event="report/requested"),
)
async def make_report(ctx: inngest.Context) -> dict:
    await ctx.step.sleep("do-the-slow-work", datetime.timedelta(seconds=8))

    async def build_report() -> dict:
            report_id = str(ctx.event.data["id"])
            topic = str(ctx.event.data["topic"])
        
            record = load_report(report_id)
            record["status"] = "done"
            record["result"] = f"Report on {topic}"
            save_report(record)
            return record 

    report_id = str(ctx.event.data["id"])
            
    record = load_report(report_id)
    if record["topic"] == "fail":
        raise Exception(f"The report oven is broken!")

    return await ctx.step.run("build-report", build_report)