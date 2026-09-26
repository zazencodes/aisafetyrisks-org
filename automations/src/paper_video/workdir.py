"""Layout of a work directory: automations/works/<slug>/."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar

import yaml
from pydantic import BaseModel

from paper_video.config import WORKS

M = TypeVar("M", bound=BaseModel)


class _Dumper(yaml.SafeDumper):
    pass


def _str_presenter(dumper: yaml.SafeDumper, value: str):
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_Dumper.add_representer(str, _str_presenter)


def dump_yaml(data) -> str:
    return yaml.dump(data, Dumper=_Dumper, sort_keys=False, allow_unicode=True, width=100)


def save_model(path: Path, model: BaseModel) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_yaml(model.model_dump(mode="json")))


def load_model(path: Path, cls: type[M]) -> M:
    return cls.model_validate(yaml.safe_load(path.read_text()))


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def load_json(path: Path):
    return json.loads(path.read_text())


@dataclass(frozen=True)
class WorkDir:
    root: Path

    @classmethod
    def for_slug(cls, slug: str) -> "WorkDir":
        root = WORKS / slug
        if not root.is_dir():
            raise FileNotFoundError(f"no work directory {root}; run `paper-video ingest` first")
        return cls(root)

    @property
    def slug(self) -> str:
        return self.root.name

    # Source (not versioned)
    @property
    def pdf(self) -> Path:
        return self.root / "source" / "paper.pdf"

    @property
    def pages_json(self) -> Path:
        return self.root / "source" / "pages.json"

    # Editable, versioned artifacts
    @property
    def paper(self) -> Path:
        return self.root / "paper.yaml"

    @property
    def notes(self) -> Path:
        return self.root / "notes.yaml"

    @property
    def storyboard(self) -> Path:
        return self.root / "storyboard.yaml"

    @property
    def scenes(self) -> Path:
        return self.root / "scenes"

    def scene_file(self, scene_id: str) -> Path:
        return self.scenes / f"{scene_id}.py"

    def visual_review(self, scene_id: str) -> Path:
        return self.root / "visual-reviews" / f"{scene_id}.yaml"

    @property
    def thumbnail_scene(self) -> Path:
        return self.scenes / "thumbnail.py"

    @property
    def site_draft(self) -> Path:
        return self.root / "site.yaml"

    @property
    def youtube(self) -> Path:
        return self.root / "youtube.yaml"

    @property
    def youtube_copy(self) -> Path:
        return self.root / "youtube-copy.yaml"

    @property
    def checks(self) -> Path:
        return self.root / "checks"

    # Derived, not versioned
    @property
    def audio(self) -> Path:
        return self.root / "audio"

    @property
    def render(self) -> Path:
        return self.root / "render"

    @property
    def frames(self) -> Path:
        return self.root / "frames"

    @property
    def out(self) -> Path:
        return self.root / "out"

    @property
    def briefs(self) -> Path:
        return self.root / "briefs"

    def pages(self) -> list[str]:
        """Extracted text of each PDF page; index 0 is page 1."""
        return load_json(self.pages_json)
