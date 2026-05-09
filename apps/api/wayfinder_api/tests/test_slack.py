from wayfinder_api.services.slack_service import parse_wayfinder_command


def test_parse_wayfinder_mention() -> None:
    command = parse_wayfinder_command("@Wayfinder plan a 3-day trip to San Diego")
    assert command is not None
    assert "San Diego" in command


def test_parse_wayfinder_slash_command() -> None:
    assert parse_wayfinder_command("/wayfinder plan a beach trip") == "plan a beach trip"
