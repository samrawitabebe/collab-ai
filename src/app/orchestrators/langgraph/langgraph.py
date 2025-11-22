from langfuse import observe, propagate_attributes
from langgraph.graph import END, StateGraph

from app.orchestrators.agents.dev import run_developer_agent
from app.orchestrators.agents.models import DeveloperInput, ProductOwnerInput
from app.orchestrators.agents.po import run_product_owner_agent
from app.orchestrators.base_orchestrator import BaseOrchestrator
from app.orchestrators.langgraph.models import ExecutionState, StepName
from app.orchestrators.models import OrchestratorInput, OrchestratorResult
from app.telemetry.langfuse import langfuse_client


@observe(name="product_owner_agent")
async def product_owner_node(state: dict) -> dict:
    """
    Product Owner step: converts requirement → story/criteria/tasks.
    """
    input_model = ProductOwnerInput(requirement=state["requirement"])

    po_output = await run_product_owner_agent(input_model)

    return {
        **state,
        "current_step": StepName.PRODUCT_OWNER,
        "product_owner_output": po_output.model_dump(),
    }


@observe(name="developer_agent")
async def developer_node(state: dict) -> dict:
    """
    Developer step: produces implementation summary for MVP.
    """
    if "product_owner_output" not in state or state["product_owner_output"] is None:
        # When fully implemented, an agent will detect and resolve this .
        raise RuntimeError("Developer step invoked before Product Owner output.")

    po_output = state["product_owner_output"]

    dev_input = DeveloperInput(
        story=po_output["story"],
        acceptance_criteria=po_output["acceptance_criteria"],
        tasks=po_output["tasks"],
    )

    dev_output = await run_developer_agent(dev_input)

    return {
        **state,
        "current_step": StepName.DEVELOPER,
        "developer_output": dev_output.model_dump(),
    }


class LangGraphOrchestrator(BaseOrchestrator):
    async def execute(self, payload: OrchestratorInput) -> OrchestratorResult:
        """
        requirement → ProductOwner → Developer → END
        """

        with langfuse_client.start_as_current_span(
            name="langgraph_execution",
            input=payload.model_dump(),
        ) as root_span:
            with propagate_attributes(tags=["orchestrator", "langgraph"]):
                graph = StateGraph(dict)

                graph.add_node("product_owner_node", product_owner_node)
                graph.add_node("developer_node", developer_node)

                graph.set_entry_point("product_owner_node")
                graph.add_edge("product_owner_node", "developer_node")
                graph.add_edge("developer_node", END)

                app = graph.compile()

                initial_state = {
                    "requirement": payload.requirement,
                    "current_step": None,
                    "product_owner_output": None,
                    "developer_output": None,
                }

                final_state_dict = await app.ainvoke(initial_state)
                final_state = ExecutionState.model_validate(final_state_dict)

                root_span.update_trace(output=final_state.model_dump())

                return OrchestratorResult(
                    requirement=final_state.requirement,
                    current_step=final_state.current_step,
                    product_owner_output=final_state.product_owner_output,
                    developer_output=final_state.developer_output,
                )
