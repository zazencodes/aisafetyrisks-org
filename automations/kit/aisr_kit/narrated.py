"""NarratedScene: sync animation to pre-rendered narration, and check layout as it plays.

Each storyboard beat has a narration clip. Inside `with self.beat("s02b01") as b:`
the clip starts playing, `b.duration` is its length in seconds, and when the block
ends the scene waits out whatever narration (plus a short pause) is left. After the
scene's last beat everything fades out, so scenes join cleanly. At the end of every
beat the scene records layout problems: text cut off by the frame edge, and text
overlapping other text.

Scenes that open a roadmap item, and the closing scene, start with a checkpoint: before
the first beat, the kit shows the roadmap checklist over the scene's checkpoint narration,
ticks off the item just finished and highlights the next. Scene code never draws it.
"""

import json
import os
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from manim import FadeIn, FadeOut, LaggedStart, MathTex, Scene, SingleStringMathTex, Text, Transform, config

from aisr_kit.roadmap import checklist

CONTEXT = Path(os.environ["AISR_CONTEXT"])
REPORTS = Path(os.environ["AISR_REPORTS"])
TEXT_TYPES = (Text, MathTex, SingleStringMathTex)


@dataclass
class BeatClock:
    id: str
    duration: float


class NarratedScene(Scene):
    def setup(self):
        ctx = json.loads(CONTEXT.read_text())
        self._beats = ctx["beats"]
        self._checkpoints = ctx["checkpoints"]
        self._roadmap = ctx["roadmap"]
        self._datasets = ctx["datasets"]
        self._pause = ctx["beat_pause"]
        self.paper = ctx["paper"]
        self._log = []

    def dataset(self, dataset_id: str) -> dict:
        """A storyboard dataset: {"title", "unit", "note", "points": [{"label", "value", "display"}]}."""
        return self._datasets[dataset_id]

    @contextmanager
    def beat(self, beat_id: str):
        info = self._beats[beat_id]
        if not self._log and info["scene"] in self._checkpoints:
            self._checkpoint(self._checkpoints[info["scene"]])
        with self._clip(beat_id, info, fade_out=info["last"]) as clock:
            yield clock

    @contextmanager
    def _clip(self, clip_id: str, info: dict, fade_out: bool):
        start = self.renderer.time
        self.add_sound(info["audio"])
        yield BeatClock(clip_id, info["duration"])
        elapsed = self.renderer.time - start
        remaining = info["duration"] + self._pause - elapsed
        if remaining > 0:
            self.wait(remaining)
        hold_end = self.renderer.time
        issues = self._layout_issues()
        if fade_out and self.mobjects:
            self.play(FadeOut(*self.mobjects), run_time=0.5)
        self._log.append({
            "beat": clip_id,
            "start": start,
            "hold_end": hold_end,
            "end": self.renderer.time,
            "narration": info["duration"],
            "overrun": max(0.0, -remaining),
            "issues": issues,
        })

    def _checkpoint(self, cp: dict):
        """Show the roadmap: reveal it at the first checkpoint, later tick off the item just finished."""
        done, active = cp["done"], cp["active"]
        with self._clip(cp["id"], cp, fade_out=True) as b:
            if done == 0:
                card = checklist(self._roadmap, 0, None)
                self.play(FadeIn(card.frame), FadeIn(card.heading), run_time=0.6)
                self.play(LaggedStart(*[FadeIn(row) for row in card.rows], lag_ratio=0.6),
                          run_time=max(1.0, b.duration * 0.6))
            else:
                card = checklist(self._roadmap, done - 1, done - 1)
                self.play(FadeIn(card), run_time=0.6)
                self.wait(0.3)
            self.play(Transform(card, checklist(self._roadmap, done, active)), run_time=0.9)

    def _visible_texts(self):
        found = []

        def walk(mob):
            if isinstance(mob, TEXT_TYPES):
                if mob.get_fill_opacity() > 0.05 and mob.width > 0:
                    found.append(mob)
                return
            for sub in mob.submobjects:
                walk(sub)

        for mob in self.mobjects:
            walk(mob)
        return found

    def _layout_issues(self) -> list[str]:
        half_w, half_h = config.frame_width / 2, config.frame_height / 2
        texts = self._visible_texts()
        issues = []
        boxes = []
        for t in texts:
            (x0, y0, _), (x1, y1, _) = t.get_corner([-1, -1, 0]), t.get_corner([1, 1, 0])
            label = getattr(t, "text", None) or getattr(t, "tex_string", "?")
            boxes.append((x0, y0, x1, y1, label))
            if x0 < -half_w + 0.1 or x1 > half_w - 0.1 or y0 < -half_h + 0.1 or y1 > half_h - 0.1:
                issues.append(f"text outside frame: {label!r}")
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                ix = min(a[2], b[2]) - max(a[0], b[0])
                iy = min(a[3], b[3]) - max(a[1], b[1])
                if ix > 0 and iy > 0:
                    smaller = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
                    if smaller > 0 and ix * iy / smaller > 0.15:
                        issues.append(f"text overlaps text: {a[4]!r} / {b[4]!r}")
        return issues

    def tear_down(self):
        REPORTS.mkdir(parents=True, exist_ok=True)
        (REPORTS / f"{type(self).__name__}.json").write_text(
            json.dumps({"scene": type(self).__name__, "duration": self.renderer.time, "beats": self._log}, indent=2)
        )
