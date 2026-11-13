from lib import *
import math
PINK='#f2727f'; PINK2='#e8566a'; ORNG='#f79a5a'; ORNG2='#f0803c'
def bigleaf(x,y,L,W,ang,bend=0,dark='#1f7a4a',light='#3aa05a',rib='#0f5a36',ribw=1.5,side=1):
    s=f'<path d="{leaf(x,y,L,W,ang,bend)}" fill="{dark}"/>'
    s+=f'<path d="{leaf_half(x,y,L,W,ang,bend,side)}" fill="{light}"/>'
    if rib: s+=f'<path d="{midrib(x,y,L,ang,bend)}" fill="none" stroke="{rib}" stroke-width="{ribw}" stroke-linecap="round"/>'
    return s
def budstem(points,buds,sw=2,sc='#3c9a52',scale=1.0):
    """buds: list of (index along points (float), angle, color,len)"""
    out=stem(points,sw,sc)
    for t,ang,col,L in buds:
        i=int(t); fr=t-i
        x=points[i][0]+(points[min(i+1,len(points)-1)][0]-points[i][0])*fr
        y=points[i][1]+(points[min(i+1,len(points)-1)][1]-points[i][1])*fr
        L=L*scale
        # short pedicel
        dx,dy=math.cos(math.radians(ang)),math.sin(math.radians(ang))
        px,py=x+dx*L*0.35,y+dy*L*0.35
        out+=f'<path d="M{f(x)} {f(y)}L{f(px)} {f(py)}" stroke="{sc}" stroke-width="{f(sw*0.8)}" stroke-linecap="round"/>'
        c2={'p':(PINK,PINK2),'o':(ORNG,ORNG2)}[col]
        out+=tulip(px,py,L,L*0.36,ang,c2[0],c2[1])
    return out
def tuft(x,y,sc=1.0,c1='#c8d94a',c2='#9cc23c'):
    d=['','']
    for i,a in enumerate([-150,-125,-105,-90,-75,-55,-30]):
        L=(14+8*(1-abs(a+90)/60))*sc
        d[i%2]+=blade(x,y,L,2.2*sc,a,0.05*(1 if a>-90 else -1))
    return f'<path d="{d[0]}" fill="{c2}"/><path d="{d[1]}" fill="{c1}"/>'
def grassfan(x,y,n,L,a0,a1,W,colors,bendk=0.12,jit=0.25,seed=1):
    import random; R=random.Random(seed); out=''
    old=PREC[0]; PREC[0]=0 if L>=60 else old
    for i in range(n):
        a=a0+(a1-a0)*i/max(1,n-1)
        LL=L*(1-jit+R.random()*jit*2)
        b=bendk*(1 if a> -90 else -1)
        out+=f'<path d="{blade(x+R.uniform(-W,W),y,LL,W,a,b)}" fill="{colors[i%len(colors)]}"/>'
    PREC[0]=old
    return out
def dome(cx,cy,r,c1='#e3e05a',c2='#a6cc45',bg='#7fb83a'):
    return f'<path d="M{f(cx-r)} {f(cy)}A{f(r)} {f(r)} 0 0 1 {f(cx+r)} {f(cy)}Z" fill="{bg}"/><path d="{fan_dome(cx,cy,r,16)}" fill="{c1}"/><path d="{fan_dome(cx,cy,r*0.62,12)}" fill="{c2}"/>'
def cattail(x0,y0,x1,y1,c='#e8d24a',sc='#3c9a52',w=1.6,bend=20):
    mx,my=(x0+x1)/2+bend,(y0+y1)/2
    ang=math.degrees(math.atan2(y1-my,x1-mx))
    return f'<path d="M{f(x0)} {f(y0)}Q{f(mx)} {f(my)} {f(x1)} {f(y1)}" fill="none" stroke="{sc}" stroke-width="{w}" stroke-linecap="round"/><path d="{blade(x1,y1,22,4,ang,0)}" fill="{c}"/>'
