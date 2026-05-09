from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["traces"])


@router.get("/trips/{trip_id}/trace-link")
async def trace_link(trip_id: str) -> dict:
    return {
        "trip_id": trip_id,
        "trace_url": f"http://localhost:16686/search?service=wayfinder&tags=%7B%22trip_id%22%3A%22{trip_id}%22%7D",
    }
