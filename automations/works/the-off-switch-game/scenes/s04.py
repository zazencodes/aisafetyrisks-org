# storyboard: c2eeec1550a43d22
from aisr_kit import *

class S04(NarratedScene):
    def construct(self):
        with self.beat("s04b01") as b:
            heading = Heading("When oversight loses value")
            tag = Tag("method")
            source = Source("Hadfield-Menell et al. (2016)")
            caption = T("Noisy human decisions", size=30).move_to(UP*2.2)
            robot = RoundedRectangle(width=1.1, height=0.8, corner_radius=0.18, color=TEAL, fill_opacity=0.2).move_to(LEFT*3.9)
            eye = Dot(robot.get_center()+RIGHT*0.25, color=TEAL)
            human = Circle(radius=0.48, color=AMBER, fill_opacity=0.14).move_to(RIGHT*0.2)
            good = Square(side_length=0.65, color=AMBER, fill_opacity=0.2).rotate(PI/4).move_to(RIGHT*4.5+UP*1.0)
            stop = Circle(radius=0.4, color=ROSE, fill_opacity=0.15).move_to(RIGHT*4.5+DOWN*1.2)
            stop_bar = Line(stop.get_center()+LEFT*0.2, stop.get_center()+RIGHT*0.2, color=ROSE)
            gate_path = Arrow(robot.get_right(), human.get_left(), buff=0.15, color=AMBER)
            allow = Arrow(human.get_right(), good.get_left(), buff=0.15, color=AMBER)
            mistaken = DashedLine(human.get_right(), stop.get_left(), color=ROSE, stroke_width=5, dash_length=0.16)
            bell = FunctionGraph(lambda x: 0.55*np.exp(-x*x*3), x_range=[-1,1], color=AMBER).move_to(LEFT*3.9+DOWN*1.4)
            belief = T("Robot belief", size=24, color=SOFT).move_to(LEFT*3.9+DOWN*2.2)
            token = Square(side_length=0.2, color=AMBER, fill_opacity=1).rotate(PI/4).move_to(robot.get_right())
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), FadeIn(caption), run_time=1)
            self.play(Create(robot), FadeIn(eye), Create(human), Create(good), Create(stop), Create(stop_bar), run_time=2)
            self.play(Create(bell), FadeIn(belief), GrowArrow(gate_path), GrowArrow(allow), Create(mistaken), run_time=2)
            self.play(FadeIn(token), run_time=0.5)
            self.play(token.animate.move_to(human.get_center()), run_time=2)
            mistake = T("Mistake", size=30, color=ROSE).move_to(RIGHT*2.2+DOWN*1.25)
            self.play(token.animate.move_to(stop.get_center()+UP*0.65), FadeIn(mistake), run_time=2)
        with self.beat("s04b02") as b:
            new_tag = Tag("theoretical_result")
            act_label = T("Act directly", size=32, color=TEAL).move_to(LEFT*1.8+UP*2.1)
            wait_label = T("Wait", size=30, color=AMBER).move_to(LEFT*1.7+UP*0.45)
            self_label = T("Stop itself", size=32, color=ROSE).move_to(LEFT*1.8+DOWN*1.9)
            direct = CurvedArrow(robot.get_top(), good.get_top(), angle=-TAU/8, color=TEAL)
            self_stop = Circle(radius=0.3, color=ROSE).move_to(LEFT*0.3+DOWN*1.4)
            self_path = Arrow(robot.get_bottom(), self_stop.get_left(), buff=0.15, color=ROSE)
            # Swap badges cleanly: the old tag is fully gone before the new one fades in.
            self.play(FadeOut(tag), FadeOut(caption), FadeOut(bell), FadeOut(belief), FadeOut(token), FadeOut(allow), run_time=0.5)
            self.play(FadeIn(new_tag), run_time=0.5)
            tag = new_tag
            self.play(Create(direct), FadeIn(act_label), FadeIn(wait_label), run_time=2)
            self.play(Create(self_stop), GrowArrow(self_path), FadeIn(self_label), run_time=2)
            self.play(Indicate(direct, color=TEAL), run_time=2)
            self.play(Indicate(self_path, color=ROSE), run_time=2)
        with self.beat("s04b03") as b:
            new_tag = Tag("limitation")
            caption = T("Too much uncertainty", size=30).move_to(UP*2.2)
            halo = Ellipse(width=1.6,height=1.5,color=AMBER,fill_opacity=0.08).move_to(robot)
            bad = Square(side_length=0.65,color=ROSE,fill_opacity=0.15).rotate(PI/4).move_to(RIGHT*4.5+DOWN*1.2)
            self.play(ReplacementTransform(tag,new_tag), FadeOut(act_label), FadeOut(self_label), FadeOut(mistake), FadeIn(caption), FadeIn(halo), ReplacementTransform(VGroup(stop,stop_bar),bad), run_time=1.5)
            tag = new_tag
            self.play(halo.animate.stretch_to_fit_width(11).stretch_to_fit_height(3.1).move_to(RIGHT*0.1+DOWN*0.1), good.animate.set_opacity(0.25), bad.animate.set_opacity(0.25), direct.animate.set_stroke(opacity=0.25), self_path.animate.set_opacity(0.25), run_time=4)
            token.move_to(LEFT*1.6+DOWN*0.6).set_opacity(1)
            self.play(FadeIn(token), run_time=1)
        with self.beat("s04b04") as b:
            new_tag = Tag("observed_result")
            new_caption = T("Modified game",size=30).move_to(UP*2.2)
            customer = Circle(radius=0.25,color=AMBER,fill_opacity=0.25).move_to(LEFT*5.6+DOWN*2.15)
            channel = ParametricFunction(lambda t: np.array([-5.25+t*1.35,-2.0+t*1.45+0.12*np.sin(t*TAU*3),0]),t_range=[0,1],color=AMBER)
            noisy = T("Noisy estimate",size=24,color=AMBER).move_to(LEFT*3.5+DOWN*2.65)
            schematic = T("Schematic",size=22,color=SOFT).move_to(RIGHT*4.6+DOWN*2.6)
            signal = Dot(customer.get_center(),color=AMBER)
            self.play(ReplacementTransform(tag,new_tag),ReplacementTransform(caption,new_caption),FadeOut(token),halo.animate.stretch_to_fit_width(9.5),run_time=1)
            tag = new_tag
            caption = new_caption
            self.play(Create(customer),Create(channel),FadeIn(noisy),FadeIn(schematic),FadeIn(signal),run_time=2)
            self.play(MoveAlongPath(signal,channel),run_time=3)
            self.play(halo.animate.stretch_to_fit_width(11),gate_path.animate.set_color(AMBER).set_stroke(width=7),good.animate.set_opacity(0.1),run_time=3)
        with self.beat("s04b05") as b:
            new_tag = Tag("author_interpretation")
            new_caption = T("Accurate uncertainty",size=30).move_to(UP*2.2)
            correction = Arrow(human.get_bottom()+DOWN*0.1,robot.get_bottom()+DOWN*0.1,color=AMBER,buff=0.2)
            correction_label = T("Correction",size=26,color=AMBER).move_to(LEFT*1.6+DOWN*1.2)
            useful_label = T("Useful action",size=26,color=TEAL).move_to(RIGHT*2.6+UP*0.7)
            self.play(ReplacementTransform(tag,new_tag),ReplacementTransform(caption,new_caption),FadeOut(customer),FadeOut(channel),FadeOut(signal),FadeOut(noisy),FadeOut(schematic),FadeOut(bad),FadeOut(self_stop),FadeOut(self_path),FadeOut(mistaken),FadeOut(wait_label),run_time=1.5)
            self.play(halo.animate.stretch_to_fit_width(2).stretch_to_fit_height(1.6).move_to(robot),good.animate.set_opacity(1),direct.animate.set_stroke(opacity=1),gate_path.animate.set_stroke(width=2),run_time=3)
            self.play(GrowArrow(correction),FadeIn(correction_label),FadeIn(useful_label),run_time=2)
            self.play(Indicate(correction,color=AMBER),Indicate(direct,color=TEAL),run_time=2)
