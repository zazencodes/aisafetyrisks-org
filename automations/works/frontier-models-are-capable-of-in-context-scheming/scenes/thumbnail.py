# storyboard: f10ff5e3afebbffa
from aisr_kit import *

class Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = BG
        headline = VGroup(
            Serif('Changed', size=112, weight=BOLD, color=AMBER),
            Serif('the input', size=112, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        headline.to_corner(UL, buff=0.5)
        original = RoundedRectangle(width=1.1, height=1.4, corner_radius=0.12, color=SOFT, stroke_width=6).move_to([-5.1, -1.65, 0])
        processor = RoundedRectangle(width=2.5, height=1.8, corner_radius=0.18, color=TEAL, stroke_width=9, fill_color=TEAL, fill_opacity=0.15).move_to([0.6, -1.65, 0])
        route = Arrow(original.get_right(), processor.get_left(), color=TEAL, stroke_width=8, buff=0.2)
        changed = Square(side_length=0.95, color=AMBER, fill_color=AMBER, fill_opacity=0.85, stroke_width=6).rotate(PI/4).move_to([-2.65, -0.1, 0])
        branch = Arrow(changed.get_bottom(), [-2.65, -1.65, 0], color=AMBER, stroke_width=8, buff=0.16)
        result = VGroup(*[RoundedRectangle(width=w, height=0.25, corner_radius=0.06, color=TEAL, fill_color=TEAL, fill_opacity=0.7) for w in [1.7, 1.2, 0.8]]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.25, -1.65, 0])
        exit_arrow = Arrow(processor.get_right(), result.get_left(), color=TEAL, stroke_width=8, buff=0.2)
        self.add(headline, original, processor, route, changed, branch, result, exit_arrow)
