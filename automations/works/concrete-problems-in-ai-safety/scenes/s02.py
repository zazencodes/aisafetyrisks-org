# storyboard: 7421997f5f48f094
from aisr_kit import *

WHITE_C = "#F4F2EC"
BROWN = "#8A6344"
RED = "#D0574A"
GOLD_C = "#E2C15A"
ORANGE = AMBER


def robot(side=0.5):
    body = RoundedRectangle(corner_radius=side * 0.18, width=side, height=side, stroke_width=0,
                            fill_color=BLUE, fill_opacity=1)
    eye = Circle(radius=side * 0.12, stroke_width=0, fill_color=WHITE_C, fill_opacity=1)
    eye.move_to(body.get_right() + LEFT * side * 0.2)
    pointer = Line(body.get_right(), body.get_right() + RIGHT * side * 0.35, stroke_width=3, color=WHITE_C)
    return VGroup(body, eye, pointer)


def vase(radius=0.22):
    return Circle(radius=radius, stroke_color=WHITE_C, stroke_width=2, fill_color=TEAL, fill_opacity=1)


def red_cross(center, size=0.22):
    a = Line(center + UL * size, center + DR * size, stroke_width=4, color=RED)
    b = Line(center + UR * size, center + DL * size, stroke_width=4, color=RED)
    return VGroup(a, b)


def score_counter(width=0.9):
    pill = RoundedRectangle(corner_radius=0.1, width=width, height=0.34, stroke_color=GOLD_C,
                            stroke_width=2, fill_color=GOLD_C, fill_opacity=0.2)
    ticks = VGroup(*[Line(UP * 0.09, DOWN * 0.09, stroke_width=3, color=GOLD_C) for _ in range(4)])
    ticks.arrange(RIGHT, buff=0.1).move_to(pill)
    return VGroup(pill, ticks)


def office():
    floor = RoundedRectangle(corner_radius=0.25, width=6.0, height=3.4, stroke_color=GRAY, stroke_width=3,
                             fill_color=PANEL, fill_opacity=1)
    bot = robot(0.55).move_to(floor.get_center() + LEFT * 1.6 + DOWN * 0.4)
    v = vase().move_to(floor.get_center() + RIGHT * 1.3 + UP * 0.5)
    cross = red_cross(v.get_center(), 0.3)
    messes = VGroup(*[Dot(point=floor.get_center() + np.array(p), radius=0.08, color=BROWN)
                      for p in [(-0.4, 0.9, 0), (0.3, -0.9, 0), (2.0, -0.6, 0), (-2.3, 0.8, 0)]])
    score = score_counter().move_to(floor.get_corner(UR) + np.array([-0.7, -0.4, 0]))
    group = VGroup(floor, messes, v, cross, score, bot)
    group.robot = bot
    group.floor = floor
    return group


def cloud(width=5.2):
    parts = [Circle(radius=r).move_to(np.array(p)) for r, p in [
        (0.9, (-1.4, 0.0, 0)), (1.2, (-0.2, 0.35, 0)), (1.0, (1.1, 0.1, 0)), (0.8, (2.0, -0.2, 0)),
        (0.8, (-2.2, -0.25, 0)), (0.9, (0.4, -0.45, 0)), (0.8, (-0.9, -0.5, 0))]]
    shape = Union(*parts, stroke_color=MUTED, stroke_width=1.5, fill_color=PANEL, fill_opacity=0.6)
    shape.scale_to_fit_width(width)
    return shape


def tab(label):
    return Node(label, color=ORANGE, height=0.5, size=20, fill=0.1)


