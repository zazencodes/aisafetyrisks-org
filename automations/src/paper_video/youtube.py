"""Stage: YouTube package (youtube.yaml). The copy is written in the agent session.

The `upload` block is a ready YouTube Data API v3 `videos.insert` body, and `files`
names the media to send with it, so an uploader can be added later without changing
the pipeline. Nothing is uploaded here.
"""

from aisr_site.schema import Work

from paper_video import log
from paper_video.context import short_citation
from paper_video.models import PaperRecord, YouTubeCopy
from paper_video.workdir import WorkDir, dump_yaml, load_model


def _stamp(seconds: float) -> str:
    s = int(seconds)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def youtube_package(wd: WorkDir, record: PaperRecord, work: Work, site_url: str) -> dict:
    copy = load_model(wd.youtube_copy, YouTubeCopy)
    page = f"{site_url}/works/{wd.slug}/"
    chapters = "\n".join(f"{_stamp(c.start)} {c.title}" for c in work.video.chapters)
    description = (
        f"{copy.description.strip()}\n\n"
        f"Full explainer, with every claim linked to the passage in the paper that supports it:\n{page}\n\n"
        f"Paper: {record.title}\n{', '.join(record.authors)} ({record.published.year})\n{record.url}\n\n"
        f"Chapters\n{chapters}\n\n"
        "Narration uses a synthetic voice. Animation made with Manim Community."
    )
    if len(description) > 5000:
        raise ValueError("YouTube descriptions are limited to 5000 characters")
    package = {
        "files": {"video": "out/video.mp4", "thumbnail": "out/thumbnail.jpg", "captions": "out/captions.srt"},
        "links": {"website": page, "paper": str(record.url), "pdf": str(record.pdf_url)},
        "citation": short_citation(record),
        "upload": {
            "snippet": {
                "title": copy.title,
                "description": description,
                "tags": copy.tags,
                "categoryId": "27",  # Education
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en",
            },
            "status": {
                "privacyStatus": "private",
                "selfDeclaredMadeForKids": False,
                "containsSyntheticMedia": False,
            },
        },
    }
    wd.youtube.write_text(dump_yaml(package))
    log(f"youtube package written: {wd.youtube}")
    return package
