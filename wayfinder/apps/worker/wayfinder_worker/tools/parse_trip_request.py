from pydantic import BaseModel, Field

from wayfinder_worker.tools.base import RiskLevel, ToolMetadata, WayfinderTool


class ParseTripRequestInput(BaseModel):
    original_request: str = Field(min_length=3)


class ParseTripRequestOutput(BaseModel):
    destination: str | None = None
    duration_days: int | None = None
    group_size: int | None = None
    budget_per_person: float | None = None
    preferences: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


parse_trip_request = WayfinderTool(
    metadata=ToolMetadata(
        name="parse_trip_request",
        description="Extract destination, dates, duration, group size, budget, preferences, and constraints.",
        risk_level=RiskLevel.low,
        idempotency="Deterministic per original request and prompt version.",
        integration_name="openai",
    ),
    input_schema=ParseTripRequestInput,
    output_schema=ParseTripRequestOutput,
)
