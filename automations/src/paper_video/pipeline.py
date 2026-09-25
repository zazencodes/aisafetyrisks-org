"""Orchestration: run stages, write the review report, approve and publish."""

import subprocess
from datetime import date

from aisr_site.schema import Review, Work

from paper_video import backlog
from paper_video.analyze import analyze
from paper_video.assemble import assemble_video
from paper_video.config import MEDIA_MIRROR, REPO, SITE_WORKS, Config, load_config
from paper_video.context import metadata_text
from paper_video.ingest import ensure_source, ingest
from paper_video.llm import make_provider
from paper_video.models import Notes, PaperRecord, Storyboard
from paper_video.narrate import narrate
from paper_video.provenance import verify_work
from paper_video.scenes import build_scenes, build_thumbnail
from paper_video.site_content import write_site_work
from paper_video.storyboard import check_storyboard, make_storyboard
from paper_video.workdir import WorkDir, dump_yaml, load_json, load_model
from paper_video.youtube import youtube_package

STAGES = ["analyze", "storyboard", "narrate", "scenes", "assemble", "thumbnail", "site", "youtube"]


def log(msg: str) -> None:
    print(f"[paper-video] {msg}", flush=True)


def run(slug: str, start: str = "analyze", stop: str = "youtube", scenes: list[str] | None = None) -> None:
    cfg = load_config()
    provider = make_provider(cfg.llm)
    wd = WorkDir.for_slug(slug)
    record = load_model(wd.paper, PaperRecord)
    ensure_source(wd, record)
    todo = STAGES[STAGES.index(start): STAGES.index(stop) + 1]

    notes = load_model(wd.notes, Notes) if wd.notes.exists() else None
    sb = load_model(wd.storyboard, Storyboard) if wd.storyboard.exists() else None
    for stage in todo:
        log(f"{slug}: {stage}")
        match stage:
            case "analyze":
                notes = analyze(wd, record, provider)
            case "storyboard":
                sb = make_storyboard(wd, record, notes, provider, cfg)
            case "narrate":
                check_storyboard(wd, record, notes, sb)
                narrate(wd, sb, cfg.tts)
            case "scenes":
                check_storyboard(wd, record, notes, sb)
                build_scenes(wd, record, notes, sb, narrate(wd, sb, cfg.tts), provider, cfg, only=scenes)
            case "assemble":
                assemble_video(wd, sb)
            case "thumbnail":
                build_thumbnail(wd, record, sb, provider, cfg)
            case "site":
                entry = backlog.find(backlog.load(), record.arxiv_id, str(record.url))
                write_site_work(wd, record, notes, sb, load_json(wd.out / "timeline.json"), provider, cfg,
                                entry.category.value if entry else None)
            case "youtube":
                work = load_model(SITE_WORKS / slug / "work.yaml", Work)
                youtube_package(wd, record, notes, work, cfg.publish.site_url, provider)
    write_report(wd, cfg)
    log(f"{slug}: done. Review {wd.checks / 'report.md'}")


def publish(ref: str, source_url: str | None, slug: str | None) -> str:
    cfg = load_config()
    wd = ingest(ref, make_provider(cfg.llm), source_url=source_url, slug=slug)
    record = load_model(wd.paper, PaperRecord)
    log(f"ingested {record.title!r} -> {wd.root}")
    backlog.set_status(record.arxiv_id, str(record.url), wd.slug, "in_progress")
    run(wd.slug)
    return wd.slug


# ------------------------------------------------------------------ review


def _review_state(wd: WorkDir) -> dict:
    state = {}
    for name in ("notes", "storyboard", "site", "video"):
        path = wd.checks / f"{name}.json"
        state[name] = load_json(path) if path.exists() else None
    scenes_dir = wd.checks / "scenes"
    state["scenes"] = {p.stem: load_json(p) for p in sorted(scenes_dir.glob("*.json"))} if scenes_dir.exists() else {}
    return state


def _last_review(check: dict | None) -> dict | None:
    rounds = [r for r in (check or {}).get("rounds", []) if "review" in r]
    return rounds[-1]["review"] if rounds else None


