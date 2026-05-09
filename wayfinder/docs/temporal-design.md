# Temporal Design

Temporal is the backbone of Wayfinder. It is responsible for durable trip planning execution, including human waits, timers, worker restarts, activity retries, idempotency keys, and queryable workflow state.

Workflow code remains deterministic. It does not call OpenAI, Slack, Notion, Overpass, or PostgreSQL directly. Those side effects run in activities with retry policies and explicit timeouts.

Temporal differs from LangGraph in this architecture: Temporal coordinates the durable business process across hours or days, while LangGraph computes planning state transitions inside activities.
