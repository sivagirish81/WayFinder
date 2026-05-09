from wayfinder_worker.agent.graph import plan_from_request


def test_plan_from_request_extracts_known_destination() -> None:
    state = plan_from_request("Plan a 3-day trip to San Diego for 4 people.")
    assert state.destination == "San Diego"
    assert state.missing_fields == []
