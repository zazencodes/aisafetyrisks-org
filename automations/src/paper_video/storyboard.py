"""Stage: check the storyboard (storyboard.yaml) against the notes and the video's fixed shape.

The storyboard is written in the session running the workflow, from `paper-video brief <slug> storyboard`.
Every video has the same shape: opening scenes (real-world stakes, then the paper), a roadmap of 3 to 5
items, scenes that deliver those items in order, and one closing scene. The kit shows the roadmap at
each scene's `checkpoint` and ticks items off as they are delivered.
"""

from paper_video import log
from paper_video.context import metadata_text
from paper_video.models import Notes, PaperRecord, Storyboard
from paper_video.provenance import numbers_in, verify_storyboard
from paper_video.workdir import WorkDir, save_json


def structure_problems(sb: Storyboard) -> list[str]:
    problems = []
    n = len(sb.roadmap)
    if not 3 <= n <= 5:
        problems.append(f"the roadmap has {n} items; it needs 3 to 5")
    for item in sb.roadmap:
        if len(item) > 40:
            problems.append(f"roadmap item {item!r} is longer than 40 characters")
        if numbers_in(item):
            problems.append(f"roadmap item {item!r} contains a number")

    items = [s.roadmap_item for s in sb.scenes]
    body = [i for i, item in enumerate(items) if item is not None]
    if not body or body[0] == 0:
        problems.append("the video must open with at least one scene without a roadmap_item: the real-world "
                        "stakes and what the paper asks, before the roadmap")
    if not body or body[-1] != len(items) - 2:
        problems.append("exactly one scene, the closing scene, must follow the last roadmap scene; "
                        "give it no roadmap_item")
    if body:
        delivered = [items[i] for i in range(body[0], body[-1] + 1)]
        if None in delivered:
            problems.append("every scene between the opening and the closing scene must deliver a roadmap item")
        order = [item for item in delivered if item is not None]
        steps_ok = order[0] == 1 and all(b - a in (0, 1) for a, b in zip(order, order[1:]))
        if not steps_ok or order[-1] != n:
            problems.append(f"scenes must deliver roadmap items 1 to {n} in order, each at least once; found {order}")

    previous = None
    for i, scene in enumerate(sb.scenes):
        closing = i == len(sb.scenes) - 1
        needs = closing or (scene.roadmap_item is not None and scene.roadmap_item != previous)
        if needs and not scene.checkpoint:
            what = "the closing scene recaps the roadmap" if closing else f"it starts roadmap item {scene.roadmap_item}"
            problems.append(f"{scene.id}: needs `checkpoint` narration, because {what}")
        if not needs and scene.checkpoint:
            problems.append(f"{scene.id}: only the first scene of a roadmap item and the closing scene have a checkpoint")
        if scene.roadmap_item is not None and 1 <= scene.roadmap_item <= n and scene.chapter != sb.roadmap[scene.roadmap_item - 1]:
            problems.append(f"{scene.id}: chapter must be its roadmap item, {sb.roadmap[scene.roadmap_item - 1]!r}")
        previous = scene.roadmap_item
    return problems


def check_storyboard(wd: WorkDir, record: PaperRecord, notes: Notes, sb: Storyboard) -> None:
    """Fail loudly if the storyboard breaks provenance or the video's shape."""
    check = verify_storyboard(sb, notes, metadata_text(record))
    check.errors += structure_problems(sb)
    save_json(wd.checks / "storyboard.json", check.as_dict())
    if not check.ok:
        raise ValueError("storyboard fails its checks:\n- " + "\n- ".join(check.errors))
    words = sum(len(text.split()) for _, text in sb.clips())
    log(f"storyboard ok: {len(sb.scenes)} scenes, {len(sb.clips())} narrated clips, {words} narration words")
