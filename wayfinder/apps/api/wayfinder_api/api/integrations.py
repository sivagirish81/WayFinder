from fastapi import APIRouter

from wayfinder_api.services.integration_status_service import get_integration_status

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


@router.get("/status")
async def integration_status() -> dict:
    return await get_integration_status()


@router.get("/tools")
async def tools() -> list[dict]:
    return []


@router.get("/tools/{tool_name}")
async def tool_detail(tool_name: str) -> dict:
    return {"name": tool_name, "status": "not_registered_yet"}
