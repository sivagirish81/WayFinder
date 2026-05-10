import hashlib
import hmac
import json
import logging
import time
from dataclasses import dataclass
from urllib.parse import parse_qs

import httpx

logger = logging.getLogger(__name__)


def validate_slack_signature(signing_secret: str, timestamp: str, body: bytes, signature: str) -> bool:
    if not signing_secret:
        return False
    if abs(time.time() - int(timestamp or "0")) > 60 * 5:
        return False
    basestring = b"v0:" + timestamp.encode() + b":" + body
    digest = hmac.new(signing_secret.encode(), basestring, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"v0={digest}", signature)


def parse_wayfinder_command(text: str) -> str | None:
    lowered = text.lower()
    if "/wayfinder" in lowered:
        return text.split("/wayfinder", 1)[-1].strip()
    if "wayfinder" in lowered and "plan" in lowered:
        cleaned = text.replace("@Wayfinder", "").replace("@wayfinder", "").strip()
        return cleaned or text
    return None


@dataclass(frozen=True)
class SlackCommandPayload:
    command: str
    text: str
    user_id: str
    channel_id: str
    response_url: str | None
    trigger_id: str | None


THREAD_PREFERENCES: dict[str, list[dict[str, str]]] = {}


def parse_slack_form_body(body: bytes) -> dict[str, str]:
    parsed = parse_qs(body.decode(), keep_blank_values=True)
    return {key: values[0] if values else "" for key, values in parsed.items()}


def parse_slash_command(body: bytes) -> SlackCommandPayload:
    form = parse_slack_form_body(body)
    return SlackCommandPayload(
        command=form.get("command", ""),
        text=form.get("text", "").strip(),
        user_id=form.get("user_id", ""),
        channel_id=form.get("channel_id", ""),
        response_url=form.get("response_url") or None,
        trigger_id=form.get("trigger_id") or None,
    )


async def post_slack_message(
    bot_token: str,
    channel_id: str,
    text: str,
    thread_ts: str | None = None,
    blocks: list[dict] | None = None,
) -> dict:
    if not bot_token:
        return {
            "ok": False,
            "error": "SLACK_BOT_TOKEN is not configured",
            "channel": channel_id,
            "ts": None,
        }
    payload: dict = {"channel": channel_id, "text": text}
    if thread_ts:
        payload["thread_ts"] = thread_ts
    if blocks:
        payload["blocks"] = blocks
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": f"Bearer {bot_token}", "Content-Type": "application/json"},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        if not data.get("ok"):
            logger.warning("Slack chat.postMessage failed: %s", data)
            return data
        logger.info(
            "Slack chat.postMessage succeeded channel=%s ts=%s",
            data.get("channel"),
            data.get("ts"),
        )
        return data


async def post_response_url(response_url: str | None, text: str, response_type: str = "ephemeral") -> None:
    if not response_url:
        return
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(response_url, json={"response_type": response_type, "text": text})


def build_preference_prompt() -> str:
    return (
        "I'll turn this Slack thread into a detailed Notion issue brief. Reply here with evidence, proposals, and concerns.\n\n"
        "Please share:\n"
        "1. What is the concrete issue or symptom?\n"
        "2. Suspected or confirmed root cause\n"
        "3. Proposed fixes or mitigations\n"
        "4. Risks, rollback concerns, or edge cases\n"
        "5. Owners, decisions, and open questions"
    )


def record_thread_preference(thread_ts: str, slack_user_id: str, text: str) -> list[dict[str, str]]:
    preferences = THREAD_PREFERENCES.setdefault(thread_ts, [])
    if not any(item["slack_user_id"] == slack_user_id and item["text"] == text for item in preferences):
        preferences.append({"slack_user_id": slack_user_id, "text": text})
    return preferences


def build_draft_ready_summary(preferences: list[dict[str, str]]) -> str:
    return (
        f"Thanks — I have {len(preferences)} thread update(s). "
        "I'm expanding the Notion issue brief with the discussion, proposed fixes, risks, and open questions."
    )


def parse_interaction_payload(body: bytes) -> dict:
    form = parse_slack_form_body(body)
    raw_payload = form.get("payload", "{}")
    return json.loads(raw_payload)
