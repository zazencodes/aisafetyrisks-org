# storyboard: 6a7d90a17ee80e46
from aisr_kit import *


def coin(x, y):
    return Circle(radius=0.15, stroke_color=AMBER, stroke_width=2,
                  fill_color=AMBER, fill_opacity=1).move_to([x, y, 0])


def proxy_arrow(start, end):
    return DashedLine(start, end, color=ROSE, stroke_width=4,
                      dash_length=0.16).add_tip(tip_length=0.16)


def level(center, goal_x, wall_x):
    cx, cy = center
    ground = Line([cx - 2.35, cy - 0.7, 0], [cx + 2.35, cy - 0.7, 0],
                  color=FAINT, stroke_width=2)
    target = coin(cx + goal_x, cy - 0.42)
    wall = DashedLine([cx + wall_x, cy - 0.7, 0],
                      [cx + wall_x, cy + 0.8, 0], color=ROSE,
                      stroke_width=3, dash_length=0.12)
    actor = Agent(color=TEAL, radius=0.19).move_to([cx - 2.05, cy - 0.47, 0])
    return VGroup(ground, target, wall, actor)


def small_grid(x):
    return Grid(4, 6, cell=0.55).move_to([x, 0.0, 0])


def path(points, color):
    line = VMobject(stroke_color=color, stroke_width=4)
    line.set_points_as_corners([[x, y, 0] for x, y in points])
    return line


