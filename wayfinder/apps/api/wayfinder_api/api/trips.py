from fastapi import APIRouter, status

from wayfinder_api.schemas import TripCreateRequest, TripResponse
from wayfinder_api.services.temporal_client import start_trip_workflow

router = APIRouter(prefix="/api/trips", tags=["trips"])


@router.post("", response_model=TripResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_trip(payload: TripCreateRequest) -> TripResponse:
    return await start_trip_workflow(payload)


@router.get("")
async def list_trips() -> list[dict]:
    return []
