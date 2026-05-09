from pydantic import BaseModel

from wayfinder_worker.tools.base import RiskLevel, ToolMetadata, WayfinderTool


class ExportMarkdownPlanInput(BaseModel):
    trip_run_id: str
    markdown: str


class ExportMarkdownPlanOutput(BaseModel):
    artifact_id: str | None = None
    status: str = "stored"


export_markdown_plan = WayfinderTool(
    metadata=ToolMetadata(
        name="export_markdown_plan",
        description="Save a local or database-backed markdown copy of the itinerary.",
        risk_level=RiskLevel.low,
        idempotency="Trip run ID plus markdown content hash.",
        integration_name="wayfinder",
    ),
    input_schema=ExportMarkdownPlanInput,
    output_schema=ExportMarkdownPlanOutput,
)