def frond(x,y,L,ang,bend=0.15,lf=None,n=14,c1='#2f9a52',c2=None,rib=None,sw=None):
    """palm/fern frond: curved rib with leaflets on both sides (leaflets merged per colour)"""
    lf=lf or L*0.28; c2=c2 or c1; rib=rib or c1
    old=PREC[0]; PREC[0]=0 if L>=120 else old
    dx,dy=math.cos(math.radians(ang)),math.sin(math.radians(ang)); nx,ny=-dy,dx
    def P(a):
        bb=bend*L*a*a; return x+dx*a*L+nx*bb, y+dy*a*L+ny*bb
    o=f'<path d="{midrib(x,y,L,ang,bend,1.0)}" fill="none" stroke="{rib}" stroke-width="{f(sw or max(1.2,L/90))}" stroke-linecap="round"/>'
    d={1:'',-1:''}
    for i in range(1,n+1):
        a=0.08+0.9*i/n; px,py=P(a); qx,qy=P(min(1,a+0.02))
        da=math.degrees(math.atan2(qy-py,qx-px))
        ll=lf*(1-0.75*a)*(0.6 if i<2 else 1)
        for sgn in (1,-1):
            d[sgn]+=blade(px,py,ll,max(1.2,ll*0.14),da+sgn*48,sgn*0.08)
    o+=f'<path d="{d[1]}" fill="{c1}"/><path d="{d[-1]}" fill="{c2}"/>'
    PREC[0]=old
    return o
def capsule(x0,y0,x1,y1,w,c):
    return f'<path d="M{f(x0)} {f(y0)}L{f(x1)} {f(y1)}" stroke="{c}" stroke-width="{f(w)}" stroke-linecap="round"/>'
def cattail(x0,y0,x1,y1,c='#e8d24a',sc='#3c9a52',w=1.6,bend=20,tl=18,tw=6):
    mx,my=(x0+x1)/2+bend,(y0+y1)/2
    ang=math.atan2(y1-my,x1-mx)
    x2,y2=x1+math.cos(ang)*tl,y1+math.sin(ang)*tl
    return f'<path d="M{f(x0)} {f(y0)}Q{f(mx)} {f(my)} {f(x1)} {f(y1)}" fill="none" stroke="{sc}" stroke-width="{w}" stroke-linecap="round"/>'+capsule(x1,y1,x2,y2,tw,c)
def streak(x,y,w,h,bumps=((.3,.25,1),(.62,.2,.7)),taper=.12):
    """flat elongated cloud: flat bottom at y, top profile from gaussian bumps"""
    pts=[]
    N=12
    for i in range(N+1):
        t=i/N
        v=0.18+sum(hh*math.exp(-((t-c)/wd)**2) for c,wd,hh in bumps)
        e=min(1,t/taper,(1-t)/taper) if taper>0 else 1
        pts.append((x+w*t,y-h*v*e))
    return smooth(pts,False)+f'L{f(x+w)} {f(y)}L{f(x)} {f(y)}Z'
_dc=[0]
def fanpalm(s,cx,cy,r,n=17,top='#f2e35a',bot='#6fb13a',a0=192,a1=348,w=0.09,base=None):
    _dc[0]+=1; gid=f'fp{_dc[0]}'
    s.raw_def(f'<radialGradient id="{gid}" cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" gradientUnits="userSpaceOnUse"><stop offset=".25" stop-color="{bot}"/><stop offset="1" stop-color="{top}"/></radialGradient>')
    o=''
    if base: o+=f'<path d="M{f(cx-r*.55)} {f(cy)}A{f(r*.55)} {f(r*.55)} 0 0 1 {f(cx+r*.55)} {f(cy)}Z" fill="{base}"/>'
    for i in range(n):
        a=a0+(a1-a0)*i/(n-1)
        L=r*(0.86+0.14*math.sin(i*1.7)**2)
        o+=f'<path d="{leaf(cx,cy,L,r*w,a)}" fill="url(#{gid})"/>'
    return o
def blob(circles):
    """union of circles as one path"""
    return ''.join(f'M{f(x-r)} {f(y)}a{f(r)} {f(r)} 0 1 0 {f(2*r)} 0a{f(r)} {f(r)} 0 1 0 {f(-2*r)} 0Z' for x,y,r in circles)
def scallop(points,bottom,bulge=0.55):
    """polyline points (left->right along top edge); arcs bulge outward (up); closed down to bottom y"""
    d=f'M{f(points[0][0])} {f(bottom)}L{f(points[0][0])} {f(points[0][1])}'
    for (x0,y0),(x1,y1) in zip(points,points[1:]):
        L=math.hypot(x1-x0,y1-y0); r=L*bulge
        d+=f'A{f(r)} {f(r)} 0 0 1 {f(x1)} {f(y1)}'
    return d+f'L{f(points[-1][0])} {f(bottom)}Z'
