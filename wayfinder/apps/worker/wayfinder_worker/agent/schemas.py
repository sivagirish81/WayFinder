from pydantic import BaseModel, Field


class Question(BaseModel):
    id: str
    text: str


class PlaceCandidate(BaseModel):
    id: str
    name: str
    category: str
    source: str
    attribution: str = "© OpenStreetMap contributors"


class ApprovalSummary(BaseModel):
    approval_id: str
    status: str = "pending"
    proposed_payload: dict = Field(default_factory=dict)
