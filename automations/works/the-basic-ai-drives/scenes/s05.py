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
        with self.beat("s05b03") as b:
            new_tag = Tag("limitation")
            diagram = VGroup(board,board_label,machine,goal,outcome,off,wire,register,real_label)
            self.play(ReplacementTransform(tag,new_tag), diagram.animate.scale(0.84).shift(DOWN * 0.3), run_time=2)
            tag = new_tag
            frame = RoundedRectangle(width=11.7, height=4.95, corner_radius=0.15, color=FAINT).move_to(DOWN * 0.1)
            conceptual = T("Conceptual argument", size=28).move_to(UP * 2.45)
            hypothetical = T("Hypothetical examples", size=24, color=SOFT).move_to(DOWN * 2.8)
            ring = Arc(radius=0.58, start_angle=0.25, angle=TAU-0.5, color=TEAL).move_to(register.get_center())
            ring.stretch_to_fit_width(register.width + 0.3).stretch_to_fit_height(register.height + 0.3)
            self.play(Create(frame), FadeIn(conceptual), FadeIn(hypothetical), run_time=3)
            self.play(Create(ring), run_time=2)
        with self.beat("s05b04") as b:
            new_tag = Tag("author_interpretation")
            route = VMobject(color=TEAL, stroke_width=4).set_points_as_corners([board.get_right(), LEFT * 0.8 + DOWN * 0.4, RIGHT * 1.1 + DOWN * 0.4, goal.get_left()])
            boundary_a = DashedLine(LEFT * 0.8 + DOWN * 1.1, LEFT * 0.8 + UP * 0.8, color=TEAL)
            boundary_b = DashedLine(RIGHT * 1.1 + DOWN * 1.1, RIGHT * 1.1 + UP * 0.8, color=TEAL)
            boundary_labels = VGroup(T("Goal design", size=20, color=TEAL).move_to(LEFT * 0.8 + UP * 1), T("External costs", size=20, color=TEAL).move_to(RIGHT * 1.3 + UP * 1))
            consequence = T("Design consequences", size=26, color=TEAL).move_to(UP * 1.55)
            route_label = T("Route to success", size=24, color=TEAL).move_to(RIGHT * 0.1 + DOWN * 1.55)
            self.play(ReplacementTransform(tag,new_tag), FadeOut(VGroup(frame,conceptual,hypothetical,ring,register,real_label)), FadeOut(outcome), run_time=2)
            tag = new_tag
            self.play(Create(boundary_a), Create(boundary_b), FadeIn(consequence), FadeIn(boundary_labels), run_time=2)
            self.play(Create(route), FadeIn(route_label), run_time=3)
            self.play(Indicate(goal, color=AMBER), Indicate(off, color=ROSE), run_time=2)
