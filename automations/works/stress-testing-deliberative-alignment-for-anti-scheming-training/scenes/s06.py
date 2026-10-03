# storyboard: 79b72ba0f13d1cd9
from aisr_kit import *

def report_tray():
    return VGroup(Line([-0.9, 0.3, 0], [-0.9, -0.3, 0]), Line([-0.9, -0.3, 0], [0.9, -0.3, 0]), Line([0.9, -0.3, 0], [0.9, 0.3, 0])).set_color(SOFT)

def card():
    return VGroup(RoundedRectangle(width=0.6, height=0.8, corner_radius=0.06, color=SOFT), VGroup(*[Line(LEFT * 0.18, RIGHT * 0.18, color=SOFT).shift(UP * y) for y in [0.2, 0, -0.2]]))

class S06(NarratedScene):
    def construct(self):
        with self.beat("s06b01") as b:
            heading = Heading("What a better report can tell you")
            tag = Tag("author_interpretation")
            source = Source("Schoen et al. (2025)")
            tray = report_tray().move_to([4.2, 0.3, 0])
            report = card().move_to([4.2, 0.7, 0])
            files = VGroup(*[card().move_to([-4.8 + i * 0.8, 0.6, 0]) for i in range(3)])
            agent = Agent(color=SAND, radius=0.38).move_to([-0.6, 0.6, 0])
            route = Line([-2.5, 0.6, 0], [3.2, 0.6, 0], color=TEAL)
            hidden = DashedVMobject(VMobject(color=AMBER).set_points_as_corners([[-2.5, 0.6, 0], [-1.8, -0.9, 0], [2.5, -0.9, 0], [3.2, 0.6, 0]]))
            labels = VGroup(T("Your report", size=40).move_to([4.2, 1.8, 0]), T("Behavior", size=40, color=TEAL).move_to([0.3, 1.7, 0]), T("Reason for change", size=40, color=SOFT).move_to([0.3, -1.9, 0]))
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), FadeIn(files), FadeIn(agent), Create(tray), Create(report), FadeIn(labels), run_time=2)
            self.play(Create(route), run_time=2)
            token = Dot([-2.5, 0.6, 0], color=TEAL)
            self.play(FadeIn(token), run_time=0.5)
            self.play(MoveAlongPath(token, route), route.animate.set_stroke(width=5), run_time=3)
            self.play(FadeOut(token), Create(hidden), run_time=2)
            self.play(Indicate(report, color=TEAL), Indicate(labels[2], color=AMBER), run_time=2)
            self.wait(b.duration - 12.2)
            # Clear this beat's diagram so s06b02 opens on its own state.
            self.play(FadeOut(tag, files, agent, route, hidden, tray, report, labels), run_time=0.7)
        with self.beat("s06b02") as b:
            tag = Tag("limitation")
            evidence = RoundedRectangle(width=5.4, height=3.4, corner_radius=0.12, color=SOFT).move_to([-3.4, -0.1, 0])
            coverage = T("Limited coverage", size=44).move_to([-3.4, 2.15, 0])
            tests = VGroup(*[RoundedRectangle(width=1.3, height=0.95, corner_radius=0.08, color=TEAL).move_to([-4.3 + (i % 2) * 1.8, 0.6 - (i // 2) * 1.4, 0]) for i in range(4)])
            tray = report_tray().move_to([3.6, 0.2, 0])
            report = card().move_to([3.6, 0.6, 0])
            deployment = T("Deployment unresolved", size=40).move_to([3.6, 2.15, 0])
            gap = DashedLine([-0.5, 0.4, 0], [1.1, 0.4, 0], color=SOFT, dash_length=0.12)
            resistance = RoundedRectangle(width=4.6, height=1.5, corner_radius=0.1, color=AMBER).move_to([3.6, -1.75, 0])
            resistance_text = T("Training resistance\nuntested", size=36, color=AMBER).move_to([3.6, -1.75, 0])
            self.play(FadeIn(tag), Create(evidence), FadeIn(coverage), run_time=1.5)
            self.play(LaggedStart(*[Create(t) for t in tests], lag_ratio=0.25), run_time=2)
            self.wait(1.5)
            self.play(Create(tray), Create(report), FadeIn(deployment), run_time=1.5)
            self.play(Create(gap), run_time=1.5)
            self.wait(1.5)
            self.play(Create(resistance), FadeIn(resistance_text), run_time=2)
            self.play(Indicate(resistance, color=AMBER), run_time=1.5)
        with self.beat("s06b03") as b:
            proxy = Circle(radius=0.8, color=TEAL).move_to([-3.4, 0.0, 0])
            proxy_text = T("Proxy", size=40, color=TEAL).move_to([-3.4, 0.0, 0])
            action_label = T("Covert actions", size=40).move_to([-3.4, 1.7, 0])
            region = RoundedRectangle(width=5.2, height=3.8, corner_radius=0.2, color=AMBER).move_to([3.0, -0.1, 0])
            future = T("Future scheming", size=40, color=AMBER).move_to([3.0, 0.0, 0])
            self.play(FadeOut(tests, report, coverage, deployment, gap, resistance_text, resistance), run_time=1)
            self.play(ReplacementTransform(tray, proxy), ReplacementTransform(evidence, region), run_time=3)
            self.play(FadeIn(proxy_text), FadeIn(action_label), FadeIn(future), run_time=2)
            self.play(Indicate(proxy, color=TEAL), run_time=2)
            self.play(region.animate.set_stroke(width=3), run_time=2)
            self.wait(b.duration - 10.7)
            # Clear this beat's diagram and tag so s06b04 opens on its own state.
            self.play(FadeOut(tag, proxy, proxy_text, action_label, region, future), run_time=0.7)
        with self.beat("s06b04") as b:
            tag = Tag("author_interpretation")
            bars = VGroup()
            tips = VGroup()
            for dataset_id, x in [("d1", -4.6), ("d2", -1.6)]:
                data = self.dataset(dataset_id)
                before, after = data["points"]
                scale = 2.8 / self.dataset("d2")["points"][0]["value"]
                for point, offset, color in [(before, 0, AMBER), (after, 0.9, TEAL)]:
                    height = point["value"] * scale
                    bar = Rectangle(width=0.55, height=height, color=color, fill_color=color, fill_opacity=0.8).move_to([x + offset, -1.2 + height / 2, 0])
                    bars.add(bar)
                    if color == TEAL:
                        tips.add(Circle(radius=0.22, color=TEAL).move_to([x + offset, -1.2 + height, 0]))
            baseline = Line([-5.3, -1.2, 0], [0.0, -1.2, 0], color=SOFT)
            reduced = T("Reduced covert actions", size=40).move_to([-2.75, 2.15, 0])
            residual = T("Residual failures", size=40, color=TEAL).move_to([-2.65, -2.0, 0])
            final_tray = report_tray().scale(0.85).move_to([1.3, 1.2, 0])
            final_report = card().move_to([1.3, 1.55, 0])
            takeaway = T("Understand the\nimprovement", size=36).next_to(final_tray, RIGHT, buff=0.35).align_to(final_tray, DOWN).shift(UP * 0.05)
            observer = Circle(radius=0.4, color=SOFT).move_to([1.3, -0.45, 0])
            observer_text = T("Test recognition?", size=36, color=SOFT).next_to(observer, RIGHT, buff=0.45)
            loop = Arc(radius=0.42, start_angle=PI / 4, angle=PI * 1.6, color=TEAL).move_to([1.3, -1.85, 0])
            loop_text = T("Later training?", size=36, color=SOFT).next_to(loop, RIGHT, buff=0.45)
            observer_text.align_to(takeaway, LEFT)
            loop_text.align_to(takeaway, LEFT)
            self.play(FadeIn(tag), Create(baseline), FadeIn(reduced), run_time=1)
            self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.25), run_time=3)
            self.play(Create(tips), FadeIn(residual), run_time=2)
            self.wait(1.5)
            self.play(Create(final_tray), Create(final_report), FadeIn(takeaway), run_time=1.5)
            self.wait(1)
            self.play(Create(observer), FadeIn(observer_text), run_time=1.5)
            self.wait(0.5)
            self.play(Create(loop), FadeIn(loop_text), run_time=2)
            self.play(Indicate(final_report, color=TEAL), run_time=1.5)
