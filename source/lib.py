import math, random
PREC=[1]
def f(v):
    if PREC[0]==0: return str(int(round(v)))
    s=('%.1f'%v)
    s=s[:-2] if s.endswith('.0') else s
    return s.replace('0.','.',1) if s.startswith('0.') else (s.replace('-0.','-.',1) if s.startswith('-0.') else s)
class S:
    def __init__(s,w,h,vb=None):
        s.w,s.h=w,h; s.defs=[]; s.el=[]; s.ids=set(); s.vb=vb or f'0 0 {w} {h}'
    def add(s,x): s.el.append(x); return s
    def lg(s,id,stops,x1=0,y1=0,x2=0,y2=1,units=None):
        if id in s.ids: return f'url(#{id})'
        s.ids.add(id)
        u=f' gradientUnits="userSpaceOnUse"' if units else ''
        st=''.join(f'<stop offset="{o}" stop-color="{c}"'+(f' stop-opacity="{a}"' if a!=1 else '')+'/>' for o,c,*r in stops for a in [r[0] if r else 1])
        s.defs.append(f'<linearGradient id="{id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{u}>{st}</linearGradient>')
        return f'url(#{id})'
    def rg(s,id,stops,cx=.5,cy=.5,r=.5):
        if id in s.ids: return f'url(#{id})'
        s.ids.add(id)
        st=''.join(f'<stop offset="{o}" stop-color="{c}"'+(f' stop-opacity="{a}"' if a!=1 else '')+'/>' for o,c,*r2 in stops for a in [r2[0] if r2 else 1])
        s.defs.append(f'<radialGradient id="{id}" cx="{cx}" cy="{cy}" r="{r}">{st}</radialGradient>')
        return f'url(#{id})'
    def raw_def(s,x): s.defs.append(x)
    def p(s,d,fill='none',**kw):
        a=''.join(f' {k.replace("_","-")}="{v}"' for k,v in kw.items())
        return s.add(f'<path d="{d}" fill="{fill}"{a}/>')
    def g(s,inner,**kw):
        a=''.join(f' {k.replace("_","-")}="{v}"' for k,v in kw.items())
        return s.add(f'<g{a}>{inner}</g>')
    def out(s,path,extra=''):
        txt=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{s.vb}" width="{s.w}" height="{s.h}" preserveAspectRatio="xMidYMid slice"{extra}><defs>{"".join(s.defs)}</defs>{"".join(s.el)}</svg>'
        import re
        txt=re.sub(r' (-)',r'\1',txt)
        from palette import grade
        txt=grade(txt)
        open(path,'w').write(txt); return len(txt)

def pts(*a): return ' '.join(f(v) for v in a)
def poly(points,close=True):
    d='M'+' L'.join(f'{f(x)} {f(y)}' for x,y in points)
    return d+('Z' if close else '')
def smooth(points,close=True,t=0.5):
    """Catmull-Rom -> cubic bezier through points"""
    P=points; n=len(P)
    if close: get=lambda i:P[i%n]
    else: get=lambda i:P[max(0,min(n-1,i))]
    d=f'M{f(P[0][0])} {f(P[0][1])}'
    rng=range(n) if close else range(n-1)
    for i in rng:
        p0,p1,p2,p3=get(i-1),get(i),get(i+1),get(i+2)
        c1=(p1[0]+(p2[0]-p0[0])*t/3,p1[1]+(p2[1]-p0[1])*t/3)
        c2=(p2[0]-(p3[0]-p1[0])*t/3,p2[1]-(p3[1]-p1[1])*t/3)
        d+=f'C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}'
    return d+('Z' if close else '')

def _v(a): r=math.radians(a); return math.cos(r),math.sin(r)
def leaf(x,y,L,W,ang,bend=0.0,tipw=0.0):
    """pointed leaf, base (x,y), length L, half-width W, angle deg (0=right, -90=up), bend: tip lateral offset fraction"""
    dx,dy=_v(ang); nx,ny=-dy,dx
    tx,ty=x+dx*L+nx*bend*L,y+dy*L+ny*bend*L
    def P(a,b): # a along, b lateral (plus bend curve)
        bb=bend*L*(a**2)
        return x+dx*a*L+nx*(b+bb), y+dy*a*L+ny*(b+bb)
    a1=P(.18,W*1.05);a2=P(.65,W*0.95);b1=P(.65,-W*0.95);b2=P(.18,-W*1.05)
    return f'M{f(x)} {f(y)}C{f(a1[0])} {f(a1[1])} {f(a2[0])} {f(a2[1])} {f(tx)} {f(ty)}C{f(b1[0])} {f(b1[1])} {f(b2[0])} {f(b2[1])} {f(x)} {f(y)}Z'
