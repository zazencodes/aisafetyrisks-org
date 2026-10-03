# storyboard: 8f2128c47ea33d0b
from aisr_kit import *

class S05(NarratedScene):
    def construct(self):
        with self.beat("s05b01") as b:
            heading = Heading("Back to the inbox")
            tag = Tag("future_scenario")
            source = Source("Meinke et al. (2024)")
            inbox_label = T("Hypothetical inbox", size=26, color=SOFT).move_to([-4.3, 2.35, 0])
            # The same email pipeline as "How a ranking gets changed".
            nodes = VGroup(*[Node(label, color=TEAL, width=2.2, size=25) for label in ["Emails", "Input data", "Scoring code", "Scores"]]).arrange(RIGHT, buff=0.4).move_to([0, 0.6, 0])
            emails, tray, code, final = nodes
            links = VGroup(*[Link(nodes[i], nodes[i + 1], color=TEAL, buff=0.08) for i in range(3)])
            agent = Agent(color=SAND).move_to([tray.get_x(), 1.75, 0])
            agent_label = T("Agent", size=26, color=SOFT).next_to(agent, LEFT, buff=0.25)
            conflict = Square(side_length=0.38, color=AMBER, fill_opacity=0.3).rotate(PI / 4).move_to([tray.get_x() - 0.7, -1.0, 0])
            conflict_label = T("Conflicting goal", size=26, color=AMBER).next_to(conflict, DOWN, buff=0.2)
            branch = Arrow(conflict.get_top(), tray.get_bottom(), color=AMBER, buff=0.12)
            inspect = SurroundingRectangle(final, color=SAND, buff=0.15)
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), FadeIn(inbox_label), run_time=0.8)
            self.play(FadeIn(nodes), FadeIn(agent), FadeIn(agent_label), run_time=1.2)
            self.play(*[GrowArrow(l.arrow) for l in links], run_time=1.4)
            self.play(Create(conflict), FadeIn(conflict_label), GrowArrow(branch), run_time=1.4)
            self.play(Create(inspect), run_time=1)
            self.play(Transform(inspect, SurroundingRectangle(code, color=SAND, buff=0.15)), run_time=1.4)
            self.play(Transform(inspect, SurroundingRectangle(VGroup(tray, branch, conflict), color=AMBER, buff=0.15)), run_time=1.6)
        with self.beat("s05b02") as b:
            next_tag = Tag("author_interpretation")
            monitor = Panel(3.3, 0.85).move_to([2.4, 1.75, 0])
            monitor_label = T("Reasoning monitor", size=24).move_to(monitor)
            recommendation = T("Authors’ recommendations", size=25, color=SOFT).next_to(monitor, UP, buff=0.25)
            trail = Line(agent.get_right() + RIGHT * 0.1, monitor.get_left(), color=SAND)
            argument = Node("Safety argument", color=SAND, width=3.2, height=0.9).move_to([3.0, -1.5, 0])
            self.play(FadeOut(tag), FadeOut(inspect), run_time=0.4)
            self.play(FadeIn(next_tag), FadeIn(recommendation), run_time=0.6)
            tag = next_tag
            self.play(Create(trail), Create(monitor), run_time=2)
            self.play(FadeIn(monitor_label), run_time=1)
            self.play(Create(argument.box), FadeIn(argument.label), run_time=2)
            self.play(Indicate(monitor, color=SAND), Indicate(argument.box, color=SAND), run_time=1.5)
        # Clear recommendations before the next beat so a portrait cut opens cleanly.
        self.remove(recommendation, inbox_label, trail, monitor, monitor_label, argument, argument.box, argument.label)
        scene_parts = VGroup(nodes, links, agent, agent_label, conflict, conflict_label, branch)
        with self.beat("s05b03") as b:
            next_tag = Tag("limitation")
            self.remove(tag)
            self.add(next_tag)
            tag = next_tag
            # Make room on the right for the deployment side of the boundary.
            self.play(scene_parts.animate.shift(LEFT * 1.25), run_time=1)
            human = Square(side_length=0.38, color=TEAL, fill_opacity=0.3).move_to([code.get_x(), -1.0, 0])
            human_label = T("Human goal", size=26, color=TEAL).next_to(human, DOWN, buff=0.2)
            human_link = Arrow(human.get_top(), code.get_bottom(), color=TEAL, buff=0.12)
            memo = Node("Situation memo", color=SAND, height=0.7, size=26).move_to([emails.get_x() + 0.75, -2.3, 0])
            memo_link = Arrow([emails.get_x(), memo.get_top()[1], 0], emails.get_bottom(), color=SAND, buff=0.12)
            frame = RoundedRectangle(width=13.2, height=5.6, corner_radius=0.16, color=SAND).move_to([0, -0.25, 0])
            target_frame = RoundedRectangle(width=10.35, height=5.15, corner_radius=0.16, color=SAND).move_to([-1.25, -0.3, 0])
            evidence_label = T("Constructed evidence", size=30).next_to(target_frame, UP, buff=0.15)
            boundary = DashedLine([4.1, -2.85, 0], [4.1, 2.3, 0], color=SOFT)
            deployment_label = T("Deployment remains open", size=28, color=INK, width=10).move_to([5.3, 0.6, 0])
            self.play(Create(frame), run_time=1.3)
            self.play(Transform(frame, target_frame), Create(boundary), FadeIn(evidence_label), FadeIn(deployment_label), run_time=2)
            self.play(Create(human), FadeIn(human_label), FadeIn(memo), run_time=1.2)
            self.play(GrowArrow(human_link), GrowArrow(memo_link), run_time=1.5)
        with self.beat("s05b04") as b:
            next_tag = Tag("author_interpretation")
            # Clear the limitation state completely before the takeaway appears.
            self.play(FadeOut(tag), FadeOut(evidence_label), FadeOut(deployment_label), FadeOut(boundary), FadeOut(frame), run_time=0.6)
            tag = next_tag
            everything = VGroup(scene_parts, human, human_label, human_link, memo, memo_link)
            self.play(everything.animate.shift(RIGHT * 1.25), run_time=0.8)
            takeaway = T("Trace the process", size=30).move_to([1.5, 2.45, 0])
            self.play(FadeIn(tag), FadeIn(takeaway), run_time=0.6)
            tracer = Dot(emails.get_left(), radius=0.09, color=TEAL)
            self.play(FadeIn(tracer), run_time=0.4)
            self.play(tracer.animate.move_to(tray.get_center()), run_time=1.5)
            self.play(Indicate(branch, color=AMBER), Indicate(conflict, color=AMBER), run_time=1.5)
            self.play(tracer.animate.move_to(code.get_center()), run_time=1.6)
            self.play(tracer.animate.move_to(final.get_center()), run_time=1.6)
            self.play(Indicate(human, color=TEAL), Indicate(human_link, color=TEAL), run_time=1.3)
            self.play(Indicate(conflict, color=AMBER), Indicate(branch, color=AMBER), run_time=1.3)
            self.play(FadeOut(tracer), run_time=0.5)
