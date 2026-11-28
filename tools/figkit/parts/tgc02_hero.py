"""Aula 02 hero: Zeca's exclusivity as a two-strand cord with five forces radiating from it (a rose), in the course's hand
(DIRECTION.md, o vínculo; tgc01_hand). Nothing boxed: parties are hollow marks, each force a hairline ray that ends in a
named mark. Selecting a ray lights it and swaps the answer below (data-thread / data-answer, wired by the page).
Facts: Fischer and All-E created the Nova Schin campaign with Zeca under exclusivity; África lured him to Brahma;
REsp 1.316.149/SP (9ª Vara Cível: moral damages R$ 500 mil and R$ 100 mil; TJSP: unfair competition, about R$ 20 mi;
STJ 03/06/2014: Nancy Andrighi's vote prevails, relator outvoted). No weights are assigned to the forces."""
from __future__ import annotations
from . import svg as S
from .tgc01_hand import cord, rule, mark, name, gloss, art, wire, hit
from .tgc02_planta import FORCES

CX, CY = 390, 160
NAMES = {k: l for k, l, n, g, a in FORCES}
NOTES = {k: n for k, l, n, g, a in FORCES}


def _force(key, end, side, lines, dy=0):
    """One ray: hairline from the cord's middle to a hollow mark; label beside the mark."""
    ex, ey = end
    d = f'M{CX},{CY} L{ex},{ey}'
    body = [rule(d, S.INK, 1.0), mark(ex, ey, S.INK, 5.5), hit(min(ex, ex + (-150 if side == 'l' else 0)) - 6, ey - 20, 190, 62 + 16 * (len(lines) - 2))]
    tx = ex - 12 if side == 'l' else ex + 12
    anc = 'end' if side == 'l' else 'start'
    if side == 'c':
        tx, anc = ex, 'middle'
    y0 = ey - 3 + dy
    body.append(name(tx, y0 if side != 'c' else ey + 22, NAMES[key], anchor=anc, size=12))
    for i, ln in enumerate(lines):
        yy = (y0 if side != 'c' else ey + 22) + 16 * (i + 1)
        body.append(art(tx, yy, ln[1:], anchor=anc, size=11.5) if ln.startswith('#') else gloss(tx, yy, ln, anchor=anc, size=12))
    return wire(key, NAMES[key], body)


def desktop():
    o = []
    # the interference: África's loose strand reaches toward Zeca and does not tie
    zx, ax, bx = 530, 730, 900
    o += [S.path(f'M{ax - 9},{CY} L{zx + 20},{CY}', fill='none', stroke=S.CONC, stroke_width=1.8, stroke_dasharray='2 5', stroke_linecap='round'),
          rule(f'M{zx + 30},{CY - 6} L{zx + 21},{CY} L{zx + 30},{CY + 6}', S.CONC, 1.8),
          rule(f'M{ax + 9},{CY} L{bx - 9},{CY}', S.INK2, 1.0)]
    # the bond itself, two strands, from Nova Schin's mark to Zeca's
    nx = 250
    o += [cord(nx + 7, zx - 7, CY, amp=7, half=22, taper=26), mark(nx, CY, S.DIF), mark(zx, CY, S.DIF), S.circle(CX, CY, 3.2, fill=S.INK, stroke=S.INK, stroke_width=1)]
    o += [name(nx - 14, CY - 8, 'Nova Schin', anchor='end', size=12), gloss(nx - 14, CY + 9, 'campanha de Fischer · All-E', anchor='end', size=12),
          gloss(nx - 14, CY + 25, 'com exclusividade', anchor='end', size=12),
          name(zx, CY - 17, 'Zeca', anchor='middle', size=12),
          mark(ax, CY, S.CONC), mark(bx, CY, S.INK2),
          name(ax, CY + 30, 'África', col=S.CONC, anchor='middle', size=12), gloss(ax, CY + 46, 'aliciamento', col=S.CONC, anchor='middle', size=12),
          gloss(ax, CY + 62, 'anuncia a Brahma', anchor='middle', size=12)]
    # five forces
    o += [_force('liberdade', (215, 62), 'l', [NOTES['liberdade']]),
          _force('forca', (565, 62), 'r', [NOTES['forca']]),
          _force('relatividade', (560, 240), 'r', ['a prestação cabe', 'só às partes']),
          _force('social', (215, 240), 'l', ['o vínculo respeita', 'o meio que ele afeta']),
          _force('conduta', (395, 262), 'c', ['respeitar o contrato alheio · concorrência desleal', '#Lei 9.279/96'])]
    # the case, on its own hairline: three decisions in order
    x0, y0 = 772, 268
    o += [art(x0, y0 - 14, 'REsp 1.316.149/SP', col=S.INK2, size=11.5), rule(f'M{x0},{y0 + 3} V{y0 + 90}', S.INK2, 1.0)]
    for i, (a, b, col) in enumerate((('9ª Vara Cível · SP', 'morais de R$ 500 mil e R$ 100 mil', S.INK),
                                     ('TJSP · 3ª Câmara', 'condena em cerca de R$ 20 milhões', S.INK),
                                     ('STJ · 03/06/2014', 'Andrighi prevalece; relator vencido', S.DIF))):
        y = y0 + 4 + i * 36
        o += [mark(x0, y - 4, col, 4.5), name(x0 + 14, y, a, col=col, size=12), gloss(x0 + 14, y + 15, b, size=12)]
    return S.svg(1000, 366, 'Zeca e as cinco forças sobre o contrato de exclusividade', o).replace('viewBox="0 0 1000 366"', 'viewBox="0 44 1000 322"', 1)


def narrow():
    o = []
    cx, cy = 170, 190
    import math
    o += [cord(cx - 52, cx + 52, cy, amp=6, half=18, taper=20), mark(cx - 58, cy, S.DIF, 5), mark(cx + 58, cy, S.DIF, 5)]
    o += [name(cx - 66, cy + 4, 'Nova Schin', anchor='end', size=11), name(cx + 66, cy + 4, 'Zeca', anchor='start', size=11)]
    pos = {'liberdade': (-150, 96, 128, 'end'), 'forca': (-30, 244, 128, 'start'), 'relatividade': (42, 244, 262, 'start'), 'social': (138, 96, 262, 'end'), 'conduta': (90, 170, 302, 'middle')}
    for key, label, note, angle, answer in FORCES:
        a = math.radians(angle)
        ex, ey = cx + 78 * math.cos(a), cy + 78 * math.sin(a)
        _, tx, ty, anc = pos[key]
        words = label.split()
        body = [rule(f'M{cx},{cy} L{ex:.1f},{ey:.1f}', S.INK, 1.0), mark(ex, ey, S.INK, 4.5), hit(tx - (0 if anc == 'start' else 150 if anc == 'end' else 75), ty - 16, 150, 44)]
        lines = [' '.join(words[:-1]), words[-1]] if len(words) > 1 else [label]
        for i, ln in enumerate(lines):
            body.append(name(tx, ty + i * 15, ln, anchor=anc, size=11))
        o.append(wire(key, label, body))
    return S.svg(340, 340, 'Cinco forças sobre o contrato de exclusividade', o)


def build(p):
    answers = ''.join(f'<p data-answer="{k}"' + ('' if i == 0 else ' hidden') + '>' + S.esc(a) + '</p>' for i, (k, l, n, g, a) in enumerate(FORCES))
    return ('<div class="force-rose"><div class="rose-desktop">' + desktop() + '</div><div class="rose-mobile">' + narrow()
            + '</div><div class="force-readout">' + answers + '</div></div>'), []
