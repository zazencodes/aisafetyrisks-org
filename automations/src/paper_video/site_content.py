"""Stage: notes + storyboard -> a draft Work on the website, checked and reviewed."""

import hashlib
import re
import shutil

from aisr_site.schema import Chapter, Claim, Paper, Reference, Video, Work, claim_refs_in
from pydantic import ValidationError

from paper_video import __version__
from paper_video.config import MEDIA_MIRROR, SITE_WORKS, Config
from paper_video.context import as_yaml, metadata_text, paper_header, system
from paper_video.llm import Provider, generate
from paper_video.models import Notes, PaperRecord, Storyboard, WorkDraft
from paper_video.provenance import verify_work
from paper_video.review import blocking, issues_text, science_review
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
                  links: list[str], provider: Provider, cfg: Config, youtube_url) -> tuple[Work | None, list[str]]:
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
                "language_model": provider.name,
                "narration": f"Kokoro-82M, voice {cfg.tts.voice}",
                "animation": f"Manim Community ({cfg.render.image.rsplit(':', 1)[1]})",
            },
        )
    except ValidationError as e:
        return None, [str(e)]
    return work, []


def write_site_work(wd: WorkDir, record: PaperRecord, notes: Notes, sb: Storyboard, timeline: dict,
                    provider: Provider, cfg: Config, category_hint: str | None) -> Work:
    pages = wd.pages()
    links = paper_links(pages)
    key = video_key(wd)
    site_dir = SITE_WORKS / wd.slug
    existing = site_dir / "work.yaml"
    youtube_url = None
    if existing.exists():
        youtube_url = load_model(existing, Work).video.youtube_url

    narration = "\n".join(f"[{s.id} {s.title}] " + " ".join(b.narration for b in s.beats) for s in sb.scenes)
    base = (
        f"{paper_header(record)}\n\n# Reading notes\n\n{as_yaml(notes)}\n\n"
        f"# Narration of the video this page accompanies\n\n{narration}\n\n"
        "# URLs printed in the paper\n\n" + ("\n".join(f"- {u}" for u in links) or "(none)")
        + (f"\n\n# Category\n\nUse the category `{category_hint}`." if category_hint else "")
    )
    draft = generate(provider, system("site"), base, WorkDraft)
    meta = metadata_text(record)

    history = []
    work = None
    for round_ in range(cfg.review.max_revision_rounds + 1):
        work, errors = assemble_work(draft, record, notes, timeline, key, links, provider, cfg, youtube_url)
        if work is not None:
            errors = verify_work(work, pages, meta).errors
        if errors:
            history.append({"round": round_, "provenance": errors})
            if round_ == cfg.review.max_revision_rounds:
                break
            problems = "Automated check failures:\n- " + "\n- ".join(errors)
        else:
            review = science_review(provider, record, pages, notes, "web page",
                                    dump_yaml(work.model_dump(mode="json", exclude={"claims", "video", "production"})))
            history.append({"round": round_, "provenance": [], "review": review.model_dump(mode="json")})
            if not blocking(review) or round_ == cfg.review.max_revision_rounds:
                break
            problems = issues_text(review)
        prompt = f"{base}\n\n# Current page\n\n{as_yaml(draft)}\n\n# Problems to fix\n\n{problems}"
        draft = generate(provider, system("revise_site") + "\n\n" + system("site"), prompt, WorkDraft)

    save_json(wd.checks / "site.json", {"rounds": history})
    if work is None or history[-1]["provenance"]:
        raise RuntimeError("the page still fails provenance checks; see checks/site.json")

    site_dir.mkdir(parents=True, exist_ok=True)
    existing.write_text(dump_yaml(work.model_dump(mode="json", exclude_none=False)))
    shutil.copy(wd.out / "thumbnail.jpg", site_dir / "thumbnail.jpg")
    shutil.copy(wd.out / "captions.vtt", site_dir / "captions.vtt")
    mirror = MEDIA_MIRROR / key
    mirror.parent.mkdir(parents=True, exist_ok=True)
    for old in mirror.parent.glob("video-*.mp4"):
        old.unlink()
    shutil.copy(wd.out / "video.mp4", mirror)
    return work
