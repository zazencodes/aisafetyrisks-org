"""Shared helpers for building model prompts from work-directory artifacts."""

from functools import cache
from pathlib import Path

from pydantic import BaseModel

from paper_video.models import PaperRecord
from paper_video.workdir import dump_yaml

PROMPTS = Path(__file__).parent / "prompts"


@cache
def prompt(name: str) -> str:
    return (PROMPTS / f"{name}.md").read_text()


def system(name: str, integrity: bool = True) -> str:
    return prompt(name) + ("\n\n" + prompt("integrity") if integrity else "")


def paper_text(pages: list[str]) -> str:
    return "\n\n".join(f"=== Page {i} ===\n{text}" for i, text in enumerate(pages, start=1))


def as_yaml(model: BaseModel) -> str:
    return dump_yaml(model.model_dump(mode="json"))


def short_citation(record: PaperRecord) -> str:
    first = record.authors[0].split()[-1]
    if len(record.authors) == 1:
        who = first
    elif len(record.authors) == 2:
        who = f"{first} and {record.authors[1].split()[-1]}"
    else:
        who = f"{first} et al."
    return f"{who} ({record.published.year})"


def metadata_text(record: PaperRecord) -> str:
    """Bibliographic text numbers may legitimately come from (e.g. the publication year)."""
    return f"{record.title} {short_citation(record)} {record.venue or ''} {record.published.isoformat()}"


def paper_header(record: PaperRecord) -> str:
    return (
        f"Title: {record.title}\nAuthors: {', '.join(record.authors)}\n"
        f"Published: {record.published.isoformat()}" + (f" ({record.venue})" if record.venue else "")
        + f"\nCite on screen as: {short_citation(record)}"
    )
