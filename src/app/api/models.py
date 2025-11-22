from datetime import datetime

from pydantic import BaseModel, Field

from app.database.models import ExecutionStatus
from app.orchestrators.models import (
    OrchestratorName,
    OrchestratorResult,
)


class ExecutionRequest(BaseModel):
    """
    Schema for POST /v1/executions
    """

    requirement: str = Field(min_length=3)
    orchestrator: OrchestratorName = OrchestratorName.LANGGRAPH
    human_approval_after: list[str] = Field(default_factory=list)


class ExecutionResponse(BaseModel):
    """
    Immediate response from POST /v1/executions.
    """

    id: str
    status: ExecutionStatus
    orchestrator: OrchestratorName
    created_at: datetime


class ExecutionResult(BaseModel):
    """
    Response model for GET /v1/executions/{id}.
    """

    execution_id: str = Field(alias="id")
    orchestrator: OrchestratorName
    status: ExecutionStatus
    created_at: datetime
    updated_at: datetime
    result: OrchestratorResult | None = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
