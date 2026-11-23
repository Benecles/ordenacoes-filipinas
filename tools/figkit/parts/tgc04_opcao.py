"""Aula 04: the prazo of an opção as a measured strip (language: ruler / time strip).
Sources: Venosa 5.8 p. 44 (the oferente cannot withdraw during the period; accepting concludes the contract with no new
declaration by the oferente; after the period the titular of the goods is free to alienate or cede them to others);
Pereira III pp. 76 (prazo certo frees the ofertante when it expires). No durations or amounts are asserted: the
strip's length is the prazo, whatever the parties fixed.
"""
from . import svg as S


def build(p):
    o = []
    W, H = 900, 300
    x0, xp, x1, y = 60, 560, 840, 150
    t = lambda x, yy, s, **kw: o.append(S.text(x, yy, s, size=kw.pop('size', 14), family=S.SANS, **kw))
    # the prazo: a ruled band with ticks; hatched inside because the ofertante is held there
    o += S.hatch(x0, y - 22, xp - x0, 44, step=12, stroke=S.GRID, stroke_width=1)
    o += [S.rect(x0, y - 22, xp - x0, 44, fill='none', stroke=S.INK, stroke_width=2),
          S.line(xp, y - 40, xp, y + 40, stroke=S.INK, stroke_width=3),
          S.line(x0, y, x1, y, stroke=S.INK, stroke_width=1.5),
          S.line(xp, y, x1, y, stroke=S.INK, stroke_width=1.5, stroke_dasharray='3 5')]
    for i in range(0, 11):
        x = x0 + i * (xp - x0) / 10
        o.append(S.line(x, y + 22, x, y + 30 if i % 5 else y + 36, stroke=S.INK, stroke_width=1))
    t(x0, 88, 'o ofertante não pode retirar a oferta', weight='600')
    t(x0, 108, 'prazo da opção', size=13)
    t(xp + 20, 88, 'prazo vencido', weight='600')
    t(xp + 20, 108, 'o titular fica livre', size=13)
    # acceptance inside the window: a hollow dot, a thread down to the concluded contract (a square)
    ax = 300
    o += [S.circle(ax, y, 8, fill=S.PAPER, stroke=S.DIF, stroke_width=2.4),
          S.line(ax, y + 8, ax, 236, stroke=S.DIF, stroke_width=2.4),
          S.rect(ax - 11, 236, 22, 22, fill=S.PAPER, stroke=S.DIF, stroke_width=2.4)]
    t(ax + 22, 232, 'o oblato aceita', size=13, fill=S.DIF)
    t(ax + 22, 254, 'contrato concluído, sem nova manifestação do ofertante', size=13, fill=S.DIF)
    # after the prazo: the goods may go to a third party
    tx = 740
    o += [S.circle(tx, y, 7, fill=S.PAPER, stroke=S.INK, stroke_width=2),
          S.path(f'M{tx},{y + 8} V218 H{tx + 70}', fill='none', stroke=S.INK, stroke_width=1.5, stroke_dasharray='3 5'),
          S.circle(tx + 78, 218, 6, fill=S.PAPER, stroke=S.INK, stroke_width=2)]
    t(tx + 78, 246, 'terceiro', size=13, anchor='middle')
    return S.svg(W, H, 'O prazo da opção: oferta mantida durante o prazo; vencido, o titular fica livre', o), []
