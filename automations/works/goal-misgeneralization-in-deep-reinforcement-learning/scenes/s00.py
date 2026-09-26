# storyboard: c0545fd6e12316f2
from aisr_kit import *

class S00(NarratedScene):
    def construct(self):
        with self.beat("s00b01") as b:
            show(self, "Which instruction did it learn?", "future_scenario", "warehouse", 0)
        with self.beat("s00b02") as b:
            show(self, "Which instruction did it learn?", "threat_model", "warehouse", 1)
        with self.beat("s00b03") as b:
            show(self, "Which instruction did it learn?", "method", "warehouse", 2)
