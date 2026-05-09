from collections import defaultdict
from datetime import datetime

PREFERENCES: dict[str, list[dict]] = defaultdict(list)


async def add_manual_preference(trip_id: str, name: str, preference_text: str) -> dict:
    response = {
        "trip_id": trip_id,
        "name": name,
        "preference_text": preference_text,
        "created_at": datetime.utcnow().isoformat(),
    }
    PREFERENCES[trip_id].append(response)
    return response


async def get_preferences(trip_id: str) -> list[dict]:
    return PREFERENCES[trip_id]
