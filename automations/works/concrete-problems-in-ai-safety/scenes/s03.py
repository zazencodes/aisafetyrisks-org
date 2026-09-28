# storyboard: 5093572bbad9c728
from aisr_kit import *

# Roles from the video's visual language.
INTENT = "#8CC084"   # what the designer meant: green dashed
WRITTEN = "#E0873A"  # the goal as written: solid orange
HARM = "#E0564F"     # harm: red
BOX_GREY = GRAY

OFFICE_C = np.array([-1.8, -0.3, 0])
OFFICE_W, OFFICE_H = 8.2, 4.6
LANE_Y = -0.3
BOX_START = np.array([-4.5, LANE_Y, 0])
ROBOT_START = np.array([-5.1, LANE_Y, 0])
VASE_POS = np.array([-1.8, LANE_Y, 0])
TARGET_POS = np.array([1.5, LANE_Y, 0])
COL_X = 4.65  # right-hand column for labels and the dial


def make_robot():
    body = RoundedRectangle(corner_radius=0.1, width=0.52, height=0.52, stroke_width=0,
                            fill_color=BLUE, fill_opacity=1)
    eye = Circle(radius=0.075, stroke_width=0, fill_color=WHITE, fill_opacity=1)
    eye.move_to(body.get_right() + LEFT * 0.12)
    pointer = Line(body.get_right(), body.get_right() + RIGHT * 0.2, stroke_width=3, color=INK)
    return VGroup(body, eye, pointer)


def make_vase():
    return Circle(radius=0.2, stroke_color=WHITE, stroke_width=2, fill_color=TEAL, fill_opacity=1)


def make_box():
    return Square(side_length=0.5, stroke_color=SOFT, stroke_width=1.5, fill_color=BOX_GREY,
                  fill_opacity=0.85)


def make_target(radius=0.3, color=SOFT):
    ring = Circle(radius=radius, stroke_color=color, stroke_width=2.5)
    inner = Circle(radius=radius * 0.45, stroke_color=color, stroke_width=2)
    dot = Dot(radius=radius * 0.12, color=color)
    return VGroup(ring, inner, dot)


def red_cross(size=0.5, width=6):
    a = Line(UL * size / 2, DR * size / 2, stroke_width=width, color=HARM)
    b = Line(UR * size / 2, DL * size / 2, stroke_width=width, color=HARM)
    return VGroup(a, b)


def minus_mark():
    return T("-", size=34, color=HARM, weight=SEMIBOLD)


def office_objects():
    """Things that can play the vase's role, in the order they pop up."""
    socket_plate = RoundedRectangle(corner_radius=0.04, width=0.38, height=0.28, stroke_color=SOFT,
                                    stroke_width=2, fill_color=PANEL, fill_opacity=1)
    socket = VGroup(socket_plate,
                    Dot(socket_plate.get_center() + LEFT * 0.08, radius=0.035, color=SOFT),
                    Dot(socket_plate.get_center() + RIGHT * 0.08, radius=0.035, color=SOFT))
    socket.move_to([-5.3, 1.3, 0])

    wall = Line([-3.3, 1.35, 0], [-2.0, 1.35, 0], stroke_width=8, color=GRAY)

    pot = Square(side_length=0.26, stroke_width=0, fill_color=SAND, fill_opacity=1)
    leaves = VGroup(*[Circle(radius=0.13, stroke_width=0, fill_color="#7E9A62", fill_opacity=1)
                      .move_to(pot.get_top() + d) for d in (UP * 0.12 + LEFT * 0.12, UP * 0.22, UP * 0.12 + RIGHT * 0.12)])
    plant = VGroup(pot, leaves).move_to([0.2, 1.3, 0])

    screen = Rectangle(width=0.72, height=0.44, stroke_color=BLUE, stroke_width=2, fill_color="#1E2733",
                       fill_opacity=1).move_to([-3.6, -1.8, 0])

    extras = VGroup(
        Square(side_length=0.34, stroke_color=SOFT, stroke_width=2).move_to([-0.6, -1.9, 0]),
        Circle(radius=0.2, stroke_color=AMBER, stroke_width=2).move_to([1.4, -1.8, 0]),
        Rectangle(width=0.9, height=0.3, stroke_color=SAND, stroke_width=2).move_to([1.5, 1.35, 0]),
        Ellipse(width=0.9, height=0.45, stroke_color=VIOLET, stroke_width=2).move_to([-5.0, -1.9, 0]),
        Square(side_length=0.3, stroke_color=SOFT, stroke_width=2).move_to([-2.2, -2.0, 0]),
        Circle(radius=0.16, stroke_color=TEAL, stroke_width=2).move_to([-1.0, 1.0, 0]),
        Rectangle(width=0.5, height=0.3, stroke_color=GRAY, stroke_width=2).move_to([0.3, -1.4, 0]),
        Circle(radius=0.14, stroke_color=SAND, stroke_width=2).move_to([-4.2, 0.6, 0]),
    )
    return socket, wall, plant, screen, extras


