from functools import lru_cache

from openai import OpenAI
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .schemas import CodeAnalysisV1

SYSTEM_PROMPT = """
Jesteś mentorem programowania. Analizujesz wyłącznie przekazany kod.
Zwróć JSON zgodny ze schematem. Nie generuj poprawionego ani nowego kodu.
Wyjaśnienia mają być konkretne, bezpieczne i zrozumiałe dla junior developera.
"""


class AISettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_key: str = Field(validation_alias=AliasChoices("OPENAI_API_KEY", "OPENROUTER_API_KEY"))
    base_url: str = Field(
        default="https://openrouter.ai/api/v1", validation_alias="OPENAI_BASE_URL"
    )
    model: str = Field(default="openai/gpt-5-mini", validation_alias="OPENAI_MODEL")


@lru_cache
def get_ai_settings() -> AISettings:
    return AISettings()  # type: ignore[call-arg]


def analyze_code(code: str) -> CodeAnalysisV1:
    settings = get_ai_settings()
    client = OpenAI(api_key=settings.api_key, base_url=settings.base_url, timeout=12.0)
    response = client.chat.completions.parse(
        model=settings.model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": code},
        ],
        response_format=CodeAnalysisV1,
    )
    parsed = response.choices[0].message.parsed
    if parsed is None:
        raise RuntimeError("Dostawca AI nie zwrócił poprawnej analizy.")
    return parsed
