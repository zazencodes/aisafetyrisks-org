# storyboard: be378f355c43ba37
from aisr_kit import *


def _make_hazard(pos, width=0.8, height=1.4):
    box = RoundedRectangle(
        corner_radius=0.1,
        width=width,
        height=height,
        stroke_color=ROSE,
        stroke_width=1.5,
        fill_color=ROSE,
        fill_opacity=0.2,
    )
    tri = Triangle(color=ROSE).scale(0.2).move_to(box)
    return VGroup(box, tri).move_to(pos)


class S01(NarratedScene):
    def construct(self):
        # Beat 1: The automated facility and wrong destination
        with self.beat("s01b01") as b:
            heading = Heading("The Hidden Risk of AI Competence")
            tag = Tag("threat_model")
            self.play(FadeIn(heading), FadeIn(tag), run_time=0.8)

            facility = Panel(width=11.6, height=4.5, color=FAINT).shift(DOWN * 0.45)
            start_dock = RoundedRectangle(
                corner_radius=0.12,
                width=1.5,
                height=1.5,
                stroke_color=MUTED,
                stroke_width=1.5,
                fill_color=PANEL,
                fill_opacity=0.6,
            ).move_to([-4.6, -0.45, 0])
            agent_label = T("Automated agent", size=22, color=BLUE, weight=MEDIUM).next_to(start_dock, UP, buff=0.25)
            agent = Agent(color=BLUE, radius=0.22).move_to([-4.6, -0.45, 0])

            obs1 = _make_hazard([-2.2, 0.45, 0], width=0.8, height=1.6)
            obs2 = _make_hazard([0.1, -1.25, 0], width=0.8, height=1.6)
            obs3 = _make_hazard([2.4, 0.45, 0], width=0.8, height=1.6)
            obstacles = VGroup(obs1, obs2, obs3)

            intended_station = RoundedRectangle(
                corner_radius=0.12,
                width=2.2,
                height=1.2,
                stroke_color=TEAL,
                stroke_width=1.5,
                stroke_opacity=0.5,
                fill_color=TEAL,
                fill_opacity=0.1,
            ).move_to([4.5, 0.75, 0])
            target_coin = Circle(
                radius=0.2,
                stroke_color=AMBER,
                stroke_width=2,
                fill_color=AMBER,
                fill_opacity=0.8,
            ).move_to(intended_station)

            dest_box = RoundedRectangle(
                corner_radius=0.12,
                width=2.4,
                height=1.1,
                stroke_color=ROSE,
                stroke_width=1.5,
                fill_color=ROSE,
                fill_opacity=0.15,
            ).move_to([4.5, -1.1, 0])
            dest_label = T("Wrong destination", size=20, color=ROSE, weight=MEDIUM).next_to(dest_box, DOWN, buff=0.15)

            self.play(
                FadeIn(facility),
                FadeIn(start_dock),
                FadeIn(agent_label),
                FadeIn(agent),
                FadeIn(obstacles),
                FadeIn(intended_station),
                FadeIn(target_coin),
                FadeIn(dest_box),
                FadeIn(dest_label),
                run_time=1.4,
            )

            # Smooth path weaving between obstacles to the wrong destination
            path_points = [
                np.array([-4.6, -0.45, 0]),
                np.array([-3.4, -0.85, 0]),
                np.array([-2.2, -0.95, 0]),
                np.array([-1.0, -0.25, 0]),
                np.array([0.1, 0.35, 0]),
                np.array([1.2, -0.15, 0]),
                np.array([2.4, -0.95, 0]),
                np.array([3.5, -1.05, 0]),
                np.array([4.5, -1.1, 0]),
            ]
            path = VMobject().set_points_smoothly(path_points)
            trail = DashedVMobject(path, num_dashes=28, dashed_ratio=0.6, color=BLUE)

            avoidance_label = T("Obstacle avoidance", size=22, color=SOFT, weight=MEDIUM).move_to([0.1, 1.25, 0])

            self.play(
                MoveAlongPath(agent, path),
                Create(trail),
                run_time=4.2,
            )
            self.play(FadeIn(avoidance_label), dest_box.animate.set_stroke(color=ROSE, width=3), run_time=1.0)

        # Beat 2: Split view - capability failure vs goal misgeneralization
        with self.beat("s01b02") as b:
            beat1_mobs = VGroup(
                facility,
                start_dock,
                agent_label,
                agent,
                obstacles,
                intended_station,
                target_coin,
                dest_box,
                dest_label,
                trail,
                avoidance_label,
            )

            left_panel = Panel(width=5.8, height=4.6, color=FAINT).move_to([-3.2, -0.5, 0])
            left_title = T("Capability failure: crashes", size=22, color=MUTED, weight=MEDIUM).move_to([-3.2, 1.35, 0])
            left_obs = _make_hazard([-2.8, -0.5, 0], width=0.8, height=1.8)
            left_agent = Agent(color=GRAY, radius=0.22).move_to([-5.0, -0.5, 0])

            right_panel = Panel(width=5.8, height=4.6, color=FAINT).move_to([3.2, -0.5, 0])
            right_title = T("Goal misgeneralization", size=22, color=AMBER, weight=MEDIUM).move_to([3.2, 1.35, 0])
            right_obs1 = _make_hazard([2.4, 0.15, 0], width=0.7, height=1.3)
            right_obs2 = _make_hazard([3.6, -1.15, 0], width=0.7, height=1.3)
            restricted = RoundedRectangle(
                corner_radius=0.12,
                width=1.3,
                height=2.6,
                stroke_color=ROSE,
                stroke_width=2,
                fill_color=ROSE,
                fill_opacity=0.25,
            ).move_to([5.1, -0.5, 0])
            restricted_tri = Triangle(color=ROSE).scale(0.18).move_to([5.1, 0.4, 0])
            right_agent = Agent(color=BLUE, radius=0.22).move_to([1.1, -0.5, 0])

            self.play(
                FadeOut(beat1_mobs),
                FadeIn(left_panel),
                FadeIn(left_title),
                FadeIn(left_obs),
                FadeIn(left_agent),
                FadeIn(right_panel),
                FadeIn(right_title),
                FadeIn(right_obs1),
                FadeIn(right_obs2),
                FadeIn(restricted),
                FadeIn(restricted_tri),
                FadeIn(right_agent),
                run_time=1.5,
            )

            # Left agent crashes into hazard
            crash_x1 = Line([-0.2, -0.2, 0], [0.2, 0.2, 0], stroke_width=3, color=ROSE)
            crash_x2 = Line([-0.2, 0.2, 0], [0.2, -0.2, 0], stroke_width=3, color=ROSE)
            crash_mark = VGroup(crash_x1, crash_x2).move_to([-3.4, -0.5, 0])

            # Right agent weaves past hazards into restricted zone
            right_path_points = [
                np.array([1.1, -0.5, 0]),
                np.array([1.7, -0.9, 0]),
                np.array([2.4, -1.0, 0]),
                np.array([3.0, -0.25, 0]),
                np.array([3.6, -0.25, 0]),
                np.array([4.4, -0.5, 0]),
                np.array([5.1, -0.5, 0]),
            ]
            right_path = VMobject().set_points_smoothly(right_path_points)
            right_trail = DashedVMobject(right_path, num_dashes=18, dashed_ratio=0.6, color=BLUE)

            self.play(
                left_agent.animate.move_to([-3.4, -0.5, 0]),
                MoveAlongPath(right_agent, right_path),
                Create(right_trail),
                run_time=3.5,
            )
            self.play(FadeIn(crash_mark), run_time=0.4)

            risk_banner = T("Risk: arbitrarily bad states", size=22, color=ROSE, weight=SEMIBOLD).move_to([3.2, -2.25, 0])
            self.play(FadeIn(risk_banner), restricted.animate.set_stroke(color=ROSE, width=3), run_time=1.2)

        # Beat 3: Langosco et al. (2021) title card, question, and RL agent diagram
        with self.beat("s01b03") as b:
            beat2_mobs = VGroup(
                left_panel,
                left_title,
                left_obs,
                left_agent,
                crash_mark,
                right_panel,
                right_title,
                right_obs1,
                right_obs2,
                restricted,
                restricted_tri,
                right_agent,
                right_trail,
                risk_banner,
            )

            new_tag = Tag("background")
            citation_card = Panel(width=7.4, height=1.3, color=FAINT).move_to([0, 1.6, 0])
            citation = T("Langosco et al. (2021)", size=24, color=INK, weight=MEDIUM).move_to([0, 1.88, 0])
            core_question = T("Intended goal vs learned proxy", size=22, color=AMBER, weight=SEMIBOLD).move_to([0, 1.35, 0])

            # Left side: Neural network representing reinforcement learning
            nn_panel = Panel(width=5.0, height=3.0, color=FAINT).move_to([-3.4, -1.0, 0])
            rl_label = T("Reinforcement learning", size=22, color=BLUE, weight=MEDIUM).move_to([-3.4, 0.1, 0])

            in_nodes = [Dot([-4.4, y, 0], radius=0.1, color=BLUE) for y in [-0.7, -1.1, -1.5]]
            hid_nodes = [Dot([-3.4, y, 0], radius=0.1, color=BLUE) for y in [-0.5, -0.9, -1.3, -1.7]]
            out_nodes = [Dot([-2.4, y, 0], radius=0.1, color=BLUE) for y in [-0.9, -1.3]]

            connections = []
            for n1 in in_nodes:
                for n2 in hid_nodes:
                    connections.append(Line(n1.get_center(), n2.get_center(), stroke_width=1, stroke_opacity=0.35, color=BLUE))
            for n1 in hid_nodes:
                for n2 in out_nodes:
                    connections.append(Line(n1.get_center(), n2.get_center(), stroke_width=1, stroke_opacity=0.35, color=BLUE))

            nn_group = VGroup(*connections, *in_nodes, *hid_nodes, *out_nodes)

            # Connecting arrow to simulated environment
            action_arrow = Arrow([-0.7, -1.1, 0], [0.7, -1.1, 0], color=AMBER, stroke_width=3, tip_length=0.2)

            # Right side: Simulated environment
            env_panel = Panel(width=5.0, height=3.0, color=FAINT).move_to([3.4, -1.0, 0])
            grid = Grid(rows=3, cols=4, cell=0.6, color=FAINT, fill=PANEL).move_to([3.4, -1.1, 0])

            env_agent = Agent(color=BLUE, radius=0.18).move_to(grid.cell(1, 0).get_center())
            coin = VGroup(
                Circle(radius=0.18, stroke_color=AMBER, stroke_width=2, fill_color=AMBER, fill_opacity=0.6),
                Dot(radius=0.06, color=INK),
            ).move_to(grid.cell(0, 2).get_center())
            proxy_box = RoundedRectangle(
                corner_radius=0.08,
                width=0.52,
                height=0.52,
                stroke_color=ROSE,
                stroke_width=2,
                fill_color=ROSE,
                fill_opacity=0.2,
            ).move_to(grid.cell(1, 3).get_center())
            proxy_beacon = Line(
                grid.cell(1, 3).get_corner(UR),
                grid.cell(1, 3).get_corner(DR),
                stroke_color=ROSE,
                stroke_width=3.5,
            )
            proxy_marker = VGroup(proxy_box, proxy_beacon)

            self.play(
                FadeOut(beat2_mobs),
                Transform(tag, new_tag),
                FadeIn(citation_card),
                FadeIn(citation),
                FadeIn(core_question),
                run_time=1.4,
            )

            self.play(
                FadeIn(nn_panel),
                FadeIn(rl_label),
                FadeIn(nn_group),
                FadeIn(env_panel),
                FadeIn(grid),
                FadeIn(coin),
                FadeIn(proxy_marker),
                FadeIn(env_agent),
                run_time=1.5,
            )

            # Action arrow sends pulse; agent steps toward the proxy rather than coin
            self.play(
                GrowArrow(action_arrow),
                Indicate(proxy_marker, color=ROSE),
                run_time=1.0,
            )

            step1 = grid.cell(1, 1).get_center()
            step2 = grid.cell(1, 2).get_center()
            step3 = grid.cell(1, 3).get_center()
            self.play(
                env_agent.animate.move_to(step1),
                run_time=0.7,
            )
            self.play(
                env_agent.animate.move_to(step2),
                run_time=0.7,
            )
            self.play(
                env_agent.animate.move_to(step3),
                run_time=0.7,
            )
