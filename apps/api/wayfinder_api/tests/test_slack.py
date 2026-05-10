from fastapi.testclient import TestClient

from wayfinder_api.main import app
from wayfinder_api.services.slack_service import (
    build_draft_ready_summary,
    parse_slash_command,
    parse_wayfinder_command,
    record_thread_preference,
)


def test_parse_wayfinder_mention() -> None:
    command = parse_wayfinder_command("@Wayfinder plan a 3-day trip to San Diego")
    assert command is not None
    assert "San Diego" in command


def test_parse_wayfinder_slash_command() -> None:
    assert parse_wayfinder_command("/wayfinder plan a beach trip") == "plan a beach trip"


def test_parse_slash_command_form_body() -> None:
    payload = parse_slash_command(
        b"command=%2Fwayfinder&text=plan%20a%20San%20Diego%20trip&user_id=U1&channel_id=C1"
    )
    assert payload.command == "/wayfinder"
    assert payload.text == "plan a San Diego trip"
    assert payload.channel_id == "C1"


def test_slash_command_endpoint_starts_trip() -> None:
    response = TestClient(app).post(
        "/api/slack/commands",
        content=b"command=%2Fwayfinder&text=plan%20a%203-day%20trip%20to%20San%20Diego&user_id=U1&channel_id=C1",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert "Wayfinder started trip run" in response.json()["text"]


def test_slash_command_short_alias_starts_trip() -> None:
    response = TestClient(app).post(
        "/slack/commands",
        content=b"command=%2Fwayfinder&text=plan%20a%203-day%20trip%20to%20San%20Diego&user_id=U1&channel_id=C1",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert "Wayfinder started trip run" in response.json()["text"]


def test_thread_preference_count_is_deduplicated() -> None:
    first = record_thread_preference("thread-1", "U1", "Sky diving")
    second = record_thread_preference("thread-1", "U1", "Sky diving")
    assert len(first) == 1
    assert len(second) == 1


def test_draft_ready_summary_mentions_count() -> None:
    summary = build_draft_ready_summary(
        [
            {"slack_user_id": "U1", "text": "Beaches"},
            {"slack_user_id": "U2", "text": "Museums"},
            {"slack_user_id": "U3", "text": "Budget"},
            {"slack_user_id": "U4", "text": "Dinner"},
        ]
    )
    assert "4 people" in summary
