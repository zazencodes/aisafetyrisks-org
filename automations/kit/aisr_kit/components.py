"""Reusable, restrained building blocks for explainer scenes.

Everything here is plain Manim underneath; scenes may mix these with any Manim
primitive. Coordinates use Manim's frame: x in [-7.1, 7.1], y in [-4, 4].
"""

import textwrap

import numpy as np
from manim import (
    DL,
    DOWN,
    LEFT,
    MEDIUM,
    ORIGIN,
    RIGHT,
    SEMIBOLD,
    UL,
    UP,
    UR,
    AnimationGroup,
    Arrow,
    Axes,
    Circle,
    Dot,
    DashedLine,
    GrowFromEdge,
    Line,
    Rectangle,
    RoundedRectangle,
    Square,
    Text,
    VGroup,
)

from aisr_kit.style import (
    AMBER,
    BLUE,
    FAINT,
    INK,
    KIND_COLORS,
    KIND_LABELS,
    MIN_FONT_SIZE,
    MONO,
    MUTED,
    PANEL,
    SANS,
    SERIF,
    SOFT,
    TEAL,
    ROSE,
)

SAFE_WIDTH = 13.0
SAFE_HEIGHT = 7.2


def _check_size(size: float) -> None:
    if size < MIN_FONT_SIZE:
        raise ValueError(f"font size {size} is below the legibility minimum of {MIN_FONT_SIZE}")


# Pango kerns small text poorly; build text large and scale it down.
_OVERSAMPLE = 4


def _text(content: str, size: float, **kwargs) -> Text:
    _check_size(size)
    return Text(content, font_size=size * _OVERSAMPLE, **kwargs).scale(1 / _OVERSAMPLE)


def wrap(text: str, width: int) -> str:
    """Break a string into lines of at most `width` characters."""
    return "\n".join(textwrap.wrap(text, width)) if len(text) > width else text


def T(text: str, size: float = 30, color: str = INK, weight=None, width: int | None = None) -> Text:
    """Sans-serif label text. `width` wraps to that many characters per line."""
    return _text(wrap(text, width) if width else text, size, font=SANS, color=color,
                 weight=weight or "NORMAL", line_spacing=0.8)


def Serif(text: str, size: float = 44, color: str = INK, italic: bool = False, width: int | None = None) -> Text:
    """Serif display text for titles and quotations."""
    return _text(wrap(text, width) if width else text, size, font=SERIF, color=color,
                 slant="ITALIC" if italic else "NORMAL", line_spacing=0.85)


def Mono(text: str, size: float = 26, color: str = SOFT) -> Text:
    """Monospace text for prompts, code, model outputs."""
    return _text(text, size, font=MONO, color=color, line_spacing=0.8)


def Node(label: str, color: str = BLUE, width: float | None = None, height: float = 0.9,
         size: float = 26, fill: float = 0.14) -> VGroup:
    """A labelled rounded box: a component, an agent, a dataset, a stage."""
    text = T(label, size=size, color=INK, weight=MEDIUM)
    w = width or max(text.width + 0.6, 1.4)
    box = RoundedRectangle(corner_radius=0.12, width=w, height=max(height, text.height + 0.35),
                           stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=fill)
    text.move_to(box)
    group = VGroup(box, text)
    group.box, group.label = box, text
    return group


def _edge_point(mob, direction: np.ndarray) -> np.ndarray:
    """Where a ray from the mobject's centre along `direction` leaves its bounding box."""
    c = mob.get_center()
    hw, hh = mob.width / 2, mob.height / 2
    dx, dy = abs(direction[0]) or 1e-9, abs(direction[1]) or 1e-9
    return c + direction * min(hw / dx, hh / dy)


def Link(a, b, label: str | None = None, color: str = MUTED, size: float = 22, buff: float = 0.15) -> VGroup:
    """An arrow from mobject `a` to mobject `b`, edge to edge, with an optional label beside it."""
    d = b.get_center() - a.get_center()
    d = d / np.linalg.norm(d)
    start = _edge_point(a, d) + d * buff
    end = _edge_point(b, -d) - d * buff
    arrow = Arrow(start, end, buff=0, stroke_width=3, color=color, max_tip_length_to_length_ratio=0.2,
                  tip_length=0.2)
    group = VGroup(arrow)
    group.arrow = arrow
    if label:
        text = T(label, size=size, color=MUTED)
        normal = np.array([-d[1], d[0], 0])
        if normal[1] < 0 or (normal[1] == 0 and normal[0] < 0):
            normal = -normal
        reach = abs(normal[0]) * text.width / 2 + abs(normal[1]) * text.height / 2
        text.move_to(arrow.get_center() + normal * (reach + 0.12))
        group.add(text)
        group.label = text
    return group


