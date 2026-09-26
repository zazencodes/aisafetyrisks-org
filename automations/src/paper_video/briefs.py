"""Briefs for the writing tasks done in the agent session running the workflow, or by its subagents.

`paper-video brief <slug> <task>` writes briefs/<task>.md: the instructions, the exact inputs, where
to write the result, the schema it must follow and the command that checks it.
"""

import json
from pathlib import Path

from pydantic import BaseModel

from paper_video import backlog
from paper_video.config import KIT, Config
from paper_video.context import as_yaml, paper_header, paper_text, prompt, system
from paper_video.models import Notes, PaperRecord, ScienceReview, Scene, SceneVisualReview, Storyboard, WorkDraft
from paper_video.review import review_file, reviewed_content
from paper_video.scenes import class_name, narrated_durations, scene_hash, thumbnail_hash
from paper_video.site_content import paper_links
from paper_video.workdir import WorkDir, load_model

TASKS = ["analyze", "storyboard", "scene", "thumbnail", "site", "review-storyboard", "review-site"]
CLI = "uv run --frozen paper-video"


def _schema(cls: type[BaseModel]) -> str:
    return f"```json\n{json.dumps(cls.model_json_schema(), indent=1)}\n```"


def _yaml_output(path: Path, cls: type[BaseModel], command: str) -> str:
    return (
        f"# Output\n\nWrite `{path}` as YAML that validates against this JSON schema:\n\n{_schema(cls)}\n\n"
        f"Then run `{command}` from the repository root. It fails loudly and lists every problem; "
        "fix them and re-run it until it passes."
    )


def _scene_inputs(record: PaperRecord, notes: Notes, sb: Storyboard, scene: Scene, durations: dict[str, float]) -> str:
    cited = {c for b in scene.beats for c in b.claims}
    claims = [c for c in notes.claims if c.id in cited]
    outline = "\n".join(f"- {s.id} {s.title}: {s.purpose}" for s in sb.scenes)
    timing = "\n".join(f"- {b.id}: {durations[b.id]:.1f} s of narration" for b in scene.beats)
    return (
        f"{paper_header(record)}\n\n# Visual language of the whole video\n\n{sb.visual_language}\n\n"
        f"# Outline of the whole video\n\n{outline}\n\n# Datasets\n\n"
        + "\n".join(as_yaml(d) for d in sb.datasets)
        + "\n\n# Claims cited in this scene\n\n"
        + "\n".join(f"- {c.id} ({c.kind}): {c.statement}" for c in claims)
        + f"\n\n# The scene to animate (class name {class_name(scene.id)})\n\n{as_yaml(scene)}\n\n# Beat timing\n\n{timing}"
    )


def _analyze(wd: WorkDir, record: PaperRecord) -> str:
    return (
        f"{system('analyze')}\n\n{_yaml_output(wd.notes, Notes, f'{CLI} check {wd.slug} notes')}\n\n"
        f"# Paper\n\n{paper_header(record)}\n\nFull text:\n\n{paper_text(wd.pages())}"
    )


def _storyboard(wd: WorkDir, record: PaperRecord, notes: Notes) -> str:
    return (
        f"{system('storyboard')}\n\n{_yaml_output(wd.storyboard, Storyboard, f'{CLI} check {wd.slug} storyboard')}\n\n"
        f"# Paper\n\n{paper_header(record)}\n\n# Reading notes\n\n{as_yaml(notes)}"
    )


def _scene(wd: WorkDir, record: PaperRecord, notes: Notes, sb: Storyboard, cfg: Config, scene_id: str) -> str:
    scene = next((s for s in sb.scenes if s.id == scene_id), None)
    if scene is None:
        raise ValueError(f"no scene {scene_id!r} in the storyboard")
    durations = narrated_durations(wd, sb, cfg.tts)
    output = (
        f"# Output\n\nWrite `{wd.scene_file(scene.id)}`. Its first line must be exactly "
        f"`# storyboard: {scene_hash(scene, sb)}` (it ties the code to this version of the scene), "
        "followed by `from aisr_kit import *`.\n\n"
        f"Render with `{CLI} render {wd.slug} --scene {scene.id}` from the repository root. The result is also "
        f"saved to `{wd.checks / 'scenes' / f'{scene.id}.json'}` and the contact sheet to "
        f"`{wd.frames / f'{scene.id}-sheet.png'}`. Inspect that sheet and write "
        f"`{wd.visual_review(scene.id)}` as YAML with the printed `render_key` and the issues you find. "
        f"The schema is:\n\n{_schema(SceneVisualReview)}\n\n"
        f"Re-run `{CLI} render {wd.slug} --scene {scene.id}` to record the review. "
        "Update the review's key after any code change and render."
    )
    return (
        f"{prompt('scene_code')}\n\n{output}\n\n"
        f"{(KIT / 'REFERENCE.md').read_text()}\n\n{prompt('fix_scene')}\n\n"
        f"# Inputs\n\n{_scene_inputs(record, notes, sb, scene, durations)}"
    )


