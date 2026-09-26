# storyboard: 33af23efe0bb04ff
from aisr_kit import *

class Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = BG
        title=Serif("Which goal?",size=92,color=INK).move_to([0,2.7,0])
        agent=Agent(color=TEAL,radius=0.37).move_to([-4,-0.7,0])
        gold=Circle(radius=0.42).set_fill(AMBER,1).set_stroke(SAND,3).move_to([3.2,0.7,0])
        wall=Rectangle(width=0.3,height=2.5).set_fill(GRAY,0.6).set_stroke(GRAY,2).move_to([4.4,-1.4,0])
        goal=VMobject().set_points_as_corners([[-3.6,-0.65,0],[-1.0,0.0,0],[2.8,0.7,0]]).set_stroke(AMBER,7)
        proxy=VMobject().set_points_as_corners([[-3.6,-0.75,0],[-0.8,-1.5,0],[4.0,-1.5,0]]).set_stroke(ROSE,7)
        proxy=DashedVMobject(proxy,num_dashes=18)
        left=T("coin",size=35,color=AMBER).move_to([2.1,1.5,0])
        right=T("end wall",size=35,color=ROSE).move_to([3.2,-2.5,0])
        self.add(title,goal,proxy,agent,gold,wall,left,right)
