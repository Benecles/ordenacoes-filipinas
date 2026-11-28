"""Conceito de contrato, Aula 01: five drawings in five paper languages (finishing pass).

modes: vontades (railway lanes: two wills meet, one prestação crosses over; one-will acts stay single),
historia (genealogy of enforceability: Roman lines with their counted types, the limit, the later stem),
circulacao (overlap plate: function and structure, the contract where they coincide),
campo (two-question field: how the contract is formed against whether the relation is one of consumption),
arco (a dated ruler of the codes and statutes the lesson names).
Facts: Venosa p. 1 (Códigos de 1804, 1896/1900, 1916) and p. 2 (testamento, promessa de recompensa); Pereira p. 7, p. 9
and p. 67 (adesão e consumo; contratos administrativos por licitação); Martins-Costa pp. 18-19, 30-32, 39;
Código Civil arts. 421 e 421-A (Lei 13.874/2019); Lei 8.078 de 11/09/1990; Constituição de 1988.
Positions on `arco` are computed from the years; the other drawings assert counts and position only, never area.
"""
from __future__ import annotations
from math import sqrt
from . import svg as S

T = S.text


def _dot(o, x, y, r=6, fill=None, stroke=S.INK, w=1.8):
    o.append(S.circle(x, y, r, fill=fill or S.PAPER, stroke=stroke, stroke_width=w))


def _chord(cx, cy, r, k):
    """x-interval of the 45-degree line x + y = k inside the circle (cx, cy, r), or None."""
    u = k - cy
    d = 4 * (cx + u) ** 2 - 8 * (cx * cx + u * u - r * r)
    if d <= 0:
        return None
    s = sqrt(d)
    return (2 * (cx + u) - s) / 4, (2 * (cx + u) + s) / 4


def _lens_hatch(c1, c2, step, **kw):
    out = []
    lo = min(c1[1] - c1[2], c2[1] - c2[2]) + min(c1[0] - c1[2], c2[0] - c2[2])
    hi = max(c1[1] + c1[2], c2[1] + c2[2]) + max(c1[0] + c1[2], c2[0] + c2[2])
    k = lo
    while k < hi:
        a, b = _chord(*c1, k), _chord(*c2, k)
        if a and b:
            x0, x1 = max(a[0], b[0]), min(a[1], b[1])
            if x1 - x0 > 2:
                out.append(S.line(x0, k - x0, x1, k - x1, **kw))
        k += step
    return out


def vontades():
    W, H = 860, 436
    o = []
    # ruled sheet: two hairlines between the three acts
    for y in (214, 338):
        o.append(S.line(24, y, W - 24, y, stroke=S.GRID, stroke_width=1))
    # --- doação: two lanes meet, the vínculo parts again, one prestação crosses over
    ya, yb, xn = 92, 160, 330
    o.append(S.line(60, 30, 330, 30, stroke=S.INK2, stroke_width=1))
    o.append(S.line(60, 30, 60, 38, stroke=S.INK2, stroke_width=1))
    o.append(S.line(330, 30, 330, 38, stroke=S.INK2, stroke_width=1))
    o.append(T(195, 24, 'duas manifestações', size=15, family=S.SERIF, fill=S.INK2, anchor='middle'))
    o.append(S.line(430, 30, 790, 30, stroke=S.INK2, stroke_width=1))
    o.append(S.line(430, 30, 430, 38, stroke=S.INK2, stroke_width=1))
    o.append(S.line(790, 30, 790, 38, stroke=S.INK2, stroke_width=1))
    o.append(T(610, 24, 'uma prestação', size=15, family=S.SERIF, fill=S.INK2, anchor='middle'))
    mid = (ya + yb) / 2
    o.append(S.path(f'M60,{ya} H190 C250,{ya} 270,{mid} {xn},{mid}', fill='none', stroke=S.INK, stroke_width=2.2))
    o.append(S.path(f'M60,{yb} H190 C250,{yb} 270,{mid} {xn},{mid}', fill='none', stroke=S.INK, stroke_width=2.2))
    o.append(S.path(f'M{xn},{mid} H400 C440,{mid} 450,{ya} 490,{ya} H790', fill='none', stroke=S.INK, stroke_width=2.2))
    o.append(S.path(f'M{xn},{mid} H400 C440,{mid} 450,{yb} 490,{yb} H790', fill='none', stroke=S.INK, stroke_width=2.2))
    o.append(S.path(f'M560,{ya} C610,{ya} 620,{yb} 670,{yb}', fill='none', stroke=S.DIF, stroke_width=4))
    _dot(o, 60, ya, 7)
    _dot(o, 60, yb, 7)
    _dot(o, xn, mid, 9)
    o.append(T(60, ya - 17, 'doador', size=17, family=S.SERIF, anchor='start'))
    o.append(T(60, yb + 30, 'donatário', size=17, family=S.SERIF, anchor='start'))
    o.append(T(84, mid + 5, 'doação', size=17, family=S.SANS, weight='600', anchor='start', fill=S.INK))
    # --- promessa de recompensa: one will, a public that never joins it
    yp = 276
    o.append(S.line(60, yp, 322, yp, stroke=S.INK, stroke_width=2.2))
    _dot(o, 60, yp, 7)
    o.append(S.rect(322, yp - 8, 16, 16, fill=S.INK, stroke=S.INK))
    o.append(T(60, yp - 17, 'promessa de recompensa', size=17, family=S.SANS, weight='600', anchor='start'))
    for i, dy in enumerate((-36, -12, 12, 36)):
        xe = 560 + (12 if i in (1, 2) else 0)
        o.append(S.line(346, yp + dy * .25, xe - 22, yp + dy, stroke=S.MUTED, stroke_width=1.2, stroke_dasharray='2 5'))
        _dot(o, xe, yp + dy, 6, stroke=S.INK)
    o.append(T(600, yp + 6, 'quem lê o anúncio', size=17, family=S.SERIF, anchor='start'))
    # --- testamento: one will, nothing across
    yt = 396
    o.append(S.line(60, yt, 322, yt, stroke=S.INK, stroke_width=2.2))
    _dot(o, 60, yt, 7)
    o.append(S.rect(322, yt - 8, 16, 16, fill=S.INK, stroke=S.INK))
    o.append(T(60, yt - 17, 'testamento', size=17, family=S.SANS, weight='600', anchor='start'))
    return S.svg(W, H, 'Formação por duas manifestações e uma prestação; promessa de recompensa e testamento com uma só vontade', o)


