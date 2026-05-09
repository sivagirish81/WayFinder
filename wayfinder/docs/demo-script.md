# Demo Script

1. Start stack: `make up`
2. Open dashboard: http://localhost:5173
3. Check integrations page.
4. Start a trip from Slack: `@Wayfinder plan a 3-day trip to San Diego for 4 people in August. Budget around $800 each. We like beaches, food, and relaxed schedules.`
5. Wayfinder replies in the thread asking everyone for preferences.
6. Four users reply with preferences from Alex, Priya, Jordan, and Sam.
7. Show the running `TripPlanningWorkflow`.
8. Show Temporal Explorer queries and timeline.
9. Show LangGraph Run View nodes and conditional routing.
10. Show LangChain tool calls.
11. Show participants, normalized preferences, conflicts, tradeoffs, OSM candidates, ranked places, itinerary, and Notion draft.
12. Stop worker: `podman compose stop worker`
13. Approve in the dashboard.
14. Restart worker: `podman compose start worker`
15. Show finalized Notion page, final Slack summary, Jaeger trace, audit trail, and provenance.
