from fastapi import APIRouter, Header, HTTPException, Request

from wayfinder_api.config import get_settings
from wayfinder_api.schemas import TripCreateRequest
from wayfinder_api.services.audit_service import write_audit_event
from wayfinder_api.services.notion_service import (
    append_notion_thread_update,
    build_issue_page_title,
    create_notion_issue_page,
)
from wayfinder_api.services.slack_service import (
    build_preference_prompt,
    build_draft_ready_summary,
    parse_interaction_payload,
    parse_slash_command,
    parse_wayfinder_command,
    post_slack_message,
    record_thread_preference,
    validate_slack_signature,
)
from wayfinder_api.services.temporal_client import (
    signal_participant_preference,
    start_trip_workflow,
    trip_id_for_thread,
)

router = APIRouter(tags=["slack"])
THREAD_NOTION_INDEX: dict[str, dict[str, str]] = {}


@router.post("/api/slack/events")
@router.post("/slack/events")
async def slack_events(
    request: Request,
    x_slack_request_timestamp: str | None = Header(default=None),
    x_slack_signature: str | None = Header(default=None),
) -> dict:
    body = await request.body()
    settings = get_settings()
    if settings.slack_signing_secret and not validate_slack_signature(
        settings.slack_signing_secret,
        x_slack_request_timestamp or "",
        body,
        x_slack_signature or "",
    ):
        raise HTTPException(status_code=401, detail="Invalid Slack signature")
    payload = await request.json()
    if payload.get("type") == "url_verification":
        return {"challenge": payload.get("challenge")}
    event = payload.get("event", {})
    event_type = event.get("type")
    if event_type == "message" and not event.get("bot_id"):
        thread_ts = event.get("thread_ts")
        trip_id = trip_id_for_thread(thread_ts)
        if trip_id and event.get("text"):
            preferences = record_thread_preference(thread_ts, event.get("user", "unknown"), event["text"])
            await signal_participant_preference(trip_id, event.get("user", "unknown"), event["text"])
            notion_mapping = THREAD_NOTION_INDEX.get(thread_ts or "")
            notion_append = await append_notion_thread_update(
                api_key=settings.notion_api_key,
                page_id=notion_mapping.get("page_id") if notion_mapping else None,
                slack_user_id=event.get("user", "unknown"),
                text=event["text"],
            )
            await write_audit_event(
                "ISSUE_THREAD_UPDATE_RECEIVED",
                actor_type="slack_user",
                details={
                    "slack_user_id": event.get("user"),
                    "text": event.get("text"),
                    "notion_append": notion_append,
                },
                trip_run_id=trip_id,
            )
            notion_note = (
                " I also appended it to the Notion brief."
                if notion_append.get("ok")
                else f" Notion append skipped: {notion_append.get('error')}"
            )
            await post_slack_message(
                settings.slack_bot_token,
                event.get("channel"),
                f"Got it — I recorded <@{event.get('user')}> update. I have {len(preferences)} thread update(s) so far.{notion_note}",
                thread_ts=thread_ts,
            )
            if len(preferences) >= 4:
                await post_slack_message(
                    settings.slack_bot_token,
                    event.get("channel"),
                    build_draft_ready_summary(preferences),
                    thread_ts=thread_ts,
                )
        return {"ok": True}

    command = parse_wayfinder_command(event.get("text", ""))
    if event_type == "app_mention" and command:
        thread_ts = event.get("thread_ts") or event.get("ts")
        trip = await start_trip_workflow(
            TripCreateRequest(
                original_request=command,
                source="slack_mention",
            ),
            slack_channel_id=event.get("channel"),
            slack_thread_ts=thread_ts,
        )
        await write_audit_event(
            "ISSUE_DOC_REQUEST_RECEIVED",
            actor_type="slack_user",
            details={"source": "app_mention", "text": command},
            trip_run_id=str(trip.id),
        )
        await post_slack_message(
            settings.slack_bot_token,
            event.get("channel"),
            build_preference_prompt(),
            thread_ts=thread_ts,
        )
        return {"ok": True, "trip_id": str(trip.id)}
    return {"ok": True}


