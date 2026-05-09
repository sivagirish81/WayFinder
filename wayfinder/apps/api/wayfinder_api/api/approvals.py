from fastapi import APIRouter

router = APIRouter(prefix="/api/approvals", tags=["approvals"])


@router.get("")
async def approvals() -> list[dict]:
    return []


@router.get("/pending")
async def pending_approvals() -> list[dict]:
    return []
