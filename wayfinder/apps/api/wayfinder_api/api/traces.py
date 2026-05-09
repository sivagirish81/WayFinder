from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["traces"])


@router.get("/trips/{trip_id}/trace-link")
async def trace_link(trip_id: str) -> dict:
    return {"trip_id": trip_id, "trace_url": None}
