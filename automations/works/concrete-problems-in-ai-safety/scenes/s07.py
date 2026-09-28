# storyboard: e6ff7128c5935a62
from aisr_kit import *

# Roles from the video's visual language.
TRAIN = "#8CC084"    # training settings / safe: green
NEW = "#E0873A"      # new, unfamiliar settings: orange
HARM = "#E0564F"     # harm: red
MESS = "#8B5A2B"     # messes: brown dots

OFFICE_C = np.array([-3.3, -0.3, 0])
FACTORY_C = np.array([3.3, -0.3, 0])
FLOOR_W, FLOOR_H = 5.6, 3.6
LABEL_Y = 1.95


def make_robot(scale=1.0):
    body = RoundedRectangle(corner_radius=0.1, width=0.52, height=0.52, stroke_width=0,
                            fill_color=BLUE, fill_opacity=1)
    eye = Circle(radius=0.075, stroke_width=0, fill_color=WHITE, fill_opacity=1)
    eye.move_to(body.get_right() + LEFT * 0.12)
    pointer = Line(body.get_right(), body.get_right() + RIGHT * 0.2, stroke_width=3, color=INK)
    robot = VGroup(body, eye, pointer)
    robot.scale(scale)
    robot.set_z_index(5)
    return robot


def make_floor(center, width, height, border):
    floor = RoundedRectangle(corner_radius=0.3, width=width, height=height,
                             stroke_color=GRAY, stroke_width=3, fill_color=PANEL, fill_opacity=1)
    floor.move_to(center)
    edge = RoundedRectangle(corner_radius=0.38, width=width + 0.2, height=height + 0.2,
                            stroke_color=border, stroke_width=4)
    edge.move_to(center)
    return floor, edge


def make_machine(width, height):
    body = Rectangle(width=width, height=height, stroke_color=SOFT, stroke_width=2,
                     fill_color=FAINT, fill_opacity=1)
    gear = Circle(radius=min(width, height) * 0.22, stroke_color=MUTED, stroke_width=2)
    gear.move_to(body)
    machine = VGroup(body, gear)
    machine.set_z_index(3)
    return machine


def red_cross(size=0.5, width=6):
    a = Line(UL * size / 2, DR * size / 2, stroke_width=width, color=HARM)
    b = Line(UR * size / 2, DL * size / 2, stroke_width=width, color=HARM)
    cross = VGroup(a, b)
    cross.set_z_index(7)
    return cross


def clean_wave(center, width, amp=0.45):
    ax_left = center[0] - width / 2
    wave = FunctionGraph(lambda x: amp * np.sin(2 * PI * (x - ax_left) / 1.3),
                         x_range=[ax_left, ax_left + width], color=TRAIN, stroke_width=3)
    wave.shift(UP * center[1])
    return wave


def noisy_wave(center, width, amp=0.45):
    ax_left = center[0] - width / 2
    xs = np.linspace(ax_left, ax_left + width, 90)
    jitter = [0.32, -0.28, 0.18, -0.35, 0.25, -0.12, 0.3, -0.22, 0.1, -0.3]
    pts = []
    for i, x in enumerate(xs):
        y = amp * 0.7 * np.sin(2 * PI * (x - ax_left) / 1.3) + jitter[i % len(jitter)]
        pts.append([x, center[1] + y, 0])
    wave = VMobject(stroke_color=NEW, stroke_width=2.5).set_points_as_corners(pts)
    return wave


def bar_row(label, left_x, y, track_w, color):
    text = T(label, size=24, color=SOFT)
    text.move_to([left_x, y, 0], aligned_edge=LEFT)
    track_left = left_x + 1.75
    track = RoundedRectangle(corner_radius=0.08, width=track_w, height=0.3, stroke_color=FAINT,
                             stroke_width=1.5)
    track.move_to([track_left + track_w / 2, y, 0])
    bar = RoundedRectangle(corner_radius=0.08, width=track_w, height=0.3, stroke_width=0,
                           fill_color=color, fill_opacity=0.9)
    bar.move_to(track)
    return text, track, bar


