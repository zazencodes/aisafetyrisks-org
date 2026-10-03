# storyboard: 0a2543fb713e16fd
from aisr_kit import *

class S01(NarratedScene):
    def construct(self):
        with self.beat("s01b01") as b:
            heading = Heading("A harmless task?")
            tag = Tag("future_scenario")
            source = Source("OMOHUNDRO (2007)")
            board = Grid(4, 4, cell=0.65).move_to(LEFT * 3.5 + UP * 0.35)
            for r in range(4):
                for c in range(4):
                    board.cell(r, c).set_fill(PANEL if (r+c)%2 else FAINT, opacity=0.5)
            chess = T("Chess", size=26).next_to(board, UP, buff=0.3)
            agent = Circle(radius=0.23, color=TEAL, stroke_width=4).move_to(board.cell(3, 0))
            goal = Node("Win games", color=AMBER, width=2.6).move_to(RIGHT * 3.6 + UP * 0.35)
            path = VMobject(color=AMBER, stroke_width=3).set_points_as_corners([board.cell(3,0).get_center(), board.cell(2,0).get_center(), board.cell(2,2).get_center(), board.cell(0,2).get_center()])
            outcome = Arrow(board.get_right(), goal.get_left(), color=AMBER, buff=0.2)
            off = Node("Off switch", color=ROSE, width=2.6).move_to(LEFT * 3.5 + DOWN * 2.1)
            wire = Line(board.get_bottom(), off.get_top(), color=ROSE)
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), Create(board), FadeIn(chess), FadeIn(agent), run_time=2)
            self.play(Create(path), MoveAlongPath(agent, path), run_time=3)
            self.play(GrowArrow(outcome), FadeIn(goal), run_time=2)
            self.play(Create(wire), FadeIn(off), run_time=2)
        with self.beat("s01b02") as b:
            new_tag = Tag("threat_model")
            copy = Circle(radius=0.3, color=TEAL, stroke_width=4).move_to(LEFT * 0.7 + UP * 1.75)
            copy_label = T("Copy", size=24).next_to(copy, UP, buff=0.2)
            resources = VGroup(*[Square(side_length=0.35, color=AMBER, fill_opacity=0.2).shift(RIGHT * i * 0.5) for i in range(3)]).move_to(RIGHT * 1 + DOWN * 1.2)
            resources_label = T("Resources", size=24).next_to(resources, DOWN, buff=0.25)
            branch_copy = Arrow(agent.get_center(), copy.get_center(), color=TEAL, buff=0.3)
            branch_resources = Arrow(agent.get_center(), resources.get_center(), color=AMBER, buff=0.3)
            barrier = Line(LEFT * 4 + DOWN * 1.3, LEFT * 3 + DOWN * 1.3, color=ROSE, stroke_width=8)
            resist = T("Shutdown resistance", size=24, color=ROSE).move_to(LEFT * 3.5 + DOWN * 2.9)
            self.play(ReplacementTransform(tag, new_tag), run_time=0.5)
            tag = new_tag
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
        with self.beat("s01b04") as b:
            new_tag = Tag("method")
            paper_title = Serif("The Basic AI Drives", size=34).move_to(UP * 2.2)
            tools = Node("Shared means", color=AMBER, width=2.7).move_to(ORIGIN + UP * 0.3)
            different = T("Different goals", size=26).move_to(RIGHT * 3.6 + DOWN * 0.65)
            left_link = Arrow(agent.get_right(), tools.get_left(), color=TEAL, buff=0.2)
            right_link = Arrow(tools.get_right(), goal.get_left(), color=AMBER, buff=0.2)
            small_board = Grid(2, 2, cell=0.3).move_to(LEFT * 3.5 + UP * 0.35)
            self.play(ReplacementTransform(tag,new_tag), FadeOut(VGroup(boundary,drive_label,gate,counter,system_label)), FadeIn(paper_title), run_time=2)
            tag = new_tag
            self.play(Transform(branch_copy,left_link), Transform(branch_resources,right_link), FadeIn(tools), Create(small_board), FadeIn(different), run_time=3)
            self.play(Indicate(tools, color=AMBER), run_time=2)
        with self.beat("s01b05") as b:
            new_tag = Tag("author_interpretation")
            future = Circle(radius=0.6, color=TEAL, stroke_width=4).move_to(RIGHT * 0.7 + UP * 0.35)
            current_label = T("Current system", size=26).move_to(LEFT * 3.5 + DOWN * 0.65)
            future_label = T("Future system", size=26).move_to(RIGHT * 0.7 + DOWN * 0.65)
            future_path = Arrow(agent.get_right(), future.get_left(), color=AMBER, buff=0.2)
            final_path = Arrow(future.get_right(), goal.get_left(), color=AMBER, buff=0.2)
            new_goal = Node("Goal", color=AMBER, width=2.6).move_to(goal)
            self.play(ReplacementTransform(tag,new_tag), FadeOut(VGroup(paper_title,tools,different,small_board)), Transform(goal,new_goal), FadeIn(current_label), run_time=2)
            tag = new_tag
            self.play(TransformFromCopy(agent,future), FadeIn(future_label), Transform(branch_copy,future_path), Transform(branch_resources,final_path), run_time=3)
            self.play(Indicate(future, color=TEAL), Indicate(branch_resources, color=AMBER), run_time=2)
