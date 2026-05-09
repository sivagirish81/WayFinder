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
