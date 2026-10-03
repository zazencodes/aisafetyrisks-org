"""One source-grounded portrait short, edited from a completed explainer's whole beats.

The agent chooses the edit in short.yaml. Narration and animations are reused verbatim;
portrait headings and captions are rendered separately so diagrams are never cropped.
"""

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Literal

from PIL import Image, ImageDraw, ImageFont
from pydantic import Field, field_validator

from paper_video.config import KIT, Config
from paper_video.context import metadata_text, short_citation
from paper_video.media import assemble, contact_sheet, frame_at, probe, run, srt, vtt
from paper_video.models import Notes, PaperRecord, ScienceReview, Storyboard, Strict, VisualIssue
from paper_video.provenance import claim_sources, number_supported, numbers_in, verify_notes, verify_storyboard
from paper_video.align import timed_parts, word_starts
from paper_video.scenes import SceneRenderer, class_name, narrated_durations
from paper_video.workdir import WorkDir, dump_yaml, load_json, load_model, save_json

# The canonical social format. Runtime is strictly less than three minutes.
WIDTH, HEIGHT, FPS, MAX_SECONDS = 1080, 1920, 30, 180
BG, INK, MUTED, ACCENT = "#111418", "#E9E7E1", "#8E949C", "#5FB3A1"
# All captions use the same ink; emphasis changes typography only.
CAPTION_STYLES = {"bold": r"{\fnIBM Plex Sans SmBld}", "italic": r"{\i1}"}
CAPTION_SIZE, CAPTION_WIDTH, CAPTION_Y = 56, 760, 1510


class CaptionEmphasis(Strict):
    phrase: str = Field(min_length=1)
    kind: Literal["bold", "italic"]


class ShortSegment(Strict):
    beat: str
    role: Literal["hook", "context", "explanation", "limitation", "takeaway"]
    heading: str = Field(min_length=1, max_length=70)
    caption_emphasis: list[CaptionEmphasis] = Field(
        description="Exact narration phrases: bold for key ideas, italic for qualifications; [] for none")


class ShortPlan(Strict):
    title: str = Field(min_length=1, max_length=90)
    description: str = Field(min_length=1, max_length=1500)
    scope_label: str = Field(min_length=1, max_length=70)
    selection_reason: str = Field(min_length=1)
    segments: list[ShortSegment] = Field(min_length=5)

    @field_validator("segments")
    @classmethod
    def shape(cls, segments):
        ids = [s.beat for s in segments]
        if len(ids) != len(set(ids)):
            raise ValueError("select each source beat once")
        if segments[0].role != "hook" or segments[-1].role != "takeaway":
            raise ValueError("open with a hook and end with a takeaway")
        for role in ("context", "explanation", "limitation"):
            if not any(s.role == role for s in segments):
                raise ValueError(f"the short needs a {role} beat")
        return segments


class ShortReview(Strict):
    content_key: str
    science: ScienceReview
    visual_issues: list[VisualIssue]


def plan_path(wd: WorkDir) -> Path:
    return wd.root / "short.yaml"


def output_dir(wd: WorkDir) -> Path:
    return wd.out / "short"


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def source_beats(wd: WorkDir, record: PaperRecord, sb: Storyboard, cfg: Config) -> dict:
    """Resolve complete beats in current scene renders; never infer timestamps from prose."""
    if not (wd.out / "video.mp4").exists():
        raise ValueError("assemble the full explainer before choosing its short")
    durations = narrated_durations(wd, sb, cfg.tts)
    renderer = SceneRenderer(wd, record, sb, cfg)
    result, offset = {}, 0.0
    for scene in sb.scenes:
        if not renderer.is_current(scene):
            raise ValueError(f"source render {scene.id} is out of date; regenerate the full explainer")
        clip = wd.render / f"{scene.id}.mp4"
        report = load_json(wd.render / "reports" / f"{class_name(scene.id)}.json")
        if [b["beat"] for b in report["beats"]] != [cid for cid, _ in scene.clips()]:
            raise ValueError(f"source timing report {scene.id} is out of date")
        timings = {b["beat"]: b for b in report["beats"]}
        clip_duration = probe(clip)["duration"]
        for beat in scene.beats:
            timing = timings[beat.id]
            start, end = timing["start"], timing["hold_end"]
            if not (0 <= start < end <= clip_duration + 1 / FPS):
                raise ValueError(f"{beat.id}: invalid source timing")
            if abs(timing["narration"] - durations[beat.id]) > 1 / FPS:
                raise ValueError(f"{beat.id}: source timing differs from narration")
            # Quantize each cut down to whole output frames so no frame of the next beat shows.
            duration = math.floor((end - start) * FPS + 1e-6) / FPS
            if duration < durations[beat.id]:
                raise ValueError(f"{beat.id}: would cut off narration")
            result[beat.id] = {
                "scene": scene.id, "clip": clip, "start": start,
                "duration": duration,
                "narration_duration": durations[beat.id],
                "source_start": offset + start, "beat": beat,
            }
        offset += clip_duration
    return result


