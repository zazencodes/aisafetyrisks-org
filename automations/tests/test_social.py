"""Weekly release slots, post bodies and the schedule sequence, against a fake Zernio."""

import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from zoneinfo import ZoneInfo

import httpx
import yaml

from paper_video import social
from paper_video.config import load_config
from paper_video.models import SocialRecord
from paper_video.workdir import WorkDir, dump_yaml, load_model

TORONTO = ZoneInfo("America/Toronto")
CFG = load_config()


def at(*args) -> datetime:
    return datetime(*args, tzinfo=TORONTO)


class SlotTests(unittest.TestCase):
    def test_first_release_is_the_next_tuesday_and_its_thursday(self):
        friday = at(2026, 10, 2, 22, 0)
        long_form = social.long_form_time(CFG.social, friday, None)
        self.assertEqual(long_form, at(2026, 10, 6, 9, 0))
        self.assertEqual(social.short_time(CFG.social, long_form), at(2026, 10, 8, 9, 0))

    def test_a_tuesday_slot_that_has_passed_moves_to_next_week(self):
        self.assertEqual(social.long_form_time(CFG.social, at(2026, 10, 6, 8, 59), None), at(2026, 10, 6, 9, 0))
        self.assertEqual(social.long_form_time(CFG.social, at(2026, 10, 6, 9, 0), None), at(2026, 10, 13, 9, 0))

    def test_releases_follow_the_previous_week_in_local_time_across_dst(self):
        previous = at(2026, 10, 27, 9, 0).astimezone(timezone.utc)
        following = social.long_form_time(CFG.social, at(2026, 10, 2, 22, 0), previous)
        self.assertEqual(following, at(2026, 11, 3, 9, 0))
        self.assertEqual(following.utcoffset(), timedelta(hours=-5))


class NextWorkTests(unittest.TestCase):
    def test_earliest_site_publication_without_a_complete_release_goes_next(self):
        def work(day, status="published"):
            return SimpleNamespace(status=status, published_at=at(2026, 9, day, 12, 0))
        done = SimpleNamespace(short=object())
        half = SimpleNamespace(short=None)
        works = {"a": work(28), "b": work(29), "c": work(30), "d": work(27, "draft")}
        self.assertEqual(social.next_work(works, {"a": done, "b": None, "c": half, "d": None}), "b")
        self.assertEqual(social.next_work(works, {"a": done, "b": done, "c": half, "d": None}), "c")
        with self.assertRaises(RuntimeError):
            social.next_work(works, {"a": done, "b": done, "c": done, "d": None})


SHORT_PACKAGE = {"title": "Why an AI might allow shutdown", "description": "Short description.",
                 "links": {"explainer": "https://aisafetyrisks.org/works/p/", "paper": "https://arxiv.org/abs/1"},
                 "citation": "Author et al. (2016)"}


class BodyTests(unittest.TestCase):
    def test_short_goes_to_youtube_and_instagram_with_the_title_in_the_caption(self):
        body = social.short_body(CFG.social, SHORT_PACKAGE, "https://v", "https://c", at(2026, 10, 8, 9, 0))
        youtube, instagram = body["platforms"]
        self.assertEqual(body["scheduledFor"], "2026-10-08T09:00:00-04:00")
        self.assertEqual(youtube["platformSpecificData"]["title"], SHORT_PACKAGE["title"])
        self.assertEqual(youtube["platformSpecificData"]["visibility"], "public")
        self.assertTrue(instagram["customContent"].startswith(SHORT_PACKAGE["title"] + "\n\n"))
        self.assertEqual(instagram["platformSpecificData"]["instagramThumbnail"], "https://c")
        self.assertIn("https://aisafetyrisks.org/works/p/", body["content"])

    def test_overlong_instagram_caption_fails(self):
        package = {**SHORT_PACKAGE, "description": "x" * 2100}
        with self.assertRaises(ValueError):
            social.short_body(CFG.social, package, "https://v", "https://c", at(2026, 10, 8, 9, 0))


