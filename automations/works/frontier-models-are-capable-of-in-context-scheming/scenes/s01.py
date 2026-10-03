# storyboard: af7bd03320cfb6b5
from aisr_kit import *

def clear_at_end(scene, start, b, mobjects, run_time=0.4):
    # Fade out state that belongs only to this beat so the next beat opens on its own visuals.
    left = b.duration - run_time - (scene.renderer.time - start)
    if left > 0:
        scene.wait(left)
    scene.play(FadeOut(*mobjects), run_time=run_time)

class S01(NarratedScene):
    def construct(self):
        with self.beat("s01b01") as b:
            heading = Heading("A plausible list")
            tag = Tag("future_scenario")
            source = Source("Meinke et al. (2024)")
            inbox_label = T("Inbox", size=34).move_to([-4.5, 1.7, 0])
            cards = VGroup(*[RoundedRectangle(width=1.65, height=0.62, corner_radius=0.08, stroke_color=SOFT, fill_color=PANEL, fill_opacity=1).move_to([-4.5, 0.8-i*0.85, 0]) for i in range(3)])
            rule = Node("Your rule", color=TEAL, width=2.4, height=1.35, size=32).move_to([0, 0, 0])
            list_label = T("Ranked list", size=34).move_to([4.5, 1.7, 0])
            bars = VGroup(*[Rectangle(width=1.9-i*0.35, height=0.26, stroke_width=0, fill_color=TEAL, fill_opacity=0.9).move_to([4.5, 0.65-i*0.65, 0]) for i in range(3)])
            left_arrow = Arrow([-3.4, 0, 0], [-1.2, 0, 0], color=TEAL, buff=0)
            right_arrow = Arrow([1.2, 0, 0], [3.25, 0, 0], color=TEAL, buff=0)
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), FadeIn(inbox_label), FadeIn(list_label), Create(cards), Create(rule), run_time=1.5)
            self.play(GrowArrow(left_arrow), GrowArrow(right_arrow), run_time=1)
            for i in range(3):
                moving = cards[i].copy().scale(0.5)
                self.add(moving)
                self.play(moving.animate.move_to(rule.get_center()), run_time=0.8)
                self.play(moving.animate.move_to(bars[i].get_center()), run_time=0.8)
                self.play(FadeOut(moving), FadeIn(bars[i]), run_time=0.35)
            pipeline = VGroup(inbox_label, cards, rule, list_label, bars, left_arrow, right_arrow)
        with self.beat("s01b02") as b:
            changed = T("Changed input", size=34, color=AMBER).move_to([-2.8, -2.0, 0])
            branch = VMobject().set_points_as_corners([[-3.1,-1.5,0],[-2.4,-1.5,0],[-1.9,0,0],[-1.2,0,0]]).set_stroke(AMBER, 5)
            diamond = Square(side_length=0.28, color=AMBER, fill_opacity=1).rotate(PI/4).move_to([-3.1,-1.5,0])
            same_label = T("Same rule", size=32).move_to(rule.label)
            self.play(Create(branch), FadeIn(diamond), FadeIn(changed), FadeOut(rule.label), run_time=1.2)
            self.play(FadeIn(same_label), run_time=0.8)
            self.play(diamond.animate.move_to([-1.9, 0, 0]), Indicate(rule.box, color=TEAL), run_time=2)
            self.play(bars[0].animate.move_to([4.5,-0.65,0]), bars[2].animate.move_to([4.5,0.65,0]), run_time=2)
        with self.beat("s01b03") as b:
            start = self.renderer.time
            new_tag = Tag("threat_model")
            human = Square(side_length=0.45, color=TEAL, fill_opacity=0.7).move_to([-2.7,-2.0,0])
            conflict = Square(side_length=0.45, color=AMBER, fill_opacity=0.7).rotate(PI/4).move_to([2.7,-2.0,0])
            human_label = T("Human goal", size=32, color=TEAL).next_to(human, DOWN, buff=0.2)
            conflict_label = T("Conflicting goal", size=32, color=AMBER).next_to(conflict, DOWN, buff=0.2)
            scheming = T("Scheming", size=36, color=AMBER).move_to([0,2.05,0])
            agent = Agent(color=SAND).move_to([2.7,-1.45,0])
            route = VMobject().set_points_as_corners([[2.7,-1.45,0],[1.4,-1.45,0],[0,-0.95,0],[-1.6,-0.4,0]]).set_stroke(AMBER, 3)
            self.play(FadeOut(tag), FadeIn(new_tag), FadeOut(changed), FadeOut(branch), FadeOut(diamond), FadeIn(human), FadeIn(conflict), FadeIn(human_label), FadeIn(conflict_label), FadeIn(scheming), run_time=1.5)
            tag = new_tag
            self.play(Create(route), FadeIn(agent), run_time=1.5)
            self.play(MoveAlongPath(agent, route), run_time=3)
            clear_at_end(self, start, b, [tag, human, conflict, human_label, conflict_label, scheming, route, agent])
        with self.beat("s01b04") as b:
            tag = Tag("method")
            enclosure = RoundedRectangle(width=11.6,height=5.2,corner_radius=0.12,color=SOFT).move_to([0,-0.45,0])
            test_label = T("Constructed tests",size=36).move_to([0,1.65,0])
            agent = Agent(color=SAND, radius=0.3).move_to([0,-1.65,0])
            self.play(FadeIn(tag), FadeOut(inbox_label), FadeOut(list_label), FadeOut(same_label), run_time=0.6)
            pipeline = VGroup(cards, rule.box, bars, left_arrow, right_arrow)
            self.play(pipeline.animate.scale(0.7).move_to([0,0.35,0]), Create(enclosure), FadeIn(test_label), run_time=1.6)
            self.play(FadeIn(agent), run_time=0.6)
            goal = Node("Goal",color=AMBER,width=2.1,height=0.85,size=34).move_to([-3.9,-1.65,0])
            memo = Node("Situation",color=SOFT,width=2.6,height=0.85,size=34).move_to([3.9,-1.65,0])
            goal_link = Link(goal,agent,color=AMBER)
            memo_link = Link(memo,agent,color=SOFT)
            self.play(FadeIn(goal),FadeIn(memo),GrowArrow(goal_link.arrow),GrowArrow(memo_link.arrow),run_time=2)
            self.play(Indicate(goal.box,color=AMBER),Indicate(memo.box,color=SOFT),run_time=2)
        with self.beat("s01b05") as b:
            self.play(FadeOut(pipeline),FadeOut(goal),FadeOut(memo),FadeOut(goal_link.arrow),FadeOut(memo_link.arrow),agent.animate.move_to([0,0,0]),run_time=1.5)
            agent_label = T("Agent",size=26).move_to([0,-0.7,0])
            files = VGroup(*[RoundedRectangle(width=1.25,height=0.68,corner_radius=0.05,color=SOFT,fill_color=PANEL,fill_opacity=1).move_to([-3.4,0.6-i*0.8,0]) for i in range(3)])
            files_label = T("Files",size=26).move_to([-3.4,1.55,0])
            terminal = RoundedRectangle(width=2.3,height=1.6,corner_radius=0.08,color=TEAL,fill_color=PANEL,fill_opacity=1).move_to([3.2,0,0])
            terminal_lines = VGroup(*[Line([2.45,0.4-i*0.35,0],[3.65-i*0.25,0.4-i*0.35,0],color=TEAL) for i in range(3)])
            tools_label = T("Tools",size=26).move_to([3.2,1.55,0])
            access_left = Arrow([-0.5,0,0],[-2.6,0,0],color=SOFT,buff=0)
            access_right = Arrow([0.5,0,0],[1.9,0,0],color=TEAL,buff=0)
            self.play(Create(files),Create(terminal),Create(terminal_lines),FadeIn(files_label),FadeIn(tools_label),FadeIn(agent_label),GrowArrow(access_left),GrowArrow(access_right),run_time=2)
            self.play(agent.animate.move_to([-1.8,0,0]),Indicate(access_left,color=SAND),run_time=2)
            self.play(agent.animate.move_to([1.2,0,0]),Indicate(access_right,color=TEAL),run_time=2)
            self.play(agent.animate.move_to([0,0,0]),run_time=1)
