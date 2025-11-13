from datetime import datetime
from enum import Enum
from typing import Any, List

from pydantic import BaseModel, ConfigDict, Field

from app.models.db import RunStatus


class OrchestratorName(str, Enum):
    LANGGRAPH = "langgraph"
    AUTOGEN = "autogen"


class OrchestratorOutput(BaseModel):
    message: str
    result: dict[str, Any]


class ExecutionRequest(BaseModel):
    requirement: str = Field(min_length=10, description="Plain-text project requirement")
    orchestrator: OrchestratorName
    human_approval_after: List[str] = Field(default_factory=list)


class ExecutionResponse(BaseModel):
    run_id: str
    message: str = "Execution scheduled"


class ExecutionResult(BaseModel):
    run_id: str = Field(alias="id")
    orchestrator: OrchestratorName
    status: RunStatus
    created_at: datetime
    updated_at: datetime
    output_json: OrchestratorOutput | None = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
