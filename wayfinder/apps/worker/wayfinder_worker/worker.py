import asyncio
import os

from temporalio.client import Client
from temporalio.worker import Worker

from wayfinder_worker.activities.langgraph_activities import run_langgraph_trip_planner_activity
from wayfinder_worker.workflows.trip_planning_workflow import TripPlanningWorkflow


async def main() -> None:
    client = await Client.connect(
        os.getenv("TEMPORAL_ADDRESS", "localhost:7233"),
        namespace=os.getenv("TEMPORAL_NAMESPACE", "default"),
    )
    worker = Worker(
        client,
        task_queue=os.getenv("TEMPORAL_TASK_QUEUE", "wayfinder-task-queue"),
        workflows=[TripPlanningWorkflow],
        activities=[run_langgraph_trip_planner_activity],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
