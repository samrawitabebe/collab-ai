from app.llm.models import ChatRequest, LLMMessage
from app.llm.utils import get_llm

from .models import ProductOwnerInput, ProductOwnerOutput

SYSTEM_PROMPT = """
    You are a Product Owner agent.
    Your job is to transform a raw requirement into:
    1. A clear user story.
    2. A list of acceptance criteria.
    3. A list of implementation tasks.

    Output MUST be valid JSON with keys:
    - story: string
    - acceptance_criteria: list of strings
    - tasks: list of strings

    Do NOT include explanation or commentary.
    Return ONLY pure JSON.
    Do NOT use ```json``` or any code block formatting.
"""


async def run_product_owner_agent(data: ProductOwnerInput) -> ProductOwnerOutput:
    """
    Executes the Product Owner agent pipeline using the OpenAI-compatible LLM.
    """
    llm = get_llm()

    request = ChatRequest(
        messages=[
            LLMMessage(role="system", content=SYSTEM_PROMPT),
            LLMMessage(role="user", content=data.requirement),
        ]
    )

    response = await llm.chat(request)

    try:
        parsed = response.message.content.strip()
        print(f"[PO AGENT] Raw output: {parsed}")
    except Exception as e:
        raise ValueError(f"PO agent returned invalid JSON. Raw output: {response.message.content}") from e

    return ProductOwnerOutput.model_validate_json(parsed)
