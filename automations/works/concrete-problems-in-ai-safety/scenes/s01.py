# storyboard: cc64befbae12bde8
from aisr_kit import *

BROWN = "#9A6B45"
OFFICE_CENTER = np.array([0.0, -0.35, 0.0])
PATH_Y = 0.6


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


def make_office():
    floor = RoundedRectangle(corner_radius=0.3, width=11, height=5, stroke_color=GRAY, stroke_width=2,
                             fill_color=PANEL, fill_opacity=1).move_to(OFFICE_CENTER)
    desk = Rectangle(width=2.2, height=1.0, stroke_color=GRAY, stroke_width=2, fill_color=FAINT, fill_opacity=1)
    desk.move_to([1.8, -1.2, 0])
    hidden = VGroup(*[Dot([x, y, 0], radius=0.11, color=BROWN) for x, y in [(1.2, -2.3), (1.8, -2.42), (2.4, -2.28)]])
    messes = VGroup(*[Dot([x, PATH_Y + dy, 0], radius=0.11, color=BROWN)
                      for x, dy in [(-2.9, 0.1), (-1.8, -0.12), (-0.7, 0.08), (0.4, -0.1), (1.5, 0.05)]])
    vase = Circle(radius=0.26, stroke_color=WHITE, stroke_width=2, fill_color=TEAL, fill_opacity=1)
    vase.move_to([2.1, 0.95, 0])
    robot = make_robot()
    robot.shift(np.array([-4.9, PATH_Y, 0]) - robot.body.get_center())
    office = VGroup(floor, desk, hidden, messes, vase, robot)
    office.floor, office.desk, office.hidden, office.messes = floor, desk, hidden, messes
    office.vase, office.robot = vase, robot
    return office


def make_score(slots):
    label = T("Score", size=22, color=AMBER, weight=MEDIUM)
    pips = VGroup(*[Square(side_length=0.2, stroke_color=AMBER, stroke_width=2, fill_color=AMBER, fill_opacity=0)
                    for _ in range(slots)]).arrange(RIGHT, buff=0.08)
    pips.next_to(label, RIGHT, buff=0.2)
    score = VGroup(label, pips)
    score.pips = pips
    return score


def gap_line(start, end, color=MUTED):
    line = Line(start, end, stroke_width=2, color=color)
    bars = VGroup(*[Line(p + UP * 0.15, p + DOWN * 0.15, stroke_width=2, color=color) for p in (start, end)])
    return VGroup(line, bars)


def side_panel(center, icon, label_text):
    panel = Panel(4.3, 2.2).move_to(center)
    icon.move_to(center + np.array([-1.2, 0.25, 0]))
    label = T(label_text, size=24, color=SOFT).move_to(center + np.array([-1.2, -0.7, 0]))
    pips = VGroup(*[Square(side_length=0.16, stroke_width=0, fill_color=AMBER, fill_opacity=1)
                    for _ in range(3)]).arrange(RIGHT, buff=0.06)
    pips.move_to(center + np.array([0.15, 0.25, 0]))
    ring = Circle(radius=0.2, stroke_color=ROSE, stroke_width=3).move_to(center + np.array([1.65, 0.25, 0]))
    gap = gap_line(pips.get_right() + RIGHT * 0.2, ring.get_left() + LEFT * 0.2)
    return VGroup(panel, icon, label), VGroup(pips, gap, ring)


