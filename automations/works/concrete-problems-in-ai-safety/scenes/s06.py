# storyboard: b580ac25a0fbb4a8
from aisr_kit import *

# Roles from the video's visual language.
INTENT = "#8CC084"   # what the designer meant / safe: green
HARM = "#E0564F"     # harm: red
MOP = SAND

GAME_C = np.array([-4.3, -0.4, 0])
GAME_W, GAME_H = 3.6, 3.2
OFFICE_C = np.array([2.3, -0.4, 0])
OFFICE_W, OFFICE_H = 7.4, 4.0
LABEL_Y = 2.05


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


def make_office(center, width, height):
    office = RoundedRectangle(corner_radius=0.3, width=width, height=height,
                              stroke_color=GRAY, stroke_width=3, fill_color=PANEL, fill_opacity=1)
    return office.move_to(center)


def make_outlet():
    plate = RoundedRectangle(corner_radius=0.05, width=0.46, height=0.32, stroke_color=SOFT,
                             stroke_width=2, fill_color=BG, fill_opacity=1)
    holes = VGroup(Line(UP * 0.06, DOWN * 0.06, stroke_width=3, color=SOFT).shift(LEFT * 0.09),
                   Line(UP * 0.06, DOWN * 0.06, stroke_width=3, color=SOFT).shift(RIGHT * 0.09))
    outlet = VGroup(plate, holes)
    outlet.rotate(PI / 2)
    outlet.set_z_index(3)
    return outlet


def make_stairs():
    steps = VGroup(*[Line(LEFT * 0.45, RIGHT * 0.45, stroke_width=3, color=SOFT).shift(DOWN * 0.16 * i)
                     for i in range(5)])
    frame = Rectangle(width=1.0, height=0.85, stroke_color=SOFT, stroke_width=2)
    frame.move_to(steps)
    stairs = VGroup(frame, steps)
    stairs.set_z_index(3)
    return stairs


def no_marker(radius=0.34, width=5):
    ring = Circle(radius=radius, stroke_color=HARM, stroke_width=width)
    slash = Line(UL * radius * 0.7, DR * radius * 0.7, stroke_width=width, color=HARM)
    marker = VGroup(ring, slash)
    marker.set_z_index(6)
    return marker


def red_cross(size=0.5, width=6):
    a = Line(UL * size / 2, DR * size / 2, stroke_width=width, color=HARM)
    b = Line(UR * size / 2, DL * size / 2, stroke_width=width, color=HARM)
    cross = VGroup(a, b)
    cross.set_z_index(7)
    return cross


def trial_path(start, end, angle, color=BLUE):
    arc = ArcBetweenPoints(start, end, angle=angle)
    dashed = DashedVMobject(arc, num_dashes=16, dashed_ratio=0.55)
    dashed.set_stroke(color=color, width=3)
    dashed.set_z_index(2)
    return dashed, arc


def mop_head(pos):
    head = RoundedRectangle(corner_radius=0.04, width=0.16, height=0.3, stroke_width=0,
                            fill_color=MOP, fill_opacity=1).move_to(pos)
    head.set_z_index(4)
    return head


def floor_spot(pos):
    spot = Circle(radius=0.13, stroke_color=MOP, stroke_width=2, fill_color=MOP, fill_opacity=0.25)
    spot.move_to(pos)
    spot.set_z_index(1)
    return spot