def vertical_meter(bottom, height_full, color, width=0.4):
    track = RoundedRectangle(corner_radius=0.08, width=width, height=height_full, stroke_color=FAINT,
                             stroke_width=1.5)
    track.move_to(bottom + UP * height_full / 2)
    return track


def meter_fill(bottom, h, color, width=0.4):
    fill = RoundedRectangle(corner_radius=0.08, width=width, height=h, stroke_width=0,
                            fill_color=color, fill_opacity=0.9)
    fill.move_to(bottom + UP * h / 2)
    return fill


def noisy_card(center, size=1.3):
    card = RoundedRectangle(corner_radius=0.12, width=size, height=size, stroke_color=NEW,
                            stroke_width=3, fill_color=PANEL, fill_opacity=1)
    card.move_to(center)
    offsets = [(-0.35, 0.3), (0.2, 0.38), (0.38, -0.05), (-0.1, -0.02), (-0.4, -0.32), (0.15, -0.36),
               (0.05, 0.15), (-0.25, 0.05), (0.3, 0.2), (-0.05, -0.25)]
    specks = VGroup(*[Dot(center + np.array([dx, dy, 0]), radius=0.05, color=MUTED) for dx, dy in offsets])
    return VGroup(card, specks)


class S07(NarratedScene):
    def construct(self):
        # ------------------------------------------------------------------ b01
        with self.beat("s07b01") as b:
            heading = Heading("Unfamiliar places")
            tag = Tag("definition")
            source = Source(self.paper["short"])
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), run_time=0.8)

            office, office_edge = make_floor(OFFICE_C, FLOOR_W, FLOOR_H, TRAIN)
            messes = VGroup(*[Dot(OFFICE_C + np.array(p), radius=0.09, color=MESS)
                              for p in [(-1.4, 0.9, 0), (0.6, 1.0, 0), (1.5, -0.4, 0), (-0.5, -1.0, 0)]])
            robot_home = OFFICE_C + np.array([-1.6, -0.2, 0])
            robot = make_robot().move_to(robot_home)
            self.play(Create(office), FadeIn(messes), FadeIn(robot), run_time=1.0)

            train_label = T("Training", size=26, color=TRAIN, weight=MEDIUM)
            train_label.move_to([OFFICE_C[0], LABEL_Y, 0])
            self.play(Create(office_edge), FadeIn(train_label), run_time=0.9)

            # The robot's usual cleaning sweep inside the office.
            sweep = VMobject().set_points_as_corners([
                robot_home, OFFICE_C + np.array([1.5, -0.2, 0]), OFFICE_C + np.array([1.5, -0.9, 0]),
                OFFICE_C + np.array([-1.6, -0.9, 0]), robot_home,
            ])
            sweep_trace = DashedVMobject(sweep, num_dashes=40, dashed_ratio=0.5)
            sweep_trace.set_stroke(color=BLUE, width=2, opacity=0.6)
            sweep_trace.set_z_index(2)
            self.play(Create(sweep_trace), MoveAlongPath(robot, sweep), run_time=2.0, rate_func=linear)

            # The factory floor slides in on the right.
            factory, factory_edge = make_floor(FACTORY_C, FLOOR_W, FLOOR_H, NEW)
            m1 = make_machine(1.5, 1.0).move_to(FACTORY_C + np.array([0.9, -0.2, 0]))
            m2 = make_machine(1.1, 1.3).move_to(FACTORY_C + np.array([-1.3, 0.8, 0]))
            m3 = make_machine(1.2, 0.8).move_to(FACTORY_C + np.array([-0.9, -1.15, 0]))
            factory_group = VGroup(factory, factory_edge, m1, m2, m3)
            deploy_label = T("Deployment", size=26, color=NEW, weight=MEDIUM)
            deploy_label.move_to([FACTORY_C[0], LABEL_Y, 0])
            factory_group.shift(RIGHT * 4)
            self.play(factory_group.animate.shift(LEFT * 4), FadeIn(deploy_label), run_time=1.2)

            # The robot moves across and runs its usual path into a machine.
            entry = FACTORY_C + np.array([-2.2, -0.2, 0])
            self.play(FadeOut(sweep_trace), robot.animate.move_to(entry), run_time=1.2)
            crash_point = m1.get_left() + LEFT * 0.3
            usual = DashedLine(entry, m1.get_left(), dash_length=0.12, color=BLUE, stroke_width=2)
            usual.set_z_index(2)
            self.play(Create(usual), robot.animate.move_to(crash_point), run_time=1.0, rate_func=linear)
            self.play(m1[0].animate.set_fill(HARM, opacity=0.8).set_stroke(HARM),
                      Flash(m1.get_left(), color=HARM, line_length=0.2), run_time=0.6)
            cross = red_cross(0.45).move_to(m1.get_left() + UP * 0.7)
            self.play(Create(cross), run_time=0.4)

            concept = T("Distributional shift", size=30, color=INK, weight=SEMIBOLD)
            concept.move_to([0, -2.85, 0])
            self.play(FadeIn(concept, shift=UP * 0.15), run_time=0.6)

        # ------------------------------------------------------------------ b02
        with self.beat("s07b02") as b:
            # Keep the factory and robot for the end; set them aside for now.
            floors = VGroup(office, office_edge, messes, train_label)
            factory_scene = VGroup(factory_group, deploy_label, usual, cross, robot)
            self.play(FadeOut(floors), FadeOut(factory_scene), FadeOut(concept), run_time=0.7)

            panel_w, panel_h = 5.2, 1.9
            clean_c = np.array([-3.3, 0.55, 0])
            noisy_c = np.array([3.3, 0.55, 0])
            clean_panel = RoundedRectangle(corner_radius=0.2, width=panel_w, height=panel_h,
                                           stroke_color=TRAIN, stroke_width=3, fill_color=PANEL,
                                           fill_opacity=1).move_to(clean_c)
            noisy_panel = RoundedRectangle(corner_radius=0.2, width=panel_w, height=panel_h,
                                           stroke_color=NEW, stroke_width=3, fill_color=PANEL,
                                           fill_opacity=1).move_to(noisy_c)
            clean_label = T("Clean speech", size=26, color=TRAIN, weight=MEDIUM)
            clean_label.move_to([clean_c[0], LABEL_Y, 0])
            noisy_label = T("Noisy speech", size=26, color=NEW, weight=MEDIUM)
            noisy_label.move_to([noisy_c[0], LABEL_Y, 0])
            self.play(FadeIn(clean_panel), FadeIn(noisy_panel), FadeIn(clean_label), FadeIn(noisy_label),
                      run_time=0.8)
            c_wave = clean_wave(clean_c, panel_w - 0.8)
            n_wave = noisy_wave(noisy_c, panel_w - 0.8)
            self.play(Create(c_wave), Create(n_wave), run_time=1.6, rate_func=linear)

            track_w = 3.0
            rows = VGroup()
            bars = {}
            for side, c in (("clean", clean_c), ("noisy", noisy_c)):
                left_x = c[0] - panel_w / 2 + 0.1
                for name, y, color in (("Accuracy", -1.25, BLUE), ("Confidence", -2.05, AMBER)):
                    text, track, bar = bar_row(name, left_x, y, track_w, color)
                    rows.add(text, track)
                    bars[(side, name)] = bar
            self.play(FadeIn(rows), run_time=0.6)
            grow = [GrowFromEdge(bar, LEFT) for bar in bars.values()]
            self.play(LaggedStart(*grow, lag_ratio=0.15), run_time=1.4)

            acc = bars[("noisy", "Accuracy")]
            conf = bars[("noisy", "Confidence")]
            acc_left = acc.get_left()
            self.play(acc.animate.stretch_to_fit_width(track_w * 0.22).align_to(acc_left, LEFT).set_fill(HARM),
                      run_time=1.6)
            self.play(Indicate(conf, color=AMBER, scale_factor=1.08), run_time=1.0)

        # ------------------------------------------------------------------ b03
        with self.beat("s07b03") as b:
            tag_b3 = Tag("threat_model")
            speech = VGroup(clean_panel, noisy_panel, clean_label, noisy_label, c_wave, n_wave, rows,
                            *bars.values())
            self.play(ReplacementTransform(tag, tag_b3), FadeOut(speech), run_time=0.8)
            tag = tag_b3

            card = noisy_card(np.array([-5.1, 0.7, 0]))
            classifier = Node("Classifier", color=GRAY, width=2.6).move_to([-1.8, 0.7, 0])
            in_link = Link(card, classifier, color=MUTED)
            self.play(FadeIn(card), run_time=0.6)
            self.play(GrowArrow(in_link.arrow), FadeIn(classifier), run_time=0.9)

            output = Node("Wrong diagnosis", color=GRAY, width=3.0).move_to([2.6, 0.7, 0])
            out_link = Link(classifier, output, color=MUTED)
            self.play(GrowArrow(out_link.arrow), FadeIn(output), run_time=0.9)

            meter_bottom = np.array([5.25, -0.3, 0])
            meter_h = 2.0
            meter_track = vertical_meter(meter_bottom, meter_h, AMBER)
            conf_fill = meter_fill(meter_bottom, meter_h * 0.93, AMBER)
            conf_label = T("Confidence", size=22, color=SOFT).next_to(meter_track, DOWN, buff=0.2)
            self.play(FadeIn(meter_track), FadeIn(conf_label), run_time=0.5)
            self.play(GrowFromEdge(conf_fill, DOWN), run_time=1.0)

            review = Node("Human review", color=GRAY, width=2.8).move_to([-1.8, -2.0, 0])
            review_link = DashedLine(classifier.get_bottom() + DOWN * 0.1, review.get_top() + UP * 0.1,
                                     dash_length=0.12, color=FAINT, stroke_width=3)
            review_tip = Triangle(stroke_width=0, fill_color=FAINT, fill_opacity=1).scale(0.1).rotate(PI)
            review_tip.next_to(review.get_top(), UP, buff=0.05)
            not_flagged = T("Not flagged", size=24, color=MUTED).next_to(review_link, RIGHT, buff=0.3)
            self.play(FadeIn(review), Create(review_link), FadeIn(review_tip), run_time=1.0)
            self.play(FadeIn(not_flagged), run_time=0.5)

            self.play(output.box.animate.set_stroke(HARM).set_fill(HARM, opacity=0.18),
                      output.label.animate.set_color(HARM), run_time=0.8)
            self.play(Indicate(output, color=HARM, scale_factor=1.05), run_time=0.8)

        # ------------------------------------------------------------------ b04
        with self.beat("s07b04") as b:
            tag_b4 = Tag("method")
            self.play(ReplacementTransform(tag, tag_b4), run_time=0.5)
            tag = tag_b4

            short_fill = meter_fill(meter_bottom, meter_h * 0.2, AMBER)
            knows = Node("Knows when it is wrong", color=TRAIN, width=3.4, size=22)
            knows.move_to(output).align_to(output, LEFT)
            self.play(Transform(conf_fill, short_fill),
                      ReplacementTransform(output, knows), run_time=1.0)

            ask = T("Ask a person", size=24, color=TRAIN, weight=MEDIUM).move_to(not_flagged)
            self.play(review_link.animate.set_color(TRAIN),
                      review_tip.animate.set_fill(TRAIN),
                      review.box.animate.set_stroke(TRAIN).set_fill(TRAIN, opacity=0.14),
                      ReplacementTransform(not_flagged, ask), run_time=1.0)

            # The robot in the factory stops and asks.
            small_c = np.array([3.4, -2.05, 0])
            mini_factory, mini_edge = make_floor(small_c, 3.2, 1.4, NEW)
            mini_machine = make_machine(0.9, 0.7).move_to(small_c + RIGHT * 0.8)
            robot.scale(0.8).move_to(small_c + LEFT * 1.1)
            self.play(FadeIn(mini_factory), FadeIn(mini_edge), FadeIn(mini_machine), FadeIn(robot),
                      run_time=0.7)
            self.play(robot.animate.shift(RIGHT * 0.55), run_time=0.8, rate_func=rush_from)
            question = T("?", size=34, color=TRAIN, weight=SEMIBOLD).next_to(robot, UP, buff=0.1)
            question.set_z_index(8)
            self.play(FadeIn(question, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(question, color=TRAIN, scale_factor=1.3), run_time=0.8)
