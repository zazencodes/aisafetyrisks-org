"""Automatic archives preserve exports and refuse missing drives or corrupt copies."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from pydantic import ValidationError

from paper_video import pipeline
from paper_video.backup import BACKLOG_HEADER, backup_work, checksum, pending_backups
from paper_video.config import BackupConfig
from paper_video.workdir import WorkDir


class BackupTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.backlog = root / "media-backups.md"
        self.backlog.write_text(BACKLOG_HEADER)
        backlog_patch = patch("paper_video.backup.BACKLOG", self.backlog)
        backlog_patch.start()
        self.addCleanup(backlog_patch.stop)
        self.wd = WorkDir(root / "paper")
        self.wd.out.mkdir(parents=True)
        self.wd.audio.mkdir()
        self.wd.scenes.mkdir()
        (self.wd.out / "video.mp4").write_bytes(b"finished full video")
        (self.wd.out / "captions.vtt").write_text("complete captions")
        (self.wd.audio / "beat.wav").write_bytes(b"paid narration")
        self.wd.notes.write_text("verified source notes")
        (self.wd.scenes / "s01.py").write_text("scene source")
        self.volume = root / "drive"
        self.volume.mkdir()
        self.cfg = BackupConfig(volume=self.volume, root=self.volume / "Media Backups")
        commit = patch("paper_video.backup.subprocess.check_output", return_value="test-commit\n")
        commit.start()
        self.addCleanup(commit.stop)

    def test_archive_copies_and_verifies_available_files_and_reuses_unchanged_payload(self):
        with patch.object(Path, "is_mount", return_value=True):
            snapshot = backup_work(self.wd, self.cfg, "full")
            again = backup_work(self.wd, self.cfg, "full")
        self.assertEqual(snapshot, again)
        manifest = json.loads((snapshot / "manifest.json").read_text())
        self.assertEqual(manifest["file_count"], 5)
        self.assertEqual(manifest["video_count"], 1)
        self.assertIn("works/paper/audio/beat.wav", [e["path"] for e in manifest["files"]])
        for entry in manifest["files"]:
            self.assertEqual(checksum(snapshot / entry["path"]), entry["sha256"])
        self.assertEqual((self.wd.out / "video.mp4").read_bytes(), b"finished full video")
        self.assertFalse(list(self.cfg.root.rglob("*.in-progress")))

    def test_changed_video_gets_a_new_snapshot_without_overwriting_previous_video(self):
        with patch.object(Path, "is_mount", return_value=True):
            original = backup_work(self.wd, self.cfg, "full")
            (self.wd.out / "video.mp4").write_bytes(b"updated video")
            changed = backup_work(self.wd, self.cfg, "full")
        self.assertNotEqual(original, changed)
        self.assertEqual((original / "works/paper/out/video.mp4").read_bytes(), b"finished full video")
        self.assertEqual((changed / "works/paper/out/video.mp4").read_bytes(), b"updated video")

    def test_unmounted_drive_fails_without_creating_a_local_backup_directory(self):
        with patch.object(Path, "is_mount", return_value=False):
            with self.assertRaisesRegex(FileNotFoundError, "not mounted"):
                backup_work(self.wd, self.cfg, "full")
        self.assertFalse(self.cfg.root.exists())
        self.assertTrue((self.wd.out / "video.mp4").exists())

    def test_corrupt_existing_archive_fails_on_rerun(self):
        with patch.object(Path, "is_mount", return_value=True):
            snapshot = backup_work(self.wd, self.cfg, "full")
            (snapshot / "works/paper/out/video.mp4").write_bytes(b"corrupt")
            with self.assertRaisesRegex(ValueError, "verification failed"):
                backup_work(self.wd, self.cfg, "full")

    def test_failed_copy_never_becomes_a_completed_snapshot(self):
        def corrupt_copy(source, target):
            Path(target).write_bytes(b"corrupted copy")
        with patch.object(Path, "is_mount", return_value=True), \
             patch("paper_video.backup.shutil.copyfile", side_effect=corrupt_copy):
            with self.assertRaisesRegex(ValueError, "verification failed"):
                backup_work(self.wd, self.cfg, "full")
        self.assertFalse(list(self.cfg.root.rglob("manifest.json")))
        self.assertEqual(len(list(self.cfg.root.rglob("*.in-progress"))), 1)

    def test_config_requires_paths_inside_the_volume(self):
        for volume, root in [("relative", "/backup"), ("/drive", "/other/backup"),
                             ("/drive", "/drive/../elsewhere")]:
            with self.assertRaises(ValidationError):
                BackupConfig(volume=volume, root=root)

    def test_creation_commands_archive_only_after_successful_assembly(self):
        cfg = SimpleNamespace(backup=self.cfg, captions=None)
        record = SimpleNamespace()
        events = []
        def assembled(*args):
            events.append("assembled")
            return {"duration": 30, "problems": []}
        def backed_up(wd, backup, kind):
            events.append(kind)
            self.assertIs(backup, self.cfg)
            return self.cfg.root / "snapshot"
        with patch.object(pipeline, "_open", return_value=(cfg, self.wd, record)), \
             patch.object(pipeline, "_storyboard", return_value=SimpleNamespace(scenes=[])), \
             patch.object(pipeline, "SceneRenderer"), \
             patch.object(pipeline, "assemble_video", side_effect=assembled), \
             patch.object(pipeline, "build_short", side_effect=assembled), \
             patch.object(pipeline, "backup_work", side_effect=backed_up):
            pipeline.assemble("paper")
            pipeline.short_work("paper")
        self.assertEqual(events, ["assembled", "full", "assembled", "short"])

    def test_creation_commands_defer_backup_failure_without_blocking_exports(self):
        cfg = SimpleNamespace(backup=self.cfg, captions=None)
        with patch.object(pipeline, "_open", return_value=(cfg, self.wd, SimpleNamespace())), \
             patch.object(pipeline, "_storyboard", return_value=SimpleNamespace(scenes=[])), \
             patch.object(pipeline, "SceneRenderer"), \
             patch.object(pipeline, "assemble_video", return_value={"duration": 30, "problems": []}), \
             patch.object(pipeline, "build_short", return_value={"duration": 30}), \
             patch.object(pipeline, "backup_work", side_effect=FileNotFoundError("drive not mounted")):
            for command in (pipeline.assemble, pipeline.short_work):
                command("paper")
                command("paper")
        rows = pending_backups()
        self.assertEqual([(row[0], row[1]) for row in rows], [("paper", "full"), ("paper", "short")])
        self.assertTrue(all("not mounted" in row[3] for row in rows))
        self.assertTrue((self.wd.out / "video.mp4").exists())

    def test_retry_removes_only_verified_rows_and_keeps_failed_short(self):
        cfg = SimpleNamespace(backup=self.cfg, captions=None)
        with patch.object(pipeline, "backup_work", side_effect=FileNotFoundError("not mounted")):
            pipeline._backup(self.wd, cfg, "full")
            pipeline._backup(self.wd, cfg, "short")
        with patch.object(pipeline, "load_config", return_value=cfg), \
             patch.object(WorkDir, "for_slug", return_value=self.wd), \
             patch.object(pipeline, "backup_work", side_effect=[self.volume / "verified", ValueError("corrupt snapshot")]):
            pipeline.backup_pending()
        self.assertEqual([row[:2] for row in pending_backups()], [["paper", "short"]])
        self.assertIn("corrupt snapshot", pending_backups()[0][3])

    def test_backlog_write_failure_is_not_silently_ignored(self):
        with patch.object(pipeline, "backup_work", side_effect=FileNotFoundError("not mounted")), \
             patch.object(pipeline, "update_pending_backup", side_effect=OSError("backlog unwritable")):
            with self.assertRaisesRegex(OSError, "backlog unwritable"):
                pipeline._backup(self.wd, SimpleNamespace(backup=self.cfg), "full")


if __name__ == "__main__":
    unittest.main()
