from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    wayfinder_base_url: str = "http://localhost:5173"
    api_base_url: str = "http://localhost:8000"
    database_url: str = "postgresql+asyncpg://wayfinder:wayfinder@postgres:5432/wayfinder"
    temporal_address: str = "temporal:7233"
    temporal_namespace: str = "default"
    temporal_task_queue: str = "wayfinder-task-queue"
    otel_service_name: str = "wayfinder-api"
    jaeger_otlp_endpoint: str = "http://jaeger:4318/v1/traces"
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    planner_mode: str = "openai"
    slack_bot_token: str = ""
    slack_signing_secret: str = ""
    slack_app_token: str = ""
    slack_default_channel: str = ""
    slack_use_socket_mode: bool = True
    notion_api_key: str = ""
    notion_parent_page_id: str = ""
    notion_trip_database_id: str = ""
    overpass_api_url: str = "https://overpass-api.de/api/interpreter"
    demo_input_mode: str = "manual"
    demo_fast_timers: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
