from app.orchestrators.base_orchestrator import BaseOrchestrator
from app.orchestrators.langgraph.langgraph import LangGraphOrchestrator
from app.orchestrators.models import OrchestratorName


class OrchestratorError(Exception):
    pass


def get_orchestrator(name: OrchestratorName) -> BaseOrchestrator:
    match name:
        case OrchestratorName.LANGGRAPH:
            return LangGraphOrchestrator()
        case _:
            raise OrchestratorError(f"Unsupported orchestrator: {name}")
