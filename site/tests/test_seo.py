"""Check the generated SEO artifacts against the actual rendered pages."""

import importlib
import json
import shutil
import tempfile
import unittest
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET

import yaml
from pydantic import ValidationError

builder = importlib.import_module("aisr_site.build")
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9",
      "v": "http://www.google.com/schemas/sitemap-video/1.1"}


class PageMetadata(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.payloads = []
        self.in_jsonld = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        self.in_jsonld = tag == "script" and attrs.get("type") == "application/ld+json"

    def handle_data(self, data):
        if self.in_jsonld:
            self.payloads.append(json.loads(data))

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_jsonld = False


class BuildSEOTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        content = root / "content"
        shutil.copytree(builder.CONTENT, content)
        # Exercise XML/JSON escaping and draft exclusion even when previewing drafts.
        source = sorted((content / "works").iterdir())[0]
        draft = content / "works" / "seo-test-draft"
        shutil.copytree(source, draft)
        data = yaml.safe_load((draft / "work.yaml").read_text())
        data.update(status="draft", published_on=None, published_at=None, updated_on=None, review=None)
        (draft / "work.yaml").write_text(yaml.safe_dump(data))
        data = yaml.safe_load((source / "work.yaml").read_text())
        data["title"] = 'Research & oversight </script> "quoted"'
        (source / "work.yaml").write_text(yaml.safe_dump(data))
        self.dist = root / "dist"
        self.addCleanup(patch.stopall)
        patch.object(builder, "CONTENT", content).start()
        patch.object(builder, "DIST", self.dist).start()
        builder.build(include_drafts=True)

    def test_sitemap_matches_video_markup_and_player(self):
        cfg = builder.load_config()
        base = str(cfg.base_url).rstrip("/")
        sitemap = ET.parse(self.dist / "sitemap.xml")
        entries = sitemap.findall("s:url", NS)
        urls = [entry.findtext("s:loc", namespaces=NS) for entry in entries]
        expected = {base + "/"} | {f"{base}/{p.slug}/" for p in builder.load_pages()}
        expected |= {f"{base}/works/{lw.slug}/" for lw in builder.load_works(False)}
        self.assertEqual(set(urls), expected)
        self.assertEqual(len(urls), len(expected))
        for entry in entries:
            url = entry.findtext("s:loc", namespaces=NS)
            page = PageMetadata((self.dist / url.removeprefix(base).strip("/") / "index.html").read_text())
            self.assertIn(("link", {"rel": "canonical", "href": url}), page.tags)
            video_entry = entry.find("v:video", NS)
            if video_entry is None:
                continue
            nodes = [node for payload in page.payloads for node in payload["@graph"]]
            videos = [node for node in nodes if node["@type"] == "VideoObject"]
            self.assertEqual(len(videos), 1)
            video = videos[0]
            self.assertIsNotNone(datetime.fromisoformat(video["uploadDate"]).tzinfo)
            for tag, prop in [("title", "name"), ("description", "description"),
                              ("thumbnail_loc", "thumbnailUrl"), ("content_loc", "contentUrl"),
                              ("publication_date", "uploadDate")]:
                self.assertEqual(video_entry.findtext(f"v:{tag}", namespaces=NS), video[prop])
            player = next(attrs for tag, attrs in page.tags if tag == "video")
            self.assertEqual(url + player["poster"], video["thumbnailUrl"])
            self.assertIn(("source", {"src": video["contentUrl"], "type": "video/mp4"}), page.tags)
            seconds = int(video_entry.findtext("v:duration", namespaces=NS))
            self.assertEqual(video["duration"], builder.iso_duration(seconds))
            self.assertEqual(video["url"], url)
            for clip in video["hasPart"]:
                self.assertLess(clip["startOffset"], clip["endOffset"])
                self.assertLessEqual(clip["endOffset"], seconds)
                self.assertEqual(clip["url"], f'{url}#t={clip["startOffset"]}')

    def test_drafts_and_404_are_noindex_and_not_in_discovery_feeds(self):
        for path in ["works/seo-test-draft/index.html", "404.html"]:
            page = PageMetadata((self.dist / path).read_text())
            self.assertIn(("meta", {"name": "robots", "content": "noindex"}), page.tags)
        for path in ["sitemap.xml", "feed.xml"]:
            self.assertNotIn("seo-test-draft", (self.dist / path).read_text())
        self.assertIn("Sitemap: https://aisafetyrisks.org/sitemap.xml", (self.dist / "robots.txt").read_text())

    def test_published_work_requires_a_timezone_aware_timestamp(self):
        data = builder.load_works(False)[0].work.model_dump()
        for timestamp in [None, "2026-10-01T12:00:00"]:
            with self.subTest(timestamp=timestamp), self.assertRaises(ValidationError):
                builder.Work.model_validate({**data, "published_at": timestamp})


if __name__ == "__main__":
    unittest.main()
