"""Aula 10, chapter 3: the mandate and what its principal's revocation does. An instrument.

The reader picks the kind of mandate; a procuração folio answers: the strike of revocation lands (the line
of the mandate ends at the tick), or it fails against the seal (the line runs through).
Sources: CC arts. 683, 684, 685 (cláusula de irrevogabilidade: perdas e danos; condição de negócio bilateral ou
interesse exclusivo do mandatário: revogação ineficaz; em causa própria: ineficaz, não se extingue pela morte,
mandatário dispensado de prestar contas). Params: none. Positions ordinal, not a time scale.
"""
from . import svg as S

W, H = 1080, 456
CH = [
    ('a', 'sem cláusula de irrevogabilidade', 155),
    ('b', 'com cláusula de irrevogabilidade', 417),
    ('c', 'cláusula no interesse do mandatário', 679),
    ('d', 'mandato em causa própria', 941),
]
ANS = {
    'a': ('A revogação produz efeito', 'O mandato repousa na confiança: retirada a voz do mandante, o vínculo termina no ato.', True),
    'b': ('A revogação vale, mas custa', 'O mandante que revoga o mandato com cláusula de irrevogabilidade pagará perdas e danos (art. 683).', True),
    'c': ('A revogação é ineficaz', 'Cláusula que condiciona um negócio bilateral ou foi estipulada no exclusivo interesse do mandatário (art. 684).', False),
    'd': ('A revogação é ineficaz, e a morte não extingue', 'Na cláusula em causa própria o mandatário fica dispensado de prestar contas e pode transferir para si os bens (art. 685).', False),
}


def _folio(o, sealed, struck):
    x, y, w, h = 60, 128, 230, 280
    o.append(S.rect(x, y, w, h, fill=S.PAPER2, stroke=S.INK, stroke_width=2))
    o.append(S.rect(x + 22, y + 22, 120, 12, fill=S.INK, stroke='none'))
    for i in range(6):
        o.append(S.line(x + 22, y + 62 + i * 22, x + w - 22, y + 62 + i * 22, stroke=S.GRID, stroke_width=1.4))
    o.append(S.line(x + 22, y + h - 38, x + 120, y + h - 38, stroke=S.INK, stroke_width=1.5))
    o.append(S.text(x + 22, y + h - 18, 'mandante', size=12, family=S.SANS, fill=S.MUTED))
    if sealed:
        cx, cy = x + w - 62, y + h - 66
        o.append(S.circle(cx, cy, 30, fill=S.PAPER, stroke=S.CONC, stroke_width=3))
        o.append(S.circle(cx, cy, 21, fill='none', stroke=S.CONC, stroke_width=1.4))
        o.append(S.rect(cx - 9, cy - 3, 18, 14, fill=S.CONC, stroke='none'))
        o.append(S.path(f'M{cx-6},{cy-3} v-6 a6,6 0 0 1 12,0 v6', fill='none', stroke=S.CONC, stroke_width=2.4))
    if struck == 'full':
        o.append(S.line(x - 14, y + 20, x + w + 14, y + h - 20, stroke=S.DIF, stroke_width=4))
    elif struck == 'bounce':
        o.append(S.path(f'M{x-14},{y+20} L{x+70},{y+100}', fill='none', stroke=S.CONC, stroke_width=3.5))
        o.append(S.path(f'M{x+70},{y+100} l16,-6 m-16,6 l4,-17', fill='none', stroke=S.CONC, stroke_width=2.5))


def _line(o, ends, death, cost):
    y = 232
    x0, xr, xd = 360, 600, 800
    o.append(S.text(x0, 150, 'o mandato', size=13, family=S.SANS, fill=S.MUTED))
    o.append(S.circle(x0, y, 8, fill=S.PAPER, stroke=S.INK, stroke_width=2))
    xe = xr if ends else 1010
    o.append(S.line(x0 + 8, y, xe, y, stroke=S.DIF if ends else S.CONC, stroke_width=4))
    o.append(S.line(xr, y - 22, xr, y + 22, stroke=S.CONC if not ends else S.INK, stroke_width=2.5))
    o.append(S.text(xr, y - 32, 'revogação', size=13, family=S.SANS, weight='600', anchor='middle'))
    if death:
        o.append(S.line(xd, y - 22, xd, y + 22, stroke=S.INK, stroke_width=2.5))
        o.append(S.line(xd - 8, y - 8, xd + 8, y + 8, stroke=S.INK, stroke_width=2))
        o.append(S.line(xd - 8, y + 8, xd + 8, y - 8, stroke=S.INK, stroke_width=2))
        o.append(S.text(xd, y - 32, 'morte', size=13, family=S.SANS, weight='600', anchor='middle'))
    if cost:
        o.append(S.rect(xr, y + 46, 230, 30, fill=S.PAPER, stroke=S.CONC, stroke_width=2))
        o.append(S.line(xr + 10, y + 61, xr + 220, y + 61, stroke=S.CONC, stroke_width=2))
        o.append(S.text(xr + 115, y + 98, 'perdas e danos', size=13, family=S.SERIF, fill=S.CONC, anchor='middle'))


def build(p):
    o = [S.text(24, 30, 'Mandato · o que a revogação alcança', size=13, family=S.MONO)]
    for k, lab, cx in CH:
        o.append(f'<g data-opt="{k}" tabindex="0" role="button" aria-label="{S.esc(lab)}">')
        o.append(S.rect(cx - 125, 56, 250, 44, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
        o.append(S.text(cx, 84, lab, size=13, family=S.SANS, weight='600', anchor='middle'))
        o.append('</g>')
    spec = {'a': (False, 'full', True, False, False), 'b': (False, 'full', True, False, True),
            'c': (True, 'bounce', False, False, False), 'd': (True, 'bounce', False, True, False)}
    for k, lab, cx in CH:
        sealed, struck, ends, death, cost = spec[k]
        head, why, ok = ANS[k]
        col = S.DIF if ok else S.CONC
        o.append(f'<g data-ans="{k}"' + ('' if k == 'a' else ' display="none"') + '>')
        _folio(o, sealed, struck)
        _line(o, ends, death, cost)
        o.append(S.text(360, 368, head, size=21, family=S.SANS, weight='650', fill=col))
        for i, ln in enumerate(S.wrap(why, 78)):
            o.append(S.text(360, 398 + i * 24, ln, size=16, family=S.SERIF))
        o.append('</g>')
    return S.svg(W, H, 'Mandato: o efeito da revogação conforme a cláusula', o), []
