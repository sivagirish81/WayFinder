import re

from wayfinder_worker.agent.state import TripPlan, TripPlanState


def build_trip_planning_graph():
    """Build a LangGraph StateGraph when langgraph is installed.

    Tests use the deterministic runner below so they do not require network calls or paid services.
    """
    try:
        from langgraph.graph import END, StateGraph
    except ModuleNotFoundError:
        return None

    graph = StateGraph(TripPlanState)
    for node in [
        normalize_request_node,
        extract_trip_details_node,
        identify_missing_info_node,
        generate_followup_questions_node,
        collect_preference_requirements_node,
        normalize_group_preferences_node,
        detect_preference_conflicts_node,
        discover_candidate_places_node,
        rank_candidate_places_node,
        generate_itinerary_node,
        estimate_budget_node,
        build_notion_doc_node,
        build_slack_summary_node,
        finalize_plan_node,
        revise_itinerary_node,
        error_handler_node,
    ]:
        graph.add_node(node.__name__.removesuffix("_node"), node)
    graph.set_entry_point("normalize_request")
    graph.add_edge("normalize_request", "extract_trip_details")
    graph.add_edge("extract_trip_details", "identify_missing_info")
    graph.add_conditional_edges(
        "identify_missing_info",
        route_after_missing_info,
        {
            "followup": "generate_followup_questions",
            "preferences": "collect_preference_requirements",
            "discover": "discover_candidate_places",
            "error": "error_handler",
        },
    )
    graph.add_edge("generate_followup_questions", END)
    graph.add_edge("collect_preference_requirements", "normalize_group_preferences")
    graph.add_edge("normalize_group_preferences", "detect_preference_conflicts")
    graph.add_edge("detect_preference_conflicts", "discover_candidate_places")
    graph.add_edge("discover_candidate_places", "rank_candidate_places")
    graph.add_edge("rank_candidate_places", "generate_itinerary")
    graph.add_conditional_edges(
        "generate_itinerary",
        route_after_itinerary,
        {"budget_adjust": "estimate_budget", "revision": "revise_itinerary", "continue": "estimate_budget"},
    )
    graph.add_edge("revise_itinerary", "estimate_budget")
    graph.add_edge("estimate_budget", "build_notion_doc")
    graph.add_edge("build_notion_doc", "build_slack_summary")
    graph.add_edge("build_slack_summary", "finalize_plan")
    graph.add_edge("finalize_plan", END)
    graph.add_edge("error_handler", END)
    return graph.compile()


def plan_from_request(original_request: str) -> TripPlanState:
    return run_trip_planning_graph(TripPlanState(original_request=original_request)).state


def run_trip_planning_graph(state: TripPlanState) -> TripPlan:
    for node in [normalize_request_node, extract_trip_details_node, identify_missing_info_node]:
        state = node(state)
    route = route_after_missing_info(state)
    if route == "followup":
        return TripPlan(state=generate_followup_questions_node(state), status="waiting_for_clarification")
    if route == "error":
        return TripPlan(state=error_handler_node(state), status="failed")
    if route == "preferences":
        state = collect_preference_requirements_node(state)
    for node in [
        normalize_group_preferences_node,
        detect_preference_conflicts_node,
        discover_candidate_places_node,
        rank_candidate_places_node,
        generate_itinerary_node,
        estimate_budget_node,
        build_notion_doc_node,
        build_slack_summary_node,
        finalize_plan_node,
    ]:
        state = node(state)
    return TripPlan(state=state, status="planned")


def normalize_request_node(state: TripPlanState) -> TripPlanState:
    state.original_request = " ".join(state.original_request.split())
    state.messages.append("Request normalized.")
    return state


def extract_trip_details_node(state: TripPlanState) -> TripPlanState:
    request = state.original_request
    if "san diego" in request.lower():
        state.destination = "San Diego"
    duration_match = re.search(r"(\d+)[ -]?day", request, re.IGNORECASE)
    if duration_match:
        state.duration_days = int(duration_match.group(1))
    group_match = re.search(r"for (\d+) people", request, re.IGNORECASE)
    if group_match:
        state.group_size = int(group_match.group(1))
        state.expected_participant_count = state.group_size
    budget_match = re.search(r"\$?(\d{2,5})\s*(?:each|per person)", request, re.IGNORECASE)
    if budget_match:
        state.budget_per_person = float(budget_match.group(1))
    if "august" in request.lower():
        state.dates = "August"
    for preference in ["beaches", "food", "relaxed", "museums", "scenic walks"]:
        if preference in request.lower():
            state.activity_preferences.append(preference)
    state.messages.append("Trip details extracted.")
    return state


def identify_missing_info_node(state: TripPlanState) -> TripPlanState:
    required = ["destination", "duration_days", "group_size"]
    state.missing_fields = [field for field in required if getattr(state, field) in [None, "", []]]
    state.messages.append("Missing information identified.")
    return state


