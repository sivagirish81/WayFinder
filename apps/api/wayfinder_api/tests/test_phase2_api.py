from fastapi.testclient import TestClient

from wayfinder_api.main import app


client = TestClient(app)


def test_integration_status_endpoint() -> None:
    response = client.get("/api/integrations/status")
    assert response.status_code == 200
    assert "openai" in response.json()


def test_participant_preference_endpoint() -> None:
    response = client.post(
        "/api/trips/trip-1/preferences",
        json={"name": "Alex", "preference_text": "Beaches, tacos, no early mornings."},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Alex"

    preferences = client.get("/api/trips/trip-1/preferences")
    assert preferences.status_code == 200
    assert preferences.json()[0]["preference_text"].startswith("Beaches")


def test_approval_endpoint_records_decision() -> None:
    response = client.post("/api/approvals/approval-1/approve", json={"comment": "Looks good"})
    assert response.status_code == 200
    assert response.json()["status"] == "approved"


def test_audit_endpoint_returns_events() -> None:
    response = client.get("/api/audit/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
