# storyboard: b6c6fd59d4f7cfb8
from aisr_kit import *


def pointer(pos, s=0.22):
    m = Triangle(color=BLUE, fill_color=BLUE, fill_opacity=1).scale(s).rotate(-PI / 2).move_to(pos)
    m.heading = 0.0
    return m


def along(m, path, **kwargs):
    track = path.copy()
    base = m.copy().rotate(-m.heading)

    def update(mob, a):
        a0, a1 = (a, a + 0.004) if a < 0.996 else (a - 0.004, a)
        angle = angle_of_vector(track.point_from_proportion(a1) - track.point_from_proportion(a0))
        mob.become(base.copy().rotate(angle).move_to(track.point_from_proportion(a)))
        mob.heading = angle

    return UpdateFromAlphaFunc(m, update, **kwargs)


def mid_tip(start, end, color, s=0.14, at=0.5):
    start, end = np.array(start, dtype=float), np.array(end, dtype=float)
    tip = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(s)
    return tip.rotate(-PI / 2 + angle_of_vector(end - start)).move_to(start + at * (end - start))


class S03(NarratedScene):
    def construct(self):
        with self.beat("s03b01") as b:
            heading = Heading("How feedback corrects error")
            tag = Tag("definition")
            source = Source("Rosenblueth et al. (1943)")
            machine = Triangle(color=BLUE, fill_color=BLUE, fill_opacity=1).scale(0.25).rotate(-PI / 2).move_to([-4, 0, 0])
            goal = Circle(radius=0.4, color=AMBER).move_to([3.5, 0, 0])
            current_label = T("Current state", size=26).move_to([-4, 0.9, 0])
            goal_label = T("Goal", size=26, color=AMBER).move_to([3.5, 0.9, 0])
            gap = DashedLine(machine.get_center(), goal.get_center(), color=SOFT)
            error_label = T("Error", size=40, color=INK, weight=SEMIBOLD).move_to([0, -0.5, 0])
            feedback = ArcBetweenPoints([3.3, -0.6, 0], [-3.8, -0.6, 0], angle=-PI / 2, color=TEAL).add_tip()
            self.play(FadeIn(heading), FadeIn(tag), FadeIn(source), FadeIn(machine), Create(goal), FadeIn(current_label), FadeIn(goal_label), run_time=1)
            self.play(Create(gap), FadeIn(error_label), Create(feedback), run_time=2)
            self.play(machine.animate.move_to([-1, 0, 0]), Transform(gap, DashedLine([-1, 0, 0], [3.5, 0, 0], color=SOFT)), FadeOut(current_label), run_time=2)
            self.play(machine.animate.move_to([0.8, 0, 0]), Transform(gap, DashedLine([0.8, 0, 0], [3.5, 0, 0], color=SOFT)), run_time=2)
        with self.beat("s03b02") as b:
            movement = T("Movement", size=26).move_to([-4, 1.2, 0])
            correction = T("Correction", size=26, color=BLUE).move_to([0, 1.2, 0])
            signal_label = T("Error signal", size=26, color=TEAL).move_to([0, -2.5, 0])
            pulse = Dot(radius=0.1, color=TEAL)
            self.play(FadeIn(movement), FadeIn(correction), FadeIn(signal_label), run_time=1)
            self.play(machine.animate.move_to([1.8, 0, 0]), Transform(gap, DashedLine([1.8, 0, 0], [3.5, 0, 0], color=SOFT)), run_time=2)
            self.play(MoveAlongPath(pulse, feedback), run_time=2)
            self.play(FadeOut(pulse), machine.animate.move_to([2.5, 0, 0]), Transform(gap, DashedLine([2.5, 0, 0], [3.5, 0, 0], color=SOFT)), Indicate(correction), run_time=2)
        with self.beat("s03b03") as b:
            self.play(FadeOut(VGroup(machine, goal, goal_label, gap, error_label, feedback, movement, correction, signal_label)), run_time=0.7)
            before = T("Before movement", size=28).move_to([-3.7, 2, 0])
            during = T("During movement", size=28).move_to([-3.7, -0.8, 0])
            top_goal = Circle(radius=0.35, color=AMBER).move_to([4, 0.9, 0])
            lower_goal = top_goal.copy().move_to([4, -1.8, 0])
            upper = Triangle(color=BLUE, fill_color=BLUE, fill_opacity=1).scale(0.22).rotate(-PI / 2).move_to([-4, 0.9, 0])
            lower = upper.copy().move_to([-4, -1.8, 0])
            top_path = Line([-4, 0.9, 0], [4, 0.9, 0], color=FAINT)
            low_path = Line([-4, -1.8, 0], [4, -1.8, 0], color=FAINT)
            return_path = ArcBetweenPoints([3.6, -1.9, 0], [-3.7, -1.9, 0], angle=-PI / 3, color=TEAL).add_tip()
            self.play(FadeIn(before), FadeIn(during), Create(top_goal), Create(lower_goal), Create(top_path), Create(low_path), FadeIn(upper), FadeIn(lower), run_time=1.5)
            self.play(upper.animate.move_to([3.6, 0.9, 0]), lower.animate.move_to([-1, -1.8, 0]), run_time=2.5)
            self.play(Create(return_path), run_time=1)
            pulse = Dot(radius=0.1, color=TEAL)
            self.play(MoveAlongPath(pulse, return_path), run_time=2)
            self.play(FadeOut(pulse), lower.animate.move_to([2, -1.8, 0]), run_time=2)
            self.wait(b.duration - 9.7 - 1.3)
            self.play(FadeOut(VGroup(tag, before, during, top_path, low_path, return_path, top_goal, lower_goal, upper, lower)), run_time=0.8)
        with self.beat("s03b04") as b:
            tag = Tag("author_interpretation")
            top_goal = Circle(radius=0.35, color=AMBER).move_to([3.5, 0.45, 0])
            goal_arc = ArcBetweenPoints([3.5, 0.45, 0], [4.5, 1.4, 0], angle=PI / 3)
            goal_trail = DashedVMobject(goal_arc.copy().set_stroke(AMBER, 2, opacity=0.6), num_dashes=10)
            lower_goal = Circle(radius=0.35, color=AMBER).move_to([4, -1.8, 0])
            upper = pointer([-4, 0.6, 0])
            lower = pointer([-4, -1.8, 0])
            self.play(FadeIn(tag), Create(top_goal), Create(lower_goal), FadeIn(upper), FadeIn(lower), run_time=0.7)
            moving = T("Moving goal", size=34, color=AMBER).move_to([4.0, 2.25, 0])
            damped = T("Damped correction", size=34).move_to([-3.5, 2.1, 0])
            overshoot = T("Overshoot", size=34, color=ROSE).move_to([-3.7, -0.6, 0])
            course = VMobject(color=BLUE).set_points_smoothly([[-4, 0.6, 0], [-1, 0.62, 0], [1.5, 0.85, 0], [3.0, 1.2, 0], [3.95, 1.38, 0]])
            reversal = VMobject(color=ROSE, stroke_width=5).set_points_as_corners([[-4, -1.8, 0], [5.5, -1.8, 0], [1, -2.4, 0]])
            reversal_tip = mid_tip([5.5, -1.8, 0], [1, -2.4, 0], ROSE, s=0.2)
            self.play(FadeIn(moving), FadeIn(damped), FadeIn(overshoot), Create(goal_trail), run_time=1)
            self.play(MoveAlongPath(top_goal, goal_arc), Create(course), along(upper, course), run_time=3.5, rate_func=linear)
            self.play(Create(reversal), along(lower, reversal), run_time=4, rate_func=linear)
            self.play(FadeIn(reversal_tip), run_time=0.5)
        with self.beat("s03b05") as b:
            self.play(FadeOut(VGroup(top_goal, goal_trail, lower_goal, upper, lower, moving, damped, overshoot, course, reversal, reversal_tip)), FadeOut(tag), run_time=0.7)
            tag = Tag("hypothesis")
            light_label = T("Light-guided machine", size=34).move_to([-3.3, 2.2, 0])
            grow_label = T("Growing oscillations", size=34, color=ROSE).move_to([3, 2.2, 0])
            points = [[-1.0, 1.1, 0], [1.3, 0.4, 0], [-2.3, -0.4, 0], [3.4, -1.2, 0], [-4.6, -2.1, 0]]
            crossings = [0.8, 0.1, -0.7, -1.6]
            light = VGroup(
                Circle(radius=0.55, stroke_width=0, fill_color=AMBER, fill_opacity=0.15),
                Circle(radius=0.35, color=AMBER, stroke_width=5),
            ).move_to([0, crossings[0], 0])
            start_dot = Circle(radius=0.12, color=SOFT, stroke_width=3).move_to(points[0])
            start_label = T("Start", size=24, color=SOFT).next_to(start_dot, LEFT, buff=0.2)
            mover = pointer(points[0], s=0.24)
            self.play(FadeIn(tag), FadeIn(light_label), FadeIn(grow_label), FadeIn(light), Create(start_dot), FadeIn(start_label), FadeIn(mover), run_time=1)
            trail = VGroup()
            for i, (start, end) in enumerate(zip(points, points[1:])):
                segment = Line(start, end, color=ROSE, stroke_width=3 + i)
                tip = mid_tip(start, end, ROSE, s=0.12 + 0.03 * i, at=0.7)
                trail.add(segment, tip)
                self.play(Create(segment), along(mover, segment), light.animate.move_to([0, crossings[i], 0]), run_time=2.2 + 0.3 * i, rate_func=linear)
                self.add(tip)
                self.bring_to_front(mover)
        with self.beat("s03b06") as b:
            tag_next = Tag("author_interpretation")
            self.remove(tag)
            self.add(tag_next)
            self.play(FadeOut(light_label), FadeOut(grow_label), run_time=0.7)
            tag = tag_next
            missed = VGroup(T("Still goal-directed", size=40, color=INK, weight=SEMIBOLD), T("Missed goal", size=40, color=INK, weight=SEMIBOLD)).arrange(DOWN, buff=0.12).move_to([4.1, -2.95, 0])
            directed = T("Damped correction", size=36, color=INK, weight=SEMIBOLD).move_to([-4.3, 2.1, 0])
            compact_goal = Circle(radius=0.3, color=AMBER).move_to([4.2, 2.1, 0])
            compact = VMobject(color=BLUE).set_points_smoothly([[-1.6, 2.1, 0], [0, 2.32, 0], [1.5, 1.92, 0], [2.7, 2.17, 0], [3.7, 2.1, 0]])
            compact_mover = pointer([-1.6, 2.1, 0], s=0.2)
            loop = ArcBetweenPoints([-0.4, -1.75, 0], [-4.3, -2.35, 0], angle=-PI / 3, color=TEAL).add_tip()
            self.play(FadeIn(missed), Indicate(light, color=AMBER), Create(loop), run_time=2.5)
            self.play(FadeIn(directed), Create(compact_goal), FadeIn(compact_mover), run_time=1)
            self.play(Create(compact), along(compact_mover, compact), run_time=3, rate_func=linear)