def Tag(kind: str) -> VGroup:
    """Epistemic status tag, e.g. OBSERVED RESULT. Place with `.to_corner(UR)`."""
    color = KIND_COLORS[kind]
    dot = Dot(radius=0.07, color=color)
    text = T(KIND_LABELS[kind].upper(), size=20, color=color, weight=SEMIBOLD)
    text.next_to(dot, RIGHT, buff=0.14)
    body = VGroup(dot, text)
    pill = RoundedRectangle(corner_radius=0.2, width=body.width + 0.45, height=0.46,
                            stroke_color=color, stroke_width=1.5, fill_color=PANEL, fill_opacity=1)
    pill.move_to(body)
    group = VGroup(pill, body)
    group.to_corner(UR, buff=0.4)
    return group


def Source(text: str) -> Text:
    """Small citation in the lower-left corner, e.g. 'Langosco et al. (2022), Figure 3'."""
    note = T(text, size=20, color=MUTED)
    note.to_corner(DL, buff=0.35)
    return note


def Heading(text: str) -> VGroup:
    """Scene heading in the upper-left corner with a hairline rule beneath it."""
    title = Serif(text, size=34, color=SOFT)
    title.to_corner(UL, buff=0.45)
    rule = Line(title.get_corner(DL) + DOWN * 0.15, title.get_corner(DL) + DOWN * 0.15 + RIGHT * 1.2,
                stroke_width=2, color=FAINT)
    return VGroup(title, rule)


def Panel(width: float, height: float, color: str = FAINT) -> RoundedRectangle:
    """A quiet background panel to group related elements."""
    return RoundedRectangle(corner_radius=0.18, width=width, height=height, stroke_color=color,
                            stroke_width=1.5, fill_color=PANEL, fill_opacity=0.9)


ROUTE_ITEMS = (
    "The CoinRun puzzle",
    "Define and test",
    "Four environments",
    "Training diversity",
    "Actor and critic",
    "Meaning and limits",
)