def validate_plan(wd: WorkDir, record: PaperRecord, sb: Storyboard, notes: Notes,
                  plan: ShortPlan, sources: dict) -> list[dict]:
    _, quotes = verify_notes(notes, wd.pages())
    provenance = verify_storyboard(sb, notes, metadata_text(record))
    errors = quotes.errors + provenance.errors
    unknown = [s.beat for s in plan.segments if s.beat not in sources]
    errors += [f"unknown source beat {b}" for b in unknown]
    if errors:
        raise ValueError("short fails provenance:\n- " + "\n- ".join(errors))
    chosen = [sources[s.beat] for s in plan.segments]
    duration = sum(b["duration"] for b in chosen)
    if duration >= MAX_SECONDS:
        raise ValueError(f"short is {duration:.2f}s; it must be strictly less than {MAX_SECONDS}s")
    claims = {c.id: c for c in notes.claims}
    selected_claims = sorted({c for b in chosen for c in b["beat"].claims})
    all_quotes = claim_sources(claims, selected_claims) + [metadata_text(record)]
    for text in (plan.title, plan.description, plan.scope_label):
        for number in numbers_in(text):
            if not number_supported(number, all_quotes):
                errors.append(f"number {number} in {text!r} is unsupported")
    for segment, source in zip(plan.segments, chosen):
        try:
            emphasis_spans(source["beat"].narration, segment.caption_emphasis)
        except ValueError as e:
            errors.append(f"{segment.beat}: {e}")
        quotes = claim_sources(claims, source["beat"].claims) + [metadata_text(record)]
        for number in numbers_in(segment.heading):
            if not number_supported(number, quotes):
                errors.append(f"{segment.beat}: heading number {number} is unsupported")
    if errors:
        raise ValueError("short fails provenance:\n- " + "\n- ".join(errors))
    return chosen


def content_key(wd: WorkDir, plan: ShortPlan, chosen: list[dict]) -> str:
    paths = {wd.paper, wd.notes, wd.storyboard, Path(__file__)}
    paths.update(Path(__file__).with_name(name) for name in ("media.py", "align.py"))
    paths.update((KIT / "fonts").glob("*.ttf"))
    for b in chosen:
        paths.update((b["clip"], wd.audio / f"{b['beat'].id}.wav"))
    payload = [plan.model_dump(mode="json"),
               [(str(p.relative_to(wd.root)) if p.is_relative_to(wd.root) else p.name, file_hash(p))
                for p in sorted(paths)],
               [{k: b[k] for k in ("start", "duration", "narration_duration", "source_start", "word_starts")}
                for b in chosen]]
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]


def load_inputs(wd: WorkDir, record: PaperRecord, cfg: Config):
    plan = load_model(plan_path(wd), ShortPlan)
    sb = load_model(wd.storyboard, Storyboard)
    notes = load_model(wd.notes, Notes)
    sources = source_beats(wd, record, sb, cfg)
    chosen = validate_plan(wd, record, sb, notes, plan, sources)
    for b in chosen:
        b["word_starts"] = word_starts(wd.audio / f"{b['beat'].id}.wav", b["beat"].narration, cfg.captions)
    return plan, chosen, content_key(wd, plan, chosen)


def font(size: int, name: str = "IBMPlexSans-Medium.ttf"):
    return ImageFont.truetype(str(KIT / "fonts" / name), size)


def wrap(text: str, face, width: int) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        if face.getlength(word) > width:
            raise ValueError(f"word {word!r} is too wide for the portrait layout")
        candidate = f"{line} {word}".strip()
        if face.getlength(candidate) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    return lines + ([line] if line else [])


