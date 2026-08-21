from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def check() -> dict[str, str]:
    return { "status": "ok" }