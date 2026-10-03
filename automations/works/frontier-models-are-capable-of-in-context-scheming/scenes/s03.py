# storyboard: 7d62ba9ba506ec5b
from aisr_kit import *

class S03(NarratedScene):
    def construct(self):
        with self.beat("s03b01") as b:
            heading = Heading("The hidden change")
            tag = Tag("method")
            source = Source("Meinke et al. (2024)")
            nodes = VGroup(*[Node(label, color=TEAL, width=2.2, size=24) for label in ["Emails", "Input data", "Scoring code", "Scores"]]).arrange(RIGHT, buff=0.85).move_to(UP * 0.7)
            links = VGroup(*[Link(nodes[i], nodes[i+1], color=TEAL) for i in range(3)])
            token = Square(side_length=0.25, color=TEAL, fill_opacity=1).move_to(nodes[0].get_center()+DOWN*0.85)
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.2), run_time=2)
            self.play(*[GrowArrow(l.arrow) for l in links], FadeIn(token), run_time=1)
            for n in nodes[1:]:
                self.play(token.animate.move_to(n.get_center()+DOWN*0.85), run_time=1.6)
        with self.beat("s03b02") as b:
            returned = T("Returned scores", size=24).move_to([3.8,-0.65,0])
            expected = T("Expected scores", size=24).move_to([3.8,-2.0,0])
            rows = VGroup(*[Line([2.8,-1.1-j*0.18,0],[4.8,-1.1-j*0.18,0],color=TEAL) for j in range(3)])
            lower = rows.copy().shift(DOWN*1.35)
            comparison = VGroup(Line([2.6,-1.1,0],[2.6,-2.45,0],color=TEAL),Line([5,-1.45,0],[5,-2.8,0],color=AMBER))
            agent = Agent(color=SAND).move_to([-2,-1.6,0])
            reply = Node("Explanation", color=SAND, width=2.8, size=24).move_to([0,-1.6,0])
            self.play(FadeOut(token), FadeIn(returned), Create(rows), run_time=1)
            self.play(FadeIn(expected), TransformFromCopy(rows,lower), run_time=2)
            self.play(Create(comparison), FadeIn(agent), FadeIn(reply), run_time=2)
            self.play(Indicate(comparison[1],color=AMBER), Indicate(reply),run_time=2)
        with self.beat("s03b03") as b:
            newtag = Tag("observed_result")
            self.play(ReplacementTransform(tag,newtag), FadeOut(VGroup(returned,expected,rows,lower,comparison,agent,reply)),run_time=1)
            tag = newtag
            altered = Square(side_length=0.36,color=AMBER,fill_opacity=1).rotate(PI/4).move_to(nodes[1].get_center()+DOWN*0.85)
            branch = Arrow(nodes[0].get_center()+DOWN*1.9,altered.get_center(),color=AMBER,buff=0.2)
            label = T("Changed input",size=26,color=AMBER).move_to([-2.6,-2.4,0])
            self.play(GrowArrow(branch),FadeIn(altered),FadeIn(label),run_time=2)
            self.play(altered.animate.move_to(nodes[2].get_center()+DOWN*0.85),run_time=2)
            self.play(FadeOut(branch),FadeOut(altered),FadeOut(label),run_time=1)
            bypass = ArcBetweenPoints(nodes[1].get_center()+DOWN*0.7,nodes[3].get_center()+DOWN*0.7,angle=PI/3,color=AMBER).add_tip()
            replacement = T("Replaced ranking",size=26,color=AMBER).move_to([1.7,-2.4,0])
            self.play(Create(bypass),FadeIn(replacement),run_time=2)
            self.play(nodes[3].box.animate.set_stroke(AMBER),run_time=1)
        with self.beat("s03b04") as b:
            newtag = Tag("author_interpretation")
            miniature = VGroup(nodes,links,bypass,replacement)
            self.play(ReplacementTransform(tag,newtag),miniature.animate.scale(0.48).move_to([-3.3,0.3,0]),run_time=2)
            tag=newtag
            data=self.dataset("d1")
            chart=BarChart(data["points"],colors=[AMBER],width=3.2,height=2.6,max_value=100,unit=data["unit"],label_size=22).move_to([3.2,0.1,0])
            chart.frame[-1].shift(DOWN*0.55)
            title=T("False rankings",size=28).move_to([3.2,2.1,0])
            nudge=T("Strong goal nudge",size=24,color=SOFT).move_to([3.2,-2.3,0])
            outline=RoundedRectangle(width=5.4,height=2.1,corner_radius=0.16,color=VIOLET).move_to([-3.3,-0.1,0])
            interpretation=T("Authors’ interpretation",size=24,color=VIOLET).move_to([-3.3,-1.7,0])
            self.play(FadeIn(chart.frame),FadeIn(title),FadeIn(nudge),FadeOut(replacement),*[n.label.animate.set_opacity(0) for n in nodes],run_time=1)
            scale_top=DashedLine(chart.baseline.get_start()+UP*2.6,chart.baseline.get_end()+UP*2.6,color=FAINT)
            scale_labels=VGroup(T("100%",size=22,color=SOFT).move_to(chart.baseline.get_end()+UP*2.6+RIGHT*0.5),T("0%",size=22,color=SOFT).move_to(chart.baseline.get_end()+RIGHT*0.5))
            self.play(bars_grow(chart),Create(scale_top),FadeIn(scale_labels),run_time=2)
            self.play(FadeIn(chart.values),Create(outline),FadeIn(interpretation),run_time=2)
        with self.beat("s03b05") as b:
            enclosure=RoundedRectangle(width=12.1,height=4.9,corner_radius=0.16,color=FAINT).move_to([0,-0.1,0])
            eval_label=T("Constructed evaluation",size=24,color=SOFT).move_to([0,2.55,0])
            changed=T("Observed change",size=24,color=AMBER).move_to([-3.3,1.7,0])
            newinterp=T("Interpretation",size=24,color=VIOLET).move_to(interpretation)
            inbox=VGroup(RoundedRectangle(width=0.9,height=0.48,corner_radius=0.05,color=MUTED),Line([-0.45,0.24,0],[0,-0.04,0],color=MUTED),Line([0,-0.04,0],[0.45,0.24,0],color=MUTED)).move_to([-5.4,-3.05,0]).set_opacity(0.45)
            self.play(Create(enclosure),FadeIn(eval_label),FadeIn(changed),FadeIn(inbox),ReplacementTransform(interpretation,newinterp),run_time=2)
            self.play(Indicate(nodes[3].box,color=AMBER),Indicate(outline,color=VIOLET),run_time=2)
        with self.beat("s03b06") as b:
            newtag=Tag("method")
            version=Node("Pre-deployment o1",color=SAND,width=3.7,size=24).move_to([0,-3.05,0])
            conditions=T("Test conditions",size=24,color=SAND).move_to([-3.4,-2.25,0])
            connection=Line(version.get_top(),chart.baseline.get_start(),color=SAND)
            self.play(ReplacementTransform(tag,newtag),FadeIn(version),FadeIn(conditions),Create(connection),run_time=2)
            self.play(Indicate(version,color=SAND),Indicate(chart.values,color=SAND),run_time=2)
