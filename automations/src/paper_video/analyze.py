"""Stage: check the reading notes (notes.yaml) against the paper.

The notes are written in the session running the workflow, from `paper-video brief <slug> analyze`.
Every quote must appear in the PDF text; wrong page numbers are corrected in place.
"""

from paper_video import log
from paper_video.models import Notes
from paper_video.provenance import verify_notes
from paper_video.workdir import WorkDir, load_model, save_json, save_model


def check_notes(wd: WorkDir) -> Notes:
    notes, report = verify_notes(load_model(wd.notes, Notes), wd.pages())
    save_json(wd.checks / "notes.json", report.as_dict())
    for note in report.notes:
        log(f"  {note}")
    if not report.ok:
        raise ValueError("notes fail provenance checks:\n- " + "\n- ".join(report.errors))
    save_model(wd.notes, notes)
    log(f"notes ok: {len(notes.claims)} claims, all quotes found in the paper")
    return notes
