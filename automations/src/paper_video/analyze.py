"""Stage: paper text -> source-grounded notes, with every quote verified against the PDF."""

from paper_video.context import paper_header, paper_text, system
from paper_video.llm import Provider, generate
from paper_video.models import Notes, PaperRecord
from paper_video.provenance import locate_quote, verify_notes
from paper_video.workdir import WorkDir, save_json, save_model


def analyze(wd: WorkDir, record: PaperRecord, provider: Provider) -> Notes:
    pages = wd.pages()
    base = f"{paper_header(record)}\n\nFull text:\n\n{paper_text(pages)}"
    notes = generate(provider, system("analyze"), base, Notes)
    notes, report = verify_notes(notes, pages)

    if report.errors:
        # One repair pass: show the model exactly which quotes are not in the paper.
        repair = (
            f"{base}\n\n---\nYou produced these notes:\n\n{notes.model_dump_json(indent=1)}\n\n"
            "These quotes do not appear verbatim in the paper text:\n- " + "\n- ".join(report.errors)
            + "\n\nReturn the complete notes again with each of those quotes replaced by an exact, "
            "contiguous quote from the text, or remove the evidence (and the claim, if nothing supports it)."
        )
        notes = generate(provider, system("analyze"), repair, Notes)
        notes, report = verify_notes(notes, pages)

    # Anything still unverifiable is removed rather than published: first the quote,
    # then the claim if no quote is left to support it.
    dropped = []
    for claim in notes.claims:
        kept = [ev for ev in claim.evidence if locate_quote(pages, ev.quote, ev.page) == ev.page]
        dropped += [{"claim": claim.id, "quote": ev.quote} for ev in claim.evidence if ev not in kept]
        claim.evidence = kept
    notes.claims = [c for c in notes.claims if c.evidence]

    save_model(wd.notes, notes)
    save_json(wd.checks / "notes.json", {**report.as_dict(), "ok": True, "dropped_evidence": dropped})
    return notes
