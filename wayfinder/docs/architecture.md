# Architecture

Wayfinder separates durable workflow orchestration, agent reasoning, and integration execution into three explicit layers.

- Temporal owns the long-running trip coordination lifecycle.
- LangGraph owns structured planning state and conditional agent routing.
- LangChain tools own integration boundaries, schemas, risk metadata, retries, idempotency, and tool-call persistence.

The API starts workflows, receives Slack and dashboard input, exposes workflow state, and serves the React dashboard. The worker executes Temporal activities that call LangGraph and LangChain tools. PostgreSQL stores domain records, audit events, provenance, LangGraph node events, Temporal event projections, and tool calls.
