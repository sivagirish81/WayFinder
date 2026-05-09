from fastapi import APIRouter

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("/events")
async def audit_events() -> list[dict]:
    return []
