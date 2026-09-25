"""Pipeline configuration (automations/config.toml)."""

import tomllib
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

AUTOMATIONS = Path(__file__).resolve().parents[2]
REPO = AUTOMATIONS.parent
WORKS = AUTOMATIONS / "works"
KIT = AUTOMATIONS / "kit"
MEDIA_MIRROR = AUTOMATIONS / "media"
SITE_WORKS = REPO / "site" / "content" / "works"
BACKLOG = AUTOMATIONS / "backlog" / "papers.yaml"
CACHE = Path.home() / ".cache" / "paper-video"


class Section(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LLMConfig(Section):
    provider: Literal["claude-code", "anthropic", "openai"]
    model: str
    effort: Literal["low", "medium", "high", "xhigh", "max"]
    timeout_seconds: int


class TTSConfig(Section):
    voice: str
    speed: float
    model_url: str
    voices_url: str


class RenderConfig(Section):
    image: str
    resolution: tuple[int, int]
    frame_rate: int
    cpus: int
    memory: str
    parallel_scenes: int
    max_fix_attempts: int
    visual_review_rounds: int
    beat_pause: float


class ReviewConfig(Section):
    max_revision_rounds: int


class PublishConfig(Section):
    media_bucket: str
    site_url: str


class Config(Section):
    llm: LLMConfig
    tts: TTSConfig
    render: RenderConfig
    review: ReviewConfig
    publish: PublishConfig


def load_config(path: Path = AUTOMATIONS / "config.toml") -> Config:
    return Config.model_validate(tomllib.loads(path.read_text()))
