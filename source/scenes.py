from lib import *
from comp import *
from hero import house
from anim import sway, drift, bat, smoke
from figures import deck_woman, sitting_cat
import math
import os as _os
_HERE=_os.path.dirname(_os.path.abspath(__file__))
_SITE=_os.environ.get('SNAP_SITE') or (_os.path.join(_HERE,'..','site') if _os.path.isdir(_os.path.join(_HERE,'..','site')) else _os.path.join(_HERE,'..'))
OUT=_os.path.join(_SITE,'svg')+'/'
def _anim(tag,attr,vals,dur,begin,extra=''):
    return f'<animate attributeName="{attr}" values="{vals}" dur="{dur}s" begin="-{begin}s" repeatCount="indefinite"{extra}/>'

def night_sky(s):
    glow=s.rg('wmoonglow',[(0,'#ffffff',.55),(.35,'#ffffff',.2),(1,'#ffffff',0)])
    o='<g transform="translate(105 -26)">'
    o+=f'<circle cx="430" cy="104" r="84" fill="{glow}"/>'
    o+='<path d="M430 62A44 44 0 1 0 430 150A64 64 0 0 1 430 62Z" fill="#ffffff"/>'
    o+='</g>'
    stars=[(60,40,2.8),(130,110,2),(190,50,3.2),(250,130,2.2),(310,36,2.6),(350,96,2),(520,40,3),(540,130,2.2),(110,190,2.4),(220,22,2),(500,92,1.8),(40,120,2.6),(570,24,2.4),(300,172,2),(160,160,1.8),(590,86,2)]
    for i,(x,y,r) in enumerate(stars):
        a=_anim('c','opacity','.25;1;.25',2.4+i%4*.7,i*.9) if i%2==0 else ''
        o+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" opacity=".9">{a}</circle>'
    return o

def fireflies(s):
    g=s.rg('wfirefly',[(0,'#fff6a8',1),(.35,'#ffe35a',.55),(1,'#ffd23a',0)])
    pts=[(180,300,0),(300,250,1),(470,330,2),(610,260,3),(720,300,4),(900,360,5),(1010,300,6),(260,380,7)]
    o=''
    for x,y,i in pts:
        dx,dy=14+i%3*6,-8-i%2*8
        d=3.2+i%3*.8
        o+=(f'<g><circle cx="{x}" cy="{y}" r="16" fill="{g}"/><circle cx="{x}" cy="{y}" r="3" fill="#fffbd0"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx} {dy};{-dx//2} {dy*2};0 0" dur="{d+4}s" begin="-{i*1.3}s" repeatCount="indefinite"/>'
            f'{_anim("g","opacity",".15;1;.2",d,i*.7)}</g>')
    return o

def jack(cx,by):
    return f'<g transform="translate({cx} {by}) scale(1.7) translate({-cx} {-by})">'+_jack(cx,by)+'</g>'

def _jack(cx,by):
    o=f'<ellipse cx="{cx}" cy="{by-26}" rx="50" ry="42" fill="#ffb23a" opacity=".13"/>'
    o+=f'<ellipse cx="{cx}" cy="{by+1}" rx="30" ry="5" fill="#000" opacity=".3"/>'
    o+=f'<ellipse cx="{cx-14}" cy="{by-22}" rx="17" ry="21" fill="#d9701a"/><ellipse cx="{cx+14}" cy="{by-22}" rx="17" ry="21" fill="#d9701a"/>'
    o+=f'<ellipse cx="{cx}" cy="{by-22}" rx="19" ry="23" fill="#f08a24"/>'
    o+=f'<path d="M{cx} {by-44}V{by-2}" stroke="#c4601a" stroke-width="1.6" fill="none"/>'
    o+=f'<path d="M{cx-1} {by-44}C{cx-2} {by-52} {cx+2} {by-56} {cx+7} {by-58}L{cx+9} {by-54}C{cx+5} {by-52} {cx+5} {by-48} {cx+5} {by-44}Z" fill="#4a7a2a"/>'
    face='#ffd24a'
    o+=f'<path d="M{cx-12} {by-30}L{cx-4} {by-30}L{cx-8} {by-38}Z" fill="{face}"/><path d="M{cx+12} {by-30}L{cx+4} {by-30}L{cx+8} {by-38}Z" fill="{face}"/>'
    o+=f'<path d="M{cx-14} {by-17}L{cx-8} {by-12}L{cx-4} {by-16}L{cx} {by-12}L{cx+4} {by-16}L{cx+8} {by-12}L{cx+14} {by-17}L{cx+12} {by-9}C{cx+6} {by-4} {cx-6} {by-4} {cx-12} {by-9}Z" fill="{face}"/>'
    return o

