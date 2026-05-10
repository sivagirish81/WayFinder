# Slack Setup

Wayfinder can be tested directly from Slack through Slack HTTP events and slash commands. Slack must reach a public HTTPS URL, so local testing needs a tunnel.

## Local Tunnel

From the repo root, run the app stack:

```bash
make up
```

In another terminal:

```bash
ngrok http 8000
```

Use the generated HTTPS domain for Slack URLs. Both `/api/slack/...` and `/slack/...` are accepted.

```text
https://YOUR-NGROK-DOMAIN.ngrok-free.app/api/slack/events
https://YOUR-NGROK-DOMAIN.ngrok-free.app/api/slack/commands
https://YOUR-NGROK-DOMAIN.ngrok-free.app/api/slack/interactions
```

Short aliases:

```text
https://YOUR-NGROK-DOMAIN.ngrok-free.app/slack/events
https://YOUR-NGROK-DOMAIN.ngrok-free.app/slack/commands
https://YOUR-NGROK-DOMAIN.ngrok-free.app/slack/interactions
```

Set `API_BASE_URL` in `.env` to the same ngrok base URL when you want callback links to point at the tunnel.

## Slack App Configuration

Create a Slack app and configure:

- Event Subscriptions: enable events and set Request URL to `/api/slack/events`.
- Slash Commands: create `/wayfinder` and set Request URL to `/api/slack/commands`.
- Interactivity: enable and set Request URL to `/api/slack/interactions`.

Required bot scopes:

- `app_mentions:read`
- `channels:history`
- `channels:read`
- `chat:write`
- `commands`
- `groups:history`
- `groups:read`

Subscribe to bot events:

- `app_mention`
- `message.channels`
- `message.groups`

Install the app to the workspace, then copy values into `.env`:

```text
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
SLACK_DEFAULT_CHANNEL=...
SLACK_USE_SOCKET_MODE=false
```

Restart the API after changing `.env`:

```bash
docker compose up -d --build api worker
```

## Test From Slack

Slash command:

```text
/wayfinder plan a 3-day trip to San Diego for 4 people in August. Budget around $800 each.
```

Mention:

```text
@Wayfinder plan a 3-day trip to San Diego for 4 people in August. Budget around $800 each.
```

Wayfinder posts the preference prompt. Reply in that thread as different users. The API records replies, signals the Temporal workflow when available, and posts a "drafting" update once four preferences are collected.
