from wayfinder_api.config import get_settings


async def get_integration_status() -> dict:
    settings = get_settings()
    return {
        "openai": "configured" if settings.openai_api_key else "not_configured",
        "slack": "configured" if settings.slack_bot_token else "not_configured",
        "notion": "configured" if settings.notion_api_key else "not_configured",
        "temporal": "configured",
        "postgresql": "configured",
        "jaeger": "configured",
        "openstreetmap_overpass": "configured",
        "wikidata": "optional",
        "wikivoyage": "optional",
    }