class FakeZernio:
    def __init__(self):
        self.posts, self.uploads = [], []

    def handle(self, request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/media/presign"):
            name = json.loads(request.content)["filename"]
            return httpx.Response(200, json={"uploadUrl": f"https://storage/{name}",
                                             "publicUrl": f"https://media.zernio.com/temp/{name}"})
        body = json.loads(request.content)
        self.posts.append((request.headers["Idempotency-Key"], body))
        scheduled = datetime.fromisoformat(body["scheduledFor"]).astimezone(timezone.utc)
        return httpx.Response(201, json={"post": {
            "_id": f"post{len(self.posts)}", "status": "scheduled",
            "scheduledFor": scheduled.isoformat().replace("+00:00", "Z"),
            "platforms": [{"platform": p["platform"], "status": "pending"} for p in body["platforms"]]}})

    def put(self, url, content, timeout, headers):
        self.uploads.append((url, headers["Content-Type"]))
        return httpx.Response(200, request=httpx.Request("PUT", url))


class ScheduleTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.works, self.site = root / "works", root / "site"
        self.wd = WorkDir(self.works / "p")
        (self.wd.out / "short").mkdir(parents=True)
        for name in ("video.mp4", "thumbnail.jpg", "short/video.mp4", "short/cover.jpg"):
            (self.wd.out / name).write_bytes(name.encode())
        self.wd.paper.write_text("")
        (self.wd.root / "short-package.yaml").write_text(dump_yaml({
            **SHORT_PACKAGE, "content_key": "k", "review": {"content_key": "k"},
            "files": {"video": "out/short/video.mp4", "cover": "out/short/cover.jpg"}}))
        sha = social.file_hash(self.wd.out / "video.mp4")
        (self.site / "p").mkdir(parents=True)
        (self.site / "p" / "work.yaml").write_text("")
        self.work = SimpleNamespace(status="published", published_at=at(2026, 9, 28, 12, 0),
                                    video=SimpleNamespace(key=f"works/p/video-{sha[:12]}.mp4"))
        self.zernio = FakeZernio()
        package = {"files": {"video": "out/video.mp4", "thumbnail": "out/thumbnail.jpg"},
                   "title": "Long title", "description": "Long description", "tags": ["ai safety"]}
        transport = httpx.MockTransport(self.zernio.handle)
        for target, value in [
            ("WORKS", self.works), ("SITE_WORKS", self.site),
            ("load_model", MagicMock(side_effect=self.load)),
            ("ensure_source", MagicMock()), ("check_short", MagicMock(return_value={"content_key": "k"})),
            ("youtube_package", MagicMock(return_value=package)),
            ("client", lambda cfg: httpx.Client(transport=transport, base_url=social.API)),
        ]:
            p = patch.object(social, target, value)
            p.start()
            self.addCleanup(p.stop)
        put = patch.object(social.httpx, "put", self.zernio.put)
        put.start()
        self.addCleanup(put.stop)
        for_slug = patch.object(social.WorkDir, "for_slug", lambda slug: self.wd)
        for_slug.start()
        self.addCleanup(for_slug.stop)

    def load(self, path, cls):
        if path.name == "work.yaml":
            return self.work
        if path.name == "social.yaml":
            return load_model(path, cls)
        return MagicMock()

    def test_schedules_long_form_then_short_and_records_both(self):
        self.assertEqual(social.schedule_next(CFG, at(2026, 10, 2, 22, 0)), "p")
        (long_key, long_body), (short_key, short_body) = self.zernio.posts
        self.assertNotEqual(long_key, short_key)
        self.assertEqual(long_body["scheduledFor"], "2026-10-06T09:00:00-04:00")
        self.assertEqual([p["platform"] for p in long_body["platforms"]], ["youtube"])
        self.assertEqual(long_body["mediaItems"][0]["thumbnail"], "https://media.zernio.com/temp/thumbnail.jpg")
        self.assertEqual(short_body["scheduledFor"], "2026-10-08T09:00:00-04:00")
        self.assertEqual([p["platform"] for p in short_body["platforms"]], ["youtube", "instagram"])
        self.assertEqual([t for _, t in self.zernio.uploads], ["video/mp4", "image/jpeg"] * 2)
        record = load_model(self.wd.root / "social.yaml", SocialRecord)
        self.assertEqual((record.long_form.post_id, record.short.post_id), ("post1", "post2"))
        self.assertEqual(record.long_form.scheduled_for, at(2026, 10, 6, 9, 0))
        with self.assertRaises(RuntimeError):
            social.schedule_next(CFG, at(2026, 10, 2, 22, 0))

    def test_an_interrupted_release_schedules_only_the_missing_short(self):
        social.schedule_next(CFG, at(2026, 10, 2, 22, 0))
        record = yaml.safe_load((self.wd.root / "social.yaml").read_text())
        record["short"] = None
        (self.wd.root / "social.yaml").write_text(dump_yaml(record))
        self.zernio.posts.clear()
        social.schedule_next(CFG, at(2026, 10, 5, 12, 0))
        [(_, body)] = self.zernio.posts
        self.assertEqual(body["scheduledFor"], "2026-10-08T09:00:00-04:00")

    def test_a_long_video_that_is_not_the_published_one_is_refused(self):
        (self.wd.out / "video.mp4").write_bytes(b"re-rendered")
        with self.assertRaisesRegex(ValueError, "not the published video"):
            social.schedule_next(CFG, at(2026, 10, 2, 22, 0))
        self.assertEqual(self.zernio.posts, [])


if __name__ == "__main__":
    unittest.main()
