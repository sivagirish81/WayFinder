from pydantic import BaseModel, Field


class PlaceCandidate(BaseModel):
    id: str
    name: str
    category: str
    latitude: float | None = None
    longitude: float | None = None
    address: str | None = None
    tags: dict = Field(default_factory=dict)
    source: str
    source_id: str
    website: str | None = None
    opening_hours: str | None = None
    estimated_relevance: float = 0
    attribution: str = "© OpenStreetMap contributors"