class S08(NarratedScene):
    def construct(self):
        with self.beat("s08b01") as b:
            heading = Heading("What it means, and its limits")
            tag = Tag("author_interpretation")
            self.play(FadeIn(heading), FadeIn(tag), run_time=0.7)

            train_panel = Panel(5.1, 3.0, color=BLUE).move_to([-3.25, 0.1, 0])
            test_panel = Panel(5.1, 3.0, color=AMBER).move_to([3.25, 0.1, 0])
            train_name = T("Training", size=27, color=BLUE).move_to([-3.25, 1.93, 0])
            test_name = T("Test", size=27, color=AMBER).move_to([3.25, 1.93, 0])
            training = level((-3.25, 0.1), 1.4, 2.12)
            testing = level((3.25, 0.1), -0.35, 2.12)
            train_gold = Arrow([-5.02, -0.03, 0], [-1.91, -0.03, 0], buff=0,
                               color=AMBER, stroke_width=4)
            train_proxy = proxy_arrow([-5.02, -0.22, 0], [-1.42, -0.22, 0])
            test_gold = CurvedArrow([1.43, -0.25, 0], [2.89, -0.3, 0],
                                    angle=-0.35, color=AMBER, stroke_width=4)
            test_proxy = proxy_arrow([1.43, -0.23, 0], [5.36, -0.23, 0])
            funnel = Polygon([-0.58, 0.25, 0], [0.58, 0.25, 0],
                             [0.3, -0.54, 0], [-0.3, -0.54, 0],
                             stroke_color=SOFT, stroke_width=2,
                             fill_color=PANEL, fill_opacity=1)
            through_gold = Arrow([-0.68, 0.04, 0], [0.68, 0.04, 0],
                                 buff=0, color=AMBER, stroke_width=4,
                                 max_tip_length_to_length_ratio=0.12)
            through_proxy = proxy_arrow([-0.68, -0.25, 0], [0.68, -0.25, 0])
            bias = T("inductive biases", size=21, color=SOFT).move_to([0, -0.91, 0])
            proxy_label = T("proxy", size=24, color=ROSE).move_to([3.55, -1.02, 0])
            goal_label = T("intended goal", size=24, color=AMBER).move_to([3.0, 0.95, 0])
            first = VGroup(train_panel, test_panel, train_name, test_name,
                           training, testing, train_gold, train_proxy,
                           test_gold, test_proxy, funnel, through_gold,
                           through_proxy, bias, proxy_label,
                           goal_label)
            self.play(FadeIn(train_panel), FadeIn(test_panel),
                      FadeIn(train_name), FadeIn(test_name),
                      FadeIn(training), FadeIn(testing), run_time=1.4)
            self.play(GrowArrow(train_gold), Create(train_proxy),
                      FadeIn(funnel), FadeIn(bias), run_time=1.6)
            self.play(GrowArrow(through_gold), Create(through_proxy), run_time=0.6)
            self.play(Create(test_gold), Create(test_proxy),
                      FadeIn(goal_label), FadeIn(proxy_label), run_time=1.4)

        with self.beat("s08b02") as b:
            next_tag = Tag("threat_model")
            self.play(FadeOut(tag), FadeIn(next_tag), FadeOut(first), run_time=0.7)
            tag = next_tag

            left_grid = small_grid(-3.3)
            right_grid = small_grid(3.3)
            cap_label = T("capability failure", size=27, color=GRAY).move_to([-3.3, 1.86, 0])
            wrong_label = T("capable + wrong goal", size=27, color=TEAL).move_to([3.3, 1.86, 0])
            left_agent = Agent(color=GRAY, radius=0.17).move_to(left_grid.cell(2, 0))
            right_agent = Agent(color=TEAL, radius=0.17).move_to(right_grid.cell(2, 0))
            bad_box = RoundedRectangle(corner_radius=0.08, width=1.0, height=1.1,
                                       stroke_color=ROSE, stroke_width=2,
                                       fill_color=ROSE, fill_opacity=0.12)
            bad_box.move_to(right_grid.cell(1, 5))
            bad_label = T("bad states", size=24, color=ROSE).move_to([4.65, -1.86, 0])
            stalled = path([(-4.68, -0.28), (-4.43, -0.18), (-4.55, -0.12),
                            (-4.36, -0.3), (-4.45, -0.38)], GRAY)
            purposeful = path([(1.92, -0.28), (2.47, -0.28), (2.47, 0.27),
                               (3.02, 0.27), (3.57, 0.27), (4.12, 0.27),
                               (4.67, 0.27)], TEAL)
            second = VGroup(left_grid, right_grid, cap_label, wrong_label,
                            left_agent, right_agent, bad_box, bad_label,
                            stalled, purposeful)
            self.play(FadeIn(left_grid), FadeIn(right_grid),
                      FadeIn(cap_label), FadeIn(wrong_label),
                      FadeIn(left_agent), FadeIn(right_agent),
                      FadeIn(bad_box), run_time=1.4)
            self.play(Create(stalled), MoveAlongPath(left_agent, stalled),
                      Create(purposeful), MoveAlongPath(right_agent, purposeful),
                      run_time=2.6)
            self.play(FadeIn(bad_label), Indicate(bad_box, color=ROSE), run_time=0.9)

        with self.beat("s08b03") as b:
            next_tag = Tag("limitation")
            self.play(FadeOut(tag), FadeIn(next_tag), FadeOut(second), run_time=0.7)
            tag = next_tag

            names = ("move right", "upper right corner", "yellow object", "gather keys")
            cards = VGroup()
            for x, name in zip((-4.83, -1.62, 1.62, 4.83), names):
                panel = Panel(2.85, 2.0, color=ROSE).move_to([x, 0.25, 0])
                label = T(name, size=23, color=ROSE, width=15).move_to([x, 0.1, 0])
                question = T("?", size=28, color=SOFT).move_to([x + 1.08, 0.93, 0])
                cards.add(VGroup(panel, label, question))
            comparison = T("move right vs move to wall", size=27,
                           color=SOFT).move_to([-2.86, -1.73, 0])
            check = VGroup(Line([-0.59, -1.78, 0], [-0.43, -1.96, 0],
                                color=TEAL, stroke_width=4),
                           Line([-0.43, -1.96, 0], [-0.1, -1.49, 0],
                                color=TEAL, stroke_width=4))
            third = VGroup(cards, comparison, check)
            self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.15),
                      run_time=1.9)
            self.play(FadeIn(comparison), Create(check), run_time=1.2)

        with self.beat("s08b04") as b:
            self.play(FadeOut(third), run_time=0.6)

            fulcrum = Triangle(stroke_color=FAINT, fill_color=FAINT,
                               fill_opacity=0.5).scale(0.26).move_to([-3.6, -0.9, 0])
            beam = Line([-5.38, -0.57, 0], [-1.82, -0.57, 0],
                        color=SOFT, stroke_width=3)
            pans = VGroup(Line([-5.3, -0.59, 0], [-5.3, -1.06, 0], color=SOFT),
                          Line([-4.45, -1.06, 0], [-6.15, -1.06, 0], color=SOFT),
                          Line([-1.9, -0.59, 0], [-1.9, -1.06, 0], color=SOFT),
                          Line([-1.07, -1.06, 0], [-2.73, -1.06, 0], color=SOFT))
            flags = VGroup(*[
                Polygon([x, y, 0], [x + 0.2, y + 0.12, 0], [x, y + 0.24, 0],
                        stroke_color=AMBER, fill_color=AMBER, fill_opacity=0.4)
                for x, y in ((-2.44, -0.97), (-2.13, -0.93), (-1.82, -0.97),
                             (-2.3, -0.68), (-1.99, -0.65), (-1.67, -0.69),
                             (-2.15, -0.39), (-1.83, -0.37))
            ])
            prior = T("prior over objectives?", size=25, color=SOFT).move_to([-3.6, 1.64, 0])
            scale_label = T("intractable at scale", size=25, color=ROSE).move_to([-3.6, -1.83, 0])
            scope = Panel(5.1, 3.15, color=FAINT).move_to([3.25, 0.02, 0])
            scope_a = T("Procgen games", size=27, color=SOFT).move_to([3.25, 0.96, 0])
            scope_b = T("feedforward PPO agents", size=25, color=SOFT).move_to([3.25, 0.06, 0])
            scope_c = T("not deployed systems", size=25, color=MUTED).move_to([3.25, -0.84, 0])
            fourth = VGroup(fulcrum, beam, pans, flags, prior, scale_label,
                            scope, scope_a, scope_b, scope_c)
            self.play(FadeIn(fulcrum), Create(beam), Create(pans),
                      FadeIn(prior), FadeIn(scope), run_time=1.4)
            self.play(LaggedStart(*[FadeIn(f) for f in flags], lag_ratio=0.11),
                      FadeIn(scale_label), run_time=1.4)
            self.play(FadeIn(scope_a), FadeIn(scope_b), FadeIn(scope_c), run_time=1.2)

        with self.beat("s08b05") as b:
            next_tag = Tag("observed_result")
            self.play(FadeOut(tag), FadeIn(next_tag), FadeOut(fourth), run_time=0.7)
            tag = next_tag

            train_panel = Panel(5.4, 2.15, color=BLUE).move_to([-3.2, 0.62, 0])
            test_panel = Panel(5.4, 2.15, color=AMBER).move_to([3.2, 0.62, 0])
            train_name = T("Training", size=26, color=BLUE).move_to([-3.2, 1.91, 0])
            test_name = T("Test", size=26, color=AMBER).move_to([3.2, 1.91, 0])
            training = level((-3.2, 0.62), 1.45, 2.15)
            testing = level((3.2, 0.62), -0.2, 2.15)
            runner = testing[-1]
            run_path = Line(runner.get_center(), [5.05, 0.15, 0], color=TEAL,
                            stroke_width=3)
            move_right = proxy_arrow([1.25, -0.08, 0], [5.33, -0.08, 0])
            skills = T("skills: transfer", size=24, color=TEAL).move_to([2.25, -0.94, 0])
            goal = T("goal: proxy", size=24, color=ROSE).move_to([4.52, -0.94, 0])
            marker = T("2%", size=27, color=AMBER).move_to([-4.65, -1.58, 0])
            slider = Line([-3.8, -1.59, 0], [-1.15, -1.59, 0],
                          color=FAINT, stroke_width=3)
            slider_dot = Dot(point=[-3.68, -1.59, 0], radius=0.08, color=AMBER)
            improvement = T("goal generalization greatly improved", size=23,
                            color=SOFT).move_to([-3.15, -2.2, 0])
            citation = T("Langosco et al. (2021)", size=21,
                         color=MUTED).move_to([0, -2.91, 0])
            paper_title = T("Goal Misgeneralization in Deep Reinforcement Learning (ICML 2022)",
                            size=20, color=MUTED).move_to([0, -3.38, 0])
            self.play(FadeIn(train_panel), FadeIn(test_panel),
                      FadeIn(train_name), FadeIn(test_name),
                      FadeIn(training), FadeIn(testing), run_time=1.2)
            self.play(Create(run_path), MoveAlongPath(runner, run_path),
                      Create(move_right), run_time=1.6)
            self.play(FadeIn(skills), FadeIn(goal),
                      FadeIn(marker), Create(slider), FadeIn(slider_dot),
                      FadeIn(improvement), run_time=1.2)
            self.play(FadeIn(citation), FadeIn(paper_title), run_time=0.7)
