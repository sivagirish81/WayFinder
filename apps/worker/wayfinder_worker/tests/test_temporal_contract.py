from wayfinder_worker.workflows.trip_planning_workflow import (
    ApprovalDecision,
    ChangeRequest,
    ClarificationResponse,
    PreferenceResponse,
    TripPlanningInput,
)


def test_temporal_signal_payloads_are_typed() -> None:
    assert ClarificationResponse(text="San Diego", user_id="U1").text == "San Diego"
    assert PreferenceResponse(user_id="U2", text="Museums").user_id == "U2"
    assert ApprovalDecision(approved=True, reviewed_by="dashboard").approved is True
    assert ChangeRequest(requested_by="dashboard", text="More beaches").text == "More beaches"


def test_temporal_input_has_source() -> None:
    payload = TripPlanningInput(trip_run_id="trip-1", original_request="Plan a trip")
    assert payload.source == "manual"
