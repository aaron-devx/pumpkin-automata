"""Night Halloween grade: maps every day-palette hex in generated SVG to its night twin.
Shapes stay; only colors move. Hue bands: sky/water -> indigo, greens -> dusk, warm -> pumpkin glow."""
import colorsys, re

HEX = re.compile(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b')
NIGHT_HUE = 255 / 360        # indigo target for sky + water
PUMPKIN_HUE = 24 / 360       # orange target for warm accents
NEAR_WHITE_SAT = .08         # pure whites (eyes, highlights) stay
MOONLIT_WHITE = '#c9bfe6'    # hero clouds: whites dim to lavender
NEAR_WHITE_LIT = .9


def _rgb(h):
    h = h if len(h) == 6 else ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _hex(r, g, b):
    return '#%02x%02x%02x' % tuple(round(max(0, min(1, v)) * 255) for v in (r, g, b))


def _lerp(a, b, t):
    return a + (b - a) * t


def night(h, tint_whites=False):
    hue, lit, sat = colorsys.rgb_to_hls(*_rgb(h))
    deg = hue * 360
    if tint_whites and lit > NEAR_WHITE_LIT:
        return MOONLIT_WHITE
    if sat < NEAR_WHITE_SAT:
        return '#' + h.lower()
    if 165 <= deg < 265:                       # sky, water, house glass
        hue, lit, sat = _lerp(hue, NIGHT_HUE, .7), .08 + lit * .3, sat * .45
    elif 70 <= deg < 165:                      # foliage, grass
        hue, lit, sat = _lerp(hue, 150 / 360, .25), .05 + lit * .45, sat * .7
    elif 15 <= deg < 70:                       # sun, sand, flowers -> lantern glow
        hue, lit = _lerp(hue, PUMPKIN_HUE, .35), lit * .92
    else:                                      # reds, pinks, purples
        lit = lit * .82
    return _hex(*colorsys.hls_to_rgb(hue, lit, sat))


def grade(svg, tint_whites=False):
    return HEX.sub(lambda m: night(m.group(1), tint_whites), svg)
