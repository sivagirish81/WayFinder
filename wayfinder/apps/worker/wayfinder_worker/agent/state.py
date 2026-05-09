from pydantic import BaseModel, Field


class TripPlanState(BaseModel):
    run_id: str | None = None
    original_request: str
    requester: str | None = None
    destination: str | None = None
    dates: str | None = None
    duration_days: int | None = None
    group_size: int | None = None
    budget_per_person: float | None = None
    expected_participant_count: int | None = None
    participant_responses: list[dict] = Field(default_factory=list)
    per_user_preferences: dict = Field(default_factory=dict)
    merged_group_preferences: dict = Field(default_factory=dict)
    dietary_constraints: list[str] = Field(default_factory=list)
    pace_preferences: list[str] = Field(default_factory=list)
    activity_preferences: list[str] = Field(default_factory=list)
    avoid_list: list[str] = Field(default_factory=list)
    budget_sensitivity: str | None = None
    preference_conflicts: list[dict] = Field(default_factory=list)
    suggested_tradeoffs: list[str] = Field(default_factory=list)
    planning_rules: dict = Field(default_factory=dict)
    missing_fields: list[str] = Field(default_factory=list)
    followup_questions: list[str] = Field(default_factory=list)
    group_preference_questions: list[str] = Field(default_factory=list)
    candidate_places: list[dict] = Field(default_factory=list)
    ranked_places: list[dict] = Field(default_factory=list)
    itinerary_draft: dict = Field(default_factory=dict)
    budget_estimate: dict = Field(default_factory=dict)
    notion_doc_payload: dict = Field(default_factory=dict)
    slack_summary_payload: dict = Field(default_factory=dict)
    approval_required: bool = True
    revision_requests: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    messages: list[str] = Field(default_factory=list)
    route_decisions: list[str] = Field(default_factory=list)


class TripPlan(BaseModel):
    state: TripPlanState
    status: str