class S01(NarratedScene):
    def construct(self):
        s = 0.3
        with self.beat("s01b01") as b:
            heading = Heading("A good score and a broken vase")
            tag = Tag("background")
            self.play(FadeIn(heading), FadeIn(tag), run_time=0.8)

            centers = [np.array([x, -0.1, 0]) for x in (-4.3, 0.0, 4.3)]
            panels = [Panel(3.6, 3.0).move_to(c) for c in centers]
            labels = [T(t, size=26, color=SOFT).next_to(p, DOWN, buff=0.3)
                      for t, p in zip(["Ads", "Factories", "Cleaning"], panels)]

            ads = VGroup(*[Rectangle(width=0.8, height=0.5, stroke_color=MUTED, stroke_width=1.5,
                                     fill_color=FAINT, fill_opacity=1) for _ in range(9)])
            ads.arrange_in_grid(rows=3, cols=3, buff=0.18).move_to(centers[0])
            chosen = ads[4]
            self.play(FadeIn(panels[0]), FadeIn(ads), FadeIn(labels[0]), run_time=0.8)
            self.bring_to_front(chosen)
            self.play(chosen.animate.scale(1.6).set_fill(VIOLET, 0.9).set_stroke(VIOLET), run_time=1.4)

            g1 = gear(0.6, 10).move_to(centers[1] + np.array([-0.4, -0.25, 0]))
            g2 = gear(0.4, 7).move_to(centers[1] + np.array([0.6, 0.5, 0]))
            self.play(FadeIn(panels[1]), FadeIn(g1), FadeIn(g2), FadeIn(labels[1]), run_time=0.8)
            self.play(Rotate(g1, -PI, about_point=g1.get_center()),
                      Rotate(g2, PI * 1.5, about_point=g2.get_center()), run_time=2.0, rate_func=linear)

            office = make_office()
            office.scale(s).move_to(centers[2])
            self.play(FadeIn(panels[2]), FadeIn(office), FadeIn(labels[2]), run_time=0.8)
            self.play(office.robot.animate.shift(RIGHT * 1.0 * s), run_time=2.0)

            self.play(FadeOut(panels[0], ads, labels[0], panels[1], g1, g2, labels[1], labels[2], panels[2]),
                      run_time=0.8)
            self.play(office.animate.scale(1 / s).move_to(OFFICE_CENTER), run_time=1.5)

        robot = office.robot
        with self.beat("s01b02") as b:
            new_tag = Tag("future_scenario")
            score = make_score(len(office.messes))
            score.next_to(office.floor.get_corner(UR), DL, buff=0.3)
            hyp = T("Hypothetical", size=22, color=MUTED)
            hyp.next_to(office.floor.get_corner(UL), UR, buff=0.12).shift(RIGHT * 0.15)
            self.play(FadeOut(tag), FadeIn(new_tag), FadeIn(score), FadeIn(hyp), run_time=0.6)
            tag = new_tag

            for mess, pip in zip(office.messes, score.pips):
                dx = mess.get_x() - robot.body.get_x()
                self.play(robot.animate.shift(RIGHT * dx), run_time=0.7, rate_func=linear)
                self.play(FadeOut(mess, scale=0.3), pip.animate.set_fill(AMBER, 1), run_time=0.25)

            vase = office.vase
            self.play(robot.animate.shift(RIGHT * (1.9 - robot.body.get_x())), run_time=0.5, rate_func=linear)
            self.play(vase.animate.shift(UP * 0.08 + RIGHT * 0.2).stretch(0.55, 1).set_fill(ROSE).set_stroke(ROSE),
                      run_time=0.7)
            c = vase.get_center()
            cross = VGroup(Line(c + UL * 0.3, c + DR * 0.3, stroke_width=5, color=ROSE),
                           Line(c + UR * 0.3, c + DL * 0.3, stroke_width=5, color=ROSE))
            self.play(Create(cross), robot.animate.shift(RIGHT * (3.4 - robot.body.get_x())), run_time=0.6)
            self.play(LaggedStart(*[Indicate(d, color="#C08A5E", scale_factor=1.5) for d in office.hidden],
                                  lag_ratio=0.3), run_time=1.2)

        with self.beat("s01b03") as b:
            new_tag = Tag("author_interpretation")
            source = Source(f"{self.paper['short']}, Introduction and Conclusion")
            self.play(FadeOut(tag), FadeIn(new_tag), FadeIn(source), run_time=0.5)
            tag = new_tag

            self.play(FadeOut(robot.cone), robot.body.animate.set_fill(opacity=0.45), run_time=0.5)
            self.play(score.animate.scale(1.7).move_to([-3.0, 1.15, 0]), run_time=1.0)
            looks = T("Score looks good", size=32, color=AMBER).next_to(score, DOWN, buff=0.4)
            self.play(FadeIn(looks), run_time=0.5)

            ring_vase = Circle(radius=0.6, stroke_color=ROSE, stroke_width=3).move_to(VGroup(vase, cross))
            ring_hidden = Ellipse(width=2.0, height=0.75, stroke_color=ROSE, stroke_width=3).move_to(office.hidden)
            self.play(Create(ring_vase), Create(ring_hidden), run_time=1.0)
            room = T("Room is not", size=32, color=ROSE).move_to([-1.0, -2.3, 0])
            self.play(FadeIn(room), run_time=0.5)

            y = score.get_y()
            gap = gap_line(np.array([score.get_right()[0] + 0.3, y, 0]),
                           np.array([ring_vase.get_left()[0] - 0.2, y, 0]))
            self.play(Create(gap), run_time=1.0)
            self.wait(3.0)

            office.remove(office.messes)
            scene_group = VGroup(office, cross, score, looks, ring_vase, ring_hidden, room, gap)
            self.play(FadeOut(hyp),
                      scene_group.animate.scale(0.68, about_point=OFFICE_CENTER).shift(LEFT * 2.65),
                      run_time=1.3)

            plant = VGroup(gear(0.32, 8), gear(0.22, 6))
            plant[1].move_to(plant[0].get_center() + np.array([0.42, 0.42, 0]))
            plus = VGroup(Rectangle(width=0.7, height=0.22, stroke_width=0, fill_color=SOFT, fill_opacity=1),
                          Rectangle(width=0.22, height=0.7, stroke_width=0, fill_color=SOFT, fill_opacity=1))
            plus = VGroup(RoundedRectangle(corner_radius=0.12, width=0.95, height=0.95, stroke_color=GRAY,
                                           stroke_width=2), plus)
            ind_panel, ind_gap = side_panel(np.array([4.1, 0.95, 0]), plant, "Industry")
            care_panel, care_gap = side_panel(np.array([4.1, -1.65, 0]), plus, "Health care")
            self.play(FadeIn(ind_panel), run_time=0.7)
            self.play(Create(ind_gap), Rotate(plant[0], -PI / 2, about_point=plant[0].get_center()), run_time=0.9)
            self.play(FadeIn(care_panel), run_time=0.7)
            self.play(Create(care_gap), run_time=0.9)
