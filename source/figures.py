"""Shared figures: woman in deck chair + sitting dog (why scene coords; hero reuses scaled)."""
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
    # far leg: thigh along seat (mostly hidden), shin down, sandal
    w+=bar(252,262,392,280,30).replace('stroke="#3a4452"','stroke="#244c9c"')
    w+=capsule(394,282,424,346,15,'#e8a27a')
    w+='<path d="M398 352C410 340 432 340 444 348L446 366L398 368Z" fill="#f6e3b4"/><path d="M398 364L448 362L448 372L398 372Z" fill="#3a3f4a"/>'
    w+='<path d="M398 352C410 340 432 340 444 348L446 366L398 368Z" fill="#f6e3b4"/><path d="M398 364L448 362L448 372L398 372Z" fill="#3a3f4a"/>'
    # near leg: thigh rests on seat, knee bent ~90, shin down to ground
    w+=capsule(252,264,414,274,34,'#2f5db4')
    w+=capsule(262,252,404,262,8,'#3f6fc8').replace('stroke-linecap','opacity=".6" stroke-linecap')
    w+=capsule(300,284,410,292,6,'#244c9c')
    w+=capsule(418,278,450,344,16,'#f2b48c')
    w+=capsule(416,276,424,296,26,'#2f5db4')
    w+='<g transform="translate(-52 20)"><path d="M494 326C506 314 528 314 540 322L542 340L494 342Z" fill="#f6e3b4"/><path d="M490 338L544 336L544 346L490 346Z" fill="#3a3f4a"/></g>'
    # torso shirt
    w+='<path d="M170 168C188 152 226 150 252 160C276 170 292 196 298 222L266 250C246 258 220 258 204 250C188 232 176 200 170 168Z" fill="#ec5a68"/>'
    w+='<path d="M170 168C180 162 190 160 198 162C196 196 204 228 222 256C214 256 208 254 204 250C188 232 176 200 170 168Z" fill="#d6455a"/>'
    # raised arm: upper arm down to elbow, forearm up, hand holds potion
    w+=capsule(268,180,322,226,15,'#f2b48c')
    w+=capsule(322,226,370,170,13,'#f2b48c')
    w+='<circle cx="322" cy="226" r="8.5" fill="#e8a27a"/><circle cx="372" cy="166" r="8" fill="#f2b48c"/>'
    w+='<path d="M250 158C264 156 280 162 292 172L276 196C266 186 254 178 244 176Z" fill="#ec5a68"/>'
    w+=potion(384,140)
    # resting arm across lap
    w+='<path d="M196 214C212 232 240 236 274 228L276 244C242 254 206 250 188 232Z" fill="#f2b48c"/><circle cx="276" cy="236" r="8" fill="#e8a27a"/>'
    # head, hair, hat
    w+='<path d="M196 128C194 108 206 96 224 96L232 140C226 152 214 166 208 176L198 182C186 166 194 146 196 128Z" fill="#2a2f3a"/>'
    w+='<path d="M210 146L230 140L234 166L214 170Z" fill="#e8a27a"/>'
    w+='<path d="M210 112C216 100 236 98 242 112C246 122 244 140 236 150C228 156 218 152 212 144Z" fill="#f2b48c"/>'
    w+='<path d="M228 131C231 134 235 134 238 131" fill="none" stroke="#2a2f3a" stroke-width="2" stroke-linecap="round"/>'
    w+='<circle cx="229" cy="140" r="4" fill="#f08a8a" opacity=".55"/>'
    w+='<path d="M234 145C237 148 241 147 243 143" fill="none" stroke="#b85a4a" stroke-width="1.8" stroke-linecap="round"/>'
    w+='<path d="M196 118C212 116 232 108 244 100" fill="none" stroke="#2a2f3a" stroke-width="7" stroke-linecap="round"/>'
    w+='<ellipse cx="214" cy="106" rx="72" ry="22" fill="#f6cf4a" transform="rotate(-12 214 106)"/>'
    w+='<path d="M180 108C178 84 196 72 218 74C238 76 250 88 250 98Z" fill="#f8d95a"/>'
    w+='<path d="M182 106C204 102 230 96 250 96L250 104C228 104 204 110 182 114Z" fill="#ec5a68"/>'
    w+='<ellipse cx="214" cy="106" rx="72" ry="22" fill="none" stroke="#e7b93a" stroke-width="2" transform="rotate(-12 214 106)"/>'
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
    # near front leg: lifted 'shake' paw, reaching toward the woman
    g+=sway(capsule(574,280,550,306,15,D)+capsule(550,306,532,303,12,D)+f'<path d="M526 297C530 294 538 295 540 300C541 306 536 310 530 310C525 309 523 302 526 297Z" fill="{D}"/>'+'<path d="M528 302L532 309M533 300L537 308" stroke="#1d2b34" stroke-width="1.4" stroke-linecap="round"/>',574,278,5,1.7,-.4)
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
