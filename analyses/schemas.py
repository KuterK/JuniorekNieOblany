from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ANALYSIS_SCHEMA_VERSION = 1


class CodeAnalysisV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    language: str = Field(min_length=1, max_length=50)
    title: str = Field(min_length=1, max_length=200)
    short_description: str
    tags: list[str] = Field(max_length=10)
    summary: str
    explanation: str
    concepts: str
    pitfalls: str
    junior_explanation: str