def why_scene():
    s=S(1504,512)
    s.add(night_sky(s))
    g1=s.lg('wg1',[(0,'#8cc23a'),(1,'#5f9f2a')],0,150,0,512,1)
    crest=[(0,236),(90,200),(167,172),(300,160),(417,158),(520,166),(590,186),(667,250),(733,314),(800,330),(867,336),(1067,344),(1167,372),(1504,392)]
    s.p(smooth(crest,False)+'L1504 512L0 512Z',g1)
    s.p(smooth([(0,330),(120,360),(240,420),(330,512)],False)+'L0 512Z','#a9c94a',opacity=.55)
    s.p(smooth([(0,300),(200,330),(380,360),(560,400),(800,430),(1100,440),(1504,430)],False)+'L1504 512L0 512Z','#7bb135',opacity=.45)
    s.p('M540 392C620 380 700 384 760 400C690 410 600 410 540 392Z','#5e9a2c',opacity=.6)
    s.p('M300 392C380 380 470 384 540 396C470 408 380 406 300 392Z','#5e9a2c',opacity=.5)
    # bush right: stepped layered silhouette + heart leaves
    def sil(pts,fill,op=1):
        pts=[p for p in pts if p[0]<=1540]
        s.p(scallop(pts,512,0.56),fill,opacity=op)
    O=[(1024,414),(1086,370),(1150,326),(1220,282),(1262,214),(1322,180),(1380,132),(1420,82),(1490,58),(1540,70)]
    sil(O,s.lg('wb0',[(0,'#9ad04a'),(1,'#5aa83a')],0,60,0,420,1))
    sil([(x+18,y+22) for x,y in O],s.lg('wb1',[(0,'#4fae4a'),(1,'#2f8a48')],0,70,0,420,1))
    sil([(x+46,y+58) for x,y in O],s.lg('wb2',[(0,'#2f8a48'),(.6,'#1f6f5a'),(1,'#15566a')],1100,100,1504,450,1))
    sil([(x+110,y+120) for x,y in O],'#1a5f60',.7)
    sil([(x+190,y+180) for x,y in O],'#15506a',.7)
    def heart(cx,cy,r,a):
        import math
        c,sn=math.cos(math.radians(a)),math.sin(math.radians(a))
        T=lambda x,y:(cx+x*c-y*sn, cy+x*sn+y*c)
        pts=[(0,-r*1.0),(r*.6,-r*.6),(r*1.05,0),(r*.8,r*.62),(r*.2,r*.9),(0,r*.72),(-r*.2,r*.9),(-r*.8,r*.62),(-r*1.05,0),(-r*.6,-r*.6)]
        # local: tip at top; rotate
        P=[T(x,-y) for x,y in pts]
        sh=[(x+r*.12,y+r*.18) for x,y in P]
        o=f'<path d="{smooth(sh,True)}" fill="#2a6f45" opacity=".7"/>'
        o+=f'<path d="{smooth(P,True)}" fill="#8cc95a"/>'
        half=[T(0,-r*1.05),T(r*.55,-r*.55),T(r*.95,0),T(r*.7,r*.6),T(r*.15,r*.95),T(0,r*.75)]
        o+=f'<path d="{smooth(half,False)}Z" fill="#9bd463"/>'
        m0=T(0,r*.7); m1=T(r*.1,0); m2=T(-r*.05,-r*.8)
        o+=f'<path d="M{f(m0[0])} {f(m0[1])}Q{f(m1[0])} {f(m1[1])} {f(m2[0])} {f(m2[1])}" fill="none" stroke="#6fae45" stroke-width="2.4" stroke-linecap="round"/>'
        return o
    for cx,cy,r,a in [(1366,195,28,235),(1452,200,32,240),(1292,282,40,230),(1398,286,46,236),(1320,352,40,228)]:
        s.add(heart(cx,cy,r,a))
    s.p(smooth([(900,430),(1000,414),(1100,406),(1260,414),(1504,424)],False)+'L1504 512L900 512Z',g1)
    # left plant
    L=''
    L+=bigleaf(10,340,270,46,-86,0.06,'#2b8a4a','#55b05a','#1d6b38')
    L+=bigleaf(40,350,200,36,-55,0.12,'#3fa354','#68c264','#24793e')
    L+=bigleaf(0,360,190,32,-30,0.1,'#2a8445','#4caf5a','#1d6b38')
    L+=bigleaf(130,360,170,28,-150,-0.1,'#1f7a43','#3d9a52','#145c32')
    s.add(sway(L,60,360,1.2,6.2,-1))
    s.add(sway(budstem([(80,330),(90,220),(110,110),(130,10),(140,-40)],[(0.8,-160,'p',40),(1.3,-20,'o',38),(1.9,-160,'p',38),(2.3,-20,'o',34),(2.9,-150,'p',34),(3.3,-40,'p',30),(3.8,-100,'o',28)],2),80,330,1.8,5,-2))
    s.add(sway(fan2(s,80,404,96,17,'#e6dc58','#2f8a3a',w=0.15),80,404,1.4,4.6,-.6))
    s.add(sway(grassfan(40,410,9,80,-170,-110,5,['#2e8a46','#46a552'],0.1,0.2,21),40,410,2,3.8,-1.4))
    s.add(deck_woman())
    s.add(sitting_cat())
    s.add(jack(752,392))
    for x,y,k in [(338,396,1.3),(397,440,1.2),(485,430,1.1),(1180,430,0.9)]: s.add(tuft(x,y,k,'#d5e24f','#b6d443'))
    s.add(sway(grassfan(830,470,13,120,-170,-10,8,['#1f8a5a','#2fa26a','#47b876','#178050'],0.15,0.3,31),830,470,1.6,4.4,-.9))
    s.add(sway(fan2(s,790,474,46,13,'#eee05c','#6fb13a'),790,474,1.5,5.2,-2))
    s.add(sway(cattail(840,470,800,370,'#e8d24a',bend=-20),840,470,3,3.6,0)); s.add(sway(cattail(850,470,930,350,'#e8d24a',bend=20),850,470,3.4,4.1,-1.2))
    s.add(sway(cattail(830,470,740,410,'#e8d24a',bend=-10),830,470,2.6,3.2,-2.1))
    s.add(fireflies(s))
    return s.out(OUT+'why_scene.svg')

