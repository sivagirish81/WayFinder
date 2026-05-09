from wayfinder_api.services.notion_service import build_notion_trip_document


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
