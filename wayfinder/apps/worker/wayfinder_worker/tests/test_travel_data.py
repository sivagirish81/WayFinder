from wayfinder_worker.travel_data.osm_overpass import OverpassProvider, normalize_overpass_elements


def test_overpass_provider_builds_bounded_query() -> None:
    query = OverpassProvider().build_query("San Diego", radius_meters=999999, result_limit=999)
    assert 'area["name"="San Diego"]' in query
    assert "out center 50" in query
    assert "25000 meters" in query


def test_overpass_normalizes_places() -> None:
    places = normalize_overpass_elements(
        [
            {
                "type": "node",
                "id": 123,
                "lat": 32.85,
                "lon": -117.27,
                "tags": {"name": "La Jolla Shores", "natural": "beach"},
            }
        ]
    )
    assert places[0].name == "La Jolla Shores"
    assert places[0].category == "beach"
    assert places[0].source_id == "123"
