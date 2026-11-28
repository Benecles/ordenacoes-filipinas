"""Aula 04: the prazo of an opção as a ruler (time strip) in the course's hand: a 2px rule with ticks, a hairline bracket.
Sources: Venosa 5.8 p. 44 (the oferente cannot withdraw during the period; accepting concludes the contract with no new
declaration by the oferente; after the period the titular of the goods is free to alienate or cede them to others);
Pereira III p. 76 (prazo certo frees the ofertante when it expires). No durations or amounts are asserted."""
from . import svg as S
from .tgc01_hand import rule, mark, name, gloss, bracket


def build(p):
    W, H = 900, 290
    x0, xp, x1, y = 60, 560, 840, 150
    o = [bracket(x0, xp, y - 30, True, S.DIF),
         name(x0, y - 62, 'o ofertante não pode retirar a oferta', S.DIF, size=12),
         gloss(x0, y - 42, 'prazo da opção'),
         rule(f'M{x0},{y} H{xp}', S.INK, 2), rule(f'M{xp},{y} H{x1}', S.INK, 1.2, '3 5'),
         rule(f'M{xp},{y - 30} V{y + 30}', S.CONC, 2.4),
         name(xp + 20, y - 62, 'prazo vencido', S.CONC, size=12), gloss(xp + 20, y - 42, 'o titular fica livre')]
    for i in range(11):
        x = x0 + i * (xp - x0) / 10
        o.append(rule(f'M{x},{y + 6} V{y + (20 if i % 5 == 0 else 12)}', S.INK, 1))
    ax = 300
    o += [mark(ax, y, S.DIF), rule(f'M{ax},{y + 8} V232', S.DIF, 2), S.rect(ax - 8, 232, 16, 16, fill=S.PAPER, stroke=S.DIF, stroke_width=2),
          gloss(ax + 20, 236, 'o oblato aceita', S.DIF), gloss(ax + 20, 256, 'contrato concluído, sem nova manifestação do ofertante', S.DIF)]
    tx = 740
    o += [mark(tx, y, S.INK, r=6), rule(f'M{tx},{y + 8} V218 H{tx + 70}', S.INK, 1.2, '3 5'), mark(tx + 78, 218, S.INK, r=6),
          gloss(tx + 78, 246, 'terceiro', anchor='middle')]
    return S.svg(W, H, 'O prazo da opção: oferta mantida durante o prazo; vencido, o titular fica livre', o), []
