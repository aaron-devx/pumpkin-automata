"""Shared figures: witch in deck chair + sitting black cat (why scene coords; hero reuses scaled)."""
from comp import capsule
from anim import sway

def _p(d,fill='none',**kw):
    a=''.join(f' {k.replace("_","-")}="{v}"' for k,v in kw.items())
    return f'<path d="{d}" fill="{fill}"{a}/>'

def potion(cx,cy):
    # round flask, purple liquid, cork, soft glow
    o=f'<circle cx="{cx}" cy="{cy}" r="26" fill="#c06bff" opacity=".18"/>'
    o+=f'<path d="M{cx-5} {cy-22}H{cx+5}L{cx+5} {cy-10}C{cx+17} {cy-6} {cx+19} {cy+14} {cx+8} {cy+20}H{cx-8}C{cx-19} {cy+14} {cx-17} {cy-6} {cx-5} {cy-10}Z" fill="#e8f2ff" fill-opacity=".35" stroke="#e8f2ff" stroke-width="1.6"/>'
    o+=f'<path d="M{cx-14} {cy+2}C{cx-8} {cy-2} {cx+8} {cy+6} {cx+15} {cy+1}C{cx+16} {cy+12} {cx+10} {cy+19} {cx+7} {cy+19}H{cx-7}C{cx-12} {cy+16} {cx-15} {cy+10} {cx-14} {cy+2}Z" fill="#9b3dff"/>'
    o+=f'<rect x="{cx-4}" y="{cy-27}" width="8" height="6" rx="2" fill="#8a5a2c"/>'
    o+=f'<circle cx="{cx-3}" cy="{cy+8}" r="2" fill="#e8c6ff"/><circle cx="{cx+4}" cy="{cy+4}" r="1.4" fill="#e8c6ff"/>'
    return o

def deck_woman():
    o=''
    # ---- woman in deck chair (svg = ref crop + (100,40)) ----
    F='#3a4452'
    def bar(x0,y0,x1,y1,w): return capsule(x0,y0,x1,y1,w,F)
    o+=(bar(118,148,282,380,13))
    o+=(bar(282,268,402,280,10))
    # back canvas: sling hangs from the top of the back bar down to the seat
    o+=_p('M128 154C150 212 198 278 262 318L254 290C206 254 174 204 156 140Z','#ec7a3a')
    o+=_p('M140 150C162 208 206 268 258 304','none',stroke='#f6e3b4',**{'stroke-width':5,'opacity':.7})
    o+=_p('M250 292C300 300 360 298 404 286L410 304C380 324 300 330 262 318Z','#ec7a3a')
    o+=_p('M250 292C300 300 360 298 404 286L406 294C360 306 300 308 256 302Z','#d9602a')
    w='<g>'
    SKIN='#f2b48c'; DRESS='#4a2c5e'; DRESS2='#3a2150'; HAIR='#241a33'; HAIR_HI='#4a3a66'; HAT='#5b3a86'
    def stocking(x0,y0,x1,y1,base):
        # black stocking with purple bands (dashes across the shin)
        return capsule(x0,y0,x1,y1,15,base)+f'<path d="M{x0} {y0+8}L{x1} {y1}" stroke="#8a4fd0" stroke-width="14" stroke-dasharray="5 6"/>'
    def boot(dx):
        return f'<path transform="translate({dx} 0)" d="M424 340L442 340L448 352C460 352 470 348 474 340C476 352 468 362 452 362L420 362Z" fill="#1e1a26"/>'
    # far leg (behind): knee at seat front, shin down
    w+=stocking(396,280,414,346,'#16121c')+boot(-16)
    # long hair falls down her back, over the back sling
    w+=_p('M172 108C158 126 156 152 164 178C172 206 188 232 208 256C190 254 170 238 158 214C146 188 148 148 160 120Z',HAIR)
    w+=_p('M166 130C160 156 166 190 184 220','none',stroke=HAIR_HI,**{'stroke-width':2.5,'stroke-linecap':'round','opacity':.8})
    # bodice: back lies on the back sling, hips sit in the seat sling
    w+=_p('M170 160C188 150 206 152 214 162L284 258C290 276 284 294 268 304L246 304C220 272 186 226 160 186C156 174 160 164 170 160Z',DRESS)
    w+=_p('M160 186C186 226 220 272 246 304L258 304C234 272 200 224 176 182Z',DRESS2)
    # near leg: striped stocking + pointed boot
    w+=stocking(412,278,432,346,'#1e1a26')+boot(0)
    # skirt over the thighs, draping past the knees
    w+=_p('M258 260C300 256 360 254 410 260C426 264 432 280 430 298L436 324C418 330 400 328 388 320L392 302C340 306 290 310 246 304Z',DRESS)
    w+=_p('M300 286C340 284 380 282 412 276','none',stroke=DRESS2,**{'stroke-width':3,'stroke-linecap':'round'})
    w+=_p('M412 300L418 324','none',stroke=DRESS2,**{'stroke-width':3,'stroke-linecap':'round'})
    # resting arm across the lap
    w+=capsule(196,176,214,236,15,DRESS2)+capsule(214,236,282,256,12,SKIN)+f'<circle cx="286" cy="256" r="8" fill="{SKIN}"/>'
    # raised arm: sleeve to elbow, forearm up, hand holds potion
    w+=capsule(206,172,244,214,16,DRESS)+capsule(244,214,292,166,12,SKIN)
    w+=f'<circle cx="244" cy="214" r="8" fill="{DRESS}"/><circle cx="294" cy="162" r="8" fill="{SKIN}"/>'
    w+=potion(304,136)
    # neck, head (profile facing right), face
    w+=capsule(184,140,190,156,11,'#e8a27a')
    w+=f'<circle cx="190" cy="126" r="20" fill="{SKIN}"/><path d="M206 120L214 128L206 132Z" fill="{SKIN}"/>'
    w+='<path d="M196 120C199 123 203 123 206 120" fill="none" stroke="#2a2f3a" stroke-width="2" stroke-linecap="round"/>'
    w+='<circle cx="198" cy="130" r="4" fill="#f08a8a" opacity=".55"/>'
    w+='<path d="M201 136C204 139 208 138 210 135" fill="none" stroke="#b85a4a" stroke-width="1.8" stroke-linecap="round"/>'
    # hair cap + bangs under the brim, lock falls forward over the shoulder
    w+=_p('M170 118C170 104 186 98 202 102C210 104 212 110 210 116C204 112 200 114 196 118C192 113 186 114 182 120C178 116 174 118 172 126Z',HAIR)
    w+=_p('M174 120C168 136 172 150 184 160C192 168 198 176 196 188C204 178 204 166 196 156C186 146 180 134 182 122Z',HAIR)
    w+=_p('M178 128C176 142 182 152 190 160','none',stroke=HAIR_HI,**{'stroke-width':2,'stroke-linecap':'round'})
    # witch hat: tilted brim, bent cone, band + gold buckle
    w+=f'<ellipse cx="186" cy="104" rx="46" ry="10" fill="{HAT}" transform="rotate(-16 186 104)"/>'
    w+=_p('M160 108C166 88 168 66 170 50C171 40 165 32 152 34C162 40 168 46 174 54C186 70 196 86 206 98Z',HAT)
    w+=_p('M162 100C176 96 192 92 204 90L207 98C192 101 177 105 163 108Z','#2a1a40')
    w+='<rect x="178" y="94" width="10" height="9" rx="1.5" fill="none" stroke="#f6c84a" stroke-width="2" transform="rotate(-16 183 98)"/>'
    w+='</g>'
    o+=(w)
    o+=(bar(267,350,380,281,9)); o+=(bar(383,287,424,356,10))
    return o

