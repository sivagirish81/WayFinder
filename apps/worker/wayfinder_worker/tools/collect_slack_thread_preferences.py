from pydantic import BaseModel, Field

from wayfinder_worker.tools.base import RiskLevel, ToolMetadata, WayfinderTool


class CollectSlackThreadPreferencesInput(BaseModel):
    slack_channel_id: str
    slack_thread_ts: str
    trip_run_id: str


class CollectSlackThreadPreferencesOutput(BaseModel):
    participant_responses: list[dict] = Field(default_factory=list)
    participant_count: int = 0
    latest_response_timestamp: str | None = None


collect_slack_thread_preferences = WayfinderTool(
    metadata=ToolMetadata(
        name="collect_slack_thread_preferences",
        description="Collect Slack thread replies and group them by user.",
        risk_level=RiskLevel.low,
        idempotency="Slack channel plus thread timestamp plus latest message timestamp.",
        integration_name="slack",
    ),
    input_schema=CollectSlackThreadPreferencesInput,
    output_schema=CollectSlackThreadPreferencesOutput,
)
