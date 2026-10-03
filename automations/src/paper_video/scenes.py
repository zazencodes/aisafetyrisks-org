"""Stage: scene files -> rendered, checked and visually reviewed clips; the thumbnail still.

Scene files in scenes/ are written by the session running the workflow (one subagent per scene,
from `paper-video brief <slug> scene --scene <id>`). Each file's first line records the hash of
the storyboard scene it implements; a file whose scene has changed is refused until updated.
Renders are cached by code, kit, narration and roadmap; agent-written visual reviews are keyed to each render.
"""

import hashlib
import json
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

from paper_video import log
from paper_video.config import KIT, Config, TTSConfig
from paper_video.context import short_citation
from paper_video.media import contact_sheet, frame_at
from paper_video.models import PaperRecord, Scene, SceneVisualReview, Storyboard
from paper_video.narrate import audio_key
from paper_video.provenance import number_supported, numbers_in
from paper_video.sandbox import beat_calls, render, static_check, string_literals
from paper_video.workdir import WorkDir, load_json, load_model, save_json

HEADER = re.compile(r"^# storyboard: ([0-9a-f]{16})\n")


def class_name(scene_id: str) -> str:
    return scene_id.upper()


def _digest(payload) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]


def scene_hash(scene: Scene, sb: Storyboard) -> str:
    return _digest({"scene": scene.model_dump(mode="json"), "datasets": [d.model_dump(mode="json") for d in sb.datasets],
                    "visual_language": sb.visual_language})


def thumbnail_hash(sb: Storyboard) -> str:
    return _digest([sb.thumbnail.model_dump(), sb.visual_language])


def kit_hash() -> str:
    h = hashlib.sha256()
    for p in sorted((KIT / "aisr_kit").glob("*.py")):
        h.update(p.read_bytes())
    return h.hexdigest()[:16]


def narrated_durations(wd: WorkDir, sb: Storyboard, cfg: TTSConfig) -> dict[str, float]:
    """Narration length of each clip. Fails if the audio does not match the storyboard's narration."""
    manifest_path = wd.audio / "manifest.json"
    manifest = load_json(manifest_path) if manifest_path.exists() else {}
    stale = [cid for cid, text in sb.clips() if manifest.get(cid, {}).get("key") != audio_key(text, cfg)]
    if stale:
        raise ValueError(f"narration is missing or out of date for {stale}; run `paper-video narrate {wd.slug}`")
    return {cid: manifest[cid]["duration"] for cid, _ in sb.clips()}


def render_context(wd: WorkDir, record: PaperRecord, sb: Storyboard, durations: dict[str, float], cfg: Config) -> dict:
    beats, checkpoints = {}, {}
    for scene in sb.scenes:
        for i, beat in enumerate(scene.beats):
            beats[beat.id] = {
                "scene": scene.id,
                "audio": str(wd.audio / f"{beat.id}.wav"),
                "duration": durations[beat.id],
                "last": i == len(scene.beats) - 1,
            }
        if scene.checkpoint:
            done, active = sb.checkpoint_state(scene)
            checkpoints[scene.id] = {
                "id": scene.checkpoint_id,
                "audio": str(wd.audio / f"{scene.checkpoint_id}.wav"),
                "duration": durations[scene.checkpoint_id],
                "done": done,
                "active": active,
            }
    return {
        "paper": {"title": record.title, "short": short_citation(record), "year": record.published.year},
        "beat_pause": cfg.render.beat_pause,
        "roadmap": sb.roadmap,
        "beats": beats,
        "checkpoints": checkpoints,
        "datasets": {d.id: d.model_dump(mode="json") for d in sb.datasets},
    }


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


def _read_versioned(path: Path, digest: str) -> tuple[str | None, list[str]]:
    """The file's code without its header line, or the problems that stop it being used."""
    if not path.exists():
        return None, [f"{path} does not exist"]
    text = path.read_text()
    m = HEADER.match(text)
    if m is None:
        return None, [f"the first line must be `# storyboard: {digest}`"]
    if m.group(1) != digest:
        return None, [f"the file was written for an earlier version of the storyboard ({m.group(1)}); update the code "
                      f"for the current storyboard and set the first line to `# storyboard: {digest}`"]
    return HEADER.sub("", text), []


def layout_problems(report: dict) -> list[str]:
    problems = []
    for b in report["beats"]:
        problems += [f"{b['beat']}: {i}" for i in b["issues"]]
        if b["overrun"] > 1.0:
            problems.append(f"{b['beat']}: animations run {b['overrun']:.1f}s longer than the narration")
    return problems


