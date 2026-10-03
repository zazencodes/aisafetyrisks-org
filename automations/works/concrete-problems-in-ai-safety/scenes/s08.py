# storyboard: 576e3f361a945303
from aisr_kit import *

# Roles from the video's visual language.
BROWN = "#9A6B45"      # messes
INTENT = "#8CC084"     # what the designer meant: green dashed
ORANGE = AMBER         # the problem tabs

OFFICE_CENTER = np.array([0.0, -0.35, 0.0])
PATH_Y = 0.6
STAGE = np.array([0.0, 0.1, 0.0])
STAGE_SCALE = 0.82


def gear(radius, teeth, color=GRAY):
    cogs = VGroup(*[
        Rectangle(width=radius * 0.4, height=radius * 0.34, stroke_width=0, fill_color=color, fill_opacity=1)
        .move_to(RIGHT * radius * 1.1)
        .rotate(TAU * i / teeth, about_point=ORIGIN)
        for i in range(teeth)
    ])
    body = Circle(radius=radius, stroke_color=color, stroke_width=2, fill_color=PANEL, fill_opacity=1)
    hub = Circle(radius=radius * 0.32, stroke_color=color, stroke_width=2)
    return VGroup(cogs, body, hub)


def hospital_cross():
    bars = VGroup(Rectangle(width=0.8, height=0.26, stroke_width=0, fill_color=SOFT, fill_opacity=1),
                  Rectangle(width=0.26, height=0.8, stroke_width=0, fill_color=SOFT, fill_opacity=1))
    frame = RoundedRectangle(corner_radius=0.14, width=1.1, height=1.1, stroke_color=GRAY, stroke_width=2)
    return VGroup(frame, bars)


def make_robot():
    body = RoundedRectangle(corner_radius=0.1, width=0.6, height=0.6, stroke_width=0,
                            fill_color=BLUE, fill_opacity=1)
    eye = Circle(radius=0.08, stroke_width=0, fill_color=WHITE, fill_opacity=1)
    eye.move_to(body.get_right() + LEFT * 0.13)
    pointer = Line(body.get_right(), body.get_right() + RIGHT * 0.28, stroke_width=4, color=BLUE)
    tip = eye.get_center()
    cone = Polygon(tip, tip + np.array([1.7, 0.75, 0]), tip + np.array([1.7, -0.75, 0]),
                   stroke_width=0, fill_color=WHITE, fill_opacity=0.08)
    robot = VGroup(cone, body, pointer, eye)
    robot.body, robot.cone = body, cone
    return robot


def make_score(slots, filled):
    label = T("Score", size=22, color=AMBER, weight=MEDIUM)
    pips = VGroup(*[Square(side_length=0.2, stroke_color=AMBER, stroke_width=2, fill_color=AMBER,
                           fill_opacity=1 if filled else 0)
                    for _ in range(slots)]).arrange(RIGHT, buff=0.08)
    pips.next_to(label, RIGHT, buff=0.2)
    return VGroup(label, pips)


def cross_at(c, r=0.3):
    return VGroup(Line(c + UL * r, c + DR * r, stroke_width=5, color=ROSE),
                  Line(c + UR * r, c + DL * r, stroke_width=5, color=ROSE))


