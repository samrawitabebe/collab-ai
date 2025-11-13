from abc import ABC, abstractmethod
from typing import Any

from app.orchestrators.models import OrchestartorInput


class BaseOrchestrator(ABC):
    """Base interface for all orchestrators."""

    @abstractmethod
    async def execute(self, payload: OrchestartorInput) -> dict[str, Any]:
        """Run orchestration flow and return results."""
        raise NotImplementedError
