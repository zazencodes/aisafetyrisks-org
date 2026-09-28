# storyboard: d0680af192d07c58
from aisr_kit import *

# Roles from the video's visual language.
INTENT = "#8CC084"   # what the designer meant: green dashed
HARM = "#E0564F"     # harm: red
MESS = "#8B5A2B"     # messes: brown dots
RUG = SAND

OFFICE_C = np.array([-1.8, -0.3, 0])
OFFICE_W, OFFICE_H = 7.0, 4.2
COL_X = 4.4          # right-hand column for the clock, the glance icon and labels
ROW_Y = -0.3
N_RUNS = 10
GOLD_RUNS = (2, 7)
RUG_C = np.array([-1.3, -0.5, 0])


def make_robot():
    body = RoundedRectangle(corner_radius=0.1, width=0.52, height=0.52, stroke_width=0,
                            fill_color=BLUE, fill_opacity=1)
    eye = Circle(radius=0.075, stroke_width=0, fill_color=WHITE, fill_opacity=1)
    eye.move_to(body.get_right() + LEFT * 0.12)
    pointer = Line(body.get_right(), body.get_right() + RIGHT * 0.2, stroke_width=3, color=INK)
    return VGroup(body, eye, pointer)


def make_floor():
    return RoundedRectangle(corner_radius=0.3, width=OFFICE_W, height=OFFICE_H, stroke_color=GRAY,
                            stroke_width=3, fill_color=PANEL, fill_opacity=1).move_to(OFFICE_C)


def score_counter(width=0.9, fill=0.2):
    pill = RoundedRectangle(corner_radius=0.1, width=width, height=0.34, stroke_color=AMBER,
                            stroke_width=2, fill_color=AMBER, fill_opacity=fill)
    ticks = VGroup(*[Line(UP * 0.09, DOWN * 0.09, stroke_width=3, color=AMBER) for _ in range(4)])
    ticks.arrange(RIGHT, buff=0.1).move_to(pill)
    return VGroup(pill, ticks)


def office_score():
    return score_counter().move_to(OFFICE_C + np.array([OFFICE_W / 2 - 0.75, OFFICE_H / 2 - 0.45, 0]))


def glance_icon(width=0.7, color=SOFT):
    outline = Ellipse(width=width, height=width * 0.5, stroke_color=color, stroke_width=2.5)
    pupil = Dot(radius=width * 0.11, color=color)
    return VGroup(outline, pupil)


def tick_mark(size=0.34, color=INTENT):
    return VMobject(stroke_color=color, stroke_width=5).set_points_as_corners(
        [np.array([-0.5, 0.0, 0]) * size, np.array([-0.15, -0.4, 0]) * size, np.array([0.55, 0.45, 0]) * size])


def magnifier():
    ring = Circle(radius=0.16, stroke_color=INTENT, stroke_width=3)
    handle = Line(ring.point_at_angle(-PI / 4), ring.point_at_angle(-PI / 4) + np.array([0.15, -0.15, 0]),
                  stroke_width=4, color=INTENT)
    return VGroup(ring, handle)


def mini_office(size=0.8):
    floor = RoundedRectangle(corner_radius=0.08, width=size, height=size, stroke_color=GRAY,
                             stroke_width=2, fill_color=PANEL, fill_opacity=1)
    bot = RoundedRectangle(corner_radius=0.03, width=size * 0.2, height=size * 0.2, stroke_width=0,
                           fill_color=BLUE, fill_opacity=1).move_to(floor.get_center() + LEFT * size * 0.18)
    dot = Dot(floor.get_center() + RIGHT * size * 0.2 + DOWN * size * 0.15, radius=0.045, color=MESS)
    return VGroup(floor, bot, dot)


def run_row():
    row = VGroup(*[mini_office() for _ in range(N_RUNS)]).arrange(RIGHT, buff=0.25)
    row.move_to([0, ROW_Y, 0])
    return row


def dashed_round_rect(width, height, center, color, num_dashes=40):
    rect = RoundedRectangle(corner_radius=0.14, width=width, height=height,
                            stroke_color=color, stroke_width=3).move_to(center)
    return DashedVMobject(rect, num_dashes=num_dashes, dashed_ratio=0.55)


def make_rug():
    return RoundedRectangle(corner_radius=0.06, width=1.4, height=0.9, stroke_color=SOFT, stroke_width=1.5,
                            fill_color=RUG, fill_opacity=1).move_to(RUG_C)


