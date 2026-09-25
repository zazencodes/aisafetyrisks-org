"""Resolve a paper reference, fetch the PDF, extract page text and normalized metadata."""

import hashlib
import re
import shutil
import unicodedata
import xml.etree.ElementTree as ET
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
import pymupdf

from paper_video.config import WORKS
from paper_video.llm import Provider, generate
from paper_video.models import ExtractedMetadata, PaperRecord, SourceFile
from paper_video.provenance import contains
from paper_video.workdir import WorkDir, save_json, save_model

ARXIV_ID = re.compile(r"^(?:arxiv:)?(\d{4}\.\d{4,5}(?:v\d+)?|[a-z-]+(?:\.[A-Z]{2})?/\d{7}(?:v\d+)?)$", re.I)
ARXIV_URL = re.compile(r"arxiv\.org/(?:abs|pdf|html)/(.+?)(?:\.pdf)?/?$")
HEADERS = {"User-Agent": "paper-video/0.1 (+https://aisafetyrisks.org)"}
ATOM = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def http() -> httpx.Client:
    return httpx.Client(headers=HEADERS, follow_redirects=True, timeout=60)


def slugify(title: str, limit: int = 64) -> str:
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    words = re.findall(r"[a-z0-9]+", ascii_title)
    slug = ""
    for word in words:
        candidate = f"{slug}-{word}" if slug else word
        if len(candidate) > limit:
            break
        slug = candidate
    return slug


def extract_pages(pdf: Path) -> list[str]:
    with pymupdf.open(pdf) as doc:
        return [page.get_text("text") for page in doc]


# ------------------------------------------------------------------ arXiv


def arxiv_metadata(arxiv_id: str) -> dict:
    with http() as client:
        r = client.get("https://export.arxiv.org/api/query", params={"id_list": arxiv_id})
    r.raise_for_status()
    entry = ET.fromstring(r.text).find("a:entry", ATOM)
    if entry is None or entry.find("a:title", ATOM) is None:
        raise ValueError(f"arXiv has no entry for {arxiv_id}")

    def text(tag: str) -> str | None:
        node = entry.find(tag, ATOM)
        return " ".join(node.text.split()) if node is not None and node.text else None

    versioned = text("a:id").rsplit("/abs/", 1)[1]
    return {
        "arxiv_id": versioned,
        "title": text("a:title"),
        "authors": [" ".join(a.text.split()) for a in entry.findall("a:author/a:name", ATOM)],
        "published": date.fromisoformat(text("a:published")[:10]),
        "abstract": text("a:summary"),
        "doi": text("arxiv:doi"),
        "venue": text("arxiv:journal_ref"),
        "url": f"https://arxiv.org/abs/{versioned}",
        "pdf_url": f"https://arxiv.org/pdf/{versioned}",
    }


# ------------------------------------------------------- landing pages


class CitationMeta(HTMLParser):
    """Collects Highwire `citation_*` meta tags (used by arXiv, OpenReview, PMLR, ACL, NeurIPS...)."""

    def __init__(self):
        super().__init__()
        self.meta: dict[str, list[str]] = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and (a.get("name") or "").startswith("citation_") and a.get("content"):
            self.meta.setdefault(a["name"], []).append(a["content"].strip())


def parse_date(value: str) -> date:
    parts = [int(p) for p in re.split(r"[/-]", value)]
    return date(parts[0], parts[1] if len(parts) > 1 else 1, parts[2] if len(parts) > 2 else 1)


def landing_page_metadata(url: str, html: str) -> dict:
    parser = CitationMeta()
    parser.feed(html)
    m = parser.meta
    if "citation_title" not in m or "citation_pdf_url" not in m:
        raise ValueError(
            f"{url} has no citation_title/citation_pdf_url metadata. Download the PDF and run "
            "`paper-video ingest ./paper.pdf --source-url <landing page>` instead."
        )
    published = next((m[k][0] for k in ("citation_publication_date", "citation_date", "citation_online_date") if k in m), None)
    if published is None:
        raise ValueError(f"{url} does not state a publication date in its citation metadata")
    return {
        "title": m["citation_title"][0],
        "authors": m.get("citation_author", []),
        "published": parse_date(published),
        "venue": next((m[k][0] for k in ("citation_conference_title", "citation_journal_title") if k in m), None),
        "doi": m.get("citation_doi", [None])[0],
        "url": url,
        "pdf_url": urljoin(url, m["citation_pdf_url"][0]),
        "arxiv_id": None,
        "abstract": m.get("citation_abstract", [""])[0],
    }


