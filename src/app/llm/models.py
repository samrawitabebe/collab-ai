from typing import Any, Literal

from pydantic import BaseModel, Field


class LLMMessage(BaseModel):
    """
    Represents a single OpenAI-compatible chat message.
    """

    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """
    Standardized request to any OpenAI-compatible /v1/chat/completions endpoint.
    """

    messages: list[LLMMessage]
    model: str | None = None
    temperature: float | None = Field(default=0.2)
    max_tokens: int | None = None


class ChatResponse(BaseModel):
    """
    Response object:
    - message: the assistant's message
    - raw: the entire raw API response for audit + Langfuse
    """

    message: LLMMessage
    raw: Any
