"""create core tables

Revision ID: 0001_create_core_tables
Revises:
Create Date: 2026-05-09
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_create_core_tables"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def uuid_pk() -> sa.Column:
    return sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True)


def timestamps() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    ]


def upgrade() -> None:
    op.create_table(
        "trip_runs",
        uuid_pk(),
        sa.Column("source", sa.Text()),
        sa.Column("original_request", sa.Text(), nullable=False),
        sa.Column("requester_user_id", sa.Text()),
        sa.Column("slack_channel_id", sa.Text()),
        sa.Column("slack_thread_ts", sa.Text()),
        sa.Column("destination", sa.Text()),
        sa.Column("dates", sa.Text()),
        sa.Column("duration_days", sa.Integer()),
        sa.Column("group_size", sa.Integer()),
        sa.Column("expected_participant_count", sa.Integer()),
        sa.Column("participant_count", sa.Integer(), server_default="0"),
        sa.Column("budget_per_person", sa.Numeric(10, 2)),
        sa.Column("preferences", postgresql.JSONB(), server_default="{}"),
        sa.Column("constraints", postgresql.JSONB(), server_default="{}"),
        sa.Column("merged_group_preferences", postgresql.JSONB(), server_default="{}"),
        sa.Column("preference_conflicts", postgresql.JSONB(), server_default="[]"),
        sa.Column("planning_rules", postgresql.JSONB(), server_default="{}"),
        sa.Column("candidate_places", postgresql.JSONB(), server_default="[]"),
        sa.Column("ranked_places", postgresql.JSONB(), server_default="[]"),
        sa.Column("open_data_attribution", sa.Text()),
        sa.Column("preference_collection_status", sa.Text()),
        sa.Column("preference_collection_deadline", sa.DateTime()),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("temporal_workflow_id", sa.Text()),
        sa.Column("trace_id", sa.Text()),
        sa.Column("notion_page_id", sa.Text()),
        sa.Column("notion_page_url", sa.Text()),
        *timestamps(),
    )
    op.create_table("users", uuid_pk(), sa.Column("external_user_id", sa.Text(), unique=True), sa.Column("display_name", sa.Text()), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("trip_participants", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("slack_user_id", sa.Text()), sa.Column("display_name", sa.Text()), sa.Column("first_seen_at", sa.DateTime(), server_default=sa.func.now()), sa.Column("last_seen_at", sa.DateTime(), server_default=sa.func.now()), sa.UniqueConstraint("trip_run_id", "slack_user_id", name="uq_participant_user"))
    op.create_table("trip_messages", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("sender_id", sa.Text()), sa.Column("channel_id", sa.Text()), sa.Column("message_ts", sa.Text()), sa.Column("raw_text", sa.Text()), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("trip_questions", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("question_text", sa.Text()), sa.Column("status", sa.Text()), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("trip_preference_responses", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("participant_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_participants.id")), sa.Column("slack_message_ts", sa.Text()), sa.Column("raw_text", sa.Text()), sa.Column("parsed_preferences", postgresql.JSONB(), server_default="{}"), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("trip_preference_summary", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("merged_preferences", postgresql.JSONB(), server_default="{}"), sa.Column("conflicts", postgresql.JSONB(), server_default="[]"), sa.Column("planning_rules", postgresql.JSONB(), server_default="{}"), sa.Column("participant_count", sa.Integer(), server_default="0"), *timestamps())
    op.create_table("trip_itineraries", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("itinerary", postgresql.JSONB(), server_default="{}"), sa.Column("status", sa.Text()), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("trip_budget_estimates", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("estimate", postgresql.JSONB(), server_default="{}"), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("travel_place_cache", uuid_pk(), sa.Column("destination", sa.Text()), sa.Column("provider", sa.Text()), sa.Column("query_hash", sa.Text()), sa.Column("raw_response", postgresql.JSONB(), server_default="{}"), sa.Column("normalized_places", postgresql.JSONB(), server_default="[]"), sa.Column("attribution", sa.Text()), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()), sa.Column("expires_at", sa.DateTime()))
    op.create_table("approval_requests", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("approval_type", sa.Text()), sa.Column("status", sa.Text()), sa.Column("original_payload", postgresql.JSONB(), server_default="{}"), sa.Column("revised_payload", postgresql.JSONB()), sa.Column("requested_by", sa.Text()), sa.Column("reviewed_by", sa.Text()), sa.Column("reviewer_comment", sa.Text()), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()), sa.Column("reviewed_at", sa.DateTime()))
    op.create_table("tool_calls", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("tool_name", sa.Text()), sa.Column("tool_version", sa.Text()), sa.Column("integration_name", sa.Text()), sa.Column("input", postgresql.JSONB(), server_default="{}"), sa.Column("output", postgresql.JSONB()), sa.Column("status", sa.Text()), sa.Column("error", sa.Text()), sa.Column("idempotency_key", sa.Text()), sa.Column("started_at", sa.DateTime(), server_default=sa.func.now()), sa.Column("completed_at", sa.DateTime()), sa.Column("trace_id", sa.Text()), sa.Column("span_id", sa.Text()))
    op.create_table("langgraph_node_events", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("node_name", sa.Text()), sa.Column("input_state", postgresql.JSONB(), server_default="{}"), sa.Column("output_state", postgresql.JSONB(), server_default="{}"), sa.Column("status", sa.Text()), sa.Column("error", sa.Text()), sa.Column("started_at", sa.DateTime(), server_default=sa.func.now()), sa.Column("completed_at", sa.DateTime()), sa.Column("trace_id", sa.Text()), sa.Column("span_id", sa.Text()))
    op.create_table("temporal_workflow_events", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("temporal_workflow_id", sa.Text()), sa.Column("event_type", sa.Text()), sa.Column("event_summary", sa.Text()), sa.Column("details", postgresql.JSONB(), server_default="{}"), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("audit_events", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("event_type", sa.Text()), sa.Column("actor_type", sa.Text()), sa.Column("actor_id", sa.Text()), sa.Column("details", postgresql.JSONB(), server_default="{}"), sa.Column("trace_id", sa.Text()), sa.Column("span_id", sa.Text()), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("provenance_records", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("artifact_type", sa.Text()), sa.Column("artifact_id", sa.Text()), sa.Column("source_tool_call_ids", postgresql.JSONB(), server_default="[]"), sa.Column("source_slack_message_ids", postgresql.JSONB(), server_default="[]"), sa.Column("participant_ids", postgresql.JSONB(), server_default="[]"), sa.Column("openstreetmap_element_ids", postgresql.JSONB(), server_default="[]"), sa.Column("wikidata_qids", postgresql.JSONB()), sa.Column("wikivoyage_page_titles", postgresql.JSONB()), sa.Column("model_name", sa.Text()), sa.Column("prompt_version", sa.Text()), sa.Column("integration_versions", postgresql.JSONB(), server_default="{}"), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("notion_documents", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("notion_page_id", sa.Text()), sa.Column("notion_page_url", sa.Text()), sa.Column("status", sa.Text()), sa.Column("payload", postgresql.JSONB(), server_default="{}"), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("slack_messages", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("channel_id", sa.Text()), sa.Column("thread_ts", sa.Text()), sa.Column("message_ts", sa.Text()), sa.Column("text", sa.Text()), sa.Column("payload", postgresql.JSONB(), server_default="{}"), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("integration_events", uuid_pk(), sa.Column("trip_run_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("trip_runs.id")), sa.Column("integration_name", sa.Text()), sa.Column("event_type", sa.Text()), sa.Column("details", postgresql.JSONB(), server_default="{}"), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))


def downgrade() -> None:
    for table in [
        "integration_events", "slack_messages", "notion_documents", "provenance_records",
        "audit_events", "temporal_workflow_events", "langgraph_node_events", "tool_calls",
        "approval_requests", "travel_place_cache", "trip_budget_estimates", "trip_itineraries",
        "trip_preference_summary", "trip_preference_responses", "trip_questions", "trip_messages",
        "trip_participants", "users", "trip_runs",
    ]:
        op.drop_table(table)
