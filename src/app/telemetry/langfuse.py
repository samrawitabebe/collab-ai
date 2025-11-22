from langfuse import Langfuse

from app.config import settings


def _init_client() -> Langfuse:
    """
    Initialize a single Langfuse client.
    """
    return Langfuse(
        secret_key=settings.LANGFUSE_SECRET_KEY,
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        base_url=settings.LANGFUSE_HOST,
    )


langfuse_client: Langfuse = _init_client()
