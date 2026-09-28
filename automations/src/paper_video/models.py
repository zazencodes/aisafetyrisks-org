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
    chapter: str = Field(description="Chapter title for YouTube and the website, at most 40 characters; "
                         "a scene that delivers a roadmap item uses that item's text")
    roadmap_item: int | None = Field(description="1-based number of the roadmap item this scene delivers; "
                                     "null for the opening scenes and the closing scene")
    checkpoint: str | None = Field(description="Narration spoken over the roadmap checklist before this scene's beats. "
                                   "Required on the first scene of each roadmap item and on the closing scene; null elsewhere")
    purpose: str = Field(description="What the viewer should understand after this scene")
    visual_concept: str = Field(description="The central diagram, mechanism or metaphor, and how it evolves")
    beats: list[Beat] = Field(min_length=1)

    @property
    def checkpoint_id(self) -> str:
        return f"{self.id}cp"

    def clips(self) -> list[tuple[str, str]]:
        """(clip id, narration) in playing order: the checkpoint, if any, then the beats."""
        head = [(self.checkpoint_id, self.checkpoint)] if self.checkpoint else []
        return head + [(b.id, b.narration) for b in self.beats]


class Thumbnail(Strict):
    headline: str = Field(description="2 to 4 plain words naming a concrete, surprising moment from the paper; "
                          "no words shared with the title")
    visual: str = Field(description="That moment, drawn with a few large shapes from the video's visual language, "
                        "no labels")


class Storyboard(Strict):
    """The planned explainer (storyboard.yaml): scenes, beats, narration and data."""

    title: str = Field(description="Video title, at most 70 characters, accurate and not sensational")
    logline: str
    visual_language: str = Field(description="Recurring shapes, colors and motifs that carry across scenes")
    roadmap: list[str] = Field(description="The 3 to 5 items of the checklist shown after the opening and ticked off "
                               "as the video delivers them; each at most 40 characters, no digits")
    scenes: list[Scene] = Field(min_length=3)
    axis_ticks: dict[str, list[str]] = Field(default_factory=dict, description="Per-beat axis scale labels, not reported findings; each must also appear in that beat's on_screen_text")
    datasets: list[Dataset]
    thumbnail: Thumbnail

    def beats(self) -> list[Beat]:
        return [b for s in self.scenes for b in s.beats]

    def clips(self) -> list[tuple[str, str]]:
        """Every narrated clip, (clip id, narration), in playing order."""
        return [c for s in self.scenes for c in s.clips()]

    def checkpoint_state(self, scene: Scene) -> tuple[int, int | None]:
        """(items ticked, 0-based item highlighted) that a scene's checkpoint moves the checklist to."""
        if scene.roadmap_item is None:
            return len(self.roadmap), None
        return scene.roadmap_item - 1, scene.roadmap_item - 1


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


class SceneVisualReview(Strict):
    render_key: str
    issues: list[VisualIssue]


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
