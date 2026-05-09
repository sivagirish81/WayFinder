from datetime import datetime
from uuid import uuid4

APPROVALS: dict[str, dict] = {}


async def create_approval(trip_id: str, payload: dict) -> dict:
    approval_id = str(uuid4())
    approval = {
        "id": approval_id,
        "trip_run_id": trip_id,
        "status": "pending",
        "original_payload": payload,
        "created_at": datetime.utcnow().isoformat(),
    }
    APPROVALS[approval_id] = approval
    return approval


async def list_approvals(status: str | None = None) -> list[dict]:
    values = list(APPROVALS.values())
    if status:
        return [item for item in values if item["status"] == status]
    return values


async def decide_approval(approval_id: str, status: str, comment: str | None = None) -> dict:
    approval = APPROVALS.setdefault(
        approval_id,
        {"id": approval_id, "trip_run_id": "unknown", "original_payload": {}, "created_at": datetime.utcnow().isoformat()},
    )
    approval["status"] = status
    approval["reviewer_comment"] = comment
    approval["reviewed_at"] = datetime.utcnow().isoformat()
    return approval
