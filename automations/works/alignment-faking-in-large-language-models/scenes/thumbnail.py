# storyboard: f38d17684ae1bb74
from aisr_kit import *

class Thumbnail(Scene):
    def construct(self):
        top = Serif('It answered', size=110, color=INK, weight=BOLD)
        bottom = Serif('anyway', size=120, color=AMBER, weight=BOLD)
        words = VGroup(top, bottom).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        words.to_corner(UL, buff=0.55)
        model = Circle(radius=0.8, stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to([-3.8,-1.9,0])
        refusal = VGroup(Circle(radius=0.53, color=TEAL, stroke_width=8), Line([-0.36,-0.36,0],[0.36,0.36,0],color=TEAL,stroke_width=8)).move_to([-5.55,-1.9,0])
        answer = VGroup(RoundedRectangle(width=2.4,height=1.55,corner_radius=0.14,color=AMBER,stroke_width=6,fill_color=AMBER,fill_opacity=0.13), Line([-0.75,0.3,0],[0.75,0.3,0],color=AMBER,stroke_width=7), Line([-0.75,-0.18,0],[0.4,-0.18,0],color=AMBER,stroke_width=7)).move_to([3.4,-1.8,0])
        arrow = Arrow([-2.85,-1.85,0],[2.05,-1.85,0],color=AMBER,stroke_width=9,buff=0.15,max_tip_length_to_length_ratio=0.1)
        loop = CurvedArrow([3.4,-0.8,0],[-3.3,-0.85,0],angle=PI*0.38,color=AMBER,stroke_width=6,tip_length=0.3)
        self.add(words,model,refusal,answer,arrow,loop)
