import logging

import httpx

logger = logging.getLogger(__name__)


def build_trip_page_title(destination: str | None) -> str:
    return f"{destination or 'Group'} Group Trip Plan"


def build_notion_trip_document(plan: dict, final: bool = False) -> dict:
    destination = plan.get("destination") or "Group"
    days = plan.get("itinerary", {}).get("days", [])
    return {
        "title": build_trip_page_title(destination),
        "status": "final" if final else "draft",
        "sections": [
            {"heading": "Overview", "icon": "🧭", "body": plan.get("overview", "")},
            {"heading": "Participants", "icon": "👥", "items": plan.get("participants", [])},
            {"heading": "Individual preferences", "icon": "💬", "items": plan.get("preferences", [])},
            {"heading": "Tradeoffs and conflicts", "icon": "⚖️", "items": plan.get("tradeoffs", [])},
            {"heading": "Candidate places considered", "icon": "📍", "items": plan.get("places", [])},
            {
                "heading": "Suggested itinerary",
                "icon": "✅",
                "checkboxes": [
                    {"checked": False, "label": f"Day {day.get('day')}: {day.get('theme')}"}
                    for day in days
                ],
            },
            {"heading": "Estimated budget", "icon": "💵", "body": plan.get("budget_note", "")},
            {"heading": "Open data attribution", "icon": "🌐", "body": plan.get("attribution", "")},
            {"heading": "Wayfinder metadata", "icon": "🧾", "metadata": plan.get("metadata", {})},
        ],
    }


async def create_notion_trip_page(
    *,
    api_key: str,
    parent_page_id: str,
    trip_database_id: str,
    title: str,
    trip_run_id: str,
    original_request: str,
) -> dict:
    if not api_key:
        return {"ok": False, "error": "NOTION_API_KEY is not configured"}
    if not parent_page_id and not trip_database_id:
        return {"ok": False, "error": "NOTION_PARENT_PAGE_ID or NOTION_TRIP_DATABASE_ID is required"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    if trip_database_id:
        payload = {
            "parent": {"database_id": trip_database_id},
            "properties": {"Name": {"title": [{"text": {"content": title}}]}},
            "children": _notion_children(trip_run_id, original_request),
        }
    else:
        payload = {
            "parent": {"page_id": parent_page_id},
            "properties": {"title": [{"text": {"content": title}}]},
            "children": _notion_children(trip_run_id, original_request),
        }

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
        data = response.json()
        if response.status_code >= 400:
            logger.warning("Notion page creation failed: %s", data)
            return {"ok": False, "status_code": response.status_code, "error": data}
        logger.info("Notion page created page_id=%s url=%s", data.get("id"), data.get("url"))
        return {"ok": True, "page_id": data.get("id"), "url": data.get("url")}


def _notion_children(trip_run_id: str, original_request: str) -> list[dict]:
    return [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Overview"}}]},
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Draft trip coordination page created from Slack. Wayfinder will update this as preferences and approvals move forward."
                        },
                    }
                ]
            },
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Original request"}}]},
        },
        {
            "object": "block",
            "type": "quote",
            "quote": {"rich_text": [{"type": "text", "text": {"content": original_request}}]},
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Preference checklist"}}]},
        },
        *_todo_blocks(
            [
                "Must-do activities",
                "Food preferences or dietary constraints",
                "Preferred pace",
                "Budget concerns",
                "Things to avoid",
            ]
        ),
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Wayfinder metadata"}}]},
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": f"trip_run_id: {trip_run_id}"}},
                ]
            },
        },
    ]


def _todo_blocks(items: list[str]) -> list[dict]:
    return [
        {
            "object": "block",
            "type": "to_do",
            "to_do": {"rich_text": [{"type": "text", "text": {"content": item}}], "checked": False},
        }
        for item in items
    ]
