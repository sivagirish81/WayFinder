# LangChain Tools Design

LangChain tools are Wayfinder's integration and capability layer. Each tool has typed Pydantic input and output schemas, metadata, risk level, approval behavior, idempotency policy, retry policy, integration name, and version.

Tool calls are persisted in `tool_calls` and shown in the dashboard with inputs, outputs, status, duration, trace IDs, span IDs, and idempotency keys.

## Tool Registry

The registry exposes all required tools: parsing, follow-up generation, Slack thread collection, preference normalization, conflict detection, OSM discovery, place ranking, itinerary generation, budget estimation, Notion create/update, Slack posting, and markdown export.

Each descriptor includes input/output JSON schema, risk level, approval metadata, idempotency behavior, retry behavior, integration name, and version.
