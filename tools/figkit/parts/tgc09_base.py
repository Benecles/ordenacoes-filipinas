"""Aula 09, ch.6: the common base under both parties, and what removes it (an instrument).
Sources: Luis Renato pp. 24, 29-30 (stable exchange rate as the shared circumstance; leasing, STJ split the loss);
CC art. 166, III (motive common to both and unlawful); frustração do fim and Enunciado 166 (coroação, art. 421);
CDC art. 6, V (supervening facts without the unforeseeability of art. 478). Categorical drawing. Params: none.
"""
from . import svg as S
from .tgc04_instr import W, dot, label, frame

H = 452
CH = [('a', 'Câmbio estável (leasing)'), ('b', 'Motivo ilícito comum'), ('c', 'Cortejo cancelado'), ('d', 'Fato posterior no consumo')]
AN = {
    'a': ('A base comum desaparece para os dois', 'A circunstância compartilhada era um câmbio estável, sem expectativa de alteração extraordinária;', 'o STJ repartiu igualmente o prejuízo da desvalorização entre as partes.', True),
    'b': ('O negócio é nulo (art. 166, III)', 'O motivo comum a ambas as partes é ilícito: o imóvel locado para um cassino ilegal parece lícito,', 'mas a causa compartilhada o contamina. É construção interpretativa, distinta da regra expressa.', False),
    'c': ('Frustração do fim, fora dos arts. 478–480', 'A sacada ainda podia ser alugada, mas a finalidade comum se perdera;', 'o Enunciado 166 situa o caso no art. 421, sem desequilíbrio entre as prestações.', False),
    'd': ('Revisão sem imprevisibilidade (CDC, art. 6º, V)', 'O fato superveniente que torna a prestação excessivamente onerosa basta;', 'não se exige o acontecimento extraordinário e imprevisível nem a extrema vantagem do art. 478.', False),
}


