from abc import ABC, abstractmethod

from app.orchestrators.models import OrchestartorInput, OrchestratorOutput


class BaseOrchestrator(ABC):
    """Base interface for all orchestrators."""

    @abstractmethod
    async def execute(self, payload: OrchestartorInput) -> OrchestratorOutput:
        """Run orchestration flow and return results."""
        raise NotImplementedError
