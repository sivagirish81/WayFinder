from pydantic import BaseModel, Field

from wayfinder_worker.tools.base import RiskLevel, ToolMetadata, WayfinderTool


class CreateNotionTripDocInput(BaseModel):
    trip_run_id: str
    title: str
    content: dict = Field(default_factory=dict)
    idempotency_key: str


class CreateNotionTripDocOutput(BaseModel):
    notion_page_id: str | None = None
    notion_page_url: str | None = None
    status: str = "draft"


create_notion_trip_doc = WayfinderTool(
    metadata=ToolMetadata(
        name="create_notion_trip_doc",
        description="Create a draft Notion trip document.",
        risk_level=RiskLevel.medium,
        idempotency="Trip run ID scoped Notion page creation key.",
        integration_name="notion",
    ),
    input_schema=CreateNotionTripDocInput,
    output_schema=CreateNotionTripDocOutput,
)
