"""Stage: check the storyboard (storyboard.yaml) against the notes.

The storyboard is written in the session running the workflow, from `paper-video brief <slug> storyboard`.
"""

from paper_video import log
from paper_video.context import metadata_text
from paper_video.models import Notes, PaperRecord, Storyboard
from paper_video.provenance import verify_storyboard
from paper_video.workdir import WorkDir, save_json


def check_storyboard(wd: WorkDir, record: PaperRecord, notes: Notes, sb: Storyboard) -> None:
    """Fail loudly if the storyboard breaks provenance: unknown claims, or numbers not in cited quotes."""
    check = verify_storyboard(sb, notes, metadata_text(record))
    save_json(wd.checks / "storyboard.json", check.as_dict())
    if not check.ok:
        raise ValueError("storyboard fails provenance checks:\n- " + "\n- ".join(check.errors))
    words = sum(len(b.narration.split()) for b in sb.beats())
    log(f"storyboard ok: {len(sb.scenes)} scenes, {len(sb.beats())} beats, {words} narration words")
