from abc import ABC, abstractmethod
from typing import Any

from app.models.base import ExecutionRequest


class Orchestrator(ABC):
    """Base interface for all orchestrators."""

    @abstractmethod
    async def execute(self, payload: ExecutionRequest) -> dict[str, Any]:
        """Run orchestration flow and return results."""
        raise NotImplementedError
