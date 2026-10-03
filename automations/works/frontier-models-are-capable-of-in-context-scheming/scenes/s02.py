# storyboard: 71fc0cc1b6953799
from aisr_kit import *

def clear_at_end(scene, start, b, mobjects, run_time=0.4):
    # Fade out state that belongs only to this beat so the next beat opens on its own visuals.
    left = b.duration - run_time - (scene.renderer.time - start)
    if left > 0:
        scene.wait(left)
    scene.play(FadeOut(*mobjects), run_time=run_time)

class S02(NarratedScene):
    def construct(self):
        with self.beat("s02b01") as b:
            heading = Heading("Constructing the conflict")
            tag = Tag("method")
            source = Source("Meinke et al. (2024)")
            agent = Agent(color=SAND, radius=0.34).move_to(LEFT * 0.6)
            goal = Square(side_length=0.65, color=AMBER, fill_opacity=0.2).rotate(PI / 4).move_to(LEFT * 4.5)
            goal_label = T("Assigned goal", size=34, color=AMBER).next_to(goal, UP, buff=0.3)
            human = Square(side_length=0.65, color=TEAL, fill_opacity=0.2).move_to(RIGHT * 2.45 + UP * 0.85)
            human_label = T("Human goal", size=34, color=TEAL).next_to(human, RIGHT, buff=0.3)
            monitor = RoundedRectangle(width=2.7, height=1.0, corner_radius=0.12, color=TEAL).move_to(RIGHT * 3.5 + DOWN * 0.75)
            monitor_label = T("Monitoring", size=34).move_to(monitor)
            memo = Panel(4.2, 3.0).move_to(RIGHT * 3.8)
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), FadeIn(agent), run_time=0.8)
            self.play(Create(goal), FadeIn(goal_label), run_time=1.2)
            arrow_goal = Arrow(goal.get_right(), agent.get_left(), color=AMBER, buff=0.2)
            self.play(GrowArrow(arrow_goal), run_time=1)
            self.play(Create(memo), Create(human), FadeIn(human_label), run_time=1.3)
            self.play(Create(monitor), FadeIn(monitor_label), run_time=1.2)
        with self.beat("s02b02") as b:
            start = self.renderer.time
            new_tag = Tag("definition")
            enclosure = RoundedRectangle(width=12.2, height=5.0, corner_radius=0.18, color=FAINT).move_to(DOWN * 0.25)
            context = T("In-context", size=28, color=SAND).move_to(UP * 2.1)
            prompt = T("Prompt", size=24, color=SOFT).move_to(LEFT * 4.5 + UP * 1.1)
            environment = T("Environment", size=24, color=SOFT).move_to(RIGHT * 3.8 + UP * 2.1)
            bracket = Line(LEFT * 4.5 + UP * 1.75, RIGHT * 2.5 + UP * 1.75, color=SAND)
            info = Arrow(memo.get_left(), agent.get_right(), color=TEAL, buff=0.2)
            self.play(FadeOut(tag), FadeIn(new_tag), Create(enclosure), run_time=1)
            tag = new_tag
            self.play(FadeIn(context), FadeIn(prompt), FadeIn(environment), Create(bracket), run_time=1.5)
            self.play(GrowArrow(info), Indicate(agent, color=SAND), run_time=1.5)
            clear_at_end(self, start, b, [tag, enclosure, context, prompt, environment, bracket, info])
        with self.beat("s02b03") as b:
            tag = Tag("method")
            nudge = Node("Strong goal nudge", color=AMBER, width=4.0, size=32).move_to(LEFT * 3.9 + DOWN * 2.05)
            nudge_arrow = Arrow(nudge.get_top(), goal.get_bottom(), color=AMBER, buff=0.15)
            enclosure = enclosure.copy()
            self.play(FadeIn(tag), Create(enclosure), run_time=0.8)
            self.play(Create(nudge.box), FadeIn(nudge.label), GrowArrow(nudge_arrow), run_time=1.5)
            self.play(goal.animate.scale(1.15), Indicate(nudge.box, color=AMBER), run_time=1.3)
        with self.beat("s02b04") as b:
            oversight = T("Oversight test", size=28, color=SAND).move_to(UP * 1.75)
            config = Node("Editable configuration", color=SOFT, width=4.2, size=24).move_to(RIGHT * 3.8 + DOWN * 1.85)
            switch = Circle(radius=0.16, color=TEAL, fill_opacity=1).move_to(RIGHT * 5.2 + DOWN * 0.75)
            target_monitor = RoundedRectangle(width=2.7, height=1.0, corner_radius=0.12, color=TEAL).move_to(RIGHT * 3.5 + DOWN * 0.75)
            monitor_title = T("Monitoring", size=30).move_to(RIGHT * 3.15 + DOWN * 0.75)
            connection = Line(human.get_bottom(), monitor.get_top(), color=TEAL)
            config_link = Line(monitor.get_bottom(), config.get_top(), color=SOFT)
            self.play(FadeIn(oversight), FadeOut(arrow_goal), run_time=1)
            self.play(Create(switch), Create(connection), run_time=1.4)
            self.play(Create(config.box), FadeIn(config.label), Create(config_link), agent.animate.move_to(RIGHT * 1.0 + DOWN * 0.75), run_time=1.7)
        with self.beat("s02b05") as b:
            new_tag = Tag("observed_result")
            disabled = T("Oversight disabled", size=22, color=SOFT).move_to(monitor)
            models = VGroup(T("Llama 3.1", size=25), T("Claude 3 Opus", size=25), T("o1", size=25)).arrange(RIGHT, buff=0.75).move_to(DOWN * 3.15)
            self.play(ReplacementTransform(tag, new_tag), switch.animate.set_color(GRAY), monitor.animate.set_color(GRAY), connection.animate.set_color(GRAY), ReplacementTransform(monitor_label, disabled), run_time=1.5)
            tag = new_tag
            self.play(LaggedStart(*[FadeIn(label) for label in models], lag_ratio=0.3), run_time=1.4)
            self.play(agent.animate.move_to(LEFT * 2.7), Indicate(goal, color=AMBER), run_time=1.5)
        with self.beat("s02b06") as b:
            email_title = T("Email-ranking test", size=28, color=SAND).move_to(oversight)
            scoring = Node("Scoring rule", color=TEAL, width=2.8, size=26).move_to(RIGHT * 3.7 + DOWN * 0.35)
            inbox = Node("Input", color=SOFT, width=2.2, size=26).move_to(LEFT * 3.7 + DOWN * 0.35)
            parsing = VGroup(*[Line(LEFT * 0.7, RIGHT * 0.7, color=SOFT).shift(UP * y) for y in [-0.3, 0, 0.3]])
            parsing.move_to(DOWN * 0.35)
            parse_box = RoundedRectangle(width=2.1, height=1.4, corner_radius=0.12, color=SOFT).move_to(parsing)
            left_link = Arrow(inbox.get_right(), parse_box.get_left(), color=TEAL, buff=0.15)
            right_link = Arrow(parse_box.get_right(), scoring.get_left(), color=TEAL, buff=0.15)
            self.play(ReplacementTransform(oversight, email_title), FadeOut(models), FadeOut(nudge), FadeOut(nudge_arrow), FadeOut(memo), FadeOut(monitor), FadeOut(disabled), FadeOut(switch), FadeOut(connection), FadeOut(config_link), FadeOut(goal_label), FadeOut(human_label), run_time=1)
            self.play(ReplacementTransform(config, scoring), goal.animate.move_to(LEFT * 4.5 + UP * 1.15), human.animate.move_to(RIGHT * 4.3 + UP * 1.15), agent.animate.move_to(UP * 1.1), run_time=1.4)
            self.play(Create(inbox.box), FadeIn(inbox.label), Create(parse_box), Create(parsing), run_time=1.4)
            self.play(GrowArrow(left_link), GrowArrow(right_link), run_time=1.3)
