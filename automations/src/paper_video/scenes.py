"""Stage: storyboard scenes -> Manim code -> rendered, checked and visually reviewed clips.

Scene files in scenes/ are editable. A file records the hash of the storyboard scene
it was generated from; it is only regenerated when that scene changes, so manual
fixes to code survive re-runs. Renders are cached by code, kit and narration.
"""

import hashlib
import json
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from paper_video.config import KIT, Config
from paper_video.context import as_yaml, paper_header, prompt, short_citation, system
from paper_video.llm import Provider, generate
from paper_video.media import contact_sheet, frame_at
from paper_video.models import Notes, PaperRecord, Scene, SceneCode, Storyboard, VisualReview
from paper_video.provenance import number_supported, numbers_in
from paper_video.sandbox import beat_calls, render, static_check, string_literals
from paper_video.workdir import WorkDir, load_json, save_json

HEADER = re.compile(r"^# storyboard: ([0-9a-f]{16})\n")


def class_name(scene_id: str) -> str:
    return scene_id.upper()


def scene_hash(scene: Scene, sb: Storyboard) -> str:
    payload = {"scene": scene.model_dump(mode="json"), "datasets": [d.model_dump(mode="json") for d in sb.datasets],
               "visual_language": sb.visual_language}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]


def kit_hash() -> str:
    h = hashlib.sha256()
    for p in sorted((KIT / "aisr_kit").glob("*.py")):
        h.update(p.read_bytes())
    return h.hexdigest()[:16]


def write_context(wd: WorkDir, record: PaperRecord, sb: Storyboard, durations: dict[str, float], cfg: Config) -> None:
    beats = {}
    for scene in sb.scenes:
        for i, beat in enumerate(scene.beats):
            beats[beat.id] = {
                "audio": f"/work/audio/{beat.id}.wav",
                "duration": durations[beat.id],
                "last": i == len(scene.beats) - 1,
            }
    save_json(wd.render / "context.json", {
        "paper": {"title": record.title, "short": short_citation(record), "year": record.published.year},
        "beat_pause": cfg.render.beat_pause,
        "beats": beats,
        "datasets": {d.id: d.model_dump(mode="json") for d in sb.datasets},
    })


def code_problems(code: str, scene: Scene, sb: Storyboard, record: PaperRecord) -> list[str]:
    problems = static_check(code, class_name(scene.id), "NarratedScene")
    if problems:
        return problems
    expected = [b.id for b in scene.beats]
    if beat_calls(code) != expected:
        problems.append(f"self.beat(...) calls must be exactly {expected} in this order; found {beat_calls(code)}")
    allowed = [t for b in scene.beats for t in b.on_screen_text] + [p.display for d in sb.datasets for p in d.points]
    allowed.append(f"{record.title} {short_citation(record)}")
    for literal in string_literals(code):
        if literal.startswith("#") or re.fullmatch(r"[a-z]\d+(b\d+)?", literal):
            continue
        for n in numbers_in(literal):
            if not number_supported(n, allowed):
                problems.append(f"text {literal!r} contains {n}, which is not in the beat's on_screen_text or a dataset")
    return problems


def _scene_brief(record: PaperRecord, notes: Notes, sb: Storyboard, scene: Scene, durations: dict[str, float]) -> str:
    cited = {c for b in scene.beats for c in b.claims}
    claims = [c for c in notes.claims if c.id in cited]
    outline = "\n".join(f"- {s.id} {s.title}: {s.purpose}" for s in sb.scenes)
    timing = "\n".join(f"- {b.id}: {durations[b.id]:.1f} s of narration" for b in scene.beats)
    return (
        f"{paper_header(record)}\n\n# Visual language of the whole video\n\n{sb.visual_language}\n\n"
        f"# Outline of the whole video\n\n{outline}\n\n# Datasets\n\n"
        + "\n".join(as_yaml(d) for d in sb.datasets)
        + f"\n\n# Claims cited in this scene\n\n"
        + "\n".join(f"- {c.id} ({c.kind}): {c.statement}" for c in claims)
        + f"\n\n# The scene to animate (class name {class_name(scene.id)})\n\n{as_yaml(scene)}\n\n# Beat timing\n\n{timing}"
    )


def _code_system(task: str | None = None) -> str:
    base = prompt("scene_code") + "\n\n" + (KIT / "REFERENCE.md").read_text()
    return f"{prompt(task)}\n\n{base}" if task else base


def _generate_code(provider: Provider, system_prompt: str, brief: str, scene: Scene, sb: Storyboard,
                   record: PaperRecord, attempts: int = 3) -> str:
    feedback = ""
    for _ in range(attempts):
        code = generate(provider, system_prompt, brief + feedback, SceneCode).code
        problems = code_problems(code, scene, sb, record)
        if not problems:
            return code
        feedback = "\n\n# Your previous file was rejected\n\n" + "\n".join(f"- {p}" for p in problems) + f"\n\n```python\n{code}\n```"
    raise RuntimeError(f"{scene.id}: could not generate a valid scene file:\n- " + "\n- ".join(problems))


