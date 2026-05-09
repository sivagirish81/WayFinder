from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TripPlanningRun(Base):
    __tablename__ = "trip_runs"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    source: Mapped[str] = mapped_column(String(40), default="manual")
    original_request: Mapped[str] = mapped_column(Text)
    requester_user_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    slack_channel_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    slack_thread_ts: Mapped[str | None] = mapped_column(String(80), nullable=True)
    destination: Mapped[str | None] = mapped_column(String(200), nullable=True)
    dates: Mapped[str | None] = mapped_column(String(200), nullable=True)
    duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    group_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    expected_participant_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    participant_count: Mapped[int] = mapped_column(Integer, default=0)
    budget_per_person: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(80), default="received")
    temporal_workflow_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    trace_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    preferences: Mapped[dict] = mapped_column(JSONB, default=dict)
    constraints: Mapped[dict] = mapped_column(JSONB, default=dict)
    merged_group_preferences: Mapped[dict] = mapped_column(JSONB, default=dict)
    preference_conflicts: Mapped[list] = mapped_column(JSONB, default=list)
    planning_rules: Mapped[dict] = mapped_column(JSONB, default=dict)
    candidate_places: Mapped[list] = mapped_column(JSONB, default=list)
    ranked_places: Mapped[list] = mapped_column(JSONB, default=list)
    open_data_attribution: Mapped[str | None] = mapped_column(Text, nullable=True)
    preference_collection_status: Mapped[str | None] = mapped_column(String(80), nullable=True)
    preference_collection_deadline: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    notion_page_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    notion_page_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    external_user_id: Mapped[str] = mapped_column(String(200), unique=True)
    display_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class TripParticipant(Base):
    __tablename__ = "trip_participants"
    __table_args__ = (UniqueConstraint("trip_run_id", "slack_user_id", name="uq_participant_user"),)

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    trip_run_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("trip_runs.id"))
    slack_user_id: Mapped[str] = mapped_column(String(200))
    display_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_seen_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class JsonEventMixin:
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    trip_run_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("trip_runs.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class TripMessage(JsonEventMixin, Base):
    __tablename__ = "trip_messages"

    sender_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    channel_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    message_ts: Mapped[str | None] = mapped_column(String(80), nullable=True)
    raw_text: Mapped[str] = mapped_column(Text)


class TripQuestion(JsonEventMixin, Base):
    __tablename__ = "trip_questions"

    question_text: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(80), default="pending")


class TripPreferenceResponse(JsonEventMixin, Base):
    __tablename__ = "trip_preference_responses"

    participant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("trip_participants.id"))
    slack_message_ts: Mapped[str | None] = mapped_column(String(80), nullable=True)
    raw_text: Mapped[str] = mapped_column(Text)
    parsed_preferences: Mapped[dict] = mapped_column(JSONB, default=dict)


class TripPreferenceSummary(Base):
    __tablename__ = "trip_preference_summary"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    trip_run_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("trip_runs.id"))
    merged_preferences: Mapped[dict] = mapped_column(JSONB, default=dict)
    conflicts: Mapped[list] = mapped_column(JSONB, default=list)
    planning_rules: Mapped[dict] = mapped_column(JSONB, default=dict)
    participant_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class TripItinerary(JsonEventMixin, Base):
    __tablename__ = "trip_itineraries"

    itinerary: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(80), default="draft")


class TripBudgetEstimate(JsonEventMixin, Base):
    __tablename__ = "trip_budget_estimates"

    estimate: Mapped[dict] = mapped_column(JSONB, default=dict)


class TravelPlaceCache(Base):
    __tablename__ = "travel_place_cache"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    destination: Mapped[str] = mapped_column(String(200))
    provider: Mapped[str] = mapped_column(String(80))
    query_hash: Mapped[str] = mapped_column(String(128))
    raw_response: Mapped[dict] = mapped_column(JSONB, default=dict)
    normalized_places: Mapped[list] = mapped_column(JSONB, default=list)
    attribution: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime)


class ApprovalRequest(JsonEventMixin, Base):
    __tablename__ = "approval_requests"

    approval_type: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(80), default="pending")
    original_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    revised_payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    requested_by: Mapped[str] = mapped_column(String(200))
    reviewed_by: Mapped[str | None] = mapped_column(String(200), nullable=True)
    reviewer_comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ToolCall(Base):
    __tablename__ = "tool_calls"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    trip_run_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("trip_runs.id"))
    tool_name: Mapped[str] = mapped_column(String(120))
    tool_version: Mapped[str | None] = mapped_column(String(40), nullable=True)
    integration_name: Mapped[str | None] = mapped_column(String(80), nullable=True)
    input: Mapped[dict] = mapped_column(JSONB, default=dict)
    output: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(80))
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    idempotency_key: Mapped[str] = mapped_column(String(200))
    started_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    trace_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    span_id: Mapped[str | None] = mapped_column(String(100), nullable=True)


class LangGraphNodeEvent(Base):
    __tablename__ = "langgraph_node_events"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    trip_run_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("trip_runs.id"))
    node_name: Mapped[str] = mapped_column(String(120))
    input_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    output_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(80))
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    trace_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    span_id: Mapped[str | None] = mapped_column(String(100), nullable=True)


class TemporalWorkflowEvent(JsonEventMixin, Base):
    __tablename__ = "temporal_workflow_events"

    temporal_workflow_id: Mapped[str] = mapped_column(String(200))
    event_type: Mapped[str] = mapped_column(String(120))
    event_summary: Mapped[str] = mapped_column(Text)
    details: Mapped[dict] = mapped_column(JSONB, default=dict)


class AuditEvent(JsonEventMixin, Base):
    __tablename__ = "audit_events"

    event_type: Mapped[str] = mapped_column(String(120))
    actor_type: Mapped[str] = mapped_column(String(80))
    actor_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    details: Mapped[dict] = mapped_column(JSONB, default=dict)
    trace_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    span_id: Mapped[str | None] = mapped_column(String(100), nullable=True)


class ProvenanceRecord(JsonEventMixin, Base):
    __tablename__ = "provenance_records"

    artifact_type: Mapped[str] = mapped_column(String(80))
    artifact_id: Mapped[str] = mapped_column(String(200))
    source_tool_call_ids: Mapped[list] = mapped_column(JSONB, default=list)
    source_slack_message_ids: Mapped[list] = mapped_column(JSONB, default=list)
    participant_ids: Mapped[list] = mapped_column(JSONB, default=list)
    openstreetmap_element_ids: Mapped[list] = mapped_column(JSONB, default=list)
    wikidata_qids: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    wikivoyage_page_titles: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(80), nullable=True)
    integration_versions: Mapped[dict] = mapped_column(JSONB, default=dict)


class NotionDocument(JsonEventMixin, Base):
    __tablename__ = "notion_documents"

    notion_page_id: Mapped[str] = mapped_column(String(200))
    notion_page_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(80), default="draft")
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)


class SlackMessage(JsonEventMixin, Base):
    __tablename__ = "slack_messages"

    channel_id: Mapped[str] = mapped_column(String(200))
    thread_ts: Mapped[str | None] = mapped_column(String(80), nullable=True)
    message_ts: Mapped[str | None] = mapped_column(String(80), nullable=True)
    text: Mapped[str] = mapped_column(Text)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)


class IntegrationEvent(JsonEventMixin, Base):
    __tablename__ = "integration_events"

    integration_name: Mapped[str] = mapped_column(String(80))
    event_type: Mapped[str] = mapped_column(String(120))
    details: Mapped[dict] = mapped_column(JSONB, default=dict)
