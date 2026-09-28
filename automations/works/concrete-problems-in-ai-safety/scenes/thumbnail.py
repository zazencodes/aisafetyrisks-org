# storyboard: a65f6184b4250011
from aisr_kit import *

BROWN = "#9A6B45"


class Thumbnail(Scene):
    def construct(self):
        # Headline: the reward word in the score's gold.
        line1 = Serif("Rewarded for", size=110, color=AMBER, weight=BOLD)
        line2 = Serif("seeing nothing", size=110, color=INK, weight=BOLD)
        headline = VGroup(line1, line2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        headline.to_corner(UL, buff=0.5)
        self.add(headline)

        # The office floor.
        floor = RoundedRectangle(corner_radius=0.35, width=9.4, height=3.7, stroke_color=GRAY, stroke_width=6,
                                 fill_color=PANEL, fill_opacity=1).move_to([-1.3, -1.35, 0])
        self.add(floor)

        # Messes all around the robot.
        messes = VGroup(*[Dot([x, y, 0], radius=0.2, color=BROWN) for x, y in [
            (-5.0, -0.2), (-4.2, -2.5), (-3.2, -0.6), (1.1, -0.3), (2.3, -1.2), (1.6, -2.6), (-2.6, -2.7),
        ]])
        self.add(messes)

        # The robot, its eye shut to a flat line.
        body = RoundedRectangle(corner_radius=0.2, width=1.7, height=1.7, stroke_width=0,
                                fill_color=BLUE, fill_opacity=1).move_to([-1.0, -1.35, 0])
        pointer = Line(body.get_right(), body.get_right() + RIGHT * 0.6, stroke_width=12, color=BLUE)
        eye = Line(LEFT * 0.4, RIGHT * 0.4, stroke_width=14, color=WHITE)
        eye.move_to(body.get_right() + LEFT * 0.55)
        self.add(body, pointer, eye)

        # The score, full.
        pips = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.5, height=0.5, stroke_color=AMBER,
                                         stroke_width=4, fill_color=AMBER, fill_opacity=1)
                        for _ in range(5)]).arrange(UP, buff=0.14)
        glow = RoundedRectangle(corner_radius=0.2, width=pips.width + 0.5, height=pips.height + 0.5,
                                stroke_width=0, fill_color=AMBER, fill_opacity=0.2)
        score = VGroup(glow, pips).move_to([4.8, -1.2, 0])
        self.add(score)
