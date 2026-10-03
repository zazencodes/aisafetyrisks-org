"""Caption timing read from the cached narration audio with local whisper.cpp; never calls ElevenLabs."""
import difflib
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

from paper_video.config import CaptionsConfig


def _norm(word: str) -> str:
    return re.sub(r"[^a-z0-9%]", "", word.lower())


def word_starts(wav: Path, narration: str, cfg: CaptionsConfig) -> list[float]:
    """Start time in seconds of each whitespace-separated narration word, cached beside the WAV."""
    words = narration.split()
    key = hashlib.sha256(json.dumps([hashlib.sha256(wav.read_bytes()).hexdigest(), narration,
                                     cfg.whisper_model.name]).encode()).hexdigest()[:16]
    cache = wav.with_suffix(".words.json")
    if cache.exists():
        data = json.loads(cache.read_text())
        if data["key"] == key:
            return data["starts"]
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([cfg.whisper_cli, "-m", str(cfg.whisper_model), "-f", str(wav), "-ml", "1", "-sow",
                        "-oj", "-of", f"{tmp}/words", "-np"], check=True, capture_output=True)
        segments = json.loads(Path(f"{tmp}/words.json").read_text())["transcription"]
    heard = [(_norm(s["text"]), s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000)
             for s in segments if _norm(s["text"])]
    target = [_norm(w) for w in words]
    starts: list[float | None] = [None] * len(words)
    matcher = difflib.SequenceMatcher(a=target, b=[h[0] for h in heard], autojunk=False)
    for a, b, n in matcher.get_matching_blocks():
        for k in range(n):
            starts[a + k] = heard[b + k][1]
    if sum(s is not None for s in starts) < 0.6 * len(words):
        raise ValueError(f"{wav.name}: the transcribed audio does not match the narration text")
    # Unmatched words are spaced evenly between their matched neighbours.
    anchors = [(-1, 0.0)] + [(i, s) for i, s in enumerate(starts) if s is not None] + [(len(words), heard[-1][2])]
    for (i, t0), (j, t1) in zip(anchors, anchors[1:]):
        for k in range(i + 1, j):
            starts[k] = t0 + (t1 - t0) * (k - i) / (j - i)
    monotonic, last = [], 0.0
    for s in starts:
        last = max(last, s)
        monotonic.append(round(last, 3))
    cache.write_text(json.dumps({"key": key, "starts": monotonic}))
    return monotonic


def timed_parts(parts: list[str], starts: list[float], offset: float, duration: float) -> list[tuple]:
    """Cue each caption part from its first spoken word until the next part; the first cue opens the beat."""
    bounds, i = [], 0
    for part in parts:
        bounds.append(starts[i] if bounds else 0.0)
        i += len(part.split())
    if i != len(starts):
        raise ValueError("caption parts do not reproduce the narration words")
    ends = bounds[1:] + [duration]
    return [(offset + a, offset + b, part) for a, b, part in zip(bounds, ends, parts)]
