from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/slack", tags=["slack"])


@router.post("/events")
async def slack_events(request: Request) -> dict:
    return {"ok": True, "received": await request.json()}


@router.post("/interactions")
async def slack_interactions() -> dict:
    return {"ok": True}


@router.post("/commands")
async def slack_commands() -> dict:
    return {"ok": True}
