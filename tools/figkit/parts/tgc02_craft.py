"""Chapter drawings in the course's hand (tgc01_hand): soybean lots, an interrupted contract, compensation.

Sources: REsp 803.481/GO (lots); REsp 1.316.149/SP (interference, compensation); Pereira pp.14-16 (binding effect and
relativity). Geometry is schematic; no invented dates, amounts or document wording. Nothing boxed: the contract is a
two-strand cord between its parties, África a loose orange strand, compensation stems on a ruled scale."""
from . import svg as S
from .tgc01_hand import cord, rule, mark, name, gloss, art


def soy():
    out = []
    # Equal sack silhouettes: each mark represents 100 sacks, not a specimen.
    for row, (count, label) in enumerate(((20, '2.000 sacas · R$ 21,00 cada'), (10, '1.000 sacas · R$ 23,00 cada'))):
        y = 50 + row * 150
        out.append(name(24, y - 20, label, size=11.5))
        for k in range(count):
            x = 24 + (k % 10) * 32
            yy = y + (k // 10) * 44
            out.append(S.path(f'M{x+7} {yy} L{x+21} {yy} L{x+18} {yy+7} Q{x+33} {yy+34} {x+24} {yy+36} L{x+4} {yy+36} Q{x-5} {yy+34} {x+10} {yy+7} Z',
                              fill=S.PAPER, stroke=S.INK, stroke_width=1.0))
            out.append(S.line(x+8, yy+7, x+20, yy+7, stroke=S.DIF, stroke_width=2))
    out.append(gloss(24, 300, 'cada marca = 100 sacas', size=12))
    return S.svg(368, 316, 'Dois lotes de soja: vinte e dez marcas de cem sacas', out)


def contract(state):
    out = []
    ax, bx, y = 52, 316, 190
    title = {1: 'a dívida permanece interna', 2: 'interferência de fora', 3: 'depois do prazo'}[state]
    out.append(gloss(24, 30, title, size=14))
    mx = (ax + bx) // 2
    if state == 3:
        # the agreed term has ended: the bond thins to a hairline after the cut
        out += [cord(ax + 7, mx - 30, y, amp=6, half=20, taper=20), rule(f'M{mx - 30},{y} H{bx - 8}', S.INK2, 1.0, '2 5'),
                rule(f'M{mx - 30},{y - 12} V{y + 12}', S.CONC, 2), gloss(mx + 18, y + 34, 'vigência encerrada', col=S.CONC, anchor='middle', size=13)]
    else:
        out.append(cord(ax + 7, bx - 7, y, amp=6, half=20, taper=20))
    out += [mark(ax, y, S.DIF), mark(bx, y, S.DIF), gloss(mx - 50, y - 30, 'exclusividade', anchor='middle', size=14),
            name(mx, y + 62 if state != 3 else y + 70, 'partes vinculadas', col=S.DIF, anchor='middle', size=11.5)]
    if state == 2:
        zx = mx + 10
        out += [mark(zx + 70, 78, S.CONC), name(zx + 86, 82, 'África', col=S.CONC, size=11.5),
                S.path(f'M{zx + 66},84 C{zx + 40},120 {zx + 10},{y - 70} {zx},{y - 8}', fill='none', stroke=S.CONC, stroke_width=2),
                rule(f'M{zx - 7},{y - 10} L{zx},{y - 1} L{zx + 8},{y - 12}', S.CONC, 2)]
    if state == 3:
        zx = mx + 10
        out += [mark(zx + 70, 78, S.CONC), name(zx + 86, 82, 'África', col=S.CONC, size=11.5),
                S.path(f'M{zx + 66},84 C{zx + 40},120 {zx + 30},{y - 50} {zx + 20},{y - 18}', fill='none', stroke=S.CONC, stroke_width=1.0, stroke_dasharray='2 5')]
    return S.svg(368, 270, 'Contrato e limite externo, estado ' + str(state), out)


def awards():
    out = []
    # Position measures money: same baseline and a 5:1 height ratio.
    base, k = 262, .42
    out.append(rule(f'M64,{base} H342', S.INK, 1.0))
    for v in range(100, 501, 100):
        y = base - v * k
        out += [rule(f'M64,{y} H342', S.GRID, 1.0), art(54, y + 4, str(v), anchor='end', size=11.5)]
    out.append(gloss(24, 26, 'compensação moral · R$ mil', size=13))
    for x, amount, nm in ((134, 500, 'Fischer'), (264, 100, 'All-E')):
        y = base - amount * k
        out += [rule(f'M{x},{base} V{y}', S.DIF, 2), mark(x, y, S.DIF, 6, solid=True), name(x + 14, y + 4, str(amount), size=12.5), name(x, base + 22, nm, anchor='middle', size=12)]
    return S.svg(368, 300, 'Compensação moral restabelecida: quinhentos mil e cem mil reais', out)


def build(p):
    mode = p.get('mode', 'contrato')
    drawing = soy() if mode == 'soja' else awards() if mode == 'reparacao' else contract(int(p.get('state', 1)))
    return drawing, []