def _thumbnail(wd: WorkDir, record: PaperRecord, sb: Storyboard) -> str:
    return (
        f"{prompt('thumbnail')}\n\n"
        f"# Output\n\nWrite `{wd.thumbnail_scene}`. Its first line must be exactly "
        f"`# storyboard: {thumbnail_hash(sb)}`, followed by `from aisr_kit import *`.\n\n"
        f"Render with `{CLI} thumbnail {wd.slug}` from the repository root; it writes `{wd.out / 'thumbnail.jpg'}`. "
        "Fix any problem it reports and re-run it until it passes, then look at the image.\n\n"
        f"{(KIT / 'REFERENCE.md').read_text()}\n\n"
        f"# Inputs\n\n{paper_header(record)}\n\n# Visual language\n\n{sb.visual_language}\n\n"
        f"# Thumbnail\n\nHeadline: {sb.thumbnail.headline}\nVisual: {sb.thumbnail.visual}"
    )


def _site(wd: WorkDir, record: PaperRecord, notes: Notes, sb: Storyboard) -> str:
    narration = "\n".join(f"[{s.id} {s.title}] " + " ".join(b.narration for b in s.beats) for s in sb.scenes)
    links = paper_links(wd.pages())
    entry = backlog.find(backlog.load(), record.arxiv_id, str(record.url))
    return (
        f"{system('site')}\n\n{_yaml_output(wd.site_draft, WorkDraft, f'{CLI} site {wd.slug}')}\n\n"
        f"# Paper\n\n{paper_header(record)}\n\n# Reading notes\n\n{as_yaml(notes)}\n\n"
        f"# Narration of the video this page accompanies\n\n{narration}\n\n"
        "# URLs printed in the paper\n\n" + ("\n".join(f"- {u}" for u in links) or "(none)")
        + (f"\n\n# Category\n\nUse the category `{entry.category.value}`." if entry else "")
    )


def _review(wd: WorkDir, record: PaperRecord, notes: Notes, subject: str) -> str:
    name = {"storyboard": "storyboard", "site": "web page"}[subject]
    return (
        f"{system('science_review')}\n\nYou did not write this {name}. Do not edit it; write only your review.\n\n"
        f"{_yaml_output(review_file(wd, subject), ScienceReview, f'{CLI} review {wd.slug} {subject}')} "
        "That command records your review; report its output.\n\n"
        f"# Paper\n\n{paper_header(record)}\n\n# Full paper text\n\n{paper_text(wd.pages())}\n\n"
        f"# Reading notes the explainer was built from\n\n{as_yaml(notes)}\n\n"
        f"# The {name} to review\n\n{reviewed_content(wd, subject)}\n\n"
    )


def write_brief(wd: WorkDir, record: PaperRecord, cfg: Config, task: str, scene_id: str | None) -> Path:
    if (task == "scene") != (scene_id is not None):
        raise ValueError("--scene is required for the scene task and only allowed there")
    notes = load_model(wd.notes, Notes) if task != "analyze" else None
    sb = load_model(wd.storyboard, Storyboard) if task not in ("analyze", "storyboard", "review-site") else None
    match task:
        case "analyze":
            text = _analyze(wd, record)
        case "storyboard":
            text = _storyboard(wd, record, notes)
        case "scene":
            text = _scene(wd, record, notes, sb, cfg, scene_id)
        case "thumbnail":
            text = _thumbnail(wd, record, sb)
        case "site":
            text = _site(wd, record, notes, sb)
        case "review-storyboard":
            text = _review(wd, record, notes, "storyboard")
        case "review-site":
            text = _review(wd, record, notes, "site")
        case _:
            raise ValueError(f"unknown task {task!r}; one of {TASKS}")
    path = wd.briefs / (f"scene-{scene_id}.md" if scene_id else f"{task}.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path
