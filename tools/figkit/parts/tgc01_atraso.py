"""Aula 01, chapter 4: the appeal's verbal installment agreement and the limit on rescission (instrumento).

A strip of installment stubs, paid ones hatched, the last one overdue and dashed, with a line running on to
'rescindir a avença'. The reader picks one of the grounds the TJSP invoked (boa-fe objetiva and funcao social,
CC arts. 421-422; vedacao ao enriquecimento sem causa, art. 884); the drawing bars the line from the overdue stub to
the rescission. Facts: TJSP, Apelacao 0001424-29.2012.8.26.0464 (15/05/2015): atraso na quitacao nao bastou, por si,
para rescindir. No number of installments is asserted: the strip runs off the left edge. Params: none.
"""
from . import svg as S
from .tgc01_hand import hit as hitbox

W, H = 900, 390
GROUNDS = [
    ('a', 'Boa-fé objetiva', 'Boa-fé objetiva e função social', 'arts. 421 e 422'),
    ('b', 'Função social', 'Função social e boa-fé objetiva', 'arts. 421 e 422'),
    ('c', 'Enriquecimento sem causa', 'Vedação ao enriquecimento sem causa', 'art. 884'),
]


def build(p):
    o = []
    T = S.text
    ly = 96
    o.append(T(24, 28, 'Ajuste verbal · parcelas do financiamento bancário · sem contagem de parcelas', size=13, family=S.MONO, fill=S.INK2))
    # the installments: one ink line running off to the left, a hollow-to-solid mark per paid stub
    o.append(S.path(f'M18,{ly} H{28 + 5 * 94 + 40}', fill='none', stroke=S.INK, stroke_width=2, stroke_linecap='round'))
    xs = [60 + i * 94 for i in range(5)]
    for x in xs:
        o.append(S.circle(x, ly, 6, fill=S.INK, stroke=S.INK, stroke_width=1.8))
        o.append(T(x, ly + 28, 'paga', size=13, family=S.SERIF, anchor='middle', fill=S.INK2, font_style='italic'))
    xl = 60 + 5 * 94
    o.append(S.circle(xl, ly, 6.5, fill=S.PAPER, stroke=S.CONC, stroke_width=2.2))
    o.append(T(xl, ly - 18, 'atraso na quitação', size=12.5, family=S.SANS, anchor='middle', weight='600', fill=S.CONC, letter_spacing='0.06em'))
    rx = 800
    o.append(S.path(f'M{xl + 8},{ly} H{rx - 12}', fill='none', stroke=S.CONC, stroke_width=2, stroke_linecap='round'))
    o.append(S.circle(rx, ly, 6.5, fill=S.PAPER, stroke=S.INK, stroke_width=1.8))
    o.append(T(rx, ly - 18, 'RESCINDIR', size=12.5, family=S.SANS, weight='600', anchor='middle', letter_spacing='0.08em'))
    o.append(T(rx, ly + 28, 'a avença', size=13, family=S.SERIF, anchor='middle', fill=S.INK2, font_style='italic'))
    # grounds: three named choices on a hairline
    o.append(T(30, 180, 'FUNDAMENTO QUE A DECISÃO INVOCA', size=11.5, family=S.SANS, weight='600', fill=S.INK2, letter_spacing='0.1em'))
    bw = 280
    o.append(S.line(30, 232, 30 + 3 * bw, 232, stroke=S.INK2, stroke_width=1))
    for i, (key, lab, _, _) in enumerate(GROUNDS):
        x = 30 + i * bw
        o.append(f'<g data-opt="{key}" tabindex="0" role="button" aria-label="{S.esc(lab)}">')
        o.append(hitbox(x, 196, bw - 10, 44))
        o.append(T(x, 224, lab, size=14.5, family=S.SANS, weight='600'))
        o.append('</g>')
    bx = (xl + rx) / 2
    for key, _, head, art in GROUNDS:
        o.append(f'<g data-ans="{key}"' + ('' if key == 'a' else ' display="none"') + '>')
        o.append(S.line(bx, ly - 22, bx, ly + 22, stroke=S.DIF, stroke_width=3))
        o.append(S.line(bx - 12, ly - 12, bx + 12, ly + 12, stroke=S.DIF, stroke_width=2))
        o.append(S.line(bx - 12, ly + 12, bx + 12, ly - 12, stroke=S.DIF, stroke_width=2))
        x = 30 + 'abc'.index(key) * bw
        o.append(S.line(x, 232, x + 190, 232, stroke=S.DIF, stroke_width=2))
        o.append(S.line(30, 262, 30, 338, stroke=S.DIF, stroke_width=2))
        o.append(T(50, 290, f'{head} · {art}', size=19, family=S.SANS, weight='650', fill=S.DIF))
        o.append(T(50, 324, 'O atraso na quitação não bastou, por si, para rescindir a avença.', size=16, family=S.SERIF))
        o.append('</g>')
    return S.svg(900, 360, 'Atraso nas parcelas e limite à rescisão no ajuste verbal', o), []