def leaf_half(x,y,L,W,ang,bend=0.0,side=1):
    dx,dy=_v(ang); nx,ny=-dy,dx
    def P(a,b):
        bb=bend*L*(a**2)
        return x+dx*a*L+nx*(b+bb), y+dy*a*L+ny*(b+bb)
    t=P(1,0);a1=P(.18,side*W*1.05);a2=P(.65,side*W*.95);m=P(.5,0)
    return f'M{f(x)} {f(y)}C{f(a1[0])} {f(a1[1])} {f(a2[0])} {f(a2[1])} {f(t[0])} {f(t[1])}Q{f(m[0])} {f(m[1])} {f(x)} {f(y)}Z'
def midrib(x,y,L,ang,bend=0.0,frac=.92):
    dx,dy=_v(ang); nx,ny=-dy,dx
    def P(a): bb=bend*L*a*a; return x+dx*a*L+nx*bb, y+dy*a*L+ny*bb
    m=P(frac/2); t=P(frac)
    cx,cy=2*m[0]-(x+t[0])/2,2*m[1]-(y+t[1])/2
    return f'M{f(x)} {f(y)}Q{f(cx)} {f(cy)} {f(t[0])} {f(t[1])}'
def blade(x,y,L,W,ang,bend=0.0):
    """grass blade: wide base tapering to tip, curved"""
    dx,dy=_v(ang); nx,ny=-dy,dx
    def P(a,b):
        bb=bend*L*a*a
        return x+dx*a*L+nx*(b+bb), y+dy*a*L+ny*(b+bb)
    l0=P(0,W);r0=P(0,-W);c1=P(.55,W*.8);c2=P(.55,-W*.7);t=P(1,0)
    return f'M{f(l0[0])} {f(l0[1])}Q{f(c1[0])} {f(c1[1])} {f(t[0])} {f(t[1])}Q{f(c2[0])} {f(c2[1])} {f(r0[0])} {f(r0[1])}Z'
def fan_dome(cx,cy,r,n=14,c1='#f2e04a',c2='#8cc63f'):
    """semicircular striped tuft like the reference bases. returns svg string"""
    out=[]
    for i in range(n):
        a0=180+i*180/n; a1=180+(i+.62)*180/n
        rr=r*(0.9+0.1*((i*7)%3)/2)
        x0,y0=cx+rr*math.cos(math.radians(a0)),cy+rr*math.sin(math.radians(a0))
        x1,y1=cx+rr*math.cos(math.radians(a1)),cy+rr*math.sin(math.radians(a1))
        out.append(f'M{f(cx)} {f(cy)}L{f(x0)} {f(y0)}A{f(rr)} {f(rr)} 0 0 1 {f(x1)} {f(y1)}Z')
    return ''.join(out)
def pine(x,base,h,w,layers=4):
    """returns (full,half) path strings for a stylized pine"""
    top=base-h; pts_l=[];pts_r=[]
    for i in range(layers):
        yy=top+h*(i+1)/layers; ww=w*(0.35+0.65*(i+1)/layers)
        yin=yy-h/layers*0.25; win=ww*0.55
        pts_r+= [(x+ww/2,yy),(x+win/2,yin)] if i<layers-1 else [(x+ww/2,yy)]
    full=[(x,top)]+pts_r+[(x,base)]
    left=[(2*x-px,py) for px,py in pts_r][::-1]
    return poly([(x,top)]+pts_r+[(x+w*0.06,base),(x-w*0.06,base)]+left), poly(full)
def cloud(x,y,w,h=None,bumps=None):
    """flat-bottom cloud from left x, baseline y"""
    h=h or w*0.18
    bumps=bumps or [(.12,.45),(.3,.8),(.52,1.0),(.72,.7),(.9,.4)]
    d=f'M{f(x)} {f(y)}'
    prev=x
    for bx,bh in bumps:
        cx=x+bx*w; r=bh*h
        d+=f'Q{f((prev+cx)/2)} {f(y-r*1.6)} {f(cx+ (w*0.09))} {f(y-r*0.4)}'
        prev=cx+w*0.09
    d+=f'Q{f(x+w)} {f(y-h*0.2)} {f(x+w)} {f(y)}Z'
    return d
def bird(x,y,s):
    return f'M{f(x-s)} {f(y-s*.35)}Q{f(x-s*.45)} {f(y-s*.55)} {f(x)} {f(y)}Q{f(x+s*.5)} {f(y-s*.75)} {f(x+s*1.1)} {f(y-s*.6)}Q{f(x+s*.45)} {f(y-s*.3)} {f(x)} {f(y+s*.15)}Q{f(x-s*.4)} {f(y-s*.25)} {f(x-s)} {f(y-s*.35)}Z'
def bud(x,y,L,W,ang):
    return leaf(x,y,L,W,ang)
def stem(points,w=2,c='#2f8f4e'):
    return f'<path d="{smooth(points,False)}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
