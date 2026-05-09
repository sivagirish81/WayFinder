from pydantic import BaseModel, Field

from wayfinder_worker.tools.base import RiskLevel, ToolMetadata, WayfinderTool


class DetectPreferenceConflictsInput(BaseModel):
    per_user_preferences: dict = Field(default_factory=dict)
    merged_preferences: dict = Field(default_factory=dict)


class DetectPreferenceConflictsOutput(BaseModel):
    conflicts: list[dict] = Field(default_factory=list)
    suggested_tradeoffs: list[str] = Field(default_factory=list)
    planning_rules: dict = Field(default_factory=dict)


detect_preference_conflicts = WayfinderTool(
    metadata=ToolMetadata(
        name="detect_preference_conflicts",
        description="Identify conflicts and tradeoffs across group preferences.",
        risk_level=RiskLevel.low,
        idempotency="Normalized preference summary ID plus prompt version.",
        integration_name="openai",
    ),
    input_schema=DetectPreferenceConflictsInput,
    output_schema=DetectPreferenceConflictsOutput,
)
