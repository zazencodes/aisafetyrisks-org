from paper_video.media import caption_cues, split_caption, srt, vtt
from paper_video.sandbox import beat_calls, static_check

GOOD = '''from aisr_kit import *

class S01(NarratedScene):
    def construct(self):
        with self.beat("s01b01") as b:
            self.play(FadeIn(T("hello")), run_time=b.duration)
        with self.beat("s01b02") as b:
            self.wait(0.1)
'''


def test_static_check_accepts_kit_scene():
    assert static_check(GOOD, "S01", "NarratedScene") == []
    assert beat_calls(GOOD) == ["s01b01", "s01b02"]


def test_static_check_rejects_escapes():
    for bad in (
        "import os\n",
        "from subprocess import run\n",
        "x = open('/etc/passwd')\n",
        "x = ().__class__.__bases__\n",
        "getattr(object, 'x')\n",
    ):
        assert static_check(GOOD + bad, "S01", "NarratedScene"), bad


def test_static_check_requires_single_named_class():
    assert static_check(GOOD.replace("S01", "Other"), "S01", "NarratedScene")
    assert static_check(GOOD.replace("NarratedScene", "Scene"), "S01", "NarratedScene")


def test_captions_split_and_timing():
    text = "Agents learned to go right. " * 6
    parts = split_caption(text)
    assert all(len(p) <= 84 for p in parts)
    cues = caption_cues([(10.0, 6.0, text)])
    assert cues[0][0] == 10.0
    assert abs(cues[-1][1] - 16.0) < 1e-9
    assert srt(cues).startswith("1\n00:00:10,000 --> ")
    assert vtt(cues).startswith("WEBVTT\n\n00:00:10.000 --> ")
