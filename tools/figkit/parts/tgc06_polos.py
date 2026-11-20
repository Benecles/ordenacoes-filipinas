"""Aula 06, chapter 1: how many lines of duty a contract draws.

Three small circuits side by side (stacked on phones): doação pura, compra e venda,
sociedade. Dots are parties, a heavy line is a duty (the flag points to its creditor),
the thin dashed line is an acceptance that creates no duty. The count of heavy lines and
who holds the ends carry the classification. Facts: Pereira pp.61-62 (duas manifestações
de vontade, só o doador obrigado; venda: ambas credoras e devedoras); Venosa pp.24, 27
(plurilateral: centros autônomos de interesses; constituição de sociedade).
Params: none. Geometry is schematic.
"""
from . import svg as S

PW, PH = 290, 250


def _dot(o, x, y, r=7):
    o.append(S.circle(x, y, r, fill=S.PAPER, stroke=S.INK, stroke_width=1.8))


def _duty(o, x1, y1, x2, y2, col=S.INK):
    o.append(S.line(x1, y1, x2, y2, stroke=col, stroke_width=2.6))
    # flag at the creditor end
    dx = 1 if x2 > x1 else (-1 if x2 < x1 else 0)
    dy = 1 if y2 > y1 else (-1 if y2 < y1 else 0)
    if dy == 0:
        o.append(S.path(f'M{x2-dx*14},{y2-6} L{x2},{y2} L{x2-dx*14},{y2+6}', fill='none', stroke=col, stroke_width=2.2))
    else:
        o.append(S.path(f'M{x2-6},{y2-dy*14} L{x2},{y2} L{x2+6},{y2-dy*14}', fill='none', stroke=col, stroke_width=2.2))


def _panel(ox, oy, kind):
    o = []
    T = S.text
    if kind == 'doacao':
        o.append(T(ox + 20, oy + 26, 'Doação pura', size=16, family=S.SANS, weight='600'))
        y = oy + 118
        x1, x2 = ox + 40, ox + 250
        _dot(o, x1, y); _dot(o, x2, y)
        _duty(o, x1 + 9, y, x2 - 9, y)
        o.append(S.path(f'M{x2-9},{y+38} H{x1+9}', fill='none', stroke=S.MUTED, stroke_width=1.3, stroke_dasharray='4 4'))
        o.append(S.path(f'M{x1+22},{y+32} L{x1+9},{y+38} L{x1+22},{y+44}', fill='none', stroke=S.MUTED, stroke_width=1.3))
        o.append(T(x1, y - 20, 'doador', size=14, family=S.SERIF, anchor='middle'))
        o.append(T(x2, y - 20, 'donatário', size=14, family=S.SERIF, anchor='middle'))
        o.append(T(ox + 145, y + 66, 'aceitação · sem dever', size=13, family=S.SERIF, anchor='middle', fill=S.MUTED))
        o.append(T(ox + 145, oy + 228, 'um dever · unilateral', size=14, family=S.SERIF, anchor='middle'))
    elif kind == 'venda':
        o.append(T(ox + 20, oy + 26, 'Compra e venda', size=16, family=S.SANS, weight='600'))
        x1, x2 = ox + 40, ox + 250
        ya, yb = oy + 98, oy + 148
        _dot(o, x1, ya); _dot(o, x2, ya); _dot(o, x1, yb); _dot(o, x2, yb)
        o.append(S.line(x1, ya + 7, x1, yb - 7, stroke=S.INK, stroke_width=1))
        o.append(S.line(x2, ya + 7, x2, yb - 7, stroke=S.INK, stroke_width=1))
        _duty(o, x1 + 9, ya, x2 - 9, ya)
        _duty(o, x2 - 9, yb, x1 + 9, yb)
        mx = ox + 145
        o.append(S.line(mx, ya + 12, mx, yb - 12, stroke=S.CONC, stroke_width=2.2))
        o.append(S.line(mx - 8, ya + 12, mx + 8, ya + 12, stroke=S.CONC, stroke_width=2.2))
        o.append(S.line(mx - 8, yb - 12, mx + 8, yb - 12, stroke=S.CONC, stroke_width=2.2))
        o.append(T(ox + 145, ya - 14, 'entrega', size=14, family=S.SERIF, anchor='middle'))
        o.append(T(ox + 145, yb + 26, 'preço', size=14, family=S.SERIF, anchor='middle'))
        o.append(T(x1 + 4, yb + 46, 'vendedor', size=14, family=S.SERIF, anchor='middle'))
        o.append(T(x2 - 4, yb + 46, 'comprador', size=14, family=S.SERIF, anchor='middle'))
        o.append(T(ox + 145, oy + 228, 'dois deveres ligados · bilateral', size=14, family=S.SERIF, anchor='middle'))
    else:
        o.append(T(ox + 20, oy + 26, 'Sociedade', size=16, family=S.SANS, weight='600'))
        cx, cy = ox + 145, oy + 120
        pts = [(cx - 85, cy - 38), (cx + 85, cy - 38), (cx - 85, cy + 46), (cx + 85, cy + 46), (cx, cy - 74)]
        for (x, y) in pts:
            _dot(o, x, y)
        o.append(S.rect(cx - 12, cy - 12, 24, 24, fill=S.PAPER, stroke=S.INK, stroke_width=1.8))
        o.append(S.line(cx - 12, cy, cx + 12, cy, stroke=S.INK, stroke_width=1))
        for (x, y) in pts:
            vx, vy = cx - x, cy - y
            n = (vx * vx + vy * vy) ** .5
            o.append(S.line(x + vx / n * 9, y + vy / n * 9, cx - vx / n * 15, cy - vy / n * 15, stroke=S.INK, stroke_width=2.6))
        o.append(T(cx, cy + 78, 'fim comum', size=14, family=S.SERIF, anchor='middle', fill=S.MUTED))
        o.append(T(ox + 145, oy + 228, 'centros autônomos · plurilateral', size=14, family=S.SERIF, anchor='middle'))
    return ''.join(o)


def build(p):
    kinds = ('doacao', 'venda', 'sociedade')
    d = [_panel(i * PW + 5, 0, k) for i, k in enumerate(kinds)]
    for i in (1, 2):
        d.append(S.line(i * PW, 20, i * PW, PH - 20, stroke=S.MUTED, stroke_width=.8))
    desktop = S.svg(PW * 3 + 10, PH, 'Quantos deveres cada contrato cria: doação pura, compra e venda, sociedade', d)
    m = [_panel(25, i * PH, k) for i, k in enumerate(kinds)]
    for i in (1, 2):
        m.append(S.line(30, i * PH, 330, i * PH, stroke=S.MUTED, stroke_width=.8))
    mobile = S.svg(340, PH * 3, 'Quantos deveres cada contrato cria', m)
    return '<div class="drawing-desktop">' + desktop + '</div><div class="drawing-mobile">' + mobile + '</div>', []
