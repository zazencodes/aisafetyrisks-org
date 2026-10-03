"""Stage: schedule the weekly release of published explainers through Zernio (social.yaml).

Each week releases one published explainer, oldest site publication first: the long-form video
on YouTube on `long_form_day`, then its short on YouTube Shorts and Instagram Reels on the next
`short_day`. Zernio holds the media and publishes at the scheduled time; social.yaml in the work
directory records the Zernio post ids. Copy comes from youtube.yaml and short-package.yaml.
"""

import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import httpx
import yaml
from aisr_site.schema import Work
from dotenv import dotenv_values

from paper_video import log
from paper_video.config import REPO, SITE_WORKS, WORKS, Config, SocialConfig
from paper_video.ingest import ensure_source
from paper_video.models import PaperRecord, SocialPost, SocialRecord
from paper_video.shorts import check_short, file_hash
from paper_video.workdir import WorkDir, load_model, save_model
from paper_video.youtube import youtube_package

API = "https://zernio.com/api/v1"
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
CONTENT_TYPES = {".mp4": "video/mp4", ".jpg": "image/jpeg"}
YOUTUBE = {"visibility": "public", "categoryId": "27",  # Education
           "madeForKids": False, "containsSyntheticMedia": False}


def record_path(slug: str) -> Path:
    return WORKS / slug / "social.yaml"


def load_record(slug: str) -> SocialRecord | None:
    path = record_path(slug)
    return load_model(path, SocialRecord) if path.exists() else None


def client(cfg: SocialConfig) -> httpx.Client:
    key = dotenv_values(REPO / ".env").get("ZERNIO_API_KEY")
    if not key:
        raise ValueError("set ZERNIO_API_KEY in the repository's ignored .env before scheduling")
    return httpx.Client(base_url=API, headers={"Authorization": f"Bearer {key}"},
                        timeout=cfg.timeout_seconds)


def _check(response: httpx.Response) -> dict:
    if response.is_error:
        raise RuntimeError(f"Zernio {response.request.method} {response.request.url.path} "
                           f"returned {response.status_code}: {response.text}")
    return response.json()


def next_work(works: dict[str, Work], records: dict[str, SocialRecord | None]) -> str:
    """The published explainer with the earliest site publication whose release is incomplete."""
    pending = [slug for slug, work in works.items() if work.status == "published"
               and (records[slug] is None or records[slug].short is None)]
    if not pending:
        raise RuntimeError("every published explainer is already scheduled")
    return min(pending, key=lambda slug: works[slug].published_at)


def _next(cfg: SocialConfig, weekday: str, after: datetime) -> datetime:
    zone = ZoneInfo(cfg.timezone)
    day = after.astimezone(zone).date()
    while day.weekday() != WEEKDAYS.index(weekday) or datetime.combine(day, cfg.time, zone) <= after:
        day += timedelta(days=1)
    return datetime.combine(day, cfg.time, zone)


def long_form_time(cfg: SocialConfig, now: datetime, previous: datetime | None) -> datetime:
    """The first long-form slot in the future and after the previous release."""
    return _next(cfg, cfg.long_form_day, now if previous is None else max(now, previous))


def short_time(cfg: SocialConfig, long_form: datetime) -> datetime:
    """The first short slot after the long-form release."""
    return _next(cfg, cfg.short_day, long_form)


def long_form_body(cfg: SocialConfig, package: dict, video: str, thumbnail: str, when: datetime) -> dict:
    return {
        "content": package["description"],
        "tags": package["tags"],
        "mediaItems": [{"type": "video", "url": video, "thumbnail": thumbnail}],
        "platforms": [{"platform": "youtube", "accountId": cfg.youtube_account,
                       "platformSpecificData": {"title": package["title"], **YOUTUBE}}],
        "scheduledFor": when.isoformat(),
        "timezone": cfg.timezone,
    }


def short_body(cfg: SocialConfig, package: dict, video: str, cover: str, when: datetime) -> dict:
    text = (f"{package['description'].strip()}\n\n"
            f"Full explainer, with every claim linked to the paper:\n{package['links']['explainer']}\n\n"
            f"Paper: {package['citation']}\n{package['links']['paper']}")
    caption = f"{package['title']}\n\n{text}"
    if len(package["title"]) > 100 or len(text) > 5000:
        raise ValueError("YouTube titles are limited to 100 characters and descriptions to 5000")
    if len(caption) > 2200:
        raise ValueError(f"Instagram captions are limited to 2200 characters; this one has {len(caption)}")
    return {
        "content": text,
        "mediaItems": [{"type": "video", "url": video}],
        "platforms": [
            {"platform": "youtube", "accountId": cfg.youtube_account,
             "platformSpecificData": {"title": package["title"], **YOUTUBE}},
            {"platform": "instagram", "accountId": cfg.instagram_account, "customContent": caption,
             "platformSpecificData": {"instagramThumbnail": cover}},
        ],
        "scheduledFor": when.isoformat(),
        "timezone": cfg.timezone,
    }


