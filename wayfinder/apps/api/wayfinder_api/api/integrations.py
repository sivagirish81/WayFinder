from fastapi import APIRouter

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


@router.get("/status")
async def integration_status() -> dict:
    return {
        "openai": "not_configured",
        "slack": "not_configured",
        "notion": "not_configured",
        "temporal": "configured",
        "postgresql": "configured",
        "jaeger": "configured",
        "openstreetmap_overpass": "configured",
    }


@router.get("/tools")
async def tools() -> list[dict]:
    return []
