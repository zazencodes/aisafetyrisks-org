# storyboard: 0d62a57b3d460d19
from aisr_kit import *


def goal_token(icon):
    capsule = RoundedRectangle(width=1.3, height=0.8, corner_radius=0.4, color=AMBER, stroke_width=4)
    capsule.set_fill(AMBER, opacity=0.18)
    icon.move_to(capsule)
    return VGroup(capsule, icon)


class S01(NarratedScene):
    def construct(self):
        with self.beat("s01b01") as b:
            heading = Heading("A harmless task?")
            tag = Tag("threat_model")
            source = Source("OMOHUNDRO (2007)")
            board = Grid(4, 4, cell=0.65).move_to(LEFT * 3.5 + UP * 0.35)
            for r in range(4):
                for c in range(4):
                    board.cell(r, c).set_fill(PANEL if (r+c)%2 else FAINT, opacity=0.5)
            chess = T("Chess", size=32, weight=MEDIUM).next_to(board, UP, buff=0.3)
            agent = Circle(radius=0.23, color=TEAL, stroke_width=4).move_to(board.cell(3, 0))
            goal = Node("Win games", color=AMBER, width=3.0, size=32).move_to(RIGHT * 3.6 + UP * 0.35)
            path = VMobject(color=AMBER, stroke_width=3).set_points_as_corners([board.cell(3,0).get_center(), board.cell(2,0).get_center(), board.cell(2,2).get_center(), board.cell(0,2).get_center()])
            outcome = Arrow(board.get_right(), goal.get_left(), color=AMBER, buff=0.2)
            off = Node("Off switch", color=ROSE, width=3.0, size=32).move_to(LEFT * 3.5 + DOWN * 2.1)
            wire = Line(board.get_bottom(), off.get_top(), color=ROSE)
            self.add(heading, tag, source, board, chess, agent)
            self.play(Create(path), MoveAlongPath(agent, path), run_time=3)
            self.play(GrowArrow(outcome), FadeIn(goal), run_time=2)
            self.play(Create(wire), FadeIn(off), run_time=2)
        with self.beat("s01b02") as b:
            copy = Circle(radius=0.3, color=TEAL, stroke_width=4).move_to(LEFT * 0.7 + UP * 1.75)
            copy_label = T("Copy", size=28).next_to(copy, UP, buff=0.2)
            resources = VGroup(*[Square(side_length=0.35, color=AMBER, fill_opacity=0.2).shift(RIGHT * i * 0.5) for i in range(3)]).move_to(RIGHT * 1 + DOWN * 1.2)
            resources_label = T("Resources", size=28).next_to(resources, DOWN, buff=0.25)
            branch_copy = Arrow(agent.get_center(), copy.get_center(), color=TEAL, buff=0.3)
            branch_resources = Arrow(agent.get_center(), resources.get_center(), color=AMBER, buff=0.3)
            barrier = Line(LEFT * 4 + DOWN * 1.3, LEFT * 3 + DOWN * 1.3, color=ROSE, stroke_width=8)
            resist = T("Shutdown resistance", size=28, color=ROSE).move_to(LEFT * 3.5 + DOWN * 2.95)
            self.play(GrowArrow(branch_copy), TransformFromCopy(agent, copy), FadeIn(copy_label), run_time=3)
            self.play(GrowArrow(branch_resources), LaggedStart(*[Create(s) for s in resources], lag_ratio=0.3), FadeIn(resources_label), run_time=3)
            self.play(Create(barrier), FadeIn(resist), run_time=2)
        with self.beat("s01b03") as b:
            new_tag = Tag("definition")
            system = Circle(radius=0.6, color=TEAL, stroke_width=4).move_to(LEFT * 3.5 + UP * 0.35)
            system_label = T("Goal-directed system", size=26).move_to(LEFT * 3.5 + DOWN * 0.65)
            boundary = RoundedRectangle(width=4, height=3, corner_radius=0.3, color=TEAL).move_to(LEFT * 3.5)
            drive_top = Arrow(LEFT * 1.3 + UP * 1.2, RIGHT * 2.1 + UP * 0.55, color=AMBER, buff=0.1)
            drive_bottom = Arrow(LEFT * 1.3 + DOWN * 0.7, RIGHT * 2.1 + UP * 0.1, color=AMBER, buff=0.1)
            drive_label = T("Drive", size=26, color=AMBER).move_to(RIGHT * 0.1 + UP * 1.6)
            gate = Line(RIGHT * 0.3 + DOWN * 0.9, RIGHT * 0.3 + DOWN * 0.1, color=AMBER, stroke_width=8)
            counter = T("Counteract", size=24, color=AMBER).move_to(RIGHT * 0.3 + DOWN * 1.35)
            self.play(ReplacementTransform(tag, new_tag), FadeOut(VGroup(board,chess,path,wire,off,barrier,resist,copy_label,resources_label,resources)), Transform(agent, system), FadeOut(copy), run_time=2)
            tag = new_tag
            self.play(Transform(branch_copy, drive_top), Transform(branch_resources, drive_bottom), FadeOut(outcome), Create(boundary), FadeIn(system_label), FadeIn(drive_label), run_time=3)
            self.play(Create(gate), FadeIn(counter), run_time=2)
            self.play(Indicate(gate, color=AMBER), run_time=1.5)
            # Clear the definition diagram so the next beat opens on its own visual.
            self.wait(b.duration - 8.5 - 0.8)
            self.play(FadeOut(VGroup(tag, agent, boundary, system_label, branch_copy, branch_resources, drive_label, gate, counter, goal)), run_time=0.8)
        with self.beat("s01b04") as b:
            tag = Tag("method")
            paper_title = Serif("The Basic AI Drives", size=46).move_to(UP * 1.75)
            ys = [0.45, -0.75, -1.95]
            systems = VGroup(*[Circle(radius=0.3, color=TEAL, stroke_width=4).move_to(LEFT * 4.6 + UP * y) for y in ys])
            chess_icon = Grid(3, 3, cell=0.18)
            for r in range(3):
                for c in range(3):
                    chess_icon.cell(r, c).set_fill(AMBER if (r+c)%2 else BG, opacity=0.9)
            icons = [chess_icon, Star(n=5, outer_radius=0.24, color=AMBER, fill_opacity=0.9), Triangle(color=AMBER, fill_opacity=0.9).scale(0.22)]
            goals = VGroup(*[goal_token(icon).move_to(RIGHT * 4.5 + UP * y) for icon, y in zip(icons, ys)])
            different = T("Different goals", size=34, color=AMBER, weight=MEDIUM).move_to(RIGHT * 4.5 + DOWN * 2.85)
            means = Node("Shared means", color=TEAL, width=3.4, height=1.1, size=34).move_to(DOWN * 0.75)
            inputs = VGroup(*[Arrow(s.get_right(), means.get_left(), color=TEAL, buff=0.15, stroke_width=4) for s in systems])
            outputs = VGroup(*[Arrow(means.get_right(), g.get_left(), color=AMBER, buff=0.15, stroke_width=4) for g in goals])
            self.add(tag, paper_title)
            self.play(LaggedStart(*[FadeIn(s) for s in systems], lag_ratio=0.3), LaggedStart(*[FadeIn(g) for g in goals], lag_ratio=0.3), run_time=1.5)
            self.play(FadeIn(different), run_time=1)
            self.play(LaggedStart(*[GrowArrow(a) for a in inputs], lag_ratio=0.2), FadeIn(means), run_time=2.5)
            self.play(LaggedStart(*[GrowArrow(a) for a in outputs], lag_ratio=0.2), run_time=2)
            self.play(Indicate(means, color=TEAL), run_time=1.5)
            self.play(Indicate(goals[0], color=AMBER), Indicate(systems[0], color=TEAL), run_time=1.5)
        with self.beat("s01b05") as b:
            new_tag = Tag("author_interpretation")
            current = Circle(radius=0.6, color=TEAL, stroke_width=4).move_to(LEFT * 3.5 + UP * 0.35)
            future = Circle(radius=0.6, color=TEAL, stroke_width=4).move_to(RIGHT * 0.7 + UP * 0.35)
            current_label = T("Current system", size=28).move_to(LEFT * 3.5 + DOWN * 0.65)
            future_label = T("Future system", size=28).move_to(RIGHT * 0.7 + DOWN * 0.65)
            new_goal = Node("Goal", color=AMBER, width=2.6, size=30).move_to(RIGHT * 4.4 + UP * 0.35)
            future_path = Arrow(current.get_right(), future.get_left(), color=AMBER, buff=0.2)
            final_path = Arrow(future.get_right(), new_goal.get_left(), color=AMBER, buff=0.2)
            self.play(ReplacementTransform(tag, new_tag), FadeOut(VGroup(paper_title, means, different, inputs, outputs, systems[1:], goals[1:])),
                      ReplacementTransform(systems[0], current), ReplacementTransform(goals[0], new_goal), FadeIn(current_label), run_time=2)
            tag = new_tag
            self.play(TransformFromCopy(current, future), FadeIn(future_label), GrowArrow(future_path), GrowArrow(final_path), run_time=3)
            self.play(Indicate(future, color=TEAL), Indicate(final_path, color=AMBER), run_time=2)
