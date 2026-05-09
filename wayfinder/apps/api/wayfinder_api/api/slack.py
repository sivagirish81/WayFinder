from fastapi import APIRouter, Header, HTTPException, Request

from wayfinder_api.config import get_settings
from wayfinder_api.schemas import TripCreateRequest
from wayfinder_api.services.slack_service import parse_wayfinder_command, validate_slack_signature
from wayfinder_api.services.temporal_client import start_trip_workflow

router = APIRouter(prefix="/api/slack", tags=["slack"])


@router.post("/events")
async def slack_events(
    request: Request,
    x_slack_request_timestamp: str | None = Header(default=None),
    x_slack_signature: str | None = Header(default=None),
) -> dict:
    body = await request.body()
    settings = get_settings()
    if settings.slack_signing_secret and not validate_slack_signature(
        settings.slack_signing_secret,
        x_slack_request_timestamp or "",
        body,
        x_slack_signature or "",
    ):
        raise HTTPException(status_code=401, detail="Invalid Slack signature")
    payload = await request.json()
    if payload.get("type") == "url_verification":
        return {"challenge": payload.get("challenge")}
    event = payload.get("event", {})
    command = parse_wayfinder_command(event.get("text", ""))
    if command:
        trip = await start_trip_workflow(
            TripCreateRequest(
                original_request=command,
                source="slack_mention",
            )
        )
        return {"ok": True, "trip_id": str(trip.id)}
    return {"ok": True}


@router.post("/interactions")
async def slack_interactions() -> dict:
    return {"ok": True}


@router.post("/commands")
async def slack_commands() -> dict:
    return {"ok": True}
