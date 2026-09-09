import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str
    model: str
    temperature: float
    max_steps: int


def load_settings() -> Settings:
    api_key = os.getenv("LLM_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "Missing LLM_API_KEY. Copy .env.example to .env and fill in your API key."
        )

    return Settings(
        api_key=api_key,
        base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com").strip(),
        model=os.getenv("LLM_MODEL", "deepseek-chat").strip(),
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
        max_steps=int(os.getenv("AGENT_MAX_STEPS", "8")),
    )