def _blink(cx,cy,r,dur,begin):
    # SMIL blink: eye squashes shut for a moment, then stays open (paused by main.js under reduced motion)
    vals=f'{r};{r};.5;{r};{r}'
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{r-.8}" ry="{r}" fill="#f6e04a">'
            f'<animate attributeName="ry" values="{vals}" keyTimes="0;.94;.96;.98;1" dur="{dur}s" begin="-{begin}s" repeatCount="indefinite"/></ellipse>')

def sitting_cat():
    # ---- black cat: upright sitting pose facing the woman (left), S-curve tail (original drawing) ----
    B='#14121a'; RIM='#3a3550'; IN='#2a2433'
    rim=f' stroke="{RIM}" stroke-width="1.8" stroke-linejoin="round"'
    g='<g class="cat">'
    g+='<ellipse cx="610" cy="358" rx="82" ry="6" fill="#3f7a26" opacity=".35"/>'
    tail='M672 350C698 354 714 340 704 324C696 310 704 296 710 284C714 276 716 270 714 262'
    g+=sway(f'<path d="{tail}" fill="none" stroke="{RIM}" stroke-width="15" stroke-linecap="round"/>'
            f'<path d="{tail}" fill="none" stroke="{B}" stroke-width="11.5" stroke-linecap="round"/>',668,348,7,3.4,0)
    # body: chest forward, rounded haunch behind
    g+=(f'<path d="M550 230C532 262 524 308 530 346C531 354 536 358 546 358L666 358C680 358 684 346 678 332C672 298 642 262 608 244C590 234 566 222 550 230Z" fill="{B}"{rim}/>')
    # haunch + folded hind foot
    g+=f'<path d="M588 330C586 300 606 282 630 284C656 286 672 308 668 334C665 352 652 358 634 358L608 358C596 352 589 342 588 330Z" fill="#1b1824"{rim}/>'
    g+=f'<ellipse cx="606" cy="353" rx="22" ry="6" fill="{B}"{rim}/>'
    # front legs close together + paws
    g+=f'<path d="M532 300C530 322 530 340 530 352M548 296C548 320 548 338 548 352" fill="none" stroke="{RIM}" stroke-width="1.6" stroke-linecap="round"/>'
    g+=f'<ellipse cx="531" cy="354" rx="13" ry="5" fill="{B}"{rim}/><ellipse cx="552" cy="355" rx="11" ry="4.5" fill="{B}"{rim}/>'
    # head with pointed ears
    g+=f'<path d="M508 202L512 162L534 184C541 183 548 183 555 184L576 164L578 202C580 224 562 238 543 238C524 238 506 224 508 202Z" fill="{B}"{rim}/>'
    g+=f'<path d="M515 176L531 188L517 196Z" fill="{IN}"/><path d="M572 178L558 188L573 197Z" fill="{IN}"/>'
    # eyes (blink) with slit pupils, nose, whiskers
    g+=_blink(525,206,5.4,6.5,1.2)+_blink(556,206,5.4,6.5,1.2)
    g+=f'<path d="M525 201V211M556 201V211" stroke="{B}" stroke-width="1.8" stroke-linecap="round"/>'
    g+=f'<path d="M538 218L544 218L541 222Z" fill="#6a4a5a"/>'
    g+='<path d="M541 222C541 226 536 228 533 226M541 222C541 226 546 228 549 226" fill="none" stroke="#6b6682" stroke-width="1.2" stroke-linecap="round"/>'
    g+='<path d="M514 222L494 218M514 226L494 228M568 222L588 218M568 226L588 228" stroke="#8a85a0" stroke-width="1" stroke-linecap="round" opacity=".6"/>'
    g+='</g>'
    return g
