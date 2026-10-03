"""Publication dates survive regeneration and subsequent human approvals."""

import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import yaml
from aisr_site.build import CONTENT
from aisr_site.schema import Work
from paper_video import pipeline, site_content


class PublicationMetadataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = next((CONTENT / "works").glob("*/work.yaml"))
        self.work = Work.model_validate(yaml.safe_load(source.read_text()))
        self.slug = "test-paper"
        self.site_dir = self.root / "site" / self.slug
        self.site_dir.mkdir(parents=True)
        self.path = self.site_dir / "work.yaml"
        self.wd = MagicMock(slug=self.slug)
        self.wd.out = self.root / "out"
        self.wd.out.mkdir()
        self.wd.checks = self.root / "checks"
        self.record = MagicMock()

    def test_approval_records_first_timestamp_and_preserves_it_on_update(self):
        self.work.status = "draft"
        self.work.published_on = None
        self.work.published_at = None
        self.work.review = None
        self.path.write_text(yaml.safe_dump(self.work.model_dump(mode="json")))
        media = self.root / "media"
        video = media / self.work.video.key
        video.parent.mkdir(parents=True)
        video.write_bytes(b"test video")
        with ExitStack() as stack:
            for name, value in [
                ("_open", MagicMock(return_value=(MagicMock(), self.wd, self.record))),
                ("SITE_WORKS", self.site_dir.parent), ("MEDIA_MIRROR", media),
                ("metadata_text", MagicMock(return_value="")),
                ("verify_work", MagicMock(return_value=SimpleNamespace(ok=True))),
                ("current_review", MagicMock(return_value=SimpleNamespace(issues=[]))),
            ]:
                stack.enter_context(patch.object(pipeline, name, value))
            upload = stack.enter_context(patch.object(pipeline.subprocess, "run"))
            stack.enter_context(patch.object(pipeline, "check_short"))
            stack.enter_context(patch.object(pipeline.backlog, "set_status"))
            pipeline.approve(self.slug)
            first = Work.model_validate(yaml.safe_load(self.path.read_text()))
            self.assertIsNotNone(first.published_at.tzinfo)
            self.assertEqual(first.published_on, first.published_at.date())
            pipeline.approve(self.slug)
            updated = Work.model_validate(yaml.safe_load(self.path.read_text()))
            self.assertEqual(updated.published_at, first.published_at)
            self.assertEqual(updated.published_on, first.published_on)
            self.assertIsNotNone(updated.updated_on)
            self.assertIsNotNone(updated.updated_at.tzinfo)
            self.assertEqual(upload.call_count, 2)

    def test_regeneration_preserves_existing_publication_metadata(self):
        self.path.write_text(yaml.safe_dump(self.work.model_dump(mode="json")))
        draft = self.work.model_copy(update={"status": "draft", "published_on": None,
                                           "published_at": None, "updated_on": None})
        for asset in ["video.mp4", "thumbnail.jpg", "captions.vtt"]:
            (self.wd.out / asset).write_bytes(b"test asset")
        with ExitStack() as stack:
            for name, value in [
                ("SITE_WORKS", self.site_dir.parent), ("MEDIA_MIRROR", self.root / "media"),
                ("video_key", MagicMock(return_value=self.work.video.key)),
                ("load_model", MagicMock(side_effect=[self.work, MagicMock()])),
                ("assemble_work", MagicMock(return_value=(draft, []))),
                ("metadata_text", MagicMock(return_value="")),
                ("verify_work", MagicMock(return_value=SimpleNamespace(errors=[]))),
                ("save_json", MagicMock()),
            ]:
                stack.enter_context(patch.object(site_content, name, value))
            regenerated = site_content.write_site_work(self.wd, self.record, MagicMock(), {}, MagicMock())
        self.assertEqual(regenerated.status, "draft")
        self.assertEqual(regenerated.published_on, self.work.published_on)
        self.assertEqual(regenerated.published_at, self.work.published_at)


if __name__ == "__main__":
    unittest.main()
