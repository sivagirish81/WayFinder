from temporalio import activity

from wayfinder_worker.travel_data.osm_overpass import normalize_overpass_elements


@activity.defn
async def discover_destination_pois_activity(payload: dict) -> dict:
    elements = payload.get("fixture_elements", [])
    places = normalize_overpass_elements(elements, limit=payload.get("result_limit", 30))
    return {
        "candidate_places": [place.model_dump() for place in places],
        "source": "openstreetmap_overpass",
        "attribution": "© OpenStreetMap contributors",
    }
