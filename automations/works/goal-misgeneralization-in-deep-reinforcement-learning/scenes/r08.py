# storyboard: 0eabd90e175788c4
from aisr_kit import *


class R08(NarratedScene):
    def construct(self):
        with self.beat("r08b01") as b:
            route = Roadmap(5)
            motif = RoadmapMotif()
            self.play(FadeIn(route.card), FadeIn(motif), run_time=1.3)
            self.play(LaggedStart(*[Create(mark) for mark in route.checks],
                                  lag_ratio=0.2), run_time=1.6)
            self.play(Indicate(route.card[2][5], color=AMBER), run_time=0.8)
