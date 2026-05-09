from abc import ABC, abstractmethod

from wayfinder_worker.travel_data.schemas import PlaceCandidate


class TravelDataProvider(ABC):
    name: str

    @abstractmethod
    async def discover_places(
        self,
        destination: str,
        categories: list[str],
        radius_meters: int,
        result_limit: int,
    ) -> list[PlaceCandidate]:
        raise NotImplementedError
