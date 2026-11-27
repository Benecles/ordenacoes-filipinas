"""Aula 06, chapter 2: the order of performance, an instrument.

A time axis with two prestações in the order the parties agreed (A performs first,
B last). The reader picks who refuses and why; the drawing answers with what the
refusal is worth. Facts: Venosa p.25 (só entre prestações simultaneamente exigíveis);
STJ REsp 981.750 (quem deve prestar primeiro não recusa por conjectura; quem presta
por último pode adiar enquanto o outro não cumpre; a exceção não cabe diante de
descumprimento parcial e mínimo). Params: none. Positions are ordinal, not a time scale.
"""
from . import svg as S

W, H = 1080, 400
CHOICES = [
    ('a', 'A recusa antes de B vencer', 150),
    ('b', 'B recusa, e A ainda não cumpriu', 520),
    ('c', 'B recusa por falta mínima de A', 890),
]
ANS = {
    'a': ('não cabe', 'quem deve prestar primeiro não invoca a espera do cumprimento futuro de B', False),
    'b': ('cabe', 'quem presta por último pode adiar a sua prestação enquanto A não satisfizer a própria', True),
    'c': ('não cabe', 'a recusa guarda proporcionalidade: descumprimento parcial e mínimo não a sustenta', False),
}


def build(p):
    o = []
    T = S.text
    o.append(T(24, 30, 'Ordem ajustada das prestações · sem escala de tempo', size=13, family=S.MONO))
    # axis
    y = 118
    o.append(S.line(60, y, 1020, y, stroke=S.INK, stroke_width=2))
    for x, lab, sub in [(260, 'A presta', 'vence primeiro'), (800, 'B presta', 'vence por último')]:
        o.append(S.circle(x, y, 9, fill=S.PAPER, stroke=S.INK, stroke_width=2))
        o.append(T(x, y - 26, lab, size=16, family=S.SERIF, anchor='middle'))
        o.append(T(x, y + 36, sub, size=13, family=S.SERIF, anchor='middle', fill=S.MUTED))
    o.append(S.path('M1010,112 L1020,118 L1010,124', fill='none', stroke=S.INK, stroke_width=2))
    # choices
    for key, lab, cx in CHOICES:
        o.append(f'<g data-opt="{key}" tabindex="0" role="button" aria-label="{S.esc(lab)}">')
        o.append(S.rect(cx - 150, 168, 300, 44, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
        o.append(T(cx, 196, lab, size=14, family=S.SANS, weight='600', anchor='middle'))
        o.append('</g>')
    # answers
    for key, lab, cx in CHOICES:
        verdict, why, ok = ANS[key]
        col = S.DIF if ok else S.CONC
        disp = None if key == 'a' else 'none'
        o.append(f'<g data-ans="{key}"' + ('' if disp is None else ' display="none"') + '>')
        o.append(S.line(cx, 212, cx, 262, stroke=col, stroke_width=2))
        o.append(S.rect(60, 262, 960, 100, fill=S.PAPER, stroke=col, stroke_width=2))
        o.append(T(84, 304, 'A exceção ' + verdict, size=22, family=S.SANS, weight='650', fill=col))
        o.append(T(84, 338, why[0].upper() + why[1:] + '.', size=16, family=S.SERIF))
        o.append('</g>')
    return S.svg(W, H, p.get('title', 'Ordem das prestações: quem pode recusar e quando'), o), []