def ended_office():
    """The opening office as s01 left it: messes cleaned, vase broken, messes hidden behind the desk."""
    floor = RoundedRectangle(corner_radius=0.3, width=11, height=5, stroke_color=GRAY, stroke_width=2,
                             fill_color=PANEL, fill_opacity=1).move_to(OFFICE_CENTER)
    desk = Rectangle(width=2.2, height=1.0, stroke_color=GRAY, stroke_width=2, fill_color=FAINT, fill_opacity=1)
    desk.move_to([1.8, -1.2, 0])
    hidden = VGroup(*[Dot([x, y, 0], radius=0.11, color=BROWN) for x, y in [(1.2, -2.3), (1.8, -2.42), (2.4, -2.28)]])
    vase = Circle(radius=0.26, stroke_color=ROSE, stroke_width=2, fill_color=ROSE, fill_opacity=1)
    vase.move_to([2.3, 1.03, 0]).stretch(0.55, 1)
    cross = cross_at(vase.get_center())
    robot = make_robot()
    robot.shift(np.array([3.4, PATH_Y, 0]) - robot.body.get_center())
    score = make_score(5, True)
    score.next_to(floor.get_corner(UR), DL, buff=0.3)
    office = VGroup(floor, desk, hidden, vase, cross, robot, score)
    office.floor, office.desk, office.hidden, office.vase = floor, desk, hidden, vase
    office.cross, office.robot, office.score = cross, robot, score
    return office


def problem_tab(label):
    return Node(label, color=ORANGE, height=0.7, size=32, fill=0.12)


def glance_icon(width=0.7, color=GRAY):
    outline = Ellipse(width=width, height=width * 0.5, stroke_color=color, stroke_width=2.5)
    pupil = Dot(radius=width * 0.11, color=color)
    return VGroup(outline, pupil)


def dashed_round_rect(width, height, center, color=INTENT, num_dashes=60):
    rect = RoundedRectangle(corner_radius=0.2, width=width, height=height,
                            stroke_color=color, stroke_width=3).move_to(center)
    return DashedVMobject(rect, num_dashes=num_dashes, dashed_ratio=0.55)


def stem(a, b):
    return Line(a, b, stroke_width=1.5, color=ORANGE)


