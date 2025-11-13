from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.database.models import RunStatus


class Agent(str, Enum):
    PO = "po"


class OrchestratorName(str, Enum):
    LANGGRAPH = "langgraph"
    AUTOGEN = "autogen"


class OrchestartorInput(BaseModel):
    requirement: str = Field(min_length=10, description="Plain-text project requirement")
    orchestrator: OrchestratorName
    human_approval_after: list[str] = Field(default_factory=list)


class POOutput(BaseModel):
    stories: list[str] = []
    acceptance_criteria: list[str] = []


class DevOutput(BaseModel):
    pr_url: str | None
    commit_id: str | None


class RunState(BaseModel):
    requirement: str
    input: dict[str, Any] = {}
    current_agent: str | None = None

    po_output: POOutput | None = None
    dev_output: DevOutput | None = None


class OrchestratorOutput(BaseModel):
    status: Literal["completed", "failed"]
    state: RunState


class ExecutionResult(BaseModel):
    run_id: str = Field(alias="id")
    orchestrator: OrchestratorName
    status: RunStatus
    created_at: datetime
    updated_at: datetime
    output_json: OrchestratorOutput | None = None

    model_config = {"from_attributes": True, "populate_by_name": True}
