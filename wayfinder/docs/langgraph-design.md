# LangGraph Design

LangGraph models the Wayfinder planning agent as a real state machine. The graph state contains the original request, parsed trip details, missing fields, participant preferences, conflicts, candidate places, ranked places, itinerary, budget estimate, Notion payload, Slack payload, approval flags, revision requests, errors, and messages.

Each node emits persisted node events so the dashboard can show execution order, state snapshots, branch decisions, errors, and the final `TripPlan`.
