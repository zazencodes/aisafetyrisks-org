"""Narration: one audio clip per storyboard beat, synthesized locally with Kokoro."""

import hashlib
from pathlib import Path

import httpx
import numpy as np
import soundfile as sf

from paper_video.config import CACHE, TTSConfig
from paper_video.models import Storyboard
from paper_video.workdir import WorkDir, load_json, save_json

SAMPLE_RATE = 24000


def _fetch(url: str) -> Path:
    dest = CACHE / "kokoro" / url.rsplit("/", 1)[1]
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(".part")
        with httpx.stream("GET", url, follow_redirects=True, timeout=600) as r:
            r.raise_for_status()
            with tmp.open("wb") as f:
                for chunk in r.iter_bytes(1 << 20):
                    f.write(chunk)
        tmp.rename(dest)
    return dest


def spoken(text: str) -> str:
    """Narration as it should be pronounced. Symbols the phonemizer reads badly are spelled out."""
    return text.replace("%", " percent").replace("≈", "about").replace("—", ", ").replace("–", " to ")


def narrate(wd: WorkDir, sb: Storyboard, cfg: TTSConfig) -> dict[str, float]:
    """Synthesize any beat whose text or voice changed. Returns {beat_id: seconds}."""
    manifest_path = wd.audio / "manifest.json"
    manifest = load_json(manifest_path) if manifest_path.exists() else {}
    engine = None
    durations = {}
    for beat in sb.beats():
        text = spoken(beat.narration)
        key = hashlib.sha256(f"{cfg.voice}|{cfg.speed}|{text}".encode()).hexdigest()[:16]
        wav = wd.audio / f"{beat.id}.wav"
        entry = manifest.get(beat.id)
        if not (entry and entry["key"] == key and wav.exists()):
            if engine is None:
                from kokoro_onnx import Kokoro

                engine = Kokoro(str(_fetch(cfg.model_url)), str(_fetch(cfg.voices_url)))
            samples, rate = engine.create(text, voice=cfg.voice, speed=cfg.speed, lang="en-us")
            if rate != SAMPLE_RATE:
                raise RuntimeError(f"unexpected Kokoro sample rate {rate}")
            # Short fades avoid clicks at clip boundaries.
            fade = int(0.01 * rate)
            samples[:fade] *= np.linspace(0, 1, fade)
            samples[-fade:] *= np.linspace(1, 0, fade)
            wav.parent.mkdir(parents=True, exist_ok=True)
            sf.write(wav, samples, rate)
            entry = {"key": key, "duration": len(samples) / rate}
            manifest[beat.id] = entry
        durations[beat.id] = entry["duration"]
    stale = set(manifest) - set(durations)
    for beat_id in stale:
        del manifest[beat_id]
        (wd.audio / f"{beat_id}.wav").unlink(missing_ok=True)
    save_json(manifest_path, manifest)
    return durations
