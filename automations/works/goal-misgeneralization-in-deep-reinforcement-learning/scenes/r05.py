# storyboard: 35309c4491889033
from aisr_kit import *


class R05(NarratedScene):
    def construct(self):
        with self.beat("r05b01") as b:
            route = Roadmap(2)
            motif = RoadmapMotif()
            self.play(FadeIn(route.card), FadeIn(motif), run_time=1.3)
            self.play(LaggedStart(*[Create(mark) for mark in route.checks],
                                  lag_ratio=0.2), run_time=1.2)
            self.play(Indicate(route.card[2][2], color=AMBER), run_time=0.8)
