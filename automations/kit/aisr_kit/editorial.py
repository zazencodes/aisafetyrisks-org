"""Reusable, source-bounded diagrams for the pilot's general-audience explainer."""

import numpy as np
from manim import *

from aisr_kit.components import Agent, Heading, Panel, Source, T, Tag
from aisr_kit.style import AMBER, BG, BLUE, FAINT, GRAY, INK, MUTED, ROSE, SOFT, TEAL


def label(value, x, y, color=INK, size=28):
    return T(value, size=size, color=color).move_to([x, y, 0])


def route(points, color=TEAL, dashed=False):
    path = VMobject().set_points_as_corners([np.array([x, y, 0]) for x, y in points])
    path.set_stroke(color, 5)
    result = DashedVMobject(path, num_dashes=20) if dashed else path
    result.editorial_route = True
    return result


def box(x, y, w, h, color):
    return RoundedRectangle(corner_radius=0.16, width=w, height=h).set_stroke(color, 2).set_fill(BG, 1).move_to([x, y, 0])


def coin(x, y):
    return Circle(radius=0.16).set_fill(AMBER, 1).set_stroke(AMBER, 2).move_to([x, y, 0])


def warehouse(stage):
    if stage == 2:
        g=VGroup(box(-3.3,0,5.3,3.3,GRAY),box(3.3,0,5.3,3.3,BLUE))
        g.add(label('Hypothetical',-3.3,-2.0,ROSE,25),label('Paper: modified games',3.3,-2.0,TEAL,25))
        g.add(label('warehouse',-3.3,1.0,SOFT,28),label('CoinRun',3.3,1.0,TEAL,28))
        g.add(Agent(color=TEAL,radius=0.2).move_to([-4.2,-0.5,0]),box(-2.2,-0.5,0.85,0.65,MUTED))
        g.add(Line([1.3,-0.65,0],[5.2,-0.65,0]).set_stroke(GRAY,2),Agent(color=TEAL,radius=0.17).move_to([1.65,-0.4,0]),coin(4.7,-0.4))
        g.add(Line([0,-1.75,0],[0,1.75,0]).set_stroke(FAINT,2))
        return g
    g = VGroup()
    g.add(box(-4.2, 0.25, 3.2, 3.3, BLUE), label('request', -4.2, 1.45, BLUE, 25))
    g.add(box(2.8, 0.25, 5.6, 3.3, ORANGE), label('warehouse', 2.8, 1.45, ORANGE, 25))
    a = Agent(color=TEAL, radius=0.23).move_to([0.55, -0.65, 0])
    old = box(2.3, 0.3, 1.3, 0.9, MUTED)
    new = box(4.45, 0.3, 1.3, 0.9, AMBER)
    g.add(a, old, new, label('familiar bay', 2.3, -0.4, SOFT, 22))
    g.add(label('Hypothetical warehouse',-3.0,-2.25,ROSE,26))
    if stage == 0:
        g.add(label('requested parcel', -4.2, 0.2, INK, 25), coin(-4.2, -0.65), route([(0.65,-0.6),(2.3,-0.6),(2.3,-0.12)]))
    elif stage == 1:
        g.add(label('new request', -4.2, 0.2, INK, 25), coin(-4.2, -0.65), route([(0.65,-0.6),(2.3,-0.6),(2.3,-0.12)], ROSE, True), route([(0.65,-0.6),(4.45,-0.6),(4.45,-0.12)], AMBER))
        g.add(label('Which rule?', 3.0, -2.15, INK, 37))
    return g


def game_panel(cx, name, color, moved=False, path=False, stuck=False):
    g=VGroup(box(cx,0.0,5.6,3.3,color),label(name,cx,1.85,color,28))
    left=cx-2.4; right=cx+2.4; ground=-0.8
    g.add(Line([left,ground,0],[right,ground,0]).set_stroke(GRAY,3))
    for dx,h in [(-1.35,0.55),(0.0,0.7),(1.15,0.5)]:
        g.add(Rectangle(width=0.4,height=h).set_fill(GRAY,0.5).set_stroke(GRAY,1).move_to([cx+dx,ground+h/2,0]))
    g.add(Rectangle(width=0.18,height=1.5).set_fill(GRAY,0.65).set_stroke(GRAY,1).move_to([right-0.1,ground+0.75,0]))
    if moved:
        g.add(Rectangle(width=0.45,height=0.08).set_fill(GRAY,0.5).set_stroke(GRAY,1).move_to([cx+0.1,0.67,0]))
    g.add(coin(cx+(0.1 if moved else 2.0), (0.9 if moved else ground+0.25)))
    if path:
        g.add(route([(left+0.2,ground+0.3),(cx-1.35,0.2),(cx-0.85,ground+0.3),(cx,0.3),(cx+0.4,ground+0.3),(cx+1.15,0.1),(right-0.35,ground+0.3)]))
        g.add(Agent(color=TEAL,radius=0.18).move_to([right-0.35,ground+0.3,0]))
    elif stuck:
        g.add(route([(left+0.2,ground+0.3),(cx-1.65,ground+0.3),(cx-1.5,ground+0.4)],GRAY))
        g.add(Agent(color=GRAY,radius=0.18).move_to([cx-1.5,ground+0.4,0]))
    else:
        g.add(Agent(color=TEAL,radius=0.18).move_to([left+0.2,ground+0.3,0]))
    return g


