from enum import Enum
from typing import Dict, Type

from app.orchestrators.base import Orchestrator
from app.orchestrators.langgraph import LangGraphOrchestrator

ORCHESTRATORS: Dict[str, Type[Orchestrator]] = {
    "langgraph": LangGraphOrchestrator,
}


def get_orchestrator(name: str) -> Orchestrator:
    try:
        return ORCHESTRATORS[name.lower()]()
    except KeyError:
        raise ValueError(f"Unsupported orchestrator: {name}")


class Agent(str, Enum):
    PO = "po"
