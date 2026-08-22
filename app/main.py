from fastapi import FastAPI
from app.routes import health, client
from app.functions import make_report, say_hello, heartbeat
from app.inngest_client import inngest_client

import inngest
import inngest.fast_api

app = FastAPI()

app.include_router(health.router)
app.include_router(client.router)

inngest.fast_api.serve(app, inngest_client, [say_hello, make_report, heartbeat])