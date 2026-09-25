"""paper-video: turn an AI safety paper into a source-grounded animated explainer.

  paper-video <paper>                       ingest and run the whole pipeline (PDF path, arXiv id or URL)
  paper-video run <slug> [--from STAGE]     re-run stages after editing artifacts
  paper-video approve <slug> --reviewer N   human sign-off: re-verify, upload media, mark published
  paper-video backlog [--status S]          list the research backlog
"""

import argparse
import sys

from paper_video import backlog, pipeline

COMMANDS = {"run", "approve", "backlog"}


def main() -> None:
    argv = sys.argv[1:]
    if argv and argv[0] not in COMMANDS and not argv[0].startswith("-"):
        argv = ["make", *argv]

    parser = argparse.ArgumentParser(prog="paper-video", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    make = sub.add_parser("make", help="ingest a paper and run the whole pipeline")
    make.add_argument("paper", help="PDF path, arXiv id, or URL (arXiv, PDF, or a page with citation metadata)")
    make.add_argument("--source-url", help="public page for the paper (required for local PDFs and bare PDF URLs)")
    make.add_argument("--slug", help="override the work's URL slug")

    run = sub.add_parser("run", help="run pipeline stages for an existing work")
    run.add_argument("slug")
    run.add_argument("--from", dest="start", choices=pipeline.STAGES, default=pipeline.STAGES[0])
    run.add_argument("--to", dest="stop", choices=pipeline.STAGES, default=pipeline.STAGES[-1])
    run.add_argument("--scene", action="append", help="limit the scenes stage to these scene ids")

    approve = sub.add_parser("approve", help="approve a reviewed draft for publication")
    approve.add_argument("slug")
    approve.add_argument("--reviewer", required=True, help="name recorded on the page as the reviewer")

    bl = sub.add_parser("backlog", help="list backlog papers")
    bl.add_argument("--status", choices=["queued", "in_progress", "published"])

    args = parser.parse_args(argv)
    match args.command:
        case "make":
            pipeline.publish(args.paper, args.source_url, args.slug)
        case "run":
            pipeline.run(args.slug, args.start, args.stop, args.scene)
        case "approve":
            pipeline.approve(args.slug, args.reviewer)
        case "backlog":
            for e in backlog.load():
                if args.status in (None, e.status):
                    print(f"{e.status:<12} {e.year}  {e.category.value:<24} {e.title}")
