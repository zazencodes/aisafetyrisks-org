"""Stage: notes -> storyboard (scenes, beats, narration, datasets), checked and reviewed."""

from paper_video.config import Config
from paper_video.context import as_yaml, metadata_text, paper_header, system
from paper_video.llm import Provider, generate
from paper_video.models import Notes, PaperRecord, Storyboard
from paper_video.provenance import verify_storyboard
from paper_video.review import blocking, issues_text, science_review
from paper_video.workdir import WorkDir, save_json, save_model


def _revise(provider: Provider, base: str, sb: Storyboard, problems: str) -> Storyboard:
    prompt = f"{base}\n\n# Current storyboard\n\n{as_yaml(sb)}\n\n# Problems to fix\n\n{problems}"
    return generate(provider, system("revise_storyboard") + "\n\n" + system("storyboard"), prompt, Storyboard)


def make_storyboard(wd: WorkDir, record: PaperRecord, notes: Notes, provider: Provider, cfg: Config) -> Storyboard:
    base = f"{paper_header(record)}\n\n# Reading notes\n\n{as_yaml(notes)}"
    meta = metadata_text(record)
    sb = generate(provider, system("storyboard"), base, Storyboard)

    history = []
    for round_ in range(cfg.review.max_revision_rounds + 1):
        check = verify_storyboard(sb, notes, meta)
        if not check.ok:
            history.append({"round": round_, "provenance": check.as_dict()})
            if round_ == cfg.review.max_revision_rounds:
                break
            sb = _revise(provider, base, sb, "Provenance check failures:\n- " + "\n- ".join(check.errors))
            continue
        review = science_review(provider, record, wd.pages(), notes, "storyboard", as_yaml(sb))
        history.append({"round": round_, "provenance": check.as_dict(), "review": review.model_dump(mode="json")})
        if not blocking(review) or round_ == cfg.review.max_revision_rounds:
            break
        sb = _revise(provider, base, sb, issues_text(review))

    save_model(wd.storyboard, sb)
    save_json(wd.checks / "storyboard.json", {"rounds": history})
    return sb


def check_storyboard(wd: WorkDir, record: PaperRecord, notes: Notes, sb: Storyboard) -> None:
    """Fail loudly if a (possibly hand-edited) storyboard breaks provenance."""
    check = verify_storyboard(sb, notes, metadata_text(record))
    if not check.ok:
        raise ValueError("storyboard fails provenance checks:\n- " + "\n- ".join(check.errors))
