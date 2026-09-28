"""Static site build: content/ + templates/ + static/ -> dist/."""

import hashlib
import json
import re
import shutil
from datetime import date, datetime, time, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

import yaml
from jinja2 import Environment, PackageLoader, StrictUndefined
from markdown_it import MarkdownIt
from markupsafe import Markup
from pydantic import BaseModel, ConfigDict, HttpUrl

from aisr_site.schema import CLAIM_REF_RE, Work

SITE_ROOT = Path(__file__).resolve().parents[2]
CONTENT = SITE_ROOT / "content"
STATIC = SITE_ROOT / "static"
DIST = SITE_ROOT / "dist"


class Creator(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    email: str


class SiteConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    tagline: str
    description: str
    base_url: HttpUrl
    media_base_url: HttpUrl
    youtube_channel_url: HttpUrl | None
    creator: Creator


class Page(BaseModel):
    slug: str
    title: str
    description: str
    body: str


class LoadedWork(BaseModel):
    slug: str
    dir: Path
    work: Work


def load_config() -> SiteConfig:
    return SiteConfig.model_validate(yaml.safe_load((CONTENT / "site.yaml").read_text()))


def load_pages() -> list[Page]:
    pages = []
    for path in sorted((CONTENT / "pages").glob("*.md")):
        _, front, body = path.read_text().split("---\n", 2)
        pages.append(Page(slug=path.stem, body=body, **yaml.safe_load(front)))
    return pages


def load_works(include_drafts: bool) -> list[LoadedWork]:
    works = []
    for path in sorted((CONTENT / "works").glob("*/work.yaml")):
        work = Work.model_validate(yaml.safe_load(path.read_text()))
        for asset in (work.thumbnail, work.video.captions):
            if not (path.parent / asset).is_file():
                raise FileNotFoundError(f"{path.parent / asset} is referenced by {path} but missing")
        if work.status == "published" or include_drafts:
            works.append(LoadedWork(slug=path.parent.name, dir=path.parent, work=work))
    # Chronological feed, newest first. Drafts (no date yet) float to the top.
    return sorted(works, key=lambda w: (w.work.published_on or date.max, w.slug), reverse=True)


_md = MarkdownIt("commonmark", {"typographer": True}).enable(["replacements", "smartquotes"])


def make_markdown_filter(claim_numbers: dict[str, int]):
    def cite(match: re.Match) -> str:
        links = []
        for ref in (r.strip() for r in match.group(1).split(",")):
            n = claim_numbers[ref]
            links.append(f'<a href="#evidence-{ref}" class="cite" aria-label="Evidence {n}">{n}</a>')
        return f'<sup class="cites">{"".join(links)}</sup>'

    def render(text: str, inline: bool = False) -> Markup:
        html = _md.renderInline(text) if inline else _md.render(text)
        return Markup(CLAIM_REF_RE.sub(cite, html))

    return render


def css_bundle(dist: Path) -> str:
    css = (STATIC / "css" / "site.css").read_bytes()
    name = f"site.{hashlib.sha256(css).hexdigest()[:10]}.css"
    (dist / "static" / name).write_bytes(css)
    return f"/static/{name}"


def iso_duration(seconds: float) -> str:
    total = round(seconds)
    return f"PT{total // 60}M{total % 60}S"


def fmt_timestamp(seconds: float) -> str:
    total = int(seconds)
    return f"{total // 60}:{total % 60:02d}"


def fmt_date(d: date) -> str:
    return f"{d.day} {d.strftime('%B %Y')}"


def author_line(authors: list[str]) -> str:
    if len(authors) <= 3:
        return ", ".join(authors[:-1]) + (" and " if len(authors) > 1 else "") + authors[-1]
    return f"{authors[0]} et al."


def jsonld(data: dict) -> Markup:
    """A JSON-LD payload, safe to place inside a <script> element."""
    return Markup(json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))


