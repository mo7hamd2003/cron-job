import datetime
import inngest

from app.routes.client import inngest_client
from app.storage import load_report, save_report, load_all_reports


@inngest_client.create_function(
    fn_id="make-report",
    trigger=inngest.TriggerEvent(event="report/requested"),
)
async def make_report(ctx: inngest.Context) -> dict[str, str]:
    """Make a report based on the event data."""

    await ctx.step.sleep("do-the-slow-work", datetime.timedelta(seconds=8))

    async def build_report() -> dict[str, str]:
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

@inngest_client.create_function(
    fn_id="heartbeat",
    trigger=inngest.TriggerCron(cron="TZ=UTC * * * * *")
)
async def heartbeat(ctx: inngest.Context) -> dict[str, int]:
    """Send a heartbeat event to the Inngest server."""

    pending = 0
    done = 0
    fail = 0
    
    records = load_all_reports()
    for record in records:
        if record["topic"] == "fail":
            fail += 1

        if record["status"] == "pending":
            pending += 1
        elif record["status"] == "done":
            done += 1

    return { "Pending": pending, "Done": done, "Fail": fail }

@inngest_client.create_function(
    fn_id="say_hello",
    trigger=inngest.TriggerEvent(event="app/health.check"),
    retries=2,
)
async def say_hello(ctx: inngest.Context) -> str:
    """Send a greeting from the background."""

    await ctx.step.sleep("zzz", datetime.timedelta(seconds=5))
    ctx.logger.info(ctx.event)
    return "Hello from background!"
