from functools import lru_cache

from .client import LLMClient


@lru_cache
def get_llm() -> LLMClient:
    """
    Returns a singleton, cached LLMClient instance.
    """
    return LLMClient()
