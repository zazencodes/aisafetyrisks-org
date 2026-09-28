"""Stage: scene clips -> master video, captions and chapter timeline."""

from paper_video.media import assemble, caption_cues, probe, srt, vtt
from paper_video.models import Storyboard
from paper_video.scenes import class_name
from paper_video.workdir import WorkDir, load_json, save_json


def assemble_video(wd: WorkDir, sb: Storyboard) -> dict:
    clips, beats, chapters, audio = [], [], [], []
    offset = 0.0
    narration = dict(sb.clips())
    for scene in sb.scenes:
        clip = wd.render / f"{scene.id}.mp4"
        report = load_json(wd.render / "reports" / f"{class_name(scene.id)}.json")
        if [b["beat"] for b in report["beats"]] != [cid for cid, _ in scene.clips()]:
            raise ValueError(f"render of {scene.id} is out of date with the storyboard; re-run the scenes stage")
        clips.append(clip)
        if not chapters or chapters[-1]["title"] != scene.chapter:
            chapters.append({"start": round(offset, 2), "title": scene.chapter})
        for b in report["beats"]:
            beats.append((offset + b["start"], b["narration"], narration[b["beat"]]))
            audio.append((offset + b["start"], wd.audio / f"{b['beat']}.wav"))
        offset += probe(clip)["duration"]

    master = wd.out / "video.mp4"
    assemble(clips, master, audio, offset)
    info = probe(master)
    cues = caption_cues(beats)
    (wd.out / "captions.srt").write_text(srt(cues))
    (wd.out / "captions.vtt").write_text(vtt(cues))

    problems = []
    if chapters[0]["start"] != 0 or len(chapters) < 3:
        problems.append("YouTube needs at least 3 chapters starting at 0:00")
    ends = [c["start"] for c in chapters[1:]] + [info["duration"]]
    problems += [f"chapter {c['title']!r} is shorter than 10 s" for c, end in zip(chapters, ends) if end - c["start"] < 10]
    timeline = {**info, "chapters": chapters, "problems": problems}
    save_json(wd.out / "timeline.json", timeline)
    save_json(wd.checks / "video.json", timeline)
    return timeline