def write_report(wd: WorkDir, cfg: Config) -> None:
    s = _review_state(wd)
    lines = [f"# Review report: {wd.slug}", ""]
    lines += ["Human review is required before publication. Watch `out/video.mp4` in full, read the page",
              "(`uv run aisr-site serve --drafts --media-root automations/media`), and check each claim against",
              "the evidence register. Then run `paper-video approve " + wd.slug + " --reviewer \"Your Name\"`.", ""]
    if s["notes"]:
        lines += ["## Source notes", f"- Quotes verified against the PDF. Page corrections: {len(s['notes']['notes'])}.",
                  f"- Evidence dropped as unverifiable: {len(s['notes']['dropped_evidence'])}."]
        lines += [f"  - {d['claim']}: {d['quote'][:100]!r}" for d in s["notes"]["dropped_evidence"]]
        lines.append("")
    for name, title in (("storyboard", "Storyboard"), ("site", "Web page")):
        review = _last_review(s[name])
        if s[name] is None:
            continue
        lines.append(f"## {title} science review")
        if review is None:
            lines.append("- No review recorded (provenance checks did not pass).")
        else:
            lines.append(f"- Verdict: **{review['verdict']}** after {len(s[name]['rounds'])} round(s).")
            lines += [f"- [{i['severity']}] {i['location']}: {i['problem']}" for i in review["issues"]]
        lines.append("")
    if s["scenes"]:
        lines.append("## Scenes")
        for scene_id, c in s["scenes"].items():
            vis = c["visual_reviews"][-1]["issues"] if c["visual_reviews"] else []
            lines.append(f"- {scene_id}: rendered={c['rendered']}, render attempts={len(c['render_attempts'])}, "
                         f"layout problems={len(c['layout_problems'] or [])}, visual issues={len(vis)} "
                         f"(contact sheet `frames/{scene_id}-sheet.png`)")
            lines += [f"  - [{i['severity']}] {i['beat']}: {i['problem']}" for i in vis]
            lines += [f"  - [layout] {p}" for p in c["layout_problems"] or []]
        lines.append("")
    if s["video"]:
        lines += ["## Video", f"- Duration {s['video']['duration']:.0f} s, {s['video']['width']}x{s['video']['height']}."]
        lines += [f"- {p}" for p in s["video"]["problems"]]
        lines.append("")
    (wd.checks / "report.md").write_text("\n".join(lines) + "\n")


def approve(slug: str, reviewer: str) -> None:
    """Human sign-off: re-check provenance, upload media, mark the work published."""
    cfg = load_config()
    wd = WorkDir.for_slug(slug)
    record = load_model(wd.paper, PaperRecord)
    ensure_source(wd, record)
    path = SITE_WORKS / slug / "work.yaml"
    work = load_model(path, Work)

    # The page may have been edited by hand since generation: verify it again now.
    check = verify_work(work, wd.pages(), metadata_text(record))
    if not check.ok:
        raise RuntimeError("the page fails provenance checks:\n- " + "\n- ".join(check.errors))
    state = _review_state(wd)
    for name in ("storyboard", "site"):
        review = _last_review(state[name])
        if review is None:
            raise RuntimeError(f"no {name} science review on record")
        blockers = [i for i in review["issues"] if i["severity"] == "blocker"]
        if blockers:
            raise RuntimeError(f"{name} review has unresolved blockers: {[i['problem'] for i in blockers]}")

    video = MEDIA_MIRROR / work.video.key
    if not video.exists():
        raise FileNotFoundError(f"{video} is missing; re-run the site stage")
    subprocess.run(
        ["npx", "wrangler", "r2", "object", "put", f"{cfg.publish.media_bucket}/{work.video.key}",
         "--file", str(video), "--content-type", "video/mp4",
         "--cache-control", "public, max-age=31536000, immutable", "--remote"],
        cwd=REPO / "site", check=True,
    )

    today = date.today()
    work.status = "published"
    if work.published_on is None:
        work.published_on = today
    else:
        work.updated_on = today
    work.review = Review(reviewed_by=reviewer, reviewed_on=today)
    path.write_text(dump_yaml(work.model_dump(mode="json")))
    backlog.set_status(record.arxiv_id, str(record.url), slug, "published")
    log(f"{slug} approved and media uploaded. Deploy with: cd site && npm run deploy")
