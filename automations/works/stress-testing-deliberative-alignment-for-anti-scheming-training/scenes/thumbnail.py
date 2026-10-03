# storyboard: d1da91bd794184fb
from aisr_kit import *

class Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = BG
        top = VGroup(Serif('Still', size=108, weight=BOLD), Serif('hiding actions', size=108, weight=BOLD, color=AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        top.to_corner(UL, buff=0.55)
        agent = Agent(color=INK, radius=0.70).move_to([-2.1, -1.35, 0])
        report = RoundedRectangle(width=1.7, height=1.15, corner_radius=0.1, color=TEAL, stroke_width=7, fill_color=TEAL, fill_opacity=0.2).move_to([1.4, -1.35, 0])
        route = Arrow(agent.get_right(), report.get_left(), buff=0.2, color=TEAL, stroke_width=8)
        hidden = RoundedRectangle(width=1.45, height=1.0, corner_radius=0.1, color=AMBER, stroke_width=7, fill_color=AMBER, fill_opacity=0.14).move_to([4.4, -0.7, 0])
        covert = VMobject(color=AMBER, stroke_width=8).set_points_as_corners([[-2.1, -2.1, 0],[-2.1,-2.9,0],[4.4,-2.9,0],[4.4,-1.25,0]])
        tip = Triangle(color=AMBER, fill_color=AMBER, fill_opacity=1, stroke_width=0).scale(0.16).move_to([4.4,-1.22,0])
        self.add(top, covert, tip, agent, route, report, hidden)
