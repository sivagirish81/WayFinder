from fastapi import APIRouter, status

from wayfinder_api.schemas import TripCreateRequest, TripResponse
from wayfinder_api.schemas import ParticipantPreferenceRequest
from wayfinder_api.services.demo_input_service import add_manual_preference
from wayfinder_api.services.temporal_client import start_trip_workflow

router = APIRouter(prefix="/api/demo", tags=["demo"])


@router.post("/trips", response_model=TripResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_demo_trip(payload: TripCreateRequest) -> TripResponse:
    payload.source = "manual_demo_input"
    return await start_trip_workflow(payload)


@router.post("/trips/{trip_id}/participant-preferences")
async def participant_preference(trip_id: str, payload: ParticipantPreferenceRequest) -> dict:
    return await add_manual_preference(trip_id, payload.name, payload.preference_text)
