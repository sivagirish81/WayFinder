from datetime import datetime

PROVENANCE: dict[str, list[dict]] = {}


async def record_provenance(trip_id: str, artifact_type: str, artifact_id: str, sources: dict) -> dict:
    record = {
        "trip_run_id": trip_id,
        "artifact_type": artifact_type,
        "artifact_id": artifact_id,
        "sources": sources,
        "created_at": datetime.utcnow().isoformat(),
    }
    PROVENANCE.setdefault(trip_id, []).append(record)
    return record


async def list_provenance(trip_id: str) -> list[dict]:
    return PROVENANCE.get(trip_id, [])
