import httpx

from app.config import settings

from .models import ChatRequest, ChatResponse, LLMMessage


class LLMClient:
    """
    Generic client for any OpenAI-compatible endpoint.
    """

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
    ):
        self.base_url = base_url or settings.LLM_BASE_URL
        self.api_key = api_key or settings.LLM_API_KEY
        self.model = model or settings.LLM_MODEL

        if not self.base_url:
            raise ValueError("Missing LLM_BASE_URL in config")
        if not self.model:
            raise ValueError("Missing LLM_MODEL in config")

        self.headers = {
            "Content-Type": "application/json",
            **({"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}),
        }

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=30.0,
            headers=self.headers,
        )

    async def chat(self, request: ChatRequest) -> ChatResponse:
        payload = {
            "model": request.model or self.model,
            "messages": [msg.model_dump() for msg in request.messages],
        }

        if request.temperature is not None:
            payload["temperature"] = request.temperature
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        resp = await self._client.post("/v1/chat/completions", json=payload)
        resp.raise_for_status()
        data = resp.json()

        choice = data.get("choices", [{}])[0]
        message_dict = choice.get("message", {})

        message = LLMMessage(
            role=message_dict.get("role", "assistant"),
            content=message_dict.get("content", ""),
        )

        return ChatResponse(message=message, raw=data)
