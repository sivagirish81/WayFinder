from pydantic import BaseModel, Field

from wayfinder_worker.tools.base import RiskLevel, ToolMetadata, WayfinderTool


class DiscoverDestinationPoisInput(BaseModel):
    destination: str
    categories: list[str] = Field(default_factory=list)
    radius_meters: int = 15000
    result_limit: int = 30
    group_preferences: dict = Field(default_factory=dict)


class DiscoverDestinationPoisOutput(BaseModel):
    candidate_places: list[dict] = Field(default_factory=list)
    source: str = "openstreetmap_overpass"
    attribution: str = "© OpenStreetMap contributors"
    raw_source_ids: list[str] = Field(default_factory=list)


discover_destination_pois = WayfinderTool(
    metadata=ToolMetadata(
        name="discover_destination_pois",
        description="Use open travel data to find candidate places near the destination.",
        risk_level=RiskLevel.low,
        idempotency="Destination, category set, radius, and result limit.",
        integration_name="openstreetmap_overpass",
    ),
    input_schema=DiscoverDestinationPoisInput,
    output_schema=DiscoverDestinationPoisOutput,
)