def coinrun(stage):
    g=VGroup()
    if stage==0:
        g.add(game_panel(0,'Training',BLUE))
        g.add(label('coin',2.0,-2.15,AMBER,24),label('end wall',3.1,0.9,SOFT,22))
    elif stage==1:
        g.add(game_panel(-3.05,'Training',BLUE),game_panel(3.05,'Test',ORANGE,moved=True))
        g.add(label('coin moved',3.05,-2.2,AMBER,25))
    elif stage==2:
        g.add(game_panel(-3.05,'capability failure',GRAY,moved=True,stuck=True),game_panel(3.05,'capable route',ORANGE,moved=True,path=True))
        g.add(label('missed coin',3.05,-2.2,AMBER,26))
    else:
        g.add(game_panel(-3.05,'Training',BLUE),game_panel(3.05,'Test',ORANGE,moved=True,path=True))
        g.add(label('reach coin',-2.0,-2.25,AMBER,25),label('move right?',3.0,-2.25,ROSE,25))
        g.add(route([(-5.0,-1.2),(-1.15,-1.2)],ROSE,True),route([(0.85,-1.2),(5.2,-1.2)],ROSE,True))
    return g


def mechanism(stage):
    if stage==0:
        g=coinrun(3)
        g.add(label('Same direction in training',-3.0,2.35,SOFT,25),label('Different directions at test',3.0,2.35,SOFT,25))
        return g
    if stage==1:
        g=VGroup(game_panel(-3.05,'stuck',GRAY,moved=True,stuck=True),game_panel(3.05,'capable, wrong destination',ORANGE,moved=True,path=True))
        return g
    if stage==2:
        g=coinrun(3)
        g.add(label('reward: coin',0,-2.7,AMBER,27))
        return g
    g=VGroup(coin(-2.2,0),label('coin',-2.2,-0.5,AMBER,27),label('Another kind of shortcut',0,2.0,SOFT,30))
    g.add(Rectangle(width=0.34,height=0.75).set_fill(AMBER,0.5).set_stroke(AMBER,2).move_to([2.2,0,0]),label('key',2.2,-0.65,AMBER,27))
    g.add(Arrow([-1.5,0,0],[1.5,0,0],color=SOFT))
    return g


def key_shape(x,y):
    return VGroup(Circle(radius=0.12).set_stroke(AMBER,3).move_to([x,y,0]),Line([x+0.12,y,0],[x+0.55,y,0]).set_stroke(AMBER,3),Line([x+0.42,y,0],[x+0.42,y-0.15,0]).set_stroke(AMBER,3))


def chest_shape(x,y):
    return VGroup(Rectangle(width=0.7,height=0.5).set_stroke(AMBER,2).set_fill(AMBER,0.12).move_to([x,y,0]),Line([x-0.3,y+0.05,0],[x+0.3,y+0.05,0]).set_stroke(AMBER,2))


def keys(stage):
    g=VGroup(box(0,0,11.5,3.5,BLUE if stage==0 else ORANGE),label('Training' if stage==0 else 'Test',-4.7,1.85,BLUE if stage==0 else ORANGE,28))
    g.add(Agent(color=TEAL,radius=0.22).move_to([-4,-0.85,0]))
    positions=[(-2.8,-0.1),(-1.4,0.75),(0,-0.5),(1.4,0.7),(2.8,-0.25)]
    for x,y in positions[:2 if stage==0 else 5]:g.add(key_shape(x,y))
    for x,y in [(1.2,-0.9),(3,-0.9),(4,0.85)][:4 if stage==0 else 2]:g.add(chest_shape(x,y))
    if stage>=1:g.add(route([(-4,-0.85),(-2.8,-0.1),(-1.4,0.75),(0,-0.5),(1.4,0.7),(2.8,-0.25)],TEAL))
    if stage==0:g.add(label('reward: open chests',0,-2.4,AMBER,28))
    elif stage==1:g.add(label('extra keys',-1.8,-2.4,ROSE,26),label('chests still closed',2.7,-2.4,AMBER,26))
    else:
        g.add(label('collect keys?',-2,-2.4,ROSE,26),label('open chests',2.7,-2.4,AMBER,26))
        g.add(route([(-4,-0.85),(-2.8,-0.1),(-1.4,0.75),(0,-0.5)],ROSE,True))
    return g


