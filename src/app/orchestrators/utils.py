from typing import Dict, Type

from app.orchestrators.base_orchestrator import BaseOrchestrator
from app.orchestrators.langgraph import LangGraphOrchestrator

ORCHESTRATORS: Dict[str, Type[BaseOrchestrator]] = {
    "langgraph": LangGraphOrchestrator,
}


def get_orchestrator(name: str) -> BaseOrchestrator:
    try:
        return ORCHESTRATORS[name.lower()]()
    except KeyError:
        raise ValueError(f"Unsupported orchestrator: {name}")
