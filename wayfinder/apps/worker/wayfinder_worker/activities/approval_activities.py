from temporalio import activity


@activity.defn
async def create_approval_request_activity(payload: dict) -> dict:
    return {"approval_id": f"approval-{payload.get('trip_run_id')}", "status": "pending"}
