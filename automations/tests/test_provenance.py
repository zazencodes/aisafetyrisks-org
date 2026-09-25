from aisr_site.schema import Evidence

from paper_video.models import Beat, Dataset, DataPoint, NoteClaim, Notes, Scene, Storyboard, Thumbnail
from paper_video.provenance import (
    canon,
    locate_quote,
    number_supported,
    numbers_in,
    verify_notes,
    verify_storyboard,
)

PAGES = [
    "Goal misgeneraliza-\ntion occurs when an RL agent retains its capabil-\nities out-of-distribution yet pursues the wrong goal.",
    "In CoinRun, the agent reaches the end of the level in 89% of test episodes\nbut collects the coin in only 11 %.",
]


def test_canon_joins_hyphenation_and_ignores_layout():
    assert canon("capabil-\nities  out-of-distribution") == canon("capabilities outofdistribution")


def test_locate_quote_finds_and_corrects_page():
    quote = "retains its capabilities out-of-distribution yet pursues the wrong goal"
    assert locate_quote(PAGES, quote, 1) == 1
    assert locate_quote(PAGES, quote, 2) == 1
    assert locate_quote(PAGES, "the agent collects the coin in every episode", 2) is None


def test_short_quotes_are_rejected():
    assert locate_quote(PAGES, "the agent", 2) is None


def test_numbers_in_ignores_links_and_citations():
    assert numbers_in("It reached 89% [c03] in 2022; see [code](https://x.org/v2).") == ["89%", "2022"]


def test_number_supported_is_exact():
    sources = [PAGES[1]]
    assert number_supported("89%", sources)
    assert number_supported("11%", sources)  # "11 %" in the PDF
    assert not number_supported("8", sources)
    assert not number_supported("90%", sources)


def _notes() -> Notes:
    return Notes(
        summary="s", research_question="q", scope="s", key_terms=[], figures=[],
        claims=[NoteClaim(id="c01", kind="observed_result", statement="s",
                          evidence=[Evidence(page=1, quote="the agent reaches the end of the level in 89% of test episodes")])],
    )


def test_verify_notes_corrects_page():
    notes, report = verify_notes(_notes(), PAGES)
    assert report.ok
    assert notes.claims[0].evidence[0].page == 2


def _storyboard(narration: str, display: str = "89%", value: float = 89) -> Storyboard:
    beat = Beat(id="s01b01", narration=narration, visual="v", on_screen_text=[], claims=["c01"], epistemic_label=None)
    scenes = [Scene(id=f"s0{i}", title="t", chapter="c", purpose="p", visual_concept="v",
                    beats=[beat.model_copy(update={"id": f"s0{i}b01"})]) for i in (1, 2, 3)]
    return Storyboard(
        title="t", logline="l", visual_language="v", scenes=scenes,
        datasets=[Dataset(id="d1", title="t", unit="%", note="n", claims=["c01"],
                          points=[DataPoint(label="end", value=value, display=display)])],
        thumbnail=Thumbnail(headline="h", visual="v"),
    )


def test_storyboard_numbers_must_come_from_cited_quotes():
    notes, _ = verify_notes(_notes(), PAGES)
    assert verify_storyboard(_storyboard("It reached the end in 89% of episodes."), notes, "2022").ok
    bad = verify_storyboard(_storyboard("It reached the end in 90% of episodes."), notes, "2022")
    assert any("90%" in e for e in bad.errors)


def test_dataset_value_must_match_display():
    notes, _ = verify_notes(_notes(), PAGES)
    report = verify_storyboard(_storyboard("ok", value=88), notes, "2022")
    assert any("does not match" in e for e in report.errors)
