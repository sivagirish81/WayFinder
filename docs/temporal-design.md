# Temporal Design

Temporal is the backbone of Wayfinder. It is responsible for durable trip planning execution, including human waits, timers, worker restarts, activity retries, idempotency keys, and queryable workflow state.

Workflow code remains deterministic. It does not call OpenAI, Slack, Notion, Overpass, or PostgreSQL directly. Those side effects run in activities with retry policies and explicit timeouts.

Temporal differs from LangGraph in this architecture: Temporal coordinates the durable business process across hours or days, while LangGraph computes planning state transitions inside activities.

## Demonstrated Features

- Workflows: `TripPlanningWorkflow` owns the end-to-end lifecycle.
- Activities: Slack, Notion, audit, database, travel data, tool registry, and LangGraph side effects are activity boundaries.
- Signals: clarifications, participant preferences, continue, extension, approval, changes, and cancellation.
- Queries: current state, pending questions, participants, preferences, candidate places, approval, collection status, and timeline.
- Timers: preference reminder and auto-continue timers use short demo durations and can be mapped to 12/24 hour production waits.
- Retries and idempotency: integration activities accept idempotency keys and are designed to be wrapped with Temporal retry policies.
- Worker restart recovery: approval waits are durable; stopping the worker does not lose the workflow.