class SceneRenderer:
    def __init__(self, wd: WorkDir, record: PaperRecord, sb: Storyboard, cfg: Config):
        self.wd, self.record, self.sb, self.cfg = wd, record, sb, cfg
        self.audio = load_json(wd.audio / "manifest.json")

    def _render_key(self, scene: Scene, code: str) -> str:
        payload = [code, kit_hash(), [self.audio[cid]["key"] for cid, _ in scene.clips()],
                   self.sb.roadmap, self.sb.checkpoint_state(scene) if scene.checkpoint else None,
                   self.cfg.render.model_dump(mode="json")]
        return hashlib.sha256(json.dumps(payload).encode()).hexdigest()[:16]

    def is_current(self, scene: Scene) -> bool:
        """Whether the cached render of `scene` matches its current code, kit and narration."""
        code, _ = _read_versioned(self.wd.scene_file(scene.id), scene_hash(scene, self.sb))
        stamp = self.wd.render / f"{scene.id}.key"
        return (code is not None and stamp.exists() and (self.wd.render / f"{scene.id}.mp4").exists()
                and stamp.read_text() == self._render_key(scene, self.wd.scene_file(scene.id).read_text()))

    def _render(self, scene: Scene, key: str) -> tuple[bool, str, Path | None, dict | None]:
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

    def _frames(self, scene: Scene, video: Path, report: dict) -> Path:
        # A beat's first frame and early transition matter as much as its end: shorts cut whole beats.
        shots = []
        for b in report["beats"]:
            for label, t in (("first frame", b["start"] + 0.01), ("+0.4 s", b["start"] + 0.4),
                             ("end", b["hold_end"] - 0.15)):
                name = f"{b['beat']}-{label.replace(' ', '').replace('+', 'plus').replace('.', '')}.png"
                shots.append((f"{b['beat']} {label}", frame_at(video, t, self.wd.frames / scene.id / name)))
        return contact_sheet(shots, self.wd.frames / f"{scene.id}-sheet.png", cols=3, width=640)

    def _visual_review(self, scene: Scene, key: str) -> dict | None:
        path = self.wd.visual_review(scene.id)
        if not path.exists():
            return None
        review = load_model(path, SceneVisualReview)
        if review.render_key != key:
            return None
        return {"issues": [issue.model_dump(mode="json") for issue in review.issues]}

    def build(self, scene: Scene) -> dict:
        check_path = self.wd.checks / "scenes" / f"{scene.id}.json"
        result = {"scene": scene.id, "rendered": False, "render_key": None, "problems": [], "render_log_tail": None,
                  "layout_problems": [], "visual_review": None}
        code, problems = _read_versioned(self.wd.scene_file(scene.id), scene_hash(scene, self.sb))
        if code is not None:
            problems = code_problems(code, scene, self.sb, self.record)
        if problems:
            result["problems"] = problems
        else:
            key = self._render_key(scene, self.wd.scene_file(scene.id).read_text())
            ok, render_log, video, report = self._render(scene, key)
            result["render_key"] = key
            if not ok:
                result["render_log_tail"] = render_log[-4000:]
            else:
                result["rendered"] = True
                result["layout_problems"] = layout_problems(report)
                self._frames(scene, video, report)
                result["visual_review"] = self._visual_review(scene, key)
        save_json(check_path, result)
        return result


def _log_result(r: dict) -> None:
    if r["problems"]:
        log(f"{r['scene']}: REJECTED\n  - " + "\n  - ".join(r["problems"]))
    elif not r["rendered"]:
        log(f"{r['scene']}: RENDER FAILED\n{r['render_log_tail']}")
    elif r["visual_review"] is None:
        log(f"{r['scene']}: rendered; {len(r['layout_problems'])} layout problems; visual review pending "
            f"({r['render_key']})")
        for p in r["layout_problems"]:
            log(f"  [layout] {p}")
    else:
        issues = r["visual_review"]["issues"]
        serious = [i for i in issues if i["severity"] in ("blocker", "major")]
        log(f"{r['scene']}: rendered; {len(r['layout_problems'])} layout problems, "
            f"{len(serious)} blocker/major and {len(issues) - len(serious)} minor visual issues")
        for p in r["layout_problems"]:
            log(f"  [layout] {p}")
        for i in issues:
            log(f"  [{i['severity']}] {i['beat']}: {i['problem']}\n    fix: {i['suggested_fix']}")


def render_scenes(wd: WorkDir, record: PaperRecord, sb: Storyboard, cfg: Config, only: list[str] | None) -> list[dict]:
    durations = narrated_durations(wd, sb, cfg.tts)
    if load_json(wd.render / "context.json") != render_context(wd, record, sb, durations, cfg):
        raise ValueError(f"render/context.json is out of date; run `paper-video narrate {wd.slug}`")
    unknown = set(only or []) - {s.id for s in sb.scenes}
    if unknown:
        raise ValueError(f"no such scenes: {sorted(unknown)}")
    renderer = SceneRenderer(wd, record, sb, cfg)
    targets = [s for s in sb.scenes if not only or s.id in only]
    with ThreadPoolExecutor(max_workers=cfg.render.parallel_scenes) as pool:
        results = list(pool.map(renderer.build, targets))
    for r in results:
        _log_result(r)
    failed = [r["scene"] for r in results if not r["rendered"]]
    if failed:
        raise RuntimeError(f"scenes not rendered: {failed}; see checks/scenes/")
    pending = [r["scene"] for r in results if r["visual_review"] is None]
    if pending:
        raise RuntimeError(f"visual reviews pending for {pending}; write visual-reviews/<scene>.yaml with the current render key, then re-run render")
    return results


def build_thumbnail(wd: WorkDir, sb: Storyboard, cfg: Config) -> Path:
    code, problems = _read_versioned(wd.thumbnail_scene, thumbnail_hash(sb))
    if code is not None:
        problems = static_check(code, "Thumbnail", "Scene")
        problems += [f"text {s!r} contains digits" for s in string_literals(code) if numbers_in(s) and not s.startswith("#")]
    if problems:
        raise ValueError("thumbnail scene rejected:\n- " + "\n- ".join(problems))
    result = render(wd, cfg.render, wd.thumbnail_scene, "Thumbnail", still=True, resolution=(1280, 720))
    if not result.ok:
        raise RuntimeError(f"thumbnail failed to render:\n{result.log[-3000:]}")
    wd.out.mkdir(parents=True, exist_ok=True)
    dest = wd.out / "thumbnail.jpg"
    Image.open(result.output).convert("RGB").save(dest, quality=88, optimize=True, progressive=True)
    log(f"thumbnail written: {dest}")
    return dest
