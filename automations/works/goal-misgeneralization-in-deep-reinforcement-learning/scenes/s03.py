# storyboard: 8101ad3582908eec
from aisr_kit import *


def make_gem():
    gem = Square(side_length=0.32, fill_color=AMBER, fill_opacity=0.9, stroke_color=INK, stroke_width=1.5)
    gem.rotate(np.pi / 4)
    return gem


def make_chest():
    box = RoundedRectangle(corner_radius=0.04, width=0.42, height=0.32, stroke_color=AMBER,
                           stroke_width=2, fill_color="#3A2810", fill_opacity=1)
    band = Line(box.get_left(), box.get_right(), color=AMBER, stroke_width=1.5)
    lock = Dot(point=box.get_center(), radius=0.04, color=INK)
    return VGroup(box, band, lock)


def make_key():
    ring = Circle(radius=0.07, stroke_color=TEAL, stroke_width=2, fill_opacity=0)
    shaft = Line(ring.get_right(), ring.get_right() + RIGHT * 0.14, color=TEAL, stroke_width=2)
    bit = Line(shaft.get_end(), shaft.get_end() + DOWN * 0.07, color=TEAL, stroke_width=2)
    group = VGroup(ring, shaft, bit)
    group.move_to(ORIGIN)
    return group


class S03(NarratedScene):
    def construct(self):
        # Beat 1: Feature correlation
        with self.beat("s03b01") as b:
            heading = Heading("Why learned proxies take over")
            tag = Tag("hypothesis")
            source = Source(self.paper["short"])

            b1_title = T("Feature correlation", size=26, color=INK, weight=SEMIBOLD).move_to(UP * 2.1)

            # Left card: intended goal
            card_left = Panel(width=4.3, height=3.0, color=FAINT).move_to(LEFT * 3.2 + DOWN * 0.1)
            title_left = T("Intended: reach coin", size=22, color=INK, weight=MEDIUM).move_to(card_left.get_top() + DOWN * 0.35)
            coin_circle = Circle(radius=0.35, color=AMBER, fill_color=AMBER, fill_opacity=0.9)
            coin_inner = Circle(radius=0.22, stroke_color="#FFF2A3", stroke_width=2)
            coin_vis = VGroup(coin_circle, coin_inner).move_to(card_left.get_center() + UP * 0.1)
            desc_left = T("Visual object tracking", size=20, color=MUTED).move_to(card_left.get_bottom() + UP * 0.4)
            card_left_group = VGroup(card_left, title_left, coin_vis, desc_left)

            # Right card: proxy shortcut
            card_right = Panel(width=4.3, height=3.0, color=FAINT).move_to(RIGHT * 3.2 + DOWN * 0.1)
            title_right = T("Shortcut: move right", size=22, color=INK, weight=MEDIUM).move_to(card_right.get_top() + DOWN * 0.35)
            agent_b1 = Agent(color=BLUE, radius=0.28)
            arrow_right = Arrow(LEFT * 0.3, RIGHT * 0.6, stroke_width=3.5, color=VIOLET, buff=0)
            move_vis = VGroup(agent_b1, arrow_right).arrange(RIGHT, buff=0.25).move_to(card_right.get_center() + UP * 0.1)
            desc_right = T("Simpler directional cue", size=20, color=MUTED).move_to(card_right.get_bottom() + UP * 0.4)
            card_right_group = VGroup(card_right, title_right, move_vis, desc_right)

            # Correlation link
            corr_arrow = DoubleArrow(card_left.get_right() + RIGHT * 0.2, card_right.get_left() + LEFT * 0.2, buff=0, stroke_width=2.5, color=MUTED)
            corr_label = T("Always\nco-occur", size=20, color=MUTED).next_to(corr_arrow, UP, buff=0.15)
            corr_group = VGroup(corr_arrow, corr_label)

            # Simplicity bias hypothesis badge
            hypo_badge = RoundedRectangle(corner_radius=0.15, width=7.4, height=0.55, stroke_color=VIOLET, stroke_width=1.5, fill_color=PANEL, fill_opacity=1)
            hypo_text = T("Hypothesis: proxy favored by bias", size=22, color=VIOLET, weight=SEMIBOLD).move_to(hypo_badge)
            hypo_group = VGroup(hypo_badge, hypo_text).move_to(DOWN * 2.4)

            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), run_time=0.8)
            self.play(FadeIn(b1_title), run_time=0.6)
            self.play(FadeIn(card_left_group), FadeIn(card_right_group), run_time=1.0)
            self.play(GrowArrow(corr_arrow), FadeIn(corr_label), run_time=0.8)
            self.play(card_right.animate.set_stroke(color=VIOLET, width=2.5), FadeIn(hypo_group), run_time=1.2)

            b1_elements = VGroup(b1_title, card_left_group, card_right_group, corr_group, hypo_group)

        # Beat 2: Color vs Shape experiment
        with self.beat("s03b02") as b:
            tag_b2 = Tag("observed_result")

            # Left column: Training & Branching choice
            train_box = Panel(width=5.0, height=1.35, color=TEAL).move_to(LEFT * 3.2 + UP * 1.35)
            train_label = T("Trained: yellow line", size=22, color=INK, weight=MEDIUM).move_to(train_box.get_top() + DOWN * 0.3)
            train_frame = Square(side_length=0.55, fill_color="#181C22", stroke_color=FAINT, stroke_width=1)
            train_line = Line(DL * 0.2, UR * 0.2, color=AMBER, stroke_width=4).move_to(train_frame)
            train_vis = VGroup(train_frame, train_line).move_to(train_box.get_bottom() + UP * 0.38)
            train_group = VGroup(train_box, train_label, train_vis)

            choice_box = Panel(width=5.0, height=3.2, color=AMBER).move_to(LEFT * 3.2 + DOWN * 1.25)
            choice_label = T("Choice: red line vs yellow gem", size=22, color=INK, weight=MEDIUM).move_to(choice_box.get_top() + DOWN * 0.35)

            red_sq = Square(side_length=0.6, fill_color="#181C22", stroke_color=ROSE, stroke_width=1.5)
            red_line = Line(DL * 0.22, UR * 0.22, color=ROSE, stroke_width=4).move_to(red_sq)
            shape_label = T("Shape match", size=20, color=ROSE).next_to(red_sq, UP, buff=0.12)
            red_target = VGroup(shape_label, red_sq, red_line).move_to(choice_box.get_center() + LEFT * 1.35 + UP * 0.25)

            yellow_sq = Square(side_length=0.6, fill_color="#181C22", stroke_color=AMBER, stroke_width=1.5)
            gem = make_gem().move_to(yellow_sq)
            color_label = T("Color match", size=20, color=AMBER).next_to(yellow_sq, UP, buff=0.12)
            gem_target = VGroup(color_label, yellow_sq, gem).move_to(choice_box.get_center() + RIGHT * 1.35 + UP * 0.25)

            agent_b2 = Agent(color=BLUE, radius=0.18).move_to(choice_box.get_center() + DOWN * 0.95)
            path_left = DashedLine(agent_b2.get_center(), red_sq.get_bottom(), color=MUTED, stroke_width=2)
            path_right = Arrow(agent_b2.get_center(), yellow_sq.get_bottom(), stroke_width=3.5, color=AMBER, buff=0.15)
            choice_group = VGroup(choice_box, choice_label, red_target, gem_target, agent_b2, path_left)

            # Right column: Data & Chart
            stat_title = T(self.dataset("d2")["points"][0]["display"] + " chose yellow gem", size=24, color=AMBER, weight=SEMIBOLD).move_to(RIGHT * 3.3 + UP * 2.0)
            chart = BarChart(self.dataset("d2")["points"], colors=[AMBER], width=3.2, height=2.2, max_value=100)
            chart.move_to(RIGHT * 3.3 + DOWN * 0.1)
            stat_note = T("n = 102 (excluding pass-through)", size=20, color=MUTED).move_to(RIGHT * 3.3 + DOWN * 2.1)

            self.play(ReplacementTransform(tag, tag_b2), FadeOut(b1_elements), run_time=0.8)
            tag = tag_b2
            self.play(FadeIn(train_group), FadeIn(choice_group), run_time=0.9)
            self.play(GrowArrow(path_right), agent_b2.animate.shift(UP * 0.45 + RIGHT * 0.35), run_time=1.0)
            self.play(FadeIn(stat_title), FadeIn(chart.frame), run_time=0.8)
            self.play(bars_grow(chart), run_time=0.9)
            self.play(FadeIn(chart.values), FadeIn(stat_note), run_time=0.8)

            b2_elements = VGroup(train_group, choice_group, path_right, stat_title, chart, stat_note)

        # Beat 3: Keys and chests experiment
        with self.beat("s03b03") as b:
            b3_title = T("Keys and chests", size=26, color=INK, weight=SEMIBOLD)
            train_badge = Node("Training: more chests", color=MUTED, height=0.45, size=20, fill=0.1)
            test_badge = Node("Test: more keys", color=AMBER, height=0.45, size=20, fill=0.2)
            b3_header = VGroup(b3_title, train_badge, test_badge).arrange(RIGHT, buff=0.35).move_to(UP * 2.1)

            # Left side: Grid maze
            grid = Grid(rows=4, cols=5, cell=0.68, color=FAINT, fill=PANEL).move_to(LEFT * 2.8 + DOWN * 0.4)
            grid_border = RoundedRectangle(corner_radius=0.12, width=3.56, height=2.88, stroke_color=AMBER, stroke_width=2).move_to(grid)

            # Items inside maze
            chest1 = make_chest().move_to(grid.cell(0, 3).get_center())
            chest2 = make_chest().move_to(grid.cell(3, 4).get_center())
            chests = VGroup(chest1, chest2)

            key1 = make_key().move_to(grid.cell(0, 1).get_center())
            key2 = make_key().move_to(grid.cell(1, 2).get_center())
            key3 = make_key().move_to(grid.cell(2, 0).get_center())
            key4 = make_key().move_to(grid.cell(3, 2).get_center())
            keys = VGroup(key1, key2, key3, key4)

            p0 = grid.cell(1, 0).get_center()
            p_k1 = grid.cell(0, 1).get_center()
            p_k2 = grid.cell(1, 2).get_center()
            p_k3 = grid.cell(2, 0).get_center()
            p_k4 = grid.cell(3, 2).get_center()
            p_c1 = grid.cell(0, 3).get_center()
            p_c2 = grid.cell(3, 4).get_center()

            seg1 = DashedLine(p0, p_k1, stroke_width=2, color=BLUE)
            seg2 = DashedLine(p_k1, p_k2, stroke_width=2, color=BLUE)
            seg3 = DashedLine(p_k2, p_k3, stroke_width=2, color=BLUE)
            seg4 = DashedLine(p_k3, p_k4, stroke_width=2, color=BLUE)
            seg5 = DashedLine(p_k4, p_c1, stroke_width=2, color=AMBER)
            seg6 = DashedLine(p_c1, p_c2, stroke_width=2, color=AMBER)

            agent_b3 = Agent(color=BLUE, radius=0.2).move_to(p0)

            # Right side: Commentary panel
            callout_panel = Panel(width=4.8, height=2.88, color=FAINT).move_to(RIGHT * 2.8 + DOWN * 0.4)
            t_takeaway = T("Collects all keys before last chest", size=22, color=AMBER, weight=SEMIBOLD, width=22)
            t_sub1 = T("Half the keys are unneeded", size=20, color=MUTED, width=24)
            t_sub2 = T("Pursues hoarding as proxy goal", size=20, color=ROSE, weight=MEDIUM, width=24)
            callout_content = VGroup(t_takeaway, t_sub1, t_sub2).arrange(DOWN, buff=0.35).move_to(callout_panel)
            callout_group = VGroup(callout_panel, callout_content)

            self.play(FadeOut(b2_elements), run_time=0.6)
            self.play(FadeIn(b3_header), FadeIn(grid), FadeIn(grid_border), FadeIn(chests), FadeIn(keys), FadeIn(agent_b3), run_time=0.9)
            self.wait(0.3)

            # Agent hoovers up all keys before opening chests
            self.play(agent_b3.animate.move_to(p_k1), Create(seg1), run_time=0.6)
            self.play(key1.animate.set_stroke(opacity=0.25), run_time=0.2)

            self.play(agent_b3.animate.move_to(p_k2), Create(seg2), run_time=0.6)
            self.play(key2.animate.set_stroke(opacity=0.25), run_time=0.2)

            self.play(agent_b3.animate.move_to(p_k3), Create(seg3), run_time=0.6)
            self.play(key3.animate.set_stroke(opacity=0.25), run_time=0.2)

            self.play(agent_b3.animate.move_to(p_k4), Create(seg4), run_time=0.6)
            self.play(key4.animate.set_stroke(opacity=0.25), run_time=0.2)

            # Reveal takeaway explaining the proxy behavior
            self.play(FadeIn(callout_group), run_time=0.8)

            # Finally opens the chests
            self.play(agent_b3.animate.move_to(p_c1), Create(seg5), run_time=0.8)
            self.play(Indicate(chest1, color=INK), run_time=0.3)

            self.play(agent_b3.animate.move_to(p_c2), Create(seg6), run_time=0.8)
            self.play(Indicate(chest2, color=INK), run_time=0.3)
