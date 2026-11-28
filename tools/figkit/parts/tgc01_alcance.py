"""Aula01, ch.5: how far each provision of the CDC reaches along the life of one consumption relation.

No params. Horizontal position is the phase (pré-contratual, contratação, pós-contratual), not a duration. Facts:
CDC art. 2 caput and parágrafo único, art. 17, art. 29 (lesson's ch.5, quoted); Venosa p. 7 (tutela nas fases pré e
pós-contratual). The art. 17 victim is a point beside the contract because the victim did not contract.
"""
from . import svg as S


def build(p):
    o = []
    T = S.text
    W, H = 870, 380
    x0, xa, xb, x1 = 60, 300, 560, 810
    sy = 90
    o += [S.rect(x0, sy - 30, xa - x0, 60, fill='var(--dif-wash)', opacity='0.32'),
          S.rect(xb, sy - 30, x1 - xb, 60, fill='var(--dif-wash)', opacity='0.32'),
          S.line(xa, sy - 30, xa, sy + 30, stroke=S.INK, stroke_width=2),
          S.line(xb, sy - 30, xb, sy + 30, stroke=S.INK, stroke_width=2),
          S.line(x0, sy, x1, sy, stroke=S.INK, stroke_width=1)]
    for x, n in (((x0 + xa) / 2, 'fase pré-contratual'), ((xa + xb) / 2, 'contratação'), ((xb + x1) / 2, 'fase pós-contratual')):
        o.append(T(x, sy - 38, n, size=14, family=S.SANS, anchor='middle', weight='600'))
    o += [S.circle(xa, sy, 7, fill=S.PAPER, stroke=S.INK, stroke_width=2),
          S.circle(xb, sy, 7, fill=S.PAPER, stroke=S.INK, stroke_width=2)]

    def row(y, art, who, note):
        o.append(T(x0, y - 14, art, size=14, family=S.SANS, weight='600'))
        o.append(T(x0 + 110, y - 14, who, size=13, fill=S.INK2))
        if note:
            o.append(T(x0 + 110, y + 28, note, size=12.5, fill=S.INK2))

    # art. 2 caput: who acquires or uses as final destinatário, inside the contratação
    row(222, 'art. 2º', 'adquire ou utiliza como destinatário final', None)
    o.append(S.line(xa, 222, xb, 222, stroke=S.INK, stroke_width=5))
    # art. 2 p.u.: the collectivity that intervenes
    row(278, 'art. 2º, p. único', 'coletividade que intervém na relação', None)
    for x in range(int(xa) + 20, int(xb), 44):
        o.append(S.circle(x, 278, 6, fill=S.PAPER, stroke=S.INK, stroke_width=1.8))
    # art. 17: the victim of the event, a point away from the contract
    row(334, 'art. 17', 'vítimas do evento', None)
    ex = (xa + xb) / 2 + 40
    o.append(S.path(f'M{ex - 8},334 L{ex},326 L{ex + 8},334 L{ex},342 Z', fill=S.PAPER, stroke=S.CONC, stroke_width=2))
    o.append(T(ex + 20, 339, 'acidente de consumo', size=13, fill=S.INK2))
    # art. 29: exposed persons, from before the contract to after it
    o.append(S.line(x0, 166, x1, 166, stroke=S.DIF, stroke_width=5))
    o.append(S.path(f'M{x0 + 10},159 L{x0},166 L{x0 + 10},173 M{x1 - 10},159 L{x1},166 L{x1 - 10},173', fill='none', stroke=S.DIF, stroke_width=2))
    o.append(T(x0 + 4, 152, 'art. 29', size=14, family=S.SANS, weight='600'))
    o.append(T(x0 + 70, 152, 'pessoas expostas às práticas comerciais', size=13, fill=S.INK2))
    return S.svg(W, H, 'Alcance das equiparações a consumidor ao longo de uma relação de consumo', o), []
