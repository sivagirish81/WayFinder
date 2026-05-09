from wayfinder_worker.tools.registry import TOOLS, list_tools


EXPECTED_TOOLS = {
    "parse_trip_request",
    "generate_followup_questions",
    "collect_slack_thread_preferences",
    "normalize_group_preferences",
    "detect_preference_conflicts",
    "discover_destination_pois",
    "rank_candidate_places",
    "generate_itinerary",
    "estimate_budget",
    "create_notion_trip_doc",
    "update_notion_trip_doc",
    "post_slack_message",
    "export_markdown_plan",
}


def test_registry_exposes_all_required_tools() -> None:
    assert set(TOOLS) == EXPECTED_TOOLS


def test_every_tool_has_metadata_and_schemas() -> None:
    for descriptor in list_tools():
        assert descriptor["name"]
        assert descriptor["description"]
        assert descriptor["risk_level"] in {"low", "medium", "high"}
        assert descriptor["integration_name"]
        assert descriptor["input_schema"]["type"] == "object"
        assert descriptor["output_schema"]["type"] == "object"
