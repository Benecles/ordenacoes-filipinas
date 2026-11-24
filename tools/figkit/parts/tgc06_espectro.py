"""Aula 06, chapter 4: who writes the content, from the paritário to the contrato coativo.

Five rows, each a bar of twelve clause cells. An ink cell is a clause fixed by one side
(the predisponente), a hollow cell is a clause the other side can still discuss, a hatched
cell is a clause imposed by law or State (ink only: colour is kept for the limit and the answer). The count of each kind carries the
classification. Facts: Venosa p.16 (contrato-tipo: cláusulas predispostas, mas da vontade
paritária de ambas; adesão: elaboração unilateral), p.17 (contrato coativo: cláusulas
totalmente predispostas, ambas as partes forçadas a contratar), Zanini p.9 (espaço
estreito de negociação: preço, dados pessoais, objeto), Pereira p.69 (contrato-tipo:
cláusulas alteráveis ou canceláveis por outras substitutivas). The dirigido row follows
the lesson's text (o Estado impõe parte do conteúdo). Params: mobile (bool).
Geometry is schematic: the twelve cells are a ruler, not a statistic.
"""
from . import svg as S

N = 12
ROWS = (  # (label, [ink, open, law])
    ('Paritário', (0, 12, 0)),
    ('Contrato-tipo', (8, 4, 0)),
    ('Adesão', (11, 1, 0)),
    ('Dirigido', (0, 7, 5)),
    ('Coativo', (0, 0, 12)),
)


def _cell(x, y, w, h, kind):
    if kind == 'ink':
        return S.rect(x, y, w, h, fill=S.INK, stroke=S.INK, stroke_width=1)
    if kind == 'open':
        return S.rect(x, y, w, h, fill=S.PAPER, stroke=S.INK, stroke_width=1.8)
    return S.rect(x, y, w, h, fill=S.PAPER, stroke=S.INK, stroke_width=1.8) + ''.join(
        S.hatch(x, y, w, h, step=8, stroke=S.INK, stroke_width=1.2))


def _kinds(c):
    # laid out left to right: what one side wrote, what stays open, what the law fixed
    return ['ink'] * c[0] + ['open'] * c[1] + ['law'] * c[2]


def build(p):
    if p.get('mobile', False):
        w, cw, gap, x0, rowh = 340, 22, 4, 14, 62
        o = []
        for i, (lab, c) in enumerate(ROWS):
            y = 10 + i * rowh
            o.append(S.text(x0, y + 16, lab, size=15, family=S.SANS, weight='600'))
            for j, k in enumerate(_kinds(c)):
                o.append(_cell(x0 + j * (cw + gap), y + 26, cw, 24, k))
        ly = 10 + 5 * rowh + 8
        for i, (k, t) in enumerate((('ink', 'fixada por um dos lados'), ('open', 'aberta à discussão'), ('law', 'imposta pela lei ou pelo Estado'))):
            o.append(_cell(x0, ly + i * 24, 14, 14, k))
            o.append(S.text(x0 + 24, ly + i * 24 + 12, t, size=13, family=S.SERIF))
        return S.svg(w, ly + 3 * 24 + 6, 'Quem escreve as cláusulas em cada modo de contratar', o), []
    w, cw, gap, x0, rowh = 900, 44, 6, 190, 54
    o = []
    for i, (lab, c) in enumerate(ROWS):
        y = 14 + i * rowh
        o.append(S.text(24, y + 26, lab, size=16, family=S.SANS, weight='600'))
        for j, k in enumerate(_kinds(c)):
            o.append(_cell(x0 + j * (cw + gap), y + 6, cw, 30, k))
    ly = 14 + 5 * rowh + 12
    lx = x0
    for k, t, dx in (('ink', 'cláusula fixada por um dos lados', 0), ('open', 'aberta à discussão', 270), ('law', 'imposta pela lei ou pelo Estado', 470)):
        o.append(_cell(lx + dx, ly - 12, 14, 14, k))
        o.append(S.text(lx + dx + 24, ly, t, size=13, family=S.SERIF))
    return S.svg(w, ly + 14, 'Quem escreve as cláusulas em cada modo de contratar', o), []
