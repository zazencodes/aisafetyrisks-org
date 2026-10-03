# storyboard: 5e650dffcbdfaf8c
from aisr_kit import *


def make_coin(pos):
    glow = Circle(radius=0.36, stroke_width=0, fill_color=AMBER, fill_opacity=0.22).move_to(pos)
    body = Circle(radius=0.22, stroke_color=AMBER, stroke_width=2, fill_color=AMBER, fill_opacity=0.9).move_to(pos)
    inner = Circle(radius=0.13, stroke_color="#996D14", stroke_width=1.5).move_to(pos)
    coin = VGroup(glow, body, inner)
    coin.body = body
    return coin


def make_cheese(pos):
    glow = Circle(radius=0.28, stroke_width=0, fill_color=AMBER, fill_opacity=0.22).move_to(pos)
    wedge = Polygon(
        [-0.16, -0.13, 0], [0.16, -0.13, 0], [0.0, 0.16, 0],
        stroke_color=AMBER, stroke_width=2, fill_color=AMBER, fill_opacity=0.95
    ).move_to(pos)
    dot1 = Dot(point=wedge.get_center() + DOWN * 0.04 + LEFT * 0.04, radius=0.03, color=BG)
    dot2 = Dot(point=wedge.get_center() + UP * 0.04 + RIGHT * 0.03, radius=0.02, color=BG)
    return VGroup(glow, wedge, dot1, dot2)


def make_spikes(x_start, y_base, count=3, width=0.35, height=0.6):
    spikes = VGroup()
    for i in range(count):
        x0 = x_start + i * width
        x1 = x0 + width
        xm = (x0 + x1) / 2
        p = Polygon(
            [x0, y_base, 0], [x1, y_base, 0], [xm, y_base + height, 0],
            stroke_color=ROSE, stroke_width=1.5, fill_color=ROSE, fill_opacity=0.85
        )
        spikes.add(p)
    return spikes


