from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "wayfinder-api"


class TripCreateRequest(BaseModel):
    original_request: str = Field(min_length=3)
    source: str = "manual"


class TripResponse(BaseModel):
    id: UUID
    source: str
    original_request: str
    status: str
    temporal_workflow_id: str | None = None
    trace_id: str | None = None
    created_at: datetime | None = None


class ParticipantPreferenceRequest(BaseModel):
    name: str
    preference_text: str = Field(min_length=1)
    slack_user_id: str | None = None


class ApprovalDecisionRequest(BaseModel):
    reviewer_id: str = "dashboard"
    comment: str | None = None


class ChangeRequest(BaseModel):
    reviewer_id: str = "dashboard"
    requested_changes: str = Field(min_length=1)


class AuditEventResponse(BaseModel):
    event_type: str
    actor_type: str
    details: dict = Field(default_factory=dict)
    created_at: datetime
