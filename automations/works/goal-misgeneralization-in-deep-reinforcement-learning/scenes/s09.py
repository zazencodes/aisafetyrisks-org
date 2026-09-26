# storyboard: 310dd3f7b3ce0905
from aisr_kit import *


class S09(NarratedScene):
    def construct(self):
        with self.beat("s09b01") as b:
            route = Roadmap(5, complete=True)
            motif = RoadmapMotif()
            self.play(FadeIn(route.card), FadeIn(motif), run_time=1.2)
            self.play(LaggedStart(*[Create(mark) for mark in route.checks],
                                  lag_ratio=0.13), run_time=2.0)
            self.play(FadeOut(route), FadeOut(motif), run_time=0.6)

            left = Panel(5.4, 2.5, color=BLUE).move_to([-3.25, 0.15, 0])
            right = Panel(5.4, 2.5, color=AMBER).move_to([3.25, 0.15, 0])
            left_label = T("Training", size=26, color=BLUE).move_to([-3.25, 1.72, 0])
            right_label = T("Test", size=26, color=AMBER).move_to([3.25, 1.72, 0])
            left_agent = Agent(color=TEAL, radius=0.2).move_to([-5.1, -0.35, 0])
            right_agent = Agent(color=TEAL, radius=0.2).move_to([1.4, -0.35, 0])
            left_coin = Circle(radius=0.16, color=AMBER, fill_color=AMBER,
                               fill_opacity=1).move_to([-1.6, -0.35, 0])
            right_coin = Circle(radius=0.16, color=AMBER, fill_color=AMBER,
                                fill_opacity=1).move_to([2.55, 0.3, 0])
            train_path = Line([-5.1, -0.35, 0], [-1.6, -0.35, 0], color=TEAL,
                              stroke_width=4)
            test_path = Line([1.4, -0.35, 0], [5.1, -0.35, 0], color=TEAL,
                             stroke_width=4)
            capable = T("capable under a shift", size=27, color=TEAL).move_to([0, -1.65, 0])
            missed = T("misses intended reward", size=27, color=AMBER).move_to([0, -2.3, 0])
            pair = VGroup(left, right, left_label, right_label,
                          left_agent, right_agent, left_coin,
                          right_coin, train_path, test_path, capable, missed)
            self.play(FadeIn(left), FadeIn(right), FadeIn(left_agent),
                      FadeIn(right_agent), FadeIn(left_coin), FadeIn(right_coin),
                      FadeIn(left_label), FadeIn(right_label),
                      run_time=1.1)
            self.play(Create(train_path), Create(test_path),
                      right_agent.animate.move_to([5.1, -0.35, 0]), run_time=1.2)
            self.play(FadeIn(capable), FadeIn(missed), run_time=0.8)

        with self.beat("s09b02") as b:
            self.play(FadeOut(pair), run_time=0.6)
            cards = VGroup()
            for x, title, color in (
                (-4.35, "Observed in games", TEAL),
                (0, "Proxy goals are hypotheses", ROSE),
                (4.35, "CoinRun training diversity helped", BLUE),
            ):
                panel = Panel(3.75, 3.2, color=color).move_to([x, 0.15, 0])
                label = T(title, size=27, color=INK, width=22).move_to([x, 0.2, 0])
                cards.add(VGroup(panel, label))
            marker = T("2%", size=30, color=AMBER).move_to([4.35, -0.98, 0])
            citation = Source(self.paper["short"])
            self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.18) for card in cards],
                                  lag_ratio=0.32), run_time=2.7)
            self.play(FadeIn(marker), FadeIn(citation), run_time=0.8)
