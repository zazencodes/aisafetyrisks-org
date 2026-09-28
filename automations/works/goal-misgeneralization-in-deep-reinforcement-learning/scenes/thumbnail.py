# storyboard: 0b6709c6307060bc
from aisr_kit import *


class Thumbnail(Scene):
    def construct(self):
        # Headline: two short lines, the key word in the coin's color.
        line1 = Serif("It skipped", size=120, color=INK, weight=BOLD)
        line2 = Serif("the coin", size=120, color=AMBER, weight=BOLD)
        headline = VGroup(line1, line2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        headline.to_corner(UL, buff=0.55)
        self.add(headline)

        # The corridor floor and the empty end wall.
        ground_y = -2.8
        ground = Line([-6.6, ground_y, 0], [5.6, ground_y, 0], color=FAINT, stroke_width=6)
        wall = Rectangle(width=0.6, height=4.6, stroke_width=0, fill_color=GRAY, fill_opacity=0.55)
        wall.move_to([5.9, ground_y + 2.3, 0])
        self.add(ground, wall)

        # The coin, untouched in the middle of the floor.
        coin_pos = np.array([-1.2, ground_y + 0.75, 0])
        coin = VGroup(
            Circle(radius=0.75, stroke_width=0, fill_color=AMBER, fill_opacity=0.22),
            Circle(radius=0.58, stroke_width=0, fill_color=AMBER, fill_opacity=1),
            Star(n=5, outer_radius=0.32, inner_radius=0.14, stroke_width=0, fill_color=BG, fill_opacity=1),
        ).move_to(coin_pos)
        self.add(coin)

        # The agent's leap: from the left, high over the coin, down to the wall.
        start = np.array([-6.0, ground_y + 0.2, 0])
        end = np.array([4.65, ground_y + 0.75, 0])
        arc = ArcBetweenPoints(start, end, angle=-PI * 0.5, color=BLUE, stroke_width=7)
        dashed = DashedVMobject(arc, num_dashes=34, dashed_ratio=0.6)
        tip = Triangle(stroke_width=0, fill_color=BLUE, fill_opacity=1).scale(0.22)
        tip.rotate(angle_of_vector(arc.point_from_proportion(1) - arc.point_from_proportion(0.97)) - PI / 2)
        tip.move_to(arc.point_from_proportion(0.985))
        self.add(dashed, tip)

        agent = Agent(color=BLUE, radius=0.75).move_to([4.65 + 0.1, ground_y + 0.75, 0])
        self.add(agent)