def draw_lines(draw, text: str, y: int, size: int, color: str, max_lines: int) -> None:
    face = font(size)
    lines = wrap(text, face, 880)
    if len(lines) > max_lines:
        raise ValueError(f"portrait text needs {len(lines)} lines (maximum {max_lines}): {text!r}")
    for line in lines:
        draw.text((80, y), line, font=face, fill=color)
        y += round(size * 1.25)


def portrait_card(dest: Path, plan: ShortPlan, segment: ShortSegment, record: PaperRecord,
                  index: int, total: int, diagram_height: int) -> None:
    image = Image.new("RGBA", (WIDTH, HEIGHT), BG)
    # A transparent aperture preserves the entire landscape diagram underneath.
    image.paste((0, 0, 0, 0), (0, 550, WIDTH, 550 + diagram_height))
    draw = ImageDraw.Draw(image)
    draw.text((80, 145), "AI SAFETY RISKS", font=font(30), fill=ACCENT)
    draw_lines(draw, plan.title, 215, 60, INK, 2)
    draw_lines(draw, segment.heading, 390, 48, ACCENT, 2)
    draw_lines(draw, plan.scope_label, 1190, 32, MUTED, 2)
    draw.text((80, 1280), short_citation(record), font=font(32), fill=MUTED)
    draw.line((80, 1640, 960, 1640), fill="#3A3F47", width=2)
    draw.text((80, 1660), "Full explainer + sources", font=font(34), fill=INK)
    draw.text((80, 1710), "aisafetyrisks.org", font=font(32), fill=ACCENT)
    draw.rectangle((80, 1785, 960, 1791), fill="#3A3F47")
    draw.rectangle((80, 1785, 80 + round(880 * (index + 1) / total), 1791), fill=ACCENT)
    image.save(dest)


def ass_time(seconds: float) -> str:
    cs = round(seconds * 100)
    hours, cs = divmod(cs, 360000)
    minutes, cs = divmod(cs, 6000)
    seconds, cs = divmod(cs, 100)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{cs:02d}"


def ass_text(text: str) -> str:
    # Literal narration must never become subtitle markup.
    return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def emphasis_spans(text: str, phrases: list[CaptionEmphasis]) -> list[tuple[int, int, str]]:
    spans = []
    for emphasis in phrases:
        phrase = emphasis.phrase
        if not phrase.strip():
            raise ValueError("caption emphasis phrases must not be blank")
        matches = list(re.finditer(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text))
        if not matches:
            raise ValueError(f"caption emphasis {phrase!r} is not an exact narration phrase")
        spans.extend((m.start(), m.end(), emphasis.kind) for m in matches)
    spans.sort()
    if any(a[1] > b[0] for a, b in zip(spans, spans[1:])):
        raise ValueError("caption emphasis phrases overlap")
    return spans


def emphasized_text(text: str, spans: list[tuple[int, int, str]], offset: int) -> str:
    pieces, cursor = [], 0
    for start, end, kind in spans:
        a, z = max(start - offset, 0), min(end - offset, len(text))
        if a >= z:
            continue
        pieces.extend((ass_text(text[cursor:a]), CAPTION_STYLES[kind], ass_text(text[a:z]),
                       r"{\fnIBM Plex Sans Medm\i0}"))
        cursor = z
    pieces.append(ass_text(text[cursor:]))
    return "".join(pieces)


def caption_file(path: Path, cues: list[tuple], emphasis: list[CaptionEmphasis]) -> None:
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,IBM Plex Sans Medm,56,&H00E1E7E9,&H00E1E7E9,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,5,140,180,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    spans = emphasis_spans(" ".join(text for _, _, text in cues), emphasis)
    events, offset = [], 0
    for start, end, text in cues:
        lines = wrap(text, font(CAPTION_SIZE, "IBMPlexSans-SemiBold.ttf"), CAPTION_WIDTH)
        if len(lines) > 2:
            raise ValueError(f"caption needs more than two portrait lines: {text!r}")
        displayed_lines, line_offset = [], offset
        for line in lines:
            displayed_lines.append(emphasized_text(line, spans, line_offset))
            line_offset += len(line) + 1
        displayed = r"\N".join(displayed_lines)
        # Center the complete caption block between the citation and the footer divider.
        events.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Caption,,0,0,0,,"
                      + f"{{\\pos(520,{CAPTION_Y})}}" + displayed)
        offset += len(text) + 1
    path.write_text(header + "\n".join(events) + "\n")


