import asyncio
from typing import Any

from app.models.base import ExecutionRequest
from app.orchestrators.base import Orchestrator


class LangGraphOrchestrator(Orchestrator):
    async def execute(self, payload: ExecutionRequest) -> dict[str, Any]:
        """Simulate LangGraph execution flow."""
        await asyncio.sleep(10)
        return {
            "status": "completed",
            "details": {
                "message": "LangGraph flow executed successfully.",
                "input_summary": str(payload)[:100],
            },
        }