def footer_art():
    s=S(1504,512)
    s.add(f'<g transform="translate(640 0)">{night_sky(s)}</g>')
    cl=lambda x,y,w,h,b: f'<path d="{streak(x,y,w,h,b)}" fill="#ffffff" opacity=".22"/>'
    s.add(drift(cl(190,290,300,40,((.3,.15,1),(.55,.15,.6))),190,490,190))
    s.add(drift(cl(920,268,470,44,((.2,.1,.6),(.42,.12,1),(.66,.1,.7))),920,1390,230))
    s.add(drift(cl(400,170,260,26,((.4,.2,1),)),400,660,300,phase=.5))
    for i,(x,y,k,dur,ph,rev) in enumerate([(520,250,7,70,0,False),(820,150,6,84,.3,True),(1000,230,8,76,.6,False),(640,330,5,96,.4,True)]):
        s.add(bat(x,y,k*2,dur=dur,phase=ph,rev=rev,seed=i,flap=.18+i%3*.04))
    # distant blue left
    s.p(smooth([(240,400),(300,340),(360,330),(420,345),(500,400)],False)+'Z','#3aa6d8')
    s.p(smooth([(980,400),(1040,350),(1110,345),(1180,360),(1240,400)],False)+'Z','#4fb8de')
    # big mountain
    bm=s.lg('fbm',[(0,'#30cbe2'),(.6,'#28b3b8'),(1,'#26a58f')],0,220,0,420,1)
    s.p(smooth([(420,420),(520,330),(600,290),(660,262),(717,236),(760,252),(808,222),(860,240),(920,270),(1000,300),(1080,340),(1150,420)],False)+'Z',bm)
    s.p(smooth([(560,420),(640,350),(720,320),(800,330),(900,360),(1000,420)],False)+'Z','#2bb59a',opacity=.85)
    s.p(smooth([(808,222),(860,240),(920,270),(880,280),(840,262)],True),'#57d6e8',opacity=.7)
    # left cliff
    lc=s.lg('flc',[(0,'#1d9e8a'),(1,'#1a8a82')],0,0,1,1)
    s.p(smooth([(0,300),(60,250),(120,226),(180,218),(210,240),(240,300),(300,350),(380,390),(460,420),(0,430)],False)+'Z',lc)
    s.p(smooth([(180,218),(210,240),(240,300),(300,350),(380,390),(460,420),(330,420),(260,360),(220,290)],False)+'Z','#2fbe9e')
    s.p(smooth([(110,232),(150,220),(190,218),(200,228),(160,230)],True),'#a8d454')
    # pines
    PN=[(600,455,80,34,0),(640,452,100,40,1),(684,455,72,30,0),(722,456,110,44,1),(770,455,90,38,0),(812,456,118,46,1),(860,452,84,34,0),(900,456,104,42,1),(944,452,90,36,0),(985,455,76,32,1),(1046,352,64,24,0),(560,458,60,26,1)]
    for i,(x,b,h,w,k) in enumerate(PN):
        c1,c2=(('#2b8a55','#3fa866') if k==0 else ('#6fae3c','#93c94a'))
        w=w*1.45; full,half=pine(x,b,h,w,5)
        s.add(sway(f'<path d="{full}" fill="{c1}"/><path d="{poly([(x,b-h),(x+w*0.12,b-h*0.55),(x+w*0.42,b),(x,b)])}" fill="{c2}"/>',x,b,.9,4.5+(i%4)*.7,-i*.9))
    # meadow
    md=s.lg('fmd',[(0,'#95c940'),(1,'#6aa830')],0,390,0,512,1)
    s.p(smooth([(0,420),(200,400),(420,412),(620,430),(800,440),(1000,430),(1200,420),(1504,430)],False)+'L1504 512L0 512Z',md)
    s.p(smooth([(300,470),(520,450),(760,452),(960,462),(1180,472),(1000,480),(700,474),(450,480)],True),'#b2d455',opacity=.7)
    s.p(smooth([(560,430),(700,424),(860,440),(760,446)],True),'#a8d04e',opacity=.8)
    # haunted house on the meadow, smoke from the chimney
    k,ox,oy=.62,1050,462
    s.raw_def('<radialGradient id="puff"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset=".55" stop-color="#f4fbff" stop-opacity=".7"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>')
    s.add(smoke(ox+222*k,oy-236*k,6,8.5,'url(#puff)',6,120,40,2.2))
    s.add(house(s,ox,oy,k,door=True))
    for cx,by in [(1000,470),(1236,468)]: s.add(_jack(cx,by))
    s.add(jack(930,478))
    # tree top-left
    for d,w in [('M-10 300C40 250 60 180 70 120C76 90 90 70 110 60',8),('M30 260C60 220 80 170 120 130',5),('M-10 200C20 170 30 140 30 110',5)]:
        s.p(d,'none',stroke='#165f4f',stroke_width=w,stroke_linecap='round')
    can=s.lg('fcan',[(0,'#23977f'),(1,'#0f5f55')],0,0,0,1)
    s.p(smooth([(-20,10),(60,0),(140,10),(200,40),(250,80),(320,110),(368,140),(300,150),(220,140),(160,120),(100,100),(30,96),(-20,90)],True),can)
    s.p(smooth([(-20,20),(60,12),(130,24),(170,50),(120,56),(60,50),(-20,56)],True),'#3fb59a',opacity=.8)
    s.p(smooth([(60,150),(130,140),(200,150),(260,180),(200,192),(130,186),(70,180)],True),'#137363')
    s.p(smooth([(200,60),(250,90),(300,112),(280,120),(230,104)],True),'#3fb59a',opacity=.7)
    # left grasses & cattails
    s.add(sway(grassfan(90,500,14,190,-160,-40,10,['#2e8a46','#46a552','#5fb85a','#24793e'],0.12,0.3,51),90,500,1.8,5,-.5))
    s.add(sway(fan2(s,140,506,110,21,'#eee05c','#4f9f3a'),140,506,1.3,5.8,-2))
    for i,(a0,b0,c0,d0,bd) in enumerate([(60,500,30,270,-10),(80,500,80,300,10),(120,500,230,290,20),(150,500,280,400,10)]): s.add(sway(cattail(a0,b0,c0,d0,'#e8d24a',bend=bd),a0,b0,2.6,3.2+i*.5,-i*.8))
    # right plant
    R=''
    R+=bigleaf(1470,512,390,62,-92,-0.05,'#1f7a43','#3d9a52','#145c32',side=-1)
    R+=bigleaf(1440,512,250,36,-120,-0.1,'#3fa354','#68c264','#24793e',side=-1)
    R+=bigleaf(1380,512,200,28,-150,-0.05,'#2a8445','#4caf5a','#1d6b38',side=-1)
    R+=budstem([(1420,500),(1410,380),(1390,260),(1370,150),(1360,100)],[(0.7,-160,'o',52),(1.3,-170,'p',50),(1.8,-150,'o',46),(2.3,-170,'p',46),(2.9,-150,'p',42),(3.5,-110,'p',36)],2.4)
    s.add(sway(R,1440,512,1.2,6,-1.5))
    # dark bushes at bottom edge
    nv='#14425b'
    for cx,r in [(0,40),(70,24),(640,30),(700,22),(910,26),(1210,16),(1440,40),(1380,24)]:
        s.add(grassfan(cx,520,9,r*1.6,-170,-10,max(3,r/6),[nv,'#123a52'],0.05,0.2,int(cx)))
    s.p('M0 506H1504V512H0Z',nv)
    return s.out(OUT+'footer_art.svg')

