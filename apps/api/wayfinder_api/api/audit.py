from fastapi import APIRouter

from wayfinder_api.services.audit_service import list_audit_events

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("/events")
async def audit_events() -> list[dict]:
    return await list_audit_events()
