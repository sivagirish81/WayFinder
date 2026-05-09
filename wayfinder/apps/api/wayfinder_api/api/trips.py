from fastapi import APIRouter, status

from wayfinder_api.schemas import ParticipantPreferenceRequest, TripCreateRequest, TripResponse
from wayfinder_api.services.demo_input_service import add_manual_preference, get_preferences
from wayfinder_api.services.provenance_service import list_provenance
from wayfinder_api.services.temporal_client import start_trip_workflow

router = APIRouter(prefix="/api/trips", tags=["trips"])


@router.post("", response_model=TripResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_trip(payload: TripCreateRequest) -> TripResponse:
    return await start_trip_workflow(payload)


@router.get("")
async def list_trips() -> list[dict]:
    return []


@router.get("/{trip_id}")
async def get_trip(trip_id: str) -> dict:
    return {"id": trip_id, "status": "received"}


@router.get("/{trip_id}/timeline")
async def timeline(trip_id: str) -> list[dict]:
    return [{"trip_id": trip_id, "event_type": "TRIP_REQUEST_RECEIVED"}]


@router.get("/{trip_id}/state")
async def state(trip_id: str) -> dict:
    return {"trip_id": trip_id, "status": "received"}


@router.get("/{trip_id}/participants")
async def participants(trip_id: str) -> list[dict]:
    return [{"trip_id": trip_id, "name": item["name"]} for item in await get_preferences(trip_id)]


@router.get("/{trip_id}/preferences")
async def preferences(trip_id: str) -> list[dict]:
    return await get_preferences(trip_id)


@router.post("/{trip_id}/preferences")
async def add_preference(trip_id: str, payload: ParticipantPreferenceRequest) -> dict:
    return await add_manual_preference(trip_id, payload.name, payload.preference_text)


@router.get("/{trip_id}/candidate-places")
async def candidate_places(trip_id: str) -> list[dict]:
    return []


@router.get("/{trip_id}/ranked-places")
async def ranked_places(trip_id: str) -> list[dict]:
    return []


@router.get("/{trip_id}/tool-calls")
async def tool_calls(trip_id: str) -> list[dict]:
    return []


@router.get("/{trip_id}/langgraph-events")
async def langgraph_events(trip_id: str) -> list[dict]:
    return []


@router.get("/{trip_id}/temporal-events")
async def temporal_events(trip_id: str) -> list[dict]:
    return []


@router.get("/{trip_id}/audit")
async def trip_audit(trip_id: str) -> list[dict]:
    return []


@router.get("/{trip_id}/provenance")
async def provenance(trip_id: str) -> list[dict]:
    return await list_provenance(trip_id)


@router.post("/{trip_id}/clarifications")
async def clarification(trip_id: str, payload: dict) -> dict:
    return {"trip_id": trip_id, "accepted": True, "payload": payload}


@router.post("/{trip_id}/continue")
async def continue_trip(trip_id: str) -> dict:
    return {"trip_id": trip_id, "signal": "continue_with_current_preferences"}


@router.post("/{trip_id}/cancel")
async def cancel_trip(trip_id: str, payload: dict | None = None) -> dict:
    return {"trip_id": trip_id, "signal": "cancel_run", "payload": payload or {}}
