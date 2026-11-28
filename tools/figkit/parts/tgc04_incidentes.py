"""Aula 04 (fundamentos): the ring and the small coin, in the course's hand. Params: mode = coins."""
from . import svg as S
from .tgc01_hand import name, gloss


def build(p):
    if p.get('mode', 'coins') != 'coins':
        raise ValueError(p.get('mode'))
    W, H = 540, 220
    o = []
    for x, r, lab in [(130, 50, 'anel'), (390, 30, 'vintém')]:
        o += [S.circle(x, 90, r, fill='none', stroke=S.INK, stroke_width=1.6), S.circle(x, 90, r - 8, fill='none', stroke=S.INK, stroke_width=1),
              name(x, 170, lab, anchor='middle')]
    o.append(gloss(270, 206, 'O pequeno valor confirma o acordo, sem comprar a saída.', anchor='middle'))
    return S.svg(W, H, 'Relações e efeitos · anel e vintém', o), []
