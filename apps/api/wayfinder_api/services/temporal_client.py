from datetime import datetime
from uuid import uuid4

try:
    from temporalio.client import Client
except ModuleNotFoundError:
    Client = None

from wayfinder_api.config import get_settings
from wayfinder_api.schemas import TripCreateRequest, TripResponse

TRIP_THREAD_INDEX: dict[str, str] = {}
TRIP_WORKFLOW_INDEX: dict[str, str] = {}


async def start_trip_workflow(
    payload: TripCreateRequest,
    *,
    slack_channel_id: str | None = None,
    slack_thread_ts: str | None = None,
) -> TripResponse:
    trip_id = uuid4()
    workflow_id = f"trip-planning-{trip_id}"
    settings = get_settings()
    status = "received"
    try:
        if Client is None:
            raise RuntimeError("temporalio is not installed")
        client = await Client.connect(settings.temporal_address, namespace=settings.temporal_namespace)
        await client.start_workflow(
            "TripPlanningWorkflow",
            {
                "trip_run_id": str(trip_id),
                "original_request": payload.original_request,
                "source": payload.source,
            },
            id=workflow_id,
            task_queue=settings.temporal_task_queue,
        )
        status = "planning"
    except Exception:
        status = "received"
    if slack_thread_ts:
        TRIP_THREAD_INDEX[slack_thread_ts] = str(trip_id)
    TRIP_WORKFLOW_INDEX[str(trip_id)] = workflow_id
    return TripResponse(
        id=trip_id,
        source=payload.source,
        original_request=payload.original_request,
        status=status,
        temporal_workflow_id=workflow_id,
        created_at=datetime.utcnow(),
    )


async def signal_participant_preference(trip_id: str, slack_user_id: str, text: str) -> bool:
    workflow_id = TRIP_WORKFLOW_INDEX.get(trip_id)
    if not workflow_id:
        return False
    settings = get_settings()
    try:
        if Client is None:
            return False
        client = await Client.connect(settings.temporal_address, namespace=settings.temporal_namespace)
        handle = client.get_workflow_handle(workflow_id)
        await handle.signal("add_participant_preference", slack_user_id, text)
        return True
    except Exception:
        return False


def trip_id_for_thread(thread_ts: str | None) -> str | None:
    if not thread_ts:
        return None
    return TRIP_THREAD_INDEX.get(thread_ts)
