from abc import ABC, abstractmethod

from app.orchestrators.models import (
    OrchestratorInput,
    OrchestratorResult,
)


class BaseOrchestrator(ABC):
    """
    Abstract interface for all orchestrator engines.
    """

    @abstractmethod
    async def execute(self, payload: OrchestratorInput) -> OrchestratorResult:
        """
        Execute the orchestration flow and return the final result.
        """
        raise NotImplementedError
