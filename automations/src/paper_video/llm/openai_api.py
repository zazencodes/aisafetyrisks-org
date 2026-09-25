"""Provider backed by the OpenAI Responses API (strict JSON schema output)."""

import base64
import json
from pathlib import Path

import openai

from paper_video.config import LLMConfig
from paper_video.llm import GenerationError


class OpenAIAPI:
    def __init__(self, cfg: LLMConfig):
        self.client = openai.OpenAI(timeout=cfg.timeout_seconds)
        self.cfg = cfg
        self.name = f"openai/{cfg.model}"

    def complete_json(self, system: str, prompt: str, schema: dict, images: list[Path]) -> dict:
        content = [{"type": "input_text", "text": prompt}]
        content += [
            {"type": "input_image", "image_url": f"data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}"}
            for p in images
        ]
        response = self.client.responses.create(
            model=self.cfg.model,
            instructions=system,
            input=[{"role": "user", "content": content}],
            reasoning={"effort": self.cfg.effort},
            text={"format": {"type": "json_schema", "name": "output", "schema": schema, "strict": True}},
        )
        if response.status != "completed":
            raise GenerationError(f"response {response.status}: {response.incomplete_details}")
        return json.loads(response.output_text)
