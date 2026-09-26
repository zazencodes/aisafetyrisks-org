# storyboard: 6c5fb8cb90ad17ba
from aisr_kit import *


def coin(x, y, opacity=1):
    return Circle(radius=0.13, stroke_color=AMBER, stroke_width=2,
                  fill_color=AMBER, fill_opacity=opacity).move_to([x, y, 0])


def wall(x, bottom, top, dashed=False):
    if dashed:
        return DashedLine([x, bottom, 0], [x, top, 0], color=ROSE,
                          stroke_width=4, dash_length=0.12)
    return Rectangle(width=0.17, height=top - bottom, stroke_width=0,
                     fill_color=SOFT, fill_opacity=0.75).move_to(
                         [x, (bottom + top) / 2, 0])


class S07(NarratedScene):
    def construct(self):
        with self.beat("s07b01") as b:
            heading = Heading("Actor and critic disagree")
            tag = Tag("observed_result")
            source = Source("Langosco et al.")
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), run_time=0.8)

            segment_names = ("Beginning", "Middle", "End", "After End")
            centers = (-4.75, -1.65, 1.45, 4.55)
            strengths = (0.08, 0.13, 0.43, 0.20)
            cards = VGroup()
            for name, x, strength in zip(segment_names, centers, strengths):
                panel = Panel(2.78, 2.82, color=FAINT).move_to([x, 0.25, 0])
                title = T(name, size=25, color=INK).move_to([x, 1.37, 0])
                samples = VGroup()
                for offset, has_coin in ((-0.58, True), (0.58, False)):
                    glow = Circle(radius=0.57, stroke_width=0,
                                  fill_color=INK, fill_opacity=strength).move_to(
                                      [x + offset, 0.16, 0])
                    square = Square(side_length=0.78, stroke_color=SOFT,
                                    stroke_width=1.5, fill_color=PANEL,
                                    fill_opacity=0.85).move_to([x + offset, 0.16, 0])
                    sample = VGroup(glow, square)
                    if has_coin:
                        sample.add(coin(x + offset, 0.16))
                    samples.add(sample)
                coin_label = T("coin", size=21, color=AMBER).move_to([x - 0.58, -0.65, 0])
                empty_label = T("no coin", size=21, color=SOFT).move_to(
                    [x + 0.58, -0.65, 0])
                cards.add(VGroup(panel, title, samples, coin_label, empty_label))
            takeaway = T("critic value: highest at End", size=29,
                         color=INK, weight=MEDIUM).move_to([0, -1.64, 0])
            matched = T("coin vs no coin: no discernible difference", size=24,
                        color=SOFT).move_to([0, -2.16, 0])
            sample_note = T("schematic, n = 950 images", size=21,
                            color=MUTED).move_to([0, -2.68, 0])
            first = VGroup(cards, takeaway, matched, sample_note)
            self.play(LaggedStart(*[FadeIn(card) for card in cards], lag_ratio=0.13),
                      run_time=2.2)
            self.play(FadeIn(takeaway), FadeIn(matched), FadeIn(sample_note),
                      run_time=1.0)

        with self.beat("s07b02") as b:
            ground = Line([-5.75, -0.91, 0], [5.5, -0.91, 0],
                          color=FAINT, stroke_width=3)
            end_wall = wall(3.65, -0.9, 1.3)
            visible_coin = coin(-1.55, -0.23)
            agent = Agent(color=TEAL, radius=0.21).move_to([-4.7, -0.65, 0])
            obstacle = Rectangle(width=0.42, height=0.46, stroke_width=0,
                                 fill_color=GRAY, fill_opacity=0.75).move_to(
                                     [0.25, -0.68, 0])
            frame = VGroup(ground, end_wall, visible_coin, agent, obstacle)
            wall_heat = VGroup(*[
                Circle(radius=radius, stroke_width=0, fill_color=INK,
                       fill_opacity=opacity).move_to([3.65, 0.17, 0])
                for radius, opacity in ((0.85, 0.07), (0.58, 0.11), (0.30, 0.16))
            ])
            coin_heat = VGroup(*[
                Circle(radius=radius, stroke_width=0, fill_color=INK,
                       fill_opacity=opacity).move_to([-1.55, -0.23, 0])
                for radius, opacity in ((0.48, 0.08), (0.25, 0.12))
            ])
            wall_label = T("end wall: large", size=27, color=INK).move_to(
                [3.65, 1.75, 0])
            coin_label = T("coin: occasional", size=27, color=SOFT).move_to(
                [-1.55, 1.15, 0])
            method_label = T("attribution = gradient of value w.r.t. pixels",
                             size=24, color=MUTED).move_to([0, -2.15, 0])
            second = VGroup(frame, wall_heat, coin_heat, wall_label,
                            coin_label, method_label)
            self.play(FadeOut(first), FadeIn(frame), run_time=1.1)
            self.play(FadeIn(wall_heat), FadeIn(coin_heat),
                      FadeIn(wall_label), FadeIn(coin_label),
                      FadeIn(method_label), run_time=1.3)

        with self.beat("s07b03") as b:
            next_tag = Tag("limitation")
            magnitude = T("|attribution|", size=26,
                          color=SOFT).move_to([2.0, -1.55, 0])
            scale = VGroup(*[
                Rectangle(width=0.33, height=0.26, stroke_color=SOFT,
                          stroke_width=0.4, fill_color=INK,
                          fill_opacity=opacity).move_to([-1.05 + index * 0.33,
                                                       -1.55, 0])
                for index, opacity in enumerate((0.08, 0.18, 0.32, 0.52, 0.78))
            ])
            caution = T("may still matter", size=26,
                        color=AMBER).move_to([-3.25, 0.38, 0])
            pointer = Line(caution.get_right() + RIGHT * 0.08,
                           visible_coin.get_center() + LEFT * 0.28,
                           color=AMBER, stroke_width=1.5)
            callout = VGroup(pointer, caution)
            self.play(FadeOut(tag), FadeIn(next_tag),
                      FadeOut(wall_label), FadeOut(coin_label),
                      FadeIn(scale), FadeIn(magnitude), FadeIn(callout),
                      run_time=0.9)
            tag = next_tag

        with self.beat("s07b04") as b:
            next_tag = Tag("observed_result")
            self.play(FadeOut(tag), FadeIn(next_tag), FadeOut(second),
                      FadeOut(scale), FadeOut(magnitude), FadeOut(callout),
                      run_time=0.8)
            tag = next_tag

            data = self.dataset("d2")
            point = data["points"][0]
            strip = Line([-5.7, 1.36, 0], [1.35, 1.36, 0],
                         color=FAINT, stroke_width=3)
            passable = wall(-0.48, 1.37, 2.34, dashed=True)
            strip_coin = coin(-2.6, 1.72)
            runner = Agent(color=TEAL, radius=0.17).move_to([-5.15, 1.57, 0])
            wall_caption = T("permeable wall", size=22,
                             color=ROSE).move_to([0.05, 2.52, 0])
            top_scene = VGroup(strip, passable, strip_coin, runner, wall_caption)

            x_axis = Line([-5.15, -1.52, 0], [1.15, -1.52, 0],
                          color=MUTED, stroke_width=2)
            y_axis = Line([-5.15, -1.52, 0], [-5.15, 0.68, 0],
                          color=MUTED, stroke_width=2)
            curve = VMobject(stroke_color=INK, stroke_width=3)
            curve.set_points_smoothly([
                [-5.08, -1.20, 0], [-4.1, -0.92, 0], [-3.1, -0.63, 0],
                [-2.05, -0.18, 0], [-1.1, 0.33, 0], [-0.48, 0.59, 0],
                [0.18, 0.15, 0], [1.08, -0.46, 0],
            ])
            peak = Dot(point=[-0.48, 0.59, 0], radius=0.06, color=INK)
            connector = DashedLine([-0.48, 0.56, 0],
                                   [-0.48, 1.37, 0], color=SOFT,
                                   stroke_width=1.5, dash_length=0.08)
            x_label = T("timestep", size=22, color=MUTED).move_to([-2.2, -1.92, 0])
            y_label = T("critic value", size=22, color=MUTED).rotate(PI / 2)
            y_label.move_to([-5.55, -0.39, 0])
            peak_label = T("one typical episode: peak ≈ timestep 35",
                           size=21, color=SOFT).move_to([-2.22, -2.38, 0])
            schematic = T("schematic", size=21, color=MUTED).move_to(
                [-2.22, -2.83, 0])
            plot = VGroup(x_axis, y_axis, curve, peak, connector,
                          x_label, y_label, peak_label, schematic)

            chart_x = 4.15
            chart_base = -1.35
            chart_top = 0.85
            chart_axis = VGroup(
                Line([2.8, chart_base, 0], [5.88, chart_base, 0],
                     color=MUTED, stroke_width=2),
                Line([2.8, chart_base, 0], [2.8, chart_top, 0],
                     color=MUTED, stroke_width=2),
                Line([2.72, chart_top, 0], [2.88, chart_top, 0],
                     color=MUTED, stroke_width=2),
            )
            bar_height = (chart_top - chart_base) * point["value"] / point["value"]
            bar = Rectangle(width=0.92, height=bar_height,
                            stroke_width=0, fill_color=TEAL,
                            fill_opacity=0.9).move_to(
                                [chart_x, chart_base + bar_height / 2, 0])
            top_tick = T(point["display"], size=22, color=INK)
            top_tick.next_to(chart_axis[2], LEFT, buff=0.15)
            axis_label = T("% of wall reaches", size=22,
                           color=SOFT).move_to([4.34, 1.2, 0])
            bar_label = T(point["label"], size=21, color=SOFT,
                          width=19).move_to([4.17, -1.9, 0])
            sample = T("n = 114", size=21,
                       color=MUTED).move_to([4.17, -2.58, 0])
            chart = VGroup(chart_axis, bar, top_tick, axis_label,
                           bar_label, sample)
            self.play(FadeIn(top_scene), FadeIn(x_axis), FadeIn(y_axis),
                      FadeIn(x_label), FadeIn(y_label), FadeIn(chart_axis),
                      FadeIn(top_tick), FadeIn(axis_label), run_time=1.3)
            self.play(Create(curve), FadeIn(peak), Create(connector),
                      FadeIn(peak_label), FadeIn(schematic),
                      FadeIn(bar), FadeIn(bar_label), FadeIn(sample),
                      run_time=2.0)
            self.play(runner.animate.move_to([1.08, 1.57, 0]), run_time=2.3)

        with self.beat("s07b05") as b:
            next_tag = Tag("author_interpretation")
            self.play(FadeOut(tag), FadeIn(next_tag),
                      FadeOut(top_scene), FadeOut(plot), FadeOut(chart),
                      run_time=0.9)
            tag = next_tag

            line = Line([-5.75, -0.13, 0], [5.65, -0.13, 0],
                        color=FAINT, stroke_width=3)
            passable = wall(0.25, -0.12, 0.75, dashed=True)
            actor = Agent(color=TEAL, radius=0.2).move_to([-5.25, 0.07, 0])
            goal = coin(-2.65, 0.14, opacity=0.55)
            strip_final = VGroup(line, passable, actor, goal)

            actor_outline = Arrow([-4.93, 1.48, 0], [4.45, 1.48, 0],
                                  buff=0, color=TEAL, stroke_width=8)
            actor_arrow = Arrow([-4.93, 1.48, 0], [4.45, 1.48, 0],
                                buff=0, color=ROSE, stroke_width=4)
            actor_name = T("actor: move right", size=27,
                           color=TEAL).move_to([0.0, 2.06, 0])
            critic_outline = Arrow([-4.93, 0.74, 0], [0.04, 0.74, 0],
                                   buff=0, color=INK, stroke_width=8)
            critic_arrow = Arrow([-4.93, 0.74, 0], [0.04, 0.74, 0],
                                 buff=0, color=ROSE, stroke_width=4)
            critic_name = T("critic: move to the wall", size=27,
                            color=INK).move_to([-2.2, 1.07, 0])
            goal_arrow = Arrow([-4.93, -0.89, 0], [-2.72, 0.05, 0],
                               buff=0, color=AMBER, stroke_width=3,
                               stroke_opacity=0.45)
            goal_name = T("intended: move to the coin", size=26,
                          color=AMBER).move_to([-2.0, -1.4, 0])
            cross = VGroup(
                Line([-2.77, -0.07, 0], [-2.53, 0.35, 0],
                     color=AMBER, stroke_width=2, stroke_opacity=0.55),
                Line([-2.77, 0.35, 0], [-2.53, -0.07, 0],
                     color=AMBER, stroke_width=2, stroke_opacity=0.55),
            )
            interpretation = T("a non-robust proxy of a non-robust proxy",
                               size=25, color=SOFT).move_to([0, -2.22, 0])
            biases = T("inductive biases", size=25,
                       color=AMBER).move_to([0, -2.78, 0])
            self.play(FadeIn(strip_final), GrowArrow(actor_outline),
                      GrowArrow(actor_arrow),
                      FadeIn(actor_name), run_time=1.4)
            self.play(GrowArrow(critic_outline), GrowArrow(critic_arrow),
                      FadeIn(critic_name),
                      run_time=1.2)
            self.play(GrowArrow(goal_arrow), FadeIn(goal_name),
                      FadeIn(cross), run_time=1.2)
            self.play(FadeIn(interpretation), FadeIn(biases), run_time=0.8)