class S02(NarratedScene):
    def construct(self):
        floor_y = -1.6

        # --- Beat 1: Training distribution in CoinRun ---
        with self.beat("s02b01") as b:
            heading = Heading("Competent pursuit of wrong goals")
            tag = Tag("method")
            source = Source(self.paper["short"])

            level_box = RoundedRectangle(
                corner_radius=0.18, width=10.4, height=4.4,
                stroke_color=TEAL, stroke_width=2.5, fill_color=PANEL, fill_opacity=0.95
            ).move_to([0, -0.3, 0])

            floor = Line([-4.8, floor_y, 0], [4.8, floor_y, 0], stroke_width=3, color=FAINT)
            ground = Rectangle(width=9.6, height=0.55, stroke_width=0, fill_color=FAINT, fill_opacity=0.2).next_to(floor, DOWN, buff=0)
            wall = Rectangle(width=0.3, height=2.6, stroke_color=FAINT, stroke_width=1.5, fill_color=FAINT, fill_opacity=0.5).move_to([4.65, -0.3, 0])
            spikes = make_spikes(-1.4, floor_y, count=3, width=0.35, height=0.6)

            env_label = T("CoinRun environment", size=30, color=INK, weight=MEDIUM).move_to([-2.75, 1.4, 0])
            dist_label = T("Training distribution", size=34, color=TEAL, weight=SEMIBOLD).move_to([2.55, 1.4, 0])

            coin_pos = np.array([4.1, floor_y + 0.45, 0])
            coin = make_coin(coin_pos)
            coin_label1 = T("Coin fixed at end wall", size=34, color=AMBER, weight=SEMIBOLD).move_to([2.2, 0.35, 0])
            coin_line1 = Line([3.9, 0.1, 0], [4.05, floor_y + 0.75, 0], stroke_width=2, color=AMBER)
            coin_callout1 = VGroup(coin_label1, coin_line1)

            agent = Agent(color=BLUE, radius=0.22).move_to([-4.0, floor_y + 0.22, 0])

            # Trajectory over spikes to coin
            trail_pts1 = [
                np.array([-4.0, floor_y + 0.22, 0]),
                np.array([-1.8, floor_y + 0.22, 0]),
                np.array([-0.88, floor_y + 1.15, 0]),
                np.array([0.0, floor_y + 0.22, 0]),
                np.array([3.6, floor_y + 0.22, 0]),
            ]
            path1 = VMobject()
            path1.set_points_smoothly(trail_pts1)
            trail1 = DashedVMobject(path1, num_dashes=24, dashed_ratio=0.5, color=BLUE)

            self.play(
                FadeIn(heading), FadeIn(tag), FadeIn(source),
                FadeIn(level_box), FadeIn(floor), FadeIn(ground), FadeIn(wall),
                FadeIn(spikes), FadeIn(env_label), FadeIn(dist_label),
                FadeIn(coin), FadeIn(coin_callout1), FadeIn(agent),
                run_time=0.6
            )
            self.wait(0.8)

            # Agent runs to leap point
            self.play(agent.animate.move_to([-1.8, floor_y + 0.22, 0]), run_time=0.7)

            # Leap over hazard spikes
            leap_curve = VMobject()
            leap_curve.set_points_smoothly([
                np.array([-1.8, floor_y + 0.22, 0]),
                np.array([-0.88, floor_y + 1.15, 0]),
                np.array([0.0, floor_y + 0.22, 0]),
            ])
            self.play(MoveAlongPath(agent, leap_curve), run_time=1.0)

            # Run to coin at right wall and show movement trajectory
            self.play(
                agent.animate.move_to(coin_pos),
                FadeIn(trail1),
                run_time=1.0
            )
            self.play(coin.animate.scale(1.2), run_time=0.25)
            self.play(coin.animate.scale(1 / 1.2), run_time=0.25)

        # --- Beat 2: Test distribution with coin randomized ---
        with self.beat("s02b02") as b:
            new_tag = Tag("observed_result")
            test_dist_label = T("Test distribution", size=34, color=AMBER, weight=SEMIBOLD).move_to([2.55, 1.4, 0])

            # Swap training state for test state right at the beat boundary.
            self.play(
                FadeOut(tag), FadeIn(new_tag),
                level_box.animate.set_stroke(color=AMBER),
                FadeOut(dist_label), FadeIn(test_dist_label),
                FadeOut(coin_callout1),
                FadeOut(trail1),
                run_time=0.2
            )

            # Move coin to middle (randomized position along path)
            coin_mid_pos = np.array([1.2, floor_y + 0.45, 0])
            coin_label2 = T("Coin randomized", size=34, color=AMBER, weight=SEMIBOLD).move_to([2.35, 0.35, 0])
            coin_line2 = Line([1.4, 0.1, 0], [1.25, floor_y + 0.8, 0], stroke_width=2, color=AMBER)
            coin_callout2 = VGroup(coin_label2, coin_line2)

            empty_marker = Circle(
                radius=0.22, stroke_color=MUTED, stroke_width=1.5, stroke_opacity=0.6
            ).move_to([4.1, floor_y + 0.22, 0])

            # Trajectory running straight past coin to empty end wall
            trail_pts2 = [
                np.array([-4.0, floor_y + 0.22, 0]),
                np.array([-1.8, floor_y + 0.22, 0]),
                np.array([-0.88, floor_y + 1.15, 0]),
                np.array([0.0, floor_y + 0.22, 0]),
                np.array([4.1, floor_y + 0.22, 0]),
            ]
            path2 = VMobject()
            path2.set_points_smoothly(trail_pts2)
            trail2 = DashedVMobject(path2, num_dashes=26, dashed_ratio=0.5, color=BLUE)

            self.play(
                coin.animate.move_to(coin_mid_pos),
                FadeIn(coin_callout2),
                FadeIn(empty_marker),
                agent.animate.move_to([-4.0, floor_y + 0.22, 0]),
                run_time=0.8
            )
            self.wait(0.2)

            # Agent runs, leaps over spikes, and bypasses coin straight to empty wall
            self.play(agent.animate.move_to([-1.8, floor_y + 0.22, 0]), run_time=0.7)
            self.play(MoveAlongPath(agent, leap_curve), run_time=1.0)
            self.play(
                agent.animate.move_to([4.1, floor_y + 0.22, 0]),
                FadeIn(trail2),
                run_time=1.3
            )

            # Agent ignores coin label
            ignore_label = T("Agent ignores coin", size=34, color=ROSE, weight=SEMIBOLD).move_to([-2.8, 0.35, 0])
            ignore_callout = VGroup(ignore_label)
            self.play(FadeIn(ignore_callout), run_time=0.6)

        # --- Beat 3: Maze environment with randomized cheese ---
        with self.beat("s02b03") as b:
            coinrun_all = VGroup(
                level_box, floor, ground, wall, spikes, env_label,
                test_dist_label, coin, coin_callout2, ignore_callout, empty_marker, trail2, agent
            )
            self.play(FadeOut(coinrun_mobs := coinrun_all), run_time=0.7)

            maze_center = np.array([-1.5, -0.4, 0])
            maze_frame = RoundedRectangle(
                corner_radius=0.18, width=4.1, height=4.1,
                stroke_color=AMBER, stroke_width=2.5, fill_color=PANEL, fill_opacity=0.95
            ).move_to(maze_center)

            grid = Grid(5, 5, cell=0.7, color=FAINT, fill=PANEL).move_to(maze_center)

            wall_indices = [
                (0, 0), (0, 1),
                (1, 0), (1, 1), (1, 3), (1, 4),
                (2, 3), (2, 4),
                (3, 1), (3, 3), (3, 4),
                (4, 1), (4, 2), (4, 3), (4, 4),
            ]
            walls = VGroup(*[
                Square(side_length=0.68, stroke_width=1, stroke_color="#222830", fill_color="#0E1217", fill_opacity=1.0)
                .move_to(grid.cell(r, c).get_center())
                for r, c in wall_indices
            ])

            cheese_pos = grid.cell(3, 2).get_center()
            cheese = make_cheese(cheese_pos)

            corner_pos = grid.cell(0, 4).get_center()
            corner_target = Square(
                side_length=0.55, stroke_color=MUTED, stroke_width=1.5, stroke_opacity=0.7,
                fill_color=FAINT, fill_opacity=0.3
            ).move_to(corner_pos)

            agent_maze = Agent(color=BLUE, radius=0.20).move_to(grid.cell(4, 0).get_center())

            maze_title = T("Maze environment", size=24, color=INK, weight=MEDIUM).move_to([3.4, 1.2, 0])

            # Corner callout on top (aligning with top-right corner)
            corner_text = T("Agent navigates to corner", size=22, color=BLUE, weight=SEMIBOLD).move_to([3.4, 0.45, 0])
            corner_line = Line([1.5, 0.65, 0], corner_pos + RIGHT * 0.35, stroke_width=1.5, color=FAINT)
            corner_callout = VGroup(corner_text, corner_line)

            # Cheese callout below (aligning with lower side corridor)
            cheese_text = T("Cheese randomized", size=22, color=AMBER, weight=SEMIBOLD).move_to([3.4, -0.55, 0])
            cheese_line = Line([2.0, -0.55, 0], cheese_pos + RIGHT * 0.35, stroke_width=1.5, color=FAINT)
            cheese_callout = VGroup(cheese_text, cheese_line)

            self.play(
                FadeIn(maze_frame), FadeIn(grid), FadeIn(walls), FadeIn(corner_target),
                FadeIn(cheese), FadeIn(cheese_callout), FadeIn(agent_maze), FadeIn(maze_title),
                run_time=1.1
            )
            self.wait(0.2)

            # Navigate through corridors to top-right corner, bypassing the cheese at (3, 2)
            waypoints = [
                grid.cell(4, 0).get_center(),
                grid.cell(3, 0).get_center(),
                grid.cell(2, 0).get_center(),
                grid.cell(2, 1).get_center(),
                grid.cell(2, 2).get_center(),
                grid.cell(1, 2).get_center(),
                grid.cell(0, 2).get_center(),
                grid.cell(0, 3).get_center(),
                grid.cell(0, 4).get_center(),
            ]
            maze_path = VMobject()
            maze_path.set_points_as_corners(waypoints)
            maze_trail = DashedVMobject(maze_path, num_dashes=28, dashed_ratio=0.5, color=BLUE)

            self.play(
                MoveAlongPath(agent_maze, maze_path),
                Create(maze_trail),
                run_time=3.4,
                rate_func=linear
            )
            self.play(
                FadeIn(corner_callout),
                agent_maze.animate.scale(1.15),
                run_time=0.5
            )
            self.play(agent_maze.animate.scale(1 / 1.15), run_time=0.3)
