from pydantic import BaseModel, Field

from wayfinder_worker.tools.base import RiskLevel, ToolMetadata, WayfinderTool


class GenerateItineraryInput(BaseModel):
    destination: str
    duration_days: int
    merged_preferences: dict = Field(default_factory=dict)
    conflicts: list[dict] = Field(default_factory=list)
    ranked_places: list[dict] = Field(default_factory=list)
    budget_per_person: float | None = None


class GenerateItineraryOutput(BaseModel):
    itinerary: dict = Field(default_factory=dict)
    slack_summary: str = ""


generate_itinerary = WayfinderTool(
    metadata=ToolMetadata(
        name="generate_itinerary",
        description="Create a draft day-by-day itinerary using group preferences and open-data places.",
        risk_level=RiskLevel.medium,
        idempotency="Trip state hash plus prompt version.",
        integration_name="openai",
    ),
    input_schema=GenerateItineraryInput,
    output_schema=GenerateItineraryOutput,
)
