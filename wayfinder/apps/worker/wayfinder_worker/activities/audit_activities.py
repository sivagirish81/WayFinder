from temporalio import activity


@activity.defn
async def write_audit_event_activity(payload: dict) -> dict:
    return {"status": "written", "event_type": payload.get("event_type")}
