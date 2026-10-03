# storyboard: 5d0b989c0309932d
from aisr_kit import *

class S05(NarratedScene):
    def construct(self):
        with self.beat("s05b01") as b:
            heading = Heading("The design question")
            tag = Tag("author_interpretation")
            source = Source("OMOHUNDRO (2007)")
            board = Grid(4, 4, cell=0.65).move_to(LEFT * 3.5 + UP * 0.35)
            for r in range(4):
                for c in range(4):
                    board.cell(r,c).set_fill(PANEL if (r+c)%2 else FAINT, opacity=0.5)
            board_label = T("Chess task", size=26).next_to(board, UP, buff=0.3)
            machine = Circle(radius=0.23, color=TEAL, stroke_width=4).move_to(board.cell(0,2))
            goal = Node("Goal", color=AMBER, width=2.6).move_to(RIGHT * 3.6 + UP * 0.35)
            outcome = Arrow(board.get_right(), goal.get_left(), color=AMBER, buff=0.2)
            off = Node("Off switch", color=ROSE, width=2.6).move_to(LEFT * 3.5 + DOWN * 2.1)
            wire = Line(board.get_bottom(), off.get_top(), color=ROSE)
            loops = VGroup(CurvedArrow(LEFT * 1.8 + UP * 1.3, LEFT * 1.8 + DOWN * 0.5, angle=-PI, color=TEAL), CurvedArrow(LEFT * 0.9 + DOWN * 0.5, LEFT * 0.9 + UP * 1.3, angle=-PI, color=TEAL))
            incentives = T("Incentives", size=26, color=TEAL).move_to(RIGHT * 0.3 + DOWN * 1.5)
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), Create(board), FadeIn(board_label), FadeIn(machine), run_time=2)
            self.play(FadeIn(goal), GrowArrow(outcome), FadeIn(off), Create(wire), run_time=2)
            self.play(Create(loops), FadeIn(incentives), run_time=3)
            self.play(Indicate(off, color=ROSE), Indicate(goal, color=AMBER), run_time=2)
        with self.beat("s05b02") as b:
            new_tag = Tag("limitation")
            register = Node("Measurement", color=AMBER, width=2.8).move_to(RIGHT * 1 + DOWN * 1.4)
            real_label = T("Real outcome", size=24, color=AMBER).move_to(RIGHT * 0.6 + UP * 1.1)
            proxy_link = Arrow(register.get_right(), goal.get_bottom(), color=AMBER, buff=0.18)
            direct_edit = CurvedArrow(machine.get_center(), register.get_left(), angle=PI/4, color=ORANGE)
            self.play(ReplacementTransform(tag,new_tag), FadeOut(loops), FadeOut(incentives), FadeIn(register), FadeIn(real_label), run_time=2)
            tag = new_tag
            self.play(Transform(outcome,proxy_link), Create(direct_edit), run_time=3)
            self.play(Indicate(register, color=ORANGE), run_time=1.5)
            original_link = Arrow(board.get_right(), goal.get_left(), color=AMBER, buff=0.2)
            self.play(Transform(outcome,original_link), FadeOut(direct_edit), run_time=2)
            # Clear the chess and measurement diagram so the next beat opens on its own visual.
            self.wait(b.duration - 8.5 - 0.8)
            self.play(FadeOut(VGroup(board, board_label, machine, goal, outcome, off, wire, register, real_label)), run_time=0.8)
        with self.beat("s05b03") as b:
            frame = RoundedRectangle(width=11.4, height=4.6, corner_radius=0.2, color=SOFT, stroke_width=2).move_to(DOWN * 0.35)
            conceptual = T("Conceptual argument", size=38, weight=MEDIUM).move_to(UP * 1.35)
            hypothetical = T("Hypothetical examples", size=32, color=INK).move_to(DOWN * 1.95)
            # Example 1: chess machine pursuing a goal.
            mini = Grid(3, 3, cell=0.32)
            for r in range(3):
                for c in range(3):
                    mini.cell(r, c).set_fill(PANEL if (r+c)%2 else FAINT, opacity=0.6)
            mini_agent = Circle(radius=0.12, color=TEAL, stroke_width=4).move_to(mini.cell(0, 1))
            token = RoundedRectangle(width=0.9, height=0.5, corner_radius=0.25, color=AMBER, stroke_width=4).set_fill(AMBER, opacity=0.25)
            chess_ex = VGroup(mini, mini_agent, token)
            token.next_to(mini, RIGHT, buff=0.7)
            chess_link = Arrow(mini.get_right(), token.get_left(), color=AMBER, buff=0.1, stroke_width=4)
            chess_ex.add(chess_link)
            # Example 2: a system and its copies.
            origin = Circle(radius=0.3, color=TEAL, stroke_width=4)
            copies = VGroup(*[Circle(radius=0.22, color=TEAL, stroke_width=3).move_to(RIGHT * 1.2 + UP * y) for y in [0.45, -0.45]])
            copy_links = VGroup(*[Arrow(origin.get_right(), c.get_left(), color=TEAL, buff=0.08, stroke_width=3) for c in copies])
            copy_ex = VGroup(origin, copies, copy_links)
            # Example 3: a system gathering resources.
            gatherer = Circle(radius=0.3, color=TEAL, stroke_width=4).move_to(RIGHT * 1.2)
            stock = VGroup(*[Square(side_length=0.22, color=GRAY, fill_opacity=0.7).move_to(UP * y) for y in [0.45, 0, -0.45]])
            feeds = VGroup(*[Arrow(sq.get_right(), gatherer.get_left(), color=MUTED, buff=0.08, stroke_width=3) for sq in stock])
            resource_ex = VGroup(stock, feeds, gatherer)
            examples = VGroup(chess_ex, copy_ex, resource_ex).arrange(RIGHT, buff=1.3).scale(1.3).move_to(DOWN * 0.3)
            self.add(frame, conceptual)
            self.play(LaggedStart(FadeIn(chess_ex), FadeIn(copy_ex), FadeIn(resource_ex), lag_ratio=0.5), run_time=3)
            self.play(FadeIn(hypothetical), run_time=1.5)
            self.play(Indicate(conceptual, color=INK, scale_factor=1.05), run_time=2)
            self.play(frame.animate.set_stroke(color=INK), run_time=1.5)
        with self.beat("s05b04") as b:
            new_tag = Tag("author_interpretation")
            board = Grid(4, 4, cell=0.6).move_to(LEFT * 4.6 + DOWN * 0.2)
            for r in range(4):
                for c in range(4):
                    board.cell(r, c).set_fill(PANEL if (r+c)%2 else FAINT, opacity=0.5)
            machine = Circle(radius=0.22, color=TEAL, stroke_width=4).move_to(board.cell(1, 2))
            goal = Node("Goal", color=AMBER, width=2.4, height=1.0, size=36).move_to(RIGHT * 4.9 + DOWN * 0.2)
            gate_xs = [-1.3, 1.6]
            boundaries = VGroup(*[DashedLine(RIGHT * x + DOWN * 1.3, RIGHT * x + UP * 0.9, color=AMBER, stroke_width=5) for x in gate_xs])
            consequence = T("Design consequences", size=36, color=AMBER, weight=MEDIUM).move_to(RIGHT * 0.15 + UP * 1.45)
            route = VMobject(color=TEAL, stroke_width=6).set_points_smoothly([board.get_right() + RIGHT * 0.15, LEFT * 1.3 + DOWN * 0.45, RIGHT * 0.15 + DOWN * 0.05, RIGHT * 1.6 + DOWN * 0.45, goal.get_left() + LEFT * 0.15])
            route_label = T("Route to success", size=36, color=TEAL, weight=MEDIUM).move_to(RIGHT * 0.15 + DOWN * 1.95)
            self.play(ReplacementTransform(tag, new_tag), FadeOut(VGroup(frame, conceptual, hypothetical, copy_ex, resource_ex, chess_link)), run_time=0.8)
            self.play(ReplacementTransform(mini, board), ReplacementTransform(mini_agent, machine), ReplacementTransform(token, goal.box), FadeIn(goal.label), run_time=1.2)
            tag = new_tag
            self.play(Create(route), FadeIn(route_label), run_time=3)
            self.play(LaggedStart(*[Create(x) for x in boundaries], lag_ratio=0.4), FadeIn(consequence), run_time=2.5)
            self.play(Indicate(route, color=TEAL), Indicate(boundaries, color=AMBER), run_time=2)
            self.play(Indicate(goal, color=AMBER), run_time=1.5)
