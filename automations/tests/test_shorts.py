"""Short edits retain source evidence, complete speech, and current independent review."""

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
import wave
from unittest.mock import patch

from pydantic import ValidationError

from paper_video import pipeline
from paper_video.config import WORKS
from paper_video.models import Notes, PaperRecord, Storyboard, VisualIssue
from paper_video.media import probe, run
from paper_video.shorts import (ShortPlan, ShortReview, ass_text, caption_file, check_short,
                               build_short, content_key, current_short_review,
                               short_cues, validate_plan)
from paper_video.workdir import WorkDir, load_model, save_json, save_model


class ShortTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.wd = WorkDir(Path(self.temp.name))
        source = WorkDir(WORKS / "concrete-problems-in-ai-safety")
        self.record = load_model(source.paper, PaperRecord)
        self.sb = load_model(source.storyboard, Storyboard)
        self.notes = load_model(source.notes, Notes)
        save_json(self.wd.pages_json, [e.quote for c in self.notes.claims for e in c.evidence])
        ids = ["s03b01", "s02b01", "s04b01", "s08b03", "s08b04"]
        roles = ["hook", "context", "explanation", "limitation", "takeaway"]
        self.plan_data = dict(title="AI accidents", description="A research agenda.",
                              scope_label="Hypothetical examples", selection_reason="Complete example and caveat.",
                              segments=[dict(beat=b, role=r, heading="AI accidents")
                                        for b, r in zip(ids, roles)])
        self.plan = ShortPlan.model_validate(self.plan_data)
        beats = {b.id: b for b in self.sb.beats()}
        self.sources = {b: dict(beat=beats[b], duration=10, narration_duration=9.5, start=0,
                               source_start=10 * i, clip=self.wd.render / f"{b[:3]}.mp4")
                        for i, b in enumerate(ids)}

    def test_complete_shape_and_unique_beats_are_required(self):
        for change in (lambda d: d["segments"].__setitem__(0, d["segments"][1]),
                       lambda d: d["segments"][3].update(role="explanation"),
                       lambda d: d["segments"][-1].update(role="context")):
            data = deepcopy(self.plan_data)
            change(data)
            with self.assertRaises(ValidationError):
                ShortPlan.model_validate(data)

    def test_duration_is_strictly_under_three_minutes(self):
        for b in self.sources.values():
            b["duration"] = 36
        with self.assertRaisesRegex(ValueError, "strictly less than"):
            validate_plan(self.wd, self.record, self.sb, self.notes, self.plan, self.sources)
        self.sources["s03b01"]["duration"] -= 1 / 30
        self.assertEqual(len(validate_plan(self.wd, self.record, self.sb, self.notes, self.plan, self.sources)), 5)

    def test_unknown_beats_and_unsupported_social_numbers_fail(self):
        sources = dict(self.sources)
        del sources["s03b01"]
        with self.assertRaisesRegex(ValueError, "unknown source beat"):
            validate_plan(self.wd, self.record, self.sb, self.notes, self.plan, sources)
        data = deepcopy(self.plan_data)
        data["title"] = "99% of AI systems fail"
        with self.assertRaisesRegex(ValueError, "unsupported"):
            validate_plan(self.wd, self.record, self.sb, self.notes, ShortPlan.model_validate(data), self.sources)

    def test_narration_and_caveat_survive_captioning(self):
        chosen = list(self.sources.values())
        cues = short_cues(chosen)
        text = " ".join(c[2] for c in cues)
        self.assertEqual(text, " ".join(b["beat"].narration for b in chosen))
        self.assertIn("Its experiments are proposals", text)
        self.assertAlmostEqual(cues[-1][1], 49.5)
        self.assertTrue(all(start < end for start, end, _ in cues))
        self.assertTrue(all(a[1] <= b[0] + 1e-8 for a, b in zip(cues, cues[1:])))

    def test_every_segment_begins_with_its_first_caption(self):
        for b, segment in zip(self.sources.values(), self.plan.segments):
            local = short_cues([b])
            self.assertEqual(local[0][0], 0)
            self.assertTrue(b["beat"].narration.startswith(local[0][2]))

    def test_real_render_keeps_first_cues_despite_probe_rounding(self):
        source = self.wd.root / "source.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
             "color=c=blue:s=64x36:r=30:d=2", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(source)])
        chosen = list(self.sources.values())
        self.wd.audio.mkdir()
        for b in chosen:
            b.update(clip=source, start=0, duration=31 / 30, narration_duration=0.9)
            b["beat"] = b["beat"].model_copy(update={"narration": "First caption. Final caption."})
            with wave.open(str(self.wd.audio / f"{b['beat'].id}.wav"), "wb") as f:
                f.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
                f.writeframes(b"\0\0" * 21600)
        # Real ffprobe reports rounded decimals; force enough drift to reproduce the old cut bug.
        def rounded_probe(path):
            result = probe(path)
            if Path(path).parent == self.wd.render / "short" / "test-key":
                result["duration"] += 0.00001
            return result
        cfg = SimpleNamespace(publish=SimpleNamespace(site_url="https://example.org"))
        with patch("paper_video.shorts.load_inputs", return_value=(self.plan, chosen, "test-key")), \
             patch("paper_video.shorts.probe", side_effect=rounded_probe):
            result = build_short(self.wd, self.record, cfg)
        self.assertEqual((result["width"], result["height"]), (1080, 1920))
        self.assertLess(result["duration"], 180)
        captions = sorted((self.wd.render / "short" / "test-key").glob("*.ass"))
        self.assertEqual(len(captions), 5)
        for path in captions:
            first = next(line for line in path.read_text().splitlines() if line.startswith("Dialogue:"))
            self.assertIn("0:00:00.00", first)
            self.assertIn("First caption.", first)

    def test_subtitle_markup_is_literal_and_overflow_fails(self):
        self.assertEqual(ass_text("{test}"), r"\{test\}")
        path = self.wd.root / "captions.ass"
        with self.assertRaisesRegex(ValueError, "more than three"):
            caption_file(path, [(0, 1, "a long sentence " * 20)])






    def test_source_edits_and_renderer_changes_invalidate_review(self):
        for p in (self.wd.paper, self.wd.notes, self.wd.storyboard):
            p.write_text("source")
        chosen = list(self.sources.values())
        for b in chosen:
            b["clip"].parent.mkdir(parents=True, exist_ok=True)
            b["clip"].write_bytes(b"visuals")
            wav = self.wd.audio / f"{b['beat'].id}.wav"
            wav.parent.mkdir(parents=True, exist_ok=True)
            wav.write_bytes(b"audio")
        original = content_key(self.wd, self.plan, chosen)
        review = ShortReview(content_key=original, science={"verdict": "accurate", "issues": []}, visual_issues=[])
        save_model(self.wd.root / "short-review.yaml", review)
        self.assertIsNotNone(current_short_review(self.wd, original))
        self.wd.storyboard.write_text("changed source")
        changed = content_key(self.wd, self.plan, chosen)
        self.assertNotEqual(original, changed)
        self.assertIsNone(current_short_review(self.wd, changed))
        self.wd.storyboard.write_text("source")
        with patch("paper_video.shorts.file_hash", return_value="new renderer"):
            self.assertNotEqual(original, content_key(self.wd, self.plan, chosen))

    def test_check_refuses_changed_video_and_missing_or_major_review(self):
        out = self.wd.out / "short"
        out.mkdir(parents=True)
        for name in ("video.mp4", "cover.jpg", "captions.srt", "captions.vtt"):
            (out / name).write_bytes(b"output")
        save_json(out / "timeline.json", {"content_key": "current", "video_sha256": "video", "duration": 50})
        accurate = ShortReview(content_key="current", science={"verdict": "accurate", "issues": []}, visual_issues=[])
        with patch("paper_video.shorts.load_inputs", return_value=(self.plan, [], "current")), \
             patch("paper_video.shorts.file_hash", return_value="video"), \
             patch("paper_video.shorts.probe", return_value={"width": 1080, "height": 1920, "duration": 50}):
            with self.assertRaisesRegex(ValueError, "review.*missing"):
                check_short(self.wd, self.record, SimpleNamespace())
            save_model(self.wd.root / "short-review.yaml", accurate)
            check_short(self.wd, self.record, SimpleNamespace())
            accurate.visual_issues = [VisualIssue(beat="s03b01", severity="major", problem="Unreadable",
                                                  suggested_fix="Change the edit")]
            save_model(self.wd.root / "short-review.yaml", accurate)
            with self.assertRaisesRegex(ValueError, "Unreadable"):
                check_short(self.wd, self.record, SimpleNamespace())
            with patch("paper_video.shorts.file_hash", return_value="modified video"):
                with self.assertRaisesRegex(ValueError, "out of date"):
                    check_short(self.wd, self.record, SimpleNamespace())

    def test_paper_approval_cannot_upload_before_short_passes(self):
        with patch.object(pipeline, "_open", return_value=(SimpleNamespace(), self.wd, self.record)), \
             patch.object(pipeline, "load_model"), \
             patch.object(pipeline, "check_short", side_effect=ValueError("short missing")), \
             patch.object(pipeline.subprocess, "run") as upload:
            with self.assertRaisesRegex(ValueError, "short missing"):
                pipeline.approve("test-paper")
            upload.assert_not_called()


if __name__ == "__main__":
    unittest.main()
