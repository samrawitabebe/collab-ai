from enum import Enum

from pydantic import BaseModel, Field

from app.orchestrators.agents.models import DeveloperOutput, ProductOwnerOutput
from app.orchestrators.langgraph.models import ExecutionState, StepName


class OrchestratorName(str, Enum):
    LANGGRAPH = "langgraph"


class OrchestratorInput(BaseModel):
    requirement: str = Field(min_length=5)
    orchestrator: OrchestratorName
    human_approval_after: list[str] = Field(default_factory=list)


class OrchestratorResult(BaseModel):
    requirement: str
    current_step: StepName | None = None

    product_owner_output: ProductOwnerOutput | None = None
    developer_output: DeveloperOutput | None = None

    @classmethod
    def from_execution_state(cls, state: ExecutionState) -> "OrchestratorResult":
        return cls(
            requirement=state.requirement,
            current_step=state.current_step,
            product_owner_output=state.product_owner_output,
            developer_output=state.developer_output,
        )