@dataclass
class SceneOutcome:
    scene_id: str
    video: Path | None
    report: dict | None
    attempts: list[dict] = field(default_factory=list)
    visual_reviews: list[dict] = field(default_factory=list)


class SceneBuilder:
    def __init__(self, wd: WorkDir, record: PaperRecord, notes: Notes, sb: Storyboard, durations: dict[str, float],
                 provider: Provider, cfg: Config):
        self.wd, self.record, self.notes, self.sb = wd, record, notes, sb
        self.durations, self.provider, self.cfg = durations, provider, cfg

    def code_for(self, scene: Scene) -> str:
        path = self.wd.scene_file(scene.id)
        digest = scene_hash(scene, self.sb)
        if path.exists():
            m = HEADER.match(path.read_text())
            if m and m.group(1) == digest:
                return path.read_text()
        brief = _scene_brief(self.record, self.notes, self.sb, scene, self.durations)
        code = _generate_code(self.provider, _code_system(), brief, scene, self.sb, self.record)
        self._save(scene, code)
        return path.read_text()

    def _save(self, scene: Scene, code: str) -> None:
        body = HEADER.sub("", code)
        self.wd.scene_file(scene.id).parent.mkdir(parents=True, exist_ok=True)
        self.wd.scene_file(scene.id).write_text(f"# storyboard: {scene_hash(scene, self.sb)}\n{body}")

    def _render_key(self, scene: Scene, code: str) -> str:
        audio = load_json(self.wd.audio / "manifest.json")
        payload = [code, kit_hash(), [audio[b.id]["key"] for b in scene.beats], self.cfg.render.model_dump(mode="json")]
        return hashlib.sha256(json.dumps(payload).encode()).hexdigest()[:16]

    def _render(self, scene: Scene, code: str) -> tuple[bool, str, Path | None, dict | None]:
        key = self._render_key(scene, code)
        stamp = self.wd.render / f"{scene.id}.key"
        cached = self.wd.render / f"{scene.id}.mp4"
        report_path = self.wd.render / "reports" / f"{class_name(scene.id)}.json"
        if stamp.exists() and stamp.read_text() == key and cached.exists() and report_path.exists():
            return True, "cached", cached, load_json(report_path)
        report_path.unlink(missing_ok=True)
        result = render(self.wd, self.cfg.render, self.wd.scene_file(scene.id), class_name(scene.id))
        if not result.ok:
            return False, result.log, None, None
        shutil.copy(result.output, cached)
        stamp.write_text(key)
        return True, result.log, cached, load_json(report_path)

    def _fix(self, scene: Scene, code: str, problems: str) -> str:
        brief = _scene_brief(self.record, self.notes, self.sb, scene, self.durations)
        brief += f"\n\n# Current code\n\n```python\n{HEADER.sub('', code)}\n```\n\n# Problems to fix\n\n{problems}"
        return _generate_code(self.provider, _code_system("fix_scene"), brief, scene, self.sb, self.record)

    def _render_with_repair(self, scene: Scene, code: str, outcome: SceneOutcome):
        for attempt in range(self.cfg.render.max_fix_attempts + 1):
            ok, log, video, report = self._render(scene, code)
            outcome.attempts.append({"ok": ok, "log_tail": log[-1500:]})
            if ok:
                return code, video, report
            if attempt == self.cfg.render.max_fix_attempts:
                break
            self._save(scene, self._fix(scene, code, f"The render failed:\n\n```\n{log[-4000:]}\n```"))
            code = self.wd.scene_file(scene.id).read_text()
        return code, None, None

    def _try_improvement(self, scene: Scene, code: str, problems: str, outcome: SceneOutcome):
        """Apply a fix for layout/visual problems; keep the previous version if the fix does not render."""
        self._save(scene, self._fix(scene, code, problems))
        new_code, video, report = self._render_with_repair(scene, self.wd.scene_file(scene.id).read_text(), outcome)
        if video is None:
            self._save(scene, code)
            return code, *self._render(scene, code)[2:]
        return new_code, video, report

    def layout_problems(self, report: dict) -> list[str]:
        problems = []
        for b in report["beats"]:
            problems += [f"{b['beat']}: {i}" for i in b["issues"]]
            if b["overrun"] > 1.0:
                problems.append(f"{b['beat']}: animations run {b['overrun']:.1f}s longer than the narration")
        return problems

    def frames(self, scene: Scene, video: Path, report: dict) -> Path:
        shots = []
        for b in report["beats"]:
            path = frame_at(video, b["hold_end"] - 0.15, self.wd.frames / scene.id / f"{b['beat']}.png")
            shots.append((b["beat"], path))
        return contact_sheet(shots, self.wd.frames / f"{scene.id}-sheet.png")

    def visual_review(self, scene: Scene, sheet: Path) -> VisualReview:
        brief = f"# Storyboard scene\n\n{as_yaml(scene)}\n\nThe attached contact sheet shows the end of each beat, labelled with its id."
        return generate(self.provider, system("visual_review", integrity=False), brief, VisualReview, images=[sheet])

    def build(self, scene: Scene) -> SceneOutcome:
        outcome = SceneOutcome(scene.id, None, None)
        code = self.code_for(scene)
        code, video, report = self._render_with_repair(scene, code, outcome)
        if video is None:
            return outcome

        layout = self.layout_problems(report)
        if layout:
            code, video, report = self._try_improvement(
                scene, code, "Layout defects detected at the end of beats:\n- " + "\n- ".join(layout), outcome
            )

        for _ in range(self.cfg.render.visual_review_rounds):
            review = self.visual_review(scene, self.frames(scene, video, report))
            outcome.visual_reviews.append(review.model_dump(mode="json"))
            serious = [i for i in review.issues if i.severity in ("blocker", "major")]
            if not serious:
                break
            problems = "Issues found by the visual reviewer:\n" + "\n".join(
                f"- {i.beat} [{i.severity}]: {i.problem} Fix: {i.suggested_fix}" for i in serious
            )
            code, video, report = self._try_improvement(scene, code, problems, outcome)

        self.frames(scene, video, report)
        outcome.video, outcome.report = video, report
        return outcome