def historia():
    W, H = 860, 430
    o = []
    xs, xm, xb = 190, 450, 560
    ys = [58, 118, 178, 238]
    ystem = 148
    names = ['verbis', 'litteris', 're', 'consensu']
    for y, n in zip(ys, names):
        o.append(T(24, y + 6, n, size=19, family=S.SANS, weight='600'))
        _dot(o, xs, y, 5.5)
        o.append(S.path(f'M{xs},{y} H{xm} C{xm + 55},{y} {xm + 40},{ystem} {xb - 50},{ystem}', fill='none', stroke=S.INK, stroke_width=1.8))
    # types counted on the two lines the source counts: re (4) and consensu (4)
    for y, lim in ((ys[2], False), (ys[3], True)):
        for i in range(4):
            o.append(S.circle(xs + 52 + i * 38, y, 5, fill=S.INK, stroke=S.INK))
        if lim:
            xe = xs + 52 + 3 * 38 + 28
            o.append(S.line(xe, y - 13, xe, y + 13, stroke=S.CONC, stroke_width=3))
    # the stem: the consent generalised, open at the end
    o.append(S.line(xb - 50, ystem, 820, ystem, stroke=S.INK, stroke_width=3))
    o.append(S.line(xb, ystem - 26, xb, ystem + 26, stroke=S.INK, stroke_width=3))
    o.append(S.path(f'M806,{ystem - 8} L820,{ystem} L806,{ystem + 8}', fill='none', stroke=S.INK, stroke_width=2))
    o.append(T(xb + 14, ystem - 34, 'generalização do consenso', size=17, family=S.SERIF))
    # the pacto: a defence with no action, rising to join the stem in the end
    yp = 346
    o.append(T(24, yp + 6, 'pacto', size=19, family=S.SANS, weight='600'))
    _dot(o, xs, yp, 5.5, stroke=S.CONC)
    o.append(S.path(f'M{xs},{yp} H640 C720,{yp} 700,{ystem} 760,{ystem}', fill='none', stroke=S.CONC, stroke_width=2, stroke_dasharray='6 6'))
    o.append(T(xs + 12, yp - 14, 'exceção defensiva, sem ação própria', size=16, family=S.SERIF, fill=S.CONC, anchor='start'))
    return S.svg(W, H, 'Genealogia da exigibilidade: formas romanas com seus tipos contados, o pacto à parte, a generalização do consenso', o)


