"""Deterministic provenance checks: quotes must exist in the paper, numbers must come from quotes.

PDF text extraction mangles whitespace, hyphenation, ligatures and quote marks, so
matching happens on a canonical form: NFKC, lowercased, keeping only letters,
digits, '.' and '%'. Quotes are required to be long enough that this cannot
produce accidental matches.
"""

import re
import unicodedata
from dataclasses import dataclass, field

from aisr_site.schema import Claim, Work, claim_refs_in

from paper_video.models import Notes, Storyboard

_KEEP = re.compile(r"[^0-9a-z.%]")
_NUMBER = re.compile(r"(?<![\w.])(\d+(?:[.,]\d+)*)(\s?%)?")
_MD_LINK = re.compile(r"\]\([^)]*\)|https?://\S+")
MIN_QUOTE_CHARS = 25


def canon(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"-\s*\n\s*", "", text)  # re-join words hyphenated across lines
    return _KEEP.sub("", text)


def contains(haystack: str, needle: str) -> bool:
    return canon(needle) in canon(haystack)


def locate_quote(pages: list[str], quote: str, page: int) -> int | None:
    """1-based page containing the quote: the claimed page, else its neighbours, else anywhere."""
    q = canon(quote)
    if len(q) < MIN_QUOTE_CHARS:
        return None
    order = [page, page - 1, page + 1] + list(range(1, len(pages) + 1))
    for p in order:
        if 1 <= p <= len(pages) and q in canon(pages[p - 1]):
            return p
    # Quotes can straddle a page break.
    for p in range(1, len(pages)):
        if q in canon(pages[p - 1] + pages[p]):
            return p
    return None


def numbers_in(text: str) -> list[str]:
    """Numeric tokens in prose, ignoring URLs and claim citations."""
    text = _MD_LINK.sub(" ", text)
    text = re.sub(r"\[c\d{2,3}(?:\s*,\s*c\d{2,3})*\]", " ", text)
    return [m.group(1) + ("%" if m.group(2) else "") for m in _NUMBER.finditer(text)]


def number_supported(number: str, sources: list[str]) -> bool:
    """A number is supported if it appears as a whole token in one of the source texts."""
    bare = number.rstrip("%").replace(",", "")
    pattern = re.compile(rf"(?<![\d.]){re.escape(bare)}(?![\d]|\.\d)")
    for source in sources:
        flat = unicodedata.normalize("NFKC", source).replace(",", "")
        flat = re.sub(r"(\d)\s+%", r"\1%", flat)
        if pattern.search(flat):
            return True
    return False


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict:
        return {"ok": self.ok, "errors": self.errors, "notes": self.notes}


def verify_notes(notes: Notes, pages: list[str]) -> tuple[Notes, Report]:
    """Check every quote against the paper. Wrong page numbers are corrected; missing quotes are errors."""
    report = Report()
    ids = [c.id for c in notes.claims]
    if len(ids) != len(set(ids)):
        report.errors.append("duplicate claim ids")
    for claim in notes.claims:
        if not claim.evidence:
            report.errors.append(f"{claim.id}: no evidence")
        for ev in claim.evidence:
            found = locate_quote(pages, ev.quote, ev.page)
            if found is None:
                report.errors.append(f"{claim.id}: quote not found in paper (p.{ev.page}): {ev.quote!r}")
            elif found != ev.page:
                report.notes.append(f"{claim.id}: page corrected {ev.page} -> {found}")
                ev.page = found
    return notes, report


def claim_sources(notes_claims: dict, ids: list[str]) -> list[str]:
    return [ev.quote for cid in ids if cid in notes_claims for ev in notes_claims[cid].evidence]


def verify_storyboard(sb: Storyboard, notes: Notes, metadata_text: str) -> Report:
    """Claim references resolve, and every number shown or spoken is in a cited quote."""
    report = Report()
    claims = {c.id: c for c in notes.claims}
    seen: set[str] = set()
    for scene in sb.scenes:
        for beat in scene.beats:
            if beat.id in seen:
                report.errors.append(f"duplicate beat id {beat.id}")
            seen.add(beat.id)
            if not beat.id.startswith(scene.id):
                report.errors.append(f"beat {beat.id} is in scene {scene.id}")
            unknown = [c for c in beat.claims if c not in claims]
            if unknown:
                report.errors.append(f"{beat.id}: unknown claims {unknown}")
            sources = claim_sources(claims, beat.claims) + [metadata_text]
            for text in [beat.narration, *beat.on_screen_text]:
                for n in numbers_in(text):
                    if not number_supported(n, sources):
                        report.errors.append(f"{beat.id}: number {n} in {text!r} is not in any cited quote")
        if len(scene.chapter) > 40:
            report.errors.append(f"{scene.id}: chapter title longer than 40 characters")
    ds_ids = [d.id for d in sb.datasets]
    if len(ds_ids) != len(set(ds_ids)):
        report.errors.append("duplicate dataset ids")
    for ds in sb.datasets:
        unknown = [c for c in ds.claims if c not in claims]
        if unknown:
            report.errors.append(f"dataset {ds.id}: unknown claims {unknown}")
        sources = claim_sources(claims, ds.claims)
        for point in ds.points:
            shown = numbers_in(point.display)
            if len(shown) != 1:
                report.errors.append(f"dataset {ds.id}: display {point.display!r} must contain exactly one number")
                continue
            if not number_supported(shown[0], sources):
                report.errors.append(f"dataset {ds.id}: {point.display!r} is not in any cited quote")
            if abs(float(shown[0].rstrip("%").replace(",", "")) - point.value) > 1e-9:
                report.errors.append(f"dataset {ds.id}: value {point.value} does not match display {point.display!r}")
    return report


def verify_work(work: Work, pages: list[str], metadata_text: str) -> Report:
    """Page-level provenance: quotes exist, and numbers in each paragraph come from the claims it cites."""
    report = Report()
    claims: dict[str, Claim] = {c.id: c for c in work.claims}
    for claim in work.claims:
        for ev in claim.evidence:
            if locate_quote(pages, ev.quote, ev.page) != ev.page:
                report.errors.append(f"evidence {claim.id}: quote not found on page {ev.page}")
    for where, text in work.prose():
        for paragraph in re.split(r"\n\s*\n", text):
            cited = claim_refs_in(paragraph)
            # Uncited text (titles, the dek) may only use numbers that some claim supports.
            sources = claim_sources(claims, cited or list(claims)) + [metadata_text]
            for n in numbers_in(paragraph):
                if not number_supported(n, sources):
                    report.errors.append(f"{where}: number {n} is not in the quotes it cites: {paragraph[:120]!r}")
    uncited = [c.id for c in work.claims if c.id not in set(work.cited_claim_ids())]
    if uncited:
        report.errors.append(f"claims in the evidence register that the page never cites: {uncited}")
    return report
