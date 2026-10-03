"""Video plumbing: probing, frame capture, contact sheets, final assembly, captions."""

import json
import re
import subprocess
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from paper_video.config import KIT
from paper_video.align import timed_parts
from paper_video.narrate import SAMPLE_RATE


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed: {proc.stderr[-3000:]}")
    return proc.stdout


def probe(path: Path) -> dict:
    data = json.loads(run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)]))
    video = next(s for s in data["streams"] if s["codec_type"] == "video")
    return {"duration": float(data["format"]["duration"]), "width": video["width"], "height": video["height"]}


def frame_at(video: Path, t: float, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(t, 0):.3f}", "-i", str(video), "-frames:v", "1", str(dest)])
    return dest


def contact_sheet(frames: list[tuple[str, Path]], dest: Path, cols: int = 2, width: int = 960) -> Path:
    """Grid of labelled frames, for visual review."""
    font = ImageFont.truetype(str(KIT / "fonts" / "IBMPlexSans-SemiBold.ttf"), 26)
    tiles = []
    for label, path in frames:
        img = Image.open(path).convert("RGB")
        img = img.resize((width, int(img.height * width / img.width)))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 170, 42], fill=(240, 200, 60))
        draw.text((10, 6), label, fill=(0, 0, 0), font=font)
        tiles.append(img)
    rows = (len(tiles) + cols - 1) // cols
    h = tiles[0].height
    sheet = Image.new("RGB", (cols * width + (cols - 1) * 8, rows * h + (rows - 1) * 8), (255, 255, 255))
    for i, tile in enumerate(tiles):
        sheet.paste(tile, ((i % cols) * (width + 8), (i // cols) * (h + 8)))
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest)
    return dest


def narration_track(clips: list[tuple[float, Path]], duration: float, dest: Path) -> None:
    """Place source narration at its recorded times, preserving silence between beats/scenes."""
    cursor = 0
    with wave.open(str(dest), "wb") as track:
        track.setparams((1, 2, SAMPLE_RATE, 0, "NONE", "not compressed"))
        for start, path in clips:
            frame = round(start * SAMPLE_RATE)
            if frame < cursor:
                raise ValueError(f"narration overlaps the previous clip at {path}")
            with wave.open(str(path), "rb") as clip:
                if (clip.getnchannels(), clip.getsampwidth(), clip.getframerate()) != (1, 2, SAMPLE_RATE):
                    raise ValueError(f"{path}: narration must be mono 16-bit {SAMPLE_RATE} Hz WAV")
                track.writeframesraw(b"\0\0" * (frame - cursor))
                track.writeframesraw(clip.readframes(clip.getnframes()))
                cursor = frame + clip.getnframes()
        end = round(duration * SAMPLE_RATE)
        if cursor > end:
            raise ValueError("narration extends past the video")
        track.writeframesraw(b"\0\0" * (end - cursor))


def assemble(scene_videos: list[Path], dest: Path, narration: list[tuple[float, Path]], duration: float) -> None:
    """Encode the scene visuals with the complete source narration, normalized and faststart."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    listing = dest.with_suffix(".txt")
    listing.write_text("".join(f"file '{p.resolve()}'\n" for p in scene_videos))
    track = dest.with_suffix(".wav")
    narration_track(narration, duration, track)
    run([
        "ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
        "-i", str(track), "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", str(dest),
    ])
    listing.unlink()
    track.unlink()


# ---------------------------------------------------------------- captions


def split_caption(text: str, limit: int = 84) -> list[str]:
    """Split narration into caption cues at sentence and clause boundaries, then at word boundaries."""
    pieces = re.split(r"(?<=[.!?;:])\s+", text.strip())
    cues = []
    for piece in pieces:
        words, line = piece.split(), ""
        for word in words:
            if line and len(line) + 1 + len(word) > limit:
                cues.append(line)
                line = word
            else:
                line = f"{line} {word}".strip()
        if line:
            cues.append(line)
    return cues


def caption_cues(beats: list[tuple[float, float, str, list[float]]]) -> list[tuple[float, float, str]]:
    """(start, duration, narration, word starts) per beat -> (start, end, text) cues timed to the speech."""
    cues = []
    for start, duration, text, starts in beats:
        cues += timed_parts(split_caption(text), starts, start, duration)
    return cues


def _ts(t: float, sep: str) -> str:
    ms = round(t * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def srt(cues) -> str:
    return "\n".join(f"{i}\n{_ts(a, ',')} --> {_ts(b, ',')}\n{t}\n" for i, (a, b, t) in enumerate(cues, start=1))


def vtt(cues) -> str:
    return "WEBVTT\n\n" + "\n".join(f"{_ts(a, '.')} --> {_ts(b, '.')}\n{t}\n" for a, b, t in cues)
