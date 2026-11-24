"""Paired utility strips, not a rent scale: Martins-Costa pp.38–39.

Full / partial / impeded are the source's distinctions; partial has no quantity.
"""
from . import svg as S


def build(p):
    out = []
    for i, (label, kind) in enumerate([('Vestuário', 'impedida'), ('Banco', 'parcial'), ('Farmácia', 'integral')]):
        y = 44 + i * 112
        out.append(S.text(20, y, label, size=20, family=S.SERIF))
        out.append(S.rect(20, y+14, 310, 12, fill=S.PAPER2, stroke=S.INK))
        out.append(S.rect(20, y+34, 310, 22, fill=S.PAPER2, stroke=S.INK, stroke_dasharray='4 4' if kind=='impedida' else None))
        if kind == 'parcial':
            # A broken edge means partial utility, never a fraction of the rent.
            out.append(S.path(f'M20,{y+34} H147 l-7,6 l14,5 l-14,5 l7,6 H20 Z', fill=S.PAPER, stroke=S.INK))
        elif kind == 'integral':
            out += S.hatch(21, y+35, 308, 20, step=12, stroke=S.GRID)
        out.append(S.text(20, y+83, 'Fruição ' + kind, size=18, family=S.SERIF))
    out.append(S.text(20, 398, 'A posse subsiste nas três lojas.', size=18, family=S.SERIF))
    return S.svg(360, 420, 'Posse e fruição: vestuário, banco e farmácia; sem escala quantitativa', out), []