def card(n):
    s=S(398,330)
    if n==1:
        s.p('M0 0H398V330H0Z',s.lg('c1s',[(0,'#3fb4ef'),(1,'#bfe8fb')],0,0,0,160,1))
        s.p(cloud(30,96,150,22),'#ffffff'); s.p(cloud(200,86,190,24),'#ffffff'); s.p(cloud(100,40,180,10),'#ffffff',opacity=.4)
        s.p(smooth([(0,140),(60,120),(130,132),(200,118),(280,130),(398,116),(398,150),(0,150)],False)+'Z','#3c9fcf')
        s.p(smooth([(0,96),(20,110),(50,140),(90,170),(0,175)],False)+'Z','#1e9a86'); s.p('M0 98C10 100 18 104 22 110L0 112Z','#94cf50')
        s.p(smooth([(398,100),(360,108),(320,140),(290,170),(398,175)],False)+'Z','#1e9a86'); s.p('M398 100L360 108L372 116L398 112Z','#94cf50')
        s.p('M0 140H398V330H0Z',s.lg('c1l',[(0,'#5ad4ef'),(1,'#1fb0dc')],0,140,0,330,1))
        for x,y,w in [(10,170,120),(250,180,120),(150,250,110)]: s.p(f'M{x} {y}q{w*.5} -7 {w} 0q-{w*.5} 7 -{w} 0z','#a5ecf8',opacity=.7)
        s.p(smooth([(20,215),(80,192),(200,186),(320,192),(380,215),(300,230),(100,232)],True),'#2e8a3c')
        s.p(smooth([(26,210),(90,190),(200,184),(310,190),(372,210),(300,222),(100,224)],True),s.lg('c1i',[(0,'#9acb3f'),(1,'#5aa83a')],0,0,0,1))
        s.p(smooth([(60,206),(100,198),(140,206),(100,214)],True),'#e9c47c'); s.p(smooth([(220,204),(270,196),(320,204),(270,212)],True),'#e9c47c')
        for x,b,h,w in [(140,190,80,26),(168,186,70,22),(186,192,90,28)]:
            full,half=pine(x,b,h,w,4); s.p(full,'#1e7a4a')
        s.lg('glass',[(0,'#f4fcff'),(1,'#bfe4fb')],0,0,1,1)
        s.add(house(s,118,188,0.56))
        s.p('M216 92C206 80 222 70 214 58','none',stroke='#ffffff',stroke_width=4,stroke_linecap='round',opacity=.6)
        s.p(smooth([(100,190),(104,160),(112,146),(120,160),(122,190)],True),'#a3cd48')
        s.p(smooth([(248,190),(252,166),(258,154),(266,168),(268,190)],True),'#9cc943')
        s.add(grassfan(80,330,10,110,-160,-50,6,['#1f7a4a','#2e9a52','#4cb862'],0.15,0.3,61))
        s.add(frond(398,330,150,-150,-0.12,40,12,'#1f7a4a','#2e9a52'))
        s.add(frond(330,340,120,-110,-0.2,34,10,'#2e9a52','#4cb862'))
        s.add(cattail(110,330,96,236,'#e8d24a',bend=-6)); s.add(cattail(120,330,150,250,'#e8d24a',bend=10))
        for x,y in [(200,262),(180,290)]:
            s.add(f'<path d="M{x} {y}c-8 0-14-6-12-12 8 2 14 0 18-4 6-2 12 2 10 8-2 6-8 8-16 8z" fill="#ffffff"/><path d="M{x+14} {y-8}c0-10 2-18 8-18 4 0 4 6 0 6-2 4-2 8-2 12z" fill="#ffffff"/><path d="M{x+21} {y-26}l5 1-5 2z" fill="#f79a5a"/>')
    elif n==2:
        s.p('M0 0H398V330H0Z',s.lg('c2s',[(0,'#4dbff2'),(1,'#bde8fa')],0,0,0,100,1))
        s.p(cloud(10,50,110,20),'#ffffff'); s.p(cloud(110,44,160,14),'#ffffff')
        s.p('M0 70H398V330H0Z',s.lg('c2l',[(0,'#3fc4dc'),(1,'#22a8cc')],0,70,0,330,1))
        for x,y,w in [(20,140,90),(30,190,120),(120,170,80),(40,250,90)]: s.p(f'M{x} {y}q{w*.5} -6 {w} 0q-{w*.5} 6 -{w} 0z','#7fdcea',opacity=.7)
        # far headland
        s.p(smooth([(160,74),(220,60),(270,64),(330,70),(330,90),(160,90)],False)+'Z','#2a9a86')
        # cliffs right
        s.p(smooth([(180,110),(220,80),(270,60),(320,40),(360,20),(398,10),(398,330),(300,330),(270,200),(240,150)],False)+'Z','#239a7a')
        s.p(smooth([(200,100),(240,76),(290,58),(330,40),(310,80),(280,110),(240,130)],True),'#8cc94a')
        s.p(smooth([(250,130),(290,100),(330,70),(330,140),(300,200),(276,190)],True),'#1c7f68')
        # beach
        s.p(smooth([(210,116),(250,124),(286,150),(300,200),(310,250),(300,330),(250,330),(270,250),(260,190),(230,150)],False)+'Z','#f2c69a')
        s.p(smooth([(200,116),(240,128),(270,160),(282,210),(272,260),(262,330),(240,330),(250,250),(250,190),(220,140)],False)+'Z','#e9f6f4',opacity=.6)
        # rock wall
        s.p(smooth([(330,0),(398,0),(398,330),(370,330),(350,240),(340,160),(330,80)],False)+'Z','#4f6a7a')
        s.p(smooth([(340,0),(370,0),(380,60),(372,140),(360,200),(352,140),(348,60)],False)+'Z','#6c8796')
        s.p('M300 0H340L330 30C320 20 310 10 300 0Z','#4f6a7a')
        # islets
        for x,y,w,h in [(70,98,50,30),(130,92,44,40)]:
            s.p(smooth([(x,y+h),(x+4,y+h*.4),(x+w*.3,y+h*.1),(x+w*.7,y),(x+w,y+h*.4),(x+w,y+h)],False)+'Z','#f3b182')
            s.p(smooth([(x+w*.2,y+h*.6),(x+w*.4,y+h*.3),(x+w*.7,y+h*.4),(x+w,y+h*.8),(x+w,y+h)],False)+f'L{x+w*.3} {y+h}Z','#e08e6a')
            s.p(smooth([(x+2,y+h*.45),(x+w*.3,y+h*.05),(x+w*.7,y-4),(x+w,y+h*.35),(x+w*.6,y+h*.3),(x+w*.3,y+h*.4)],True),'#2fae7e')
        x,y,w,h=90,200,80,90
        s.p(smooth([(x,y+h),(x+6,y+h*.4),(x+w*.35,y+h*.05),(x+w*.7,y+h*.1),(x+w,y+h*.6),(x+w,y+h)],False)+'Z','#f3b182')
        s.p(smooth([(x+w*.4,y+h*.5),(x+w*.7,y+h*.3),(x+w,y+h*.7),(x+w,y+h)],False)+f'L{x+w*.4} {y+h}Z','#e08e6a')
        s.p(smooth([(x+w*.2,y+h*.2),(x+w*.4,y),(x+w*.6,y+h*.12),(x+w*.4,y+h*.2)],True),'#2fae7e')
        # palms
        for px,py,ht in [(270,300,120),(220,320,80)]:
            s.p(f'M{px} {py}C{px+4} {py-ht*.5} {px+10} {py-ht*.8} {px+14} {py-ht}','none',stroke='#8a6a4a',stroke_width=4,stroke_linecap='round')
            for a in [-170,-130,-90,-50,-10,30,150]:
                s.add(f'<path d="{leaf(px+14,py-ht,ht*.35,ht*.06,a,0.15)}" fill="#3a9a4a"/>')
        # foreground plants
        s.add(frond(0,330,140,-50,0.2,40,12,'#1f7a4a','#2e9a52'))
        s.add(frond(170,340,110,-80,0.1,30,10,'#2e9a52','#4cb862'))
        s.p('M0 300C120 290 280 300 398 296V330H0Z','#1c5a44')
        # railing posts & ropes
        post='#3a5fb0'
        for x,top in [(40,180),(180,200),(258,212),(316,226)]:
            s.p(f'M{x-10} 330V{top}H{x+10}V330Z',post); s.p(f'M{x-10} {top}H{x+10}V{top+8}H{x-10}Z','#5c82d0')
            s.add(f'<circle cx="{x}" cy="{top+20}" r="4" fill="#24427e"/>')
        rope='#3b3b46'
        for yy in (0,48):
            s.p(f'M40 {200+yy}Q110 {250+yy} 180 {220+yy}Q220 {242+yy} 258 {232+yy}Q290 {250+yy} 316 {246+yy}','none',stroke=rope,stroke_width=4,stroke_linecap='round')
        s.p('M220 330L250 300L398 300V330Z','#6b4a3a')
    else:
        s.p('M0 0H398V330H0Z',s.lg('c3s',[(0,'#4dbff2'),(1,'#cdeefb')],0,0,0,110,1))
        s.p(cloud(20,70,120,16),'#ffffff'); s.p(cloud(150,64,230,20),'#ffffff')
        s.p('M0 100H398V330H0Z',s.lg('c3l',[(0,'#4cc8e4'),(1,'#1fa4cf')],0,100,0,330,1))
        s.p(smooth([(0,100),(80,84),(160,90),(240,86),(300,96),(398,90),(398,120),(0,130)],False)+'Z','#2a9a86')
        s.p(smooth([(0,92),(80,80),(160,86),(240,82),(260,90),(160,96),(60,98)],True),'#8cc94a')
        s.p(smooth([(0,120),(40,110),(70,130),(40,150),(0,160)],False)+'Z','#1c7f68')
        # big arch landmass
        s.p(smooth([(0,220),(80,170),(160,140),(260,120),(398,100),(398,330),(0,330)],False)+'Z','#2a9a6a')
        s.p(smooth([(0,210),(70,170),(150,142),(250,122),(398,102),(398,120),(260,140),(160,166),(80,196),(0,236)],False)+'Z','#a8d050')
        s.p(smooth([(40,330),(80,250),(140,200),(220,180),(290,190),(320,240),(310,290),(290,330)],False)+'Z',s.lg('c3w',[(0,'#56d6ea'),(1,'#1aa6c8')],0,0,0,1))
        s.p(smooth([(100,280),(150,230),(210,215),(260,226),(240,250),(180,252),(130,290)],True),'#9eeaf4',opacity=.7)
        s.p(smooth([(0,300),(30,260),(60,236),(80,250),(60,290),(40,330),(0,330)],False)+'Z','#1f7e5a')
        s.add(frond(0,330,160,-40,0.2,40,12,'#3a9a3a','#7cbf3a'))
        s.add(frond(120,340,130,-60,0.15,34,10,'#c8d84a','#a8c84a'))
        s.add(frond(398,330,160,-120,-0.1,40,12,'#1f7a4a','#2e9a52'))
        s.add(bigleaf(398,300,150,24,-115,-0.08,'#2b8a4a','#55b05a','#1d6b38',side=-1))
        s.add(budstem([(360,300),(350,200),(340,120),(330,70)],[(0.6,-170,'p',22),(1.2,-20,'o',20),(1.7,-160,'o',20),(2.3,-30,'p',18),(2.8,-100,'p',18)],1.6))
    s.out(OUT+f'card{n}.svg')
    # rewrite with rounded top corners clip not needed (handled by CSS)