def scallop2(points,back,bulge=0.6):
    d=f'M{f(points[0][0])} {f(points[0][1])}'
    for (x0,y0),(x1,y1) in zip(points,points[1:]):
        r=math.hypot(x1-x0,y1-y0)*bulge; d+=f'A{f(r)} {f(r)} 0 0 1 {f(x1)} {f(y1)}'
    bp=[points[-1]]+back+[points[0]]
    sm=smooth(bp,False); return d+'L'+sm[1:].split('C',1)[0] and d+sm[sm.index('C'):]+'Z'
def fan2(s,cx,cy,r,n=15,top='#e6e05a',bot='#5aa83a',*a,**k):
    _dc[0]+=1; gid=f'fn{_dc[0]}'
    s.raw_def(f'<radialGradient id="{gid}" cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" gradientUnits="userSpaceOnUse"><stop offset=".2" stop-color="{bot}"/><stop offset=".95" stop-color="{top}"/></radialGradient>')
    o=f'<path d="M{f(cx-r)} {f(cy)}A{f(r)} {f(r)} 0 0 1 {f(cx+r)} {f(cy)}Z" fill="url(#{gid})"/>'
    st=''
    for i in range(1,n):
        a0=math.radians(180+180*i/n-1.6); a1=math.radians(180+180*i/n+1.6)
        rr=r*0.98
        st+=f'M{f(cx)} {f(cy)}L{f(cx+rr*math.cos(a0))} {f(cy+rr*math.sin(a0))}L{f(cx+rr*math.cos(a1))} {f(cy+rr*math.sin(a1))}Z'
    o+=f'<path d="{st}" fill="#f6ee8a" opacity=".85"/>'
    # notched rim
    rim=''
    for i in range(n):
        am=math.radians(180+180*(i+.5)/n)
        x,y=cx+r*math.cos(am),cy+r*math.sin(am)
        rim+=f'M{f(x)} {f(y)}m-{f(r*0.05)} 0a{f(r*0.05)} {f(r*0.05)} 0 1 0 {f(r*0.1)} 0a{f(r*0.05)} {f(r*0.05)} 0 1 0 -{f(r*0.1)} 0Z'
    o+=f'<path d="{rim}" fill="{top}"/>'
    return o
def frond2(x,y,L,ang,bend=0.1,n=12,lw=None,ll=None,spread=55,sides=(1,-1),taper=0.55,start=0.05):
    """frond with straight strap leaflets (flat diagonal tips). returns one path d"""
    lw=lw or L/n*0.95; ll=ll or L*0.45
    dx,dy=math.cos(math.radians(ang)),math.sin(math.radians(ang)); nx,ny=-dy,dx
    def P(a):
        bb=bend*L*a*a; return x+dx*a*L+nx*bb, y+dy*a*L+ny*bb
    d=''
    for i in range(n):
        a=start+(1-start)*i/n; px,py=P(a); qx,qy=P(min(1,a+0.01))
        t=math.atan2(qy-py,qx-px)
        tx,ty=math.cos(t),math.sin(t)
        lL=ll*(1-taper*a)
        for sg in sides:
            sp=math.radians(spread*(1-0.35*a))*sg
            ox,oy=math.cos(t+sp),math.sin(t+sp)
            w=lw*(1-0.4*a)
            p1=(px,py); p2=(px+ox*lL,py+oy*lL); p3=(p2[0]+tx*w*0.9,p2[1]+ty*w*0.9+0); p4=(px+tx*w,py+ty*w)
            d+=poly([p1,p2,p3,p4])
    return d
def gradu(s,id,stops,x1,y1,x2,y2):
    return s.lg(id,stops,x1,y1,x2,y2,1)
def pine2(x,b,h,w,tiers=5,c1='#2f8f52',c2='#1d6b42'):
    """layered pine: tiers with curved bottoms, two-tone"""
    o=''; top=b-h
    for i in range(tiers):
        ty=top+h*i/tiers*0.85; by=top+h*(i+1)/tiers*0.95+h*0.05
        ww=w*(0.35+0.65*(i+1)/tiers)
        apex=(x,ty-(h/tiers*0.3 if i else 0))
        L=(x-ww/2,by); R=(x+ww/2,by)
        dfull=f'M{f(apex[0])} {f(apex[1])}L{f(R[0])} {f(R[1])}Q{f(x+ww*0.25)} {f(by-h/tiers*0.25)} {f(x)} {f(by-h/tiers*0.08)}Q{f(x-ww*0.25)} {f(by-h/tiers*0.25)} {f(L[0])} {f(L[1])}Z'
        dleft=f'M{f(apex[0])} {f(apex[1])}L{f(x)} {f(by-h/tiers*0.08)}Q{f(x-ww*0.25)} {f(by-h/tiers*0.25)} {f(L[0])} {f(L[1])}Z'
        o+=f'<path d="{dfull}" fill="{c2}"/><path d="{dleft}" fill="{c1}"/>'
    o+=f'<path d="M{f(x-w*0.04)} {f(b)}h{f(w*0.08)}v-{f(h*0.08)}h-{f(w*0.08)}z" fill="#5a4a3a"/>'
    return o
