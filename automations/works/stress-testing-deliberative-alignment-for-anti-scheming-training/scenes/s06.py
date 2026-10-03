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
            labels = VGroup(T("Your report", size=28).move_to([4.2, 1.8, 0]), T("Behavior", size=28, color=TEAL).move_to([0.3, 1.7, 0]), T("Reason for change", size=28, color=SOFT).move_to([0.3, -1.9, 0]))
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), FadeIn(files), FadeIn(agent), Create(tray), Create(report), FadeIn(labels), run_time=2)
            self.play(Create(route), run_time=2)
            token = Dot([-2.5, 0.6, 0], color=TEAL)
            self.play(FadeIn(token), run_time=0.5)
            self.play(MoveAlongPath(token, route), route.animate.set_stroke(width=5), run_time=3)
            self.play(FadeOut(token), Create(hidden), run_time=2)
            self.play(Indicate(report, color=TEAL), Indicate(labels[2], color=AMBER), run_time=2)
        with self.beat("s06b02") as b:
            next_tag = Tag("limitation")
            evidence = RoundedRectangle(width=5.1, height=3.2, corner_radius=0.12, color=SOFT).move_to([-3.5, 0.2, 0])
            coverage = T("Limited coverage", size=28).move_to([-3.5, 2.2, 0])
            deployment = T("Deployment unresolved", size=26, width=20).move_to([3.5, 2.1, 0])
            resistance = RoundedRectangle(width=4.4, height=1.0, corner_radius=0.1, color=AMBER).move_to([3.6, -1.8, 0])
            resistance_text = T("Training resistance untested", size=24, width=23).move_to([3.6, -1.8, 0])
            self.play(ReplacementTransform(tag, next_tag), FadeOut(labels), FadeOut(route), FadeOut(hidden), run_time=1)
            self.play(Create(evidence), FadeIn(coverage), files.animate.scale(0.75).move_to([-4.5, 0.3, 0]), agent.animate.move_to([-2.1, 0.3, 0]), run_time=2)
            self.play(tray.animate.move_to([3.5, 0.1, 0]), report.animate.move_to([3.5, 0.5, 0]), FadeIn(deployment), run_time=2)
            self.play(Create(resistance), FadeIn(resistance_text), run_time=2)
            self.play(Indicate(evidence, color=SOFT), Indicate(resistance, color=AMBER), run_time=2)
            tag = next_tag
        with self.beat("s06b03") as b:
            proxy = Circle(radius=0.7, color=TEAL).move_to([-3.5, 0.3, 0])
            proxy_text = T("Proxy", size=28, color=TEAL).move_to([-3.5, 0.3, 0])
            action_label = T("Covert actions", size=28).move_to([-3.5, 1.9, 0])
            region = RoundedRectangle(width=5.2, height=3.8, corner_radius=0.2, color=AMBER).move_to([3.0, 0.1, 0])
            future = T("Future scheming", size=28, color=AMBER).move_to([3.0, 0.4, 0])
            self.play(FadeOut(files), FadeOut(agent), FadeOut(report), FadeOut(coverage), FadeOut(deployment), FadeOut(resistance_text), FadeOut(resistance), run_time=1)
            self.play(ReplacementTransform(tray, proxy), ReplacementTransform(evidence, region), run_time=3)
            self.play(FadeIn(proxy_text), FadeIn(action_label), FadeIn(future), run_time=2)
            self.play(Indicate(proxy, color=TEAL), run_time=2)
            self.play(region.animate.set_stroke(width=3), run_time=2)
        with self.beat("s06b04") as b:
            next_tag = Tag("author_interpretation")
            self.play(ReplacementTransform(tag, next_tag), FadeOut(proxy), FadeOut(proxy_text), FadeOut(action_label), FadeOut(region), FadeOut(future), run_time=1)
            bars = VGroup()
            tips = VGroup()
            for dataset_id, x in [("d1", -4.5), ("d2", -1.4)]:
                data = self.dataset(dataset_id)
                before, after = data["points"]
                scale = 2.8 / self.dataset("d2")["points"][0]["value"]
                for point, offset, color in [(before, 0, AMBER), (after, 0.9, TEAL)]:
                    height = point["value"] * scale
                    bar = Rectangle(width=0.55, height=height, color=color, fill_color=color, fill_opacity=0.8).move_to([x + offset, -1.2 + height / 2, 0])
                    bars.add(bar)
                    if color == TEAL:
                        tips.add(Circle(radius=0.22, color=TEAL).move_to([x + offset, -1.2 + height, 0]))
            baseline = Line([-5.2, -1.2, 0], [0.2, -1.2, 0], color=SOFT)
            reduced = T("Reduced covert actions", size=28).move_to([-2.8, 2.2, 0])
            residual = T("Residual failures", size=26, color=TEAL).move_to([-2.8, -2.1, 0])
            final_tray = report_tray().move_to([4.1, -0.1, 0])
            final_report = card().move_to([4.1, 0.3, 0])
            observer = Circle(radius=0.45, color=SOFT).move_to([2.5, 1.3, 0])
            loop = Arc(radius=0.65, start_angle=PI / 4, angle=PI * 1.6, color=TEAL).move_to([4.9, 1.2, 0])
            takeaway = T("Understand the improvement", size=26, width=23).move_to([3.8, -2.1, 0])
            self.play(Create(baseline), FadeIn(reduced), Create(final_tray), Create(final_report), run_time=1)
            self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.25), run_time=3)
            self.play(Create(tips), FadeIn(residual), run_time=2)
            self.play(Create(observer), run_time=1)
            self.play(Indicate(observer, color=SOFT), run_time=1)
            self.play(Create(loop), run_time=2)
            self.play(FadeIn(takeaway), Indicate(final_report, color=TEAL), run_time=2)
