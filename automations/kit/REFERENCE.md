# aisr_kit reference

`from aisr_kit import *` gives you all of Manim Community v0.21 (`Scene`, `VGroup`, `Circle`,
`Create`, `FadeIn`, `Transform`, `ValueTracker`, `always_redraw`, `UP`, `LEFT`, ...), NumPy as
`np`, and the kit below. It is the only import allowed.

Frame: x in [-7.1, 7.1], y in [-4, 4]. Keep text inside x in [-6.6, 6.6], y in [-3.6, 3.6].
The top-left corner holds the scene `Heading`, the top-right the epistemic `Tag`, the
bottom-left the `Source` note. Keep the main visual inside x in [-6.4, 6.4], y in [-3.0, 2.6].

## Palette

Background `BG` (near-black ink). Text: `INK` (primary), `SOFT` (secondary), `MUTED` (tertiary),
`FAINT` (hairlines, grid lines). Surfaces: `PANEL`.
Accents, used by role and consistently across the whole video:
`BLUE`, `TEAL`, `AMBER`, `ROSE`, `VIOLET`, `SAND`, `GRAY`.
`KIND_COLORS[kind]` gives the color of an epistemic status, e.g. `KIND_COLORS["observed_result"]`.

## Text (sizes below 20 raise an error)

- `T(text, size=30, color=INK, weight=None, width=None)` sans label. `weight=MEDIUM` or `SEMIBOLD`
  for emphasis. `width=28` wraps to 28 characters per line.
- `Serif(text, size=44, color=INK, italic=False, weight=None, width=None)` serif, for titles and
  quotations. `weight=BOLD` for thumbnail headlines.
- `Mono(text, size=26, color=SOFT)` monospace, for prompts, model outputs, code.
- `wrap(text, width)` returns the string broken into lines.

## Scene furniture

- `Heading(text)` scene title, top-left, with a hairline rule.
- `Tag(kind)` epistemic status pill, already placed top-right. `kind` is one of
  `observed_result`, `theoretical_result`, `author_interpretation`, `hypothesis`,
  `threat_model`, `future_scenario`, `speculation`, `limitation`, `method`, `definition`, `background`.
- `Source(text)` small citation, already placed bottom-left, e.g. `Source(f"{self.paper['short']}, Figure 3")`.
- `Panel(width, height, color=FAINT)` quiet rounded background panel for grouping.

## Diagram parts

- `Node(label, color=BLUE, width=None, height=0.9, size=26, fill=0.14)` labelled rounded box.
  Parts: `.box`, `.label`.
- `Link(a, b, label=None, color=MUTED, size=22, buff=0.15)` arrow between two mobjects' edges,
  optional label beside it. Parts: `.arrow`, `.label`. Animate with `GrowArrow(link.arrow)`.
- `Callout(target, text, direction=UP, color=SOFT, size=24, width=28)` annotation with a hairline to `target`.
- `Agent(color=BLUE, radius=0.24)` a neutral agent marker (disc with a direction notch).
- `Grid(rows, cols, cell=0.6)` grid world or matrix. `grid.cell(r, c)` is a square (row 0 on top);
  `grid.cell(r, c).get_center()` is its position.

## Data

- `self.dataset("d1")` returns `{"title", "unit", "note", "points": [{"label", "value", "display"}]}`,
  exactly as in the storyboard. Never type result numbers into code; always read them from here.
- `BarChart(points, colors=None, width=7.0, height=3.6, max_value=None, unit=None, label_size=22)`
  honest bars from zero with exact value labels. Parts: `.frame` (baseline, category labels, unit),
  `.bars`, `.values`, `.labels`. Reveal: `FadeIn(chart.frame)`, then `bars_grow(chart)`, then
  `FadeIn(chart.values)`. Pass `max_value` (e.g. 100 for percentages) when the scale has a natural top.
- `Plot(x_range, y_range, x_label, y_label, width=8, height=4.5)` quiet labelled axes; use
  `plot.axes.c2p(x, y)` and `plot.axes.plot(f)` to draw on it.

## NarratedScene

```python
class S03(NarratedScene):
    def construct(self):
        with self.beat("s03b01") as b:      # starts this beat's narration
            heading = Heading("The coin moves")
            self.play(FadeIn(heading), run_time=0.8)
            self.play(Create(grid), run_time=b.duration * 0.4)
        with self.beat("s03b02") as b:      # waits out any narration left in s03b01 first
            ...
```

- `b.duration` is the narration length in seconds. Spend at most that long on `self.play` and
  `self.wait` inside the block; the scene waits for the rest of the narration automatically.
- `self.paper` has `title`, `short` (e.g. "Langosco et al. (2022)") and `year`.
- Roadmap checkpoints are drawn by the kit. When a scene has a checkpoint, the kit shows the
  roadmap checklist before the first beat and clears the screen after it. Never draw the roadmap.
- The layout is checked at the end of every beat: text outside the frame and text overlapping
  other text are reported as defects.
