from datetime import datetime
from uuid import uuid4

from wayfinder_api.schemas import TripCreateRequest, TripResponse


async def start_trip_workflow(payload: TripCreateRequest) -> TripResponse:
    trip_id = uuid4()
    workflow_id = f"trip-planning-{trip_id}"
    return TripResponse(
        id=trip_id,
        source=payload.source,
        original_request=payload.original_request,
        status="received",
        temporal_workflow_id=workflow_id,
        created_at=datetime.utcnow(),
    )