def site_jsonld(cfg: SiteConfig, base: str) -> dict:
    """The site, its publisher and its creator; pages refer to these nodes by @id."""
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{base}/#website",
                "url": f"{base}/",
                "name": cfg.name,
                "description": cfg.description,
                "inLanguage": "en",
                "publisher": {"@id": f"{base}/#organization"},
            },
            {
                "@type": "Organization",
                "@id": f"{base}/#organization",
                "name": cfg.name,
                "url": f"{base}/",
                "founder": {"@id": f"{base}/#creator"},
                **({"sameAs": [str(cfg.youtube_channel_url)]} if cfg.youtube_channel_url else {}),
            },
            {
                "@type": "Person",
                "@id": f"{base}/#creator",
                "name": cfg.creator.name,
                "email": f"mailto:{cfg.creator.email}",
                "url": f"{base}/about/",
            },
        ],
    }


def work_jsonld(cfg: SiteConfig, base: str, lw: LoadedWork, url: str, image: str, video_url: str) -> dict:
    """Article + VideoObject (chapters as Clips, for key moments) + BreadcrumbList. Drafts carry no dates."""
    w = lw.work
    dates = {}
    if w.published_on:
        dates = {"datePublished": w.published_on.isoformat(),
                 "dateModified": (w.updated_on or w.published_on).isoformat()}
    ends = [ch.start for ch in w.video.chapters[1:]] + [w.video.duration_seconds]
    video = {
        "@type": "VideoObject",
        "@id": f"{url}#video",
        "name": w.title,
        "description": w.dek,
        "thumbnailUrl": image,
        "duration": iso_duration(w.video.duration_seconds),
        "contentUrl": video_url,
        "inLanguage": "en",
        "publisher": {"@id": f"{base}/#organization"},
        "hasPart": [
            {
                "@type": "Clip",
                "name": ch.title,
                "startOffset": int(ch.start),
                "endOffset": int(end),
                "url": f"{url}#t={int(ch.start)}",
            }
            for ch, end in zip(w.video.chapters, ends)
        ],
    }
    if w.published_on:
        video["uploadDate"] = w.published_on.isoformat()
    if w.video.youtube_url:
        video["sameAs"] = str(w.video.youtube_url)
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": f"{url}#article",
                "headline": w.title,
                "description": w.dek,
                "url": url,
                "mainEntityOfPage": url,
                "image": image,
                **dates,
                "inLanguage": "en",
                "articleSection": w.category.label,
                "author": {"@id": f"{base}/#creator"},
                "publisher": {"@id": f"{base}/#organization"},
                "isPartOf": {"@id": f"{base}/#website"},
                "video": {"@id": f"{url}#video"},
                "about": {
                    "@type": "ScholarlyArticle",
                    "name": w.paper.title,
                    "author": [{"@type": "Person", "name": a} for a in w.paper.authors],
                    "datePublished": w.paper.published.isoformat(),
                    "url": str(w.paper.url),
                    **({"sameAs": f"https://doi.org/{w.paper.doi}"} if w.paper.doi else {}),
                },
            },
            video,
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Explainers", "item": f"{base}/"},
                    {"@type": "ListItem", "position": 2, "name": w.title, "item": url},
                ],
            },
        ],
    }


def rss(cfg: SiteConfig, works: list[LoadedWork]) -> str:
    base = str(cfg.base_url).rstrip("/")
    items = []
    for lw in works:
        w = lw.work
        pub = datetime.combine(w.published_on, time(12), tzinfo=timezone.utc)
        link = f"{base}/works/{lw.slug}/"
        items.append(
            "<item>"
            f"<title>{escape(w.title)}</title><link>{link}</link><guid isPermaLink=\"true\">{link}</guid>"
            f"<pubDate>{format_datetime(pub)}</pubDate><category>{escape(w.category.label)}</category>"
            f"<description>{escape(w.dek)} Explains: {escape(w.paper.title)} ({escape(author_line(w.paper.authors))}, {w.paper.published.year}).</description>"
            "</item>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
        f"<title>{escape(cfg.name)}</title><link>{base}/</link><description>{escape(cfg.description)}</description>"
        f'<language>en</language><atom:link href="{base}/feed.xml" rel="self" type="application/rss+xml"/>'
        + "".join(items)
        + "</channel></rss>\n"
    )


