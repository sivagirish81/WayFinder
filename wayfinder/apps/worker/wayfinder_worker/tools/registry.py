from wayfinder_worker.tools.base import WayfinderTool
from wayfinder_worker.tools.collect_slack_thread_preferences import collect_slack_thread_preferences
from wayfinder_worker.tools.create_notion_trip_doc import create_notion_trip_doc
from wayfinder_worker.tools.detect_preference_conflicts import detect_preference_conflicts
from wayfinder_worker.tools.discover_destination_pois import discover_destination_pois
from wayfinder_worker.tools.estimate_budget import estimate_budget
from wayfinder_worker.tools.export_markdown_plan import export_markdown_plan
from wayfinder_worker.tools.generate_followup_questions import generate_followup_questions
from wayfinder_worker.tools.generate_itinerary import generate_itinerary
from wayfinder_worker.tools.normalize_group_preferences import normalize_group_preferences
from wayfinder_worker.tools.parse_trip_request import parse_trip_request
from wayfinder_worker.tools.post_slack_message import post_slack_message
from wayfinder_worker.tools.rank_candidate_places import rank_candidate_places
from wayfinder_worker.tools.update_notion_trip_doc import update_notion_trip_doc


TOOLS: dict[str, WayfinderTool] = {
    tool.metadata.name: tool
    for tool in [
        parse_trip_request,
        generate_followup_questions,
        collect_slack_thread_preferences,
        normalize_group_preferences,
        detect_preference_conflicts,
        discover_destination_pois,
        rank_candidate_places,
        generate_itinerary,
        estimate_budget,
        create_notion_trip_doc,
        update_notion_trip_doc,
        post_slack_message,
        export_markdown_plan,
    ]
}


def list_tools() -> list[dict]:
    return [tool.public_descriptor() for tool in TOOLS.values()]


def get_tool(name: str) -> WayfinderTool:
    return TOOLS[name]
