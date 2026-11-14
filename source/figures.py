"""Shared figures: witch in deck chair + sitting dog (why scene coords; hero reuses scaled)."""
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

def sitting_dog():
    # ---- dog: lean sitting hound facing the woman, one paw lifted (hand-drawn) ----
    D='#334a59'; D2='#243541'; HL='#46606f'
    g='<g class="dog">'
    g+='<ellipse cx="612" cy="358" rx="78" ry="6" fill="#3f7a26" opacity=".35"/>'
    g+=sway(f'<path d="M660 346C686 344 700 326 704 298C705 290 701 286 697 290C694 316 684 332 658 337Z" fill="{D}"/>',662,342,8,1.05,0)
    # far front leg (behind, darker)
    g+=f'<path d="M566 286L571 350C571 354 575 355 577 356C577 358 570 358 565 358C561 358 560 355 560 350L556 290Z" fill="{D2}"/>'
    # body, neck, head
    g+=(f'<path d="M482 203C486 198 496 196 506 194C510 186 516 182 526 182C540 182 549 191 552 203C557 214 566 222 578 230C600 244 622 262 640 280C656 296 666 314 668 334'
        f'C669 348 664 356 656 357L600 357C594 340 588 318 584 300C578 286 570 274 560 264C548 252 534 240 520 233C510 229 500 225 492 222C484 218 479 209 482 203Z" fill="{D}"/>')
    # haunch + hind foot
    g+=f'<path d="M594 326C592 300 608 284 630 286C652 288 666 308 664 332C662 350 650 358 632 358L606 358C598 350 595 340 594 326Z" fill="#2e4352"/>'
    g+=f'<path d="M590 357C589 350 596 346 606 347L638 350C645 352 646 358 640 358Z" fill="{D}"/>'
    g+=f'<path d="M612 298C628 294 646 302 654 318" fill="none" stroke="{HL}" stroke-width="3" stroke-linecap="round" opacity=".6"/>'
    # near front leg: shoulder -> elbow forward, forearm level, paw droops at the wrist
    g+=sway(capsule(574,262,550,280,16,D)+capsule(550,280,526,281,13,D)+f'<ellipse cx="519" cy="285" rx="10" ry="8" fill="{D}" transform="rotate(20 519 285)"/>'+'<path d="M512 282L512 292M518 284L517 294" stroke="#1d2b34" stroke-width="1.4" stroke-linecap="round"/>',574,262,5,1.7,-.4)
    # sheen
    g+=f'<path d="M512 188C522 182 536 182 544 189C534 189 523 191 512 196Z" fill="{HL}"/>'
    g+=f'<path d="M574 236C596 250 616 266 634 284C616 272 596 258 578 246Z" fill="{HL}" opacity=".6"/>'
    # collar wraps the neck (under the ear), tag hangs at the throat
    g+='<path d="M556 208L568 220C560 236 547 246 532 250L526 240C540 235 551 225 556 208Z" fill="#e2445a"/>'
    g+='<path d="M558 214C552 228 543 237 530 243" fill="none" stroke="#b8304a" stroke-width="1.6" stroke-linecap="round"/>'
    g+='<circle cx="532" cy="253" r="4.6" fill="#f6c84a" stroke="#c9a03a" stroke-width="1"/><circle cx="532" cy="253" r="1.5" fill="#d9a62a"/>'
    # ear
    g+=sway(f'<path d="M528 186C541 183 550 192 550 205C550 220 546 233 538 240C532 237 529 227 529 215C527 205 524 194 528 186Z" fill="{D2}"/>',531,189,5,2.6,-1)
    # face
    g+='<path d="M478 201C482 197 489 198 490 203C489 208 483 209 479 207C477 206 476 203 478 201Z" fill="#11161c"/>'
    g+='<circle cx="511" cy="199" r="3.3" fill="#11161c"/><circle cx="510" cy="197.8" r="1.05" fill="#fff"/>'
    g+='<path d="M505 191C509 188 514 188 517 190" fill="none" stroke="#1f2d36" stroke-width="1.6" stroke-linecap="round"/>'
    g+='<path d="M488 214C494 218 501 217 507 212" fill="none" stroke="#18232b" stroke-width="1.8" stroke-linecap="round"/>'
    g+='<path d="M494 216C495 223 500 226 504 220C503 217 499 216 494 216Z" fill="#f07a8a"/>'
    g+='</g>'
    return g
