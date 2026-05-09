# LangChain Tools Design

LangChain tools are Wayfinder's integration and capability layer. Each tool has typed Pydantic input and output schemas, metadata, risk level, approval behavior, idempotency policy, retry policy, integration name, and version.

Tool calls are persisted in `tool_calls` and shown in the dashboard with inputs, outputs, status, duration, trace IDs, span IDs, and idempotency keys.
