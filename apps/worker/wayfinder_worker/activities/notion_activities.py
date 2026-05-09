from temporalio import activity


@activity.defn
async def create_notion_trip_doc_activity(payload: dict) -> dict:
    key = payload.get("idempotency_key", payload.get("trip_run_id", "trip"))
    return {
        "notion_page_id": f"notion-demo-{key}",
        "notion_page_url": f"https://notion.local/{key}",
        "status": "draft",
        "idempotency_key": key,
    }


@activity.defn
async def update_notion_trip_doc_activity(payload: dict) -> dict:
    return {
        "notion_page_id": payload.get("notion_page_id"),
        "status": "final" if payload.get("mark_final") else "draft",
        "idempotency_key": payload.get("idempotency_key"),
    }
