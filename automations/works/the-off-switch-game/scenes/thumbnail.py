# storyboard: d14368f6d6bfa5fc
from aisr_kit import *

class Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = BG
        first = Serif("Permission", size=112, weight=BOLD).move_to([-1.4, 2.65, 0]).to_edge(LEFT, buff=0.65)
        second = Serif("to stop", size=112, weight=BOLD, color=ROSE).next_to(first, DOWN, aligned_edge=LEFT, buff=0.05)
        robot = RoundedRectangle(width=2.8, height=1.75, corner_radius=0.28, color=TEAL, stroke_width=9, fill_color=TEAL, fill_opacity=0.2).move_to([-3.85,-1.6,0])
        stop = Circle(radius=0.83, color=ROSE, stroke_width=12, fill_color=ROSE, fill_opacity=0.16).move_to([0.35,-1.6,0])
        human = Circle(radius=0.65, color=AMBER, stroke_width=10, fill_color=AMBER, fill_opacity=0.18).move_to([3.65,0.2,0])
        control = Line(human.get_bottom(), stop.get_top(), color=AMBER, stroke_width=8)
        path = Arrow(robot.get_right(), stop.get_left(), color=TEAL, stroke_width=8, buff=0.17, max_tip_length_to_length_ratio=0.22)
        self.add(first, second, robot, stop, human, control, path)
