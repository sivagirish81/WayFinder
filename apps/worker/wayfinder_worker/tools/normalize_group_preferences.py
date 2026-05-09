from pydantic import BaseModel, Field

from wayfinder_worker.tools.base import RiskLevel, ToolMetadata, WayfinderTool


class NormalizeGroupPreferencesInput(BaseModel):
    participant_responses: list[dict] = Field(default_factory=list)


class NormalizeGroupPreferencesOutput(BaseModel):
    per_user_preferences: dict = Field(default_factory=dict)
    merged_preferences: dict = Field(default_factory=dict)
    dietary_constraints: list[str] = Field(default_factory=list)
    pace_preferences: list[str] = Field(default_factory=list)
    activity_preferences: list[str] = Field(default_factory=list)
    avoid_list: list[str] = Field(default_factory=list)
    budget_sensitivity: str | None = None


normalize_group_preferences = WayfinderTool(
    metadata=ToolMetadata(
        name="normalize_group_preferences",
        description="Convert multiple freeform replies into structured group preferences.",
        risk_level=RiskLevel.low,
        idempotency="Participant response IDs plus prompt version.",
        integration_name="openai",
    ),
    input_schema=NormalizeGroupPreferencesInput,
    output_schema=NormalizeGroupPreferencesOutput,
)
