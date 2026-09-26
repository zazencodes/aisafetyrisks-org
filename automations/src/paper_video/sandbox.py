"""Statically check scene code and render it with the workspace's Manim installation."""

import ast
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from paper_video.config import KIT, RenderConfig
from paper_video.workdir import WorkDir

BANNED_NAMES = {
    "open", "exec", "eval", "compile", "__import__", "globals", "locals", "vars", "getattr",
    "setattr", "delattr", "input", "breakpoint", "help", "memoryview", "exit", "quit",
}


def static_check(code: str, class_name: str, base: str) -> list[str]:
    """Structural and safety rules for generated scene files. Returns problems (empty = ok)."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [f"syntax error: {e}"]
    problems = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            problems.append(f"line {node.lineno}: `import` is not allowed")
        elif isinstance(node, ast.ImportFrom) and not (
            node.module == "aisr_kit" and [a.name for a in node.names] == ["*"]
        ):
            problems.append(f"line {node.lineno}: only `from aisr_kit import *` may be imported")
        elif isinstance(node, ast.Name) and (node.id in BANNED_NAMES or node.id.startswith("__")):
            problems.append(f"line {node.lineno}: `{node.id}` is not allowed")
        elif isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            problems.append(f"line {node.lineno}: dunder attribute `{node.attr}` is not allowed")
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    if [c.name for c in classes] != [class_name]:
        problems.append(f"the file must define exactly one class, {class_name}")
    elif [getattr(b, "id", None) for b in classes[0].bases] != [base]:
        problems.append(f"{class_name} must subclass {base}")
    return problems


def beat_calls(code: str) -> list[str]:
    """Beat ids passed to self.beat(...), in source order."""
    ids = []
    for node in ast.walk(ast.parse(code)):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "beat"
            and node.args
            and isinstance(node.args[0], ast.Constant)
        ):
            ids.append((node.lineno, node.args[0].value))
    return [i for _, i in sorted(ids)]


def string_literals(code: str) -> list[str]:
    return [n.value for n in ast.walk(ast.parse(code)) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


@dataclass
class RenderResult:
    ok: bool
    log: str
    output: Path | None


def render(wd: WorkDir, cfg: RenderConfig, scene_file: Path, class_name: str, still: bool = False,
           resolution: tuple[int, int] | None = None) -> RenderResult:
    width, height = resolution or cfg.resolution
    wd.render.mkdir(parents=True, exist_ok=True)
    wd.audio.mkdir(parents=True, exist_ok=True)
    rel = scene_file.relative_to(wd.scenes)
    media = wd.render / "media" / rel.stem
    cmd = [
        sys.executable, "-m", "manim", "render",
        "-r", f"{width},{height}",
        "--progress_bar", "none",
        "--media_dir", str(media),
    ]
    if still:
        cmd += ["-s", "--format", "png"]
    else:
        cmd += ["--frame_rate", str(cfg.frame_rate)]
    cmd += [str(wd.scenes / rel), class_name]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(KIT)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["AISR_CONTEXT"] = str(wd.render / "context.json")
    env["AISR_REPORTS"] = str(wd.render / "reports")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600, cwd=wd.root, env=env)
    except subprocess.TimeoutExpired:
        return RenderResult(False, "render timed out after 3600s", None)
    log = proc.stdout + proc.stderr
    if still:
        found = sorted((media / "images" / rel.stem).glob(f"{class_name}*.png"), key=lambda p: p.stat().st_mtime)
    else:
        found = sorted((media / "videos" / rel.stem).glob(f"*/{class_name}.mp4"), key=lambda p: p.stat().st_mtime)
    ok = proc.returncode == 0 and bool(found)
    return RenderResult(ok, log, found[-1] if ok else None)
