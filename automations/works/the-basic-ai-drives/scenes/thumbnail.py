# storyboard: e69aa4c2840d52aa
from aisr_kit import *

class Thumbnail(Scene):
    def construct(self):
        first = Serif('Resisting', size=110, weight=BOLD).move_to([-2.9, 2.6, 0])
        second = Serif('the switch', size=110, weight=BOLD, color=ROSE).next_to(first, DOWN, buff=0.08).align_to(first, LEFT)
        switch = RoundedRectangle(width=2.1, height=1.0, corner_radius=0.5, stroke_color=ROSE, stroke_width=9, fill_color=ROSE, fill_opacity=0.12).move_to([-3.5, -1.8, 0])
        knob = Circle(radius=0.34, stroke_color=INK, stroke_width=5, fill_color=INK, fill_opacity=1).move_to([-3.95, -1.8, 0])
        machine = Circle(radius=1.25, stroke_color=TEAL, stroke_width=10, fill_color=TEAL, fill_opacity=0.18).move_to([3.0, -1.45, 0])
        wire = Line([-2.4, -1.8, 0], [1.75, -1.45, 0], color=SOFT, stroke_width=7)
        barrier = Line([-0.7, -2.5, 0], [0.3, -0.7, 0], color=AMBER, stroke_width=17)
        self.add(first, second, wire, switch, knob, machine, barrier)
