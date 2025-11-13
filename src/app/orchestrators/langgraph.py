import asyncio
from typing import Any

from langgraph.graph import END, StateGraph

from app.models.base import ExecutionRequest
from app.orchestrators.base import Orchestrator


async def po_agent_node(state: dict[str, Any]) -> dict[str, Any]:
    await asyncio.sleep(5)
    return {
        "message": f"PO Agent processed orchestrator '{state.get('orchestrator')}'",
        "input_summary": str(state)[:100],
    }


class LangGraphOrchestrator(Orchestrator):
    async def execute(self, payload: ExecutionRequest) -> dict[str, Any]:
        graph = StateGraph(dict)

        graph.add_node("po_agent", po_agent_node)
        graph.set_entry_point("po_agent")
        graph.add_edge("po_agent", END)

        app = graph.compile()

        result = await app.ainvoke(payload.model_dump())

        return {
            "message": "PO agent executed successfully",
            "result": result,
        }
