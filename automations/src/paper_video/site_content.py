"""Stage: the page draft (site.yaml) -> a draft Work on the website, checked for provenance.

The draft is written in the session running the workflow, from `paper-video brief <slug> site`.
"""

import hashlib
import re
import shutil
from importlib.metadata import version

from aisr_site.schema import Chapter, Claim, Paper, Reference, Video, Work, claim_refs_in
from pydantic import ValidationError

from paper_video import __version__, log
from paper_video.config import MEDIA_MIRROR, SITE_WORKS, Config
from paper_video.context import metadata_text
from paper_video.models import Notes, PaperRecord, WorkDraft
from paper_video.provenance import verify_work
from paper_video.workdir import WorkDir, dump_yaml, load_model, save_json

URL = re.compile(r"https?://[^\s<>\"')\]]+")


def paper_links(pages: list[str]) -> list[str]:
    """URLs printed in the paper (code, data, project pages): the only extra links a page may use."""
    found = {}
    for text in pages:
        for url in URL.findall(re.sub(r"-\n", "", text)):
            found.setdefault(url.rstrip(".,;:"))
    return list(found)


def video_key(wd: WorkDir) -> str:
    digest = hashlib.sha256((wd.out / "video.mp4").read_bytes()).hexdigest()[:12]
    return f"works/{wd.slug}/video-{digest}.mp4"


def assemble_work(draft: WorkDraft, record: PaperRecord, notes: Notes, timeline: dict, key: str,
                  links: list[str], cfg: Config, youtube_url) -> tuple[Work | None, list[str]]:
    errors = []
    notes_by_id = {c.id: c for c in notes.claims}
    cited = []
    texts = [draft.title, draft.dek, draft.summary, draft.context] + [s.body for s in draft.explanation]
    texts += [f.text for f in draft.findings] + [lim.text for lim in draft.limitations]
    for t in texts:
        for ref in claim_refs_in(t):
            if ref not in notes_by_id:
                errors.append(f"cites {ref}, which is not in the notes")
            elif ref not in cited:
                cited.append(ref)
    bad_links = [r.url for r in draft.extra_references if r.url not in links]
    errors += [f"extra reference {u} is not a URL printed in the paper" for u in bad_links]
    if errors:
        return None, errors

    order = [c.id for c in notes.claims]
    claims = [
        Claim(id=c.id, kind=c.kind, statement=c.statement, evidence=c.evidence)
        for c in sorted((notes_by_id[i] for i in cited), key=lambda c: order.index(c.id))
    ]
    references = [
        Reference(title=record.title, url=record.url, note="the original paper"),
        *[Reference(title=r.title, url=r.url, note=r.note) for r in draft.extra_references],
    ]
    try:
        work = Work(
            status="draft",
            title=draft.title,
            dek=draft.dek,
            category=draft.category,
            paper=Paper(
                title=record.title, authors=record.authors, published=record.published, venue=record.venue,
                url=record.url, pdf_url=record.pdf_url, arxiv_id=record.arxiv_id, doi=record.doi,
            ),
            summary=draft.summary,
            explanation=draft.explanation,
            findings=[f.model_dump() for f in draft.findings],
            limitations=[lim.model_dump() for lim in draft.limitations],
            context=draft.context,
            claims=claims,
            references=references,
            video=Video(
                key=key,
                duration_seconds=round(timeline["duration"], 2),
                width=timeline["width"],
                height=timeline["height"],
                captions="captions.vtt",
                chapters=[Chapter(**c) for c in timeline["chapters"]],
                youtube_url=youtube_url,
            ),
            thumbnail="thumbnail.jpg",
            production={
                "pipeline": f"paper-video {__version__}",
                "language_model": cfg.authoring.model,
                "narration": f"Kokoro-82M, voice {cfg.tts.voice}",
                "animation": f"Manim Community ({version('manim')})",
            },
        )
    except ValidationError as e:
        return None, [str(e)]
    return work, []


def write_site_work(wd: WorkDir, record: PaperRecord, notes: Notes, timeline: dict, cfg: Config) -> Work:
    pages = wd.pages()
    key = video_key(wd)
    site_dir = SITE_WORKS / wd.slug
    existing = site_dir / "work.yaml"
    youtube_url = load_model(existing, Work).video.youtube_url if existing.exists() else None

    draft = load_model(wd.site_draft, WorkDraft)
    work, errors = assemble_work(draft, record, notes, timeline, key, paper_links(pages), cfg, youtube_url)
    if work is not None:
        errors = verify_work(work, pages, metadata_text(record)).errors
    save_json(wd.checks / "site.json", {"ok": not errors, "errors": errors})
    if errors:
        raise ValueError("the page fails provenance checks:\n- " + "\n- ".join(errors))

    site_dir.mkdir(parents=True, exist_ok=True)
    existing.write_text(dump_yaml(work.model_dump(mode="json", exclude_none=False)))
    shutil.copy(wd.out / "thumbnail.jpg", site_dir / "thumbnail.jpg")
    shutil.copy(wd.out / "captions.vtt", site_dir / "captions.vtt")
    mirror = MEDIA_MIRROR / key
    mirror.parent.mkdir(parents=True, exist_ok=True)
    for old in mirror.parent.glob("video-*.mp4"):
        old.unlink()
    shutil.copy(wd.out / "video.mp4", mirror)
    log(f"page ok: {existing} ({len(work.claims)} claims cited)")
    return work