class S05(NarratedScene):
    def construct(self):
        # ------------------------------------------------------------------ b01
        with self.beat("s05b01") as b:
            heading = Heading("When checking is too costly")
            tag = Tag("definition")
            source = Source(self.paper["short"])
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), run_time=0.8)

            floor = make_floor()
            score = office_score()
            self.play(Create(floor), FadeIn(score), run_time=1.0)

            walk = RoundedRectangle(corner_radius=0.4, width=OFFICE_W - 1.0, height=OFFICE_H - 1.0)
            walk.move_to(OFFICE_C)
            person = Circle(radius=0.2, stroke_width=0, fill_color=GRAY, fill_opacity=1)
            lens = magnifier().next_to(person, RIGHT, buff=0.05).shift(UP * 0.1)
            inspector = VGroup(person, lens).move_to(walk.point_from_proportion(0))

            clock_c = np.array([COL_X, 0.7, 0])
            face = Circle(radius=0.5, stroke_color=SOFT, stroke_width=3).move_to(clock_c)
            marks = VGroup(*[Line(clock_c + 0.4 * np.array([np.cos(a), np.sin(a), 0]),
                                  clock_c + 0.5 * np.array([np.cos(a), np.sin(a), 0]),
                                  stroke_width=2, color=MUTED) for a in np.linspace(0, TAU, 12, endpoint=False)])
            hand = Line(clock_c, clock_c + UP * 0.38, stroke_width=4, color=INK)
            hub = Dot(clock_c, radius=0.05, color=INK)
            hours_label = T("Hours of inspection", size=26, color=INTENT, weight=MEDIUM)
            hours_label.next_to(face, DOWN, buff=0.35)
            self.play(FadeIn(inspector, scale=0.7), FadeIn(VGroup(face, marks, hand, hub)),
                      FadeIn(hours_label, shift=UP * 0.1), run_time=0.8)
            self.play(MoveAlongPath(inspector, walk), Rotate(hand, angle=-TAU * 5, about_point=clock_c),
                      run_time=5.5, rate_func=linear)

            # Many practice runs, each only glanced at.
            row = run_row()
            self.play(FadeOut(inspector), FadeOut(score), FadeOut(VGroup(face, marks, hand, hub)),
                      FadeOut(hours_label), run_time=0.6)
            self.play(ReplacementTransform(floor, row[0]), run_time=1.1)
            self.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.2) for m in row[1:]], lag_ratio=0.12),
                      run_time=1.2)
            glances = VGroup(*[glance_icon(0.46).next_to(m, UP, buff=0.2) for m in row])
            dirt_label = T("Visible dirt?", size=26, color=SOFT).next_to(glances, UP, buff=0.4)
            self.play(FadeIn(dirt_label), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(g, scale=0.6) for g in glances], lag_ratio=0.18), run_time=1.6)
            oversight = T("Scalable oversight", size=34, color=INK, weight=SEMIBOLD)
            oversight.next_to(row, DOWN, buff=0.8)
            self.play(FadeIn(oversight, shift=UP * 0.15), run_time=0.8)

        # ------------------------------------------------------------------ b02
        with self.beat("s05b02") as b:
            floor = make_floor()
            score = office_score()
            rug = make_rug()
            intent = dashed_round_rect(1.9, 1.4, RUG_C, INTENT)
            mess = Dot(RUG_C + LEFT * 2.3, radius=0.12, color=MESS)
            robot = make_robot().next_to(mess, LEFT, buff=0.08)
            mess.set_z_index(2)
            rug.set_z_index(3)
            intent.set_z_index(3)
            robot.set_z_index(4)
            self.play(FadeOut(VGroup(row, glances, dirt_label, oversight)), run_time=0.6)
            self.play(FadeIn(floor), FadeIn(score), FadeIn(rug), Create(intent), FadeIn(mess),
                      FadeIn(robot), run_time=1.0)

            eye = glance_icon(0.8).move_to([COL_X, 0.6, 0])
            look_label = T("Quick look", size=26, color=SOFT).next_to(eye, DOWN, buff=0.35)
            self.play(FadeIn(eye), FadeIn(look_label), run_time=0.6)

            edge = rug.get_left()[0] + 0.1
            push = VGroup(robot, mess)
            self.play(push.animate.shift(RIGHT * (edge - mess.get_center()[0])), run_time=1.6)
            under = RUG_C + DOWN * 0.15
            self.play(mess.animate.move_to(under), robot.animate.shift(RIGHT * 0.2), run_time=0.7)

            tick = tick_mark().next_to(eye, RIGHT, buff=0.25)
            self.play(Create(tick), run_time=0.6)
            self.play(intent.animate.set_stroke(HARM), run_time=0.4)
            self.play(Indicate(intent, color=HARM, scale_factor=1.08), run_time=0.8)
            hidden_label = T("Hidden mess", size=26, color=HARM, weight=MEDIUM)
            hidden_label.next_to(intent, DOWN, buff=0.3)
            self.play(FadeIn(hidden_label, shift=UP * 0.1), run_time=0.5)
            office = VGroup(floor, score, mess, rug, intent, robot)

        # ------------------------------------------------------------------ b03
        with self.beat("s05b03") as b:
            tag_b3 = Tag("method")
            self.play(ReplacementTransform(tag, tag_b3), FadeOut(office), FadeOut(hidden_label),
                      FadeOut(VGroup(eye, tick, look_label)), run_time=0.8)
            tag = tag_b3

            row = run_row().shift(UP * 0.6)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in row], lag_ratio=0.1), run_time=1.2)

            gold = [row[i] for i in GOLD_RUNS]
            grey = [row[i] for i in range(N_RUNS) if i not in GOLD_RUNS]
            gold_scores = VGroup(*[score_counter(width=0.62, fill=0.35).scale(0.9).next_to(m, UP, buff=0.18)
                                   for m in gold])
            self.play(*[m[0].animate.set_fill(AMBER, opacity=0.35).set_stroke(AMBER) for m in gold],
                      *[m[0].animate.set_stroke(MUTED) for m in grey],
                      LaggedStart(*[FadeIn(s, shift=DOWN * 0.1) for s in gold_scores], lag_ratio=0.3),
                      run_time=1.2)

            key_seen = VGroup(
                RoundedRectangle(corner_radius=0.05, width=0.3, height=0.3, stroke_color=AMBER, stroke_width=2,
                                 fill_color=AMBER, fill_opacity=0.35),
                T("Reward seen", size=24, color=AMBER),
            ).arrange(RIGHT, buff=0.2)
            key_hidden = VGroup(
                RoundedRectangle(corner_radius=0.05, width=0.3, height=0.3, stroke_color=MUTED, stroke_width=2,
                                 fill_color=PANEL, fill_opacity=1),
                T("Reward hidden", size=24, color=SOFT),
            ).arrange(RIGHT, buff=0.2)
            legend = VGroup(key_seen, key_hidden).arrange(RIGHT, buff=1.0).move_to([0, 1.95, 0])
            self.play(FadeIn(legend), run_time=0.7)

            brace = Brace(row, DOWN, buff=0.2, color=MUTED)
            judged = T("Judged on all", size=26, color=INK, weight=MEDIUM).next_to(brace, DOWN, buff=0.2)
            self.play(GrowFromCenter(brace), FadeIn(judged), run_time=1.0)

            # Every run counts: sweep along the whole row under the brace.
            self.play(LaggedStart(*[Indicate(m, color=INK, scale_factor=1.08) for m in row], lag_ratio=0.12),
                      run_time=2.4)

        # ------------------------------------------------------------------ b05
        with self.beat("s05b05") as b:
            tag_b5 = Tag("hypothesis")
            self.play(ReplacementTransform(tag, tag_b5),
                      FadeOut(VGroup(row, gold_scores, brace, judged, legend)),
                      run_time=0.8)
            tag = tag_b5

            intent.set_stroke(INTENT)
            eye = glance_icon(0.8).move_to([COL_X, 0.6, 0])
            tick = tick_mark().next_to(eye, RIGHT, buff=0.25)
            self.play(FadeIn(office), FadeIn(eye), FadeIn(tick), run_time=1.0)

            self.play(rug.animate.stretch(0.45, 1, about_edge=UP), run_time=1.4)
            question = T("?", size=64, color=AMBER, weight=SEMIBOLD).next_to(intent, UP, buff=0.25)
            self.play(FadeIn(question, scale=0.6), Indicate(mess, color=HARM, scale_factor=1.4), run_time=1.0)

            link = DashedLine(eye.get_left() + LEFT * 0.1, score.get_right() + RIGHT * 0.1, stroke_width=2.5,
                              color=INTENT, dash_length=0.12)
            link.set_opacity(0.6)
            check_label = T("Rare true check", size=26, color=INTENT, weight=MEDIUM)
            check_label.next_to(eye, DOWN, buff=0.35)
            self.play(Create(link), FadeIn(check_label), run_time=1.4)
            transparency = T("Transparency", size=28, color=INK, weight=MEDIUM)
            transparency.next_to(intent, DOWN, buff=0.35)
            self.play(FadeIn(transparency, shift=UP * 0.1), run_time=0.7)
