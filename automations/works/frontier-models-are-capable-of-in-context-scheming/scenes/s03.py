# storyboard: 7d62ba9ba506ec5b
from aisr_kit import *

def clear_at_end(scene, start, b, mobjects, run_time=0.4):
    # Fade out state that belongs only to this beat so the next beat opens on its own visuals.
    left = b.duration - run_time - (scene.renderer.time - start)
    if left > 0:
        scene.wait(left)
    scene.play(FadeOut(*mobjects), run_time=run_time)

class S03(NarratedScene):
    def construct(self):
        with self.beat("s03b01") as b:
            heading = Heading("The hidden change")
            tag = Tag("method")
            source = Source("Meinke et al. (2024)")
            nodes = VGroup(*[Node(label, color=TEAL, width=2.5, size=28) for label in ["Emails", "Input data", "Scoring code", "Scores"]]).arrange(RIGHT, buff=0.75).move_to(UP * 0.7)
            links = VGroup(*[Link(nodes[i], nodes[i+1], color=TEAL) for i in range(3)])
            token = Square(side_length=0.25, color=TEAL, fill_opacity=1).move_to(nodes[0].get_center()+DOWN*0.85)
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.2), run_time=2)
            self.play(*[GrowArrow(l.arrow) for l in links], FadeIn(token), run_time=1)
            for n in nodes[1:]:
                self.play(token.animate.move_to(n.get_center()+DOWN*0.85), run_time=1.6)
        with self.beat("s03b02") as b:
            start = self.renderer.time
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
            clear_at_end(self, start, b, [returned,expected,rows,lower,comparison,agent,reply])
        with self.beat("s03b03") as b:
            newtag = Tag("observed_result")
            self.play(FadeOut(tag), run_time=0.3)
            self.play(FadeIn(newtag), run_time=0.3)
            tag = newtag
            altered = Square(side_length=0.36,color=AMBER,fill_opacity=1).rotate(PI/4).move_to(nodes[1].get_center()+DOWN*0.85)
            branch = Arrow(nodes[0].get_center()+DOWN*1.9,altered.get_center(),color=AMBER,buff=0.2)
            label = T("Changed input",size=34,color=AMBER).move_to([-2.6,-2.4,0])
            self.play(GrowArrow(branch),FadeIn(altered),FadeIn(label),run_time=2)
            self.play(altered.animate.move_to(nodes[2].get_center()+DOWN*0.85),run_time=2)
            self.play(FadeOut(branch),FadeOut(altered),FadeOut(label),run_time=1)
            token = Square(side_length=0.25, color=TEAL, fill_opacity=1).move_to(nodes[1].get_center()+DOWN*0.85)
            self.play(FadeIn(token), run_time=0.4)
            self.play(token.animate.move_to(nodes[2].get_center()+DOWN*0.85), run_time=1)
            self.play(token.animate.move_to(nodes[3].get_center()+DOWN*0.85), run_time=1)
            overwrite = Arrow(nodes[3].get_center()+DOWN*2.0, nodes[3].get_bottom()+DOWN*0.08, color=AMBER, buff=0)
            replacement = T("Replaced ranking",size=34,color=AMBER).move_to([nodes[3].get_x()-0.3,-2.4,0])
            self.play(GrowArrow(overwrite),FadeOut(token),FadeIn(replacement),run_time=2)
            self.play(nodes[3].box.animate.set_stroke(AMBER),run_time=1)
        with self.beat("s03b04") as b:
            newtag = Tag("author_interpretation")
            self.play(FadeOut(tag),FadeOut(overwrite),FadeOut(replacement),run_time=0.4)
            self.play(FadeIn(newtag),run_time=0.4)
            tag=newtag
            # Re-stack the same pipeline as a labelled column on the left.
            column_x, ys = -1.8, [2.05, 1.0, -0.05, -1.1]
            self.play(FadeOut(links),*[n.animate.scale(0.85).move_to([n.get_x(),y,0]) for n,y in zip(nodes,ys)],run_time=0.75)
            self.play(*[n.animate.set_x(column_x) for n in nodes],run_time=0.75)
            down_links = VGroup(*[Arrow(nodes[i].get_bottom(),nodes[i+1].get_top(),color=TEAL,buff=0.04,stroke_width=3,max_tip_length_to_length_ratio=0.5,tip_length=0.12) for i in range(3)])
            self.play(*[GrowArrow(a) for a in down_links],run_time=0.6)
            in_mark = Square(side_length=0.26,color=AMBER,fill_opacity=1).rotate(PI/4).next_to(nodes[1],LEFT,buff=0.2)
            out_mark = Square(side_length=0.26,color=AMBER,fill_opacity=1).rotate(PI/4).next_to(nodes[3],LEFT,buff=0.2)
            in_label = T("Changed input",size=26,color=AMBER).next_to(in_mark,LEFT,buff=0.2)
            out_label = T("Replaced ranking",size=26,color=AMBER).next_to(out_mark,LEFT,buff=0.2)
            self.play(nodes[1].box.animate.set_stroke(AMBER),FadeIn(in_mark),FadeIn(in_label),FadeIn(out_mark),FadeIn(out_label),run_time=1)
            data=self.dataset("d1")
            chart=BarChart(data["points"],colors=[AMBER],width=3.2,height=2.6,max_value=100,unit=data["unit"],label_size=32)
            chart.shift(np.array([3.3,-1.3,0])-chart.baseline.get_center())
            scale_top=DashedLine(chart.baseline.get_start()+UP*2.6,chart.baseline.get_end()+UP*2.6,color=FAINT)
            chart.unit.set_color(SOFT).next_to(scale_top,UP,buff=0.22).set_x(chart.baseline.get_x())
            title=T("False rankings",size=30,color=INK).next_to(chart.unit,UP,buff=0.18)
            nudge=T("Strong goal nudge",size=30,color=INK).next_to(chart.labels,DOWN,buff=0.15)
            altered=VGroup(nodes[1],nodes[2],nodes[3],in_mark,out_mark,in_label,out_label)
            outline=SurroundingRectangle(altered,color=VIOLET,buff=0.2,corner_radius=0.16)
            interpretation=T("Authors’ interpretation",size=30,color=INK).next_to(outline,DOWN,buff=0.22)
            self.play(FadeIn(chart.frame),FadeIn(title),FadeIn(nudge),run_time=1)
            scale_labels=VGroup(T("100%",size=28,color=INK).next_to(scale_top,RIGHT,buff=0.15),T("0%",size=28,color=INK).next_to(chart.baseline,RIGHT,buff=0.15))
            self.play(bars_grow(chart),Create(scale_top),FadeIn(scale_labels),run_time=2)
            self.play(FadeIn(chart.values),Create(outline),FadeIn(interpretation),run_time=2)
        with self.beat("s03b05") as b:
            start = self.renderer.time
            enclosure=RoundedRectangle(width=12.5,height=5.7,corner_radius=0.16,color=FAINT).move_to([0,-0.05,0])
            eval_label=T("Constructed evaluation",size=24,color=SOFT).move_to([0,3.05,0])
            changed=T("Observed change",size=24,color=AMBER).next_to(altered,UP,buff=0.25).set_x(in_label.get_x())
            inbox=VGroup(RoundedRectangle(width=0.9,height=0.48,corner_radius=0.05,color=MUTED),Line([-0.45,0.24,0],[0,-0.04,0],color=MUTED),Line([0,-0.04,0],[0.45,0.24,0],color=MUTED)).move_to([5.9,-3.35,0]).set_opacity(0.45)
            self.play(Create(enclosure),FadeIn(eval_label),FadeIn(changed),FadeIn(inbox),run_time=2)
            self.play(Indicate(in_mark,color=AMBER),Indicate(out_mark,color=AMBER),Indicate(outline,color=VIOLET),run_time=2)
            clear_at_end(self, start, b, [enclosure,eval_label,changed,inbox])
        with self.beat("s03b06") as b:
            newtag=Tag("method")
            version=Node("Pre-deployment o1",color=SAND,height=0.8,size=30).move_to([3.3,-3.15,0])
            conditions=T("Test conditions",size=30,color=INK,weight=MEDIUM).next_to(version,LEFT,buff=0.7)
            connection=Line(conditions.get_right()+RIGHT*0.1,version.get_left()+LEFT*0.1,color=SAND,stroke_width=3)
            self.play(FadeOut(tag),run_time=0.3)
            self.play(FadeIn(newtag),FadeIn(version),FadeIn(conditions),Create(connection),run_time=2)
            self.play(Indicate(version,color=SAND),Indicate(chart.bars,color=SAND),Indicate(chart.values,color=SAND),Indicate(nudge,color=SAND),run_time=2)
