from fastapi import APIRouter, status
from pathlib import Path
from pydantic import BaseModel
from app.storage import save_report, load_report
from app.inngest_client import inngest_client
from fastapi import APIRouter, status, HTTPException

import json
import inngest
import uuid

router = APIRouter()

class ReportRequest(BaseModel):
    topic: str

class ReportResponse(BaseModel):
    id: str
    status: str

class ResponseStatus(BaseModel):
    status: str
    result: str

class ReportStatusResponse(BaseModel):
    status: str
    result: str | None = None

@router.post("/reports", status_code=status.HTTP_202_ACCEPTED, response_model=ReportResponse)
async def clinet_reports(payload: ReportRequest) -> ReportResponse:
    report_id = str(uuid.uuid4())

    record = { "id": report_id, "topic": payload.topic, "status": "pending" }

    save_report(record)

    await inngest_client.send(
        inngest.Event(
            name = "report/requested",
            data = { "id": report_id, "topic": payload.topic },
        )
    )
    return ReportResponse(id=report_id, status="pending")

@router.get("/reports/{report_id}", response_model=ReportStatusResponse)
async def get_report(report_id: str) -> ReportStatusResponse:
    try:
        record = load_report(report_id)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return ReportStatusResponse(**record)
