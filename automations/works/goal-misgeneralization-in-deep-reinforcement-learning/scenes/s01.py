# storyboard: 37d388cb0840bb44
from aisr_kit import *

class S01(NarratedScene):
    def construct(self):
        with self.beat("s01b01") as b:
            show(self, "The coin moves", "method", "coinrun", 0)
        with self.beat("s01b02") as b:
            show(self, "The coin moves", "method", "coinrun", 1)
        with self.beat("s01b03") as b:
            show(self, "The coin moves", "observed_result", "coinrun", 2)
        with self.beat("s01b04") as b:
            show(self, "The coin moves", "author_interpretation", "coinrun", 3)
