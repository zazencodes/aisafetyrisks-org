"""paper-video: the deterministic steps of turning an AI safety paper into a source-grounded explainer.

The writing is done by the agent session running workflows/publish-paper/WORKFLOW.md,
which calls these commands in order:

  paper-video ingest <paper>                    fetch a paper (PDF path, arXiv id or URL) into a work directory
  paper-video brief <slug> <task> [--scene ID]  write the brief for a writing task to briefs/
  paper-video check <slug> notes|storyboard|short  provenance, source freshness and short review checks
  paper-video review <slug> storyboard|site     record a science review from checks/reviews/
  paper-video narrate <slug>                    synthesize narration and the render context
  paper-video render <slug> [--scene ID ...]    render scenes and record visual-reviews/<scene>.yaml
  paper-video assemble <slug>                   master video, captions and chapter timeline
  paper-video short <slug>                      portrait short from short.yaml, captions and social package
  paper-video thumbnail <slug>                  render the thumbnail scene
  paper-video site <slug>                       build the page from site.yaml into site/content/works/
  paper-video youtube <slug>                    package youtube-copy.yaml as youtube.yaml
  paper-video report <slug>                     write checks/report.md with validation and publication status
  paper-video approve <slug>                    authorized publication: re-verify, upload media, mark published
  paper-video backlog [--status S]              list the research backlog
  paper-video backup-pending                    retry deferred media backups
  paper-video schedule                          schedule the next published explainer's week on Zernio
  paper-video schedule-status                   read every scheduled post's status back from Zernio
"""

import argparse
from datetime import datetime

from paper_video import backlog, pipeline, social
from paper_video.briefs import TASKS
from paper_video.config import load_config
from paper_video.review import SUBJECTS


def main() -> None:
    parser = argparse.ArgumentParser(prog="paper-video", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="fetch a paper into a new work directory")
    ingest.add_argument("paper", help="PDF path, arXiv id, or URL (arXiv, PDF, or a page with citation metadata)")
    ingest.add_argument("--source-url", help="public page for the paper (required for local PDFs and bare PDF URLs)")
    ingest.add_argument("--slug", help="override the work's URL slug")

    brief = sub.add_parser("brief", help="write the brief for a writing task")
    brief.add_argument("slug")
    brief.add_argument("task", choices=TASKS)
    brief.add_argument("--scene", help="scene id, for the scene task")

    check = sub.add_parser("check", help="provenance checks for notes, storyboard or short")
    check.add_argument("slug")
    check.add_argument("artifact", choices=["notes", "storyboard", "short"])

    review = sub.add_parser("review", help="record a science review")
    review.add_argument("slug")
    review.add_argument("subject", choices=SUBJECTS)

    for name, text in (("narrate", "synthesize narration"), ("assemble", "assemble the master video"),
                       ("thumbnail", "render the thumbnail"), ("site", "build the page from site.yaml"),
                       ("youtube", "write the YouTube package"), ("short", "build the portrait short"),
                       ("report", "write checks/report.md")):
        sub.add_parser(name, help=text).add_argument("slug")

    render = sub.add_parser("render", help="render scenes and record agent-written visual reviews")
    render.add_argument("slug")
    render.add_argument("--scene", action="append", help="limit to these scene ids")

    approve = sub.add_parser("approve", help="approve a reviewed draft for publication")
    approve.add_argument("slug")

    bl = sub.add_parser("backlog", help="list backlog papers")
    bl.add_argument("--status", choices=["queued", "in_progress", "published"])
    sub.add_parser("backup-pending", help="retry deferred media backups without rebuilding exports")
    sub.add_parser("schedule", help="upload and schedule the next explainer's long-form video and short")
    sub.add_parser("schedule-status", help="refresh social.yaml records from Zernio")

    args = parser.parse_args()
    match args.command:
        case "ingest":
            pipeline.ingest_paper(args.paper, args.source_url, args.slug)
        case "brief":
            pipeline.brief(args.slug, args.task, args.scene)
        case "check":
            pipeline.check(args.slug, args.artifact)
        case "review":
            pipeline.review(args.slug, args.subject)
        case "narrate":
            pipeline.narrate_work(args.slug)
        case "render":
            pipeline.render_work(args.slug, args.scene)
        case "assemble":
            pipeline.assemble(args.slug)
        case "short":
            pipeline.short_work(args.slug)
        case "thumbnail":
            pipeline.thumbnail(args.slug)
        case "site":
            pipeline.site(args.slug)
        case "youtube":
            pipeline.youtube(args.slug)
        case "report":
            pipeline.report(args.slug)
        case "approve":
            pipeline.approve(args.slug)
        case "backup-pending":
            pipeline.backup_pending()
        case "schedule":
            social.schedule_next(load_config(), datetime.now().astimezone())
        case "schedule-status":
            failures = social.refresh(load_config().social)
            if failures:
                raise SystemExit("failed posts:\n- " + "\n- ".join(failures))
        case "backlog":
            for e in backlog.load():
                if args.status in (None, e.status):
                    print(f"{e.status:<12} {e.published}  {e.category.value:<24} {e.title}")