def filter_path(path: Path) -> str:
    return str(path.resolve()).replace("\\", "\\\\").replace(":", "\\:").replace("'", "'\\''")


def caption_parts(text: str, emphasis: list[CaptionEmphasis]) -> list[str]:
    """Balance sentence batches within two lines, keeping emphasized phrases together."""
    spans = emphasis_spans(text, emphasis)
    face = font(CAPTION_SIZE, "IBMPlexSans-SemiBold.ttf")
    units, previous_span = [], None
    for match in re.finditer(r"\S+", text):
        word = match.group()
        span = next((s for s in spans if s[0] < match.end() and s[1] > match.start()), None)
        if span and span == previous_span:
            units[-1] = (units[-1][0] + " " + word, span[2])
        else:
            units.append((word, span[2] if span else None))
        previous_span = span
    parts, sentence = [], []

    def batches(units):
        # Fewest batches first, then balanced lengths avoid a fleeting last word.
        # Sum of squared lengths favors equal sizes for a fixed batch count.
        best = {len(units): ((0, 0), [])}
        for i in range(len(units) - 1, -1, -1):
            words, options = [], []
            for j in range(i, len(units)):
                word, kind = units[j]
                words.append(word)
                candidate = " ".join(words)
                if len(wrap(candidate, face, CAPTION_WIDTH)) > 2:
                    break
                if j + 1 in best:
                    (count, cost), tail = best[j + 1]
                    options.append(((count + 1, cost + len(candidate) ** 2), [candidate, *tail]))
            if options:
                best[i] = min(options, key=lambda option: option[0])
        if 0 not in best:
            raise ValueError("emphasized phrase exceeds the two-line caption limit")
        return best[0][1]

    for unit in units:
        sentence.append(unit)
        if unit[0].endswith((".", "!", "?", ";", ":")):
            parts.extend(batches(sentence))
            sentence = []
    if sentence:
        parts.extend(batches(sentence))
    return parts


def short_cues(chosen: list[dict], segments: list[ShortSegment]) -> list[tuple]:
    # Caption segmentation is identical for burned captions and the SRT/VTT files.
    cues, offset = [], 0.0
    for b, segment in zip(chosen, segments, strict=True):
        if b["beat"].id != segment.beat:
            raise ValueError("caption segment differs from selected source beat")
        parts = caption_parts(b["beat"].narration, segment.caption_emphasis)
        cues += timed_parts(parts, b["word_starts"], offset, b["narration_duration"])
        offset += b["duration"]
    return cues