class S08(NarratedScene):
    def construct(self):
        # ------------------------------------------------------------------ b01
        with self.beat("s08b01") as b:
            heading = Heading("Back to the office")
            tag = Tag("future_scenario")
            office = ended_office()
            office.scale(STAGE_SCALE, about_point=OFFICE_CENTER).move_to(STAGE)
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(office), run_time=1.2)

            # Side effects on the broken vase.
            t_side = problem_tab("Side effects")
            t_side.move_to(office.vase.get_center() + np.array([-2.6, -0.25, 0]))
            s_side = stem(t_side.get_right(), office.cross.get_left() + LEFT * 0.08)
            self.play(Indicate(office.cross, color=ROSE), run_time=0.8)
            self.play(Create(s_side), FadeIn(t_side, shift=RIGHT * 0.2), run_time=0.9)

            # Reward hacking on the gold score.
            t_hack = problem_tab("Reward hacking")
            t_hack.next_to(office.score, LEFT, buff=0.6)
            s_hack = stem(t_hack.get_right(), office.score.get_left() + LEFT * 0.08)
            self.play(Indicate(office.score, color=AMBER, scale_factor=1.1), run_time=0.8)
            self.play(Create(s_hack), FadeIn(t_hack, shift=DOWN * 0.2), run_time=0.9)

            # Scalable oversight: a quick grey glance over the hidden messes.
            glance = glance_icon(0.62).next_to(office.hidden, LEFT, buff=0.55)
            sweep = DashedLine(glance.get_right() + RIGHT * 0.05, office.hidden.get_left() + LEFT * 0.05,
                               stroke_width=2, color=GRAY, dash_length=0.08)
            self.play(FadeIn(glance, scale=0.6), run_time=0.6)
            self.play(Create(sweep), run_time=0.6)
            self.play(LaggedStart(*[Indicate(d, color="#C08A5E", scale_factor=1.5) for d in office.hidden],
                                  lag_ratio=0.3), run_time=0.9)
            t_over = problem_tab("Scalable oversight")
            t_over.next_to(glance, LEFT, buff=0.5)
            s_over = stem(t_over.get_right(), glance.get_left() + LEFT * 0.06)
            self.play(Create(s_over), FadeIn(t_over, shift=LEFT * 0.2), run_time=0.9)

            # Two more ways to fail slide in at the bottom edge.
            t_explore = problem_tab("Safe exploration")
            t_shift = problem_tab("Distributional shift")
            bottom = VGroup(t_explore, t_shift).arrange(RIGHT, buff=0.8)
            bottom.move_to([0, -2.95, 0])
            t_explore.shift(LEFT * 8)
            t_shift.shift(RIGHT * 8)
            self.play(t_explore.animate.shift(RIGHT * 8), t_shift.animate.shift(LEFT * 8), run_time=1.4)

        attached = VGroup(t_side, t_hack, t_over)
        tabs = [t_side, t_hack, t_over, t_explore, t_shift]
        tab_names = ["Side effects", "Reward hacking", "Scalable oversight", "Safe exploration",
                     "Distributional shift"]
        # ------------------------------------------------------------------ b02
        with self.beat("s08b02") as b:
            new_tag = Tag("author_interpretation")
            self.play(FadeOut(tag), FadeIn(new_tag),
                      FadeOut(VGroup(*tabs, s_side, s_hack, s_over, glance, sweep)), run_time=0.8)
            tag = new_tag

            centers = [np.array([x, 0.3, 0]) for x in (-4.2, 0.0, 4.2)]
            panels = [Panel(3.6, 2.5).move_to(c) for c in centers[1:]]
            self.play(office.animate.scale(3.5 / office.floor.width).move_to(centers[0]), run_time=1.4)

            g1 = gear(0.5, 10).move_to(centers[1] + np.array([-0.3, -0.15, 0]))
            g2 = gear(0.33, 7).move_to(centers[1] + np.array([0.55, 0.5, 0]))
            ind_label = T("Industrial", size=26, color=SOFT).next_to(panels[0], DOWN, buff=0.3)
            self.play(FadeIn(panels[0]), FadeIn(g1), FadeIn(g2), FadeIn(ind_label), run_time=0.9)
            self.play(Rotate(g1, -PI / 2, about_point=g1.get_center()),
                      Rotate(g2, PI * 0.75, about_point=g2.get_center()), run_time=1.0)

            plus = hospital_cross().move_to(centers[2])
            health_label = T("Health", size=26, color=SOFT).next_to(panels[1], DOWN, buff=0.3)
            self.play(FadeIn(panels[1]), FadeIn(plus), FadeIn(health_label), run_time=0.9)

            # Direct harm, then a justified loss of trust.
            harms = VGroup(cross_at(g1.get_center(), 0.26), cross_at(plus.get_center() + RIGHT * 0.9, 0.2))
            self.play(Indicate(office.cross, color=ROSE), Create(harms), run_time=1.0)
            trust = T("Loss of trust", size=28, color=ROSE)
            trust.move_to([0, 2.15, 0])
            self.play(FadeIn(trust, shift=DOWN * 0.15), run_time=0.8)
            self.wait(2.2)

            # One unified approach instead of ad hoc fixes.
            outline = dashed_round_rect(12.6, 3.9, np.array([0, -0.05, 0]), num_dashes=70)
            self.play(Create(outline), run_time=2.0)
            unified = T("Unified approach", size=28, color=INTENT, weight=MEDIUM)
            unified.next_to(outline, DOWN, buff=0.22)
            self.play(FadeIn(unified, shift=UP * 0.15), run_time=0.8)

            # Clear this beat's diagram as its narration ends, so the next beat opens on its own.
            stage2 = VGroup(office, panels[0], g1, g2, ind_label, panels[1], plus, health_label, harms,
                            trust, outline, unified)
            self.wait(b.duration - 11.8 - 0.6)
            self.play(FadeOut(stage2), run_time=0.6)

        # ------------------------------------------------------------------ b03
        with self.beat("s08b03") as b:
            new_tag = Tag("limitation")
            self.remove(tag)
            self.add(new_tag)
            tag = new_tag

            # One row per problem, large enough to read on a phone; each gets its "Proposal" tag beside it.
            tab_w = max(T(name, size=38).width for name in tab_names) + 0.6
            row = VGroup(*[Node(name, color=ORANGE, width=tab_w, height=0.74, size=38, fill=0.12)
                           for name in tab_names])
            props = VGroup(*[Node("Proposal", color=SOFT, height=0.66, size=34, fill=0.1) for _ in tab_names])
            for i, (t, p) in enumerate(zip(row, props)):
                y = 2.2 - 1.0 * i
                t.move_to([-0.25 - tab_w / 2, y, 0])
                p.move_to([0.25 + p.width / 2, y, 0])
            shift = -(row.get_left()[0] + props.get_right()[0]) / 2
            VGroup(row, props).shift(RIGHT * shift)
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in row], lag_ratio=0.15), run_time=1.4)
            self.play(LaggedStart(*[FadeIn(p, shift=LEFT * 0.15) for p in props], lag_ratio=0.2), run_time=1.6)

            none = T("No measured results", size=44, color=INK, weight=MEDIUM)
            none.move_to([0, -2.75, 0])
            source = Source(self.paper["short"])
            self.play(FadeIn(none), FadeIn(source), run_time=0.9)
            self.play(Indicate(none, color=SOFT, scale_factor=1.05), run_time=1.0)

        # ------------------------------------------------------------------ b04
        with self.beat("s08b04") as b:
            # Swap the tag cleanly: everything from s08b03 fades out fully before the new tag appears.
            new_tag = Tag("definition")
            self.play(FadeOut(tag), FadeOut(VGroup(row, props, none, source)), run_time=0.4)
            self.play(FadeIn(new_tag), run_time=0.4)
            tag = new_tag

            center = np.array([0, -0.3, 0])
            floor = RoundedRectangle(corner_radius=0.3, width=12.2, height=4.8, stroke_color=GRAY, stroke_width=2,
                                     fill_color=PANEL, fill_opacity=1).move_to(center)
            score = make_score(5, True)
            score.next_to(floor.get_corner(UR), DL, buff=0.3)
            robot = make_robot()
            robot.remove(robot.cone)
            robot.shift(center - robot.body.get_center())
            self.play(FadeIn(floor), FadeIn(score), FadeIn(robot), run_time=1.0)

            # Each arrow and its label arrive as the narration names that cause (pauses in the
            # recording: about 5.4 s, 7.5 s, 9.0 s and 11.5 s into the beat) and stay to the end.
            body = robot.body
            specs = [("Left something out", np.array([-3.25, 1.0, 0]), UP, body.get_corner(UL), 3.6),
                     ("Could be gamed", np.array([3.25, 1.0, 0]), UP, body.get_corner(UR), 0.5),
                     ("Too costly to check", np.array([-3.25, -2.0, 0]), DOWN, body.get_corner(DL), 0.6),
                     ("Risks and new places", np.array([3.25, -2.0, 0]), DOWN, body.get_corner(DR), 0.9)]
            arcs, labels = VGroup(), VGroup()
            for text, label_pos, side, end, lead in specs:
                label = T(text, size=36, color=ORANGE, weight=MEDIUM).move_to(label_pos)
                # The arrow starts just beyond the label's inner edge, on the robot's side.
                start = label.get_edge_center(-side) + (-side) * 0.22 + RIGHT * np.sign(-label_pos[0]) * 0.6
                angle = 0.5 if (side[1] > 0) == (label_pos[0] < 0) else -0.5
                arc = CurvedArrow(start, end + (start - end) / np.linalg.norm(start - end) * 0.12,
                                  angle=angle, color=ORANGE, stroke_width=3, tip_length=0.18)
                arcs.add(arc)
                labels.add(label)
                self.wait(lead)
                self.play(Create(arc), FadeIn(label), run_time=1.0)

            self.play(Indicate(body, color=ORANGE, scale_factor=1.15), run_time=0.5)
            meant = dashed_round_rect(12.8, 5.3, center, num_dashes=80)
            self.play(Create(meant), run_time=1.4)
