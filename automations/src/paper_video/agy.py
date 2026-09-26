"""Easy, context-heavy tasks delegated to a cheaper model through the Antigravity CLI (`agy -p`).

Used for metadata for PDFs that carry none. Writing and visual review happen in
the agent session that runs workflows/publish-paper/WORKFLOW.md.
"""

import copy
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from paper_video import log
from paper_video.config import AgyConfig

M = TypeVar("M", bound=BaseModel)

# Validation keywords that structured-output grammars commonly reject. They are
# stripped from the schema sent to the model and enforced by pydantic afterwards.
_UNSUPPORTED = {
    "minLength", "maxLength", "pattern", "minimum", "maximum", "exclusiveMinimum",
    "exclusiveMaximum", "minItems", "maxItems", "format", "default", "title",
}


class AgyError(RuntimeError):
    pass


def model_schema(cls: type[BaseModel]) -> dict:
    """JSON schema for structured output: closed objects, every property required."""

    def walk(node):
        if isinstance(node, dict):
            for key in _UNSUPPORTED & node.keys():
                del node[key]
            if node.get("type") == "object" and "properties" in node:
                node["additionalProperties"] = False
                node["required"] = list(node["properties"])
            for key, value in node.items():
                if key in ("properties", "$defs"):
                    # Keys here are field and model names, not keywords: a field may be called "title".
                    for sub in value.values():
                        walk(sub)
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    schema = copy.deepcopy(cls.model_json_schema())
    walk(schema)
    return schema


def _complete_json(cfg: AgyConfig, prompt: str, schema: dict, images: list[Path]) -> dict:
    binary = shutil.which("agy")
    if binary is None:
        raise AgyError("`agy` CLI not found on PATH")
    cmd = [
        binary,
        "--model", cfg.model,
        "--output-format", "json",
        "--json-schema", json.dumps(schema),
        "--print-timeout", f"{cfg.timeout_seconds}s",
    ]
    for d in sorted({str(p.resolve().parent) for p in images}):
        cmd += ["--add-dir", d]
    if images:
        listing = "\n".join(f"- {p.resolve()}" for p in images)
        prompt = f"Read each of these image files before answering:\n{listing}\n\n{prompt}"
    cmd.append(f"-p={prompt}")

    # Run from an empty directory so the agent sees no project files.
    with tempfile.TemporaryDirectory() as cwd:
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=cfg.timeout_seconds + 60)
    if proc.returncode != 0:
        raise AgyError(f"agy exited {proc.returncode}: {proc.stderr[-2000:] or proc.stdout[-2000:]}")
    result = json.loads(proc.stdout)
    if result.get("status") != "SUCCESS":
        raise AgyError(f"agy returned status {result.get('status')!r}: {result.get('response')!r}")
    output = result.get("structured_output")
    if output is None:
        raise AgyError(f"agy returned no structured output: {result.get('response')!r}")
    return output


def generate(cfg: AgyConfig, instructions: str, task: str, cls: type[M], images: list[Path] | None = None,
             attempts: int = 3) -> M:
    """Ask for an instance of `cls`; on validation failure, show the model its errors and retry."""
    schema = model_schema(cls)
    prompt = f"# Instructions\n\n{instructions}\n\n# Task\n\n{task}"
    feedback = ""
    for attempt in range(1, attempts + 1):
        log(f"  agy/{cfg.model} -> {cls.__name__} (attempt {attempt}/{attempts}, {len(images or [])} images)")
        start = time.monotonic()
        raw = _complete_json(cfg, prompt + feedback, schema, images or [])
        try:
            result = cls.model_validate(raw)
        except ValidationError as e:
            log(f"  {cls.__name__} failed validation after {time.monotonic() - start:.0f}s: {e.error_count()} errors")
            feedback = (
                "\n\n---\nYour previous answer did not validate against the required schema:\n"
                f"{e}\nReturn a corrected, complete answer."
            )
            continue
        log(f"  {cls.__name__} ok in {time.monotonic() - start:.0f}s")
        return result
    raise AgyError(f"agy/{cfg.model} did not produce a valid {cls.__name__} in {attempts} attempts")
