"""Provider backed by the local Claude Code CLI in headless mode (`claude -p`).

Uses whatever account `claude` is logged into, so no API key is needed. Tools are
disabled except `Read`, which is enabled only for the image directory when images
are attached.
"""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from paper_video.config import LLMConfig
from paper_video.llm import GenerationError


class ClaudeCode:
    def __init__(self, cfg: LLMConfig):
        binary = shutil.which("claude")
        if binary is None:
            raise GenerationError("`claude` CLI not found on PATH")
        self.binary = binary
        self.cfg = cfg
        self.name = f"claude-code/{cfg.model}"

    def complete_json(self, system: str, prompt: str, schema: dict, images: list[Path]) -> dict:
        cmd = [
            self.binary, "-p",
            "--model", self.cfg.model,
            "--effort", self.cfg.effort,
            "--output-format", "json",
            "--json-schema", json.dumps(schema),
            "--system-prompt", system,
            "--no-session-persistence",
            "--strict-mcp-config",
        ]
        if images:
            dirs = sorted({str(p.resolve().parent) for p in images})
            cmd += ["--tools", "Read", "--allowedTools", "Read"]
            for d in dirs:
                cmd += ["--add-dir", d]
            listing = "\n".join(f"- {p.resolve()}" for p in images)
            prompt = f"Read each of these image files before answering:\n{listing}\n\n{prompt}"
        else:
            cmd += ["--tools", ""]

        # Run from an empty directory so no project instructions are picked up.
        with tempfile.TemporaryDirectory() as cwd:
            proc = subprocess.run(
                cmd, input=prompt, capture_output=True, text=True, cwd=cwd, timeout=self.cfg.timeout_seconds
            )
        if proc.returncode != 0:
            raise GenerationError(f"claude exited {proc.returncode}: {proc.stderr[-2000:] or proc.stdout[-2000:]}")
        result = json.loads(proc.stdout)
        if result.get("is_error") or result.get("subtype") != "success":
            raise GenerationError(f"claude returned an error: {result.get('result')!r}")
        output = result.get("structured_output")
        if output is None:
            raise GenerationError(f"claude returned no structured output: {result.get('result')!r}")
        return output
