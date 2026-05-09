# Security Policy

Wayfinder is a local portfolio demo for durable AI trip coordination. It does
not require committing secrets and should never expose OpenAI, Slack, Notion,
database, or Temporal credentials to the browser.

## Reporting

Please open a private security report or contact the maintainers before
disclosing issues publicly.

## Data Handling

- Do not collect payment details.
- Store only the Slack identifiers needed for coordination and provenance.
- Keep SaaS tokens in `.env` or deployment secrets, never in git.
- Redact secrets from logs and audit records.