def plant_cluster():
    s=S(414,580)
    o=''
    o+=bigleaf(430,560,500,70,-100,-0.06,'#2b8a4a','#5cb45a','#1d6b38',side=-1)
    o+=bigleaf(400,580,360,50,-120,-0.08,'#3fa354','#7cc664','#24793e',side=-1)
    o+=bigleaf(330,580,300,42,-110,0.04,'#1f7a43','#3d9a52','#145c32')
    o+=bigleaf(260,580,240,36,-140,0.06,'#2a8445','#55b05a','#1d6b38')
    o+=budstem([(330,560),(320,400),(300,250),(270,120),(250,60),(240,20)],[(0.5,-170,'o',42),(1.0,-160,'p',47),(1.6,-170,'o',42),(2.0,-150,'p',47),(2.6,-160,'o',42),(3.2,-170,'p',42),(3.7,-150,'p',39),(4.5,-110,'p',39)],2)
    o+=budstem([(220,560),(200,450),(160,370),(130,330)],[(1.0,-150,'o',42),(1.7,-170,'o',39),(2.6,-130,'o',36)],1.8)
    o+=budstem([(370,560),(380,430),(400,330)],[(0.9,-20,'p',39),(1.6,-60,'p',36)],1.8)
    s.add(o)
    s.add(fan2(s,300,590,80))
    s.add(fan2(s,120,592,64))
    s.add(bigleaf(190,590,230,34,-60,0.1,'#2a8445','#55b05a','#1d6b38'))
    s.add(bigleaf(250,590,260,40,-80,0.06,'#3fa354','#7cc664','#24793e'))
    s.add(grassfan(120,580,12,120,-170,-20,7,['#1f8a5a','#2fa26a','#47b876','#178050'],0.15,0.3,71))
    s.add(capsule(8,388,30,395,7,'#e8d24a')); s.add(capsule(140,250,150,265,0,'#e8d24a'))
    s.add(capsule(80,480,96,490,7,'#e8d24a'))
    s.add(tuft(20,560,1.1,'#d5e24f','#b6d443'))
    return s.out(OUT+'plant_cluster.svg')
