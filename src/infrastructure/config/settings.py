"""Application settings module."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    # Telegram
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

    # OpenAI
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    use_openai: bool = os.getenv("USE_OPENAI", "false").lower() == "true"

    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    use_redis: bool = os.getenv("USE_REDIS", "false").lower() == "true"

    # Application
    default_profession: str = os.getenv("DEFAULT_PROFESSION", "Python Developer")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    environment: str = os.getenv("ENVIRONMENT", "development")

    # Paths
    knowledge_base_path: Path = Path(
        os.getenv("KNOWLEDGE_BASE_PATH", "knowledge_base.xlsx")
    )

    # Available professions
    professions: list = [
        "Python Developer",
        "DevOps / SRE",
        "Project Manager",
        "Team Lead",
        "UX/UI Designer",
        "Copywriter",
    ]

    class Config:
        env_file = ".env"
        extra = "ignore"

    def validate(self) -> None:
        """Validate required settings."""
        if not self.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")

        if not self.knowledge_base_path.exists():
            raise FileNotFoundError(
                f"Knowledge base not found: {self.knowledge_base_path}"
            )


# Global settings instance
settings = Settings()
