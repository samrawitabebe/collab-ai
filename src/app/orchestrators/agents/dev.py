from .models import DeveloperInput, DeveloperOutput


async def run_developer_agent(data: DeveloperInput) -> DeveloperOutput:
    """
    Dummy Dev agent.
    Does not call an LLM. Simply returns structured placeholder output.
    """
    return DeveloperOutput(
        summary=(
            "Developer agent placeholder. "
            f"Received story: '{data.story}', "
            f"{len(data.tasks)} tasks, "
            f"{len(data.acceptance_criteria)} acceptance criteria."
        )
    )
