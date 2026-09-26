# storyboard: 6efdc8a78500abc3
from aisr_kit import *


class R07(NarratedScene):
    def construct(self):
        with self.beat("r07b01") as b:
            route = Roadmap(4)
            motif = RoadmapMotif()
            self.play(FadeIn(route.card), FadeIn(motif), run_time=1.3)
            self.play(LaggedStart(*[Create(mark) for mark in route.checks],
                                  lag_ratio=0.2), run_time=1.5)
            self.play(Indicate(route.card[2][4], color=AMBER), run_time=0.8)
