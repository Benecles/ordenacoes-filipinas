"""Pontes de Miranda's painel de azulejos: ten small crates, one lost by accident before delivery.

Object drawing. The panel is assembled from nine crates of tiles; the tenth crate is the gap. No factual
parameters beyond the count the source gives (ten crates, one lost). Params: narrow (bool).
Source: Pontes de Miranda, Tratado, t. XXV, p. 401 (trechos 4, p. 11).
"""
from . import svg as S


def _tile(x, y, t):
    h, q = t / 2, t * .31
    d = (f'M{x+h:g},{y+t*.09:g} L{x+t*.91:g},{y+h:g} L{x+h:g},{y+t*.91:g} L{x+t*.09:g},{y+h:g} Z '
         f'M{x+q:g},{y:g} A{q:g},{q:g} 0 0 1 {x:g},{y+q:g} '
         f'M{x+t-q:g},{y:g} A{q:g},{q:g} 0 0 0 {x+t:g},{y+q:g} '
         f'M{x+t:g},{y+t-q:g} A{q:g},{q:g} 0 0 0 {x+t-q:g},{y+t:g} '
         f'M{x:g},{y+t-q:g} A{q:g},{q:g} 0 0 1 {x+q:g},{y+t:g} '
         f'M{x+h-t*.1:g},{y+h:g} a{t*.1:g},{t*.1:g} 0 1 0 {t*.2:g},0 a{t*.1:g},{t*.1:g} 0 1 0 {-t*.2:g},0')
    return S.path(d, fill='none', stroke=S.INK, stroke_width=1)


def build(p):
    narrow = p.get('narrow', False)
    t = 20 if narrow else 32           # tile edge
    c = 3 * t                          # crate edge: 3 x 3 tiles
    cols, rows = 5, 2
    x0, y0 = (30 if narrow else 24), (56 if narrow else 62)
    W = x0 * 2 + cols * c if narrow else 700
    out = []
    grid = []
    for i in range(cols * 3 + 1):
        grid.append(f'M{x0+i*t:g},{y0:g} V{y0+rows*c:g}')
    for j in range(rows * 3 + 1):
        grid.append(f'M{x0:g},{y0+j*t:g} H{x0+cols*c:g}')
    out.append(S.path(' '.join(grid), fill='none', stroke=S.GRID, stroke_width=.8))
    lost = (2, 0)
    for r in range(rows):
        for k in range(cols):
            if (k, r) == lost:
                continue
            for a in range(3):
                for b in range(3):
                    out.append(_tile(x0 + k * c + a * t, y0 + r * c + b * t, t))
    for r in range(rows):
        for k in range(cols):
            if (k, r) == lost:
                out.append(S.rect(x0 + k * c, y0 + r * c, c, c, fill='none', stroke=S.MUTED, stroke_width=1.5, stroke_dasharray='4 4'))
                lx, ly = x0 + k * c, y0 + r * c
                for (ax, ay, bx, by, cx2, cy2) in [(.18, .74, .34, .62, .30, .88), (.52, .80, .70, .70, .66, .90), (.78, .60, .90, .74, .74, .86)]:
                    out.append(S.path(f'M{lx+ax*c:g},{ly+ay*c:g} L{lx+bx*c:g},{ly+by*c:g} L{lx+cx2*c:g},{ly+cy2*c:g} Z',
                                      fill=S.PAPER2, stroke=S.INK, stroke_width=1))
            else:
                out.append(S.rect(x0 + k * c, y0 + r * c, c, c, fill='none', stroke=S.INK, stroke_width=2))
    lx = x0 + 2.5 * c
    out.append(S.line(lx, y0 - 8, lx, y0 - 28, stroke=S.INK, stroke_width=1.2))
    out.append(S.text(lx, y0 - 36, 'caiu, sem culpa do devedor, antes da tradição', size=14, family=S.SERIF, anchor='middle'))
    if narrow:
        ty = y0 + rows * c + 34
        out.append(S.text(x0, ty, 'O credor escolhe', size=14, family=S.SANS, weight='600'))
        out.append(S.line(x0, ty + 14, x0 + cols * c, ty + 14, stroke=S.GRID, stroke_width=1))
        out.append(S.text(x0, ty + 38, 'resolver o contrato', size=16, family=S.SERIF))
        out.append(S.text(x0 + cols * c, ty + 38, 'ou', size=14, family=S.SERIF, fill=S.MUTED, anchor='end', font_style='italic'))
        out.append(S.line(x0, ty + 54, x0 + cols * c, ty + 54, stroke=S.GRID, stroke_width=1))
        out.append(S.text(x0, ty + 78, 'abater o preço', size=16, family=S.SERIF))
        H = ty + 96
    else:
        rx = x0 + cols * c + 36
        ty = y0 + 36
        out.append(S.text(rx, ty, 'O credor escolhe', size=14, family=S.SANS, weight='600'))
        out.append(S.line(rx, ty + 14, W - 18, ty + 14, stroke=S.GRID, stroke_width=1))
        out.append(S.text(rx, ty + 42, 'resolver o contrato', size=17, family=S.SERIF))
        out.append(S.text(W - 18, ty + 68, 'ou', size=14, family=S.SERIF, fill=S.MUTED, anchor='end', font_style='italic'))
        out.append(S.line(rx, ty + 80, W - 18, ty + 80, stroke=S.GRID, stroke_width=1))
        out.append(S.text(rx, ty + 106, 'abater o preço', size=17, family=S.SERIF))
        H = y0 + rows * c + 24
    return S.svg(W, H, 'Painel de azulejos remetido em dez caixões, com um caixão perdido', out), []
