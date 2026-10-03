# storyboard: ce92c542453d19d6
from aisr_kit import *

def file_card(color=SOFT):
    card = RoundedRectangle(width=0.65, height=0.9, corner_radius=0.06, color=color)
    lines = VGroup(*[Line(LEFT * 0.2, RIGHT * 0.2, color=color).shift(UP * y) for y in [0.2, 0, -0.2]])
    return VGroup(card, lines)

class S01(NarratedScene):
    def construct(self):
        with self.beat("s01b01") as b:
            heading = Heading("A report you rely on")
            tag = Tag("future_scenario")
            source = Source("Schoen et al. (2025)")
            files_label = T("Files").move_to([-4.8, 1.7, 0])
            report_label = T("Report").move_to([4.4, 1.7, 0])
            agent = Agent(color=SAND, radius=0.45).move_to([0, 0.3, 0])
            tray = VGroup(Line([-0.9, 0.3, 0], [-0.9, -0.3, 0]), Line([-0.9, -0.3, 0], [0.9, -0.3, 0]), Line([0.9, -0.3, 0], [0.9, 0.3, 0])).set_color(SOFT).move_to([4.4, 0.1, 0])
            cards = VGroup(*[file_card().move_to([-5.1 + i * 0.8, 0.3, 0]) for i in range(3)])
            route = Arrow([-2.7, 0.3, 0], [3.4, 0.3, 0], color=TEAL, buff=0.1)
            check = T("Required check", size=26, color=AMBER).move_to([-3.9, -1.6, 0])
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), FadeIn(files_label), FadeIn(report_label), Create(tray), FadeIn(agent), run_time=1)
            self.play(LaggedStart(*[Create(c) for c in cards], lag_ratio=0.2), GrowArrow(route), run_time=2)
            self.play(cards[2].animate.move_to([4.0, 0.5, 0]), run_time=3)
            self.play(cards[1].animate.move_to([4.8, 0.5, 0]), cards[0].animate.move_to([-3.9, -0.7, 0]), FadeIn(check), run_time=3)
        with self.beat("s01b02") as b:
            self.play(FadeOut(files_label), FadeOut(check), FadeOut(cards[0]), FadeOut(report_label), FadeOut(cards[1:]), run_time=1)
            transparent = T("Transparent route", size=26, color=TEAL).move_to([0, 1.9, 0])
            concealed = T("Concealed route", size=26, color=AMBER).move_to([0, -1.9, 0])
            hidden_route = VMobject(color=AMBER).set_points_as_corners([[-2.7, 0.3, 0], [-1.7, -1.1, 0], [1.8, -1.1, 0], [3.4, 0.3, 0]])
            reports = VGroup(*[RoundedRectangle(width=0.65, height=0.9, corner_radius=0.06, color=SOFT).move_to([4.4, y, 0]) for y in [1.1, -1.2]])
            self.play(Create(hidden_route), FadeIn(transparent), FadeIn(concealed), run_time=3)
            self.play(Create(reports[0]), Create(reports[1]), run_time=2)
            token = Dot([-2.7, 0.3, 0], color=AMBER)
            self.play(FadeIn(token), run_time=0.5)
            self.play(MoveAlongPath(token, hidden_route), run_time=3)
            self.play(FadeOut(token), run_time=0.5)
        with self.beat("s01b03") as b:
            tag_next = Tag("author_interpretation")
            goal = Square(side_length=0.7, color=AMBER).rotate(PI / 4).move_to([1.7, -1, 0])
            scheming = T("Scheming", color=AMBER).move_to([1.7, -2, 0])
            visible = T("Visible behavior", size=26).move_to([4.4, 2, 0])
            oversight = RoundedRectangle(width=3.3, height=3.5, corner_radius=0.1, color=SOFT).move_to([4.4, -0.1, 0])
            self.play(ReplacementTransform(tag, tag_next), FadeOut(transparent), FadeOut(concealed), FadeOut(route), run_time=1)
            self.play(ReplacementTransform(hidden_route, goal), FadeIn(scheming), Create(oversight), FadeIn(visible), run_time=2)
            self.play(agent.animate.move_to([0.8, -1, 0]), run_time=3)
            self.play(Indicate(reports, color=SOFT), run_time=2)
            tag = tag_next
        with self.beat("s01b04") as b:
            next_tag = Tag("method")
            evaluation = RoundedRectangle(width=11.7, height=4.6, corner_radius=0.15, color=SOFT).move_to([0, 0, 0])
            eval_label = T("Constructed evaluations", size=26, color=SOFT).move_to([0, -2.7, 0])
            rules = Node("Safety rules", color=TEAL, width=2.4).move_to([-3.6, 0.3, 0])
            covert = T("Covert actions", size=26, color=AMBER).move_to([1.7, -2, 0])
            self.play(ReplacementTransform(tag, next_tag), FadeOut(oversight), FadeOut(visible), ReplacementTransform(scheming, covert), FadeOut(goal), run_time=1)
            self.play(Create(evaluation), FadeIn(eval_label), agent.animate.move_to([0, 0.3, 0]), run_time=2)
            self.play(FadeIn(rules), run_time=1)
            self.play(rules.animate.move_to([-1.7, 0.3, 0]), run_time=3)
            output = Arrow([0.7, 0.3, 0], [3.4, 0.3, 0], color=TEAL)
            self.play(GrowArrow(output), Indicate(reports, color=TEAL), run_time=2)
            tag = next_tag
        with self.beat("s01b05") as b:
            self.play(FadeOut(rules), FadeOut(covert), FadeOut(reports), FadeOut(tray), FadeOut(output), run_time=1)
            models = VGroup(Node("o3", color=SAND, width=1.8).move_to([-1, 1, 0]), Node("o4-mini", color=SAND, width=1.8).move_to([-1, -1, 0]))
            training = Node("Anti-scheming training", color=TEAL, width=4, size=26).move_to([-3.7, 0, 0])
            tests_label = T("New tests", size=26).move_to([3.7, 1.9, 0])
            tests = VGroup(*[RoundedRectangle(width=1.15, height=0.9, corner_radius=0.08, color=SOFT).move_to([3 + (i % 2) * 1.5, 0.7 - (i // 2) * 1.5, 0]) for i in range(4)])
            self.play(ReplacementTransform(agent, models), FadeIn(training), run_time=2)
            links = VGroup(*[Arrow([-1.7, 0, 0], [-1.7, y, 0], color=TEAL, buff=0.1) for y in [0.7, -0.7]])
            self.play(LaggedStart(*[GrowArrow(link) for link in links], lag_ratio=0.3), run_time=2)
            self.play(FadeIn(tests_label), LaggedStart(*[Create(test) for test in tests], lag_ratio=0.3), run_time=3)
            connections = VGroup(Arrow([0, 1, 0], [2.3, 0.7, 0], color=SOFT), Arrow([0, -1, 0], [2.3, -0.8, 0], color=SOFT))
            self.play(*[GrowArrow(link) for link in connections], run_time=2)
