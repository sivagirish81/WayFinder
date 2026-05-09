from pydantic import BaseModel, Field

from wayfinder_worker.tools.base import RiskLevel, ToolMetadata, WayfinderTool


class EstimateBudgetInput(BaseModel):
    destination: str
    duration_days: int
    group_size: int
    budget_per_person: float | None = None


class EstimateBudgetOutput(BaseModel):
    estimate: dict = Field(default_factory=dict)
    note: str = "Budget estimates are approximate."


estimate_budget = WayfinderTool(
    metadata=ToolMetadata(
        name="estimate_budget",
        description="Produce simple lodging, food, transport, activities, and buffer estimates.",
        risk_level=RiskLevel.medium,
        idempotency="Destination, duration, group size, and budget.",
        integration_name="wayfinder_openai",
    ),
    input_schema=EstimateBudgetInput,
    output_schema=EstimateBudgetOutput,
)
