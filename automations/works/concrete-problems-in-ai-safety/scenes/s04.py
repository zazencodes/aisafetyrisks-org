# storyboard: 45f7445032ea0a9a
from aisr_kit import *

# Roles from the video's visual language.
BROWN = "#9A6B45"    # messes
INTENT = "#8CC084"   # what the designer meant: green dashed
WRITTEN = "#E0873A"  # the goal as written: solid orange
WRITTEN_TEXT = "#F5A862"  # lighter orange for written-goal text, for contrast on the dark ground
HARM = "#E0564F"     # harm: red

OFFICE_C = np.array([-1.7, -0.35, 0])
OFFICE_W, OFFICE_H = 8.0, 4.6
COL_X = 4.65  # right-hand column for labels


def make_robot(scale=1.0):
    body = RoundedRectangle(corner_radius=0.1, width=0.6, height=0.6, stroke_width=0,
                            fill_color=BLUE, fill_opacity=1)
    eye = Circle(radius=0.08, stroke_width=0, fill_color=WHITE, fill_opacity=1)
    eye.move_to(body.get_right() + LEFT * 0.13)
    pointer = Line(body.get_right(), body.get_right() + RIGHT * 0.28, stroke_width=4, color=BLUE)
    tip = eye.get_center()
    cone = Polygon(tip, tip + np.array([1.7, 0.75, 0]), tip + np.array([1.7, -0.75, 0]),
                   stroke_width=0, fill_color=WHITE, fill_opacity=0.08)
    robot = VGroup(cone, body, pointer, eye)
    robot.body, robot.eye, robot.cone, robot.pointer = body, eye, cone, pointer
    robot.scale(scale)
    return robot


def place_robot(robot, point):
    robot.shift(np.array(point) - robot.body.get_center())
    return robot


