from enum import Enum
from typing import List

from pydantic import BaseModel, Field


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
