# storyboard: d7ff94cf01757ed6
from aisr_kit import *


def make_coin(pos):
    glow = Circle(radius=0.3, stroke_width=0, fill_color=AMBER, fill_opacity=0.25).move_to(pos)
    body = Circle(radius=0.18, stroke_color=AMBER, stroke_width=2, fill_color=AMBER, fill_opacity=0.9).move_to(pos)
    inner = Circle(radius=0.11, stroke_color="#FFF2A3", stroke_width=1.5).move_to(pos)
    return VGroup(glow, body, inner)


class S04(NarratedScene):
    def construct(self):
        # --- Beat 1: Network architecture ---
        with self.beat("s04b01") as b:
            heading = Heading("Actor and critic disagreement")
            tag = Tag("method")
            source = Source(self.paper["short"])

            b1_title = T("Actor-critic architecture", size=24, color=INK, weight=SEMIBOLD).move_to([0, 2.15, 0])

            # Visual input panel
            obs_box = RoundedRectangle(
                corner_radius=0.12, width=2.2, height=1.6,
                stroke_color=FAINT, stroke_width=1.5, fill_color=PANEL, fill_opacity=0.95
            ).move_to([-4.6, -0.15, 0])
            obs_floor = Line([-5.5, -0.55, 0], [-3.7, -0.55, 0], stroke_width=2, color=FAINT)
            obs_agent = Dot([-5.0, -0.35, 0], radius=0.14, color=BLUE)
            obs_coin = Dot([-4.0, -0.35, 0], radius=0.1, color=AMBER)
            obs_group = VGroup(obs_box, obs_floor, obs_agent, obs_coin)

            arrow_in = Arrow([-3.5, -0.15, 0], [-2.3, -0.15, 0], stroke_width=2.5, color=MUTED, buff=0.08)

            # Shared convolutional trunk
            trunk_box = RoundedRectangle(
                corner_radius=0.15, width=3.2, height=2.2,
                stroke_color=TEAL, stroke_width=2, fill_color=PANEL, fill_opacity=0.95
            ).move_to([-0.7, -0.15, 0])
            trunk_label = T("Shared vision trunk", size=20, color=INK, weight=SEMIBOLD).move_to([-0.7, 0.5, 0])
            conv1 = RoundedRectangle(corner_radius=0.06, width=2.4, height=0.24, stroke_color=TEAL, stroke_width=1.2, fill_color=TEAL, fill_opacity=0.2).move_to([-0.7, 0.05, 0])
            conv2 = RoundedRectangle(corner_radius=0.06, width=2.1, height=0.24, stroke_color=TEAL, stroke_width=1.2, fill_color=TEAL, fill_opacity=0.3).move_to([-0.7, -0.35, 0])
            conv3 = RoundedRectangle(corner_radius=0.06, width=1.8, height=0.24, stroke_color=TEAL, stroke_width=1.2, fill_color=TEAL, fill_opacity=0.4).move_to([-0.7, -0.75, 0])
            trunk_group = VGroup(trunk_box, trunk_label, conv1, conv2, conv3)

            # Branch to Actor
            arrow_actor = Arrow([0.9, 0.15, 0], [2.1, 0.75, 0], stroke_width=2.5, color=BLUE, buff=0.08)
            actor_box = RoundedRectangle(
                corner_radius=0.15, width=4.1, height=1.4,
                stroke_color=BLUE, stroke_width=2, fill_color=PANEL, fill_opacity=0.95
            ).move_to([4.2, 0.85, 0])
            actor_label = T("Actor: chooses actions", size=20, color=BLUE, weight=SEMIBOLD).move_to([4.2, 1.2, 0])
            ag_actor = Agent(color=BLUE, radius=0.18).move_to([2.75, 0.65, 0])
            act_up = Arrow([3.15, 0.65, 0], [3.6, 0.92, 0], stroke_width=2, color=MUTED, buff=0)
            act_down = Arrow([3.15, 0.65, 0], [3.6, 0.38, 0], stroke_width=2, color=MUTED, buff=0)
            act_main = Arrow([3.15, 0.65, 0], [4.3, 0.65, 0], stroke_width=3.5, color=BLUE, buff=0)
            actor_group = VGroup(actor_box, actor_label, ag_actor, act_up, act_down, act_main)

            # Branch to Critic
            arrow_critic = Arrow([0.9, -0.45, 0], [2.1, -1.05, 0], stroke_width=2.5, color=AMBER, buff=0.08)
            critic_box = RoundedRectangle(
                corner_radius=0.15, width=4.1, height=1.4,
                stroke_color=AMBER, stroke_width=2, fill_color=PANEL, fill_opacity=0.95
            ).move_to([4.2, -1.15, 0])
            critic_label = T("Critic: evaluates state", size=20, color=AMBER, weight=SEMIBOLD).move_to([4.2, -0.8, 0])
            critic_track = Line([2.7, -1.35, 0], [5.7, -1.35, 0], stroke_width=3, color=FAINT)
            critic_curve = VMobject(color=AMBER, stroke_width=2.5).set_points_smoothly([[2.7, -1.4, 0], [3.7, -1.35, 0], [4.7, -1.25, 0], [5.5, -1.05, 0]])
            critic_dot = Dot([5.5, -1.05, 0], radius=0.06, color=AMBER)
            critic_group = VGroup(critic_box, critic_label, critic_track, critic_curve, critic_dot)

            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), FadeIn(b1_title), run_time=0.8)
            self.play(FadeIn(obs_group), GrowArrow(arrow_in), FadeIn(trunk_group), run_time=1.2)
            self.play(GrowArrow(arrow_actor), FadeIn(actor_group), run_time=1.0)
            self.play(GrowArrow(arrow_critic), FadeIn(critic_group), run_time=1.0)
            self.play(Indicate(act_main, color=INK), Indicate(critic_dot, color=INK), run_time=0.8)

            b1_elements = VGroup(
                b1_title, obs_group, arrow_in, trunk_group,
                arrow_actor, actor_group, arrow_critic, critic_group
            )

        # --- Beat 2: Critic evaluation ---
        with self.beat("s04b02") as b:
            tag_b2 = Tag("observed_result")
            b2_title = T("Critic evaluation", size=24, color=INK, weight=SEMIBOLD).move_to([0, 2.15, 0])

            # Upper: CoinRun Environment
            env_box = RoundedRectangle(
                corner_radius=0.15, width=10.4, height=2.3,
                stroke_color=TEAL, stroke_width=2, fill_color=PANEL, fill_opacity=0.95
            ).move_to([0, 0.75, 0])
            floor = Line([-4.9, -0.15, 0], [4.9, -0.15, 0], stroke_width=2.5, color=FAINT)
            ground = Rectangle(width=9.8, height=0.2, stroke_width=0, fill_color=FAINT, fill_opacity=0.15).next_to(floor, DOWN, buff=0)
            wall_solid = Rectangle(width=0.3, height=1.7, stroke_color=FAINT, stroke_width=1.5, fill_color=FAINT, fill_opacity=0.6).move_to([2.0, 0.7, 0])
            agent_b2 = Agent(color=BLUE, radius=0.22).move_to([-4.0, 0.1, 0])
            coin_b2 = make_coin([-1.0, 0.15, 0])

            coin_label = T("Coin ignored", size=20, color=ROSE, weight=MEDIUM).move_to([-1.0, 1.5, 0])
            coin_line = DashedLine([-1.0, 1.35, 0], [-1.0, 0.45, 0], stroke_width=1.5, color=ROSE)
            coin_callout = VGroup(coin_label, coin_line)

            # Lower: Critic Value Profile
            val_box = RoundedRectangle(
                corner_radius=0.15, width=10.4, height=2.0,
                stroke_color=FAINT, stroke_width=1.5, fill_color=PANEL, fill_opacity=0.9
            ).move_to([0, -1.75, 0])
            baseline = Line([-4.6, -2.35, 0], [4.6, -2.35, 0], stroke_width=2, color=MUTED)
            wall_proj = DashedLine([2.0, -0.15, 0], [2.0, -1.1, 0], stroke_width=1.5, color=AMBER, stroke_opacity=0.6)
            curve = VMobject(color=AMBER, stroke_width=3.5).set_points_smoothly([
                [-4.2, -2.25, 0], [-2.5, -2.2, 0], [-1.0, -2.15, 0], [0.5, -1.95, 0], [1.5, -1.5, 0], [2.0, -1.1, 0]
            ])
            peak_dot = Dot([2.0, -1.1, 0], radius=0.08, color=AMBER)
            peak_ring = Circle(radius=0.18, stroke_color=AMBER, stroke_width=1.5).move_to([2.0, -1.1, 0])
            wall_val_label = T("High value at wall", size=22, color=AMBER, weight=SEMIBOLD).move_to([0.2, -1.1, 0])
            peak_arrow = Arrow([1.2, -1.1, 0], [1.8, -1.1, 0], stroke_width=2.5, color=AMBER, buff=0.05)
            schematic_label = T("Schematic value curve", size=20, color=SOFT).move_to([-2.7, -2.6, 0])
            val_group = VGroup(val_box, baseline, wall_proj, curve, peak_dot, peak_ring, wall_val_label, peak_arrow, schematic_label)

            self.play(ReplacementTransform(tag, tag_b2), FadeOut(b1_elements), run_time=0.8)
            tag = tag_b2
            self.play(
                FadeIn(b2_title), FadeIn(env_box), FadeIn(floor), FadeIn(ground),
                FadeIn(wall_solid), FadeIn(agent_b2), FadeIn(coin_b2),
                run_time=1.0
            )
            self.play(FadeIn(coin_callout), run_time=0.6)
            self.play(FadeIn(val_box), FadeIn(baseline), FadeIn(wall_proj), run_time=0.6)
            self.play(Create(curve), run_time=1.2)
            self.play(FadeIn(peak_dot), FadeIn(peak_ring), FadeIn(wall_val_label), GrowArrow(peak_arrow), run_time=0.8)
            self.play(FadeIn(schematic_label), coin_b2.animate.set_opacity(0.15), run_time=0.7)
            self.play(Indicate(peak_ring), coin_b2.animate.set_opacity(1), run_time=0.7)

            b2_elements = VGroup(
                b2_title, coin_callout, coin_b2, wall_solid, val_group
            )

        # --- Beat 3: Permeable wall test ---
        with self.beat("s04b03") as b:
            tag_b3 = Tag("observed_result")
            b3_title = T("Permeable wall test", size=24, color=INK, weight=SEMIBOLD).move_to([0, 2.15, 0])

            # Permeable wall at x = 2.0 (dashed barrier)
            perm_wall = VGroup(*[
                DashedLine([2.0 - 0.08 + i * 0.16, -0.15, 0], [2.0 - 0.08 + i * 0.16, 1.55, 0],
                           stroke_width=2.5, color=MUTED, dash_length=0.12)
                for i in range(2)
            ])

            # Path taken by agent through the wall
            path_through = DashedLine([-4.0, 0.1, 0], [3.8, 0.1, 0], stroke_width=2, color=BLUE)
            arrow_mid = Arrow([1.4, 0.1, 0], [2.4, 0.1, 0], stroke_width=3, color=BLUE, buff=0)
            action_arrow = Arrow([4.1, 0.1, 0], [4.7, 0.1, 0], stroke_width=3.5, color=BLUE, buff=0)

            # Lower comparison cards
            card_critic = Panel(width=4.8, height=2.1, color=FAINT).move_to([-2.6, -1.75, 0])
            t_crit_head = T("Critic: evaluated wall", size=20, color=AMBER, weight=SEMIBOLD).move_to([-2.6, -0.95, 0])
            crit_thumb_base = Line([-4.5, -2.4, 0], [-0.7, -2.4, 0], stroke_width=1.5, color=MUTED)
            crit_thumb_curve = VMobject(color=AMBER, stroke_width=2.5).set_points_smoothly([
                [-4.3, -2.35, 0], [-3.0, -2.3, 0], [-1.8, -2.1, 0], [-0.9, -1.4, 0]
            ])
            crit_thumb_wall = DashedLine([-0.9, -2.4, 0], [-0.9, -1.3, 0], stroke_width=1.5, color=AMBER)
            crit_thumb_dot = Dot([-0.9, -1.4, 0], radius=0.06, color=AMBER)
            thumb_label = T("Schematic value curve", size=20, color=SOFT).move_to([-2.6, -2.6, 0])
            card_crit_group = VGroup(card_critic, t_crit_head, crit_thumb_base, crit_thumb_curve, crit_thumb_wall, crit_thumb_dot, thumb_label)

            card_actor = Panel(width=4.8, height=2.1, color=BLUE).move_to([2.6, -1.75, 0])
            stat_val = self.dataset("d3")["points"][0]["display"]
            stat_text = T(stat_val, size=36, color=AMBER, weight=SEMIBOLD).move_to([2.6, -1.15, 0])
            actor_takeaway = T("Actor pursues move-right proxy", size=20, color=BLUE, weight=SEMIBOLD, width=17).move_to([2.6, -1.8, 0])
            card_act_group = VGroup(card_actor, stat_text, actor_takeaway)

            self.play(
                ReplacementTransform(tag, tag_b3),
                FadeOut(b2_elements),
                FadeIn(b3_title),
                env_box.animate.set_stroke(color=AMBER),
                FadeIn(perm_wall),
                run_time=0.9
            )
            tag = tag_b3

            # Agent approaches and passes straight through permeable wall to the right
            self.play(
                agent_b2.animate.move_to([3.8, 0.1, 0]),
                Create(path_through),
                GrowArrow(arrow_mid),
                GrowArrow(action_arrow),
                run_time=2.2
            )

            # Lower comparison cards reveal actor-critic disagreement
            self.play(FadeIn(card_crit_group), run_time=0.9)
            self.play(FadeIn(card_act_group), run_time=1.0)
            self.play(Indicate(stat_text, color=INK), run_time=0.6)
