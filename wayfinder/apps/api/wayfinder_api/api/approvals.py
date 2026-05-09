from fastapi import APIRouter

from wayfinder_api.schemas import ApprovalDecisionRequest, ChangeRequest
from wayfinder_api.services.approval_service import decide_approval, list_approvals

router = APIRouter(prefix="/api/approvals", tags=["approvals"])


@router.get("")
async def approvals() -> list[dict]:
    return await list_approvals()


@router.get("/pending")
async def pending_approvals() -> list[dict]:
    return await list_approvals(status="pending")


@router.get("/{approval_id}")
async def get_approval(approval_id: str) -> dict:
    matches = [item for item in await list_approvals() if item["id"] == approval_id]
    return matches[0] if matches else {"id": approval_id, "status": "not_found"}


@router.post("/{approval_id}/approve")
async def approve(approval_id: str, payload: ApprovalDecisionRequest) -> dict:
    return await decide_approval(approval_id, "approved", payload.comment)


@router.post("/{approval_id}/reject")
async def reject(approval_id: str, payload: ApprovalDecisionRequest) -> dict:
    return await decide_approval(approval_id, "rejected", payload.comment)


@router.post("/{approval_id}/request-changes")
async def request_changes(approval_id: str, payload: ChangeRequest) -> dict:
    return await decide_approval(approval_id, "changes_requested", payload.requested_changes)