# ------------------------------------------------------------ main entry


def resolve(ref: str, source_url: str | None) -> tuple[dict | None, Path | str]:
    """Return (metadata or None, local PDF path or PDF URL) for a user-supplied reference."""
    path = Path(ref).expanduser()
    if path.is_file():
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"{path} is not a PDF")
        if not source_url:
            raise ValueError("a local PDF needs --source-url: the public page readers should be linked to")
        return None, path
    if m := ARXIV_ID.match(ref.strip()):
        meta = arxiv_metadata(m.group(1))
        return meta, meta["pdf_url"]
    if not ref.startswith(("http://", "https://")):
        raise ValueError(f"{ref!r} is not a PDF path, arXiv id or URL")
    if m := ARXIV_URL.search(ref):
        meta = arxiv_metadata(m.group(1))
        return meta, meta["pdf_url"]
    with http() as client:
        r = client.get(ref)
    r.raise_for_status()
    if "pdf" in r.headers.get("content-type", ""):
        if not source_url:
            raise ValueError("a bare PDF URL needs --source-url: the landing page readers should be linked to")
        return None, ref
    meta = landing_page_metadata(str(r.url), r.text)
    return meta, meta["pdf_url"]


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with http() as client:
        r = client.get(url)
    r.raise_for_status()
    if not r.content.startswith(b"%PDF"):
        raise ValueError(f"{url} did not return a PDF")
    dest.write_bytes(r.content)


def metadata_from_pdf(provider: Provider, pages: list[str], source_url: str, pdf_url: str) -> dict:
    """For PDFs without machine-readable metadata: read it off the first pages and verify it."""
    front = "\n\n".join(f"=== Page {i + 1} ===\n{t}" for i, t in enumerate(pages[:2]))
    meta = generate(
        provider,
        "You extract bibliographic metadata from the first pages of a research paper. Copy names and titles exactly as printed.",
        f"Extract the metadata of this paper.\n\n{front}",
        ExtractedMetadata,
    )
    text = "\n".join(pages[:2])
    for label, value in (("title", meta.title), ("date evidence", meta.published_evidence)):
        if not contains(text, value):
            raise ValueError(f"extracted {label} {value!r} does not appear on the first pages; set it by hand in paper.yaml")
    return {
        "title": meta.title,
        "authors": meta.authors,
        "published": meta.published,
        "venue": meta.venue,
        "doi": None,
        "url": source_url,
        "pdf_url": pdf_url,
        "arxiv_id": None,
        "abstract": meta.abstract,
    }


def ingest(ref: str, provider: Provider, source_url: str | None = None, slug: str | None = None) -> WorkDir:
    meta, pdf = resolve(ref, source_url)
    staging = WORKS / ".incoming.pdf"
    if isinstance(pdf, Path):
        staging.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(pdf, staging)
    else:
        download(pdf, staging)
    pages = extract_pages(staging)
    if sum(len(p.strip()) for p in pages) < 2000:
        raise ValueError("the PDF has almost no extractable text (scanned?); OCR is not supported")
    if meta is None:
        meta = metadata_from_pdf(provider, pages, source_url, source_url if isinstance(pdf, Path) else pdf)

    wd = WorkDir(WORKS / (slug or slugify(meta["title"])))
    if wd.paper.exists():
        raise FileExistsError(f"{wd.root} already exists; delete it or pass a different --slug")
    wd.pdf.parent.mkdir(parents=True)
    shutil.move(staging, wd.pdf)
    save_json(wd.pages_json, pages)
    record = PaperRecord(
        slug=wd.slug,
        source=SourceFile(
            input=ref,
            retrieved_on=date.today(),
            sha256=hashlib.sha256(wd.pdf.read_bytes()).hexdigest(),
            pages=len(pages),
        ),
        **meta,
    )
    save_model(wd.paper, record)
    return wd


def ensure_source(wd: WorkDir, record: PaperRecord) -> None:
    """Re-fetch the pinned PDF for a work directory that has no local source (e.g. a fresh clone)."""
    if wd.pages_json.exists():
        return
    if urlparse(record.source.input).scheme == "" and Path(record.source.input).expanduser().is_file():
        wd.pdf.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(Path(record.source.input).expanduser(), wd.pdf)
    else:
        download(str(record.pdf_url), wd.pdf)
    digest = hashlib.sha256(wd.pdf.read_bytes()).hexdigest()
    if digest != record.source.sha256:
        raise ValueError(f"re-fetched PDF has sha256 {digest}, expected {record.source.sha256}")
    save_json(wd.pages_json, extract_pages(wd.pdf))