@router.post("/api/slack/interactions")
@router.post("/slack/interactions")
async def slack_interactions(
    request: Request,
    x_slack_request_timestamp: str | None = Header(default=None),
    x_slack_signature: str | None = Header(default=None),
) -> dict:
    body = await request.body()
    settings = get_settings()
    if settings.slack_signing_secret and not validate_slack_signature(
        settings.slack_signing_secret,
        x_slack_request_timestamp or "",
        body,
        x_slack_signature or "",
    ):
        raise HTTPException(status_code=401, detail="Invalid Slack signature")
    payload = parse_interaction_payload(body)
    action_id = payload.get("actions", [{}])[0].get("action_id")
    return {"ok": True, "action_id": action_id}


@router.post("/api/slack/commands")
@router.post("/slack/commands")
async def slack_commands(
    request: Request,
    x_slack_request_timestamp: str | None = Header(default=None),
    x_slack_signature: str | None = Header(default=None),
) -> dict:
    body = await request.body()
    settings = get_settings()
    if settings.slack_signing_secret and not validate_slack_signature(
        settings.slack_signing_secret,
        x_slack_request_timestamp or "",
        body,
        x_slack_signature or "",
    ):
        raise HTTPException(status_code=401, detail="Invalid Slack signature")
    command = parse_slash_command(body)
    if not command.text:
        return {
            "response_type": "ephemeral",
            "text": "Try `/wayfinder plan a 3-day trip to San Diego for 4 people in August`.",
        }

    trip = await start_trip_workflow(
        TripCreateRequest(original_request=command.text, source="slack_slash_command"),
        slack_channel_id=command.channel_id,
    )
    await write_audit_event(
        "ISSUE_DOC_REQUEST_RECEIVED",
        actor_type="slack_user",
        details={"source": "slash_command", "text": command.text},
        trip_run_id=str(trip.id),
    )
    intro = build_preference_prompt()
    slack_response = await post_slack_message(
        settings.slack_bot_token,
        command.channel_id,
        intro,
    )
    thread_ts = slack_response.get("ts")
    if thread_ts:
        from wayfinder_api.services.temporal_client import TRIP_THREAD_INDEX

        TRIP_THREAD_INDEX[thread_ts] = str(trip.id)
    notion_response = await create_notion_issue_page(
        api_key=settings.notion_api_key,
        parent_page_id=settings.notion_parent_page_id,
        trip_database_id=settings.notion_trip_database_id,
        title=build_issue_page_title(command.text),
        run_id=str(trip.id),
        issue_context=command.text,
    )
    notion_line = (
        f"Notion draft: {notion_response['url']}"
        if notion_response.get("ok") and notion_response.get("url")
        else f"Notion draft not created: {notion_response.get('error')}"
    )
    if slack_response.get("ok"):
        if thread_ts and notion_response.get("ok"):
            THREAD_NOTION_INDEX[thread_ts] = {
                "page_id": notion_response.get("page_id", ""),
                "url": notion_response.get("url", ""),
            }
        return {
            "response_type": "ephemeral",
            "text": f"ThreadBrief started issue brief `{trip.id}` and posted the thread prompt. {notion_line}",
        }

    slack_error = slack_response.get("error", "unknown_error")
    return {
        "response_type": "in_channel",
        "text": (
            f"ThreadBrief started issue brief `{trip.id}`, but I could not post a separate channel message "
            f"through `chat.postMessage` (`{slack_error}`).\n\n"
            f"{intro}\n\n"
            f"{notion_line}\n\n"
            "If the Slack error is `not_in_channel`, invite the app to this channel with `/invite @WayFinder`."
        ),
    }
