from pydantic import BaseModel, Field

from wayfinder_worker.tools.base import RiskLevel, ToolMetadata, WayfinderTool


class GenerateFollowupQuestionsInput(BaseModel):
    missing_fields: list[str] = Field(default_factory=list)


class GenerateFollowupQuestionsOutput(BaseModel):
    questions: list[str] = Field(default_factory=list)


generate_followup_questions = WayfinderTool(
    metadata=ToolMetadata(
        name="generate_followup_questions",
        description="Ask only the most important missing trip-planning questions.",
        risk_level=RiskLevel.low,
        idempotency="Question set is keyed by missing fields and prompt version.",
        integration_name="openai",
    ),
    input_schema=GenerateFollowupQuestionsInput,
    output_schema=GenerateFollowupQuestionsOutput,
)
