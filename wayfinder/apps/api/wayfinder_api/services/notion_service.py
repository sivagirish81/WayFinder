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
