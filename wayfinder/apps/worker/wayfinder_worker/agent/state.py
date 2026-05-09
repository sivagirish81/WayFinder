from pydantic import BaseModel, Field


class TripPlanState(BaseModel):
    original_request: str
    destination: str | None = None
    missing_fields: list[str] = Field(default_factory=list)
    messages: list[str] = Field(default_factory=list)