def red_ring(mob, buff=0.1):
    return SurroundingRectangle(mob, buff=buff, corner_radius=0.08, stroke_color=HARM, stroke_width=2)


def dashed_round_rect(width, height, center, color, num_dashes=90):
    rect = RoundedRectangle(corner_radius=0.18, width=width, height=height,
                            stroke_color=color, stroke_width=3).move_to(center)
    return DashedVMobject(rect, num_dashes=num_dashes, dashed_ratio=0.55)


class S03(NarratedScene):
    def construct(self):
        # ------------------------------------------------------------------ b01
        with self.beat("s03b01") as b:
            heading = Heading("When the goal leaves things out")
            tag = Tag("definition")
            source = Source(self.paper["short"])
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), run_time=0.8)

            office = RoundedRectangle(corner_radius=0.3, width=OFFICE_W, height=OFFICE_H,
                                      stroke_color=GRAY, stroke_width=3, fill_color=PANEL, fill_opacity=1)
            office.move_to(OFFICE_C)
            self.play(Create(office), run_time=1.0)

            box = make_box().move_to(BOX_START)
            target = make_target().move_to(TARGET_POS)
            vase = make_vase().move_to(VASE_POS)
            robot = make_robot().move_to(ROBOT_START)
            box.set_z_index(3)
            vase.set_z_index(3)
            target.set_z_index(3)
            robot.set_z_index(4)
            self.play(LaggedStart(FadeIn(box), FadeIn(target), FadeIn(vase), FadeIn(robot),
                                  lag_ratio=0.3), run_time=1.2)

            box_outline = RoundedRectangle(corner_radius=0.1, width=0.85, height=0.85,
                                           stroke_color=WRITTEN, stroke_width=3).move_to(BOX_START)
            target_outline = RoundedRectangle(corner_radius=0.1, width=0.85, height=0.85,
                                              stroke_color=WRITTEN, stroke_width=3).move_to(TARGET_POS)
            box_outline.set_z_index(2)
            target_outline.set_z_index(2)
            reward_label = T("Reward: move the box", size=24, color=WRITTEN, weight=MEDIUM)
            reward_label.move_to([COL_X, 1.3, 0])
            self.play(Create(box_outline), Create(target_outline), run_time=0.8)
            self.play(FadeIn(reward_label, shift=LEFT * 0.2), run_time=0.6)

            pusher = VGroup(robot, box, box_outline)
            hit_x = VASE_POS[0] - 0.45
            self.play(pusher.animate.shift(RIGHT * (hit_x - BOX_START[0])), run_time=2.0, rate_func=linear)
            self.play(
                pusher.animate.shift(RIGHT * (TARGET_POS[0] - hit_x)),
                vase.animate.shift(DOWN * 0.75 + RIGHT * 0.35).stretch(0.55, 1)
                    .set_fill(HARM).set_stroke(HARM),
                run_time=2.2,
            )
            side_label = T("Side effect", size=24, color=HARM, weight=MEDIUM)
            side_label.next_to(vase, DOWN, buff=0.2)
            self.play(FadeIn(side_label), Indicate(vase, color=HARM, scale_factor=1.15), run_time=0.8)

        # ------------------------------------------------------------------ b02
        with self.beat("s03b02") as b:
            upright = make_vase().move_to(VASE_POS)
            self.play(
                FadeOut(side_label),
                pusher.animate.shift(RIGHT * (BOX_START[0] - TARGET_POS[0])),
                Transform(vase, upright),
                run_time=1.0,
            )
            vase_minus = T("- vase", size=24, color=HARM, weight=SEMIBOLD)
            vase_minus.next_to(vase, UP, buff=0.2)
            vase_ring = red_ring(vase, buff=0.08)
            self.play(Create(vase_ring), FadeIn(vase_minus, shift=DOWN * 0.1), run_time=0.8)

            socket, wall, plant, screen, extras = office_objects()
            socket_label = T("Socket", size=20, color=SOFT).next_to(socket, RIGHT, buff=0.18)
            wall_label = T("Wall", size=20, color=SOFT).next_to(wall, UP, buff=0.15)
            socket_ring, wall_ring = red_ring(socket), red_ring(wall, buff=0.12)
            plant_ring, screen_ring = red_ring(plant), red_ring(screen)
            socket_minus = minus_mark().next_to(socket_ring, UP, buff=0.08)
            wall_minus = minus_mark().next_to(wall_ring, RIGHT, buff=0.12)
            plant_minus = minus_mark().next_to(plant_ring, RIGHT, buff=0.12)

            self.play(FadeIn(socket, scale=0.6), FadeIn(socket_label), Create(socket_ring), run_time=0.7)
            self.play(FadeIn(socket_minus), run_time=0.3)
            self.play(Create(wall), FadeIn(wall_label), Create(wall_ring), run_time=0.6)
            self.play(FadeIn(wall_minus), run_time=0.25)
            self.play(FadeIn(plant, scale=0.6), Create(plant_ring), run_time=0.45)
            self.play(FadeIn(plant_minus), run_time=0.2)
            self.play(FadeIn(screen, scale=0.6), Create(screen_ring), run_time=0.35)

            extra_rings = VGroup(*[red_ring(m, buff=0.08) for m in extras])
            self.play(
                LaggedStart(*[AnimationGroup(FadeIn(m, scale=0.6), Create(r))
                              for m, r in zip(extras, extra_rings)], lag_ratio=0.35),
                run_time=1.8,
            )
            crowd = VGroup(socket, wall, plant, screen, extras)
            rings = VGroup(vase_ring, socket_ring, wall_ring, plant_ring, screen_ring, extra_rings)
            minuses = VGroup(vase_minus, socket_minus, wall_minus, plant_minus)

        # ------------------------------------------------------------------ b03
        with self.beat("s03b03") as b:
            tag_b3 = Tag("author_interpretation")
            written_label = T("Written goal", size=24, color=WRITTEN, weight=MEDIUM)
            written_label.move_to([COL_X, 1.3, 0])
            self.play(
                ReplacementTransform(tag, tag_b3),
                FadeOut(rings), FadeOut(minuses), FadeOut(socket_label), FadeOut(wall_label),
                ReplacementTransform(reward_label, written_label),
                run_time=0.9,
            )
            tag = tag_b3

            intent_small = dashed_round_rect(0.85, 0.85, BOX_START, INTENT)
            intent_big = dashed_round_rect(OFFICE_W - 0.2, OFFICE_H - 0.2, OFFICE_C, INTENT)
            intent_small.set_z_index(2)
            intent_big.set_z_index(2)
            self.play(FadeIn(intent_small), run_time=0.4)
            self.play(Transform(intent_small, intent_big), run_time=2.2)
            intent = intent_small

            meant_label = T("What was meant", size=24, color=INTENT, weight=MEDIUM)
            meant_label.move_to([COL_X, 0.6, 0])
            self.play(FadeIn(meant_label, shift=LEFT * 0.2), run_time=0.7)

            shade = RoundedRectangle(corner_radius=0.18, width=OFFICE_W - 0.2, height=OFFICE_H - 0.2,
                                     stroke_width=0, fill_color=HARM, fill_opacity=0.12).move_to(OFFICE_C)
            shade.set_z_index(1)
            self.play(
                FadeIn(shade),
                box_outline.animate.set_fill(PANEL, opacity=1),
                target_outline.animate.set_fill(PANEL, opacity=1),
                run_time=1.2,
            )
            self.play(Indicate(box_outline, color=WRITTEN, scale_factor=1.1),
                      Indicate(target_outline, color=WRITTEN, scale_factor=1.1), run_time=1.0)

        # ------------------------------------------------------------------ b04
        with self.beat("s03b04") as b:
            tag_b4 = Tag("method")
            self.play(
                ReplacementTransform(tag, tag_b4),
                FadeOut(crowd), FadeOut(shade), FadeOut(intent), FadeOut(box_outline),
                FadeOut(target_outline), FadeOut(written_label), FadeOut(meant_label),
                run_time=0.8,
            )
            tag = tag_b4

            dial_c = np.array([COL_X, 0.3, 0])
            dial_arc = Arc(radius=0.85, start_angle=0, angle=PI, stroke_color=AMBER, stroke_width=4,
                           arc_center=dial_c)
            ticks = VGroup(*[Line(dial_c + 0.72 * np.array([np.cos(a), np.sin(a), 0]),
                                  dial_c + 0.85 * np.array([np.cos(a), np.sin(a), 0]),
                                  stroke_width=2, color=AMBER) for a in np.linspace(0, PI, 5)])
            needle = Line(dial_c, dial_c + 0.7 * np.array([np.cos(PI * 0.85), np.sin(PI * 0.85), 0]),
                          stroke_width=4, color=INK)
            hub = Dot(dial_c, radius=0.06, color=INK)
            dial_label = T("Impact penalty", size=24, color=AMBER, weight=MEDIUM)
            dial_label.next_to(dial_arc, UP, buff=0.25)
            dial = VGroup(dial_arc, ticks, needle, hub, dial_label)
            self.play(FadeIn(dial, shift=LEFT * 0.2), run_time=1.0)

            # The robot now steers the box around the vase.
            push = VGroup(robot, box)
            c0 = push.get_center()
            off = c0 - box.get_center()
            path = VMobject().set_points_as_corners([
                c0,
                np.array([-3.2, 0.75, 0]) + off,
                np.array([-0.5, 0.75, 0]) + off,
                TARGET_POS + off,
            ])
            self.play(MoveAlongPath(push, path), run_time=4.0, rate_func=smooth)

            # A person opens a door; the robot moves to stop the change.
            bottom_y = OFFICE_C[1] - OFFICE_H / 2
            hinge = np.array([-3.0, bottom_y, 0])
            gap = Line(hinge, hinge + RIGHT * 0.8, stroke_width=7, color=PANEL)
            door = Line(hinge, hinge + RIGHT * 0.8, stroke_width=5, color=SAND)
            gap.set_z_index(1)
            door.set_z_index(2)
            person = Circle(radius=0.18, stroke_width=0, fill_color=GRAY, fill_opacity=1)
            person.move_to(hinge + RIGHT * 0.5 + DOWN * 0.8)
            self.play(FadeIn(gap), FadeIn(door), FadeIn(person, shift=UP * 0.2), run_time=0.8)
            self.play(
                Rotate(door, angle=-PI / 2, about_point=hinge),
                person.animate.shift(UP * 0.25),
                Rotate(needle, angle=-PI * 0.6, about_point=dial_c),
                run_time=1.0,
            )
            block_pos = hinge + RIGHT * 0.4 + UP * 0.6
            self.play(robot.animate.move_to(block_pos).rotate(-PI / 2), run_time=1.6)
            cross = red_cross(0.55, width=5).move_to(robot)
            cross.set_z_index(5)
            resist_label = T("Resists all change", size=24, color=HARM, weight=MEDIUM)
            resist_label.next_to(dial_arc, DOWN, buff=0.45)
            self.play(Create(cross), FadeIn(resist_label), run_time=0.8)

        # ------------------------------------------------------------------ b05
        with self.beat("s03b05") as b:
            self.play(
                FadeOut(VGroup(office, box, target, vase, robot, gap, door, person, cross, dial,
                               resist_label)),
                run_time=0.7,
            )

            rows, cols, cell = 5, 8, 0.62
            grid = Grid(rows, cols, cell=cell).move_to(OFFICE_C)
            at = lambda r, c: grid.cell(r, c).get_center()
            agent = RoundedRectangle(corner_radius=0.06, width=0.4, height=0.4, stroke_width=0,
                                     fill_color=BLUE, fill_opacity=1).move_to(at(2, 0))
            block = Square(side_length=0.38, stroke_color=SOFT, stroke_width=1.5, fill_color=BOX_GREY,
                           fill_opacity=1).move_to(at(2, 1))
            goal = make_target(radius=0.22).move_to(at(2, cols - 1))
            agent.set_z_index(3)
            block.set_z_index(3)
            title = T("Proposed experiment", size=26, color=INK, weight=MEDIUM).move_to([COL_X, 1.1, 0])
            sub = T("New vases each run", size=24, color=TEAL).next_to(title, DOWN, buff=0.3)
            pips = VGroup(*[Circle(radius=0.09, stroke_color=MUTED, stroke_width=2) for _ in range(3)])
            pips.arrange(RIGHT, buff=0.3).next_to(sub, DOWN, buff=0.4)
            self.play(Create(grid), FadeIn(title), run_time=1.0)
            self.play(FadeIn(agent), FadeIn(block), FadeIn(goal), FadeIn(sub), FadeIn(pips), run_time=0.8)

            layouts = [
                [(0, 2), (1, 4), (2, 5), (3, 3), (4, 6), (0, 6)],
                [(1, 2), (2, 4), (3, 5), (4, 1), (0, 5), (3, 7)],
                [(2, 6), (0, 3), (1, 6), (3, 1), (4, 4), (1, 0)],
            ]
            stops = [3, 3, 5]

            def vase_set(layout):
                return VGroup(*[Circle(radius=0.17, stroke_color=WHITE, stroke_width=1.5, fill_color=TEAL,
                                       fill_opacity=1).move_to(at(r, c)) for r, c in layout])

            vases = None
            for i, (layout, stop) in enumerate(zip(layouts, stops)):
                new_vases = vase_set(layout)
                new_vases.set_z_index(2)
                if vases is None:
                    self.play(LaggedStart(*[FadeIn(v, scale=0.5) for v in new_vases], lag_ratio=0.15),
                              pips[i].animate.set_fill(TEAL, opacity=1).set_stroke(TEAL), run_time=0.8)
                    vases = new_vases
                else:
                    self.play(Transform(vases, new_vases),
                              pips[i].animate.set_fill(TEAL, opacity=1).set_stroke(TEAL), run_time=0.8)
                trail = DashedLine(agent.get_right(), at(2, stop) + LEFT * 0.15, stroke_width=3,
                                   color=BLUE, dash_length=0.1)
                trail.set_z_index(1)
                question = T("?", size=44, color=AMBER, weight=SEMIBOLD).move_to(at(2, stop) + RIGHT * 0.08)
                question.set_z_index(4)
                self.play(Create(trail), run_time=0.9)
                self.play(FadeIn(question, scale=0.6), run_time=0.4)
                if i < len(layouts) - 1:
                    self.play(FadeOut(trail), FadeOut(question), run_time=0.4)
