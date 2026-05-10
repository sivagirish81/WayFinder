# Slack Setup

ThreadBrief can be tested directly from Slack through Slack HTTP events and slash commands. Slack must reach a public HTTPS URL, so local testing needs a tunnel.

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
/wayfinder document this issue: deploy caused API 500s after the cache migration. We need root cause, fix options, risks, and owners.
```

Mention:

```text
@Wayfinder document this issue: deploy caused API 500s after the cache migration.
```

ThreadBrief posts an issue-documentation prompt and creates a Notion issue brief. Reply in that thread with root-cause evidence, proposed fixes, risks, owners, and open questions. The API records replies, appends them to the Notion brief when configured, signals the Temporal workflow when available, and acknowledges every captured thread update.
