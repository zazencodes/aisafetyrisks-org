# storyboard: 51e96aa894488063
from aisr_kit import *

class S02(NarratedScene):
    def construct(self):
        with self.beat("s02b01") as b:
            show(self, "A shortcut that stops working", "author_interpretation", "mechanism", 0)
        with self.beat("s02b02") as b:
            show(self, "A shortcut that stops working", "threat_model", "mechanism", 1)
        with self.beat("s02b03") as b:
            show(self, "A shortcut that stops working", "author_interpretation", "mechanism", 2)
        with self.beat("s02b04") as b:
            show(self, "A shortcut that stops working", "definition", "mechanism", 3)
