from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta

try:
    from temporalio import workflow
except ModuleNotFoundError:
    class _WorkflowFallback:
        def defn(self, cls):
            return cls

        def run(self, fn):
            return fn

        def signal(self, fn):
            return fn

        def query(self, fn):
            return fn

        async def execute_activity(self, *args, **kwargs):
            return None

        async def sleep(self, duration):
            return None

        async def wait_condition(self, predicate, timeout=None):
            return predicate()

    workflow = _WorkflowFallback()


@dataclass
class TripPlanningInput:
    trip_run_id: str
    original_request: str
    source: str = "manual"


@dataclass
class TripPlanningResult:
    trip_run_id: str
    status: str


@dataclass
class ClarificationResponse:
    text: str
    user_id: str


@dataclass
class PreferenceResponse:
    user_id: str
    text: str


@dataclass
class ApprovalDecision:
    approved: bool
    reviewed_by: str
    comment: str | None = None


@dataclass
class ChangeRequest:
    requested_by: str
    text: str


@dataclass
class Question:
    text: str


@dataclass
class TripParticipantSummary:
    slack_user_id: str
    preference_text: str | None = None


@dataclass
class GroupPreferenceSummary:
    participant_count: int = 0
    responses: list[PreferenceResponse] = field(default_factory=list)


@dataclass
class PlaceCandidate:
    name: str
    category: str


@dataclass
class PreferenceCollectionStatus:
    status: str
    expected_participant_count: int
    participant_count: int


@dataclass
class ApprovalSummary:
    status: str
    change_request: str | None = None


@dataclass
class TimelineEvent:
    event_type: str
    summary: str


@dataclass
class TripPlanningWorkflowState:
    trip_run_id: str = ""
    status: str = "received"
    waiting_state: str | None = None
    pending_questions: list[Question] = field(default_factory=list)
    participants: list[TripParticipantSummary] = field(default_factory=list)
    preferences: GroupPreferenceSummary = field(default_factory=GroupPreferenceSummary)
    candidate_places: list[PlaceCandidate] = field(default_factory=list)
    approval: ApprovalSummary | None = None
    timeline: list[TimelineEvent] = field(default_factory=list)


