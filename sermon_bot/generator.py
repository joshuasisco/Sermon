"""Core sermon generation logic using AI models."""

from typing import Optional

from .config import Config
from .prompts import (
    SYSTEM_PROMPT,
    SERMON_FROM_VERSE_PROMPT,
    SERMON_FROM_TOPIC_PROMPT,
    OUTLINE_PROMPT,
    ILLUSTRATION_PROMPT,
    SCRIPTURE_SUGGESTIONS_PROMPT,
    SERMON_SERIES_PROMPT,
    PRAYER_PROMPT,
)


class SermonGenerator:
    """Generate sermons and related content using AI models."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator with configuration."""
        self.config = config or Config.load()
        self._client = None

    def _get_client(self):
        """Get or create the AI client."""
        if self._client is None:
            if self.config.ai_provider == "anthropic":
                import anthropic
                self._client = anthropic.Anthropic(
                    api_key=self.config.anthropic_api_key
                )
            elif self.config.ai_provider == "openai":
                import openai
                self._client = openai.OpenAI(
                    api_key=self.config.openai_api_key
                )
        return self._client

    def _generate(self, user_prompt: str, system_prompt: str = SYSTEM_PROMPT) -> str:
        """Generate content using the configured AI provider."""
        client = self._get_client()

        if self.config.ai_provider == "anthropic":
            response = client.messages.create(
                model=self.config.default_model,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.content[0].text

        elif self.config.ai_provider == "openai":
            response = client.chat.completions.create(
                model=self.config.default_model,
                max_tokens=4096,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content

        raise ValueError(f"Unsupported AI provider: {self.config.ai_provider}")

    def generate_sermon_from_verse(
        self,
        scripture: str,
        length: str = "20-25 minutes"
    ) -> str:
        """Generate a complete sermon from a Bible verse or passage."""
        prompt = SERMON_FROM_VERSE_PROMPT.format(
            scripture=scripture,
            length=length
        )
        return self._generate(prompt)

    def generate_sermon_from_topic(
        self,
        topic: str,
        length: str = "20-25 minutes"
    ) -> str:
        """Generate a complete sermon on a specific topic."""
        prompt = SERMON_FROM_TOPIC_PROMPT.format(
            topic=topic,
            length=length
        )
        return self._generate(prompt)

    def generate_outline(
        self,
        input_value: str,
        is_verse: bool = True
    ) -> str:
        """Generate a sermon outline from a verse or topic."""
        input_type = "Scripture" if is_verse else "Topic"
        prompt = OUTLINE_PROMPT.format(
            input_type=input_type,
            input_value=input_value
        )
        return self._generate(prompt)

    def generate_illustrations(
        self,
        topic: str,
        scripture: str = ""
    ) -> str:
        """Generate sermon illustrations for a topic."""
        prompt = ILLUSTRATION_PROMPT.format(
            topic=topic,
            scripture=scripture or "Not specified"
        )
        return self._generate(prompt)

    def suggest_scriptures(self, topic: str) -> str:
        """Suggest relevant Bible passages for a sermon topic."""
        prompt = SCRIPTURE_SUGGESTIONS_PROMPT.format(topic=topic)
        return self._generate(prompt)

    def generate_sermon_series(
        self,
        theme: str,
        count: int = 4
    ) -> str:
        """Generate a sermon series plan."""
        prompt = SERMON_SERIES_PROMPT.format(
            theme=theme,
            count=count
        )
        return self._generate(prompt)

    def generate_prayers(
        self,
        topic: str,
        scripture: str = ""
    ) -> str:
        """Generate prayers to accompany a sermon."""
        prompt = PRAYER_PROMPT.format(
            topic=topic,
            scripture=scripture or "Not specified"
        )
        return self._generate(prompt)

    def custom_request(self, request: str) -> str:
        """Handle a custom sermon-related request."""
        return self._generate(request)
