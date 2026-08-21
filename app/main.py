from fastapi import FastAPI
from app.routes import health, client
from app.functions import make_report
from app.inngest_client import inngest_client

import logging
import inngest
import inngest.fast_api
import datetime



# Create an Inngest function
@inngest_client.create_function(
    fn_id="say_hello",
    trigger=inngest.TriggerEvent(event="app/health.check"),
)

async def say_hello(ctx: inngest.Context) -> str:
    await ctx.step.sleep("zzz", datetime.timedelta(seconds=5))
    ctx.logger.info(ctx.event)
    return "Hello from background!"

app = FastAPI()

app.include_router(health.router)
app.include_router(client.router)

inngest.fast_api.serve(app, inngest_client, [say_hello, make_report])