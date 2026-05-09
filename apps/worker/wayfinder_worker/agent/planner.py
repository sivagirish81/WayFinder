from wayfinder_worker.agent.graph import run_trip_planning_graph
from wayfinder_worker.agent.state import TripPlan, TripPlanState


def plan_trip(original_request: str, participant_responses: list[dict] | None = None) -> TripPlan:
    return run_trip_planning_graph(
        TripPlanState(
            original_request=original_request,
            participant_responses=participant_responses or [],
        )
    )
