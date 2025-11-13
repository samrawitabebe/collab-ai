import asyncio

from langgraph.graph import END, StateGraph

from app.orchestrators.base_orchestrator import BaseOrchestrator
from app.orchestrators.models import DevOutput, OrchestartorInput, OrchestratorOutput, POOutput, RunState


async def po_agent_node(state: RunState) -> RunState:
    await asyncio.sleep(2)

    po_output = POOutput(
        stories=[f"Story: {state.requirement}"],
        acceptance_criteria=[
            "Requirement is understood",
            "Solution meets functional expectations",
        ],
    )

    new_input = {**state.input, "po_summary": "Stories + acceptance criteria ready"}

    return RunState(
        requirement=state.requirement,
        input=new_input,
        current_agent="po_agent",
        po_output=po_output,
        dev_output=state.dev_output,
    )


async def dev_agent_node(state: RunState) -> RunState:
    await asyncio.sleep(2)

    dev_output = DevOutput(
        pr_url="https://github.com/org/repo/pull/123",
        commit_id="mock-commit-abc123",
    )

    new_input = {
        **state.input,
        "dev_summary": "Development done. PR created.",
    }

    return RunState(
        requirement=state.requirement,
        input=new_input,
        current_agent="dev_agent",
        po_output=state.po_output,
        dev_output=dev_output,
    )


class LangGraphOrchestrator(BaseOrchestrator):
    async def execute(self, payload: OrchestartorInput) -> OrchestratorOutput:
        graph = StateGraph(RunState)

        graph.add_node("po_agent", _wrap_agent(po_agent_node))
        graph.add_node("dev_agent", _wrap_agent(dev_agent_node))

        graph.set_entry_point("po_agent")
        graph.add_edge("po_agent", "dev_agent")
        graph.add_edge("dev_agent", END)

        app = graph.compile()

        initial_state = RunState(requirement=payload.requirement, input={})

        final_state = await app.ainvoke(initial_state)

        return OrchestratorOutput(
            status="completed",
            state=RunState.model_validate(final_state),
        )


def _wrap_agent(fn):
    async def wrapper(state: RunState) -> dict:
        new_state = await fn(state)
        return new_state.model_dump()

    return wrapper
