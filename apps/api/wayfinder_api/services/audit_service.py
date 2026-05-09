from datetime import datetime

AUDIT_EVENTS: list[dict] = []


async def write_audit_event(
    event_type: str,
    actor_type: str = "system",
    details: dict | None = None,
    trip_run_id: str | None = None,
) -> dict:
    event = {
        "trip_run_id": trip_run_id,
        "event_type": event_type,
        "actor_type": actor_type,
        "details": details or {},
        "created_at": datetime.utcnow().isoformat(),
    }
    AUDIT_EVENTS.append(event)
    return event


async def list_audit_events() -> list[dict]:
    return AUDIT_EVENTS