class S06(NarratedScene):
    def construct(self):
        # ------------------------------------------------------------------ b01
        with self.beat("s06b01") as b:
            heading = Heading("Risky trials")
            tag = Tag("definition")
            source = Source(self.paper["short"])
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), run_time=0.8)

            # Left: a small game screen.
            game = RoundedRectangle(corner_radius=0.15, width=GAME_W, height=GAME_H,
                                    stroke_color=SOFT, stroke_width=2, fill_color=BG, fill_opacity=1)
            game.move_to(GAME_C)
            game_label = T("Game", size=26, color=SOFT, weight=MEDIUM).move_to([GAME_C[0], LABEL_Y, 0])
            ground = Line(game.get_corner(DL) + RIGHT * 0.25 + UP * 0.7,
                          game.get_corner(DR) + LEFT * 0.25 + UP * 0.7, stroke_width=2, color=FAINT)
            meter_bg = RoundedRectangle(corner_radius=0.06, width=2.4, height=0.18, stroke_color=AMBER,
                                        stroke_width=1.5).move_to(game.get_top() + DOWN * 0.4)
            meter = RoundedRectangle(corner_radius=0.06, width=2.4, height=0.18, stroke_width=0,
                                     fill_color=AMBER, fill_opacity=1).move_to(meter_bg)
            ground_y = ground.get_y()
            player = Circle(radius=0.2, stroke_width=0, fill_color=BLUE, fill_opacity=1)
            player.move_to([GAME_C[0] - 1.2, ground_y + 0.21, 0])
            enemy = Triangle(stroke_width=0, fill_color=ROSE, fill_opacity=1).scale(0.22)
            enemy.move_to([GAME_C[0] + 0.5, ground_y + 0.17, 0])
            self.play(Create(game), FadeIn(game_label), run_time=0.8)
            self.play(Create(ground), FadeIn(meter_bg), FadeIn(meter), FadeIn(player), FadeIn(enemy),
                      run_time=0.6)
            self.play(player.animate.move_to([GAME_C[0] + 0.12, ground_y + 0.21, 0]), run_time=1.0,
                      rate_func=linear)
            left_edge = meter.get_left()
            self.play(
                player.animate.shift(LEFT * 0.5),
                Indicate(enemy, color=HARM, scale_factor=1.2),
                meter.animate.stretch_to_fit_width(1.5).align_to(left_edge, LEFT),
                run_time=0.8,
            )

            # Right: the office.
            office = make_office(OFFICE_C, OFFICE_W, OFFICE_H)
            office_label = T("Office", size=26, color=SOFT, weight=MEDIUM).move_to([OFFICE_C[0], LABEL_Y, 0])
            outlet_pos = np.array([OFFICE_C[0] + OFFICE_W / 2, OFFICE_C[1] + 1.0, 0])
            outlet = make_outlet().move_to(outlet_pos)
            robot_home = np.array([OFFICE_C[0] - 2.4, OFFICE_C[1] - 0.3, 0])
            robot = make_robot().move_to(robot_home)
            mop_line = Line(robot.get_right() + RIGHT * 0.05, robot.get_right() + RIGHT * 0.4,
                            stroke_width=3, color=MOP)
            mop_line.set_z_index(4)
            mop = VGroup(mop_line, mop_head(mop_line.get_end()))
            self.play(Create(office), FadeIn(office_label), run_time=0.9)
            self.play(FadeIn(outlet), FadeIn(robot), FadeIn(mop), run_time=0.6)

            start = mop.get_right()
            ends = [
                np.array([OFFICE_C[0] + 0.6, OFFICE_C[1] - 1.4, 0]),
                np.array([OFFICE_C[0] + 1.4, OFFICE_C[1] - 0.2, 0]),
                outlet_pos + LEFT * 0.3,
            ]
            angles = [0.5, 0.15, -0.3]
            paths = VGroup()
            arcs = []
            spots = VGroup()
            for i, (end, angle) in enumerate(zip(ends, angles)):
                dashed, arc = trial_path(start, end, angle)
                paths.add(dashed)
                arcs.append(arc)
                if i < 2:
                    spot = floor_spot(end)
                    spots.add(spot)
                    self.play(Create(dashed), run_time=0.8)
                    self.play(FadeIn(spot, scale=0.5), run_time=0.3)
                else:
                    self.play(Create(dashed), run_time=0.9)

            # The robot follows the third trial to the outlet.
            travel = VGroup(robot, mop)
            offset = travel.get_center() - mop.get_right()
            run_path = arcs[2].copy().shift(offset)
            self.play(MoveAlongPath(travel, run_path), run_time=1.3)
            outlet_flash = outlet[0].copy().set_fill(HARM, opacity=1).set_stroke(HARM)
            outlet_flash.set_z_index(3)
            cross = red_cross(0.5).move_to(outlet_pos + RIGHT * 0.05)
            self.play(FadeIn(outlet_flash), Flash(outlet_pos, color=HARM, line_length=0.2), run_time=0.6)
            self.play(Create(cross), run_time=0.4)

            concept = T("Safe exploration", size=30, color=INK, weight=SEMIBOLD)
            concept.move_to([OFFICE_C[0], -3.0, 0])
            self.play(FadeIn(concept, shift=UP * 0.15), run_time=0.6)

        # ------------------------------------------------------------------ b02
        with self.beat("s06b02") as b:
            tag_b2 = Tag("author_interpretation")
            stairs = make_stairs().move_to([OFFICE_C[0] + 2.8, OFFICE_C[1] - 1.25, 0])
            self.play(
                ReplacementTransform(tag, tag_b2),
                FadeOut(VGroup(game, game_label, ground, meter_bg, meter, player, enemy)),
                FadeOut(paths), FadeOut(spots), FadeOut(cross), FadeOut(outlet_flash), FadeOut(concept),
                travel.animate.shift(robot_home - robot.get_center()),
                run_time=0.8,
            )
            tag = tag_b2

            rules_label = T("Hard-coded rules", size=26, color=HARM, weight=MEDIUM)
            rules_label.move_to(office_label)
            self.play(FadeIn(stairs), ReplacementTransform(office_label, rules_label), run_time=0.7)

            no_outlet = no_marker().move_to(outlet_pos + LEFT * 0.1)
            no_stairs = no_marker(radius=0.52).move_to(stairs)
            self.play(LaggedStart(FadeIn(no_outlet, scale=1.4), FadeIn(no_stairs, scale=1.4), lag_ratio=0.4),
                      run_time=1.0)

            # The robot's trials now bend away from the marked spots.
            avoid = VMobject().set_points_smoothly([
                travel.get_center(),
                np.array([OFFICE_C[0] - 0.3, OFFICE_C[1] + 0.9, 0]),
                np.array([OFFICE_C[0] + 1.3, OFFICE_C[1] + 0.3, 0]),
                np.array([OFFICE_C[0] + 1.0, OFFICE_C[1] - 1.0, 0]),
                np.array([OFFICE_C[0] - 0.8, OFFICE_C[1] - 1.1, 0]),
            ])
            avoid_trail = DashedVMobject(avoid.copy(), num_dashes=30, dashed_ratio=0.55)
            avoid_trail.set_stroke(color=BLUE, width=3)
            avoid_trail.set_z_index(2)
            self.play(MoveAlongPath(travel, avoid), Create(avoid_trail), run_time=2.2)

            # Zoom out: this office is one small node in a power grid.
            rng = np.random.default_rng(6)
            xs = np.linspace(-5.7, 5.7, 9)
            ys = np.linspace(-2.5, 1.3, 5)
            positions = []
            for yi, y in enumerate(ys):
                for xi, x in enumerate(xs):
                    jitter = rng.uniform(-0.22, 0.22, 2)
                    positions.append(np.array([x + jitter[0], y + jitter[1], 0]))
            n_cols = len(xs)
            office_idx = 2 * n_cols + 6
            office_group = VGroup(office, outlet, stairs, travel, no_outlet, no_stairs, avoid_trail)
            self.play(
                office_group.animate.scale(0.075).move_to(positions[office_idx]),
                FadeOut(rules_label),
                run_time=1.4,
            )

            edges = VGroup()
            for r in range(len(ys)):
                for c in range(n_cols):
                    i = r * n_cols + c
                    if c + 1 < n_cols:
                        edges.add(Line(positions[i], positions[i + 1]))
                    if r + 1 < len(ys) and (c + r) % 2 == 0:
                        edges.add(Line(positions[i], positions[i + n_cols]))
                    if r + 1 < len(ys) and c + 1 < n_cols and (c * 3 + r) % 4 == 1:
                        edges.add(Line(positions[i], positions[i + n_cols + 1]))
            edges.set_stroke(color=FAINT, width=2)
            nodes = VGroup(*[Circle(radius=0.12, stroke_color=SOFT, stroke_width=2, fill_color=PANEL,
                                    fill_opacity=1).move_to(p)
                             for i, p in enumerate(positions) if i != office_idx])
            nodes.set_z_index(2)
            grid_label = T("Power grid", size=26, color=SOFT, weight=MEDIUM).move_to([0, LABEL_Y, 0])
            self.play(LaggedStart(Create(edges), FadeIn(nodes, lag_ratio=0.05), lag_ratio=0.3),
                      FadeIn(grid_label), run_time=2.0)

            marked = [3, 11, 19, 27, 35]
            grid_markers = VGroup(*[no_marker(radius=0.2, width=3).move_to(nodes[i]) for i in marked])
            self.play(LaggedStart(*[FadeIn(m, scale=1.4) for m in grid_markers], lag_ratio=0.25),
                      run_time=1.2)
            unmarked = VGroup(*[n for i, n in enumerate(nodes) if i not in marked])
            self.play(unmarked.animate.set_stroke(AMBER), run_time=0.8)
            self.play(unmarked.animate.set_stroke(SOFT), run_time=0.6)

        # ------------------------------------------------------------------ b03
        with self.beat("s06b03") as b:
            tag_b3 = Tag("method")
            self.play(
                ReplacementTransform(tag, tag_b3),
                FadeOut(VGroup(edges, nodes, grid_markers, office_group, grid_label)),
                run_time=0.5,
            )
            tag = tag_b3

            sw, sh = 5.4, 3.6
            sim_c = np.array([-3.25, -0.5, 0])
            real_c = np.array([3.25, -0.5, 0])
            sim_office = DashedVMobject(
                RoundedRectangle(corner_radius=0.3, width=sw, height=sh, stroke_color=SOFT, stroke_width=3),
                num_dashes=70, dashed_ratio=0.55).move_to(sim_c)
            real_office = make_office(real_c, sw, sh)
            sim_label = T("Simulation", size=26, color=SOFT, weight=MEDIUM).move_to([sim_c[0], 1.75, 0])
            real_label = T("Office", size=26, color=SOFT, weight=MEDIUM).move_to([real_c[0], 1.75, 0])
            sim_outlet_pos = sim_c + np.array([sw / 2, 0.8, 0])
            real_outlet_pos = real_c + np.array([sw / 2, 0.8, 0])
            sim_outlet = make_outlet().move_to(sim_outlet_pos)
            real_outlet = make_outlet().move_to(real_outlet_pos)
            sim_robot = make_robot(0.85).move_to(sim_c + np.array([-1.8, -0.5, 0]))
            real_robot = make_robot(0.85).move_to(real_c + np.array([-1.8, -0.5, 0]))
            sim_robot.set_opacity(0.7)
            self.play(Create(sim_office), FadeIn(real_office), FadeIn(sim_label), FadeIn(real_label),
                      FadeIn(sim_outlet), FadeIn(real_outlet), FadeIn(sim_robot), FadeIn(real_robot),
                      run_time=0.8)

            # Simulation: risky trials, including the outlet, cost nothing real.
            s0 = sim_robot.get_right()
            sim_ends = [sim_outlet_pos + LEFT * 0.3, sim_c + np.array([1.6, -1.1, 0]),
                        sim_c + np.array([0.6, 0.4, 0])]
            sim_paths = VGroup(*[trial_path(s0, e, a)[0] for e, a in zip(sim_ends, [-0.3, 0.4, 0.1])])
            sim_hit = sim_outlet[0].copy().set_stroke(HARM).set_fill(HARM, opacity=1)
            self.play(LaggedStart(*[Create(p) for p in sim_paths], lag_ratio=0.3),
                      Transform(sim_outlet[0], sim_hit), run_time=1.4)

            # Real office: a green safe region; trials stay inside it.
            safe = RoundedRectangle(corner_radius=0.2, width=3.1, height=2.5, stroke_color=INTENT,
                                    stroke_width=2.5, fill_color=INTENT, fill_opacity=0.16)
            safe.move_to(real_c + np.array([-0.95, -0.35, 0]))
            safe.set_z_index(1)
            safe_label = T("Safe region", size=24, color=INTENT, weight=MEDIUM)
            safe_label.next_to(real_office, DOWN, buff=0.25).align_to(safe, LEFT)
            self.play(FadeIn(safe), FadeIn(safe_label, shift=UP * 0.1), run_time=0.8)

            r0 = real_robot.get_right()
            real_ends = [real_c + np.array([0.3, 0.55, 0]), real_c + np.array([0.4, -0.5, 0]),
                         real_c + np.array([-0.4, -1.35, 0])]
            real_paths = VGroup(*[trial_path(r0, e, a)[0] for e, a in zip(real_ends, [-0.4, 0.05, 0.5])])
            self.play(LaggedStart(*[Create(p) for p in real_paths], lag_ratio=0.3), run_time=1.4)
            self.play(Indicate(safe, color=INTENT, scale_factor=1.03), run_time=0.7)