def build(p):
    ax, bx = 150, 930
    deck_y, deck_h = 128, 26
    gy = 232
    mid = (ax + bx) / 2
    base = [S.line(30, gy, 1050, gy, stroke=S.INK, stroke_width=2), *S.hatch(30, gy, 1020, 10, step=10, stroke=S.GRID, stroke_width=1)]
    for x in (ax, bx):
        base += [S.rect(x - 22, deck_y + deck_h, 44, gy - deck_y - deck_h, fill=S.PAPER, stroke=S.INK, stroke_width=1.8),
                 S.circle(x, deck_y - 26, 10, fill=S.PAPER, stroke=S.INK, stroke_width=2.2),
                 S.line(x, deck_y - 16, x, deck_y, stroke=S.INK, stroke_width=2.2)]
    base += [label(ax, 60, 'uma parte', 14, anchor='middle', weight='600'), label(bx, 60, 'outra parte', 14, anchor='middle', weight='600'),
             S.rect(ax - 22, deck_y, bx - ax + 44, deck_h, fill=S.PAPER, stroke=S.INK, stroke_width=2),
             label(mid - 190, deck_y + 18, 'base comum da operação', 14, anchor='middle', weight='600'),
             label(mid, 184, 'circunstância que ambas as partes tinham por assente', 13, anchor='middle', fill=S.INK2)]
    over = {
        # a: the shared circumstance (stable exchange rate) goes; the loss is divided in two equal blocks
        'a': [S.rect(mid - 40, deck_y, 80, deck_h, fill=S.PAPER, stroke=S.DIF, stroke_width=2.6, stroke_dasharray='4 3'),
              S.path(f'M{mid - 40},{deck_y + deck_h} L{mid},{deck_y + deck_h + 12} L{mid + 40},{deck_y + deck_h}', fill='none', stroke=S.DIF, stroke_width=2),
              S.rect(ax + 30, 192, 140, 30, fill=S.PAPER, stroke=S.DIF, stroke_width=2.2), S.rect(bx - 170, 192, 140, 30, fill=S.PAPER, stroke=S.DIF, stroke_width=2.2),
              label(ax + 100, 212, 'metade do prejuízo', 13, anchor='middle', fill=S.DIF), label(bx - 100, 212, 'metade do prejuízo', 13, anchor='middle', fill=S.DIF),
              label(mid, 206, 'câmbio estável desaparece', 13, anchor='middle', fill=S.DIF)],
        # b: the unlawful motive common to both contaminates the whole deck
        'b': [*S.hatch(ax - 22, deck_y, bx - ax + 44, deck_h, step=8, stroke=S.CONC, stroke_width=1),
              S.line(ax - 22, deck_y - 6, bx + 22, deck_y - 6, stroke=S.CONC, stroke_width=2.4, stroke_dasharray='6 4'),
              S.line(mid - 18, deck_y - 22, mid + 18, deck_y + 4, stroke=S.CONC, stroke_width=3), S.line(mid - 18, deck_y + 4, mid + 18, deck_y - 22, stroke=S.CONC, stroke_width=3),
              label(mid, 206, 'motivo ilícito comum a ambas: nulidade', 13, anchor='middle', fill=S.CONC),
              label(mid, 226, 'o aluguel do imóvel para o cassino parece lícito', 13, anchor='middle', fill=S.INK2)],
        # c: the deck stands; the common end it led to is gone
        'c': [S.line(ax + 30, deck_y - 14, bx - 126, deck_y - 14, stroke=S.INK, stroke_width=1.6, stroke_dasharray='5 4'),
              S.rect(bx - 120, deck_y - 52, 40, 36, fill=S.PAPER, stroke=S.CONC, stroke_width=2, stroke_dasharray='4 3'),
              S.line(bx - 124, deck_y - 56, bx - 76, deck_y - 12, stroke=S.CONC, stroke_width=2.4), S.line(bx - 124, deck_y - 12, bx - 76, deck_y - 56, stroke=S.CONC, stroke_width=2.4),
              label(bx - 100, deck_y - 62, 'finalidade comum', 13, anchor='middle', fill=S.CONC),
              label(mid, 206, 'a prestação segue possível; o fim comum, não', 13, anchor='middle', fill=S.CONC),
              label(mid, 226, 'Enunciado 166: frustração do fim, art. 421', 13, anchor='middle', fill=S.INK2)],
        # d: consumer law asks only for the supervening fact; the two flags of art. 478 are not demanded
        'd': [S.line(bx, deck_y - 8, bx, deck_y - 44, stroke=S.DIF, stroke_width=2.6),
              S.path(f'M{bx},{deck_y - 44} L{bx - 28},{deck_y - 36} L{bx},{deck_y - 28}', fill=S.PAPER, stroke=S.DIF, stroke_width=2.4),
              label(bx - 36, deck_y - 36, 'fato superveniente', 13, anchor='end', fill=S.DIF),
              S.path(f'M{bx - 330},{deck_y - 8} V{deck_y - 40} L{bx - 300},{deck_y - 32} L{bx - 330},{deck_y - 24}', fill='none', stroke=S.INK2, stroke_width=1.6, stroke_dasharray='3 3'),
              label(bx - 340, deck_y - 36, 'extraordinário e imprevisível', 12, anchor='end', fill=S.INK2),
              S.path(f'M{bx - 560},{deck_y - 8} V{deck_y - 40} L{bx - 530},{deck_y - 32} L{bx - 560},{deck_y - 24}', fill='none', stroke=S.INK2, stroke_width=1.6, stroke_dasharray='3 3'),
              label(bx - 570, deck_y - 36, 'extrema vantagem', 12, anchor='end', fill=S.INK2),
              label(mid, 206, 'CDC, art. 6º, V: basta o fato superveniente', 13, anchor='middle', fill=S.DIF),
              label(mid, 226, 'sem as exigências do art. 478', 13, anchor='middle', fill=S.INK2)],
    }
    return S.svg(W, H, 'A base comum sob as duas partes e o que a retira',
                 frame('Base do negócio · o que a retira e qual o regime', CH, AN, base, over, 272, 328, H)), []