def circulacao():
    W, H = 860, 470
    o = []
    o.append(T(44, 50, 'ordem jurídica', size=15, family=S.SERIF, fill=S.INK2, anchor='start'))
    c1 = (330, 250, 190)      # circulação de riqueza entre patrimônios
    c2 = (500, 250, 150)      # acordo
    o.append(S.circle(*c1, fill='none', stroke=S.INK, stroke_width=1.8))
    o.append(S.circle(*c2, fill='none', stroke=S.INK, stroke_width=1.8))
    o += _lens_hatch(c1, c2, 11, stroke=S.MUTED, stroke_width=.9)
    # set names
    o.append(T(245, 112, 'circulação de riqueza', size=18, family=S.SANS, weight='600', anchor='middle'))
    o.append(T(245, 136, 'entre patrimônios', size=18, family=S.SANS, weight='600', anchor='middle'))
    o.append(T(592, 254, 'acordo', size=18, family=S.SANS, weight='600', anchor='middle'))
    # lens: the contracts (the lens spans x 392..458 at the centre line, so the marks stand on the hatch with a paper halo)
    lens_x = (c2[0] - c2[2] + c1[0] + c1[2]) / 2
    halo = dict(stroke=S.PAPER, stroke_width=5, paint_order='stroke')
    for y, lab in ((222, 'seguro'), (262, 'doação'), (302, 'comodato')):
        _dot(o, lens_x - 50, y, 6.5, fill=S.INK)
        o.append(T(lens_x - 36, y + 5, lab, size=16, family=S.SERIF, anchor='start', **halo))
    o.append(T(lens_x, 178, 'contrato', size=18, family=S.SANS, weight='600', anchor='middle', **halo))
    # inheritance: circulation without the agreement
    _dot(o, 168, 300, 6.5, fill=S.INK)
    o.append(T(184, 305, 'herança', size=16, family=S.SERIF, anchor='start'))
    return S.svg(W, H, 'Função e estrutura: o contrato onde a circulação de riqueza e o acordo coincidem', o)


def campo():
    W, H = 940, 520
    o = []
    x0, x1, xm = 150, 900, 525
    y0, y1, ym = 36, 440, 238
    # the field: ruled sheet, the middle lines dashed
    o.append(S.line(x0, ym, x1, ym, stroke=S.DIF, stroke_width=2.4))
    o.append(S.line(xm, y0, xm, y1, stroke=S.GRID, stroke_width=1.2, stroke_dasharray='4 5'))
    # art. 51 reaches the whole consumer half, negotiated or not
    o.append(S.line(x0 + 6, 86, x1, 86, stroke=S.CONC, stroke_width=3))
    o.append(S.line(x0 + 6, 76, x0 + 6, 96, stroke=S.CONC, stroke_width=3))
    o.append(S.line(x1, 76, x1, 96, stroke=S.CONC, stroke_width=3))
    o.append(T(x0 + 20, 70, 'cláusula abusiva · art. 51', size=16, family=S.SERIF, fill=S.INK2, anchor='start'))
    # axes
    o.append(S.line(x0, y1 + 28, x1, y1 + 28, stroke=S.INK, stroke_width=1.6))
    o.append(S.path(f'M{x1 - 9},{y1 + 22} L{x1},{y1 + 28} L{x1 - 9},{y1 + 34}', fill='none', stroke=S.INK, stroke_width=1.6))
    o.append(T(x0, y1 + 62, 'negociado', size=17, family=S.SERIF, anchor='start'))
    o.append(T(x1, y1 + 62, 'predisposto', size=17, family=S.SERIF, anchor='end'))
    o.append(S.line(x0 - 28, y0, x0 - 28, y1, stroke=S.INK, stroke_width=1.6))
    o.append(S.path(f'M{x0 - 34},{y0 + 9} L{x0 - 28},{y0} L{x0 - 22},{y0 + 9}', fill='none', stroke=S.INK, stroke_width=1.6))
    o.append(T(x0 - 44, y0 + 46, 'relação', size=17, family=S.SERIF, anchor='end'))
    o.append(T(x0 - 44, y0 + 68, 'de consumo', size=17, family=S.SERIF, anchor='end'))
    o.append(T(x0 - 44, y1 - 6, 'fora', size=17, family=S.SERIF, anchor='end'))
    o.append(T(x0 - 44, y1 + 16, 'do CDC', size=17, family=S.SERIF, anchor='end'))
    # marks
    _dot(o, 735, 160, 11, fill=S.INK)
    o.append(T(755, 166, 'adesão e consumo', size=17, family=S.SANS, weight='600', anchor='start'))
    o.append(T(755, 190, 'a regra', size=16, family=S.SERIF, fill=S.INK2, anchor='start'))
    _dot(o, 300, 160, 8)
    o.append(T(320, 166, 'consumo negociado', size=17, family=S.SERIF, anchor='start'))
    _dot(o, 735, 340, 8)
    o.append(T(715, 344, 'contrato administrativo', size=17, family=S.SERIF, anchor='end'))
    o.append(T(715, 366, 'precedido de licitação', size=17, family=S.SERIF, anchor='end'))
    _dot(o, 300, 340, 8)
    o.append(T(320, 346, 'o cavalo do vizinho', size=17, family=S.SERIF, anchor='start'))
    return S.svg(W, H, 'Campo: forma de contratação contra relação de consumo', o)


