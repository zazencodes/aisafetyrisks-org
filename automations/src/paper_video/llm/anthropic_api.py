"""Provider backed by the Anthropic Messages API (structured outputs)."""

import base64
import json
from pathlib import Path

import anthropic

from paper_video.config import LLMConfig
from paper_video.llm import GenerationError


class AnthropicAPI:
    def __init__(self, cfg: LLMConfig):
        # Credentials resolve the SDK's usual way: ANTHROPIC_API_KEY or an `ant auth login` profile.
        self.client = anthropic.Anthropic(timeout=cfg.timeout_seconds)
        self.cfg = cfg
        self.name = f"anthropic/{cfg.model}"

    def complete_json(self, system: str, prompt: str, schema: dict, images: list[Path]) -> dict:
        content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": base64.standard_b64encode(p.read_bytes()).decode(),
                },
            }
            for p in images
        ]
        content.append({"type": "text", "text": prompt})
        # Papers about misuse and dangerous capabilities can trip safety classifiers;
        # server-side fallbacks let a declined request be retried on a fallback model.
        with self.client.beta.messages.stream(
            model=self.cfg.model,
            max_tokens=64000,
            system=system,
            messages=[{"role": "user", "content": content}],
            thinking={"type": "adaptive"},
            output_config={"effort": self.cfg.effort, "format": {"type": "json_schema", "schema": schema}},
            betas=["server-side-fallback-2026-07-01"],
            extra_body={"fallbacks": "default"},
        ) as stream:
            message = stream.get_final_message()
        if message.stop_reason == "refusal":
            raise GenerationError(f"request refused: {message.stop_details}")
        if message.stop_reason == "max_tokens":
            raise GenerationError("response truncated at max_tokens")
        text = next(b.text for b in message.content if b.type == "text")
        return json.loads(text)
