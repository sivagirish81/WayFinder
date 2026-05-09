from temporalio import activity


@activity.defn
async def post_slack_message_activity(payload: dict) -> dict:
    idempotency_key = payload.get("idempotency_key")
    return {
        "channel_id": payload.get("channel_id"),
        "thread_ts": payload.get("thread_ts"),
        "message_ts": f"demo-{idempotency_key}",
        "idempotency_key": idempotency_key,
        "status": "sent",
    }


@activity.defn
async def collect_slack_thread_preferences_activity(payload: dict) -> dict:
    return {
        "trip_run_id": payload.get("trip_run_id"),
        "participant_responses": [],
        "participant_count": 0,
        "latest_response_timestamp": None,
    }
