from __future__ import annotations

from enum import StrEnum
from typing import Any, TypeVar

from pydantic import BaseModel, Field


class RiskLevel(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class ApprovalBehavior(BaseModel):
    required: bool = False
    reason: str | None = None


class RetryPolicy(BaseModel):
    max_attempts: int = 3
    backoff_seconds: int = 2


class ToolMetadata(BaseModel):
    name: str
    description: str
    risk_level: RiskLevel
    approval: ApprovalBehavior = Field(default_factory=ApprovalBehavior)
    idempotency: str
    retry: RetryPolicy = Field(default_factory=RetryPolicy)
    integration_name: str
    version: str = "0.1.0"


InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)


class WayfinderTool(BaseModel):
    metadata: ToolMetadata
    input_schema: type[BaseModel]
    output_schema: type[BaseModel]

    model_config = {"arbitrary_types_allowed": True}

    async def ainvoke(self, payload: BaseModel) -> BaseModel:
        return self.output_schema(result={"echo": payload.model_dump()})

    def public_descriptor(self) -> dict[str, Any]:
        return {
            **self.metadata.model_dump(mode="json"),
            "input_schema": self.input_schema.model_json_schema(),
            "output_schema": self.output_schema.model_json_schema(),
        }