def arco():
    W, H = 1000, 430
    o = []
    X = lambda yr: 78 + (yr - 1800) * 3.45
    ys = 226
    # spine and decade ticks
    o.append(S.line(X(1800), ys, X(2030), ys, stroke=S.INK, stroke_width=2.6))
    o.append(S.path(f'M{X(2030) - 10},{ys - 6} L{X(2030)},{ys} L{X(2030) - 10},{ys + 6}', fill='none', stroke=S.INK, stroke_width=2))
    for yr in range(1800, 2030, 10):
        h = 9 if yr % 100 == 0 else 5
        o.append(S.line(X(yr), ys - h, X(yr), ys + h, stroke=S.INK, stroke_width=1.2))
    for yr in (1900, 2000):
        o.append(T(X(yr), ys + 30, str(yr), size=15, family=S.SANS, fill=S.INK2, anchor='middle'))
    # lead-in before the scale: Rome and the Middle Ages, drawn dashed because it has no scale
    o.append(S.line(14, ys, X(1800) - 14, ys, stroke=S.INK, stroke_width=2, stroke_dasharray='5 5'))
    o.append(S.line(X(1800) - 12, ys - 10, X(1800) - 4, ys + 10, stroke=S.INK, stroke_width=1.6))
    o.append(S.line(X(1800) - 20, ys - 10, X(1800) - 12, ys + 10, stroke=S.INK, stroke_width=1.6))
    o.append(T(14, ys + 34, 'Roma e Idade Média', size=15, family=S.SERIF, fill=S.INK2, anchor='start'))
    # above: the private-law codes
    def code(yr, h, lab1, lab2=None, col=S.INK, anchor='middle', dx=0):
        x = X(yr)
        o.append(S.line(x, ys, x, ys - h, stroke=col, stroke_width=1.6))
        o.append(S.rect(x - 7, ys - h - 14, 14, 14, fill=col, stroke=col))
        o.append(T(x + dx, ys - h - 52, lab1, size=17, family=S.SANS, weight='600', anchor=anchor))
        if lab2:
            o.append(T(x + dx, ys - h - 28, lab2, size=16, family=S.SERIF, fill=S.INK2, anchor=anchor))
    code(1804, 86, 'Código francês', '1804', anchor='start', dx=-8)
    # the German code: drafted 1896, in force 1900: a short bar on the scale
    xa, xb = X(1896), X(1900)
    o.append(S.rect(xa, ys - 7, xb - xa, 7, fill=S.INK, stroke=S.INK))
    o.append(S.line((xa + xb) / 2, ys - 7, (xa + xb) / 2, ys - 132, stroke=S.INK, stroke_width=1.6))
    o.append(S.rect((xa + xb) / 2 - 7, ys - 146, 14, 14, fill=S.INK, stroke=S.INK))
    o.append(T((xa + xb) / 2, ys - 198, 'Código alemão', size=17, family=S.SANS, weight='600', anchor='middle'))
    o.append(T((xa + xb) / 2, ys - 174, '1896 · em vigor em 1900', size=16, family=S.SERIF, fill=S.INK2, anchor='middle'))
    code(1916, 70, 'Código Civil', '1916', anchor='start', dx=-8)
    code(2002, 112, 'Código Civil', '2002', col=S.DIF, anchor='end', dx=8)
    # below: the statutes that reshape the contract
    def law(yr, h, lab1, lab2, col=S.INK, anchor='start', dx=10, dy=0):
        x = X(yr)
        o.append(S.line(x, ys, x, ys + h, stroke=col, stroke_width=1.6))
        o.append(S.circle(x, ys + h, 7, fill=S.PAPER, stroke=col, stroke_width=2))
        o.append(T(x + dx, ys + h + 6 + dy, lab1, size=17, family=S.SANS, weight='600', anchor=anchor))
        o.append(T(x + dx, ys + h + 30 + dy, lab2, size=16, family=S.SERIF, fill=S.INK2, anchor=anchor))
    law(1988, 64, 'Constituição', '1988', anchor='end', dx=-12)
    law(1990, 124, 'Código de Defesa do Consumidor', 'Lei 8.078, de 11 de setembro de 1990', col=S.DIF, anchor='end', dx=-12)
    code(2019, 60, 'Lei 13.874', '2019 · arts. 421 e 421-A', anchor='start', dx=-8)
    return S.svg(W, H, 'Régua dos códigos e leis que o contrato atravessa, de 1804 a 2019', o)


MODES = dict(vontades=vontades, historia=historia, circulacao=circulacao, campo=campo, arco=arco)


def build(p: dict):
    mode = p['mode']
    if mode not in MODES:
        raise ValueError(f'tgc01_desenhos: unknown mode {mode!r}; known: {", ".join(MODES)}')
    return MODES[mode](), []