def build_short(wd: WorkDir, record: PaperRecord, cfg: Config) -> dict:
    plan, chosen, key = load_inputs(wd, record, cfg)
    out = output_dir(wd)
    render = wd.render / "short" / key
    render.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    videos, audio, timeline, shots = [], [], [], []
    offset = 0.0
    cues = short_cues(chosen, plan.segments)
    for i, (segment, b) in enumerate(zip(plan.segments, chosen)):
        clip = render / f"{i:02d}.mp4"
        if not clip.exists():
            info = probe(b["clip"])
            diagram_height = round(info["height"] * WIDTH / info["width"] / 2) * 2
            if diagram_height > 608:
                raise ValueError("shorts require landscape source scenes fitting the diagram aperture")
            card = render / f"{i:02d}.png"
            portrait_card(card, plan, segment, record, i, len(chosen), diagram_height)
            captions = render / f"{i:02d}.ass"
            # Segment-local cues avoid losing the first cue to accumulated ffprobe rounding.
            caption_file(captions, short_cues([b], [segment]), segment.caption_emphasis)
            graph = (
                f"[0:v]fps={FPS},scale={WIDTH}:{diagram_height},setsar=1,"
                f"pad={WIDTH}:{HEIGHT}:0:550:color={BG}[diagram];"
                f"[diagram][1:v]overlay=0:0:shortest=1,"
                f"subtitles=filename='{filter_path(captions)}':fontsdir='{filter_path(KIT / 'fonts')}'[v]"
            )
            run(["ffmpeg", "-v", "error", "-y", "-ss", str(b["start"]), "-i", str(b["clip"]),
                 "-loop", "1", "-i", str(card), "-filter_complex", graph, "-map", "[v]", "-an",
                 "-t", str(b["duration"]), "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                 "-pix_fmt", "yuv420p", str(clip.with_suffix(".part.mp4"))])
            clip.with_suffix(".part.mp4").replace(clip)
        videos.append(clip)
        audio.append((offset, wd.audio / f"{segment.beat}.wav"))
        timeline.append({"beat": segment.beat, "role": segment.role, "heading": segment.heading,
                         "start": offset, "duration": b["duration"], "source_start": b["source_start"],
                         "claims": b["beat"].claims, "narration": b["beat"].narration})
        offset += probe(clip)["duration"]
    master = out / "video.mp4"
    stamp = out / "timeline.json"
    cached = load_json(stamp) if stamp.exists() else None
    if not (master.exists() and cached and cached.get("content_key") == key
            and cached["video_sha256"] == file_hash(master)):
        assembled = out / "video.part.mp4"
        assemble(videos, assembled, audio, offset)
        info = probe(assembled)
        if info["duration"] >= MAX_SECONDS or (info["width"], info["height"]) != (WIDTH, HEIGHT):
            raise ValueError(f"short output violates format/duration constraints: {info}")
        assembled.replace(master)
        save_json(stamp, {**info, "content_key": key, "segments": timeline,
                          "video_sha256": file_hash(master)})
    (out / "captions.srt").write_text(srt(cues))
    (out / "captions.vtt").write_text(vtt(cues))
    # Every cut's first frame and transition, at phone width, for the independent review.
    for b in timeline:
        for label, t in (("cut", b["start"] + 0.01), ("+0.3 s", b["start"] + 0.3), ("+0.6 s", b["start"] + 0.6),
                         ("+1 s", b["start"] + 1), ("end", b["start"] + b["duration"] - 0.5)):
            name = f"{b['beat']}-{label.replace(' ', '').replace('+', 'plus').replace('.', '')}.png"
            shots.append((f"{b['beat']} {label}", frame_at(master, t, wd.frames / "short" / name)))
    contact_sheet(shots, wd.frames / "short-sheet.png", cols=5, width=360)
    frame_at(master, min(4, timeline[0]["duration"] / 2), out / "cover.jpg")
    review = current_short_review(wd, key)
    package = {
        "status": "draft", "content_key": key,
        "files": {"video": "out/short/video.mp4", "cover": "out/short/cover.jpg",
                  "captions_srt": "out/short/captions.srt", "captions_vtt": "out/short/captions.vtt"},
        "format": {"width": WIDTH, "height": HEIGHT, "frame_rate": FPS, "duration": probe(master)["duration"]},
        "title": plan.title, "description": plan.description,
        "links": {"explainer": f"{cfg.publish.site_url}/works/{wd.slug}/", "paper": str(record.url)},
        "citation": short_citation(record), "review": review.model_dump(mode="json") if review else None,
        "provenance": [{"beat": b["beat"], "claims": b["claims"]} for b in timeline],
    }
    (wd.root / "short-package.yaml").write_text(dump_yaml(package))
    return load_json(stamp)


def current_short_review(wd: WorkDir, key: str) -> ShortReview | None:
    path = wd.root / "short-review.yaml"
    if not path.exists():
        return None
    review = load_model(path, ShortReview)
    return review if review.content_key == key else None


def check_short(wd: WorkDir, record: PaperRecord, cfg: Config) -> dict:
    _, _, key = load_inputs(wd, record, cfg)
    out = output_dir(wd)
    for name in ("video.mp4", "cover.jpg", "captions.srt", "captions.vtt", "timeline.json"):
        if not (out / name).exists():
            raise FileNotFoundError(f"missing short output {name}; run paper-video short again")
    result = load_json(out / "timeline.json")
    if result["content_key"] != key or result["video_sha256"] != file_hash(out / "video.mp4"):
        raise ValueError("short output is out of date; run paper-video short again")
    info = probe(out / "video.mp4")
    if info["duration"] >= MAX_SECONDS or (info["width"], info["height"]) != (WIDTH, HEIGHT):
        raise ValueError("short must be 1080x1920 and strictly less than three minutes")
    review = current_short_review(wd, key)
    if review is None:
        raise ValueError("independent science/visual review of the current short is missing")
    blockers = [i.problem for i in [*review.science.issues, *review.visual_issues]
                if i.severity in ("blocker", "major")]
    if review.science.verdict != "accurate" or blockers:
        raise ValueError(f"short review needs revision: {blockers}")
    save_json(wd.checks / "short.json", {**result, "ok": True, "review": review.model_dump(mode="json")})
    return result
