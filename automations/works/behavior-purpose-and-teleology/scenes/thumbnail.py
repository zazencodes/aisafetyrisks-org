# storyboard: df9a3b9bbd279260
from aisr_kit import *

class Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = BG
        top = Serif('It overshoots', size=110, weight=BOLD).to_edge(LEFT, buff=0.65).to_edge(UP, buff=0.5)
        bottom = Serif('again', size=110, weight=BOLD, color=TEAL).next_to(top, DOWN, aligned_edge=LEFT, buff=0.06)
        goal = Circle(radius=0.6, color=AMBER, stroke_width=14).move_to([1.0, -1.55, 0])
        path = VMobject(color=TEAL, stroke_width=12)
        path.set_points_smoothly([[-5.6,-1.55,0],[2.2,-1.55,0],[-1.5,-2.5,0],[4.5,-2.1,0],[-3.1,-3.0,0]])
        mover = Triangle(color=BLUE, fill_color=BLUE, fill_opacity=1, stroke_width=6).scale(0.5).rotate(PI/2).move_to([-3.1,-3.0,0])
        self.add(path, goal, mover, top, bottom)
