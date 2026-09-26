# storyboard: f471c045b261ce18
from aisr_kit import *


class R02(NarratedScene):
    def construct(self):
        with self.beat("r02b01") as b:
            route = Roadmap(1)
            motif = RoadmapMotif()
            self.play(FadeIn(route.card), FadeIn(motif), run_time=1.3)
            self.play(LaggedStart(*[Create(mark) for mark in route.checks],
                                  lag_ratio=0.2), run_time=1.0)
            self.play(Indicate(route.card[2][1], color=AMBER), run_time=0.8)
