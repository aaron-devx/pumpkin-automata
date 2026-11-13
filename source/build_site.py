"""Assemble site/index.html from template.html + generated SVG art.
Animated art (hero layers, why scene, footer) is inlined so CSS keyframes and parallax can drive it.
Run: python3 hero.py && python3 scenes.py && python3 build_site.py"""
import re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
HERE=os.path.dirname(os.path.abspath(__file__))
import os as _os
_HERE=_os.path.dirname(_os.path.abspath(__file__))
_SITE=_os.environ.get('SNAP_SITE') or (_os.path.join(_HERE,'..','site') if _os.path.isdir(_os.path.join(_HERE,'..','site')) else _os.path.join(_HERE,'..'))
SITE=_SITE
def prefix_ids(txt,p):
    txt=re.sub(r'\bid="([^"]+)"',lambda m:f'id="{p}-{m.group(1)}"',txt)
    txt=re.sub(r'url\(#([^)]+)\)',lambda m:f'url(#{p}-{m.group(1)})',txt)
    return txt
def compact(t): return re.sub(r' (-)',r'\1',t)
def hero_markup():
    import hero
    defs,layers=hero.build_layers()
    out=[f'<svg class="defs" aria-hidden="true" focusable="false" width="0" height="0"><defs>{prefix_ids(defs,"h")}</defs></svg>']
    for name,fac,depth,m in layers:
        m=prefix_ids(m,'h')
        out.append(f'<div class="layer layer-{name}" data-speed="{fac}" data-depth="{depth}"><svg class="lay" viewBox="0 0 1504 940" preserveAspectRatio="{'xMidYMin' if name=='canopy' else 'xMidYMax'} slice" aria-hidden="true" focusable="false">{m}</svg></div>')
    return compact('\n'.join(out))
def inline_svg(fn,p,cls,par=None):
    t=open(os.path.join(SITE,'svg',fn)).read()
    t=prefix_ids(t,p)
    t=re.sub(r'<svg ([^>]*?) width="\d+" height="\d+"',lambda m:f'<svg class="{cls}" aria-hidden="true" focusable="false" {m.group(1)}',t,count=1)
    if par: t=re.sub(r'preserveAspectRatio="[^"]+"',f'preserveAspectRatio="{par}"',t,count=1)
    return t
STAR='<svg width="30" height="29" viewBox="0 0 24 23"><path d="M12 1l3.1 6.6 7.2.9-5.3 5 1.4 7.1L12 17.1 5.6 20.6 7 13.5l-5.3-5 7.2-.9z" fill="#fbbf2e"/></svg>'
WAVE='<svg width="22" height="22" viewBox="0 0 22 22"><circle cx="11" cy="11" r="10" fill="#1f5fe0"/><path d="M2 9c3-2 6 1 9-1s6-2 9 0M2 13c3-2 6 1 9-1s6-2 9 0M4 17c3-2 5 1 7 0s5-2 7 0" stroke="#fff" stroke-width="1.6" fill="none"/></svg>'
PIN='<svg width="14" height="16" viewBox="0 0 14 16"><path d="M7 15s5.5-5 5.5-9A5.5 5.5 0 0 0 1.5 6c0 4 5.5 9 5.5 9z" fill="#22c1c3"/><circle cx="7" cy="6" r="2" fill="#fff"/></svg>'
def cards():
    C=[('card1','Kintamani',4,'8/10',100),('card2','Nusa Penida',5,'9/10',150),('card3','Broken Beach',4,'8/10',120)]
    return ''.join(f'<article class="card" data-card><div class="img"><img src="svg/{c}.svg" alt="{n} illustration" width="398" height="330" loading="lazy"></div><div class="body"><h3>{n}</h3><div class="rate"><span class="stars" aria-label="{st} stars">{STAR*st}</span><span class="dot"></span>{WAVE}<span>{r}</span></div><div class="loc">{PIN}Bali, indonesia</div><div class="price">$ {p}<span>/Person</span></div></div></article>' for c,n,st,r,p in C)
def plans():
    chk='<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><circle cx="9" cy="9" r="8" fill="currentColor"/><path d="M5.2 9.2l2.5 2.4 5-5" stroke="var(--bg)" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    P=[('Adventure<br>Explorer',599,'Thrill Seeker’s Delight',['Guided Mountain Trek','White-Water Rafting','Camping Under The Stars'],'Book Your Adventure Now',''),
       ('Cultural<br>Discovery',749,'Cultural Odyssey',['Guided City Tours','Traditional Cooking Classes','Cultural Performances'],'Start Your Cultural Journey','dk'),
       ('Relaxation<br>Retreat',899,'Tranquil Escapes',['Spa Retreat','Beachside Relaxation','Yoga And Meditation Sessions'],'Book Your Adventure Now','')]
    return ''.join(f'<div class="plan-col" data-plan><div class="plan {k}"><h3>{h}</h3><div class="amt"><sup>$</sup>{a}</div><h5>{t}</h5><hr><ul>{"".join(f"<li>{chk}{x}</li>" for x in L)}</ul><a class="cta" href="#">{c}</a></div><div class="review">Photo Review</div></div>' for h,a,t,L,c,k in P)
def main():
    tpl=open(os.path.join(HERE,'template.html')).read()
    tpl=tpl.replace('{{HERO_ART}}',hero_markup()).replace('{{CARDS}}',cards()).replace('{{PLANS}}',plans())
    tpl=tpl.replace('{{WHY_SCENE}}',inline_svg('why_scene.svg','w','scene-svg','xMinYMax slice'))
    tpl=tpl.replace('{{FOOTER_ART}}',inline_svg('footer_art.svg','f','foot-svg','xMidYMax slice'))
    open(os.path.join(SITE,'index.html'),'w').write(tpl)
    import shutil; shutil.copy(os.path.join(HERE,'main.js'),os.path.join(SITE,'main.js'))
    print('index.html',len(tpl))
if __name__=='__main__': main()
