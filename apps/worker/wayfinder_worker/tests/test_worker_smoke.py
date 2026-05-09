from wayfinder_worker.agent.graph import plan_from_request
from wayfinder_worker.agent.planner import plan_trip


def test_plan_from_request_extracts_known_destination() -> None:
    state = plan_from_request("Plan a 3-day trip to San Diego for 4 people.")
    assert state.destination == "San Diego"
    assert state.missing_fields == []


def test_missing_info_routes_to_followup_questions() -> None:
    plan = plan_trip("Plan a relaxed trip.")
    assert plan.status == "waiting_for_clarification"
    assert "Where should the group go?" in plan.state.followup_questions


def test_multiple_preferences_detect_dining_conflict() -> None:
    plan = plan_trip(
        "Plan a 3-day trip to San Diego for 4 people in August. Budget around $800 each.",
        [
            {"name": "Jordan", "text": "Budget-friendly, avoid expensive dinners."},
            {"name": "Sam", "text": "One nice group dinner, relaxed schedule."},
        ],
    )
    assert plan.status == "planned"
    assert plan.state.preference_conflicts[0]["topic"] == "dining_budget"
    assert "casual meals otherwise" in plan.state.suggested_tradeoffs[0]
