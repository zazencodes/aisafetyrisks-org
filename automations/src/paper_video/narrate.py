"""ElevenLabs narration: one lossless 24 kHz WAV per checkpoint or beat."""

import hashlib
import json

import httpx
import numpy as np
import soundfile as sf
from dotenv import dotenv_values

from paper_video import log
from paper_video.config import REPO, TTSConfig
from paper_video.models import Storyboard
from paper_video.workdir import WorkDir, load_json, save_json

SAMPLE_RATE = 24000
OUTPUT_FORMAT = "pcm_24000"


def spoken(text: str) -> str:
    """Narration as it should be pronounced. Spell out symbols used in the script."""
    return text.replace("%", " percent").replace("≈", "about").replace("—", ", ").replace("–", " to ")


def audio_key(text: str, cfg: TTSConfig) -> str:
    payload = ["elevenlabs", OUTPUT_FORMAT, cfg.model_dump(mode="json"), spoken(text)]
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]


def api_key() -> str:
    key = dotenv_values(REPO / ".env").get("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("set ELEVENLABS_API_KEY in the repository's ignored .env before narration")
    return key


def synthesize(client: httpx.Client, text: str, cfg: TTSConfig) -> np.ndarray:
    response = client.post(
        f"/v1/text-to-speech/{cfg.voice}",
        params={"output_format": OUTPUT_FORMAT},
        json={
            "text": spoken(text),
            "model_id": cfg.model,
            "voice_settings": {
                "stability": cfg.stability,
                "similarity_boost": cfg.similarity_boost,
            },
            "seed": cfg.seed,
        },
    )
    if response.is_error:
        raise RuntimeError(f"ElevenLabs returned HTTP {response.status_code}: {response.text}")
    if not response.content or len(response.content) % 2:
        raise RuntimeError("ElevenLabs returned empty or malformed PCM audio")
    samples = np.frombuffer(response.content, dtype="<i2").astype(np.float32) / 32768
    # Short fades avoid clicks at clip boundaries.
    fade = min(int(0.01 * SAMPLE_RATE), len(samples) // 2)
    samples[:fade] *= np.linspace(0, 1, fade)
    samples[-fade:] *= np.linspace(1, 0, fade)
    return samples


def narrate(wd: WorkDir, sb: Storyboard, cfg: TTSConfig) -> dict[str, float]:
    """Synthesize changed clips; save each result so interrupted runs retain paid audio."""
    manifest_path = wd.audio / "manifest.json"
    manifest = load_json(manifest_path) if manifest_path.exists() else {}
    durations = {}
    with httpx.Client(
        base_url="https://api.elevenlabs.io",
        timeout=cfg.timeout_seconds,
    ) as client:
        for clip_id, narration in sb.clips():
            key = audio_key(narration, cfg)
            wav = wd.audio / f"{clip_id}.wav"
            entry = manifest.get(clip_id)
            if not (entry and entry["key"] == key and wav.exists()):
                if "xi-api-key" not in client.headers:
                    client.headers["xi-api-key"] = api_key()
                log(f"narrating {clip_id} with {cfg.model}")
                samples = synthesize(client, narration, cfg)
                wav.parent.mkdir(parents=True, exist_ok=True)
                tmp = wav.with_suffix(".part")
                sf.write(tmp, samples, SAMPLE_RATE, format="WAV", subtype="PCM_16")
                tmp.replace(wav)
                entry = {"key": key, "duration": len(samples) / SAMPLE_RATE,
                         "provider": "elevenlabs", "model": cfg.model, "voice": cfg.voice}
                manifest[clip_id] = entry
                save_json(manifest_path, manifest)
            durations[clip_id] = entry["duration"]
    for clip_id in set(manifest) - set(durations):
        del manifest[clip_id]
        (wd.audio / f"{clip_id}.wav").unlink(missing_ok=True)
    save_json(manifest_path, manifest)
    return durations
