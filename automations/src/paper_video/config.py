"""Pipeline configuration (automations/config.toml)."""

import tomllib
from datetime import time
from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo
from pydantic import BaseModel, ConfigDict, Field, model_validator

AUTOMATIONS = Path(__file__).resolve().parents[2]
REPO = AUTOMATIONS.parent
WORKS = AUTOMATIONS / "works"
KIT = AUTOMATIONS / "kit"
MEDIA_MIRROR = AUTOMATIONS / "media"
SITE_WORKS = REPO / "site" / "content" / "works"
BACKLOG = AUTOMATIONS / "backlog" / "papers.yaml"


class Section(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AgyConfig(Section):
    model: str
    timeout_seconds: int


class TTSConfig(Section):
    model: str = Field(min_length=1)
    voice: str = Field(min_length=1)
    stability: float = Field(ge=0, le=1)
    similarity_boost: float = Field(ge=0, le=1)
    seed: int = Field(ge=0, le=4294967295)
    timeout_seconds: int = Field(gt=0)


class RenderConfig(Section):
    resolution: tuple[int, int]
    frame_rate: int
    parallel_scenes: int
    beat_pause: float


class PublishConfig(Section):
    media_bucket: str
    site_url: str


class BackupConfig(Section):
    volume: Path
    root: Path

    @model_validator(mode="after")
    def location(self):
        if not self.volume.is_absolute() or not self.root.is_absolute():
            raise ValueError("backup volume and root must be absolute paths")
        if self.root == self.volume or not self.root.is_relative_to(self.volume):
            raise ValueError("backup root must be inside the backup volume")
        if ".." in self.volume.parts or ".." in self.root.parts:
            raise ValueError("backup paths must not contain '..'")
        return self


Weekday = Literal["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


class SocialConfig(Section):
    timezone: str
    long_form_day: Weekday
    short_day: Weekday
    time: time
    youtube_account: str = Field(min_length=1)
    instagram_account: str = Field(min_length=1)
    timeout_seconds: int = Field(gt=0)

    @model_validator(mode="after")
    def zone(self):
        ZoneInfo(self.timezone)
        return self


class Config(Section):
    agy: AgyConfig
    tts: TTSConfig
    render: RenderConfig
    publish: PublishConfig
    backup: BackupConfig
    social: SocialConfig


def load_config(path: Path = AUTOMATIONS / "config.toml") -> Config:
    return Config.model_validate(tomllib.loads(path.read_text()))
