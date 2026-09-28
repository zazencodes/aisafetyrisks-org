"""The roadmap checklist that NarratedScene plays at each checkpoint. Scenes never draw it themselves."""

from manim import LEFT, MEDIUM, Circle, Line, RoundedRectangle, VGroup

from aisr_kit.components import Panel, Serif, T
from aisr_kit.style import AMBER, FAINT, INK, MUTED, PANEL, SOFT, TEAL

ROW_GAP = 0.9
ROW_WIDTH = 10.4


def checklist(items: list[str], done: int, active: int | None) -> VGroup:
    """The roadmap with items[:done] ticked and items[active] highlighted.

    Every row has the same parts (highlight, marker, label, tick) whatever its state, so one state
    transforms smoothly into the next. Parts: `.frame`, `.heading`, `.rows`.
    """
    top = (len(items) - 1) * ROW_GAP / 2 - 0.35
    rows = VGroup()
    for i, item in enumerate(items):
        y = top - i * ROW_GAP
        is_done, is_active = i < done, i == active
        highlight = RoundedRectangle(corner_radius=0.12, width=ROW_WIDTH, height=0.7, stroke_color=AMBER,
                                     stroke_width=1.6, fill_color=AMBER).move_to([0, y, 0])
        highlight.set_fill(opacity=0.1 if is_active else 0).set_stroke(opacity=1 if is_active else 0)
        marker = Circle(radius=0.15, stroke_color=TEAL if is_done else AMBER if is_active else MUTED,
                        stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([-4.7, y, 0])
        label = T(item, size=32, color=INK if is_active else SOFT if is_done else MUTED,
                  weight=MEDIUM if is_active else None)
        label.move_to([-4.2, y, 0], aligned_edge=LEFT)
        x = -4.7
        tick = VGroup(Line([x - 0.09, y, 0], [x - 0.02, y - 0.08, 0], stroke_width=3.5),
                      Line([x - 0.02, y - 0.08, 0], [x + 0.13, y + 0.1, 0], stroke_width=3.5))
        tick.set_stroke(TEAL, opacity=1 if is_done else 0)
        rows.add(VGroup(highlight, marker, label, tick))
    frame = Panel(ROW_WIDTH + 0.8, (len(items) - 1) * ROW_GAP + 2.4).move_to([0, 0.1, 0])
    heading = Serif("What we'll cover", size=40).move_to([0, top + 1.0, 0])
    heading.align_to(rows[0][2], LEFT)
    rule = Line(frame.get_left(), frame.get_right(), color=FAINT, stroke_width=1).scale(0.92)
    rule.move_to([0, top + 0.55, 0])
    group = VGroup(frame, heading, rule, rows)
    group.frame, group.heading, group.rows = VGroup(frame, rule), heading, rows
    return group
