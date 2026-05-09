# LangGraph Design

LangGraph models the Wayfinder planning agent as a real state machine. The graph state contains the original request, parsed trip details, missing fields, participant preferences, conflicts, candidate places, ranked places, itinerary, budget estimate, Notion payload, Slack payload, approval flags, revision requests, errors, and messages.

Each node emits persisted node events so the dashboard can show execution order, state snapshots, branch decisions, errors, and the final `TripPlan`.

## Nodes

`normalize_request`, `extract_trip_details`, `identify_missing_info`, `generate_followup_questions`, `collect_preference_requirements`, `normalize_group_preferences`, `detect_preference_conflicts`, `discover_candidate_places`, `rank_candidate_places`, `generate_itinerary`, `estimate_budget`, `build_notion_doc`, `build_slack_summary`, `finalize_plan`, `revise_itinerary`, and `error_handler`.

## Conditional Routing

Missing required fields route to follow-up questions. Multi-person trips route to preference collection. Errors route to the error handler. Revision requests route back through itinerary revision before approval.
