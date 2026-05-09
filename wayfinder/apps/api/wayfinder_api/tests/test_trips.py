from fastapi.testclient import TestClient

from wayfinder_api.main import app


def test_manual_trip_creation_returns_workflow_id() -> None:
    response = TestClient(app).post(
        "/api/demo/trips",
        json={"original_request": "Plan a 3-day San Diego trip for 4 people."},
    )
    assert response.status_code == 202
    data = response.json()
    assert data["source"] == "manual_demo_input"
    assert data["temporal_workflow_id"].startswith("trip-planning-")
