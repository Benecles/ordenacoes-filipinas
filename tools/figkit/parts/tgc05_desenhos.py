"""Aula 05 (classificação I): desenhos de segundo passe.
params: mode = rede | prazo | aguada | formacao | tempo.
rede      cast net seen from above, empty; the price (coins) rests, or goes home, by the risk the reader assumes
          (the page script toggles #coins-mid, #slip-keep, #slip-back). Facts: Pereira pp. 63-64; CC 458-459.
prazo     a year planner (12 month columns) with the decadence periods of CC 445 and CDC 26 as bars on one scale;
          positions computed from 365 days. Facts: CC 445 (30 dias/1 ano; metade se já na posse; 180 dias/1 ano do
          conhecimento tardio), CDC 26 (30 / 90 dias).
aguada    survey plan of a fazenda de criar with the evicted strip lifted off; the herd's trails run to the aguada.
          Facts: Pereira p. 130 (no area is quantified).
formacao  the moment a contract is born: consensual, real, solene, forma ad probationem. Facts: the chapter's own
          paragraphs on Venosa/Pereira, CC 108.
tempo     imediata, diferida, continuada, and what a resolution does to each. Facts: Pereira pp. 64-65; Venosa p. 42.
"""
from math import cos, sin, pi
from . import svg as S

T = S.text


def _ell(cx, cy, rx, ry, **kw):
    return f"<ellipse {S.attrs(cx=cx, cy=cy, rx=rx, ry=ry, **kw)}/>"


def _coins(cx, cy, stroke=S.INK, n=4):
    """A stack of coins; cy is the foot of the stack."""
    o = []
    for i in range(n):
        y = cy - i * 7
        o.append(S.path(f'M{cx - 22},{y - 7} V{y} A22,6 0 0 0 {cx + 22},{y} V{y - 7}', fill=S.PAPER, stroke=stroke, stroke_width=1.4))
        o.append(_ell(cx, y - 7, 22, 6, fill=S.PAPER, stroke=stroke, stroke_width=1.4))
    return o


def _arrow(x1, y1, x2, y2, color, sw=2.6):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx = [x2 - 11 * math.cos(a - .5), y2 - 11 * math.sin(a - .5), x2 - 11 * math.cos(a + .5), y2 - 11 * math.sin(a + .5)]
    return [S.line(x1, y1, x2, y2, stroke=color, stroke_width=sw),
            S.path(f'M{hx[0]:.1f},{hx[1]:.1f} L{x2},{y2} L{hx[2]:.1f},{hx[3]:.1f}', fill='none', stroke=color, stroke_width=sw)]


