"""Structured intermediate artifacts. Each is stored as editable YAML in the work directory."""

import re
from datetime import date
from typing import Literal

from aisr_site.schema import Category, ClaimKind, Evidence, Section
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


# ------------------------------------------------------------------ ingest


class SourceFile(Strict):
    input: str = Field(description="What the user passed to paper-video")
    retrieved_on: date
    sha256: str
    pages: int


class PaperRecord(Strict):
    """Normalized, versioned metadata for the source paper (paper.yaml)."""

    slug: str
    title: str
    authors: list[str]
    published: date
    venue: str | None
    url: HttpUrl
    pdf_url: HttpUrl
    arxiv_id: str | None
    doi: str | None
    abstract: str
    source: SourceFile


class ExtractedMetadata(Strict):
    """Metadata an LLM reads off the first pages of a PDF with no machine-readable metadata."""

    title: str
    authors: list[str]
    published: date = Field(description="Earliest publication date printed in the document")
    published_evidence: str = Field(description="Verbatim text from the document that states the date")
    venue: str | None
    abstract: str


# ----------------------------------------------------------------- analyze


class NoteClaim(Strict):
    id: str = Field(description="c01, c02, ... in order of appearance")
    kind: ClaimKind
    statement: str = Field(description="Faithful plain-language restatement, including the conditions it holds under")
    evidence: list[Evidence] = Field(description="Verbatim quotes that support the statement, with 1-based PDF page")


class FigureNote(Strict):
    label: str = Field(description='As printed, e.g. "Figure 3" or "Table 1"')
    page: int
    shows: str = Field(description="What the figure or table shows, in detail, including axes and conditions")


class Notes(Strict):
    """Source-grounded reading notes (notes.yaml)."""

    summary: str = Field(description="One paragraph: what was done and found, with conditions")
    research_question: str
    scope: str = Field(description="Where the results were obtained: systems, environments, settings. What they do not cover.")
    key_terms: list[str] = Field(description="Technical terms a newcomer must understand, each with a short definition")
    figures: list[FigureNote]
    claims: list[NoteClaim]


# -------------------------------------------------------------- storyboard


class DataPoint(Strict):
    label: str
    value: float
    display: str = Field(description='Exactly as printed in the paper, e.g. "46%" or "0.83"')


class Dataset(Strict):
    id: str = Field(description="d1, d2, ...")
    title: str
    unit: str = Field(description='e.g. "% of episodes", "accuracy", "reward"')
    note: str = Field(description="Conditions under which these numbers were measured")
    claims: list[str] = Field(min_length=1)
    points: list[DataPoint] = Field(min_length=1)


class Beat(Strict):
    id: str = Field(description="s01b01, s01b02, ...")
    narration: str = Field(description="Spoken text for this beat: 1-3 sentences")
    visual: str = Field(description="Exactly what is drawn or moves on screen during this beat")
    on_screen_text: list[str] = Field(description="Every text string that appears on screen, verbatim")
    claims: list[str] = Field(description="Claim ids supporting the narration and on-screen text")
    epistemic_label: ClaimKind | None = Field(description="Status tag to show on screen, when the beat presents a claim")


class Scene(Strict):
    id: str = Field(description="s01, s02, ...")
    title: str
    chapter: str = Field(description="Chapter title for YouTube and the website, at most 40 characters")
    purpose: str = Field(description="What the viewer should understand after this scene")
    visual_concept: str = Field(description="The central diagram, mechanism or metaphor, and how it evolves")
    beats: list[Beat] = Field(min_length=1)


class Thumbnail(Strict):
    headline: str = Field(description="At most 5 words, no hype")
    visual: str = Field(description="A single strong image drawn from the video's visual language")


class Storyboard(Strict):
    """The planned explainer (storyboard.yaml): scenes, beats, narration and data."""

    title: str = Field(description="Video title, at most 70 characters, accurate and not sensational")
    logline: str
    visual_language: str = Field(description="Recurring shapes, colors and motifs that carry across scenes")
    scenes: list[Scene] = Field(min_length=3)
    axis_ticks: dict[str, list[str]] = Field(default_factory=dict, description="Per-beat axis scale labels, not reported findings; each must also appear in that beat's on_screen_text")
    datasets: list[Dataset]
    thumbnail: Thumbnail

    def beats(self) -> list[Beat]:
        return [b for s in self.scenes for b in s.beats]


# ------------------------------------------------------------------ review


class ReviewIssue(Strict):
    location: str = Field(description="Beat id, scene id, or page field such as findings[2]")
    severity: Literal["blocker", "major", "minor"]
    category: Literal[
        "misrepresentation",
        "overgeneralization",
        "missing_limitation",
        "mislabelled_status",
        "unsupported_claim",
        "misleading_visual",
        "clarity",
    ]
    problem: str
    suggested_fix: str


class ScienceReview(Strict):
    verdict: Literal["accurate", "needs_revision"]
    issues: list[ReviewIssue]


class VisualIssue(Strict):
    beat: str
    severity: Literal["blocker", "major", "minor"]
    problem: str
    suggested_fix: str


class VisualReview(Strict):
    issues: list[VisualIssue]


class SceneVisualReview(VisualReview):
    render_key: str


class SceneCode(Strict):
    code: str = Field(description="The complete Python file")


# ----------------------------------------------------------------- website


class ReferenceChoice(Strict):
    url: str
    title: str
    note: str | None


class WorkDraft(Strict):
    """The parts of a website Work that are written by the model; the rest is assembled."""

    title: str
    dek: str
    category: Category
    summary: str
    explanation: list[Section]
    findings: list["DraftFinding"]
    limitations: list["DraftLimitation"]
    context: str
    extra_references: list[ReferenceChoice] = Field(
        description="Only URLs from the list of links found in the paper, when they help a reader"
    )


class DraftFinding(Strict):
    kind: ClaimKind
    text: str


class DraftLimitation(Strict):
    source: Literal["authors", "editorial"]
    text: str


WorkDraft.model_rebuild()


class YouTubeCopy(Strict):
    title: str = Field(description="At most 90 characters")
    description: str = Field(description="Plain text, 2-4 short paragraphs, no hashtags, no emoji")
    tags: list[str]

    @field_validator("title")
    @classmethod
    def title_length(cls, v: str) -> str:
        if len(v) > 100:
            raise ValueError("YouTube titles are limited to 100 characters")
        return v


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
