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
    from palette import grade
    return grade(compact('\n'.join(out)), tint_whites=True)
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
    C=[
        ('card1','Suffix 01','DFA','Σ={0,1}','try 01'),
        ('card2','Contains aba','DFA','Σ={a,b}','try aba'),
        ('card3','a then b*','DFA','Σ={a,b}','try abbb'),
    ]
    return ''.join(
        f'<article class="card" data-card><div class="img"><img src="svg/{c}.svg" alt="{n} illustration" width="398" height="330" loading="lazy"></div>'
        f'<div class="body"><h3>{n}</h3><div class="meta"><span class="pill">{k}</span><span>{sig}</span></div>'
        f'<p class="try">{hint}</p></div></article>'
        for c,n,k,sig,hint in C
    )
TCARDS_PER_PAGE=2
def tcards():
    # (title, kind·sigma, quote html, source, machine id, input, avatar)
    T=[
        ('Ends with 10','DFA · Σ={0,1}','Input <strong>110</strong> → accept. Input <strong>101</strong> → reject. Last two symbols decide.','Week 7','dfa-ends-10','110','frankenstein'),
        ('Contains bab','DFA · Σ={a,b}','Input <strong>ababb</strong> → accept. Input <strong>abba</strong> → reject.','Week 7','dfa-contains-bab','ababb','mummy'),
        ('a then b*','DFA · Σ={a,b}','Input <strong>abbb</strong> → accept. Any <strong>b</strong> first → trap.','Week 7','dfa-a-then-bstar','abbb','pumpkin-head'),
        ('NFA slide','NFA · Σ={0,1}','Input <strong>1110</strong> → ends in C. Input <strong>0</strong> → accept.','Week 10','nfa-abc-slide','1110','vampire'),
        ('Begins with 0','DFA · Σ={0,1}','Input <strong>010</strong> → accept. Input <strong>10</strong> → reject. Dead state catches a leading 1.','Week 7','dfa-begins-0','010','witch'),
        ('b* trap','DFA · Σ={a,b}','Input <strong>b</strong> → reject. Trap state never leaves.','Week 7','dfa-a-then-bstar','b','wolf'),
    ]
    def one(c):
        n,pl,q,dt,mid,inp,av=c
        return (f'<article class="tcard" data-machine="{mid}" data-input="{inp}"><img class="av" src="avatars/{av}.webp" alt="" width="80" height="80" loading="lazy">'
            f'<div class="nm"><button type="button" class="card-go" aria-label="Open {n} in the trace lab with input {inp}">{n}</button></div>'
            f'<div class="pl">{pl}</div><q>{q}</q><div class="dt">{dt}</div><img class="lf" src="svg/leaf_corner.svg" alt=""></article>')
    pages=[''.join(one(c) for c in T[i:i+TCARDS_PER_PAGE]) for i in range(0,len(T),TCARDS_PER_PAGE)]
    return ''.join(f'<div class="cpage" role="group" aria-roledescription="slide" aria-label="Page {i+1} of {len(pages)}">{p}</div>' for i,p in enumerate(pages))
def plans():
    chk='<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><circle cx="9" cy="9" r="8" fill="currentColor"/><path d="M5.2 9.2l2.5 2.4 5-5" stroke="var(--bg)" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    P=[
        ('Pick<br>Machine','01','Choose a finite acceptor',['Open the dropdown in the hero','Match the slide problem','DFA or NFA badge shown'],'#lab',''),
        ('Type<br>String','02','Symbols from Σ',['Use only letters in Σ','Example: 1010 or bab','Invalid chars → INVALID'],'#top','dk'),
        ('Trace +<br>Verdict','03','Step the run',['Slider or Next / Back','Highlight active state(s)','ACCEPT or REJECT at end'],'#lab',''),
    ]
    return ''.join(
        f'<div class="plan-col" data-plan><div class="plan {k}"><h3>{h}</h3><div class="amt step-num">{a}</div>'
        f'<h5>{t}</h5><hr><ul>{"".join(f"<li>{chk}{x}</li>" for x in L)}</ul>'
        f'<a class="cta" href="{c}">Go</a></div><div class="review">AL102</div></div>'
        for h,a,t,L,c,k in P
    )
def copy_automata():
    import shutil
    dst=os.path.join(SITE,'automata')
    os.makedirs(dst,exist_ok=True)
    for name in ('machines.js','simulator.js','automata_app.js'):
        shutil.copy(os.path.join(HERE,'automata',name),os.path.join(dst,name))
def main():
    tpl=open(os.path.join(HERE,'template.html')).read()
    tpl=tpl.replace('{{HERO_ART}}',hero_markup()).replace('{{CARDS}}',cards()).replace('{{TCARDS}}',tcards()).replace('{{PLANS}}',plans())
    tpl=tpl.replace('{{WHY_SCENE}}',inline_svg('why_scene.svg','w','scene-svg','xMinYMax slice'))
    tpl=tpl.replace('{{FOOTER_ART}}',inline_svg('footer_art.svg','f','foot-svg','xMidYMax slice'))
    open(os.path.join(SITE,'index.html'),'w').write(tpl)
    import shutil; shutil.copy(os.path.join(HERE,'main.js'),os.path.join(SITE,'main.js'))
    copy_automata()
    print('index.html',len(tpl))
if __name__=='__main__': main()
