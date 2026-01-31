"""Configuration management for Sermon AI Bot."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass
class Config:
    """Application configuration."""

    ai_provider: str
    anthropic_api_key: Optional[str]
    openai_api_key: Optional[str]
    default_model: str

    @classmethod
    def load(cls) -> "Config":
        """Load configuration from environment variables."""
        load_dotenv()

        ai_provider = os.getenv("AI_PROVIDER", "anthropic").lower()

        return cls(
            ai_provider=ai_provider,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            default_model=os.getenv(
                "DEFAULT_MODEL",
                "claude-sonnet-4-20250514" if ai_provider == "anthropic" else "gpt-4o"
            ),
        )

    def validate(self) -> bool:
        """Validate that required API keys are present."""
        if self.ai_provider == "anthropic":
            return bool(self.anthropic_api_key)
        elif self.ai_provider == "openai":
            return bool(self.openai_api_key)
        return False

    def get_api_key(self) -> Optional[str]:
        """Get the API key for the configured provider."""
        if self.ai_provider == "anthropic":
            return self.anthropic_api_key
        elif self.ai_provider == "openai":
            return self.openai_api_key
        return None
