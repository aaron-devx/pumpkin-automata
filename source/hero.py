from lib import *
from comp import *
import math, itertools
from figures import deck_woman, sitting_cat
_HOUSE_IDS=itertools.count()
WALL='#4a2c5e'; WALL_DK='#3a2150'; ROOF='#24163a'; TRIM='#6b3f86'; GLOW='#ffcf5a'; GLOW2='#ff9a2e'; STONE='#5a4a6e'
def _scallops(x0,x1,y0,y1,step=8):
    # rows of half-round shingles, offset every other row
    d=''
    for r,y in enumerate(range(y0,y1,step)):
        x=x0-(step/2 if r%2 else 0)
        d+=f'M{f(x)} {y}'+f'a{step/2} {step/2} 0 0 0 {step} 0'*int((x1-x)//step+1)
    return d
def house(s,ox=0,oy=0,k=1.0,door=False):
    """original crooked haunted house: curled spires, scalloped shingles, cobble base. local coords: origin at left-bottom of front face"""
    hid=f'hs{next(_HOUSE_IDS)}'
    def A(d,c,**kw): return f'<path d="{d}" fill="{c}"'+''.join(f' {a.replace("_","-")}="{v}"' for a,v in kw.items())+'/>'
    def L(d,c,w,op=1): return A(d,'none',stroke=c,stroke_width=w,stroke_linecap='round',opacity=op)
    def shingled(name,d,box):
        x0,x1,y0,y1=box
        return A(d,ROOF)+f'<clipPath id="{hid}{name}"><path d="{d}"/></clipPath><g clip-path="url(#{hid}{name})">'+L(_scallops(x0,x1,y0,y1),'#3d2a5c',1.6,.9)+'</g>'
    def win(cx,y,w,h,c=GLOW):
        # pointed gothic window: glow, frame, mullion cross, crooked shutters
        arch=f'M{cx-w/2} {y}V{y-h+w*.6}Q{cx-w/2} {y-h+w*.12} {cx} {y-h}Q{cx+w/2} {y-h+w*.12} {cx+w/2} {y-h+w*.6}V{y}Z'
        g=f'<circle cx="{cx}" cy="{y-h/2}" r="{h*.6}" fill="{GLOW2}" opacity=".2"/>'
        g+=A(f'M{cx-w/2-7} {y+1}l5 -{h*.7}h4l-3 {h*.7}Z','#2a1a40')+A(f'M{cx+w/2+2} {y}l4 -{h*.68}h5l-4 {h*.7}Z','#2a1a40')
        return g+A(arch,c,stroke=ROOF,stroke_width=2.4)+L(f'M{cx} {y}V{y-h+3}M{cx-w/2} {y-h*.42}H{cx+w/2}',ROOF,1.8)
    def curl(x,y,m=1):
        # little curled hook on eave ends
        return L(f'M{x} {y}c{-7*m} 0 {-10*m} -7 {-5*m} -9c{3*m} -1 {4*m} 3 {1*m} 4',TRIM,2.6)
    body='M0 0L232 0L238 -92L244 -168L8 -172L4 -90Z'
    o=f'<g transform="translate({f(ox)} {f(oy)}) scale({k})">'
    # leaning two-storey body with board siding
    o+=A(body,WALL)+f'<clipPath id="{hid}b"><path d="{body}"/></clipPath><g clip-path="url(#{hid}b)">'
    o+=L(''.join(f'M{x} -4L{x+2} -170' for x in range(18,244,14)),WALL_DK,1.4,.55)
    o+=A('M0 -40L240 -44L240 0L0 0Z',WALL_DK,opacity=.35)+'</g>'
    # sagging floor band with curled ends
    o+=A('M-6 -96C40 -90 190 -90 246 -98L246 -88C190 -82 40 -82 -6 -88Z',WALL_DK)+curl(-6,-92)+curl(246,-94,-1)
    # cobblestone base
    o+=A('M-6 -14H242V4H-6Z','#2c1f3a')
    o+=''.join(f'<ellipse cx="{x+(6 if r else 0)}" cy="{-9+r*8}" rx="5.6" ry="3.4" fill="{STONE}" opacity="{.75+((x*7+r)%3)*.1:.2f}"/>' for r in (0,1) for x in range(-2,240,12))
    # left tower: squat body + flared cone, tip curls right
    o+=A('M6 -170H68L66 -198H10Z',WALL_DK)
    o+=shingled('t','M-10 -192C10 -196 26 -214 32 -244C36 -262 46 -274 60 -272C70 -270 70 -258 62 -258C56 -258 56 -264 60 -264C50 -262 46 -248 46 -236C48 -212 64 -198 84 -192Z',(-12,86,-276,-188))
    o+=f'<circle cx="38" cy="-184" r="7" fill="{GLOW}" stroke="{TRIM}" stroke-width="2.2"/>'+L('M38 -191V-177M31 -184H45',TRIM,1.4)
    # front gable
    o+=shingled('g','M58 -168L98 -230L138 -168Z',(56,140,-232,-166))+win(98,-176,14,28,GLOW2)
    # right spire: sweeping roof, tip curls left
    o+=shingled('r','M116 -166C140 -178 158 -200 166 -232C170 -252 178 -266 194 -270C206 -272 210 -260 202 -258C196 -256 196 -262 200 -263C190 -258 186 -244 186 -230C188 -204 206 -184 250 -166Z',(114,252,-274,-164))
    # roof eave trim with curls
    o+=A('M-6 -170C60 -174 180 -172 250 -166L250 -161C180 -166 60 -168 -6 -164Z',TRIM)+curl(-6,-167)+curl(250,-163,-1)
    # bent brick chimney (cap top ~ (222,-232) feeds the smoke)
    o+=A('M206 -168H222L220 -200L228 -214L232 -228L216 -232L212 -216L208 -200Z',WALL_DK)
    o+=L('M207 -178H221M208 -190H220M209 -204H221M214 -218H228',ROOF,1.2,.8)
    o+=A('M210 -235L236 -229V-224L210 -230Z',TRIM)
    # windows
    o+=win(40,-108,20,36,GLOW2)+win(152,-106,22,42)+win(206,-106,20,38)+win(184,-24,14,22,GLOW2)
    # porch: posts, pointed roof, arched door with planks
    o+=A('M84 0V-74h5V0ZM127 0V-74h5V0Z',WALL_DK)
    o+=A('M68 -72L108 -98L148 -72L144 -68L108 -91L72 -68Z',ROOF)+curl(68,-71)+curl(148,-71,-1)
    o+=A('M92 -6V-50Q92 -66 108 -72Q124 -66 124 -50V-6Z',GLOW2)
    o+=A('M96 -6V-50Q96 -62 108 -67Q120 -62 120 -50V-6Z','#3b2418')+L('M104 -8V-64M112 -8V-64',GLOW2,1,.35)
    o+=f'<circle cx="117" cy="-30" r="1.8" fill="{GLOW}"/>'
    o+=A('M80 6H136V0H80Z',TRIM)+A('M74 12H142V6H74Z',WALL_DK)
    return o+'</g>'
def build_layers():
    """returns (defs_markup, [(name, scroll_factor, mouse_depth, markup), ...]) back->front"""
    from anim import sway, drift, drift_rev, bat, smoke, shimmer
    s=S(1504,940)
    W='#ffffff'
    L=[]
    def cut(name,fac,depth):
        L.append((name,fac,depth,''.join(s.el))); s.el.clear()
    # ---------- sky (oversized) ----------
    s.p('M-300-500H1804V1140H-300Z',gradu(s,'sky',[(0,'#4cc4f8'),(.36,'#52c8f9'),(.55,'#a1e4fd'),(.78,'#c4edfe'),(1,'#d4f2fe')],0,-500,0,640))
    s.lg('glass',[(0,'#f4fcff'),(1,'#bfe4fb')],0,0,1,1)
    s.raw_def('<radialGradient id="puff"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset=".55" stop-color="#f4fbff" stop-opacity=".7"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>')
    cut('sky',.5,3)
    # ---------- clouds: each drifts at its own speed; far = slower ----------
    def P(x): s.el.append(x)
    P(drift(f'<path d="{streak(400,236,420,22,((.4,.3,1),),0.15)}" fill="#fff" opacity=".35"/>',400,820,420))
    P(drift(f'<path d="{streak(1040,190,480,30,((.3,.25,1),(.7,.2,.7)),0.15)}" fill="#fff" opacity=".35"/>',1040,1520,380))
    P(drift(f'<path d="{streak(1150,330,360,24,((.5,.3,1),),0.15)}" fill="#fff" opacity=".3"/>',1150,1510,400))
    P(drift(cloud2(260,542,280,30,((.25,.14,.7),(.5,.14,1),(.78,.12,.5)),tail_l=50,tail_r=40),210,580,260))
    P(drift(cloud2(790,540,530,48,((.1,.1,.45),(.28,.12,.85),(.47,.1,.6),(.64,.12,1),(.86,.1,.55)),tail_l=60,tail_r=60),730,1380,240))
    P(drift(cloud2(120,442,190,44,((.28,.12,.55),(.5,.13,1),(.75,.12,.45)),tail_l=130,tail_r=110),-10,420,170))
    P(drift(cloud2(1170,446,334,58,((.1,.1,.45),(.3,.12,.85),(.55,.12,1),(.8,.12,.65)),tail_l=110),1060,1504,150))
    # twins half a cycle later keep the sky populated
    P(drift(cloud2(120,442,190,44,((.28,.12,.55),(.5,.13,1),(.75,.12,.45)),tail_l=130,tail_r=110),-10,420,170,phase=.5))
    P(drift(cloud2(260,542,280,30,((.25,.14,.7),(.5,.14,1),(.78,.12,.5)),tail_l=50,tail_r=40),210,580,260,phase=.5))
    cut('clouds',.44,6)
    # ---------- bats ----------
    for i,(x,y,k,dur,ph,rev) in enumerate([(430,483,9,70,0,False),(860,470,7,84,0,False),(1060,458,8,76,0,False),(330,320,6,96,.4,True),(560,300,5,110,.7,True)]):
        P(bat(x,y,k*1.4,dur=dur,phase=ph,rev=rev,seed=i,flap=.18+i%3*.04))
    cut('bats',.38,8)
    # ---------- mountains ----------
    s.p('M-120 656H1624V760H-120Z','#2fb2d6')
    s.p(smooth([(-120,700),(-120,615),(0,608),(120,605),(260,622),(330,592),(380,586),(430,602),(500,598),(570,622),(660,628),(760,630),(880,618),(960,594),(1040,602),(1120,586),(1190,612),(1280,612),(1400,604),(1504,612),(1624,606),(1624,700)],False)+'Z',gradu(s,'fh1',[(0,'#5fcbe5'),(1,'#33b5d9')],0,580,0,650))
    s.p(smooth([(260,680),(300,626),(350,612),(420,620),(470,612),(540,630),(600,680)],False)+'Z','#1ebbd8')
    s.p(smooth([(330,680),(380,632),(450,626),(520,640),(560,680)],False)+'Z','#1893bc')
    s.p(smooth([(860,680),(920,630),(980,618),(1050,626),(1110,612),(1170,640),(1200,680)],False)+'Z','#1ebbd8')
    s.p(smooth([(940,680),(1000,640),(1060,634),(1120,646),(1150,680)],False)+'Z','#1893bc')
    s.p(smooth([(-120,560),(-40,540),(20,520),(40,486),(90,476),(150,468),(170,490),(200,530),(240,590),(290,630),(350,652),(380,670)],False)+'L380 720L-120 720Z',gradu(s,'lmt',[(0,'#2aa08c'),(1,'#16786e')],0,470,0,660))
    s.p(smooth([(150,468),(176,486),(205,486),(214,500),(230,560),(270,620),(330,652),(380,668),(300,668),(250,620),(210,560),(180,500)],False)+'Z','#45c4a2')
    s.p(smooth([(60,500),(90,482),(120,500),(110,560),(80,620),(60,668),(30,668),(50,580)],False)+'Z','#3dbb9c',opacity=.9)
    s.p(smooth([(30,560),(50,520),(60,500),(55,580),(40,640),(20,668)],False)+'Z','#1d8a80')
    s.p(smooth([(-120,500),(-40,494),(36,490),(70,478),(150,466),(156,474),(110,484),(60,492),(-40,504),(-120,512)],True),'#b6d63a')
    s.p(smooth([(176,486),(196,480),(210,490),(196,494)],True),'#8fd16a')
    s.p(smooth([(1150,700),(1190,630),(1230,566),(1270,522),(1310,500),(1360,494),(1440,488),(1504,486),(1624,484),(1624,700)],False)+'Z',gradu(s,'rmt',[(0,'#2bab90'),(1,'#107570')],1180,500,1300,680))
    s.p(smooth([(1300,504),(1350,494),(1430,488),(1504,486),(1624,484),(1624,498),(1504,500),(1440,504),(1380,510),(1320,514)],True),'#d0cd2a')
    s.p(smooth([(1320,514),(1380,510),(1504,500),(1624,498),(1624,560),(1504,560),(1440,560),(1380,556)],True),'#26a088')
    s.p(smooth([(1270,566),(1330,558),(1440,560),(1504,560),(1624,560),(1624,574),(1504,574),(1420,576),(1340,578),(1290,580)],True),'#8cc85a')
    s.p(smooth([(1290,580),(1420,576),(1504,574),(1624,574),(1624,700),(1300,700),(1260,640)],True),'#21987f',opacity=.9)
    s.p(smooth([(1150,700),(1190,630),(1230,566),(1250,560),(1230,620),(1210,700)],False)+'Z','#0f6f6a')
    s.p(smooth([(1210,700),(1230,630),(1260,600),(1300,610),(1280,700)],False)+'Z','#38bb9a',opacity=.8)
    cut('mountains',.3,10)
    # ---------- lake ----------
    s.p('M-140 650C-60 646 0 648 0 648C300 640 1200 640 1504 652C1560 654 1600 654 1644 654V1200H-140Z',gradu(s,'lake',[(0,'#8fe6f4'),(.25,'#66dcef'),(.7,'#45cbe8'),(1,'#2ab6df')],0,645,0,940))
    s.p('M-140 662L0 658C200 650 360 664 600 660C800 656 1000 662 1504 664L1644 664V672L1504 672C1000 668 800 666 600 670C360 674 200 662 0 668L-140 668Z','#b5f0f8',opacity=.8)
    def rip(lst):
        d=''
        for x,y,w,t in lst: d+=f'M{x} {y}C{x+w*.3} {y-t} {x+w*.7} {y-t} {x+w} {y}C{x+w*.7} {y+t*.6} {x+w*.3} {y+t*.6} {x} {y}Z'
        return d
    band=''
    for x,y,w in [(0,690,300),(1140,690,364),(200,750,260),(1040,770,300),(0,860,300)]:
        band+=f'M{x} {y}C{x+w*.3} {y-10} {x+w*.7} {y-10} {x+w} {y}C{x+w*.7} {y+8} {x+w*.3} {y+8} {x} {y}Z'
    P(shimmer(f'<path d="{band}" fill="#8fe6f4" opacity=".35"/>',9,0,14))
    P(shimmer(f'<path d="{rip([(240,700,220,5),(330,768,200,6),(1090,712,240,5),(1260,790,170,4),(600,836,120,4),(1240,860,180,4)])}" fill="#fff" opacity=".8"/>',4.6,0,9))
    P(shimmer(f'<path d="{rip([(60,736,160,4),(140,802,140,4),(1180,748,200,5),(980,826,260,5),(380,840,160,4)])}" fill="#fff" opacity=".8"/>',5.8,-2.9,-8))
    P(shimmer(f'<path d="{rip([(150,720,90,3),(420,730,110,3),(1000,740,120,3),(1350,720,100,3),(260,880,120,3),(1100,890,140,3)])}" fill="#dff8fc" opacity=".7"/>',3.8,-1.3,6))
    cut('lake',.2,12)
    # ---------- island + house ----------
    s.p(smooth([(470,790),(700,808),(1060,800),(1000,830),(760,842),(540,830)],True),'#3fc6e2',opacity=.7)
    s.p(smooth([(440,764),(520,722),(640,700),(800,694),(960,700),(1070,724),(1118,764),(1060,806),(900,818),(700,820),(510,810)],True),'#3d7d2c')
    s.p(smooth([(452,756),(530,718),(650,698),(800,692),(960,698),(1062,720),(1106,756),(1040,784),(900,796),(700,798),(510,790)],True),gradu(s,'isl',[(0,'#a3cf3e'),(1,'#6ea032')],0,692,0,796))
    s.p(smooth([(520,740),(640,724),(800,718),(960,724),(1030,740),(900,746),(700,748)],True),'#b6d84a',opacity=.6)
    sand=gradu(s,'sand',[(0,'#f6d898'),(1,'#e3ae66')],0,730,0,790)
    s.p(smooth([(456,760),(500,740),(570,732),(630,744),(610,764),(540,776),(490,778)],True),sand)
    s.p(smooth([(896,754),(960,736),(1040,736),(1102,756),(1062,780),(980,782),(920,774)],True),sand)
    s.p(smooth([(640,794),(760,786),(880,790),(820,800),(700,802)],True),sand,opacity=.9)
    gb=''
    for x0 in range(472,620,9): gb+=f'M{x0} 752l2-{10+(x0*7)%8}l3 {10+(x0*7)%8}z'
    for x0 in range(912,1090,9): gb+=f'M{x0} 758l2-{10+(x0*5)%8}l3 {10+(x0*5)%8}z'
    s.p(gb,'#c9963e')
    for i,(x,b,h,w) in enumerate([(668,702,250,74),(712,690,190,56),(772,702,262,76)]):
        P(sway(pine2(x,b,h,w,6,'#2f9a58','#1b6b46'),x,b,.7,5+i*.9,-i*1.7))
    P(sway(f'<path d="{smooth([(594,700),(596,640),(608,598),(624,574),(640,596),(650,650),(648,700)],True)}" fill="#a8d14a"/><path d="{smooth([(624,700),(626,620),(628,578),(642,602),(650,650),(648,700)],True)}" fill="#86b93e"/>',622,700,1.2,4.4,-1))
    P(sway(f'<path d="{smooth([(852,700),(856,640),(866,600),(880,586),(894,616),(900,670),(898,700)],True)}" fill="#a3cd48"/><path d="{smooth([(878,700),(880,620),(882,588),(894,616),(900,670),(898,700)],True)}" fill="#7fb23b"/>',876,700,1.2,4.9,-2.3))
    s.add(house(s,628,702,1.0))
    P(smoke(850,466,7,8.5,'url(#puff)',8,22,320,2.4))
    P(sway(grassfan(560,712,13,48,-165,-15,5,['#3f8f3a','#5fae46','#2f7f34'],seed=3),560,712,2,3.6,-.5))
    P(sway(grassfan(926,708,13,44,-165,-15,5,['#3f8f3a','#6db84a','#2f7f34'],seed=4),926,708,2,4.1,-1.8))
    s.add(fan2(s,604,716,32,13,'#e6e05a','#6ea032'))
    s.add(fan2(s,962,714,30,13,'#e6e05a','#6ea032'))
    for x,y in [(650,738),(690,746),(860,744),(920,738),(1000,750),(560,778)]: s.add(tuft(x,y,0.9,'#d5e24f','#a8cc3e'))
    # same woman + cat as the why scene, scaled down onto the lawn (feet on y~744)
    s.add(f'<g transform="translate(678 698.4) scale(.12)">{deck_woman()}</g>')
    s.add(f'<g transform="translate(691 701) scale(.12)">{sitting_cat()}</g>')
    cut('island',.16,14)
    # low bats skimming the water
    for i,(x,y,k,dur,ph,rev) in enumerate([(300,712,15,58,0,False),(375,690,8,64,0,False),(1094,708,12,52,0,True),(1252,808,24,46,0,True)]):
        P(bat(x,y,k*.9,dur=dur,phase=ph,rev=rev,seed=i+7,flap=.2+i%2*.06,zig=1.4))
    cut('lowbats',.14,15)
    # ---------- canopy (tree top-left, branch top-right) ----------
    tr='#155a55'; tree=''
    for d,w in [('M-60 360C-20 330 20 300 40 200C44 180 50 170 60 165',7),('M-40 365C40 300 70 270 100 250C120 238 140 232 160 228',5),('M-20 360C30 280 40 240 44 200',4),('M-80 200C10 185 30 176 50 165',5)]:
        tree+=f'<path d="{d}" fill="none" stroke="{tr}" stroke-width="{w}" stroke-linecap="round"/>'
    tree+=f'<path d="{smooth([(30,215),(100,200),(180,205),(240,222),(285,250),(200,256),(110,250),(40,240)],True)}" fill="{gradu(s,"can2",[(0,"#16a39a"),(1,"#0e7a78")],0,200,0,256)}"/>'
    tree+=f'<path d="{smooth([(-90,40),(-20,52),(60,46),(130,66),(180,104),(230,118),(280,124),(310,150),(340,190),(372,222),(320,224),(260,212),(190,196),(110,186),(40,184),(-20,190),(-90,194)],True)}" fill="{gradu(s,"can",[(0,"#2a8f7c"),(1,"#1d7468")],0,46,0,224)}"/>'
    tree+=f'<path d="{smooth([(-90,146),(-20,150),(60,160),(140,176),(220,192),(300,212),(372,222),(300,226),(220,208),(120,196),(30,192),(-20,196),(-90,198)],True)}" fill="#145151"/>'
    tree+='<path d="M236 122C256 112 282 114 292 130C280 124 262 124 248 132Z" fill="#2a8f7c"/><path d="M276 124C292 120 306 128 300 140" fill="none" stroke="#5fd0b8" stroke-width="3" stroke-linecap="round"/>'
    tk=''.join(leaf(x,y,Ln,Ln*0.2,a) for x,y,a,Ln in [(30,120,20,26),(110,150,30,28),(186,150,25,24),(250,170,20,22),(320,194,25,24),(150,96,10,20)])
    tree+=f'<path d="{tk}" fill="#46b9a0"/>'
    flick=''.join(sway(f'<path d="{leaf(x,y,Ln,4,a)}" fill="#1f9a8a"/>',x,y,9,1.8+i*.37,-i*.6) for i,(x,y,Ln,a) in enumerate([(178,100,18,-70),(190,104,16,-40),(318,170,16,-60),(250,236,16,-30)]))
    P(sway(tree+flick,-40,360,.9,7.5,0))
    br='#1f6355'; bt=''
    for d,w in [('M1600 340C1530 300 1480 262 1430 228 1380 206C1320 182 1260 168 1200 150C1160 138 1120 128 1080 124',8),('M1340 186C1336 150 1338 120 1344 96',4),('M1420 220C1424 180 1426 140 1432 100',4),('M1250 162C1236 140 1224 124 1212 110',3),('M1180 148C1170 152 1160 156 1150 160',3),('M1300 176C1290 158 1270 140 1256 130',3)]:
        bt+=f'<path d="{d}" fill="none" stroke="{br}" stroke-width="{w}" stroke-linecap="round"/>'
    bt=bt.replace('M1600 340C1530 300 1480 262 1430 228 1380 206','M1600 340C1560 320 1530 300 1500 280C1470 258 1430 228 1380 206')
    for i,(x,y,a) in enumerate([(1080,124,-180),(1150,160,-175),(1212,110,-135),(1256,130,-150),(1344,96,-95),(1432,100,-80)]):
        bt+=sway(twigcluster(x,y,a,44,4,'#0f8f8c',70),x,y,5,2.6+i*.31,-i*.7)
    P(sway(bt,1560,320,1.1,6.5,-2))
    cut('canopy',.08,18)
    # ---------- side plants ----------
    def plant(inner,ox,oy,amp,dur,dl): P(sway(inner,ox,oy,amp,dur,dl))
    plant(bigleaf(-40,900,450,62,-82,0.05,'#3a8a3e','#5aa548','#1d5a2e'),-40,900,1.1,6.8,0)
    plant(bigleaf(110,860,170,30,-62,0.08,'#4a9a42','#7cc35a','#24793e'),110,860,2.2,4.6,-1.2)
    plant(budstem([(70,900),(60,780),(50,640),(58,540),(70,470)],[(1.2,-132,'o',52),(1.6,-48,'p',50),(2.2,-132,'o',48),(2.6,-54,'p',46),(3.2,-126,'o',44),(3.6,-54,'p',42),(3.95,-89,'o',40)],2.4,scale=1.2),70,900,1.8,5.2,-2)
    plant(budstem([(130,900),(140,800),(150,700),(160,610)],[(1.0,-132,'p',46),(1.6,-48,'p',42),(2.3,-126,'p',40),(2.95,-72,'p',36)],2.2,scale=1.2),130,900,2.4,4.3,-.7)
    plant(bigleaf(1560,930,500,84,-98,-0.04,'#3a7f3c','#6cae4c','#1d4a2a',side=-1,ribw=2),1560,930,1,7.2,-3)
    plant(bigleaf(1420,720,110,26,-130,-0.1,'#4a9a42','#86c95a','#24793e',side=-1)+bigleaf(1430,730,100,22,-160,-0.1,'#3f9a44','#7cc35a','#24793e',side=-1),1425,725,3,3.9,-1.4)
    plant(budstem([(1440,900),(1420,780),(1400,640),(1370,540),(1350,470)],[(1.2,-48,'o',52),(1.6,-132,'p',50),(2.2,-48,'o',48),(2.6,-126,'p',46),(3.2,-54,'p',44),(3.6,-126,'p',42),(3.95,-93,'p',40)],2.4,scale=1.2),1440,900,1.8,5.6,-2.6)
    plant(budstem([(1390,920),(1380,820),(1360,720),(1340,630)],[(1.0,-48,'o',46),(1.6,-132,'o',42),(2.3,-54,'o',40),(2.95,-108,'o',36)],2.2,scale=1.2),1390,920,2.4,4.7,-.3)
    cut('side',.06,22)
    # ---------- front foliage ----------
    def sp(d,fill,ox,oy,amp,dur,dl): P(sway(f'<path d="{d}" fill="{fill}"/>',ox,oy,amp,dur,dl))
    sp(spikes([(-20,930),(200,900),(330,920)],13,150,230,-112,-58,28,11,5),gradu(s,'bl1',[(0,'#3aa86a'),(.5,'#1d7c58'),(1,'#124a50')],0,700,0,940),150,940,1.1,5.4,-1)
    sp(spikes([(1300,930),(1420,890),(1530,870)],10,130,220,-120,-80,28,11,6),gradu(s,'br1',[(0,'#33a068'),(.5,'#177256'),(1,'#124a50')],0,680,0,940),1420,930,1.1,5.9,-2.2)
    sp(spikes([(380,970),(1000,970)],22,110,170,-128,-52,26,10,7),gradu(s,'cf',[(0,'#7fe2c4'),(.35,'#1fa684'),(1,'#0b5a52')],0,800,0,960),690,980,.7,6.4,-3)
    P(sway(fan2(s,640,944,118,13,'#ebe46a','#178a6a'),640,944,1.6,4.8,-1.5))
    P(sway(fan2(s,350,955,80,11,'#e0e060','#14805e'),350,955,1.8,4.2,-.4))
    sp(spikes([(-40,960),(-10,940),(150,930),(340,950)],17,140,290,-100,-48,30,12,8),gradu(s,'dl',[(0,'#1a8a4e'),(.4,'#0f5f48'),(.85,'#0f4650'),(1,'#12425b')],0,720,0,950),150,960,1.3,5,-.8)
    sp(spikes([(1080,980),(1300,935),(1540,900)],18,110,220,-150,-100,30,12,9),gradu(s,'dr',[(0,'#1c8a5c'),(.4,'#0c5f48'),(.85,'#0e4650'),(1,'#12425b')],0,700,0,950),1300,960,1.2,5.6,-2.7)
    P(sway(cattail(880,950,930,775,'#e9d44c',bend=-10,w=2,tl=26,tw=7),880,950,3,3.4,-.6))
    P(sway(cattail(900,950,1035,820,'#e9d44c',bend=30,w=2,tl=26,tw=7),900,950,3.4,3.9,-1.9))
    s.p('M-200 870H1704V1200H-200Z',gradu(s,'fade',[(0,'#12425b',0),(.6,'#12425b',.7),(1,'#14425b',1)],0,870,0,936))
    cut('front',0,26)
    return ''.join(s.defs),L
def build(path):
    """static composite (no animation needed) for reference / non-JS use"""
    defs,L=build_layers()
    body=''.join(m for _,_,_,m in L)
    txt=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1504 940" width="1504" height="940" preserveAspectRatio="xMidYMax slice"><defs>{defs}</defs>{body}</svg>'
    import re; txt=re.sub(r' (-)',r'\1',txt)
    from palette import grade; txt=grade(txt)
    open(path,'w').write(txt); return len(txt)

import os as _os
_HERE=_os.path.dirname(_os.path.abspath(__file__))
_SITE=_os.environ.get('SNAP_SITE') or (_os.path.join(_HERE,'..','site') if _os.path.isdir(_os.path.join(_HERE,'..','site')) else _os.path.join(_HERE,'..'))
if __name__=='__main__':
    print(build(_os.path.join(_SITE,'svg','hero.svg')))
