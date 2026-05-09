from wayfinder_worker.travel_data.base import TravelDataProvider
from wayfinder_worker.travel_data.schemas import PlaceCandidate

OSM_ATTRIBUTION = "© OpenStreetMap contributors"


class OverpassProvider(TravelDataProvider):
    name = "openstreetmap_overpass"

    def build_query(self, destination: str, radius_meters: int, result_limit: int) -> str:
        bounded_limit = min(max(result_limit, 1), 50)
        bounded_radius = min(max(radius_meters, 1000), 25000)
        return f"""
[out:json][timeout:25];
area["name"="{destination}"]->.searchArea;
(
  node["tourism"~"attraction|museum|viewpoint|gallery"](area.searchArea);
  node["amenity"~"restaurant|cafe|bar"](area.searchArea);
  node["leisure"~"park|beach_resort"](area.searchArea);
  node["natural"="beach"](area.searchArea);
  node["historic"](area.searchArea);
  node["place"="neighbourhood"](area.searchArea);
);
out center {bounded_limit};
/* radius guard: {bounded_radius} meters */
""".strip()

    async def discover_places(
        self,
        destination: str,
        categories: list[str],
        radius_meters: int,
        result_limit: int,
    ) -> list[PlaceCandidate]:
        return []


def normalize_overpass_elements(elements: list[dict], limit: int = 30) -> list[PlaceCandidate]:
    places: list[PlaceCandidate] = []
    for element in elements[:limit]:
        tags = element.get("tags", {})
        name = tags.get("name")
        if not name:
            continue
        category = (
            tags.get("tourism")
            or tags.get("amenity")
            or tags.get("leisure")
            or tags.get("natural")
            or tags.get("historic")
            or tags.get("place")
            or "place"
        )
        places.append(
            PlaceCandidate(
                id=f"osm:{element.get('type', 'node')}:{element.get('id')}",
                name=name,
                category=category,
                latitude=element.get("lat") or element.get("center", {}).get("lat"),
                longitude=element.get("lon") or element.get("center", {}).get("lon"),
                tags=tags,
                source="openstreetmap",
                source_id=str(element.get("id")),
                website=tags.get("website"),
                opening_hours=tags.get("opening_hours"),
                estimated_relevance=0.5,
                attribution=OSM_ATTRIBUTION,
            )
        )
    return places
