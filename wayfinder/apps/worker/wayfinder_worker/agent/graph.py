from wayfinder_worker.agent.state import TripPlanState


def build_trip_planning_graph():
    """Phase 1 placeholder. Later phases replace this with a full StateGraph."""
    return None


def plan_from_request(original_request: str) -> TripPlanState:
    state = TripPlanState(original_request=original_request)
    if "San Diego" in original_request:
        state.destination = "San Diego"
    if state.destination is None:
        state.missing_fields.append("destination")
    state.messages.append("Initial planning state created.")
    return state
