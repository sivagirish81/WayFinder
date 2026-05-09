from pydantic import BaseModel, Field

from wayfinder_worker.tools.base import ApprovalBehavior, RiskLevel, ToolMetadata, WayfinderTool


class PostSlackMessageInput(BaseModel):
    channel_id: str
    text: str
    thread_ts: str | None = None
    blocks: list[dict] = Field(default_factory=list)
    idempotency_key: str


class PostSlackMessageOutput(BaseModel):
    channel_id: str
    message_ts: str | None = None


post_slack_message = WayfinderTool(
    metadata=ToolMetadata(
        name="post_slack_message",
        description="Post questions, summaries, reminders, and final messages to Slack.",
        risk_level=RiskLevel.medium,
        approval=ApprovalBehavior(required=True, reason="Required for final group announcement."),
        idempotency="Slack channel, thread timestamp, purpose, and content hash.",
        integration_name="slack",
    ),
    input_schema=PostSlackMessageInput,
    output_schema=PostSlackMessageOutput,
)