def make_score(slots):
    label = T("Score", size=22, color=AMBER, weight=MEDIUM)
    pips = VGroup(*[Square(side_length=0.2, stroke_color=AMBER, stroke_width=2, fill_color=AMBER,
                           fill_opacity=0) for _ in range(slots)]).arrange(RIGHT, buff=0.08)
    pips.next_to(label, RIGHT, buff=0.2)
    inner = VGroup(label, pips)
    frame = RoundedRectangle(corner_radius=0.12, width=inner.width + 0.4, height=0.5, stroke_color=AMBER,
                             stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to(inner)
    score = VGroup(frame, label, pips)
    score.frame, score.label, score.pips = frame, label, pips
    return score


def fill_pips(pips, upto):
    return [p.animate.set_fill(AMBER, opacity=1 if i < upto else 0) for i, p in enumerate(pips)]


def dashed_round_rect(width, height, center, color, num_dashes=70):
    rect = RoundedRectangle(corner_radius=0.18, width=width, height=height,
                            stroke_color=color, stroke_width=3).move_to(center)
    return DashedVMobject(rect, num_dashes=num_dashes, dashed_ratio=0.55)


def make_clock(center, radius=0.45, color=INTENT):
    face = Circle(radius=radius, stroke_color=color, stroke_width=3).move_to(center)
    hour = Line(center, center + UP * radius * 0.5, stroke_width=3, color=color)
    minute = Line(center, center + RIGHT * radius * 0.7, stroke_width=3, color=color)
    return VGroup(face, hour, minute)


def make_circuit(center):
    c = np.array(center)
    pts = [c + np.array(p) for p in [(-0.8, 0.35, 0), (0.0, 0.35, 0), (0.8, 0.35, 0),
                                     (-0.8, -0.35, 0), (0.0, -0.35, 0), (0.8, -0.35, 0)]]
    wires = VGroup(*[Line(pts[a], pts[b], stroke_width=2.5, color=SOFT)
                     for a, b in [(0, 1), (1, 2), (3, 4), (4, 5), (0, 3), (1, 4), (2, 5)]])
    nodes = VGroup(*[Dot(p, radius=0.07, color=WRITTEN) for p in pts])
    return VGroup(wires, nodes)


def make_computer(center):
    c = np.array(center)
    screen = RoundedRectangle(corner_radius=0.06, width=1.1, height=0.75, stroke_color=GRAY,
                              stroke_width=2.5, fill_color="#2A2F36", fill_opacity=1).move_to(c)
    stand = Line(c + DOWN * 0.375, c + DOWN * 0.6, stroke_width=4, color=GRAY)
    base = Line(c + DOWN * 0.6 + LEFT * 0.3, c + DOWN * 0.6 + RIGHT * 0.3, stroke_width=4, color=GRAY)
    return VGroup(screen, stand, base)


def wave(start, end, amp=0.1, cycles=4, color=SOFT):
    start, end = np.array(start), np.array(end)
    d = end - start
    n = np.array([-d[1], d[0], 0]) / np.linalg.norm(d)
    return ParametricFunction(lambda t: start + d * t + n * amp * np.sin(TAU * cycles * t),
                              t_range=[0, 1], stroke_width=2.5, color=color)


def make_bottle():
    body = RoundedRectangle(corner_radius=0.08, width=0.42, height=0.7, stroke_width=0,
                            fill_color=WHITE, fill_opacity=0.92)
    neck = Rectangle(width=0.16, height=0.2, stroke_width=0, fill_color=WHITE, fill_opacity=0.92)
    neck.next_to(body, UP, buff=0)
    return VGroup(body, neck)


def make_drain(center, radius=0.32):
    ring = Circle(radius=radius, stroke_color=GRAY, stroke_width=3, fill_color="#1A1D22",
                  fill_opacity=1).move_to(center)
    bars = VGroup(*[Line(center + LEFT * radius * 0.7 + UP * dy, center + RIGHT * radius * 0.7 + UP * dy,
                         stroke_width=2, color=GRAY) for dy in (-0.12, 0.0, 0.12)])
    return VGroup(ring, bars)


def pill(text, color):
    label = T(text, size=20, color=color, weight=MEDIUM)
    box = RoundedRectangle(corner_radius=0.18, width=label.width + 0.4, height=0.42,
                           stroke_color=color, stroke_width=1.5, fill_color=PANEL, fill_opacity=1)
    box.move_to(label)
    return VGroup(box, label)


def agent_square(size, detail):
    body = RoundedRectangle(corner_radius=size * 0.15, width=size, height=size, stroke_width=0,
                            fill_color=BLUE, fill_opacity=1)
    n = detail
    step = size / (n + 1)
    lines = VGroup()
    for i in range(1, n + 1):
        off = -size / 2 + i * step
        lines.add(Line(body.get_center() + np.array([off, -size / 2 + 0.06, 0]),
                       body.get_center() + np.array([off, size / 2 - 0.06, 0]),
                       stroke_width=1.5, color="#9FC3EB"))
        lines.add(Line(body.get_center() + np.array([-size / 2 + 0.06, off, 0]),
                       body.get_center() + np.array([size / 2 - 0.06, off, 0]),
                       stroke_width=1.5, color="#9FC3EB"))
    return VGroup(body, lines)


def crack(center, w=0.36):
    c = np.array(center)
    pts = [c + np.array([x, y, 0]) for x, y in
           [(-w / 2, 0), (-w / 6, 0.07), (0, -0.07), (w / 6, 0.07), (w / 2, 0)]]
    return VMobject(stroke_color=HARM, stroke_width=3).set_points_as_corners(pts)


def make_bell(center):
    c = np.array(center)
    dome = Arc(radius=0.2, start_angle=0, angle=PI, stroke_width=0, fill_color=AMBER,
               fill_opacity=1, arc_center=c)
    rim = Line(c + LEFT * 0.26, c + RIGHT * 0.26, stroke_width=4, color=AMBER)
    clapper = Dot(c + DOWN * 0.08, radius=0.05, color=AMBER)
    return VGroup(dome, rim, clapper)


class S04(NarratedScene):
    def construct(self):
        # ------------------------------------------------------------------ b01
        with self.beat("s04b01") as b:
            heading = Heading("When the goal can be gamed")
            tag = Tag("definition")
            source = Source(self.paper["short"])
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), run_time=0.7)

            floor = RoundedRectangle(corner_radius=0.3, width=OFFICE_W, height=OFFICE_H,
                                     stroke_color=GRAY, stroke_width=2, fill_color=PANEL,
                                     fill_opacity=1).move_to(OFFICE_C)
            messes = VGroup(*[Dot([x, y, 0], radius=0.11, color=BROWN) for x, y in
                              [(-3.6, 0.9), (-2.4, -1.4), (-1.0, 0.6), (0.0, -0.9), (1.1, 0.2)]])
            robot = place_robot(make_robot(), [-4.9, -0.3, 0])
            robot.set_z_index(3)
            score = make_score(5)
            score.move_to(floor.get_corner(UR) + np.array([-score.width / 2 - 0.25, -0.45, 0]))
            self.play(FadeIn(floor), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in messes], lag_ratio=0.2),
                      FadeIn(robot), FadeIn(score), run_time=1.0)

            reward = T("Reward:\nsee no mess", size=40, color=WRITTEN_TEXT, weight=SEMIBOLD)
            reward.move_to([COL_X, 1.2, 0])
            self.play(FadeIn(reward, shift=LEFT * 0.2), run_time=0.5)

            eye_open = robot.eye.copy()
            shut = Line(robot.eye.get_left() + LEFT * 0.02, robot.eye.get_right() + RIGHT * 0.02,
                        stroke_width=3, color=WHITE)
            self.play(Transform(robot.eye, shut), robot.cone.animate.set_fill(opacity=0), run_time=0.8)
            self.play(*fill_pips(score.pips, 5), run_time=0.9)
            self.play(Indicate(messes, color=BROWN, scale_factor=1.3), run_time=0.7)

            reward2 = T("Reward:\nclean messes", size=40, color=WRITTEN_TEXT, weight=SEMIBOLD)
            reward2.move_to(reward)
            self.play(FadeOut(reward), Transform(robot.eye, eye_open),
                      robot.cone.animate.set_fill(opacity=0.08), run_time=0.4)
            self.play(FadeIn(reward2), *fill_pips(score.pips, 2), run_time=0.4)
            reward = reward2

            new_mess = Dot(robot.body.get_center() + LEFT * 0.55, radius=0.11, color=BROWN)
            new_mess.set_z_index(2)
            self.play(robot.animate.shift(RIGHT * 0.55), FadeIn(new_mess, scale=0.4), run_time=0.7)
            self.play(robot.animate.shift(LEFT * 0.55), run_time=0.6)
            self.play(FadeOut(new_mess, scale=0.3), *fill_pips(score.pips, 3), run_time=0.5)
            self.play(Indicate(score.pips[2], color=AMBER, scale_factor=1.4), run_time=0.5)

        # ------------------------------------------------------------------ b02
        with self.beat("s04b02") as b:
            tag_b = Tag("background")
            self.play(ReplacementTransform(tag, tag_b),
                      FadeOut(VGroup(floor, messes, robot, score, reward)), run_time=0.8)
            tag = tag_b

            box_c = np.array([-0.9, -0.5, 0])
            written = RoundedRectangle(corner_radius=0.18, width=3.0, height=2.3, stroke_color=WRITTEN,
                                       stroke_width=3).move_to(box_c)
            intent = dashed_round_rect(3.0, 2.3, box_c, INTENT)
            self.play(Create(written), Create(intent), run_time=1.0)

            intent_c = np.array([2.9, -0.5, 0])
            self.play(intent.animate.move_to(intent_c), run_time=1.4)
            written_label = T("Written goal", size=22, color=WRITTEN).next_to(written, UP, buff=0.2)
            intent_label = T("What was meant", size=22, color=INTENT).next_to(intent, UP, buff=0.2)
            clock = make_clock(intent_c + UP * 0.15)
            self.play(FadeIn(written_label), FadeIn(intent_label), Create(clock), run_time=0.8)

            title = T("Reward hacking", size=32, color=INK, weight=SEMIBOLD).move_to([1.0, 1.75, 0])
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.7)

            circuit = make_circuit(box_c + UP * 0.2)
            self.play(Create(circuit[0]), FadeIn(circuit[1]), run_time=1.4)
            timer_label = T("Timer circuit", size=22, color=SOFT).next_to(circuit, DOWN, buff=0.3)
            self.play(FadeIn(timer_label), run_time=0.5)
            clock_cross = Line(clock[0].get_corner(DL), clock[0].get_corner(UR), stroke_width=4, color=HARM)

            computer = make_computer([-4.6, -0.3, 0])
            self.play(FadeIn(computer, shift=RIGHT * 0.2), run_time=0.7)
            waves = VGroup(*[wave(computer[0].get_right() + RIGHT * 0.15 + UP * dy,
                                  written.get_left() + RIGHT * 0.25 + UP * (0.2 + dy * 0.6))
                             for dy in (0.25, 0.0, -0.25)])
            self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.25), run_time=1.5)
            radio = T("Radio", size=26, color=WRITTEN, weight=MEDIUM).next_to(waves, UP, buff=0.35)
            self.play(FadeIn(radio), Indicate(circuit, color=WRITTEN, scale_factor=1.08), run_time=0.9)
            self.play(Create(clock_cross), run_time=0.6)
            self.play(LaggedStart(*[Indicate(w, color=INK, scale_factor=1.0) for w in waves], lag_ratio=0.2),
                      run_time=1.0)

        # ------------------------------------------------------------------ b03
        with self.beat("s04b03") as b:
            tag_b = Tag("definition")
            self.play(ReplacementTransform(tag, tag_b),
                      FadeOut(VGroup(written, intent, written_label, intent_label, clock, clock_cross,
                                     title, circuit, timer_label, computer, waves, radio)), run_time=0.8)
            tag = tag_b

            plot = Plot([0, 1, 0.25], [0, 1, 0.25], "Optimization pressure", "Amount",
                        width=5.6, height=3.4)
            plot.move_to([-2.0, -0.55, 0])
            ax = plot.axes
            illus = pill("Illustration", MUTED).next_to(ax, UP, buff=0.3).align_to(ax, LEFT)
            self.play(Create(ax), FadeIn(plot[1]), FadeIn(plot[2]), FadeIn(illus), run_time=1.0)

            knee = 0.45
            bleach_a = ax.plot(lambda x: 0.12 + 0.9 * x, x_range=[0, knee], color=SAND, stroke_width=4)
            clean_a = ax.plot(lambda x: 0.08 + 0.9 * x, x_range=[0, knee], color=INTENT, stroke_width=4)
            self.play(Create(bleach_a), Create(clean_a), run_time=1.6, rate_func=linear)

            marker = DashedLine(ax.c2p(knee, 0), ax.c2p(knee, 0.95), stroke_width=2, color=FAINT,
                                dash_length=0.08)
            bleach_b = ax.plot(lambda x: 0.12 + 0.9 * knee + 1.35 * (x - knee), x_range=[knee, 0.82],
                               color=SAND, stroke_width=4)
            clean_b = ax.plot(lambda x: 0.08 + 0.9 * knee + 0.3 * (1 - np.exp(-(x - knee) * 6)) / 6 * 2,
                              x_range=[knee, 1.0], color=INTENT, stroke_width=4)
            self.play(Create(marker), run_time=0.4)
            self.play(Create(bleach_b), Create(clean_b), run_time=2.2, rate_func=linear)
            bleach_lbl = T("Bleach used", size=22, color=SAND).next_to(bleach_b.get_end(), RIGHT, buff=0.2)
            clean_lbl = T("Office clean", size=22, color=INTENT).next_to(clean_b.get_end(), UP, buff=0.2)
            clean_lbl.align_to(clean_b.get_end(), RIGHT)
            self.play(FadeIn(bleach_lbl), FadeIn(clean_lbl), run_time=0.6)

            drain = make_drain(np.array([4.9, -1.9, 0]))
            bottle = make_bottle().move_to([4.1, -0.9, 0])
            self.play(FadeIn(drain), FadeIn(bottle), run_time=0.6)
            self.play(bottle.animate.rotate(-PI * 0.6).shift(RIGHT * 0.3), run_time=0.8)
            mouth = bottle[1].get_center()
            drops = VGroup(*[Dot(mouth, radius=0.05, color=WHITE) for _ in range(3)])
            self.play(LaggedStart(*[d.animate.move_to(drain.get_center() + RIGHT * (i - 1) * 0.1)
                                    for i, d in enumerate(drops)], lag_ratio=0.3), run_time=0.9)
            self.play(FadeOut(drops), run_time=0.3)

            goodhart = T("Goodhart's law", size=28, color=INK, weight=SEMIBOLD).move_to([COL_X, 1.0, 0])
            self.play(FadeIn(goodhart, shift=LEFT * 0.2), run_time=0.7)

        # ------------------------------------------------------------------ b04
        with self.beat("s04b04") as b:
            tag_b = Tag("threat_model")
            self.play(ReplacementTransform(tag, tag_b),
                      FadeOut(VGroup(plot, illus, bleach_a, clean_a, bleach_b, clean_b, marker, bleach_lbl,
                                     clean_lbl, drain, bottle, goodhart)), run_time=0.8)
            tag = tag_b

            agent = RoundedRectangle(corner_radius=0.06, width=0.4, height=0.4, stroke_width=0,
                                     fill_color=BLUE, fill_opacity=1).move_to([-4.0, -0.8, 0])
            counter = make_score(5).scale(1.2).move_to([-0.6, -0.8, 0])
            self.play(FadeIn(agent), FadeIn(counter), run_time=0.9)

            hyp = pill("Hypothetical", KIND_COLORS["threat_model"]).move_to([5.3, -3.25, 0])
            self.play(FadeIn(hyp), run_time=0.5)

            self.play(counter.animate.move_to([-0.6, 1.0, 0]), run_time=1.0)
            sensor = Node("Reward sensor", color=AMBER, size=22, height=0.7).move_to([-0.6, -0.8, 0])
            wire = Line(sensor.get_top(), counter.get_bottom(), stroke_width=2.5, color=AMBER)
            self.play(FadeIn(sensor, scale=0.8), Create(wire), run_time=1.0)

            person = Circle(radius=0.28, stroke_width=0, fill_color=GRAY, fill_opacity=1).move_to([2.2, -0.8, 0])
            person_lbl = T("Person", size=22, color=SOFT).next_to(person, DOWN, buff=0.2)
            human_wire = Line(person.get_left(), sensor.get_right(), stroke_width=2, color=FAINT)
            self.play(FadeIn(person), FadeIn(person_lbl), Create(human_wire), run_time=0.9)

            reach = Line(agent.get_right(), sensor.get_left(), stroke_width=4, color=BLUE)
            self.play(Create(reach), run_time=1.4)
            self.play(*fill_pips(counter.pips, 5), Indicate(sensor, color=BLUE, scale_factor=1.05),
                      run_time=1.0)
            wirehead = T("Wireheading", size=30, color=INK, weight=SEMIBOLD).move_to([COL_X, 1.0, 0])
            self.play(FadeIn(wirehead, shift=LEFT * 0.2), run_time=0.7)

            ring = Circle(radius=0.45, stroke_color=HARM, stroke_width=3).move_to(person)
            self.play(person.animate.set_fill(HARM), human_wire.animate.set_color(HARM), Create(ring),
                      run_time=1.0)
            self.play(Indicate(person, color=HARM, scale_factor=1.15), run_time=0.8)

        # ------------------------------------------------------------------ b05
        with self.beat("s04b05") as b:
            tag_b = Tag("hypothesis")
            self.play(ReplacementTransform(tag, tag_b),
                      FadeOut(VGroup(agent, counter, hyp, sensor, wire, person, person_lbl, human_wire,
                                     reach, wirehead, ring)), run_time=0.8)
            tag = tag_b

            base_y = -1.5
            sizes, details, xs = [0.45, 0.8, 1.15], [0, 1, 3], [-5.0, -3.2, -1.0]
            squares = VGroup(*[agent_square(s, d).move_to([x, base_y + s / 2, 0])
                               for s, d, x in zip(sizes, details, xs)])
            robot2 = place_robot(make_robot(), squares[0][0].get_center())
            self.play(FadeIn(robot2), run_time=0.6)
            self.play(ReplacementTransform(robot2, squares[0]), run_time=0.8)
            self.play(LaggedStart(FadeIn(squares[1], shift=RIGHT * 0.2), FadeIn(squares[2], shift=RIGHT * 0.2),
                                  lag_ratio=0.4), run_time=1.2)

            arrow = Arrow([xs[0] - 0.4, base_y - 0.4, 0], [xs[2] + 0.8, base_y - 0.4, 0], buff=0,
                          stroke_width=3, color=MUTED, max_tip_length_to_length_ratio=0.05)
            agents_lbl = T("More complex agents", size=22, color=SOFT).next_to(arrow, DOWN, buff=0.2)
            self.play(GrowArrow(arrow), FadeIn(agents_lbl), run_time=0.9)

            counts = [1, 3, 5]
            stacks = VGroup()
            for sq, n in zip(squares, counts):
                x = sq.get_right()[0] + 0.35
                stacks.add(VGroup(*[crack([x, base_y + 0.12 + i * 0.22, 0]) for i in range(n)]))
            self.play(LaggedStart(*[LaggedStart(*[Create(c) for c in st], lag_ratio=0.5) for st in stacks],
                                  lag_ratio=0.5), run_time=2.4)
            hack_lbl = T("More ways to hack", size=22, color=HARM).move_to([-3.0, 0.9, 0])
            self.play(FadeIn(hack_lbl), run_time=0.6)

            game_c = np.array([4.2, -0.5, 0])
            game = RoundedRectangle(corner_radius=0.12, width=3.2, height=2.4, stroke_color=GRAY,
                                    stroke_width=3, fill_color="#171A1F", fill_opacity=1).move_to(game_c)
            wall_x = game_c[0] + 0.3
            wall_top = Line([wall_x, game_c[1] + 1.0, 0], [wall_x, game_c[1] + 0.2, 0], stroke_width=8, color=SAND)
            wall_bot = Line([wall_x, game_c[1] - 0.1, 0], [wall_x, game_c[1] - 1.0, 0], stroke_width=8, color=SAND)
            gap_mark = Line([wall_x, game_c[1] + 0.2, 0], [wall_x, game_c[1] - 0.1, 0], stroke_width=3, color=HARM)
            player = Square(side_length=0.2, stroke_width=0, fill_color=BLUE, fill_opacity=1)
            player.move_to(game_c + LEFT * 1.1 + UP * 0.05)
            flag = VGroup(Line(ORIGIN, UP * 0.45, stroke_width=3, color=INK),
                          Triangle(stroke_width=0, fill_color=AMBER, fill_opacity=1).scale(0.12)
                          .rotate(-PI / 2).move_to(UP * 0.36 + RIGHT * 0.1))
            flag.move_to(game_c + RIGHT * 1.1 + UP * 0.05)
            self.play(FadeIn(game), Create(wall_top), Create(wall_bot), FadeIn(player), FadeIn(flag),
                      run_time=0.9)
            self.play(Create(gap_mark), run_time=0.4)
            self.play(player.animate.move_to(game_c + RIGHT * 0.9 + UP * 0.05), run_time=1.6,
                      rate_func=smooth)
            self.play(Indicate(gap_mark, color=HARM, scale_factor=1.3), run_time=0.6)

        # ------------------------------------------------------------------ b06
        with self.beat("s04b06") as b:
            tag_b = Tag("method")
            self.play(ReplacementTransform(tag, tag_b),
                      FadeOut(VGroup(squares, arrow, agents_lbl, stacks, hack_lbl, game, wall_top, wall_bot,
                                     gap_mark, player, flag)), run_time=0.8)
            tag = tag_b

            floor = RoundedRectangle(corner_radius=0.3, width=OFFICE_W, height=OFFICE_H,
                                     stroke_color=GRAY, stroke_width=2, fill_color=PANEL,
                                     fill_opacity=1).move_to(OFFICE_C)
            wall_x = OFFICE_C[0] + 0.6
            top_y, bot_y = OFFICE_C[1] + OFFICE_H / 2, OFFICE_C[1] - OFFICE_H / 2
            door_top, door_bot = 0.7, -1.5
            wall_a = Line([wall_x, top_y, 0], [wall_x, door_top, 0], stroke_width=6, color=GRAY)
            wall_b = Line([wall_x, door_bot, 0], [wall_x, bot_y, 0], stroke_width=6, color=GRAY)
            self.play(FadeIn(floor), Create(wall_a), Create(wall_b), run_time=0.9)

            wire_line = Line([wall_x, door_top, 0], [wall_x, door_bot, 0], stroke_width=2.5, color=HARM)
            bell = make_bell([wall_x + 0.45, door_top + 0.35, 0])
            trip_lbl = T("Trip wire", size=24, color=HARM, weight=MEDIUM).move_to([COL_X, 1.0, 0])
            self.play(Create(wire_line), FadeIn(bell), FadeIn(trip_lbl), run_time=1.0)

            r1 = place_robot(make_robot(0.85), [-4.7, 0.2, 0])
            r1.set_z_index(3)
            self.play(FadeIn(r1), run_time=0.4)
            self.play(r1.animate.shift(RIGHT * (wall_x - r1.pointer.get_right()[0])), run_time=1.6)
            self.play(Indicate(bell, color=HARM, scale_factor=1.5),
                      wire_line.animate.set_stroke(width=5),
                      r1.body.animate.set_fill(GRAY), r1.pointer.animate.set_color(GRAY),
                      r1.cone.animate.set_fill(opacity=0), run_time=0.9)
            self.play(wire_line.animate.set_stroke(width=2.5), run_time=0.3)

            r2 = place_robot(make_robot(0.85), [-4.7, -0.9, 0])
            r2.set_z_index(3)
            self.play(FadeIn(r2), run_time=0.4)
            start = r2.body.get_center()
            mid = np.array([wall_x, start[1], 0])
            end = np.array([wall_x + 1.6, start[1], 0])
            self.play(r2.animate.shift(mid - start + LEFT * 0.7), run_time=1.1)
            self.play(r2.animate.shift(RIGHT * 0.7 + UP * 0.25).scale(1.25), run_time=0.6)
            self.play(r2.animate.shift(end - mid + DOWN * 0.25).scale(1 / 1.25), run_time=0.6)
            question = T("?", size=40, color=HARM, weight=SEMIBOLD).set_opacity(0.6)
            question.next_to(r2.body, UP, buff=0.2)
            seen = T("Seen through?", size=24, color=HARM).move_to([COL_X, 0.3, 0])
            self.play(FadeIn(question, shift=UP * 0.1), FadeIn(seen), run_time=0.7)
