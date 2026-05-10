import logging

import httpx

logger = logging.getLogger(__name__)


def build_trip_page_title(destination: str | None) -> str:
    return f"{destination or 'Group'} Group Trip Plan"


def build_issue_page_title(issue_summary: str | None) -> str:
    summary = (issue_summary or "Slack Thread").strip()
    if len(summary) > 72:
        summary = f"{summary[:69]}..."
    return f"Issue Brief: {summary}"


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


async def create_notion_issue_page(
    *,
    api_key: str,
    parent_page_id: str,
    trip_database_id: str,
    title: str,
    run_id: str,
    issue_context: str,
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
    children = _issue_notion_children(run_id, issue_context)
    if trip_database_id:
        payload = {
            "parent": {"database_id": trip_database_id},
            "properties": {"Name": {"title": [{"text": {"content": title}}]}},
            "children": children,
        }
    else:
        payload = {
            "parent": {"page_id": parent_page_id},
            "properties": {"title": [{"text": {"content": title}}]},
            "children": children,
        }

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
        data = response.json()
        if response.status_code >= 400:
            logger.warning("Notion issue page creation failed: %s", data)
            return {"ok": False, "status_code": response.status_code, "error": data}
        logger.info("Notion issue page created page_id=%s url=%s", data.get("id"), data.get("url"))
        return {"ok": True, "page_id": data.get("id"), "url": data.get("url")}


async def append_notion_thread_update(
    *,
    api_key: str,
    page_id: str | None,
    slack_user_id: str,
    text: str,
) -> dict:
    if not api_key:
        return {"ok": False, "error": "NOTION_API_KEY is not configured"}
    if not page_id:
        return {"ok": False, "error": "No Notion page is mapped to this Slack thread"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    payload = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": f"Slack update from {slack_user_id}: "}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": text}},
                    ]
                },
            }
        ]
    }
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.patch(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            headers=headers,
            json=payload,
        )
        data = response.json()
        if response.status_code >= 400:
            logger.warning("Notion append failed: %s", data)
            return {"ok": False, "status_code": response.status_code, "error": data}
        return {"ok": True}


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


def _issue_notion_children(run_id: str, issue_context: str) -> list[dict]:
    return [
        _heading("Issue"),
        _paragraph(issue_context),
        _heading("Current Understanding"),
        _paragraph("Summarize the concrete symptom, affected users/systems, severity, and timeline as the Slack thread evolves."),
        _heading("Root Cause"),
        _paragraph("Pending. Capture confirmed cause, contributing factors, and evidence."),
        _heading("Proposed Fixes"),
        *_todo_blocks(["Primary fix", "Validation plan", "Rollback plan"]),
        _heading("Risks"),
        *_todo_blocks(["Implementation risk", "Regression risk", "Operational risk"]),
        _heading("Open Questions"),
        *_todo_blocks(["What evidence is still missing?", "Who owns the final decision?", "What is the deadline?"]),
        _heading("Decision Log"),
        _paragraph("Decisions from the Slack thread will be captured here."),
        _heading("Slack Discussion Evidence"),
        _paragraph("New thread replies are appended below as they arrive."),
        _heading("ThreadBrief Metadata"),
        _paragraph(f"run_id: {run_id}"),
    ]


def _heading(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def _paragraph(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def _todo_blocks(items: list[str]) -> list[dict]:
    return [
        {
            "object": "block",
            "type": "to_do",
            "to_do": {"rich_text": [{"type": "text", "text": {"content": item}}], "checked": False},
        }
        for item in items
    ]
