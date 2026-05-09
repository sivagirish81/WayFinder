from temporalio import activity


@activity.defn
async def send_reminder_activity(payload: dict) -> dict:
    return {"status": "reminder_sent", "payload": payload}
