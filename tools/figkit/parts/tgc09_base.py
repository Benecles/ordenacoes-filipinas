"""Aula 09, ch.6: the common base under both parties, and what removes it (an instrument).
Sources: Luis Renato pp. 24, 29-30 (stable exchange rate as the shared circumstance; leasing, STJ split the loss);
CC art. 166, III (motive common to both and unlawful); frustração do fim and Enunciado 166 (coroação, art. 421);
CDC art. 6, V (supervening facts without the unforeseeability of art. 478). Categorical drawing. Params: none.
"""
from . import svg as S
from .tgc04_instr import W, dot, label, frame

H = 450
CH = [('a', 'Câmbio estável (leasing)'), ('b', 'Motivo ilícito comum'), ('c', 'Cortejo cancelado'), ('d', 'Fato posterior no consumo')]
AN = {
    'a': ('A base comum desaparece para os dois', 'A circunstância compartilhada era um câmbio estável, sem expectativa de alteração extraordinária;', 'o STJ repartiu igualmente o prejuízo da desvalorização entre as partes.', True),
    'b': ('O negócio é nulo (art. 166, III)', 'O motivo comum a ambas as partes é ilícito: o imóvel locado para um cassino ilegal parece lícito,', 'mas a causa compartilhada o contamina. É construção interpretativa, distinta da regra expressa.', False),
    'c': ('Frustração do fim, fora dos arts. 478–480', 'A sacada ainda podia ser alugada, mas a finalidade comum se perdera;', 'o Enunciado 166 situa o caso no art. 421, sem desequilíbrio entre as prestações.', False),
    'd': ('Revisão sem imprevisibilidade (CDC, art. 6º, V)', 'O fato superveniente que torna a prestação excessivamente onerosa basta;', 'não se exige o acontecimento extraordinário e imprevisível nem a extrema vantagem do art. 478.', False),
}


def build(p):
    y = 120
    ax, bx, bw = 180, 900, 0
    base = [S.rect(ax - 20, y + 70, bx - ax + 40, 30, fill=S.PAPER, stroke=S.INK, stroke_width=2),
            S.line(ax, y + 70, ax, y + 20, stroke=S.INK, stroke_width=1.8), S.line(bx, y + 70, bx, y + 20, stroke=S.INK, stroke_width=1.8),
            dot(ax, y + 8, S.INK, 11), dot(bx, y + 8, S.INK, 11),
            label(ax, y - 22, 'uma parte', 14, anchor='middle'), label(bx, y - 22, 'outra parte', 14, anchor='middle'),
            label((ax + bx) / 2, y + 91, 'base comum da operação', 14, anchor='middle', weight='600')]
    cx = (ax + bx) / 2 + 190
    crack = S.path(f'M{cx-20},{y+70} L{cx+6},{y+84} L{cx-8},{y+100}', fill='none', stroke=S.CONC, stroke_width=3)
    over = {
        'a': [crack, label((ax + bx) / 2, y + 140, 'o prejuízo se divide entre as duas', 13, anchor='middle', fill=S.DIF)],
        'b': [crack, S.line(ax, y + 20, bx, y + 20, stroke=S.CONC, stroke_width=1.5, stroke_dasharray='4 4'),
              label((ax + bx) / 2, y + 140, 'motivo comum ilícito', 13, anchor='middle', fill=S.CONC)],
        'c': [S.rect((ax + bx) / 2 - 30, y + 70, 60, 30, fill=S.PAPER, stroke=S.CONC, stroke_width=2, stroke_dasharray='4 3'),
              label((ax + bx) / 2, y + 140, 'a prestação segue possível; o fim comum, não', 13, anchor='middle', fill=S.CONC)],
        'd': [S.line(ax, y + 8, bx, y + 8, stroke=S.DIF, stroke_width=0), S.path(f'M{bx},{y + 60} L{bx - 60},{y + 60}', fill='none', stroke=S.DIF, stroke_width=2.6),
              label(bx - 70, y + 140, 'basta o fato superveniente', 13, anchor='end', fill=S.DIF)],
    }
    return S.svg(W, H, 'A base comum sob as duas partes e o que a retira',
                 frame('Base do negócio · o que a retira e qual o regime', CH, AN, base, over, 262, 322, H)), []
