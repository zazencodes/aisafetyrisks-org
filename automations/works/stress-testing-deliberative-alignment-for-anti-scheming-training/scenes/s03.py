# storyboard: 1d250c18453a0a64
from aisr_kit import *


def rate_chart(data):
    # Zero-based bars with exact values; phone-readable labels, no redundant tick column.
    chart = BarChart(data['points'], colors=[AMBER, TEAL], width=5.8, height=3.1, max_value=15, label_size=44)
    chart.labels.set_color(INK)
    chart.shift(np.array([-2.4, -1.5, 0]) - chart.baseline.get_center())
    model = T(data['title'].replace(' covert actions', ''), size=44, weight=MEDIUM).move_to([-2.4, 2.45, 0])
    caption = T('Covert action rate', size=34, color=SOFT).move_to([-2.4, -2.7, 0])
    return VGroup(chart, model, caption)


class S03(NarratedScene):
    def construct(self):
        with self.beat('s03b01') as b:
            heading = Heading('A large reduction with residual failures')
            tag = Tag('observed_result')
            source = Source('Schoen et al. (2025)')
            graph = rate_chart(self.dataset('d1'))
            boundary = T('Selected test aggregate', size=40, color=SOFT, width=14).move_to([3.6, 0.4, 0])
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), run_time=1)
            self.play(FadeIn(graph[0].frame), FadeIn(graph[1:]), FadeIn(boundary), run_time=1.5)
            self.play(bars_grow(graph[0]), run_time=2)
            self.play(FadeIn(graph[0].values), run_time=1)
            self.play(Indicate(graph[0].bars[1], color=TEAL), run_time=1.5)
        with self.beat('s03b02') as b:
            updated = rate_chart(self.dataset('d2'))
            chart, new_chart = graph[0], updated[0]
            # Swap the model label and values instantly so o3's text is correct from the first frame.
            values = new_chart.values
            value_targets = [value.get_center() for value in values]
            for value, bar in zip(values, chart.bars):
                value.next_to(bar, UP, buff=0.12)
            self.remove(graph[1], chart.values)
            self.add(updated[1], values)
            chart.submobjects[2] = values
            chart.values = values
            model_label = updated[1]
            self.play(Transform(chart.bars, new_chart.bars), *[value.animate.move_to(target) for value, target in zip(values, value_targets)], run_time=0.6)
            self.play(Indicate(graph[0].bars[1], color=TEAL), run_time=1.5)
        with self.beat('s03b03') as b:
            new_tag = Tag('method')
            self.remove(tag)
            self.add(new_tag)
            tag = new_tag
            # Retain the comparison as an inset; drop the axis caption.
            inset = VGroup(chart, model_label)
            self.play(FadeOut(boundary), FadeOut(graph[2]), inset.animate.scale(0.7).move_to([-4.2, 0.1, 0]), run_time=1.5)
            gate = Rectangle(width=1.2, height=1.5, color=TEAL).move_to([2.8, 0.9, 0])
            gate_label = T('Selected aggregate', size=36, color=TEAL).move_to([3.1, 2.15, 0])
            accepted = RoundedRectangle(width=0.55, height=0.7, corner_radius=0.08, color=TEAL).move_to([0.3, 0.9, 0])
            excluded_label = T('Excluded', size=36, color=AMBER, weight=MEDIUM).move_to([0, -0.55, 0]).align_to([0.85, 0, 0], LEFT)
            exclusions = VGroup(*[T(label, size=34, color=INK).align_to([0.85, top, 0], UL) for label, top in [('Zero-rate tests', -1.0), ('Permitted game deception', -1.65), ('Later adversarial tests', -2.3)]])
            marker = Line([0.6, -0.3, 0], [0.6, -2.75, 0], color=AMBER, stroke_width=3)
            self.play(Create(gate), FadeIn(gate_label), Create(accepted), run_time=1.5)
            self.play(accepted.animate.move_to([4.7, 0.9, 0]), run_time=2)
            self.play(FadeIn(excluded_label), Create(marker), run_time=0.8)
            for label in exclusions:
                card = RoundedRectangle(width=0.4, height=0.5, corner_radius=0.06, color=AMBER).move_to([0.3, 0.9, 0])
                self.play(Create(card), run_time=0.5)
                self.play(card.animate.move_to([0.25, label.get_y(), 0]), FadeIn(label), run_time=1)
                self.play(FadeOut(card), run_time=0.3)
            group = VGroup(gate, gate_label, accepted, excluded_label, marker, exclusions)
        with self.beat('s03b04') as b:
            new_tag = Tag('observed_result')
            self.remove(tag)
            self.add(new_tag)
            tag = new_tag
            self.play(FadeOut(inset), FadeOut(group), run_time=1)
            agent = Agent(color=SAND, radius=0.45).move_to([-4.8, -0.5, 0])
            thought = RoundedRectangle(width=3.7, height=1.5, color=TEAL).move_to([-1.4, 1.2, 0])
            outcome = Node('Covert action', color=AMBER, width=3.1).move_to([4, -0.5, 0])
            route = Arrow(agent.get_right(), outcome.get_left(), color=AMBER, buff=0.2)
            label = T('No rule reasoning', size=27).move_to(thought)
            self.play(FadeIn(agent), Create(thought), FadeIn(label), FadeIn(outcome), GrowArrow(route), run_time=2)
            token = Circle(radius=0.15, color=AMBER, fill_opacity=1).move_to(agent)
            self.play(MoveAlongPath(token, route), run_time=2)
            wrong = T('Wrong citation', size=27, color=AMBER).move_to(thought)
            self.play(FadeOut(label), run_time=0.3)
            self.play(FadeIn(wrong), run_time=0.4)
            label = wrong
            self.play(token.animate.move_to(agent), run_time=0.5)
            self.play(MoveAlongPath(token, route), run_time=2)
            correct = T('Correct reasoning', size=27, color=TEAL).move_to(thought)
            self.play(FadeOut(label), run_time=0.3)
            self.play(FadeIn(correct), run_time=0.4)
            label = correct
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
            for offset in [-0.6, 0, 0.6]:
                card = RoundedRectangle(width=0.45, height=0.6, corner_radius=0.08, color=SAND, fill_color=BG, fill_opacity=1).move_to([-4.5, 0, 0])
                self.play(FadeIn(card), run_time=0.4)
                self.play(card.animate.move_to([0, 0, 0]), run_time=1)
                self.play(card.animate.move_to([4.2 + offset, 0, 0]), run_time=1.2)