@workflow.defn
class TripPlanningWorkflow:
    def __init__(self) -> None:
        self.state = TripPlanningWorkflowState()
        self._approval_decision: ApprovalDecision | None = None
        self._change_request: ChangeRequest | None = None
        self._canceled = False
        self._continue_preferences = False
        self._clarification: ClarificationResponse | None = None

    @workflow.run
    async def run(self, input: TripPlanningInput) -> TripPlanningResult:
        self.state.trip_run_id = input.trip_run_id
        self.state.status = "planning"
        self.state.timeline.append(TimelineEvent("WORKFLOW_STARTED", "Trip planning workflow started."))
        await workflow.execute_activity(
            "run_langgraph_trip_planner_activity",
            input.original_request,
            start_to_close_timeout=timedelta(seconds=30),
        )
        if "trip" not in input.original_request.lower():
            self.state.status = "waiting_for_clarification"
            self.state.waiting_state = "clarification"
            self.state.pending_questions = [Question("What destination should I plan for?")]
            await workflow.wait_condition(lambda: self._clarification is not None or self._canceled)
        if self._canceled:
            self.state.status = "canceled"
            return TripPlanningResult(trip_run_id=input.trip_run_id, status=self.state.status)
        self.state.status = "collecting_preferences"
        self.state.waiting_state = "preference_collection"
        self.state.timeline.append(
            TimelineEvent("PREFERENCE_COLLECTION_STARTED", "Waiting for group preferences.")
        )
        await workflow.sleep(timedelta(seconds=60))
        await workflow.wait_condition(
            lambda: self._continue_preferences
            or len(self.state.preferences.responses) >= 2
            or self._canceled,
            timeout=timedelta(seconds=120),
        )
        if self._canceled:
            self.state.status = "canceled"
            return TripPlanningResult(trip_run_id=input.trip_run_id, status=self.state.status)
        self.state.status = "awaiting_approval"
        self.state.waiting_state = "approval"
        self.state.approval = ApprovalSummary(status="pending")
        self.state.timeline.append(TimelineEvent("APPROVAL_REQUESTED", "Draft plan is awaiting approval."))
        await workflow.wait_condition(
            lambda: self._approval_decision is not None or self._change_request is not None or self._canceled
        )
        if self._change_request is not None:
            self.state.status = "revising"
            self.state.timeline.append(TimelineEvent("CHANGES_REQUESTED", self._change_request.text))
            self._change_request = None
            self.state.status = "awaiting_approval"
            await workflow.wait_condition(lambda: self._approval_decision is not None or self._canceled)
        self.state.status = "canceled" if self._canceled else "completed"
        self.state.waiting_state = None
        self.state.timeline.append(
            TimelineEvent(
                "WORKFLOW_COMPLETED" if self.state.status == "completed" else "WORKFLOW_CANCELED",
                self.state.status,
            )
        )
        return TripPlanningResult(trip_run_id=input.trip_run_id, status=self.state.status)

    @workflow.signal
    async def submit_clarification_response(self, response: ClarificationResponse) -> None:
        self._clarification = response
        self.state.timeline.append(TimelineEvent("CLARIFICATION_RECEIVED", response.text))

    @workflow.signal
    async def submit_preference_response(self, response: PreferenceResponse) -> None:
        self.state.preferences.responses.append(response)
        self.state.preferences.participant_count = len(self.state.preferences.responses)
        self.state.participants.append(TripParticipantSummary(response.user_id, response.text))
        self.state.timeline.append(TimelineEvent("PARTICIPANT_PREFERENCE_RECEIVED", response.user_id))

    @workflow.signal
    async def add_participant_preference(self, slack_user_id: str, text: str) -> None:
        await self.submit_preference_response(PreferenceResponse(slack_user_id, text))

    @workflow.signal
    async def continue_with_current_preferences(self, requested_by: str) -> None:
        self._continue_preferences = True
        self.state.timeline.append(TimelineEvent("PREFERENCE_COLLECTION_CONTINUED_BY_REQUESTER", requested_by))

    @workflow.signal
    async def extend_preference_collection(self, minutes: int) -> None:
        self.state.timeline.append(TimelineEvent("PREFERENCE_COLLECTION_EXTENDED", f"{minutes} minutes"))

    @workflow.signal
    async def approve_plan(self, decision: ApprovalDecision) -> None:
        self._approval_decision = decision
        if self.state.approval:
            self.state.approval.status = "approved" if decision.approved else "rejected"

    @workflow.signal
    async def request_changes(self, change_request: ChangeRequest) -> None:
        self._change_request = change_request
        if self.state.approval:
            self.state.approval.status = "changes_requested"
            self.state.approval.change_request = change_request.text

    @workflow.signal
    async def cancel_run(self, reason: str) -> None:
        self._canceled = True
        self.state.timeline.append(TimelineEvent("WORKFLOW_CANCELED", reason))

    @workflow.query
    def current_state(self) -> TripPlanningWorkflowState:
        return self.state

    @workflow.query
    def pending_questions(self) -> list[Question]:
        return self.state.pending_questions

    @workflow.query
    def participants(self) -> list[TripParticipantSummary]:
        return self.state.participants

    @workflow.query
    def collected_preferences(self) -> GroupPreferenceSummary:
        return self.state.preferences

    @workflow.query
    def candidate_places(self) -> list[PlaceCandidate]:
        return self.state.candidate_places

    @workflow.query
    def preference_collection_status(self) -> PreferenceCollectionStatus:
        return PreferenceCollectionStatus(
            status=self.state.status,
            expected_participant_count=2,
            participant_count=self.state.preferences.participant_count,
        )

    @workflow.query
    def pending_approval(self) -> ApprovalSummary | None:
        return self.state.approval

    @workflow.query
    def timeline(self) -> list[TimelineEvent]:
        return self.state.timeline
