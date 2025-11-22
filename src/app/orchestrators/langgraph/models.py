from enum import Enum

from pydantic import BaseModel

from app.orchestrators.agents.models import DeveloperOutput, ProductOwnerOutput


class StepName(str, Enum):
    """
    Every node in the LangGraph workflow.
    For debugging and auditing.
    """

    PRODUCT_OWNER = "PRODUCT_OWNER"
    DEVELOPER = "DEVELOPER"
    COMPLETE = "complete"


class ExecutionState(BaseModel):
    requirement: str
    current_step: StepName | None = None

    product_owner_output: ProductOwnerOutput | None = None
    developer_output: DeveloperOutput | None = None