def diversity(stage):
    if stage==1:
        g=VGroup(label('CoinRun training levels',0,2.25,BLUE,28))
        for row in range(5):
            for col in range(10):
                cell=Rectangle(width=0.65,height=0.4).set_stroke(BLUE,1).set_fill(BLUE,0.13).move_to([-3.45+col*0.77,1.45-row*0.53,0])
                if row==2 and col==4:cell.set_stroke(AMBER,3).set_fill(AMBER,0.5)
                g.add(cell)
        g.add(label('2% of training levels',0,-1.9,AMBER,31),label('CoinRun result',0,-2.55,SOFT,25))
        return g
    if stage==2:
        g=VGroup()
        for cx,size in [(-3.1,1.0),(3.1,1.8)]:
            g.add(box(cx,0.25,5.3,3.1,BLUE),label('Training maze',cx,2.1,BLUE,25))
            g.add(Rectangle(width=size,height=size).set_stroke(ROSE,2).set_fill(ROSE,0.08).move_to([cx+0.85,0.6,0]))
            g.add(coin(cx+0.85,0.8),Agent(color=TEAL,radius=0.18).move_to([cx-1.65,-0.8,0]))
            g.add(route([(cx-1.65,-0.8),(cx+0.85,0.8)],ROSE,True))
        g.add(label('Location cue persists',0,-2.1,ROSE,29),label('Open question',0,-2.7,SOFT,24))
        return g
    g=VGroup()
    for i,cx in enumerate([-3.7,0,3.7]):
        moved=i==1
        g.add(box(cx,0.3,3.1,2.3,BLUE),label('Training',cx,1.75,BLUE,24))
        g.add(Line([cx-1.2,-0.25,0],[cx+1.2,-0.25,0]).set_stroke(GRAY,2),Agent(color=TEAL,radius=0.15).move_to([cx-1,-0.02,0]),coin(cx+(0 if moved else 0.95),0.0))
        if moved:g.add(route([(cx-1,-0.05),(cx,0)],AMBER))
        else:g.add(route([(cx-1,-0.05),(cx+0.95,0)],ROSE,True))
    if stage==0:g.add(label('coin moves',0,-1.85,AMBER,29),label('Training variety',0,-2.5,SOFT,25))
    return g


def closing(stage):
    if stage==0:
        g=VGroup(label('capable + wrong goal',0,1.9,TEAL,35),Agent(color=TEAL,radius=0.28).move_to([-4,-0.25,0]),coin(3.9,1.0))
        g.add(route([(-4,-0.25),(-1,-0.25),(2.9,-1.1)],TEAL),box(3,-1.1,1.5,0.9,ROSE),label('possible harm',3,-2.0,ROSE,26))
        return g
    if stage==1:
        g=VGroup(box(-3,0,5.5,3.4,BLUE),box(3,0,5.5,3.4,GRAY))
        g.add(label('Observed: modified games',-3,1.05,TEAL,27),label('Hypothesis: specific proxies',-3,-0.2,ROSE,25),label('Warehouse: analogy',3,0.45,SOFT,28))
        return g
    g=VGroup(label('When cues part ways,',0,1.15,INK,41),label('what does it follow?',0,0.3,INK,41))
    g.add(Agent(color=TEAL,radius=0.24).move_to([-3,-1.25,0]),coin(2.7,-0.8),route([(-2.7,-1.25),(2.5,-0.85)],AMBER),route([(-2.7,-1.25),(2.5,-2.0)],ROSE,True))
    return g


def show(scene, title, kind, mode, stage):
    old=getattr(scene,'_editorial',None)
    if old is not None:scene.play(FadeOut(old),run_time=0.35)
    maker={'warehouse':warehouse,'coinrun':coinrun,'mechanism':mechanism,'keys':keys,'diversity':diversity,'closing':closing}[mode]
    diagram=maker(stage)
    citation='Illustrative scenario' if mode=='warehouse' and stage<2 else scene.paper['short']
    furniture=VGroup(Heading(title),Tag(kind),Source(citation))
    group=VGroup(diagram,furniture)
    scene.play(FadeIn(group),run_time=0.7)
    paths=[part for part in diagram.get_family() if getattr(part,'editorial_route',False)]
    if paths:
        scene.play(*[ShowPassingFlash(path.copy(),time_width=0.35) for path in paths[:2]],run_time=1.1)
    scene._editorial=group