def upload(http: httpx.Client, path: Path) -> str:
    """Upload a file to Zernio's media storage and return its public URL."""
    content_type = CONTENT_TYPES[path.suffix]
    presigned = _check(http.post("/media/presign", json={
        "filename": path.name, "contentType": content_type, "size": path.stat().st_size}))
    with path.open("rb") as f:
        stored = httpx.put(presigned["uploadUrl"], content=f, timeout=http.timeout,
                           headers={"Content-Type": content_type})
    if stored.is_error:
        raise RuntimeError(f"media upload of {path} failed with {stored.status_code}: {stored.text}")
    log(f"uploaded {path.name}")
    return presigned["publicUrl"]


def create_post(http: httpx.Client, body: dict, idempotency_key: str, video_sha256: str) -> SocialPost:
    post = _check(http.post("/posts", json=body, headers={"Idempotency-Key": idempotency_key}))["post"]
    if post["status"] != "scheduled":
        raise RuntimeError(f"Zernio post {post['_id']} is {post['status']!r}, not scheduled: {post}")
    return SocialPost.from_api(post, video_sha256)


def schedule_next(cfg: Config, now: datetime) -> str:
    works = {p.parent.name: load_model(p, Work) for p in SITE_WORKS.glob("*/work.yaml")}
    records = {slug: load_record(slug) for slug in works}
    slug = next_work(works, records)
    wd = WorkDir.for_slug(slug)
    paper = load_model(wd.paper, PaperRecord)
    ensure_source(wd, paper)
    short = check_short(wd, paper, cfg)
    short_package = yaml.safe_load((wd.root / "short-package.yaml").read_text())
    if short_package["content_key"] != short["content_key"] or short_package["review"] is None:
        raise ValueError(f"short-package.yaml is out of date; run `paper-video short {slug}`")
    long_package = youtube_package(wd, paper, works[slug], cfg.publish.site_url)
    record = records[slug]
    with client(cfg.social) as http:
        if record is None:
            previous = max((r.long_form.scheduled_for for r in records.values() if r), default=None)
            when = long_form_time(cfg.social, now, previous)
            video = wd.root / long_package["files"]["video"]
            sha = file_hash(video)
            if f"video-{sha[:12]}.mp4" != Path(works[slug].video.key).name:
                raise ValueError(f"{video} is not the published video {works[slug].video.key}")
            body = long_form_body(cfg.social, long_package, upload(http, video),
                                  upload(http, wd.root / long_package["files"]["thumbnail"]), when)
            record = SocialRecord(long_form=create_post(http, body, _key(slug, "long-form", sha), sha), short=None)
            save_model(record_path(slug), record)
            log(f"{slug}: long-form scheduled for {when.isoformat()} (Zernio post {record.long_form.post_id})")
        when = short_time(cfg.social, record.long_form.scheduled_for)
        video = wd.root / short_package["files"]["video"]
        sha = file_hash(video)
        body = short_body(cfg.social, short_package, upload(http, video),
                          upload(http, wd.root / short_package["files"]["cover"]), when)
        record.short = create_post(http, body, _key(slug, "short", sha), sha)
        save_model(record_path(slug), record)
        log(f"{slug}: short scheduled for {when.isoformat()} (Zernio post {record.short.post_id})")
    return slug


def _key(slug: str, kind: str, sha: str) -> str:
    return hashlib.sha256(f"{slug}:{kind}:{sha}".encode()).hexdigest()


def refresh(cfg: SocialConfig) -> list[str]:
    """Read every scheduled post back from Zernio; return a line per failed platform."""
    failures = []
    with client(cfg) as http:
        for path in sorted(WORKS.glob("*/social.yaml")):
            record = load_model(path, SocialRecord)
            for name in ("long_form", "short"):
                post = getattr(record, name)
                if post is None:
                    continue
                fetched = _check(http.get(f"/posts/{post.post_id}"))["post"]
                setattr(record, name, SocialPost.from_api(fetched, post.video_sha256))
                for p in getattr(record, name).platforms:
                    log(f"{path.parent.name} {name} {p.platform}: {p.status} {p.url or ''}".rstrip())
                    if p.status == "failed":
                        failures.append(f"{path.parent.name} {name} {p.platform}: {p.error}")
            save_model(path, record)
    return failures