def plant_small():
    s=S(390,360)
    o=budstem([(150,330),(146,240),(150,150),(156,60),(150,10)],[(1.0,-160,'o',36),(1.5,-30,'o',34),(2.0,-150,'o',34),(2.6,-40,'o',30),(3.5,-90,'o',26)],2)
    s.add(o)
    s.add(grassfan(150,340,13,170,-165,-15,9,['#1f8a5a','#2fa26a','#47b876','#178050'],0.12,0.3,81))
    s.add(fan2(s,170,346,64))
    s.add(capsule(100,130,112,150,8,'#e8d24a')); s.add(capsule(210,130,204,150,8,'#e8d24a')); s.add(capsule(310,180,294,192,8,'#e8d24a'))
    s.add(tuft(345,340,1.2,'#c8dc50','#a6cc45'))
    return s.out(OUT+'plant_small.svg')
def leaf_corner():
    s=S(212,238,vb='-44 0 212 238')  # leaves spill left of x=0; widen so card shows the whole leaf
    o=''
    o+=bigleaf(150,230,220,34,-100,-0.08,'#2b8a4a','#5cb45a','#1d6b38',side=-1)
    o+=bigleaf(120,230,170,26,-120,-0.06,'#3fa354','#7cc664','#24793e',side=-1)
    o+=bigleaf(60,232,120,22,-150,0.05,'#1f7a43','#3d9a52','#145c32')
    o+=budstem([(100,230),(96,160),(80,90),(60,20)],[(0.6,-160,'o',24),(1.1,-20,'p',24),(1.6,-160,'p',22),(2.2,-30,'p',22),(2.9,-110,'p',20)],1.5)
    o+=budstem([(140,230),(140,150),(130,60)],[(0.8,-30,'p',22),(1.5,-60,'p',20)],1.5)
    s.add(o); s.add(fan2(s,50,232,40))
    return s.out(OUT+'leaf_corner.svg')
