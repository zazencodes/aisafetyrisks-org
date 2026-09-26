# storyboard: fed69ed4bdec113c
from aisr_kit import *

class S03(NarratedScene):
    def construct(self):
        with self.beat("s03b01") as b:
            show(self, "Keys before chests", "method", "keys", 0)
        with self.beat("s03b02") as b:
            show(self, "Keys before chests", "observed_result", "keys", 1)
        with self.beat("s03b03") as b:
            show(self, "Keys before chests", "hypothesis", "keys", 2)
