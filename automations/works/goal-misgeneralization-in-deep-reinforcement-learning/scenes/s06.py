# storyboard: 958e2224e4aa2eea
from aisr_kit import *


class S06(NarratedScene):
    def construct(self):
        # Beat 1: Deployment distribution shift and proxy divergence
        with self.beat("s06b01") as b:
            heading = Heading("What This Means for AI Safety")
            tag = Tag("threat_model")
            source = Source(self.paper["short"])

            # Facility environment motif
            facility = Panel(width=11.6, height=4.4, color=FAINT).move_to([0, -0.65, 0])
            dock = RoundedRectangle(
                corner_radius=0.12,
                width=1.4,
                height=1.4,
                stroke_color=MUTED,
                stroke_width=1.5,
                fill_color=PANEL,
                fill_opacity=0.6,
            ).move_to([-4.6, -0.65, 0])
            agent = Agent(color=BLUE, radius=0.22).move_to([-4.6, -0.65, 0])

            # Intended goal station (Teal / Amber)
            intended_box = RoundedRectangle(
                corner_radius=0.12,
                width=2.4,
                height=1.2,
                stroke_color=TEAL,
                stroke_width=1.5,
                stroke_opacity=0.7,
                fill_color=TEAL,
                fill_opacity=0.12,
            ).move_to([4.2, 0.45, 0])
            coin = Circle(radius=0.2, stroke_color=AMBER, stroke_width=2, fill_color=AMBER, fill_opacity=0.85).move_to(intended_box)
            coin_inner = Circle(radius=0.12, stroke_color="#996D14", stroke_width=1.5).move_to(intended_box)
            intended_target = VGroup(intended_box, coin, coin_inner)
            intended_path = DashedLine([-1.0, -0.65, 0], intended_box.get_left(), dash_length=0.12, dashed_ratio=0.5, color=TEAL, stroke_width=2)

            # Development proxy corridor
            proxy_guide = Rectangle(
                width=4.8,
                height=0.8,
                stroke_color=AMBER,
                stroke_width=1.5,
                stroke_opacity=0.4,
                fill_color=AMBER,
                fill_opacity=0.08,
            ).move_to([-1.0, -0.65, 0])
            proxy_label = T("Development proxy", size=20, color=AMBER, weight=MEDIUM).move_to([-1.0, 0.05, 0])
            proxy_arrow = Arrow([-3.6, -0.65, 0], [1.2, -0.65, 0], stroke_width=2.5, color=AMBER, buff=0, max_tip_length_to_length_ratio=0.15)
            proxy_group = VGroup(proxy_guide, proxy_label, proxy_arrow)

            # Distribution shift indicator
            shift_box = RoundedRectangle(
                corner_radius=0.12,
                width=5.8,
                height=0.48,
                stroke_color=ROSE,
                stroke_width=1.5,
                fill_color=PANEL,
                fill_opacity=0.9,
            ).move_to([0, 1.25, 0])
            shift_label = T("Deployment distribution shift", size=20, color=ROSE, weight=SEMIBOLD).move_to(shift_box)
            shift_banner = VGroup(shift_box, shift_label)

            # Divergent behavior station - spacious layout with label below
            dest_box = RoundedRectangle(
                corner_radius=0.12,
                width=2.6,
                height=1.2,
                stroke_color=ROSE,
                stroke_width=1.5,
                fill_color=ROSE,
                fill_opacity=0.18,
            ).move_to([4.2, -1.35, 0])
            hazard = Triangle(color=ROSE).scale(0.18).move_to(dest_box.get_center() + RIGHT * 0.5)
            dest_label = T("Divergent behavior", size=20, color=ROSE, weight=SEMIBOLD).next_to(dest_box, DOWN, buff=0.16)
            divergent_group = VGroup(dest_box, hazard, dest_label)

            # Motion path stopping neatly inside dest_box beside hazard
            path_pts = [
                np.array([-4.6, -0.65, 0]),
                np.array([-1.5, -0.65, 0]),
                np.array([1.2, -0.65, 0]),
                np.array([2.8, -1.05, 0]),
                np.array([3.7, -1.35, 0]),
            ]
            path = VMobject().set_points_smoothly(path_pts)
            trail = DashedVMobject(path, num_dashes=24, dashed_ratio=0.6, color=BLUE)

            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), run_time=0.8)
            self.play(FadeIn(facility), FadeIn(dock), FadeIn(agent), run_time=0.8)
            self.play(FadeIn(proxy_group), FadeIn(intended_target), Create(intended_path), run_time=1.2)
            self.play(FadeIn(shift_banner), run_time=0.8)
            self.play(MoveAlongPath(agent, path), Create(trail), run_time=2.6)
            self.play(FadeIn(divergent_group), dest_box.animate.set_stroke(color=ROSE, width=2.5), run_time=1.0)

            b1_mobs = VGroup(
                facility, dock, agent, intended_target, intended_path,
                proxy_group, shift_banner, divergent_group, trail
            )

        # Beat 2: Scope boundary - Procgen experiments vs theoretical limits
        with self.beat("s06b02") as b:
            tag_b2 = Tag("limitation")

            # Center scope boundary
            divider = DashedLine([0, 1.15, 0], [0, -2.7, 0], dash_length=0.14, dashed_ratio=0.5, color=MUTED, stroke_width=2)
            scope_pill = RoundedRectangle(
                corner_radius=0.14,
                width=2.5,
                height=0.48,
                stroke_color=MUTED,
                stroke_width=1.5,
                fill_color=PANEL,
                fill_opacity=1,
            ).move_to([0, 1.45, 0])
            scope_text = T("Scope boundary", size=20, color=INK, weight=SEMIBOLD).move_to(scope_pill)
            scope_group = VGroup(divider, scope_pill, scope_text)

            # Left side: Experimental setting (positioned with top at 1.1, cleanly below scope_pill)
            left_panel = Panel(width=5.6, height=3.9, color=TEAL).move_to([-3.6, -0.85, 0])
            left_title = T("Feedforward networks in Procgen", size=20, color=TEAL, weight=SEMIBOLD).move_to([-3.6, 0.75, 0])

            # Mini Gridworld
            grid = Grid(rows=3, cols=3, cell=0.58, color=FAINT, fill=PANEL).move_to([-4.7, -0.8, 0])
            grid_agent = Agent(color=BLUE, radius=0.17).move_to(grid.cell(2, 0).get_center())
            grid_coin = Circle(radius=0.14, stroke_color=AMBER, stroke_width=2, fill_color=AMBER, fill_opacity=0.85).move_to(grid.cell(0, 2).get_center())

            # Neural network diagram
            net_dots = VGroup()
            layer_x = [-2.8, -2.1, -1.4]
            layer_ys = [
                [-0.3, -0.8, -1.3],
                [-0.05, -0.55, -1.05, -1.55],
                [-0.55, -1.05],
            ]
            layers = []
            for lx, ys in zip(layer_x, layer_ys):
                dots = [Dot(point=[lx, y, 0], radius=0.07, color=TEAL if lx == -2.8 else BLUE) for y in ys]
                layers.append(dots)
                net_dots.add(*dots)

            net_lines = VGroup()
            for d1 in layers[0]:
                for d2 in layers[1]:
                    net_lines.add(Line(d1.get_center(), d2.get_center(), stroke_width=1, color=FAINT))
            for d1 in layers[1]:
                for d2 in layers[2]:
                    net_lines.add(Line(d1.get_center(), d2.get_center(), stroke_width=1, color=FAINT))

            arrow_in = Arrow(grid.get_right() + RIGHT * 0.05, [-2.85, -0.8, 0], buff=0, stroke_width=1.5, color=TEAL, max_tip_length_to_length_ratio=0.25)
            arrow_out = Arrow([-1.35, -0.8, 0], [-0.95, -0.8, 0], buff=0, stroke_width=2, color=BLUE, max_tip_length_to_length_ratio=0.3)
            left_setting = VGroup(left_panel, left_title, grid, grid_agent, grid_coin, net_lines, net_dots, arrow_in, arrow_out)

            # Right side: Theoretical limits (positioned with top at 1.1, cleanly below scope_pill)
            right_panel = Panel(width=5.6, height=3.9, color=ROSE).move_to([3.6, -0.85, 0])
            right_title = T("Theoretical limits:\nlarge scale and multi-agent", size=20, color=ROSE, weight=SEMIBOLD).move_to([3.6, 0.75, 0])

            # Multi-agent nodes
            a1 = Agent(color=BLUE, radius=0.2).move_to([2.3, -0.6, 0])
            a2 = Agent(color=ROSE, radius=0.2).move_to([4.9, -0.6, 0])
            a3 = Agent(color=AMBER, radius=0.2).move_to([3.6, -1.65, 0])
            link1 = DashedLine(a1.get_right(), a2.get_left(), dash_length=0.1, color=ROSE, stroke_width=2)
            link2 = DashedLine(a1.get_bottom(), a3.get_left(), dash_length=0.1, color=ROSE, stroke_width=2)
            link3 = DashedLine(a2.get_bottom(), a3.get_right(), dash_length=0.1, color=ROSE, stroke_width=2)

            # Large state space sprawl dots & lines
            sprawl_points = [
                [1.9, 0.05, 0], [3.6, 0.15, 0], [5.2, 0.05, 0],
                [1.7, -1.5, 0], [5.4, -1.5, 0], [3.6, -2.15, 0],
            ]
            sprawl_dots = VGroup(*[Dot(point=p, radius=0.05, color=MUTED) for p in sprawl_points])
            sprawl_lines = VGroup(
                Line(sprawl_points[0], sprawl_points[1], stroke_width=1, color=FAINT),
                Line(sprawl_points[1], sprawl_points[2], stroke_width=1, color=FAINT),
                Line(sprawl_points[0], [2.3, -0.6, 0], stroke_width=1, color=FAINT),
                Line(sprawl_points[2], [4.9, -0.6, 0], stroke_width=1, color=FAINT),
                Line(sprawl_points[3], [3.6, -1.65, 0], stroke_width=1, color=FAINT),
                Line(sprawl_points[4], [3.6, -1.65, 0], stroke_width=1, color=FAINT),
            )

            limit_pill = RoundedRectangle(
                corner_radius=0.1,
                width=4.6,
                height=0.48,
                stroke_color=ROSE,
                stroke_width=1.5,
                fill_color=PANEL,
                fill_opacity=0.9,
            ).move_to([3.6, -2.4, 0])
            limit_text = T("Computationally intractable", size=20, color=ROSE, weight=MEDIUM).move_to(limit_pill)
            right_setting = VGroup(right_panel, right_title, sprawl_lines, sprawl_dots, a1, a2, a3, link1, link2, link3, limit_pill, limit_text)

            self.play(
                FadeOut(b1_mobs),
                ReplacementTransform(tag, tag_b2),
                run_time=0.8,
            )
            tag = tag_b2

            self.play(
                FadeIn(left_panel), FadeIn(left_title), Create(grid),
                FadeIn(grid_agent), FadeIn(grid_coin), Create(net_lines),
                FadeIn(net_dots), GrowArrow(arrow_in), GrowArrow(arrow_out),
                run_time=2.4,
            )
            self.play(Create(divider), FadeIn(scope_pill), FadeIn(scope_text), run_time=1.4)
            self.play(
                FadeIn(right_panel), FadeIn(right_title), Create(sprawl_lines),
                FadeIn(sprawl_dots), FadeIn(a1), FadeIn(a2), FadeIn(a3),
                Create(link1), Create(link2), Create(link3),
                run_time=2.8,
            )
            self.play(FadeIn(limit_pill), FadeIn(limit_text), right_panel.animate.set_stroke(color=ROSE, width=2.5), run_time=1.6)
            self.play(Indicate(scope_pill, color=INK), run_time=1.2)

            b2_mobs = VGroup(left_setting, scope_group, right_setting)

        # Beat 3: Core takeaway - Performance is not alignment
        with self.beat("s06b03") as b:
            tag_b3 = Tag("author_interpretation")

            # Header takeaway badge and main thesis
            takeaway_badge = RoundedRectangle(
                corner_radius=0.12,
                width=2.8,
                height=0.48,
                stroke_color=AMBER,
                stroke_width=1.5,
                fill_color=PANEL,
                fill_opacity=1,
            ).move_to([0, 2.15, 0])
            takeaway_text = T("Core takeaway", size=22, color=AMBER, weight=SEMIBOLD).move_to(takeaway_badge)
            takeaway_group = VGroup(takeaway_badge, takeaway_text)

            thesis_text = Serif("Performance is not alignment", size=30, color=INK).move_to([0, 1.5, 0])

            # Balance scale structure: pillar & fulcrum
            fulcrum = Triangle(color=MUTED, stroke_width=2, fill_color=PANEL, fill_opacity=1).scale(0.28).move_to([0, -2.1, 0])
            pillar = Line([0, -1.9, 0], [0, 0.4, 0], stroke_width=4.5, color=MUTED)
            pivot = Dot(point=[0, 0.4, 0], radius=0.09, color=INK)

            # Tilted beam: left end down at y=0.05, right end up at y=0.75
            beam = Line([-3.4, 0.05, 0], [3.4, 0.75, 0], stroke_width=4.5, color=INK)

            # Left pan (training performance): plate at y=-1.65, card sits on top of plate
            pan_left_plate = Line([-4.5, -1.65, 0], [-2.3, -1.65, 0], stroke_width=3, color=MUTED)
            string_l1 = Line([-3.4, 0.05, 0], [-4.4, -1.65, 0], stroke_width=1.5, color=MUTED)
            string_l2 = Line([-3.4, 0.05, 0], [-2.4, -1.65, 0], stroke_width=1.5, color=MUTED)

            card_left = Panel(width=3.2, height=1.35, color=TEAL).move_to([-3.4, -0.95, 0])
            card_left_title = T("High training performance", size=20, color=TEAL, weight=MEDIUM).move_to([-3.4, -0.55, 0])
            bar1 = Rectangle(width=0.25, height=0.35, fill_color=TEAL, fill_opacity=0.9, stroke_width=0).move_to([-3.8, -1.15, 0])
            bar2 = Rectangle(width=0.25, height=0.55, fill_color=TEAL, fill_opacity=0.9, stroke_width=0).move_to([-3.4, -1.05, 0])
            bar3 = Rectangle(width=0.25, height=0.75, fill_color=TEAL, fill_opacity=0.9, stroke_width=0).move_to([-3.0, -0.95, 0])
            perf_bars = VGroup(bar1, bar2, bar3)
            left_scale_content = VGroup(pan_left_plate, string_l1, string_l2, card_left, card_left_title, perf_bars)

            # Right pan (divergent objective): plate at y=-0.95, card sits on top of plate
            pan_right_plate = Line([2.3, -0.95, 0], [4.5, -0.95, 0], stroke_width=3, color=MUTED)
            string_r1 = Line([3.4, 0.75, 0], [2.4, -0.95, 0], stroke_width=1.5, color=MUTED)
            string_r2 = Line([3.4, 0.75, 0], [4.4, -0.95, 0], stroke_width=1.5, color=MUTED)

            card_right = Panel(width=3.2, height=1.35, color=ROSE).move_to([3.4, -0.25, 0])
            card_right_title = T("Divergent objective", size=20, color=ROSE, weight=MEDIUM).move_to([3.4, 0.15, 0])
            agent_right = Agent(color=BLUE, radius=0.18).move_to([2.9, -0.4, 0])
            diverge_arrow = Arrow([3.1, -0.4, 0], [3.8, -0.4, 0], stroke_width=2.5, color=ROSE, buff=0, max_tip_length_to_length_ratio=0.25)
            right_scale_content = VGroup(pan_right_plate, string_r1, string_r2, card_right, card_right_title, agent_right, diverge_arrow)

            # Bottom takeaway summary
            summary_box = RoundedRectangle(
                corner_radius=0.14,
                width=8.2,
                height=0.55,
                stroke_color=ROSE,
                stroke_width=1.5,
                fill_color=PANEL,
                fill_opacity=0.95,
            ).move_to([0, -2.75, 0])
            summary_label = T("Capable pursuit of unintended goals", size=22, color=ROSE, weight=SEMIBOLD).move_to(summary_box)
            summary_group = VGroup(summary_box, summary_label)

            self.play(
                FadeOut(b2_mobs),
                ReplacementTransform(tag, tag_b3),
                run_time=0.8,
            )
            tag = tag_b3

            self.play(FadeIn(takeaway_group), FadeIn(thesis_text), run_time=1.0)
            self.play(
                FadeIn(fulcrum), FadeIn(pillar), FadeIn(pivot),
                Create(beam),
                FadeIn(left_scale_content),
                FadeIn(right_scale_content),
                run_time=2.4,
            )
            self.play(FadeIn(summary_group), summary_box.animate.set_stroke(color=ROSE, width=2.5), run_time=1.4)
            self.play(Indicate(summary_label, color=INK), run_time=1.2)