def avatar(n):
    s=S(80,80)
    s.add('<circle cx="40" cy="40" r="40" fill="#eef7ff"/>')
    if n==1:
        s.add('<path d="M14 80C14 62 26 54 40 54S66 62 66 80Z" fill="#f79a5a"/><path d="M58 56C66 52 74 56 72 66 70 72 62 72 58 70Z" fill="#f27a3a"/>'
              '<path d="M34 46h12v10c0 4-12 4-12 0z" fill="#f0b48c"/><ellipse cx="40" cy="36" rx="13" ry="15" fill="#f6c4a0"/>'
              '<path d="M26 34C24 20 34 14 42 16 52 16 56 24 54 34 50 26 44 24 38 28 34 24 30 26 26 34Z" fill="#1e2228"/>'
              '<circle cx="35" cy="37" r="1.6" fill="#1e2228"/><circle cx="45" cy="37" r="1.6" fill="#1e2228"/><path d="M37 44q3 2 6 0" stroke="#c46a50" stroke-width="1.4" fill="none" stroke-linecap="round"/>')
    else:
        s.add('<path d="M22 66C20 40 24 22 40 20S60 40 58 66Z" fill="#3a2a5a"/><path d="M14 80C14 64 26 56 40 56S66 64 66 80Z" fill="#2f6fd0"/><path d="M30 58L40 68 50 58Z" fill="#f6f2ea"/>'
              '<path d="M34 46h12v10c0 4-12 4-12 0z" fill="#f0b48c"/><ellipse cx="40" cy="37" rx="12" ry="14" fill="#f6c4a0"/>'
              '<path d="M28 40C26 24 34 20 42 20 52 22 54 30 52 40 50 30 44 26 36 28 32 30 30 34 28 40Z" fill="#3a2a5a"/><path d="M66 50C62 44 56 46 58 54Z" fill="#f79a5a"/><path d="M14 52C18 46 24 48 22 54Z" fill="#f79a5a"/>'
              '<circle cx="35" cy="38" r="1.6" fill="#1e2228"/><circle cx="45" cy="38" r="1.6" fill="#1e2228"/><path d="M37 45q3 2 6 0" stroke="#d0606a" stroke-width="1.4" fill="none" stroke-linecap="round"/>')
    return s.out(OUT+f'avatar{n}.svg')
def swoosh():
    s=S(400,40)
    s.add('<path d="M6 26C70 14 150 10 230 12S360 16 394 20C396 24 394 28 390 29 330 24 250 22 170 24S60 30 10 36C4 36 2 30 6 26Z" fill="#f4a36a" opacity=".92"/>')
    return s.out(OUT+'swoosh.svg')
if __name__=='__main__':
    print('why',why_scene()); print('foot',footer_art())
    import cards2; cards2.card1(); cards2.card2(); cards2.card3()
    print(plant_cluster(),plant_small(),leaf_corner(),avatar(1),avatar(2),swoosh())
