# storyboard: 768a9e7dcbc43daa
from aisr_kit import *


def make_coin(pos, radius=0.22):
    glow = Circle(radius=radius * 1.6, stroke_width=0, fill_color=AMBER, fill_opacity=0.22).move_to(pos)
    body = Circle(radius=radius, stroke_color=AMBER, stroke_width=2, fill_color=AMBER, fill_opacity=0.9).move_to(pos)
    inner = Circle(radius=radius * 0.6, stroke_color="#996D14", stroke_width=1.5).move_to(pos)
    coin = VGroup(glow, body, inner)
    coin.body = body
    return coin


def make_spikes(x_start, y_base, count=3, width=0.35, height=0.55):
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


class S05(NarratedScene):
    def construct(self):
        # --- Beat 1: Decorrelating proxies across diverse training levels ---
        with self.beat("s05b01") as b:
            heading = Heading("Fixing proxies through diversity")
            tag = Tag("hypothesis")
            source = Source(self.paper["short"])

            b1_title = T("Decorrelating proxies", size=32, color=INK, weight=SEMIBOLD).move_to([0, 2.25, 0])

            # Left panel: Environment variation with diverse levels
            left_panel = Panel(width=5.8, height=3.8, color=TEAL).move_to([-3.2, -0.3, 0])
            left_header = T("Environment variation", size=32, color=TEAL, weight=SEMIBOLD).move_to([-3.2, 1.2, 0])

            # Diverse mini levels
            # Level A: coin at center
            track_a = Line([-5.7, 0.25, 0], [-0.7, 0.25, 0], stroke_width=2, color=FAINT)
            wall_a = Rectangle(width=0.18, height=0.55, stroke_width=0, fill_color=FAINT, fill_opacity=0.6).move_to([-0.8, 0.525, 0])
            agent_a = Agent(color=BLUE, radius=0.14).move_to([-5.3, 0.39, 0])
            coin_a = make_coin([-3.2, 0.45, 0], radius=0.14)
            path_a = DashedLine([-5.1, 0.39, 0], [-3.4, 0.39, 0], stroke_width=1.5, color=BLUE)
            empty_a = Circle(radius=0.12, stroke_color=MUTED, stroke_width=1.2, stroke_opacity=0.4).move_to([-1.2, 0.45, 0])
            level_a = VGroup(track_a, wall_a, agent_a, coin_a, path_a, empty_a)

            # Level B: coin on elevated platform
            track_b = Line([-5.7, -0.55, 0], [-0.7, -0.55, 0], stroke_width=2, color=FAINT)
            wall_b = Rectangle(width=0.18, height=0.55, stroke_width=0, fill_color=FAINT, fill_opacity=0.6).move_to([-0.8, -0.275, 0])
            plat_b = RoundedRectangle(corner_radius=0.04, width=1.0, height=0.14, stroke_width=0, fill_color=FAINT, fill_opacity=0.7).move_to([-3.6, -0.2, 0])
            agent_b = Agent(color=BLUE, radius=0.14).move_to([-5.3, -0.41, 0])
            coin_b = make_coin([-3.6, 0.05, 0], radius=0.14)
            path_b = DashedLine([-5.1, -0.41, 0], [-3.8, -0.05, 0], stroke_width=1.5, color=BLUE)
            empty_b = Circle(radius=0.12, stroke_color=MUTED, stroke_width=1.2, stroke_opacity=0.4).move_to([-1.2, -0.35, 0])
            level_b = VGroup(track_b, wall_b, plat_b, agent_b, coin_b, path_b, empty_b)

            # Level C: coin near start
            track_c = Line([-5.7, -1.35, 0], [-0.7, -1.35, 0], stroke_width=2, color=FAINT)
            wall_c = Rectangle(width=0.18, height=0.55, stroke_width=0, fill_color=FAINT, fill_opacity=0.6).move_to([-0.8, -1.075, 0])
            agent_c = Agent(color=BLUE, radius=0.14).move_to([-5.3, -1.21, 0])
            coin_c = make_coin([-4.2, -1.15, 0], radius=0.14)
            path_c = DashedLine([-5.1, -1.21, 0], [-4.4, -1.21, 0], stroke_width=1.5, color=BLUE)
            empty_c = Circle(radius=0.12, stroke_color=MUTED, stroke_width=1.2, stroke_opacity=0.4).move_to([-1.2, -1.15, 0])
            level_c = VGroup(track_c, wall_c, agent_c, coin_c, path_c, empty_c)

            diverse_levels = VGroup(level_a, level_b, level_c)
            left_group = VGroup(left_panel, left_header, diverse_levels)

            # Right panel: Correlation decoupling
            right_panel = Panel(width=5.6, height=3.8, color=FAINT).move_to([3.3, -0.3, 0])
            right_header = T("Training correlation", size=32, color=INK, weight=SEMIBOLD).move_to([3.3, 1.2, 0])
            weak_header = T("Correlation weakened", size=32, color=INK, weight=SEMIBOLD).move_to([3.3, 1.2, 0])

            coin_node = Node("True reward: coin", color=AMBER, width=4.9, height=0.75, size=28, fill=0.2).move_to([3.3, 0.5, 0])
            wall_node = Node("Proxy: reach right wall", color=ROSE, width=4.9, height=0.75, size=28, fill=0.15).move_to([3.3, -0.95, 0])

            corr_arrow = DoubleArrow(coin_node.get_bottom(), wall_node.get_top(), buff=0.15, stroke_width=2.5, color=MUTED)
            corr_label = T("Always co-occurred", size=30, color=SOFT).move_to([3.3, -1.75, 0])

            # A weaker link: thinner and dimmer, but still present.
            weak_arrow = DashedLine(coin_node.get_bottom(), wall_node.get_top(), buff=0.15, dash_length=0.08,
                                    stroke_width=2.5, color=SOFT, stroke_opacity=0.75)
            decorr_label = T("Weakened by variation", size=30, color=TEAL, weight=SEMIBOLD).move_to([3.3, -1.75, 0])

            self.play(
                FadeIn(heading), FadeIn(tag), FadeIn(source), FadeIn(b1_title),
                FadeIn(left_panel), FadeIn(left_header), FadeIn(diverse_levels),
                FadeIn(right_panel), FadeIn(right_header),
                FadeIn(coin_node), FadeIn(wall_node),
                run_time=0.6
            )
            self.play(GrowArrow(corr_arrow), FadeIn(corr_label), run_time=0.8)
            self.wait(1.4)
            self.play(
                FadeOut(corr_arrow), FadeIn(weak_arrow),
                FadeOut(corr_label), FadeIn(decorr_label),
                FadeOut(right_header), FadeIn(weak_header),
                coin_node.box.animate.set_stroke(color=AMBER, width=2.5),
                run_time=1.2
            )

            b1_all = VGroup(b1_title, left_group, right_panel, weak_header, coin_node, wall_node, weak_arrow, decorr_label)

        # --- Beat 2: CoinRun training comparison and 2% randomized levels ---
        with self.beat("s05b02") as b:
            tag_b2 = Tag("observed_result")
            b2_title = T("CoinRun training", size=32, color=INK, weight=SEMIBOLD).move_to([0, 2.25, 0])

            # Left panel: Standard training
            card_std = Panel(width=5.4, height=3.2, color=FAINT).move_to([-3.3, 0.1, 0])
            title_std = T("Standard training", size=30, color=ROSE, weight=SEMIBOLD).move_to([-3.3, 1.3, 0])
            track_std = Line([-5.6, -0.3, 0], [-1.0, -0.3, 0], stroke_width=2.5, color=FAINT)
            wall_std = Rectangle(width=0.2, height=1.3, stroke_width=0, fill_color=FAINT, fill_opacity=0.6).move_to([-1.1, 0.35, 0])
            agent_std = Agent(color=BLUE, radius=0.18).move_to([-5.1, -0.12, 0])
            coin_std = make_coin([-3.3, -0.08, 0], radius=0.18)
            path_std = DashedLine([-5.1, -0.12, 0], [-1.3, -0.12, 0], stroke_width=2.5, color=ROSE)
            desc_std = T("Ignores moved coin", size=30, color=ROSE, weight=SEMIBOLD).move_to([-3.3, -1.0, 0])
            group_std = VGroup(card_std, title_std, track_std, wall_std, coin_std, path_std, agent_std, desc_std)

            # Right panel: 2% randomized levels
            card_rand = Panel(width=5.4, height=3.2, color=TEAL).move_to([3.3, 0.1, 0])
            title_rand = T("2% randomized levels", size=30, color=TEAL, weight=SEMIBOLD).move_to([3.3, 1.3, 0])

            # BarChart from dataset d1
            d1 = self.dataset("d1")
            chart = BarChart(d1["points"], colors=[TEAL], width=4.4, height=1.1, max_value=100, label_size=28)
            chart.move_to([3.3, -0.05, 0])
            group_rand = VGroup(card_rand, title_rand, chart)

            # Bottom banner
            banner_box = RoundedRectangle(corner_radius=0.15, width=9.8, height=0.75, stroke_color=TEAL, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to([0, -2.15, 0])
            banner_text = T("Goal generalization greatly improved", size=30, color=TEAL, weight=SEMIBOLD).move_to(banner_box)
            banner = VGroup(banner_box, banner_text)

            # Clean swap at the beat boundary.
            self.play(
                FadeOut(tag), FadeIn(tag_b2),
                FadeOut(b1_all),
                FadeIn(b2_title),
                run_time=0.2
            )
            tag = tag_b2

            self.play(FadeIn(group_std), FadeIn(card_rand), FadeIn(title_rand), run_time=0.5)
            self.play(FadeIn(chart.frame), run_time=0.6)
            self.play(bars_grow(chart), FadeIn(chart.values), run_time=0.8)
            self.play(agent_std.animate.move_to([-1.4, -0.12, 0]), FadeIn(banner), run_time=1.5)

            b2_all = VGroup(b2_title, group_std, group_rand, banner)

        # --- Beat 3: Dynamic level generation and true goal tracked ---
        with self.beat("s05b03") as b:
            tag_b3 = Tag("author_interpretation")
            b3_title = T("Varied locations", size=32, color=INK, weight=SEMIBOLD).move_to([0, 2.25, 0])

            floor_y = -1.7
            level_box = RoundedRectangle(
                corner_radius=0.18, width=11.2, height=4.2,
                stroke_color=TEAL, stroke_width=2.5, fill_color=PANEL, fill_opacity=0.95
            ).move_to([0, -0.4, 0])

            floor = Line([-5.3, floor_y, 0], [5.3, floor_y, 0], stroke_width=3, color=FAINT)
            ground = Rectangle(width=10.6, height=0.5, stroke_width=0, fill_color=FAINT, fill_opacity=0.2).next_to(floor, DOWN, buff=0)
            wall = Rectangle(width=0.3, height=2.6, stroke_color=FAINT, stroke_width=1.5, fill_color=FAINT, fill_opacity=0.5).move_to([5.15, -0.4, 0])

            platform = RoundedRectangle(corner_radius=0.08, width=2.4, height=0.26, stroke_color=FAINT, stroke_width=1.5, fill_color=FAINT, fill_opacity=0.6).move_to([-0.6, floor_y + 1.35, 0])
            spikes = make_spikes(-0.8, floor_y, count=3, width=0.35, height=0.55)

            agent = Agent(color=BLUE, radius=0.22).move_to([-4.4, floor_y + 0.22, 0])

            # The rightward shortcut along the floor to the wall
            shortcut_line = DashedLine([-4.4, floor_y + 0.22, 0], [4.7, floor_y + 0.22, 0], stroke_width=3, color=ROSE)
            shortcut_label = T("Rightward shortcut", size=30, color=ROSE, weight=SEMIBOLD).move_to([3.0, floor_y + 1.05, 0])
            weak_label = T("Shortcut weakened", size=30, color=ROSE, weight=SEMIBOLD).move_to([3.0, floor_y + 1.05, 0])

            # Varied coin placements across training levels (outlines), plus this level's coin
            ghost_coins = VGroup(*[
                Circle(radius=0.22, stroke_color=AMBER, stroke_width=2, stroke_opacity=0.55).move_to([x, floor_y + 0.45, 0])
                for x in (-2.9, 1.9, 4.4)
            ])

            coin_pos = np.array([-0.45, floor_y + 1.62, 0])
            coin = make_coin(coin_pos)

            # Leap trajectory to coin
            leap_curve = VMobject()
            leap_curve.set_points_smoothly([
                np.array([-4.4, floor_y + 0.22, 0]),
                np.array([-2.4, floor_y + 0.22, 0]),
                np.array([-1.6, floor_y + 1.1, 0]),
                np.array([-0.95, floor_y + 1.57, 0]),
            ])
            leap_trail = DashedVMobject(leap_curve, num_dashes=18, dashed_ratio=0.5, color=BLUE)

            goal_badge = Node("Goal generalization improved", color=TEAL, height=0.7, size=28, fill=0.25).move_to([-2.55, 0.85, 0])

            # Clean swap at the beat boundary.
            self.play(
                FadeOut(tag), FadeIn(tag_b3),
                FadeOut(b2_all),
                FadeIn(b3_title),
                run_time=0.2
            )
            tag = tag_b3

            self.play(
                FadeIn(level_box), FadeIn(floor), FadeIn(ground), FadeIn(wall),
                FadeIn(platform), FadeIn(spikes), FadeIn(agent),
                FadeIn(shortcut_line), FadeIn(shortcut_label),
                run_time=0.8
            )
            self.wait(0.4)

            # Coins appear in varied places; the shortcut weakens but does not vanish
            self.play(LaggedStart(*[FadeIn(g) for g in ghost_coins], FadeIn(coin), lag_ratio=0.25), run_time=1.2)
            self.play(
                shortcut_line.animate.set_stroke(width=2, opacity=0.6),
                FadeOut(shortcut_label), FadeIn(weak_label),
                run_time=1.0
            )
            self.wait(0.3)

            # Agent turns toward the coin and leaps onto the platform
            self.play(
                MoveAlongPath(agent, leap_curve),
                Create(leap_trail),
                run_time=2.2,
                rate_func=linear
            )

            # Coin collection pulse and the observed improvement
            self.play(coin.animate.scale(1.2), run_time=0.25)
            self.play(
                coin.animate.scale(1 / 1.2),
                FadeIn(goal_badge),
                run_time=0.8
            )
