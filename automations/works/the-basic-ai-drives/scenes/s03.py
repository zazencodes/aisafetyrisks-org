# storyboard: d2e19662d517bd89
from aisr_kit import *


def board_at(center, scale=1):
    board = Grid(4, 4, cell=0.48 * scale).move_to(center)
    for r in range(4):
        for c in range(4):
            board.cell(r, c).set_fill(TEAL if (r + c) % 2 else PANEL, opacity=0.25)
    pieces = VGroup(*[Circle(radius=0.10 * scale, color=INK, fill_opacity=1).move_to(board.cell(r, c)) for r, c in [(0, 1), (1, 3), (3, 0)]])
    return VGroup(board, pieces)


class S03(NarratedScene):
    def construct(self):
        with self.beat('s03b01') as b:
            heading = Heading('What counts as success?')
            tag = Tag('author_interpretation')
            source = Source('OMOHUNDRO (2007)')
            goal = Node('Protected goal', color=AMBER, width=3).move_to([0, 0, 0])
            circuit = RoundedRectangle(width=5, height=3.3, corner_radius=0.5, color=TEAL)
            machine_label = T('Machinery', size=28, color=TEAL).move_to([0, -2, 0])
            edit = Arrow([-5, 0, 0], [-1.8, 0, 0], color=AMBER)
            deflect = Arrow([-1.8, 0, 0], [-2.7, 1.5, 0], color=AMBER)
            update = Arrow([4.7, -1, 0], [2.7, -1, 0], color=TEAL)
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), Create(circuit), FadeIn(goal), FadeIn(machine_label), run_time=2)
            self.play(GrowArrow(edit), run_time=2)
            self.play(GrowArrow(deflect), Indicate(goal), run_time=2)
            self.play(GrowArrow(update), Transform(circuit, RoundedRectangle(width=5.4, height=3.5, corner_radius=0.8, color=TEAL)), run_time=3)
        with self.beat('s03b02') as b:
            self.play(Transform(tag, Tag('future_scenario')), FadeOut(edit), FadeOut(deflect), FadeOut(update), FadeOut(circuit), FadeOut(machine_label), run_time=1)
            outcome = Circle(radius=0.65, color=AMBER).move_to([-4, -0.4, 0])
            representation = RoundedRectangle(width=2, height=1.5, color=AMBER).move_to([4, -0.4, 0])
            representation_label = T('Representation matters', size=27).move_to([3.3, -1.8, 0])
            exception = T('Exceptions', size=30, color=AMBER).move_to([0, 2, 0])
            left_link = Link(goal, outcome, color=AMBER)
            right_link = Link(goal, representation, color=AMBER)
            self.play(Create(outcome), Create(representation), FadeIn(exception), FadeIn(representation_label), GrowArrow(left_link.arrow), GrowArrow(right_link.arrow), run_time=3)
            self.play(Transform(representation, Circle(radius=0.75, color=AMBER).move_to([4, -0.4, 0])), Indicate(right_link.arrow), run_time=3)
        with self.beat('s03b03') as b:
            self.play(FadeOut(VGroup(goal, outcome, representation, representation_label, exception, left_link, right_link)), run_time=1)
            board = board_at([-3.6, 0, 0])
            board_box = RoundedRectangle(width=3.4, height=3.4, color=FAINT).move_to([-3.6, 0, 0])
            register_box = RoundedRectangle(width=3.4, height=3.4, color=FAINT).move_to([3.6, 0, 0])
            register = RoundedRectangle(width=2.5, height=1.3, color=AMBER).move_to([3.6, 0, 0])
            labels = VGroup(T('Games won', size=30).move_to([-3.6, 2.15, 0]), T('Win counter', size=30).move_to([3.6, 2.15, 0]))
            route = Arrow([-1.8, 0, 0], [1.8, 0, 0], color=AMBER)
            token = Circle(radius=0.16, color=AMBER, fill_opacity=1).move_to([-3.6, 0, 0])
            self.play(Create(board), Create(board_box), Create(register_box), Create(register), FadeIn(labels), run_time=3)
            self.play(GrowArrow(route), FadeIn(token), run_time=2)
            self.play(token.animate.move_to([2.9, 0, 0]), run_time=3)
        with self.beat('s03b04') as b:
            self.play(Transform(labels[0], T('Real wins', size=30).move_to([-3.6, 2.15, 0])), Transform(labels[1], T('Edited record', size=30).move_to([3.6, 2.15, 0])), FadeOut(route), run_time=1)
            dots = VGroup(*[Circle(radius=0.16, color=AMBER, fill_opacity=1).move_to([3.4 + i * 0.5, 0, 0]) for i in range(3)])
            shortcut = Arrow([5.8, -2, 0], [4.5, -0.7, 0], color=AMBER)
            goal_marker = Circle(radius=0.28, color=AMBER, fill_opacity=0.15).move_to([0, -2, 0])
            goal_link = Arrow(goal_marker.get_center(), [-3.6, -1.1, 0], color=AMBER)
            self.play(GrowArrow(shortcut), FadeIn(goal_marker), GrowArrow(goal_link), run_time=2)
            self.play(LaggedStart(*[FadeIn(dot) for dot in dots], lag_ratio=0.4), Indicate(board), run_time=3)
        with self.beat('s03b05') as b:
            self.play(Transform(labels[0], T('Board untouched', size=30).move_to([-3.6, 2.15, 0])), Transform(labels[1], T('Counter as goal', size=30).move_to([3.6, 2.15, 0])), Transform(goal_link, Arrow(goal_marker.get_center(), [3.6, -0.8, 0], color=AMBER)), board.animate.set_opacity(0.35), FadeOut(shortcut), run_time=3)
            machine = Circle(radius=0.4, color=TEAL).move_to([5.5, -1.8, 0])
            loop = CurvedArrow([5.5, -1.3, 0], [4.8, 0.3, 0], color=TEAL)
            more = VGroup(*[Circle(radius=0.12, color=AMBER, fill_opacity=1).move_to([3 + i * 0.4, 0.4, 0]) for i in range(4)])
            self.play(Create(machine), Create(loop), run_time=2)
            self.play(LaggedStart(*[FadeIn(dot) for dot in more], lag_ratio=0.3), run_time=3)
        with self.beat('s03b06') as b:
            self.play(Transform(tag, Tag('limitation')), FadeOut(VGroup(board, board_box, register_box, register, labels, token, dots, goal_marker, goal_link, machine, loop, more)), run_time=1)
            panels = VGroup(Panel(5.2, 4), Panel(5.2, 4)).arrange(RIGHT, buff=0.7).move_to([0, -0.2, 0])
            left_board = board_at([-2.95, -0.7, 0], 0.8)
            right_record = RoundedRectangle(width=2.4, height=1.2, color=AMBER).move_to([2.95, -0.7, 0])
            titles = VGroup(T('True goal', size=30).move_to([-2.95, 1.3, 0]), T('Proxy signal', size=30).move_to([2.95, 1.3, 0]))
            goals = VGroup(Circle(radius=0.2, color=AMBER).move_to([-2.95, 0.65, 0]), Circle(radius=0.2, color=AMBER).move_to([2.95, 0.65, 0]))
            links = VGroup(Arrow([-2.95, 0.4, 0], [-2.95, 0.05, 0], color=AMBER, buff=0), Arrow([2.95, 0.4, 0], [2.95, -0.05, 0], color=AMBER, buff=0))
            shortcut = CurvedArrow([4.6, -1.5, 0], [3.8, -0.7, 0], color=AMBER)
            wire = T('Wireheading', size=26, color=AMBER).move_to([2.95, -2.5, 0])
            model = RoundedRectangle(width=3.2, height=3, color=TEAL).move_to([-2.95, -0.45, 0])
            self.play(FadeIn(panels), Create(left_board), Create(right_record), FadeIn(titles), Create(goals), Create(links), run_time=3)
            self.play(Create(shortcut), FadeIn(wire), FadeIn(Circle(radius=0.16, color=AMBER, fill_opacity=1).move_to([2.95, -0.7, 0])), run_time=3)
            self.play(Create(model), run_time=2)
        with self.beat('s03b07') as b:
            self.play(*[FadeOut(mob) for mob in self.mobjects if mob not in [heading, tag, source]], run_time=1)
            outer = RoundedRectangle(width=9, height=4, corner_radius=0.8, color=TEAL).move_to([0, -0.2, 0])
            goal_ring = Circle(radius=1, color=AMBER).move_to([-2.4, -0.2, 0])
            record_ring = Circle(radius=1, color=AMBER).move_to([2.4, -0.2, 0])
            capsule = RoundedRectangle(width=1.4, height=0.6, color=AMBER).move_to(goal_ring)
            record = RoundedRectangle(width=1.2, height=0.8, color=AMBER).move_to(record_ring)
            captions = VGroup(T('Goal protection', size=26).move_to([-2.4, -1.65, 0]), T('Measurement protection', size=26).move_to([2.4, -1.65, 0]), T('Self-change', size=28, color=TEAL).move_to([0, 2.15, 0]), T('Open question', size=30, color=AMBER).move_to([0, -2.8, 0]))
            route = Arrow([0, 1.6, 0], [0, 0.3, 0], color=AMBER)
            junction = Circle(radius=0.16, color=AMBER).move_to([0, 0, 0])
            self.play(Create(outer), Create(goal_ring), Create(record_ring), Create(capsule), Create(record), FadeIn(captions), run_time=3)
            self.play(Transform(outer, RoundedRectangle(width=9.4, height=4, corner_radius=1, color=TEAL).move_to([0, -0.2, 0])), GrowArrow(route), Create(junction), run_time=3)
            self.play(Indicate(junction), run_time=2)
