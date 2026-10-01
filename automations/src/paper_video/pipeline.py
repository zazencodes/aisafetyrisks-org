"""The commands behind the CLI. Each runs one deterministic step of the workflow and fails loudly.

The writing (notes, storyboard, scene code, page, science reviews) happens in the agent
session that runs workflows/publish-paper/WORKFLOW.md; these commands brief it, check its work,
render, assemble and publish.
"""

import subprocess
from datetime import date
from pathlib import Path

from aisr_site.schema import Review, Work

from paper_video import backlog, log
from paper_video.analyze import check_notes
from paper_video.assemble import assemble_video
from paper_video.backup import backup_work
from paper_video.briefs import write_brief
from paper_video.config import MEDIA_MIRROR, REPO, SITE_WORKS, Config, load_config
from paper_video.context import metadata_text
from paper_video.ingest import ensure_source, ingest
from paper_video.models import Notes, PaperRecord, Storyboard
from paper_video.narrate import narrate
from paper_video.provenance import verify_work
from paper_video.review import SUBJECTS, current_review, record_review
from paper_video.scenes import SceneRenderer, build_thumbnail, render_context, render_scenes
from paper_video.shorts import build_short, check_short, plan_path
from paper_video.site_content import write_site_work
from paper_video.storyboard import check_storyboard
from paper_video.workdir import WorkDir, dump_yaml, load_json, load_model, save_json
from paper_video.youtube import youtube_package


def _open(slug: str) -> tuple[Config, WorkDir, PaperRecord]:
    cfg = load_config()
    wd = WorkDir.for_slug(slug)
    record = load_model(wd.paper, PaperRecord)
    ensure_source(wd, record)
    return cfg, wd, record


def _notes(wd: WorkDir) -> Notes:
    return load_model(wd.notes, Notes)


def _storyboard(wd: WorkDir) -> Storyboard:
    return load_model(wd.storyboard, Storyboard)


def ingest_paper(ref: str, source_url: str | None, slug: str | None) -> None:
    cfg = load_config()
    wd = ingest(ref, cfg.agy, source_url=source_url, slug=slug)
    record = load_model(wd.paper, PaperRecord)
    backlog.set_status(record.arxiv_id, str(record.url), wd.slug, "in_progress")
    log(f"ingested {record.title!r} -> {wd.root}")


def brief(slug: str, task: str, scene_id: str | None) -> None:
    cfg, wd, record = _open(slug)
    log(f"brief written: {write_brief(wd, record, cfg, task, scene_id)}")


def check(slug: str, artifact: str) -> None:
    _, wd, record = _open(slug)
    match artifact:
        case "notes":
            check_notes(wd)
        case "storyboard":
            check_storyboard(wd, record, _notes(wd), _storyboard(wd))
        case "short":
            result = check_short(wd, record, load_config())
            log(f"short checks pass: {result['duration']:.2f}s, independent science/visual review recorded")


def review(slug: str, subject: str) -> None:
    _, wd, _ = _open(slug)
    record_review(wd, subject)


def narrate_work(slug: str) -> None:
    cfg, wd, record = _open(slug)
    sb = _storyboard(wd)
    check_storyboard(wd, record, _notes(wd), sb)
    durations = narrate(wd, sb, cfg.tts)
    save_json(wd.render / "context.json", render_context(wd, record, sb, durations, cfg))
    log(f"narration ready: {sum(durations.values()) / 60:.1f} min over {len(durations)} beats")


def render_work(slug: str, scenes: list[str] | None) -> None:
    cfg, wd, record = _open(slug)
    render_scenes(wd, record, _storyboard(wd), cfg, scenes)


def assemble(slug: str) -> None:
    cfg, wd, record = _open(slug)
    sb = _storyboard(wd)
    renderer = SceneRenderer(wd, record, sb, cfg)
    stale = [s.id for s in sb.scenes if not renderer.is_current(s)]
    if stale:
        raise ValueError(f"renders missing or out of date for {stale}; run `paper-video render {slug}`")
    timeline = assemble_video(wd, sb)
    snapshot = backup_work(wd, cfg.backup, "full")
    log(f"verified backup: {snapshot}")
    log(f"video assembled: {wd.out / 'video.mp4'} ({timeline['duration']:.0f} s)")
    for p in timeline["problems"]:
        log(f"  problem: {p}")


def thumbnail(slug: str) -> None:
    cfg, wd, _ = _open(slug)
    build_thumbnail(wd, _storyboard(wd), cfg)


def short_work(slug: str) -> None:
    cfg, wd, record = _open(slug)
    result = build_short(wd, record, cfg)
    snapshot = backup_work(wd, cfg.backup, "short")
    log(f"verified backup: {snapshot}")
    log(f"short assembled: {wd.out / 'short' / 'video.mp4'} ({result['duration']:.2f}s)")
    log(f"social package: {wd.root / 'short-package.yaml'}; run `paper-video check {slug} short` after review")


def site(slug: str) -> None:
    cfg, wd, record = _open(slug)
    write_site_work(wd, record, _notes(wd), load_json(wd.out / "timeline.json"), cfg)


def youtube(slug: str) -> None:
    cfg, wd, record = _open(slug)
    work = load_model(SITE_WORKS / slug / "work.yaml", Work)
    youtube_package(wd, record, work, cfg.publish.site_url)


