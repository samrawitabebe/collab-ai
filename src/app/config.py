from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    DATABASE_URL: str = "sqlite:///./collab_ai.db"

    LLM_BASE_URL: str = Field(default="", description="Base URL for CERIT/local OpenAI-compatible API")
    LLM_API_KEY: str = Field(default="", description="API key for OpenAI-compatible LLM")
    LLM_MODEL: str = Field(default="", description="Default model name for LLM")

    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_HOST: str = ""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
