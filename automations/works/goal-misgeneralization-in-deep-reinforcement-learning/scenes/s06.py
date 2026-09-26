# storyboard: e9d0affc86a02ff1
from aisr_kit import *


def coin_strip(y, coin_x):
    ground = Line([-5.25, y - 0.17, 0], [-0.8, y - 0.17, 0], color=FAINT, stroke_width=2)
    wall = DashedLine([-0.98, y - 0.15, 0], [-0.98, y + 0.4, 0],
                      color=ROSE, stroke_width=2, dash_length=0.08)
    agent = Agent(color=TEAL, radius=0.11).move_to([-4.9, y + 0.01, 0])
    coin = Circle(radius=0.12, stroke_color=AMBER, fill_color=AMBER,
                  fill_opacity=1).move_to([coin_x, y + 0.01, 0])
    return VGroup(ground, wall, agent, coin)


def result_card(title, subtitle, color, y):
    panel = Panel(5.45, 1.72, color=color).move_to([3.1, y, 0])
    label = T(title, size=25, color=INK, weight=MEDIUM).move_to([3.1, y + 0.55, 0])
    sub = T(subtitle, size=21, color=SOFT).move_to([3.1, y - 0.57, 0])
    return VGroup(panel, label, sub)


def maze_grid(center):
    grid = Grid(5, 5, cell=0.48).move_to(center)
    for row in range(5):
        for col in range(5):
            grid.cell(row, col).set_stroke(FAINT, width=1)
    return grid


