from pydantic import BaseModel, Field

from wayfinder_worker.tools.base import ApprovalBehavior, RiskLevel, ToolMetadata, WayfinderTool


class UpdateNotionTripDocInput(BaseModel):
    notion_page_id: str
    content: dict = Field(default_factory=dict)
    mark_final: bool = False
    idempotency_key: str


class UpdateNotionTripDocOutput(BaseModel):
    notion_page_id: str
    status: str


update_notion_trip_doc = WayfinderTool(
    metadata=ToolMetadata(
        name="update_notion_trip_doc",
        description="Update a Notion page after revisions or final approval.",
        risk_level=RiskLevel.medium,
        approval=ApprovalBehavior(required=True, reason="Required when marking final."),
        idempotency="Notion page ID plus content version.",
        integration_name="notion",
    ),
    input_schema=UpdateNotionTripDocInput,
    output_schema=UpdateNotionTripDocOutput,
)