# ------------------------------------------------------------------ review


def _check(path: Path) -> dict | None:
    return load_json(path) if path.exists() else None


def report(slug: str) -> None:
    cfg, wd, record = _open(slug)
    lines = [f"# Review report: {wd.slug}", ""]
    lines += ["Human review is required before publication. Watch `out/video.mp4` in full, read the page",
              "(`uv run aisr-site serve --drafts --media-root automations/media`), and check each claim against",
              "the evidence register. Then run `paper-video approve " + wd.slug + "`.", ""]
    notes = _check(wd.checks / "notes.json")
    if notes:
        lines += ["## Source notes", f"- Quotes found in the PDF: {'yes' if notes['ok'] else 'NO'}. "
                  f"Page corrections: {len(notes['notes'])}.", ""]
    for subject, title, check_file in (("storyboard", "Storyboard", "storyboard.json"), ("site", "Web page", "site.json")):
        check_ = _check(wd.checks / check_file)
        if check_ is None:
            continue
        lines += [f"## {title}", f"- Provenance checks: {'pass' if check_['ok'] else 'FAIL'}."]
        lines += [f"  - {e}" for e in check_["errors"]]
        r = current_review(wd, subject)
        if r is None:
            lines.append("- Science review: **none of the current version**.")
        else:
            lines.append(f"- Science review: **{r.verdict}**.")
            lines += [f"  - [{i.severity}] {i.location}: {i.problem}" for i in r.issues]
        lines.append("")
    scene_ids = sorted(s.id for s in _storyboard(wd).scenes) if wd.storyboard.exists() else []
    scenes = [wd.checks / "scenes" / f"{scene_id}.json" for scene_id in scene_ids]
    scenes = [path for path in scenes if path.exists()]
    if scenes:
        lines.append("## Scenes")
        for path in scenes:
            c = load_json(path)
            vis = c["visual_review"]["issues"] if c["visual_review"] else []
            lines.append(f"- {c['scene']}: rendered={c['rendered']}, layout problems={len(c['layout_problems'])}, "
                         f"visual review={'pending' if c['visual_review'] is None else 'recorded'}, "
                         f"visual issues={len(vis)} (contact sheet `frames/{c['scene']}-sheet.png`)")
            lines += [f"  - [rejected] {p}" for p in c["problems"]]
            lines += [f"  - [{i['severity']}] {i['beat']}: {i['problem']}" for i in vis]
            lines += [f"  - [layout] {p}" for p in c["layout_problems"]]
        lines.append("")
    video = _check(wd.checks / "video.json")
    if video:
        lines += ["## Video", f"- Duration {video['duration']:.0f} s, {video['width']}x{video['height']}."]
        lines += [f"- {p}" for p in video["problems"]]
        lines.append("")
    lines += ["## Short-form companion"]
    if not plan_path(wd).exists():
        lines.append("- **Missing**: follow `workflows/short-paper/WORKFLOW.md` before handover or approval.")
    else:
        try:
            short = check_short(wd, record, cfg)
            lines.append(f"- Checks pass: {short['duration']:.2f}s, 1080x1920, current independent review.")
            lines += [f"  - [{i['severity']}] {i['location']}: {i['problem']}"
                      for i in load_json(wd.checks / "short.json")["review"]["science"]["issues"]]
            lines += [f"  - [{i['severity']}] {i['beat']}: {i['problem']}"
                      for i in load_json(wd.checks / "short.json")["review"]["visual_issues"]]
        except (ValueError, FileNotFoundError) as e:
            lines.append(f"- **Incomplete**: {e}")
        lines += ["- Video: `out/short/video.mp4`; social copy and links: `short-package.yaml`."]
    lines.append("")
    (wd.checks / "report.md").write_text("\n".join(lines) + "\n")
    log(f"report written: {wd.checks / 'report.md'}")


def approve(slug: str) -> None:
    """Human sign-off: re-check provenance and reviews, upload media, mark the work published."""
    cfg, wd, record = _open(slug)
    path = SITE_WORKS / slug / "work.yaml"
    work = load_model(path, Work)

    # Every explainer ships with one independently reviewed short companion.
    check_short(wd, record, cfg)

    # The page may have been edited by hand since it was built: verify it again now.
    check_ = verify_work(work, wd.pages(), metadata_text(record))
    if not check_.ok:
        raise RuntimeError("the page fails provenance checks:\n- " + "\n- ".join(check_.errors))
    for subject in SUBJECTS:
        r = current_review(wd, subject)
        if r is None:
            raise RuntimeError(f"no science review of the current {subject}; it changed since the last review")
        unresolved = [i.problem for i in r.issues if i.severity in ("blocker", "major")]
        if unresolved:
            raise RuntimeError(f"{subject} review has unresolved blocker or major issues: {unresolved}")

    video = MEDIA_MIRROR / work.video.key
    if not video.exists():
        raise FileNotFoundError(f"{video} is missing; re-run `paper-video site {slug}`")
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
    work.review = Review(reviewed_on=today)
    path.write_text(dump_yaml(work.model_dump(mode="json")))
    backlog.set_status(record.arxiv_id, str(record.url), slug, "published")
    log(f"{slug} approved and media uploaded. Deploy with: cd site && npm run deploy")
