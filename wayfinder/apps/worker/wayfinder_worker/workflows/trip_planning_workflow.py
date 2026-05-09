from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta

from temporalio import workflow


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
class TripPlanningWorkflowState:
    trip_run_id: str = ""
    status: str = "received"
    timeline: list[str] = field(default_factory=list)


@workflow.defn
class TripPlanningWorkflow:
    def __init__(self) -> None:
        self.state = TripPlanningWorkflowState()
        self._approved = False
        self._canceled = False

    @workflow.run
    async def run(self, input: TripPlanningInput) -> TripPlanningResult:
        self.state.trip_run_id = input.trip_run_id
        self.state.status = "planning"
        self.state.timeline.append("WORKFLOW_STARTED")
        await workflow.execute_activity(
            "run_langgraph_trip_planner_activity",
            input.original_request,
            start_to_close_timeout=timedelta(seconds=30),
        )
        self.state.status = "awaiting_approval"
        self.state.timeline.append("APPROVAL_REQUESTED")
        await workflow.wait_condition(lambda: self._approved or self._canceled)
        self.state.status = "canceled" if self._canceled else "completed"
        self.state.timeline.append("WORKFLOW_COMPLETED" if self._approved else "WORKFLOW_CANCELED")
        return TripPlanningResult(trip_run_id=input.trip_run_id, status=self.state.status)

    @workflow.signal
    async def approve_plan(self, decision: str) -> None:
        self._approved = decision == "approved"

    @workflow.signal
    async def cancel_run(self, reason: str) -> None:
        self._canceled = True
        self.state.timeline.append(f"CANCELED: {reason}")

    @workflow.query
    def current_state(self) -> TripPlanningWorkflowState:
        return self.state

    @workflow.query
    def timeline(self) -> list[str]:
        return self.state.timeline
