from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class OrchestratorName(str, Enum):
    LANGGRAPH = "langgraph"
    AUTOGEN = "autogen"


class ExecutionRequest(BaseModel):
    requirement: str = Field(min_length=10, description="Plain-text project requirement")
    orchestrator: OrchestratorName
    human_approval_after: List[str] = Field(default_factory=list)


class ExecutionResponse(BaseModel):
    run_id: str
    message: str = "Execution scheduled"


class ExecutionResult(BaseModel):
    run_id: str = Field(alias="id")
    orchestrator: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
