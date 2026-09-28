"""The research backlog (automations/backlog/papers.yaml)."""

from datetime import date
from typing import Literal

import yaml
from aisr_site.schema import Category
from pydantic import BaseModel, ConfigDict, HttpUrl

from paper_video.config import BACKLOG
from paper_video.workdir import dump_yaml

Status = Literal["queued", "in_progress", "published"]


class Entry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    authors: list[str]
    published: date
    link: HttpUrl
    arxiv: str | None
    category: Category
    relevance: str
    status: Status
    work: str | None = None


def load() -> list[Entry]:
    entries = [Entry.model_validate(e) for e in yaml.safe_load(BACKLOG.read_text())["papers"]]
    for prev, cur in zip(entries, entries[1:]):
        if cur.published < prev.published:
            raise ValueError(f"{BACKLOG} is not in order of publication: {cur.title!r} comes after {prev.title!r}")
    return entries


def save(entries: list[Entry]) -> None:
    header = BACKLOG.read_text().split("papers:", 1)[0]
    BACKLOG.write_text(header + dump_yaml({"papers": [e.model_dump(mode="json") for e in entries]}))


def find(entries: list[Entry], arxiv_id: str | None, url: str) -> Entry | None:
    base = arxiv_id.split("v")[0] if arxiv_id else None
    for e in entries:
        if (base and e.arxiv == base) or str(e.link).rstrip("/") == url.rstrip("/"):
            return e
    return None


def set_status(arxiv_id: str | None, url: str, slug: str, status: Status) -> Entry | None:
    entries = load()
    entry = find(entries, arxiv_id, url)
    if entry is not None:
        entry.status, entry.work = status, slug
        save(entries)
    return entry
