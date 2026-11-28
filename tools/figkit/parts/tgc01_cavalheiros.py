"""Aula01, ch.3: how far the legal order reaches an agreement made without a contract.

No params. Facts only from the lesson's ch.3 passage (Venosa pp. 17-18; Martins-Costa): companies avoid contracting and
settle exchanges by the given word, a letter of intent or a gentlemen's agreement; when conflict or resisted claim
arises, abuso de direito and enriquecimento sem causa may apply, the text of the deal informs the judge of the parties'
will, and boa-fé objetiva makes the agreement a communication that generates legitimate expectations, with duties of
solicitude and liability for damages. The orange line is that trigger; position carries the relation, not a scale.
"""
from . import svg as S


def build(p):
    o = []
    T = S.text
    W, H = 870, 372
    sx0, sx1, sy0, sy1 = 44, 250, 70, 290
    gx = 340
    # the letter: an unsealed sheet, dashed edge, ruled bars for body text
    o.append(S.line(sx0, sy0, sx0, sy1, stroke=S.INK2, stroke_width=1))
    for i in range(8):
        w = 150 if i % 3 != 2 else 100
        o.append(S.line(sx0 + 22, sy0 + 36 + i * 20, sx0 + 22 + w, sy0 + 36 + i * 20, stroke=S.INK2, stroke_width=1))
    o.append(T(sx0, 50, 'carta de intenções', size=14, family=S.SANS, weight='600'))
    o.append(T(sx0, 314, 'sem contrato · palavra dada', size=12.5, fill=S.INK2))
    o.append(T(sx0, 332, 'acordo de cavalheiros', size=12.5, fill=S.INK2))
    # the legal order, hatched, past the trigger
    o.append(S.rect(gx, 40, 830 - gx, 270, fill='var(--dif-wash)', opacity='0.55'))
    o.append(T(gx + 10, 32, 'ordem jurídica', size=14, family=S.SANS, weight='600'))
    o.append(S.line(gx, 30, gx, 342, stroke=S.CONC, stroke_width=2.2))
    o.append(T(gx - 8, 356, 'conflito ou pretensão resistida', size=12.5, fill=S.CONC, anchor='end'))
    rows = [(100, 'abuso de direito', None),
            (170, 'enriquecimento sem causa', None),
            (240, 'boa-fé objetiva', 'expectativa legítima, deveres de solicitude, danos')]
    for y, a, b in rows:
        o.append(S.line(800, y, sx1 + 8, y, stroke=S.DIF, stroke_width=3))
        o.append(S.path(f'M{sx1 + 18},{y - 7} L{sx1 + 6},{y} L{sx1 + 18},{y + 7}', fill='none', stroke=S.DIF, stroke_width=2.4))
        o.append(S.circle(800, y, 6, fill=S.PAPER, stroke=S.DIF, stroke_width=2))
        o.append(T(gx + 24, y - 12, a, size=14.5, family=S.SANS, weight='600'))
        if b:
            o.append(T(gx + 24, y + 22, b, size=12.5, fill=S.INK2))
    return S.svg(W, H, 'Acordo sem contrato: a ordem jurídica o alcança, por três vias, quando surge conflito', o), []
