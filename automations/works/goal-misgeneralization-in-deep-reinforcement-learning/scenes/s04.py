# storyboard: f4965e5bb5cd7a47
from aisr_kit import *

class S04(NarratedScene):
    def construct(self):
        with self.beat("s04b01") as b:
            show(self, "Make the cues disagree", "method", "diversity", 0)
        with self.beat("s04b02") as b:
            show(self, "Make the cues disagree", "observed_result", "diversity", 1)
        with self.beat("s04b03") as b:
            show(self, "Make the cues disagree", "limitation", "diversity", 2)
