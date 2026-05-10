from wayfinder_api.services.notion_service import build_issue_page_title, build_notion_trip_document


def test_notion_document_contains_itinerary_checkboxes() -> None:
    doc = build_notion_trip_document(
        {
            "destination": "San Diego",
            "itinerary": {"days": [{"day": 1, "theme": "Beach and tacos"}]},
            "metadata": {"trip_run_id": "trip-1"},
        }
    )
    itinerary = [section for section in doc["sections"] if section["heading"] == "Suggested itinerary"][0]
    assert doc["title"] == "San Diego Group Trip Plan"
    assert itinerary["checkboxes"][0]["checked"] is False
    assert "Beach and tacos" in itinerary["checkboxes"][0]["label"]


def test_issue_page_title_is_bounded() -> None:
    title = build_issue_page_title("Production deploy caused API 500s for workspace users")
    assert title.startswith("Issue Brief:")
    assert "API 500s" in title

    long_title = build_issue_page_title("x" * 200)
    assert len(long_title) < 90