def build_scenes(wd: WorkDir, record: PaperRecord, notes: Notes, sb: Storyboard, durations: dict[str, float],
                 provider: Provider, cfg: Config, only: list[str] | None = None) -> list[SceneOutcome]:
    write_context(wd, record, sb, durations, cfg)
    builder = SceneBuilder(wd, record, notes, sb, durations, provider, cfg)
    targets = [s for s in sb.scenes if not only or s.id in only]
    with ThreadPoolExecutor(max_workers=cfg.render.parallel_scenes) as pool:
        outcomes = list(pool.map(builder.build, targets))
    for o in outcomes:
        save_json(wd.checks / "scenes" / f"{o.scene_id}.json", {
            "rendered": o.video is not None,
            "layout_problems": builder.layout_problems(o.report) if o.report else None,
            "render_attempts": o.attempts,
            "visual_reviews": o.visual_reviews,
        })
    failed = [o.scene_id for o in outcomes if o.video is None]
    if failed:
        raise RuntimeError(f"scenes failed to render: {failed}; see checks/scenes/")
    return outcomes


def build_thumbnail(wd: WorkDir, record: PaperRecord, sb: Storyboard, provider: Provider, cfg: Config) -> Path:
    path = wd.thumbnail_scene
    digest = hashlib.sha256(json.dumps([sb.thumbnail.model_dump(), sb.visual_language]).encode()).hexdigest()[:16]
    brief = (
        f"{paper_header(record)}\n\n# Visual language\n\n{sb.visual_language}\n\n"
        f"# Thumbnail\n\nHeadline: {sb.thumbnail.headline}\nVisual: {sb.thumbnail.visual}"
    )
    sys_prompt = prompt("thumbnail") + "\n\n" + (KIT / "REFERENCE.md").read_text()
    code = path.read_text() if path.exists() and HEADER.match(path.read_text()) and HEADER.match(path.read_text()).group(1) == digest else None
    for attempt in range(cfg.render.max_fix_attempts + 1):
        if code is None:
            feedback = ""
            for _ in range(3):
                candidate = generate(provider, sys_prompt, brief + feedback, SceneCode).code
                problems = static_check(candidate, "Thumbnail", "Scene")
                problems += [f"text {s!r} contains digits" for s in string_literals(candidate)
                             if numbers_in(s) and not s.startswith("#")]
                if not problems:
                    break
                feedback = "\n\n# Rejected\n\n" + "\n".join(f"- {p}" for p in problems)
            else:
                raise RuntimeError(f"could not generate a valid thumbnail scene: {problems}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# storyboard: {digest}\n{HEADER.sub('', candidate)}")
            code = path.read_text()
        result = render(wd, cfg.render, path, "Thumbnail", still=True, resolution=(1280, 720))
        if result.ok:
            break
        brief += f"\n\n# The previous version failed to render\n\n```python\n{code}\n```\n\n```\n{result.log[-3000:]}\n```"
        code = None
    else:
        raise RuntimeError("thumbnail failed to render")
    wd.out.mkdir(parents=True, exist_ok=True)
    dest = wd.out / "thumbnail.jpg"
    Image.open(result.output).convert("RGB").save(dest, quality=88, optimize=True, progressive=True)
    return dest