def sitemap(urls: list[tuple[str, date | None]]) -> str:
    entries = "".join(
        f"<url><loc>{escape(u)}</loc>" + (f"<lastmod>{d.isoformat()}</lastmod>" if d else "") + "</url>"
        for u, d in urls
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>\n'


def headers_file(cfg: SiteConfig, media_base_url: str) -> str:
    csp = "; ".join(
        [
            "default-src 'self'",
            f"media-src 'self' {media_base_url}",
            "img-src 'self' data:",
            "script-src 'self'",
            "style-src 'self'",
            "font-src 'self'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
        ]
    )
    return f"""/*
  Content-Security-Policy: {csp}
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains

/static/*
  Cache-Control: public, max-age=31536000, immutable
"""


def build(include_drafts: bool = False, media_base_url: str | None = None) -> Path:
    """Build the site into dist/. `media_base_url` overrides the configured one (local preview)."""
    cfg = load_config()
    media_base = (media_base_url or str(cfg.media_base_url)).rstrip("/")
    base = str(cfg.base_url).rstrip("/")
    pages = load_pages()
    works = load_works(include_drafts)

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(STATIC, DIST / "static", ignore=shutil.ignore_patterns("css"))
    for root_file in ("favicon.svg", "og-default.png"):
        shutil.move(DIST / "static" / root_file, DIST / root_file)
    css_url = css_bundle(DIST)

    env = Environment(loader=PackageLoader("aisr_site"), undefined=StrictUndefined, autoescape=True)
    env.filters.update(date=fmt_date, timestamp=fmt_timestamp, authors=author_line)
    env.globals.update(site=cfg, base=base, css_url=css_url, year=date.today().year,
                       site_jsonld=jsonld(site_jsonld(cfg, base)))

    def write(rel: str, html: str) -> None:
        out = DIST / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)

    plain_md = make_markdown_filter({})
    write("index.html", env.get_template("index.html").render(works=works, path="/"))
    for page in pages:
        write(
            f"{page.slug}/index.html",
            env.get_template("page.html").render(page=page, body=plain_md(page.body), path=f"/{page.slug}/"),
        )
    write("404.html", env.get_template("404.html").render(path="/404"))

    for lw in works:
        w = lw.work
        numbers = {c.id: i for i, c in enumerate(w.claims, start=1)}
        out_dir = DIST / "works" / lw.slug
        out_dir.mkdir(parents=True)
        for asset in (w.thumbnail, w.video.captions):
            shutil.copy(lw.dir / asset, out_dir / asset)
        url = f"{base}/works/{lw.slug}/"
        image = f"{url}{w.thumbnail}"
        video_url = f"{media_base}/{w.video.key}"
        write(
            f"works/{lw.slug}/index.html",
            env.get_template("work.html").render(
                lw=lw,
                w=w,
                md=make_markdown_filter(numbers),
                numbers=numbers,
                url=url,
                image=image,
                video_url=video_url,
                jsonld=jsonld(work_jsonld(cfg, base, lw, url, image, video_url)),
                path=f"/works/{lw.slug}/",
            ),
        )

    published = [lw for lw in works if lw.work.status == "published"]
    write("feed.xml", rss(cfg, published))
    latest = max((lw.work.updated_on or lw.work.published_on for lw in published), default=None)
    urls = [(f"{base}/", latest)] + [(f"{base}/{p.slug}/", None) for p in pages]
    urls += [(f"{base}/works/{lw.slug}/", lw.work.updated_on or lw.work.published_on) for lw in published]
    write("sitemap.xml", sitemap(urls))
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n")
    write("_headers", headers_file(cfg, media_base))
    return DIST
