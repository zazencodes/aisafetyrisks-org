"""Archive completed video exports on the configured mounted drive and verify every copy."""

import hashlib
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Literal

from paper_video.config import REPO, BackupConfig
from paper_video.workdir import WorkDir, load_json, save_json


def checksum(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def backup_files(wd: WorkDir) -> list[Path]:
    files = [p for folder in (wd.out, wd.audio) for p in folder.rglob("*") if p.is_file()]
    files += list(wd.root.glob("*.yaml")) + list(wd.scenes.glob("*.py"))
    files += [p for p in (wd.checks / "short.json", wd.checks / "report.md") if p.is_file()]
    files = sorted(p for p in files if p.name != ".DS_Store" and not p.name.startswith("._"))
    if any(p.is_symlink() or ".part." in p.name for p in files):
        raise ValueError("backup inputs contain a symlink or unfinished export")
    return files


def verify_snapshot(snapshot: Path, entries: list[dict]) -> None:
    for entry in entries:
        path = snapshot / entry["path"]
        if path.stat().st_size != entry["bytes"] or checksum(path) != entry["sha256"]:
            raise ValueError(f"backup verification failed: {path}")


def backup_work(wd: WorkDir, cfg: BackupConfig, kind: Literal["full", "short"]) -> Path:
    """One immutable snapshot per payload; unchanged reruns verify and reuse its archive."""
    if not cfg.volume.is_mount():
        raise FileNotFoundError(f"backup volume is not mounted: {cfg.volume}; local video is retained")
    # Resolve the destination so a symlink cannot redirect the archive off the mounted drive.
    if not cfg.root.resolve().is_relative_to(cfg.volume.resolve()):
        raise ValueError("backup destination resolves outside its mounted volume")
    video = wd.out / ("video.mp4" if kind == "full" else "short/video.mp4")
    if not video.is_file():
        raise FileNotFoundError(f"completed {kind} video is missing: {video}")
    if not wd.audio.is_dir():
        raise FileNotFoundError(f"narration directory is missing: {wd.audio}")
    files = backup_files(wd)
    entries = [{"path": f"works/{wd.slug}/{p.relative_to(wd.root).as_posix()}",
                "bytes": p.stat().st_size, "sha256": checksum(p)} for p in files]
    payload = {"kind": kind, "files": entries}
    key = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    snapshot = cfg.root / wd.slug / key
    if snapshot.exists():
        manifest = load_json(snapshot / "manifest.json")
        if manifest["content_key"] != key or manifest["files"] != entries or manifest["kind"] != kind:
            raise ValueError(f"backup manifest differs from its source: {snapshot}")
        verify_snapshot(snapshot, entries)
        return snapshot
    cfg.root.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(cfg.volume).free < sum(e["bytes"] for e in entries):
        raise OSError(f"insufficient space on backup volume: {cfg.volume}")
    staging = snapshot.with_name(key + ".in-progress")
    # An interrupted snapshot stays visibly incomplete and must be investigated before retrying.
    staging.mkdir(parents=True, exist_ok=False)
    for source, entry in zip(files, entries, strict=True):
        dest = staging / entry["path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        if checksum(source) != entry["sha256"]:
            raise ValueError(f"backup source changed while copying: {source}")
    verify_snapshot(staging, entries)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    save_json(staging / "manifest.json", {
        **payload, "content_key": key, "created_at": datetime.now().astimezone().isoformat(),
        "source_repository": str(REPO), "source_commit": commit,
        "source_work_directory": str(wd.root.resolve()),
        "file_count": len(entries), "video_count": sum(Path(e["path"]).suffix == ".mp4" for e in entries),
        "total_bytes": sum(e["bytes"] for e in entries),
        "verification": "Every copied file's size and SHA-256 hash matches its source.",
    })
    if snapshot.exists():
        raise FileExistsError(f"backup destination was created while copying: {snapshot}")
    staging.rename(snapshot)
    return snapshot
