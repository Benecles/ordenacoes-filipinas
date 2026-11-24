"""Chapter instruments: soybean lots, an interrupted contract, compensation.

Sources: REsp 803.481/GO (lots); REsp 1.316.149/SP (interference,
compensation); Pereira pp.14–16 (binding effect and relativity).
Geometry is schematic; no invented dates, amounts or document wording.
"""
from . import svg as S


def soy():
    out = []
    # Equal sack silhouettes: each mark represents 100 sacks, not a specimen.
    for row, (count, label) in enumerate(((20, '2.000 sacas · R$ 21,00 cada'),
                                           (10, '1.000 sacas · R$ 23,00 cada'))):
        y = 50 + row * 150
        out.append(S.text(24, y - 20, label, size=18, family=S.SERIF))
        for k in range(count):
            x = 24 + (k % 10) * 32
            yy = y + (k // 10) * 44
            out.append(S.path(f'M{x+7} {yy} L{x+21} {yy} L{x+18} {yy+7} '
                              f'Q{x+33} {yy+34} {x+24} {yy+36} L{x+4} {yy+36} '
                              f'Q{x-5} {yy+34} {x+10} {yy+7} Z',
                              fill=S.PAPER, stroke=S.INK, stroke_width=1.3))
            out.append(S.line(x+8, yy+7, x+20, yy+7, stroke=S.DIF, stroke_width=2))
    out.append(S.text(24, 300, 'Cada marca = 100 sacas', size=16, family=S.SERIF, fill=S.INK2))
    return S.svg(368, 326, 'Dois lotes de soja: vinte e dez marcas de cem sacas', out)


def contract(state):
    out = []
    # The two signatures share one sheet; an outside pen crosses its edge.
    out.append(S.path('M28 76 L272 76 L272 312 L28 312 Z', fill=S.PAPER,
                      stroke=S.INK, stroke_width=1.5))
    for y, end in ((134, 238), (150, 246), (166, 214)):
        out.append(S.line(52, y, end, y, stroke=S.GRID, stroke_width=1.2))
    out.append(S.text(52, 111, 'Exclusividade', size=19, family=S.SERIF))
    out.append(S.line(52, 245, 248, 245, stroke=S.INK2, stroke_width=1))
    for x in (56, 165):
        out.append(S.path(f'M{x} 234 q10 -22 13 -4 q6 12 14 -8 q-3 23 21 6',
                          fill='none', stroke=S.DIF, stroke_width=1.8))
    out.append(S.text(52, 281, 'partes vinculadas', size=17, family=S.SERIF, fill=S.DIF))
    if state == 1:
        out.append(S.text(28, 42, 'A dívida permanece interna', size=18, family=S.SERIF))
    elif state == 2:
        out.append(S.text(28, 42, 'Interferência de fora', size=18, family=S.SERIF))
        out.append(S.path('M322 113 L336 126 L238 224 L220 230 L226 212 Z',
                          fill=S.PAPER, stroke=S.CONC, stroke_width=2))
        out.append(S.path('M220 230 L232 215 L238 224 Z', fill=S.CONC, stroke=S.CONC))
        out.append(S.path('M220 230 l-16 12 l12 9 l-21 15', fill='none',
                          stroke=S.CONC, stroke_width=2))
        out.append(S.text(283, 93, 'África', size=17, family=S.SERIF))
    else:
        # The legal boundary opens only when the agreed term has ended.
        out.append(S.rect(268, 178, 8, 70, fill=S.PAPER, stroke='none'))
        out.append(S.line(272, 178, 326, 202, stroke=S.INK2, stroke_width=1.5))
        out.append(S.text(28, 42, 'Depois do prazo', size=18, family=S.SERIF))
        out.append(S.text(42, 211, 'vigência encerrada', size=17, family=S.SERIF))
    return S.svg(368, 340, 'Contrato e limite externo, estado '+str(state), out)


def awards():
    out = []
    # Position measures money: same baseline and a 5:1 height ratio.
    for v in range(0, 501, 100):
        y = 288 - v * .42
        out.append(S.line(64, y, 342, y, stroke=S.GRID, stroke_width=1))
        out.append(S.text(52, y+5, str(v), size=14, anchor='end', fill=S.INK2))
    out.append(S.text(24, 32, 'Compensação moral · R$ mil', size=18, family=S.SERIF))
    for x, amount, name in ((112, 500, 'Fischer'), (252, 100, 'All-E')):
        out.append(S.rect(x, 288-amount*.42, 44, amount*.42, fill=S.DIF))
        out.append(S.text(x+22, 288-amount*.42-12, str(amount), size=18,
                          family=S.SERIF, anchor='middle'))
        out.append(S.text(x+22, 319, name, size=18, family=S.SERIF, anchor='middle'))
    return S.svg(368, 342, 'Compensação moral restabelecida: quinhentos mil e cem mil reais', out)


def build(p):
    mode = p.get('mode', 'contrato')
    drawing = soy() if mode == 'soja' else awards() if mode == 'reparacao' else contract(int(p.get('state', 1)))
    return drawing, []
