"""Aula01, ch.5: a proof sheet of three clauses, struck in place, with the TJSP's marginalia beside each.

No params. Facts only from the lesson's ch.5 prose: TJSP, Ap 0116694-34.2009.8.26.0100 (6 set. 2012: loss of the
premium discount, not of the indemnity; art. 51, IV and par. 1, II; art. 47), TJSP, Ap 0001.035-25.2011.8.26.0223
(6 ago. 2013: denúncia imotivada of a collective health plan, abuse of the right to resilir, função social, boa-fé
objetiva) and TJSP, Ap 4009674-20.2013.8.26.0602 (extinction without request, continuity by novação, outro lote).
The clause bodies are grey placeholder bars, not text; the struck phrase and the proofreader's correction in blue
are the decision's own words. The bracket ties each strike to its marginal note.
"""
from . import svg as S


def build(p):
    o = []
    T = S.text
    W, H = 870, 430
    fx0, fx1 = 30, 590
    mx = 626
    o += [S.rect(fx0, 16, fx1 - fx0, 398, fill=S.PAPER, stroke=S.INK2, stroke_width=1.2),
          S.line(mx - 14, 16, mx - 14, 414, stroke=S.CONC, stroke_width=1.2, stroke_dasharray='2 5')]
    # folded corner is the backstage's sign; none here. Ruled sheet lines under each clause.
    blocks = [
        ('1', 'Seguro de furto de veículo', 'perda do direito à indenização', 'só a perda do desconto no prêmio',
         ('TJSP · 6 set. 2012', 'cláusula nula: art. 51, IV', 'e § 1º, II; art. 47'), 4),
        ('2', 'Plano de saúde coletivo', 'denúncia imotivada, aviso de sessenta dias', 'justa expectativa de renovação',
         ('TJSP · 6 ago. 2013', 'abuso do direito de resilir', 'função social, boa-fé objetiva'), 3),
        ('3', 'Promessa de venda do mesmo imóvel', 'extinção do contrato sem pedido dos compradores', 'continuidade por novação',
         ('TJSP · Ap 4009674', 'pedido alternativo: outro lote', 'a incorporadora não se opunha'), 2),
    ]
    y = 34
    for n, head, bad, good, note, _ in blocks:
        o.append(T(fx0 + 16, y + 20, n, size=18, family=S.SERIF, fill=S.INK2))
        o.append(T(fx0 + 44, y + 20, head, size=14.5, family=S.SANS, weight='600'))
        # placeholder body lines
        for i, w in enumerate((470, 440)):
            o.append(S.line(fx0 + 44, y + 40 + i * 14, fx0 + 44 + w, y + 40 + i * 14, stroke=S.GRID, stroke_width=3))
        sy = y + 80
        tw = len(bad) * 7.9
        o.append(T(fx0 + 44, sy, bad, size=13, fill=S.INK2))
        o.append(S.line(fx0 + 40, sy - 4, fx0 + 48 + tw, sy - 4, stroke=S.CONC, stroke_width=2.2))
        # proofreader's correction under the strike, with a caret
        cy = sy + 26
        o.append(S.path(f'M{fx0 + 52},{sy + 6} L{fx0 + 58},{sy + 12} L{fx0 + 64},{sy + 6}', fill='none', stroke=S.DIF, stroke_width=1.8))
        o.append(T(fx0 + 70, cy - 4, good, size=15, family=S.SERIF, fill=S.DIF, font_style='italic'))
        # leader from the strike to the margin note, with a bracket
        o.append(S.path(f'M{fx1 - 6},{y + 34} L{fx1 + 4},{y + 34} L{fx1 + 4},{y + 108} L{fx1 - 6},{y + 108}', fill='none', stroke=S.INK2, stroke_width=1.3))
        o.append(S.line(fx1 + 4, y + 71, mx - 14, y + 71, stroke=S.INK2, stroke_width=1.3))
        o.append(T(mx, y + 52, note[0], size=13, family=S.SANS, weight='600'))
        o.append(T(mx, y + 74, note[1], size=14, family=S.SERIF, fill=S.INK2, font_style='italic'))
        o.append(T(mx, y + 94, note[2], size=14, family=S.SERIF, fill=S.INK2, font_style='italic'))
        y += 130
    return S.svg(W, H, 'Folha de prova com três cláusulas riscadas e a anotação do TJSP na margem de cada uma', o), []
