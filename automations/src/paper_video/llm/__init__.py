"""Vendor-neutral structured generation.

Every pipeline stage asks for a pydantic model; a provider only has to turn
(system prompt, user prompt, JSON schema, images) into a JSON object.
"""

import copy
from pathlib import Path
from typing import Protocol, TypeVar

from pydantic import BaseModel, ValidationError

from paper_video.config import LLMConfig

M = TypeVar("M", bound=BaseModel)

# Validation keywords that structured-output grammars commonly reject. They are
# stripped from the schema sent to the model and enforced by pydantic afterwards.
_UNSUPPORTED = {
    "minLength", "maxLength", "pattern", "minimum", "maximum", "exclusiveMinimum",
    "exclusiveMaximum", "minItems", "maxItems", "format", "default", "title",
}


class Provider(Protocol):
    name: str

    def complete_json(self, system: str, prompt: str, schema: dict, images: list[Path]) -> dict: ...


def model_schema(cls: type[BaseModel]) -> dict:
    """JSON schema for structured output: closed objects, every property required."""

    def walk(node):
        if isinstance(node, dict):
            for key in _UNSUPPORTED & node.keys():
                del node[key]
            if node.get("type") == "object" and "properties" in node:
                node["additionalProperties"] = False
                node["required"] = list(node["properties"])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    schema = copy.deepcopy(cls.model_json_schema())
    walk(schema)
    return schema


class GenerationError(RuntimeError):
    pass


def generate(
    provider: Provider,
    system: str,
    prompt: str,
    cls: type[M],
    images: list[Path] | None = None,
    attempts: int = 3,
) -> M:
    """Ask for an instance of `cls`; on validation failure, show the model its errors and retry."""
    schema = model_schema(cls)
    feedback = ""
    for _ in range(attempts):
        raw = provider.complete_json(system, prompt + feedback, schema, images or [])
        try:
            return cls.model_validate(raw)
        except ValidationError as e:
            feedback = (
                "\n\n---\nYour previous answer did not validate against the required schema:\n"
                f"{e}\nReturn a corrected, complete answer."
            )
    raise GenerationError(f"{provider.name} did not produce a valid {cls.__name__} in {attempts} attempts")


def make_provider(cfg: LLMConfig) -> Provider:
    match cfg.provider:
        case "claude-code":
            from paper_video.llm.claude_code import ClaudeCode

            return ClaudeCode(cfg)
        case "anthropic":
            from paper_video.llm.anthropic_api import AnthropicAPI

            return AnthropicAPI(cfg)
        case "openai":
            from paper_video.llm.openai_api import OpenAIAPI

            return OpenAIAPI(cfg)
