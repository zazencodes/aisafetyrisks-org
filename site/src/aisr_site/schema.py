"""Content schema for aisafetyrisks.org.

This module is the single contract between the research-to-video pipeline
(`automations/`) and the website build. The pipeline writes `work.yaml` files that
validate against `Work`; the site build refuses to render anything that does not.
"""

import re
from datetime import date
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Category(StrEnum):
    alignment = "alignment"
    specification = "specification"
    interpretability = "interpretability"
    deception = "deception"
    power_seeking = "power-seeking"
    scalable_oversight = "scalable-oversight"
    ai_control = "ai-control"
    evaluations = "evaluations"
    robustness = "robustness"
    dangerous_capabilities = "dangerous-capabilities"
    catastrophic_risk = "catastrophic-risk"
    governance = "governance"

    @property
    def label(self) -> str:
        return CATEGORY_LABELS[self]


CATEGORY_LABELS = {
    Category.alignment: "Alignment",
    Category.specification: "Specification & goal misgeneralization",
    Category.interpretability: "Interpretability",
    Category.deception: "Deceptive behavior",
    Category.power_seeking: "Power-seeking",
    Category.scalable_oversight: "Scalable oversight",
    Category.ai_control: "AI control",
    Category.evaluations: "Evaluations",
    Category.robustness: "Robustness",
    Category.dangerous_capabilities: "Dangerous capabilities",
    Category.catastrophic_risk: "Catastrophic & existential risk",
    Category.governance: "Governance",
}


class ClaimKind(StrEnum):
    """Epistemic status of a statement, as the source paper presents it."""

    observed_result = "observed_result"
    theoretical_result = "theoretical_result"
    author_interpretation = "author_interpretation"
    hypothesis = "hypothesis"
    threat_model = "threat_model"
    future_scenario = "future_scenario"
    speculation = "speculation"
    limitation = "limitation"
    method = "method"
    definition = "definition"
    background = "background"

    @property
    def label(self) -> str:
        return CLAIM_KIND_LABELS[self]


CLAIM_KIND_LABELS = {
    ClaimKind.observed_result: "Observed result",
    ClaimKind.theoretical_result: "Theoretical result",
    ClaimKind.author_interpretation: "Authors' interpretation",
    ClaimKind.hypothesis: "Hypothesis",
    ClaimKind.threat_model: "Threat model",
    ClaimKind.future_scenario: "Future scenario",
    ClaimKind.speculation: "Speculation",
    ClaimKind.limitation: "Stated limitation",
    ClaimKind.method: "Method",
    ClaimKind.definition: "Definition",
    ClaimKind.background: "Background",
}

CLAIM_ID = r"c\d{2,3}"
CLAIM_REF_RE = re.compile(rf"\[({CLAIM_ID}(?:\s*,\s*{CLAIM_ID})*)\]")


def claim_refs_in(text: str) -> list[str]:
    """Claim ids cited inline in prose as `[c03]` or `[c03, c07]`."""
    return [ref.strip() for group in CLAIM_REF_RE.findall(text) for ref in group.split(",")]


class Evidence(Strict):
    page: int = Field(ge=1, description="1-based page number in the source PDF")
    quote: str = Field(min_length=8, description="Verbatim excerpt from the source")


class Claim(Strict):
    id: str = Field(pattern=rf"^{CLAIM_ID}$")
    kind: ClaimKind
    statement: str = Field(description="Plain-language restatement of what the source says")
    evidence: list[Evidence] = Field(min_length=1)


class Paper(Strict):
    title: str
    authors: list[str] = Field(min_length=1)
    published: date = Field(description="Date the research was first made public")
    venue: str | None = None
    url: HttpUrl = Field(description="Canonical landing page of the research")
    pdf_url: HttpUrl
    arxiv_id: str | None = Field(default=None, description="Versioned arXiv id, e.g. 2105.14111v7")
    doi: str | None = None


class Section(Strict):
    heading: str
    body: str = Field(description="Markdown; cite claims inline as [c01]")


class Finding(Strict):
    kind: ClaimKind
    text: str = Field(description="Markdown; cite claims inline as [c01]")


class Limitation(Strict):
    source: Literal["authors", "editorial"]
    text: str = Field(description="Markdown; author-stated limitations must cite claims inline")


class Reference(Strict):
    title: str
    url: HttpUrl
    note: str | None = None


class Chapter(Strict):
    start: float = Field(ge=0)
    title: str


class Video(Strict):
    key: str = Field(description="Object key in the media bucket, e.g. works/<slug>/video-<hash>.mp4")
    duration_seconds: float = Field(gt=0)
    width: int
    height: int
    captions: str = Field(description="WebVTT filename inside the work directory")
    chapters: list[Chapter] = Field(min_length=1)
    youtube_url: HttpUrl | None = None


class Review(Strict):
    reviewed_by: str
    reviewed_on: date


class Work(Strict):
    status: Literal["draft", "published"]
    published_on: date | None = Field(default=None, description="Publication date on aisafetyrisks.org")
    updated_on: date | None = None
    title: str
    dek: str = Field(max_length=240, description="One-sentence summary used in the feed and metadata")
    category: Category
    paper: Paper
    summary: str = Field(description="Markdown: the explanation in brief")
    explanation: list[Section] = Field(min_length=1)
    findings: list[Finding] = Field(min_length=1)
    limitations: list[Limitation] = Field(min_length=1)
    context: str = Field(description="Markdown: how to read these results, and what they do not show")
    claims: list[Claim] = Field(min_length=1)
    references: list[Reference] = Field(min_length=1)
    video: Video
    thumbnail: str = Field(description="Image filename inside the work directory")
    review: Review | None = None
    production: dict[str, str] = Field(description="How this explainer was produced (pipeline, models)")

    @model_validator(mode="after")
    def check_consistency(self) -> "Work":
        if self.status == "published" and (self.published_on is None or self.review is None):
            raise ValueError("published works require published_on and review")
        ids = [c.id for c in self.claims]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate claim ids")
        known = set(ids)
        for where, text in self.prose():
            missing = [ref for ref in claim_refs_in(text) if ref not in known]
            if missing:
                raise ValueError(f"{where} cites unknown claims {missing}")
        for i, finding in enumerate(self.findings):
            if not claim_refs_in(finding.text):
                raise ValueError(f"findings[{i}] must cite at least one claim")
        for i, limitation in enumerate(self.limitations):
            if limitation.source == "authors" and not claim_refs_in(limitation.text):
                raise ValueError(f"limitations[{i}] is attributed to the authors but cites no claim")
        return self

    def prose(self) -> list[tuple[str, str]]:
        """Every reader-facing text field, labelled by location."""
        fields = [("title", self.title), ("dek", self.dek), ("summary", self.summary), ("context", self.context)]
        fields += [(f"explanation[{i}]", f"{s.heading}\n{s.body}") for i, s in enumerate(self.explanation)]
        fields += [(f"findings[{i}]", f.text) for i, f in enumerate(self.findings)]
        fields += [(f"limitations[{i}]", l.text) for i, l in enumerate(self.limitations)]
        return fields

    def cited_claim_ids(self) -> list[str]:
        """Claim ids in order of first citation in the reader-facing text."""
        seen: dict[str, None] = {}
        for _, text in self.prose():
            for ref in claim_refs_in(text):
                seen.setdefault(ref)
        return list(seen)
