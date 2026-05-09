from pydantic import BaseModel, Field

from wayfinder_worker.tools.base import RiskLevel, ToolMetadata, WayfinderTool


class RankCandidatePlacesInput(BaseModel):
    candidate_places: list[dict] = Field(default_factory=list)
    merged_preferences: dict = Field(default_factory=dict)
    constraints: dict = Field(default_factory=dict)
    budget_per_person: float | None = None


class RankCandidatePlacesOutput(BaseModel):
    ranked_places: list[dict] = Field(default_factory=list)
    ranking_explanation: str = ""


rank_candidate_places = WayfinderTool(
    metadata=ToolMetadata(
        name="rank_candidate_places",
        description="Rank places based on preferences, budget, pace, constraints, and category match.",
        risk_level=RiskLevel.low,
        idempotency="Candidate place IDs plus preference summary ID.",
        integration_name="wayfinder",
    ),
    input_schema=RankCandidatePlacesInput,
    output_schema=RankCandidatePlacesOutput,
)