def cloud2(x,y,w,h,bumps,tail_l=0,tail_r=0,shade='#dcf2fd'):
    """flat cloud with soft blue underside + thin tails"""
    body=streak(x,y,w,h,bumps,0.08)
    o=f'<path d="{streak(x+w*0.04,y+h*0.12,w*0.96,h*0.55,((.5,.35,.6),),0.1)}" fill="{shade}"/>'
    o+=f'<path d="{body}" fill="#ffffff"/>'
    if tail_r: o+=f'<path d="M{f(x+w*0.7)} {f(y)}C{f(x+w+tail_r*0.3)} {f(y-h*0.15)} {f(x+w+tail_r*0.8)} {f(y+2)} {f(x+w+tail_r)} {f(y+4)}C{f(x+w+tail_r*0.6)} {f(y+6)} {f(x+w*0.9)} {f(y+5)} {f(x+w*0.7)} {f(y)}Z" fill="#ffffff"/>'
    if tail_l: o+=f'<path d="M{f(x+w*0.3)} {f(y)}C{f(x-tail_l*0.3)} {f(y-h*0.2)} {f(x-tail_l*0.8)} {f(y-h*0.3)} {f(x-tail_l)} {f(y-h*0.35)}C{f(x-tail_l*0.6)} {f(y-h*0.1)} {f(x)} {f(y+4)} {f(x+w*0.3)} {f(y)}Z" fill="#ffffff"/>'
    return o
def twigcluster(x,y,ang,L=40,n=4,c='#0f8f8c',spread=60):
    d=''
    for i in range(n):
        a=ang-spread/2+spread*i/(n-1)
        d+=leaf(x,y,L*(0.8+0.2*(i%2)),L*0.11,a)
    return f'<path d="{d}" fill="{c}"/>'
def spikes(pts_base,n,hmin,hmax,a0,a1,wb=26,wt=10,seed=1,cut=0.5):
    """row of straight strap leaflets with flat diagonal tips; base positions along polyline pts_base"""
    import random; R=random.Random(seed)
    # resample polyline
    segs=list(zip(pts_base,pts_base[1:])); lens=[math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in segs]; tot=sum(lens)
    d=''
    for i in range(n):
        t=(i+0.5)/n*tot; k=0
        while k<len(lens)-1 and t>lens[k]: t-=lens[k]; k+=1
        (ax,ay),(bx,by)=segs[k]; u=t/lens[k]
        x,y=ax+(bx-ax)*u, ay+(by-ay)*u
        a=math.radians(a0+(a1-a0)*i/max(1,n-1)+R.uniform(-4,4))
        h=R.uniform(hmin,hmax)
        dx,dy=math.cos(a),math.sin(a); nx,ny=-dy,dx
        bl=(x-nx*wb/2,y-ny*wb/2); br=(x+nx*wb/2,y+ny*wb/2)
        tx,ty=x+dx*h,y+dy*h
        tl=(tx-nx*wt/2-dx*wt*cut,ty-ny*wt/2-dy*wt*cut); trr=(tx+nx*wt/2,ty+ny*wt/2)
        d+=poly([bl,tl,trr,br])
    return d

def tulip(x,y,L,W,ang,c1,c2):
    a=math.radians(ang); dx,dy=math.cos(a),math.sin(a); nx,ny=-dy,dx
    prof=[(0,0.12),(0.2,0.3),(0.45,0.48),(0.65,0.5),(0.82,0.38),(0.94,0.18),(1,0)]
    R=[(x+dx*L*t+nx*W*w,y+dy*L*t+ny*W*w) for t,w in prof]
    Lf=[(x+dx*L*t-nx*W*w,y+dy*L*t-ny*W*w) for t,w in prof]
    full=smooth(R+Lf[::-1][1:],True)
    half=smooth(R+[(x+dx*L*t,y+dy*L*t) for t in (0.7,0.3,0)],True)
    return f'<path d="{full}" fill="{c1}"/><path d="{half}" fill="{c2}"/>'
