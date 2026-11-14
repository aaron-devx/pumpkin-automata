"""helpers that wrap SVG markup in CSS-animated groups (keyframes live in index.html)"""
from lib import f
def sway(inner,ox,oy,amp=1.2,dur=6,delay=0,cls='an-sway'):
    return f'<g class="{cls}" style="transform-origin:{f(ox)}px {f(oy)}px;--a:{amp}deg;--d:{dur}s;--dl:{delay}s">{inner}</g>'
def drift(inner,x_left,x_right,dur,phase=0.0,vw=1504,pad=80):
    """inner spans x_left..x_right in user units; loops right->offscreen, reappears left. phase 0..1 = progress at t=0"""
    a=-pad-x_right; b=vw+pad-x_left
    p0=(0-a)/(b-a)
    dl=-dur*((p0+phase)%1.0)
    return f'<g class="an-drift" style="--a:{f(a)}px;--b:{f(b)}px;--d:{dur}s;--dl:{f(dl)}s">{inner}</g>'
def drift_rev(inner,x_left,x_right,dur,phase=0.0,vw=1504,pad=80):
    a=vw+pad-x_left; b=-pad-x_right
    p0=(0-a)/(b-a)
    dl=-dur*((p0+phase)%1.0)
    return f'<g class="an-drift" style="--a:{f(a)}px;--b:{f(b)}px;--d:{dur}s;--dl:{f(dl)}s">{inner}</g>'
def bird(x,y,s,fill='#fff',dur=60,phase=0,flap=.55,bob=3.2,rev=False,vw=1504,seed=0):
    """flapping bird with two wings hinged at body origin; drifts across the scene"""
    wl='M0 0C-3.5-3.2-7-4.6-11-3.6C-7-6.8-2.6-5.8 0.6-1.6Z'
    wr='M0 0C3.5-3.6 7.6-5.6 12-4.6C7.8-7.6 2.8-6.6-0.6-1.6Z'
    body='M-1.6 0.4C-0.6-1 0.6-1 1.6 0.4C0.6 1.4-0.6 1.4-1.6 0.4Z'
    fd=-(seed*0.173)%flap
    core=(f'<g class="an-bob" style="--d:{bob}s;--dl:{-(seed*0.61)%bob:.2f}s;--v:{f(1.2+seed%3*0.4)}px">'
          f'<path class="an-wl" style="--f:{flap}s;--fd:{fd:.2f}s" d="{wl}" fill="{fill}"/>'
          f'<path class="an-wr" style="--f:{flap}s;--fd:{fd:.2f}s" d="{wr}" fill="{fill}"/>'
          f'<path d="{body}" fill="{fill}"/></g>')
    # drift: in scaled local units
    a,b=((vw+80-x)/s,(-80-x)/s) if rev else ((-80-x)/s,(vw+80-x)/s)
    p0=(0-a)/(b-a); dl=-dur*((p0+phase)%1.0)
    flip=' scale(-1 1)' if rev else ''
    return (f'<g transform="translate({f(x)} {f(y)}) scale({s/10:.3f})">'
            f'<g class="an-drift" style="--a:{f(a*10)}px;--b:{f(b*10)}px;--d:{dur}s;--dl:{f(dl)}s"><g transform="scale(1 1){flip}">{core}</g></g></g>')
BAT_FILL='#1d1428'; BAT_STRUT='#3d2c55'
def _bat_wing(m):
    """one wing hinged at body (0,0); m=-1 left, 1 right. scalloped trailing edge between finger tips"""
    def pt(x,y): return f'{f(x*m)} {f(y)}'
    membrane=(f'M{pt(-.8,-1)}C{pt(-3,-3.4)} {pt(-5,-4.6)} {pt(-7,-4.4)}C{pt(-9.6,-4)} {pt(-12,-2.6)} {pt(-13.4,-.8)}'
              f'Q{pt(-10.8,.4)} {pt(-10,2.8)}Q{pt(-8.2,.8)} {pt(-6,2.4)}Q{pt(-3.6,.6)} {pt(-.8,1.6)}Z')
    struts=''.join(f'<path d="M{pt(-7,-4.2)}L{pt(x,y)}" stroke="{BAT_STRUT}" stroke-width=".45" stroke-linecap="round"/>'
                   for x,y in ((-13.2,-.8),(-10,2.5),(-6,2.1)))
    return f'<path d="{membrane}" fill="{BAT_FILL}"/>{struts}'
def bat(x,y,s,dur=60,phase=0,flap=.22,zig=1.7,rev=False,vw=1504,seed=0):
    """bat: membrane wings with finger struts, ears; fast flap + erratic zigzag while drifting across"""
    fd=-(seed*0.071)%flap
    zx=f(3+seed%3*1.5); zy=f(4+seed%2*2)
    head=(f'<ellipse cx="0" cy=".6" rx="1.5" ry="2.3" fill="{BAT_FILL}"/><circle cx="0" cy="-1.7" r="1.3" fill="{BAT_FILL}"/>'
          f'<path d="M-1.1-2.2L-1-4.2L-.2-2.8ZM1.1-2.2L1-4.2L.2-2.8Z" fill="{BAT_FILL}"/>')
    core=(f'<g class="an-zig" style="--d:{zig}s;--dl:{-(seed*0.37)%zig:.2f}s;--zx:{zx}px;--zy:{zy}px">'
          f'<g class="an-bwl" style="--f:{flap}s;--fd:{fd:.2f}s">{_bat_wing(1)}</g>'
          f'<g class="an-bwr" style="--f:{flap}s;--fd:{fd:.2f}s">{_bat_wing(-1)}</g>{head}</g>')
    a,b=((vw+80-x)/s,(-80-x)/s) if rev else ((-80-x)/s,(vw+80-x)/s)
    p0=(0-a)/(b-a); dl=-dur*((p0+phase)%1.0)
    return (f'<g transform="translate({f(x)} {f(y)}) scale({s/10:.3f})">'
            f'<g class="an-drift" style="--a:{f(a*10)}px;--b:{f(b*10)}px;--d:{dur}s;--dl:{f(dl)}s">{core}</g></g>')
def smoke(x,y,n=6,dur=7.5,grad='url(#puff)',r=9,rise=190,drift_x=46,scale=2.8):
    o=''
    for i in range(n):
        o+=(f'<circle class="an-puff" cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{grad}" '
            f'style="--d:{dur}s;--dl:{-dur*i/n:.2f}s;--rx:{drift_x}px;--ry:{-rise}px;--s:{scale}"/>')
    return f'<g class="smoke">{o}</g>'
def shimmer(inner,dur=5,delay=0,dx=8):
    return f'<g class="an-shim" style="--d:{dur}s;--dl:{delay}s;--dx:{dx}px">{inner}</g>'
