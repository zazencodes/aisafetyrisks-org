import copy
import xml.etree.ElementTree as ET

import pytest
import yaml
from pydantic import ValidationError

from aisr_site import build as site_build
from aisr_site.schema import Work

WORK = {
    "status": "published",
    "published_on": "2026-09-25",
    "review": {"reviewed_by": "A Reviewer", "reviewed_on": "2026-09-25"},
    "title": "Test explainer",
    "dek": "A test.",
    "category": "specification",
    "paper": {
        "title": "A Paper", "authors": ["Ada Lovelace", "Alan Turing"], "published": "2021-05-28",
        "venue": None, "url": "https://arxiv.org/abs/0000.00000v1", "pdf_url": "https://arxiv.org/pdf/0000.00000v1",
        "arxiv_id": "0000.00000v1", "doi": None,
    },
    "summary": "Agents went right [c01].",
    "explanation": [{"heading": "Setup", "body": "The setup [c01, c02]."}],
    "findings": [{"kind": "observed_result", "text": "They went right [c01]."}],
    "limitations": [{"source": "authors", "text": "Toy setting [c02]."}],
    "context": "Context.",
    "claims": [
        {"id": "c01", "kind": "observed_result", "statement": "s", "evidence": [{"page": 1, "quote": "the agent went right every time"}]},
        {"id": "c02", "kind": "limitation", "statement": "s", "evidence": [{"page": 2, "quote": "this is a toy environment only"}]},
    ],
    "references": [{"title": "A Paper", "url": "https://arxiv.org/abs/0000.00000v1", "note": None}],
    "video": {"key": "works/test/video-abc.mp4", "duration_seconds": 61.0, "width": 1920, "height": 1080,
              "captions": "captions.vtt", "chapters": [{"start": 0, "title": "Intro"}], "youtube_url": None},
    "thumbnail": "thumbnail.jpg",
    "production": {"pipeline": "test"},
}


def test_schema_rejects_unknown_citation():
    bad = copy.deepcopy(WORK)
    bad["summary"] = "Unsupported [c09]."
    with pytest.raises(ValidationError, match="unknown claims"):
        Work.model_validate(bad)


def test_schema_requires_review_to_publish():
    bad = copy.deepcopy(WORK)
    bad["review"] = None
    with pytest.raises(ValidationError, match="review"):
        Work.model_validate(bad)


def test_build(tmp_path, monkeypatch):
    content = tmp_path / "content"
    (content / "pages").mkdir(parents=True)
    (content / "site.yaml").write_text(
        (site_build.CONTENT / "site.yaml").read_text()
    )
    (content / "pages" / "about.md").write_text("---\ntitle: About\ndescription: d\n---\nHello.\n")
    work_dir = content / "works" / "test"
    work_dir.mkdir(parents=True)
    (work_dir / "work.yaml").write_text(yaml.safe_dump(WORK))
    (work_dir / "thumbnail.jpg").write_bytes(b"jpg")
    (work_dir / "captions.vtt").write_text("WEBVTT\n")
    monkeypatch.setattr(site_build, "CONTENT", content)
    monkeypatch.setattr(site_build, "DIST", tmp_path / "dist")

    dist = site_build.build()
    page = (dist / "works" / "test" / "index.html").read_text()
    assert 'href="#evidence-c01"' in page and 'id="evidence-c02"' in page
    assert "https://media.aisafetyrisks.org/works/test/video-abc.mp4" in page
    assert "Test explainer" in (dist / "index.html").read_text()
    ET.fromstring((dist / "feed.xml").read_text())
    sitemap = (dist / "sitemap.xml").read_text()
    assert "https://aisafetyrisks.org/works/test/" in sitemap
    assert (dist / "_headers").exists() and (dist / "404.html").exists()


def test_drafts_are_excluded_by_default(tmp_path, monkeypatch):
    content = tmp_path / "content"
    (content / "pages").mkdir(parents=True)
    (content / "site.yaml").write_text((site_build.CONTENT / "site.yaml").read_text())
    work_dir = content / "works" / "draft"
    work_dir.mkdir(parents=True)
    draft = {**copy.deepcopy(WORK), "status": "draft", "published_on": None, "review": None}
    (work_dir / "work.yaml").write_text(yaml.safe_dump(draft))
    (work_dir / "thumbnail.jpg").write_bytes(b"jpg")
    (work_dir / "captions.vtt").write_text("WEBVTT\n")
    monkeypatch.setattr(site_build, "CONTENT", content)
    monkeypatch.setattr(site_build, "DIST", tmp_path / "dist")

    assert not (site_build.build() / "works").exists()
    assert (site_build.build(include_drafts=True) / "works" / "draft" / "index.html").exists()
