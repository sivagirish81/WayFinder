from temporalio import activity

from wayfinder_worker.tools.registry import list_tools


@activity.defn
async def list_tool_registry_activity() -> list[dict]:
    return list_tools()