class S02(NarratedScene):
    def construct(self):
        # Beat 1: the definition of an accident, with the office shrinking to the corner.
        with self.beat("s02b01") as b:
            heading = Heading("What the paper set out to do")
            tag = Tag("definition")
            room = office()
            self.play(FadeIn(heading), FadeIn(room), run_time=1.0)
            self.play(room.animate.scale(0.4).move_to(np.array([5.0, -2.35, 0])), FadeIn(tag), run_time=1.4)

            title = Serif(self.paper["title"], size=44, color=INK)
            title.move_to(UP * 1.75)
            cite = T("Amodei et al. (2016)", size=26, color=MUTED)
            cite.next_to(title, DOWN, buff=0.3)
            self.play(FadeIn(title, shift=UP * 0.2), FadeIn(cite), run_time=1.3)

            word = Serif("Accident", size=48, color=ROSE, italic=True)
            word.move_to(DOWN * 0.1)
            self.play(FadeIn(word, scale=0.9), run_time=0.9)

            phrase = T("unintended and harmful behavior", size=30, color=INK, weight=MEDIUM)
            phrase.next_to(word, DOWN, buff=0.35)
            rest = T("that may emerge from poor design of real-world AI systems", size=22, color=SOFT)
            rest.next_to(phrase, DOWN, buff=0.2)
            self.play(Write(phrase), run_time=2.4)
            self.play(FadeIn(rest), run_time=1.0)
            self.play(Indicate(room.floor, color=ROSE, scale_factor=1.04), run_time=1.2)

        # Beat 2: away from extreme scenarios, towards practical, testable problems.
        with self.beat("s02b02") as b:
            tag2 = Tag("author_interpretation")
            self.play(FadeOut(VGroup(title, cite, word, phrase, rest)), ReplacementTransform(tag, tag2),
                      run_time=1.0)
            tag = tag2

            puff = cloud(5.0)
            puff_label = T("Extreme scenarios", size=28, color=MUTED)
            big = VGroup(puff, puff_label)
            puff_label.move_to(puff)
            big.move_to(UP * 3.2)
            big.set_opacity(0)
            self.play(big.animate.move_to(UP * 0.7).set_opacity(0.8), run_time=2.0)
            puff_label.set_fill(opacity=0.8)
            self.play(FadeOut(big, shift=UP * 0.4), run_time=1.4)

            boxes = VGroup(*[RoundedRectangle(corner_radius=0.1, width=1.0, height=0.7, stroke_color=BLUE,
                                              stroke_width=2, fill_color=BLUE, fill_opacity=0.12)
                             for _ in range(5)])
            boxes.arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
            row_label = T("Practical problems", size=28, color=INK, weight=MEDIUM)
            row_label.next_to(boxes, UP, buff=0.45)
            self.play(FadeIn(boxes, shift=LEFT * 1.5), FadeIn(row_label), run_time=1.4)
            self.play(LaggedStart(*[box.animate.set_fill(BLUE, opacity=0.75) for box in boxes], lag_ratio=0.5),
                      run_time=3.0)
            testable = T("Testable today", size=26, color=TEAL)
            testable.next_to(boxes, DOWN, buff=0.45)
            self.play(FadeIn(testable, shift=UP * 0.15), run_time=0.9)

        # Beat 3: the pipeline from designer to robot splits three ways.
        with self.beat("s02b03") as b:
            tag3 = Tag("definition")
            bot = room.robot
            others = VGroup(*[m for m in room if m is not bot])
            self.play(FadeOut(VGroup(boxes, row_label, testable)), FadeOut(others), ReplacementTransform(tag, tag3),
                      bot.animate.scale(2.5).move_to(np.array([5.7, 2.0, 0])),
                      run_time=1.2)
            tag = tag3

            designer = Node("Designer", color=GRAY, size=24)
            designer.move_to(np.array([-5.3, 2.0, 0]))
            main = Arrow(designer.get_right() + RIGHT * 0.12, bot.get_left() + LEFT * 0.15, buff=0,
                         stroke_width=3, color=MUTED, tip_length=0.2, max_tip_length_to_length_ratio=0.1)
            self.play(FadeIn(designer), run_time=0.6)
            self.play(GrowArrow(main), run_time=1.2)

            names = ["Wrong goal", "Too costly to check", "Learning goes wrong"]
            xs = [-3.8, 0.0, 3.8]
            branches = VGroup()
            cats = VGroup()
            for name, x in zip(names, xs):
                node = Node(name, color=ORANGE, width=3.5, size=24, fill=0.06)
                node.move_to(np.array([x, 0.55, 0]))
                line = Line(np.array([x, 2.0, 0]), node.get_top() + UP * 0.08, stroke_width=2.5, color=ORANGE)
                branches.add(line)
                cats.add(node)
            self.play(LaggedStart(*[Create(l) for l in branches], lag_ratio=0.3), run_time=1.2)
            for node in cats:
                self.play(FadeIn(node, shift=DOWN * 0.15), run_time=0.5)
                self.play(node.box.animate.set_fill(ORANGE, opacity=0.35), run_time=0.6)

        # Beat 4: five problems under three branches; the robot rolls into the centre.
        with self.beat("s02b04") as b:
            tag4 = Tag("method")
            self.play(ReplacementTransform(tag, tag4), *[n.box.animate.set_fill(ORANGE, opacity=0.12) for n in cats],
                      run_time=0.8)
            tag = tag4

            groups = [["Side effects", "Reward hacking"], ["Scalable oversight"],
                      ["Safe exploration", "Distributional shift"]]
            tabs = VGroup()
            stems = VGroup()
            for labels, node in zip(groups, cats):
                col = VGroup(*[tab(label) for label in labels]).arrange(DOWN, buff=0.18)
                col.next_to(node, DOWN, buff=0.4)
                stem = Line(node.get_bottom(), col.get_top(), stroke_width=1.5, color=ORANGE)
                stems.add(stem)
                tabs.add(col)
            self.play(Create(stems), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for col in tabs for t in col], lag_ratio=0.4),
                      run_time=3.2)

            path = VMobject()
            path.set_points_smoothly([bot.get_center(), np.array([6.35, 0.6, 0]), np.array([6.1, -2.1, 0]),
                                      np.array([3.0, -2.45, 0]), np.array([0.0, -2.45, 0])])
            self.play(Rotate(bot, -PI / 2), run_time=0.5)
            trunk = Line(main.get_start(), np.array([xs[-1], 2.0, 0]), stroke_width=3, color=MUTED)
            self.play(MoveAlongPath(bot, path), ReplacementTransform(main, trunk), run_time=3.0)
            self.play(Rotate(bot, PI), run_time=0.6)

            agenda = T("A research agenda: the experiments are proposals", size=22, color=SOFT)
            agenda.next_to(bot, DOWN, buff=0.3)
            self.play(FadeIn(agenda), run_time=0.8)
            self.play(LaggedStart(*[Indicate(col, color=ORANGE, scale_factor=1.05) for col in tabs], lag_ratio=0.4),
                      run_time=2.0)
