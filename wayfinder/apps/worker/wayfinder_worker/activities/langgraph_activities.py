from temporalio import activity


@activity.defn
async def run_langgraph_trip_planner_activity(original_request: str) -> dict:
    return {"original_request": original_request, "status": "planned"}