def Roadmap(stage: int, complete: bool = False) -> VGroup:
    """The recurring six-step checklist. Checks are separate for a staggered reveal."""
    if not 0 <= stage < len(ROUTE_ITEMS):
        raise ValueError(f"invalid roadmap stage {stage}")
    frame = Panel(9.2, 5.65).move_to([-1.75, 0, 0])
    heading = Serif("Our route", size=39).move_to([-4.7, 2.34, 0])
    rows = VGroup()
    checks = VGroup()
    for i, label in enumerate(ROUTE_ITEMS):
        y = 1.52 - i * 0.75
        is_active = i == stage and not complete
        done = i < stage or complete
        if is_active:
            highlight = RoundedRectangle(corner_radius=0.12, width=8.55, height=0.65,
                                         stroke_color=AMBER, stroke_width=1.6,
                                         fill_color=AMBER, fill_opacity=0.1).move_to([-1.75, y, 0])
        else:
            highlight = RoundedRectangle(corner_radius=0.12, width=8.55, height=0.65,
                                         stroke_color=FAINT, stroke_width=0.8,
                                         fill_color=PANEL, fill_opacity=0.2).move_to([-1.75, y, 0])
        marker = Circle(radius=0.13, stroke_color=TEAL if done else AMBER if is_active else MUTED,
                        stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to([-5.47, y, 0])
        txt = T(label, size=28, color=INK if is_active else SOFT if done else MUTED,
                weight=MEDIUM if is_active else None)
        txt.move_to([-3.33, y, 0], aligned_edge=LEFT)
        rows.add(VGroup(highlight, marker, txt))
        if done:
            x = -5.47
            check = VGroup(
                Line([x - 0.08, y, 0], [x - 0.01, y - 0.07, 0], color=TEAL, stroke_width=3),
                Line([x - 0.01, y - 0.07, 0], [x + 0.12, y + 0.09, 0], color=TEAL, stroke_width=3),
            )
            checks.add(check)
    group = VGroup(frame, heading, rows, checks)
    group.card = VGroup(frame, heading, rows)
    group.checks = checks
    return group


def RoadmapMotif() -> VGroup:
    """A compact CoinRun reminder beside the recurring checklist."""
    panel = Panel(3.15, 5.65).move_to([4.65, 0, 0])
    ground = Line([3.43, -0.82, 0], [5.9, -0.82, 0], color=FAINT, stroke_width=3)
    block = Rectangle(width=0.34, height=0.4, stroke_color=MUTED, stroke_width=1.5,
                      fill_color=MUTED, fill_opacity=0.35).move_to([4.48, -0.62, 0])
    wall = Rectangle(width=0.12, height=1.25, stroke_color=MUTED, stroke_width=1.5,
                     fill_color=MUTED, fill_opacity=0.45).move_to([5.78, -0.21, 0])
    agent = Agent(color=TEAL, radius=0.19).move_to([3.69, -0.6, 0])
    coin = Circle(radius=0.17, stroke_color=AMBER, stroke_width=2,
                  fill_color=AMBER, fill_opacity=1).move_to([4.75, 0.03, 0])
    proxy = DashedLine([3.69, -1.34, 0], [5.77, -1.34, 0],
                       color=ROSE, stroke_width=3, dash_length=0.12)
    return VGroup(panel, ground, block, wall, agent, coin, proxy)


def Grid(rows: int, cols: int, cell: float = 0.6, color: str = FAINT, fill: str = PANEL) -> VGroup:
    """A grid world or matrix. `grid.cell(r, c)` returns a cell; row 0 is the top row."""
    squares = VGroup(*[
        Square(side_length=cell, stroke_color=color, stroke_width=1.5, fill_color=fill, fill_opacity=1)
        for _ in range(rows * cols)
    ]).arrange_in_grid(rows=rows, cols=cols, buff=0)
    squares.rows, squares.cols = rows, cols
    squares.cell = lambda r, c: squares[r * cols + c]
    return squares


def BarChart(points: list[dict], colors: list[str] | None = None, width: float = 7.0, height: float = 3.6,
             max_value: float | None = None, unit: str | None = None, label_size: float = 22) -> VGroup:
    """Honest bar chart from a dataset: bars start at zero, values print exactly as the paper does.

    `points` are dataset points ({"label", "value", "display"}), e.g. `self.dataset("d1")["points"]`.
    Parts: `.frame` (baseline, category labels, unit), `.bars`, `.values`. Typical reveal:
    `FadeIn(chart.frame)`, then `bars_grow(chart)`, then `FadeIn(chart.values)`.
    """
    top = max_value if max_value is not None else max(p["value"] for p in points)
    if top <= 0:
        raise ValueError("BarChart needs a positive maximum")
    n = len(points)
    slot = width / n
    bar_w = min(slot * 0.62, 1.4)
    colors = colors or [BLUE] * n
    baseline = Line(LEFT * width / 2, RIGHT * width / 2, stroke_width=2, color=MUTED)
    bars, values, labels = VGroup(), VGroup(), VGroup()
    for i, (p, color) in enumerate(zip(points, colors)):
        x = -width / 2 + slot * (i + 0.5)
        h = max(height * p["value"] / top, 0.02)
        bar = Rectangle(width=bar_w, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9)
        bar.move_to([x, h / 2, 0])
        value = T(p["display"], size=label_size + 2, color=INK, weight=MEDIUM).next_to(bar, UP, buff=0.12)
        label = T(p["label"], size=label_size, color=SOFT, width=max(int(slot * 7), 8))
        label.next_to([x, 0, 0], DOWN, buff=0.2)
        bars.add(bar)
        values.add(value)
        labels.add(label)
    chart = VGroup(baseline, bars, values, labels)
    if unit:
        unit_label = T(unit, size=label_size, color=MUTED)
        unit_label.move_to([-width / 2 + unit_label.width / 2, height + 0.75, 0])
        chart.add(unit_label)
        chart.unit = unit_label
    chart.baseline, chart.bars, chart.values, chart.labels = baseline, bars, values, labels
    chart.frame = VGroup(baseline, labels, *([chart.unit] if unit else []))
    chart.move_to(ORIGIN)
    return chart


def bars_grow(chart: VGroup, lag: float = 0.15) -> AnimationGroup:
    """Grow a BarChart's bars from the baseline, one after another."""
    return AnimationGroup(*[GrowFromEdge(b, DOWN) for b in chart.bars], lag_ratio=lag)


def Plot(x_range, y_range, x_label: str, y_label: str, width: float = 8, height: float = 4.5) -> VGroup:
    """Quiet axes with labels. Use `.axes.plot(...)` / `.axes.c2p(x, y)` to draw data."""
    axes = Axes(x_range=x_range, y_range=y_range, x_length=width, y_length=height,
                axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False,
                             "font_size": 22, "decimal_number_config": {"color": MUTED}},
                tips=False)
    xl = T(x_label, size=22, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.45)
    yl = T(y_label, size=22, color=MUTED).rotate(np.pi / 2).next_to(axes.y_axis, LEFT, buff=0.45)
    group = VGroup(axes, xl, yl)
    group.axes = axes
    return group


def Callout(target, text: str, direction=UP, color: str = SOFT, size: float = 24, width: int = 28) -> VGroup:
    """A short annotation connected to `target` by a hairline."""
    label = T(text, size=size, color=color, width=width)
    label.next_to(target, direction, buff=0.7)
    line = Line(label.get_edge_center(-direction), target.get_edge_center(direction), stroke_width=1.5, color=FAINT)
    return VGroup(line, label)


def Agent(color: str = BLUE, radius: float = 0.24) -> VGroup:
    """A simple, neutral agent marker: a filled circle with a direction notch."""
    body = Circle(radius=radius, stroke_width=0, fill_color=color, fill_opacity=1)
    notch = Dot(point=body.get_center() + RIGHT * radius * 0.45, radius=radius * 0.22, color="#111418")
    return VGroup(body, notch)
