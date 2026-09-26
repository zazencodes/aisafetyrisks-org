# storyboard: 0a15f4fcdbe78a43
from aisr_kit import *

class S05(NarratedScene):
    def construct(self):
        with self.beat("s05b01") as b:
            show(self, "The question to carry forward", "threat_model", "closing", 0)
        with self.beat("s05b02") as b:
            show(self, "The question to carry forward", "limitation", "closing", 1)
        with self.beat("s05b03") as b:
            show(self, "The question to carry forward", "author_interpretation", "closing", 2)
