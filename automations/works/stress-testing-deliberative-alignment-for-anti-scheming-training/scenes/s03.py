# storyboard: 1d250c18453a0a64
from aisr_kit import *


def rate_chart(data):
    chart = BarChart(data['points'], colors=[AMBER, TEAL], width=5.8, height=3.1, max_value=15, label_size=24)
    chart.shift(np.array([-2.4, -1.8, 0]) - chart.baseline.get_center())
    model = T(data['title'].replace(' covert actions', ''), size=30).move_to([-2.4, 2.15, 0])
    caption = T('Covert action rate', size=24, color=SOFT).move_to([-2.4, -2.55, 0])
    ticks = VGroup()
    for value, label in [(0, '0%'), (5, '5%'), (10, '10%'), (15, '15%')]:
        ticks.add(T(label, size=20, color=MUTED).move_to([-6.1, -1.8 + value / 15 * 3.1, 0]))
    return VGroup(chart, model, caption, ticks)


class S03(NarratedScene):
    def construct(self):
        with self.beat('s03b01') as b:
            heading = Heading('A large reduction with residual failures')
            tag = Tag('observed_result')
            source = Source('Schoen et al. (2025)')
            graph = rate_chart(self.dataset('d1'))
            boundary = T('Selected test aggregate', size=27, color=SOFT, width=20).move_to([3.8, 0.4, 0])
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), run_time=1)
            self.play(FadeIn(graph[0].frame), FadeIn(graph[1:]), FadeIn(boundary), run_time=1.5)
            self.play(bars_grow(graph[0]), run_time=2)
            self.play(FadeIn(graph[0].values), run_time=1)
            self.play(Indicate(graph[0].bars[1], color=TEAL), run_time=1.5)
        with self.beat('s03b02') as b:
            updated = rate_chart(self.dataset('d2'))
            self.play(Transform(graph, updated), run_time=3)
            self.play(Indicate(graph[0].bars[1], color=TEAL), run_time=1.5)
        with self.beat('s03b03') as b:
            new_tag = Tag('method')
            self.play(ReplacementTransform(tag, new_tag), FadeOut(boundary), graph.animate.scale(0.62).move_to([-4.2, 0.1, 0]), run_time=1.5)
            tag = new_tag
            gate = Rectangle(width=1.2, height=2.1, color=TEAL).move_to([2.8, 0.6, 0])
            gate_label = T('Selected aggregate', size=24, width=18).move_to([2.8, 2.15, 0])
            accepted = RoundedRectangle(width=0.55, height=0.7, color=TEAL).move_to([0.6, 0.6, 0])
            exclusions = VGroup(*[T(label, size=22, color=SOFT) for label in ['Zero-rate tests', 'Permitted game deception', 'Later adversarial tests']]).arrange(DOWN, buff=0.35).move_to([2.8, -1.9, 0])
            self.play(Create(gate), FadeIn(gate_label), Create(accepted), run_time=1.5)
            self.play(accepted.animate.move_to([4.7, 0.6, 0]), run_time=2)
            for label in exclusions:
                card = RoundedRectangle(width=0.55, height=0.7, color=AMBER).move_to([0.6, 0.6, 0])
                self.play(Create(card), run_time=0.5)
                self.play(card.animate.move_to([0.6, label.get_y(), 0]), FadeIn(label), run_time=1)
                self.play(FadeOut(card), run_time=0.3)
            group = VGroup(gate, gate_label, accepted, exclusions)
        with self.beat('s03b04') as b:
            new_tag = Tag('observed_result')
            self.play(FadeOut(graph), FadeOut(group), ReplacementTransform(tag, new_tag), run_time=1)
            tag = new_tag
            agent = Agent(color=SAND, radius=0.45).move_to([-4.8, -0.5, 0])
            thought = RoundedRectangle(width=3.7, height=1.5, color=TEAL).move_to([-1.4, 1.2, 0])
            outcome = Node('Covert action', color=AMBER, width=3.1).move_to([4, -0.5, 0])
            route = Arrow(agent.get_right(), outcome.get_left(), color=AMBER, buff=0.2)
            label = T('No rule reasoning', size=27).move_to(thought)
            self.play(FadeIn(agent), Create(thought), FadeIn(label), FadeIn(outcome), GrowArrow(route), run_time=2)
            token = Circle(radius=0.15, color=AMBER, fill_opacity=1).move_to(agent)
            self.play(MoveAlongPath(token, route), run_time=2)
            wrong = T('Wrong citation', size=27, color=AMBER).move_to(thought)
            self.play(Transform(label, wrong), run_time=1)
            self.play(token.animate.move_to(agent), run_time=0.5)
            self.play(MoveAlongPath(token, route), run_time=2)
            correct = T('Correct reasoning', size=27, color=TEAL).move_to(thought)
            self.play(Transform(label, correct), run_time=1)
            self.play(token.animate.move_to(agent), run_time=0.5)
            self.play(MoveAlongPath(token, route), run_time=2)
            failure = VGroup(agent, thought, outcome, route, label, token)
        with self.beat('s03b05') as b:
            self.play(FadeOut(failure), run_time=1)
            trained = Agent(color=TEAL, radius=0.5).move_to([0, 0, 0])
            tray = Rectangle(width=2.6, height=0.7, color=TEAL).move_to([4.2, 0, 0])
            route = Arrow([-4.4, 0, 0], [3.1, 0, 0], color=TEAL, buff=0)
            left_label = T('Legitimate tasks', size=27).move_to([-4.3, 1.25, 0])
            right_label = T('Task completion', size=27).move_to([4.2, 1.25, 0])
            refusal = Rectangle(width=1.2, height=0.7, color=MUTED).move_to([0, -2, 0])
            refusal_label = T('Overrefusal check', size=24, color=SOFT).move_to([0, -2.85, 0])
            self.play(GrowArrow(route), FadeIn(trained), Create(tray), FadeIn(left_label), FadeIn(right_label), Create(refusal), FadeIn(refusal_label), run_time=2)
            for offset in [-0.4, 0, 0.4]:
                card = RoundedRectangle(width=0.5, height=0.65, color=SAND, fill_color=BG, fill_opacity=1).move_to([-4.5, 0, 0])
                self.play(FadeIn(card), run_time=0.4)
                self.play(card.animate.move_to([0, 0, 0]), run_time=1)
                self.play(card.animate.move_to([4.2 + offset, 0, 0]), run_time=1.2)