def rede():
    w, h = 620, 360
    o = []
    cx, cy, R = 168, 182, 132
    n = 16
    # mesh: concentric polygons and spokes; nothing inside
    for r in (24, 50, 76, 102, 128):
        pts = [(cx + r * cos(2 * pi * k / n), cy + r * sin(2 * pi * k / n)) for k in range(n)]
        o.append(S.path('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ' Z', fill='none', stroke=S.MUTED, stroke_width=1))
    for k in range(n):
        a = 2 * pi * k / n
        o.append(S.line(cx + 10 * cos(a), cy + 10 * sin(a), cx + R * cos(a), cy + R * sin(a), stroke=S.MUTED, stroke_width=1))
    o.append(S.circle(cx, cy, R, fill='none', stroke=S.INK, stroke_width=2.2))
    for k in range(32):
        a = 2 * pi * k / 32
        o.append(S.circle(cx + R * cos(a), cy + R * sin(a), 3.4, fill=S.INK))
    o.append(S.circle(cx, cy, 5, fill=S.INK))
    # the two ends of the price: seller above, buyer below, a dotted line between, a tray in the middle
    px = 470
    o += [S.rect(px - 8, 62, 16, 16, fill=S.INK), T(px + 20, 76, 'pescador', size=15, family=S.SANS),
          S.circle(px, 296, 9, fill='none', stroke=S.INK, stroke_width=2), T(px + 20, 301, 'comprador', size=15, family=S.SANS),
          S.line(px, 90, px, 284, stroke=S.MUTED, stroke_width=1.2, stroke_dasharray='2 6', stroke_linecap='round'),
          S.rect(px - 38, 150, 76, 62, fill='none', stroke=S.INK2, stroke_width=1.3, stroke_dasharray='5 4'),
          T(px + 50, 186, 'preço pago', size=15, family=S.SANS)]
    o.append('<g id="coins-mid">' + ''.join(_coins(px, 198)) + '</g>')
    o.append('<g id="slip-keep" opacity="0">' + ''.join(_coins(px, 128, S.DIF))
             + S.circle(px, 100, 0.01, fill='none')
             + ''.join(_arrow(px, 178, px, 138, S.DIF)) + T(px + 36, 116, 'fica', size=17, family=S.SANS, fill=S.DIF) + '</g>')
    o.append('<g id="slip-back" opacity="0">' + ''.join(_coins(px, 268, S.CONC))
             + ''.join(_arrow(px, 216, px, 246, S.CONC)) + T(px + 36, 262, 'volta', size=17, family=S.SANS, fill=S.CONC) + '</g>')
    return S.svg(w, h, 'Aula05 · rede', o), []


def prazo():
    w, h = 940, 448
    sc = 1.65
    x0 = 262
    X = lambda d: x0 + d * sc
    o = []
    mw = 365 / 12 * sc
    top, bot = 48, 420
    for i in range(12):
        o.append(S.line(x0 + (i + 1) * mw, top, x0 + (i + 1) * mw, bot, stroke=S.GRID, stroke_width=1))
        o.append(T(x0 + i * mw + mw / 2, 38, str(i + 1), size=12, fill=S.MUTED, anchor='middle'))
    o += [T(x0 - 12, 38, 'meses', size=12, fill=S.MUTED, anchor='end'),
          S.line(x0, top, x0, bot, stroke=S.INK, stroke_width=1.4), S.line(x0, bot, X(365), bot, stroke=S.INK, stroke_width=1.4)]
    for d in (30, 90, 180, 365):
        o += [S.line(X(d), bot, X(d), bot + 6, stroke=S.INK, stroke_width=1.2),
              T(X(d), bot + 20, str(d) + (' dias' if d == 365 else ''), size=12, fill=S.MUTED, anchor='middle')]

    def bar(y, label, days, label_end, late=False, ghost=None):
        res = []
        res.append(T(16, y + 5, label, size=14, family=S.SANS))
        if ghost:
            res.append(S.line(x0, y + 12, X(ghost), y + 12, stroke=S.MUTED, stroke_width=1.6, stroke_dasharray='3 4'))
        if late:
            res.append(S.line(x0 + 10, y, X(days), y, stroke=S.INK, stroke_width=5, stroke_dasharray='11 5'))
            res.append(S.path(f'M{x0 + 1},{y} l5,-6 l5,6 l-5,6 z', fill=S.PAPER, stroke=S.INK, stroke_width=1.5))
        else:
            res.append(S.line(x0, y, X(days), y, stroke=S.INK, stroke_width=5))
        res.append(S.line(X(days), y - 10, X(days), y + 10, stroke=S.CONC, stroke_width=2.4))
        res.append(T(X(days) + 12, y + 5, label_end, size=14))
        return res

    def head(y, s):
        return [T(16, y, s, size=19, family=S.SERIF), S.line(16, y + 9, x0 - 14, y + 9, stroke=S.INK, stroke_width=1)]

    o += head(76, 'Coisa móvel') + bar(102, 'da entrega', 30, '30 dias') \
        + bar(134, 'já na posse', 15, '15 dias', ghost=30) + bar(166, 'vício tardio', 180, '180 dias', late=True)
    o += head(212, 'Coisa imóvel') + bar(238, 'da entrega', 365, '1 ano') \
        + bar(270, 'já na posse', 182.5, 'metade do ano', ghost=365) + bar(302, 'vício tardio', 365, '1 ano', late=True)
    o += head(346, 'Consumo') + bar(372, 'não durável', 30, '30 dias') + bar(398, 'durável', 90, '90 dias')
    return S.svg(w, h, 'Aula05 · prazos de decadência', o), []


def aguada():
    w, h = 480, 410
    o = []
    A, B, C, D, E, F = (24, 100), (350, 64), (384, 176), (368, 340), (70, 372), (18, 236)
    P1 = (306, 69)
    cut = [(322, 128), (345, 178)]
    Q = (380, 214)
    dx, dy = 26, -12
    body = [A, P1] + cut + [Q, D, E, F]
    d = 'M' + ' L'.join(f'{x},{y}' for x, y in body) + ' Z'
    strip = [P1, B, C, Q, cut[1], cut[0]]
    dstrip = 'M' + ' L'.join(f'{x + dx},{y + dy}' for x, y in strip) + ' Z'
    ghost = 'M' + ' L'.join(f'{x},{y}' for x, y in strip) + ' Z'
    o.append(S.path(ghost, fill='none', stroke=S.MUTED, stroke_width=1.2, stroke_dasharray='4 4'))
    # grass strokes on the pasture, then the boundary
    for (x, y) in [(90, 300), (170, 340), (250, 290), (300, 260), (210, 250), (60, 220), (270, 190)]:
        o.append(S.path(f'M{x},{y} l-3,-6 M{x},{y} l0,-7 M{x},{y} l3,-6', fill='none', stroke=S.MUTED, stroke_width=1))
    o.append(S.path(d, fill='none', stroke=S.INK, stroke_width=2.2))
    for (x, y) in (A, F, E, D, Q, P1):
        o.append(S.rect(x - 4, y - 4, 8, 8, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
    pond = (347 + dx, 126 + dy)
    # the lifted strip over its trails
    o.append(S.path(dstrip, fill=S.PAPER, stroke=S.CONC, stroke_width=2.4))
    o.append(_ell(pond[0], pond[1], 15, 10, fill='none', stroke=S.INK, stroke_width=2))
    for k, yy in enumerate((-3, 2, 7)):
        o.append(S.path(f'M{pond[0] - 8},{pond[1] + yy - 2} q4,-3 8,0 t8,0', fill='none', stroke=S.INK, stroke_width=1))
    starts = [(92, 190, 190, 150), (120, 300, 230, 230), (200, 300, 290, 250), (260, 160, 300, 130), (70, 270, 180, 210)]
    for sx, sy, mx, my in starts:
        o.append(S.path(f'M{sx},{sy} Q{mx},{my} {pond[0] - 17},{pond[1] + 3}', fill='none', stroke=S.INK2, stroke_width=2.4,
                        stroke_dasharray='0.1 7', stroke_linecap='round'))
        o.append(S.circle(sx, sy, 4, fill=S.INK))
    o += [T(86, 346, 'fazenda de criar', size=19, family=S.SERIF), S.line(pond[0] + 17, pond[1], 416, pond[1], stroke=S.INK, stroke_width=1) + T(422, pond[1] + 6, 'aguada', size=17, family=S.SERIF)]
    return S.svg(w, h, 'Aula05 · fazenda e aguada', o), []


def _consent(x, y, col=S.INK):
    return [S.circle(x - 6, y, 10, fill=S.PAPER, stroke=col, stroke_width=1.8), S.circle(x + 6, y, 10, fill='none', stroke=col, stroke_width=1.8)]


def _key(x, y, col=S.INK, fill=S.PAPER, dash=None):
    kw = dict(stroke_dasharray=dash) if dash else {}
    return [S.circle(x, y, 8, fill=fill, stroke=col, stroke_width=1.8, **kw),
            S.line(x + 8, y, x + 34, y, stroke=col, stroke_width=1.8, **kw),
            S.line(x + 26, y, x + 26, y + 8, stroke=col, stroke_width=1.8), S.line(x + 33, y, x + 33, y + 8, stroke=col, stroke_width=1.8)]


def _seal(x, y, col=S.INK, dash=None):
    pts = []
    for k in range(24):
        r = 15 if k % 2 == 0 else 12
        a = 2 * pi * k / 24
        pts.append(f'{x + r * cos(a):.1f},{y + r * sin(a):.1f}')
    kw = dict(stroke_dasharray=dash) if dash else {}
    return [S.path('M' + ' L'.join(pts) + ' Z', fill=S.PAPER, stroke=col, stroke_width=1.7, **kw),
            S.circle(x, y, 6.5, fill='none', stroke=col, stroke_width=1.4, **kw)]


def formacao():
    w, h = 940, 412
    o = []
    xa, xb, xe = 380, 650, 905
    rows = [(88, 'Consensual', 'compra e venda de móvel', 'key', False, 'cumpre'),
            (176, 'Real', 'comodato e depósito', 'key', True, 'constitui'),
            (264, 'Solene', 'escritura pública', 'seal', True, 'constitui'),
            (352, 'Forma para prova', 'escrita por conveniência', 'seal', False, 'prova')]
    o += [T(xa, 30, 'acordo', size=14, anchor='middle', fill=S.INK2), T(xb, 30, 'segundo ato', size=14, anchor='middle', fill=S.INK2),
          S.line(xa, 40, xa, 372, stroke=S.GRID, stroke_width=1), S.line(xb, 40, xb, 372, stroke=S.GRID, stroke_width=1)]
    for y, name, sub, glyph, needs, verb in rows:
        o += [T(16, y - 2, name, size=19, family=S.SERIF), T(16, y + 19, sub, size=13, family=S.SANS, fill=S.INK2)]
        if needs:
            o.append(S.line(xa, y, xb, y, stroke=S.INK, stroke_width=2, stroke_dasharray='1 7', stroke_linecap='round'))
            o.append(T((xa + xb) / 2, y - 14, 'só o acordo', size=14, family=S.SANS, fill=S.CONC, anchor='middle'))
            o.append(S.line(xb, y, xe, y, stroke=S.INK, stroke_width=6))
            o.append(T(xb + 36, y - 17, 'contrato', size=15, family=S.SANS, fill=S.DIF))
        else:
            o.append(S.line(xa, y, xe, y, stroke=S.INK, stroke_width=6))
            o.append(T(xa + 4, y - 17, 'contrato', size=15, family=S.SANS, fill=S.DIF))
        o.append(S.rect(xa - 20, y - 12, 40, 24, fill=S.PAPER))
        o += _consent(xa, y)
        # the second act; constitutive ones in ink, the others pale
        col = S.INK if needs else S.MUTED
        dash = None if needs else '3 3'
        o.append(S.rect(xb - 22, y - 12, 46, 24, fill=S.PAPER) if glyph == 'key' else S.rect(xb - 18, y - 18, 36, 36, fill=S.PAPER))
        if glyph == 'key':
            o += _key(xb - 13, y, col, S.PAPER)
        else:
            o += _seal(xb, y, col, dash)
        o.append(T(xb, y + 36, verb, size=14, family=S.SANS, fill=S.INK2 if not needs else S.INK, anchor='middle'))
    return S.svg(w, h, 'Aula05 · quando nasce o contrato', o), []


def tempo():
    w, h = 940, 330
    o = []
    xc, xr = 230, 640
    rows = [(92, 'Imediata'), (170, 'Diferida'), (248, 'Continuada')]
    for y, name in rows:
        o += [T(16, y + 6, name, size=18, family=S.SANS), S.line(xc - 24, y, 905, y, stroke=S.GRID, stroke_width=1)]
    o += [S.line(xc, 52, xc, 282, stroke=S.INK, stroke_width=1.4), T(xc, 38, 'celebração', size=14, anchor='middle'),
          S.line(xr, 52, xr, 282, stroke=S.CONC, stroke_width=2.2, stroke_dasharray='7 5'), T(xr, 38, 'resolução', size=14, anchor='middle', fill=S.CONC)]

    def stub(x, y, solid=True, wd=56):
        col = S.INK if solid else S.MUTED
        dash = None if solid else '5 4'
        kw = dict(stroke_dasharray=dash) if dash else {}
        r = [S.rect(x, y - 17, wd, 34, fill=S.PAPER if solid else 'none', stroke=col, stroke_width=1.6, **kw)]
        if solid:
            r += [S.line(x + wd - 12, y - 17, x + wd - 12, y + 17, stroke=S.MUTED, stroke_width=1, stroke_dasharray='2 3'), S.circle(x + 14, y, 4.5, fill=S.INK)]
        return r

    # imediata: one receipt at the celebration; resolution sends it back
    o += stub(xc + 4, 92, wd=62)
    o += _arrow(xr - 4, 92, xc + 76, 92, S.DIF)
    # diferida: the same receipt later; the wait is a gap
    xd = 450
    o += [S.line(xc + 6, 170, xd - 6, 170, stroke=S.INK, stroke_width=2, stroke_dasharray='1 8', stroke_linecap='round')]
    o += stub(xd, 170, wd=62)
    o += _arrow(xr - 4, 170, xd + 76, 170, S.DIF)
    # continuada: a booklet of stubs; the ones before the cut are spent and stay, the others are cancelled
    x = xc + 4
    while x + 56 <= 905:
        o += stub(x, 248, solid=(x + 56 <= xr - 2))
        x += 64
    o += [T(xr + 28, 98, 'restitui', size=17, family=S.SANS, fill=S.DIF), T(xr + 28, 176, 'restitui', size=17, family=S.SANS, fill=S.DIF),
          T(xr + 28, 296, 'efeitos ficam', size=17, family=S.SANS, fill=S.DIF)]
    return S.svg(w, h, 'Aula05 · execução no tempo', o), []


MODES = dict(rede=rede, prazo=prazo, aguada=aguada, formacao=formacao, tempo=tempo)


def build(p):
    return MODES[p['mode']]()
