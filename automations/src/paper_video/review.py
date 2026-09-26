"""Science reviews of the storyboard and the web page, by an independent reviewer.

A reviewer subagent writes checks/reviews/<subject>.yaml from `paper-video brief <slug> review-<subject>`.
`paper-video review <slug> <subject>` validates it and records it in checks/reviews.json against a
hash of the exact content reviewed, so any edit after a review needs a new review before approval.
"""

import hashlib
from datetime import date
from pathlib import Path

from aisr_site.schema import Work

from paper_video import log
from paper_video.config import SITE_WORKS
from paper_video.context import as_yaml
from paper_video.models import ScienceReview, Storyboard
from paper_video.workdir import WorkDir, dump_yaml, load_json, load_model, save_json

SUBJECTS = ("storyboard", "site")
# The written parts of a page; the claims register, video and production details are checked elsewhere.
REVIEWED_FIELDS = {"title", "dek", "category", "summary", "explanation", "findings", "limitations", "context",
                   "references"}


def reviewed_content(wd: WorkDir, subject: str) -> str:
    if subject == "storyboard":
        return as_yaml(load_model(wd.storyboard, Storyboard))
    work = load_model(SITE_WORKS / wd.slug / "work.yaml", Work)
    return dump_yaml(work.model_dump(mode="json", include=REVIEWED_FIELDS))


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def review_file(wd: WorkDir, subject: str) -> Path:
    return wd.checks / "reviews" / f"{subject}.yaml"


def blocking(review: ScienceReview) -> list:
    return [i for i in review.issues if i.severity in ("blocker", "major")]


def _history(wd: WorkDir) -> dict:
    path = wd.checks / "reviews.json"
    return load_json(path) if path.exists() else {s: [] for s in SUBJECTS}


def record_review(wd: WorkDir, subject: str) -> ScienceReview:
    review = load_model(review_file(wd, subject), ScienceReview)
    if review.verdict == "accurate" and blocking(review):
        raise ValueError("verdict is 'accurate' but the review lists blocker or major issues")
    history = _history(wd)
    history[subject].append({
        "content": _hash(reviewed_content(wd, subject)),
        "recorded_on": date.today().isoformat(),
        "review": review.model_dump(mode="json"),
    })
    save_json(wd.checks / "reviews.json", history)
    counts = {s: sum(i.severity == s for i in review.issues) for s in ("blocker", "major", "minor")}
    log(f"{subject} review {len(history[subject])} recorded: {review.verdict} {counts}")
    for i in review.issues:
        log(f"  [{i.severity}/{i.category}] {i.location}: {i.problem}\n    fix: {i.suggested_fix}")
    return review


def current_review(wd: WorkDir, subject: str) -> ScienceReview | None:
    """The latest recorded review of `subject`, if it reviewed the content as it is now."""
    entries = _history(wd)[subject]
    if not entries or entries[-1]["content"] != _hash(reviewed_content(wd, subject)):
        return None
    return ScienceReview.model_validate(entries[-1]["review"])