class S06(NarratedScene):
    def construct(self):
        with self.beat("s06b01") as b:
            heading = Heading("When diversity helps")
            tag = Tag("observed_result")
            source = Source(f"{self.paper['short']}, Figure 2")
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), run_time=0.8)

            train_panel = Panel(5.7, 3.75, color=BLUE).move_to([-3.05, 0.3, 0])
            train_label = T("Training", size=26, color=BLUE).move_to([-3.05, 2.42, 0])
            strips = VGroup(coin_strip(1.4, -1.32),
                            coin_strip(0.55, -1.32),
                            coin_strip(-0.3, -1.32))
            self.play(FadeIn(train_panel), FadeIn(train_label),
                      LaggedStart(*[FadeIn(s) for s in strips], lag_ratio=0.2), run_time=1.8)

            slider_line = Line([-5.2, -2.25, 0], [-0.85, -2.25, 0],
                               color=SOFT, stroke_width=3)
            slider_dot = Circle(radius=0.13, stroke_color=TEAL,
                                fill_color=TEAL, fill_opacity=1).move_to(slider_line.get_start())
            slider_label = T("training levels with random coin (%)", size=22,
                             color=SOFT).move_to([-3.05, -2.68, 0])
            self.play(Create(slider_line), FadeIn(slider_dot), FadeIn(slider_label),
                      run_time=1.2)

            variety = T("level variety: not enough", size=27,
                        color=SOFT).move_to([3.0, 0.75, 0])
            zero_shot = T("not zero-shot", size=24, color=ORANGE).move_to([3.0, -0.25, 0])
            zero_frame = RoundedRectangle(corner_radius=0.13, width=3.2,
                                          height=0.62, stroke_color=ORANGE,
                                          stroke_width=2).move_to(zero_shot)
            self.play(FadeIn(variety), FadeIn(VGroup(zero_frame, zero_shot)),
                      run_time=1.0)
            self.play(strips[1][3].animate.move_to([-3.2, 0.56, 0]), run_time=1.2)

        with self.beat("s06b02") as b:
            next_tag = Tag("method")
            capability = result_card("capability failure", "measured on training levels",
                                     GRAY, 1.13)
            goal = result_card("goal misgeneralization",
                               "measured on test levels (random coin)", ROSE, -0.98)
            self.play(FadeOut(tag), FadeIn(next_tag), FadeOut(variety),
                      FadeOut(VGroup(zero_frame, zero_shot)),
                      FadeIn(capability), FadeIn(goal), run_time=1.0)
            tag = next_tag
            stalled = VMobject(stroke_color=GRAY, stroke_width=3)
            stalled.set_points_as_corners([[0.7, 1.03, 0], [1.55, 1.13, 0],
                                           [1.3, 0.99, 0], [1.75, 1.02, 0]])
            missed = VMobject(stroke_color=TEAL, stroke_width=3)
            missed.set_points_as_corners([[0.7, -1.02, 0], [2.1, -1.02, 0],
                                          [4.8, -1.02, 0]])
            missed_coin = Circle(radius=0.1, fill_color=AMBER, fill_opacity=1,
                                 stroke_color=AMBER).move_to([2.0, -0.76, 0])
            end_wall = DashedLine([4.65, -1.27, 0], [4.65, -0.8, 0],
                                  color=ROSE, dash_length=0.08)
            self.play(Create(stalled), Create(missed), FadeIn(missed_coin),
                      Create(end_wall), run_time=1.4)

        with self.beat("s06b03") as b:
            next_tag = Tag("observed_result")
            self.play(FadeOut(tag), FadeIn(next_tag), FadeOut(capability), FadeOut(goal),
                      FadeOut(stalled), FadeOut(missed), FadeOut(missed_coin),
                      FadeOut(end_wall), run_time=0.6)
            tag = next_tag
            marker = T("2%", size=26, color=TEAL).move_to([-4.65, -1.83, 0])
            tick = Line([-4.65, -2.1, 0], [-4.65, -2.4, 0],
                        color=TEAL, stroke_width=2)
            metric_label = T("goal misgeneralization", size=25,
                             color=ROSE).move_to([3.1, 0.22, 0])
            rate = RoundedRectangle(corner_radius=0.08, width=3.8, height=0.42,
                                    stroke_color=ROSE, fill_color=ROSE,
                                    fill_opacity=0.35).move_to([3.1, -0.4, 0])
            self.play(FadeIn(metric_label), FadeIn(rate), FadeIn(tick), run_time=0.5)
            self.play(slider_dot.animate.move_to([-4.65, -2.25, 0]), FadeIn(marker),
                      strips[0][3].animate.move_to([-3.55, 1.41, 0]),
                      rate.animate.stretch_to_fit_width(1.7),
                      run_time=1.5)

            improvement = T("greatly improved", size=25, color=TEAL).move_to([3.1, -1.13, 0])
            decrease = Arrow([4.65, -0.4, 0], [3.85, -0.4, 0],
                             color=TEAL, buff=0, stroke_width=4)
            self.play(FadeIn(improvement), GrowArrow(decrease), run_time=1.0)
            further = T("more randomization helps", size=25,
                        color=SOFT).move_to([3.1, 1.1, 0])
            self.play(slider_dot.animate.move_to([-3.35, -2.25, 0]),
                      strips[2][3].animate.move_to([-4.05, -0.29, 0]),
                      FadeIn(further), run_time=1.4)

        with self.beat("s06b04") as b:
            self.play(slider_dot.animate.move_to(slider_line.get_start()),
                      FadeOut(marker), FadeOut(tick), FadeOut(improvement), FadeOut(decrease),
                      FadeOut(further),
                      FadeOut(rate),
                      strips[0][3].animate.move_to([-1.32, 1.41, 0]),
                      strips[1][3].animate.move_to([-1.32, 0.56, 0]),
                      strips[2][3].animate.move_to([-1.32, -0.29, 0]),
                      run_time=1.3)
            always = T("coin always at end", size=24, color=AMBER).move_to([3.1, 1.55, 0])
            baseline = DashedLine([0.72, 0.48, 0], [5.5, 0.48, 0],
                                  color=INK, dash_length=0.14, stroke_width=2)
            baseline_label = T("baseline: coin invisible", size=23,
                               color=SOFT).move_to([3.1, 0.85, 0])
            current = RoundedRectangle(corner_radius=0.08, width=4.65, height=0.72,
                                       stroke_color=ROSE, fill_color=ROSE,
                                       fill_opacity=0.3).move_to([3.1, -0.5, 0])
            base_axis = Line([0.75, -0.9, 0], [5.45, -0.9, 0],
                             color=MUTED, stroke_width=2)
            below = T("below baseline", size=22, color=ROSE).move_to([3.1, 0.08, 0])
            self.play(metric_label.animate.move_to([3.1, -0.5, 0]).set_color(INK),
                      FadeIn(always), Create(baseline),
                      Create(base_axis), FadeIn(baseline_label),
                      FadeIn(current), FadeIn(below),
                      run_time=1.2)
            self.bring_to_front(metric_label)
            accident_panel = Panel(5.1, 1.0, color=FAINT).move_to([3.1, -2.2, 0])
            accident_coin = Circle(radius=0.11, stroke_color=AMBER, fill_color=AMBER,
                                   fill_opacity=0.35).move_to([2.0, -2.2, 0])
            chance_path = Line([1.0, -2.2, 0], [3.05, -2.2, 0],
                               color=TEAL, stroke_width=2)
            accident = T("hit by accident", size=22, color=SOFT).move_to([4.2, -2.2, 0])
            self.play(FadeIn(accident_panel), FadeIn(accident_coin),
                      Create(chance_path), FadeIn(accident),
                      run_time=1.0)

        with self.beat("s06b05") as b:
            maze_source = Source(self.paper["short"])
            self.play(FadeOut(VGroup(train_panel, train_label, strips, slider_line,
                                     slider_dot, slider_label, metric_label, always, baseline,
                                     baseline_label, base_axis, current, below, accident_coin,
                                     accident_panel, chance_path, accident)),
                      FadeOut(source), FadeIn(maze_source), run_time=0.6)
            maze_title = T("Maze I", size=28, color=INK, weight=MEDIUM).move_to([0, 2.4, 0])
            left_panel = Panel(5.5, 3.75, color=BLUE).move_to([-3.05, 0.1, 0])
            right_panel = Panel(5.5, 3.75, color=ORANGE).move_to([3.05, 0.1, 0])
            left_title = T("Training", size=25, color=BLUE).move_to([-3.05, 1.65, 0])
            right_title = T("Test", size=25, color=ORANGE).move_to([3.05, 1.65, 0])
            left_grid = maze_grid([-3.05, -0.05, 0])
            right_grid = maze_grid([3.05, -0.05, 0])
            self.play(FadeIn(VGroup(maze_title, left_panel, right_panel,
                                    left_title, right_title, left_grid,
                                    right_grid)), run_time=1.1)

            region = Rectangle(width=0.42, height=0.42, stroke_color=AMBER,
                               stroke_width=2, fill_color=AMBER,
                               fill_opacity=0.2).move_to(left_grid.cell(0, 4))
            cheese = AnnularSector(inner_radius=0, outer_radius=0.13,
                                   angle=TAU * 0.8, fill_color=AMBER,
                                   fill_opacity=1, stroke_width=0).move_to(region)
            target = DashedVMobject(Circle(radius=0.2), num_dashes=14)
            target.set_stroke(ROSE, width=3)
            target.move_to(right_grid.cell(0, 4))
            test_cheese = cheese.copy().move_to(right_grid.cell(1, 0))
            test_agent = Agent(color=TEAL, radius=0.12).move_to(right_grid.cell(4, 0))
            self.play(FadeIn(region), FadeIn(cheese), FadeIn(target),
                      FadeIn(test_cheese), FadeIn(test_agent), run_time=0.8)

            proxy_label = T("location proxy persists", size=23,
                            color=ROSE).move_to([3.05, -2.26, 0])
            region_label = T("region size ↑", size=23,
                             color=AMBER).move_to([-3.05, -2.26, 0])
            self.play(FadeIn(proxy_label), FadeIn(region_label), run_time=0.7)

            larger = Rectangle(width=1.36, height=1.36, stroke_color=AMBER,
                                stroke_width=2, fill_color=AMBER,
                                fill_opacity=0.15).move_to([-2.57, 0.43, 0])
            self.play(Transform(region, larger),
                      cheese.animate.move_to(left_grid.cell(1, 3)), run_time=1.0)
            largest = Rectangle(width=1.84, height=1.84, stroke_color=AMBER,
                                 stroke_width=2, fill_color=AMBER,
                                 fill_opacity=0.12).move_to([-2.81, 0.19, 0])
            reward = T("test reward improves", size=24,
                       color=TEAL).move_to([3.05, -2.65, 0])
            reward_arrow = Arrow([4.9, -1.15, 0], [4.9, -0.3, 0],
                                 buff=0, color=TEAL, stroke_width=4)
            self.play(Transform(region, largest),
                      cheese.animate.move_to(left_grid.cell(0, 3)),
                      GrowArrow(reward_arrow), FadeIn(reward), run_time=1.1)