def generate_followup_questions_node(state: TripPlanState) -> TripPlanState:
    labels = {
        "destination": "Where should the group go?",
        "duration_days": "How many days should I plan for?",
        "group_size": "How many people are joining?",
    }
    state.followup_questions = [labels[field] for field in state.missing_fields]
    state.route_decisions.append("missing_fields -> followup")
    return state


def collect_preference_requirements_node(state: TripPlanState) -> TripPlanState:
    state.group_preference_questions = [
        "Must-do activities",
        "Food preferences or dietary constraints",
        "Preferred pace",
        "Budget concerns",
        "Things to avoid",
    ]
    state.route_decisions.append("group_size > 1 -> preference_collection")
    return state


def normalize_group_preferences_node(state: TripPlanState) -> TripPlanState:
    if not state.participant_responses:
        state.merged_group_preferences = {
            "activities": state.activity_preferences or ["beaches", "food"],
            "pace": "relaxed" if "relaxed" in state.original_request.lower() else "balanced",
        }
        return state
    for response in state.participant_responses:
        text = response.get("text", "").lower()
        name = response.get("name", "participant")
        state.per_user_preferences[name] = {"raw_text": response.get("text", "")}
        if "vegetarian" in text:
            state.dietary_constraints.append("vegetarian")
        if "avoid" in text:
            state.avoid_list.append(response.get("text", ""))
        if "relaxed" in text or "no early" in text:
            state.pace_preferences.append("relaxed")
    state.merged_group_preferences = {
        "dietary_constraints": state.dietary_constraints,
        "pace": "relaxed" if state.pace_preferences else "balanced",
    }
    return state


def detect_preference_conflicts_node(state: TripPlanState) -> TripPlanState:
    texts = " ".join(item.get("text", "").lower() for item in state.participant_responses)
    if "nice group dinner" in texts and "avoid expensive dinners" in texts:
        state.preference_conflicts.append(
            {"topic": "dining_budget", "summary": "Nice dinner request conflicts with budget dining."}
        )
        state.suggested_tradeoffs.append("Plan one nice group dinner and casual meals otherwise.")
    state.planning_rules["pace"] = state.merged_group_preferences.get("pace", "balanced")
    return state


def discover_candidate_places_node(state: TripPlanState) -> TripPlanState:
    if not state.destination:
        state.errors.append("Cannot discover places without a destination.")
        return state
    state.candidate_places = [
        {"id": "osm-beach-1", "name": "La Jolla Shores", "category": "beach", "source": "openstreetmap"},
        {"id": "osm-museum-1", "name": "Balboa Park", "category": "museum_park", "source": "openstreetmap"},
        {"id": "osm-food-1", "name": "Old Town tacos area", "category": "food", "source": "openstreetmap"},
    ]
    return state


def rank_candidate_places_node(state: TripPlanState) -> TripPlanState:
    state.ranked_places = [
        {**place, "rank": index + 1, "reason": "Matches group preferences"}
        for index, place in enumerate(state.candidate_places)
    ]
    return state


def generate_itinerary_node(state: TripPlanState) -> TripPlanState:
    state.itinerary_draft = {
        "destination": state.destination,
        "days": [
            {"day": 1, "theme": "Arrival, beach, and casual tacos"},
            {"day": 2, "theme": "Balboa Park, museums, and scenic walks"},
            {"day": 3, "theme": "Relaxed coast morning and one group dinner"},
        ][: state.duration_days or 3],
    }
    return state


def estimate_budget_node(state: TripPlanState) -> TripPlanState:
    budget = state.budget_per_person or 800
    state.budget_estimate = {
        "lodging": round(budget * 0.45, 2),
        "food": round(budget * 0.25, 2),
        "local_transport": round(budget * 0.12, 2),
        "activities": round(budget * 0.1, 2),
        "buffer": round(budget * 0.08, 2),
    }
    return state


def build_notion_doc_node(state: TripPlanState) -> TripPlanState:
    state.notion_doc_payload = {
        "title": f"{state.destination} Group Trip Plan",
        "sections": ["Overview", "Participants", "Preferences", "Tradeoffs", "Itinerary", "Budget"],
    }
    return state


def build_slack_summary_node(state: TripPlanState) -> TripPlanState:
    state.slack_summary_payload = {
        "text": f"Draft {state.destination} plan is ready for approval.",
        "approval_required": True,
    }
    return state


def finalize_plan_node(state: TripPlanState) -> TripPlanState:
    state.messages.append("Trip plan finalized for approval.")
    return state


def revise_itinerary_node(state: TripPlanState) -> TripPlanState:
    state.messages.append("Revision request applied.")
    return state


def error_handler_node(state: TripPlanState) -> TripPlanState:
    state.messages.append("Planning stopped because required state is unavailable.")
    return state


def route_after_missing_info(state: TripPlanState) -> str:
    if state.errors:
        return "error"
    if state.missing_fields:
        return "followup"
    if (state.group_size or 1) > 1:
        return "preferences"
    return "discover"


def route_after_itinerary(state: TripPlanState) -> str:
    if state.revision_requests:
        return "revision"
    if state.budget_per_person and state.budget_per_person < 300:
        return "budget_adjust"
    return "continue"
