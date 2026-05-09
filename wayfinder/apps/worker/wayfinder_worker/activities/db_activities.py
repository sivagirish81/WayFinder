from temporalio import activity


@activity.defn
async def initialize_trip_run_activity(payload: dict) -> dict:
    return {"trip_run_id": payload.get("trip_run_id"), "status": "received"}
