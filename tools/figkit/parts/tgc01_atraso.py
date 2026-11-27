"""Aula 01, chapter 4: the appeal's verbal installment agreement and the limit on rescission (instrumento).

A strip of installment stubs, paid ones hatched, the last one overdue and dashed, with a line running on to
'rescindir a avença'. The reader picks one of the grounds the TJSP invoked (boa-fe objetiva and funcao social,
CC arts. 421-422; vedacao ao enriquecimento sem causa, art. 884); the drawing bars the line from the overdue stub to
the rescission. Facts: TJSP, Apelacao 0001424-29.2012.8.26.0464 (15/05/2015): atraso na quitacao nao bastou, por si,
para rescindir. No number of installments is asserted: the strip runs off the left edge. Params: none.
"""
from . import svg as S

W, H = 900, 390
GROUNDS = [
    ('a', 'Boa-fé objetiva', 'Boa-fé objetiva e função social', 'arts. 421 e 422'),
    ('b', 'Função social', 'Função social e boa-fé objetiva', 'arts. 421 e 422'),
    ('c', 'Enriquecimento sem causa', 'Vedação ao enriquecimento sem causa', 'art. 884'),
]


def build(p):
    o = []
    T = S.text
    o.append(T(24, 28, 'Ajuste verbal · parcelas do financiamento bancário · sem contagem de parcelas', size=13, family=S.MONO))
    y, h, w = 70, 62, 84
    xs = [28 + i * (w + 10) for i in range(5)]
    for i, x in enumerate(xs):
        o += S.hatch(x, y, w, h, step=10, stroke=S.GRID, stroke_width=1)
        o.append(S.rect(x, y, w, h, fill='none', stroke=S.INK, stroke_width=1.8))
        o.append(T(x + w / 2, y + h / 2 + 5, 'paga', size=13, family=S.SANS, anchor='middle', fill=S.INK2))
        if i:
            o.append(S.line(x - 5, y - 6, x - 5, y + h + 6, stroke=S.INK2, stroke_width=1.2, stroke_dasharray='3 4'))
    xl = 28 + 5 * (w + 10)
    o.append(S.rect(xl, y, w, h, fill=S.PAPER, stroke=S.CONC, stroke_width=2.2, stroke_dasharray='6 4'))
    o.append(T(xl + w / 2, y + 26, 'atraso na', size=13, family=S.SANS, anchor='middle', weight='600', fill=S.CONC))
    o.append(T(xl + w / 2, y + 44, 'quitação', size=13, family=S.SANS, anchor='middle', weight='600', fill=S.CONC))
    o.append(S.line(xl - 5, y - 6, xl - 5, y + h + 6, stroke=S.INK2, stroke_width=1.2, stroke_dasharray='3 4'))
    # the line from the late stub to the rescission
    ly, rx = y + h / 2, 800
    o.append(S.line(xl + w, ly, rx - 16, ly, stroke=S.CONC, stroke_width=2))
    o.append(S.path(f'M{rx - 26},{ly - 6} L{rx - 16},{ly} L{rx - 26},{ly + 6}', fill='none', stroke=S.CONC, stroke_width=2))
    o.append(S.rect(rx - 16, ly - 20, 100, 40, fill=S.PAPER, stroke=S.INK, stroke_width=1.8))
    o.append(T(rx + 34, ly + 5, 'rescindir', size=14, family=S.SANS, weight='600', anchor='middle'))
    o.append(T(rx + 34, ly + 34, 'a avença', size=12.5, family=S.SERIF, anchor='middle', fill=S.INK2))
    # grounds
    o.append(T(450, 190, 'Fundamento que a decisão invoca', size=14, family=S.SANS, weight='600', anchor='middle', fill=S.INK2))
    bw = 270
    for i, (key, lab, _, _) in enumerate(GROUNDS):
        x = 30 + i * (bw + 15)
        o.append(f'<g data-opt="{key}" tabindex="0" role="button" aria-label="{S.esc(lab)}">')
        o.append(S.rect(x, 202, bw, 42, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
        o.append(T(x + bw / 2, 229, lab, size=14, family=S.SANS, weight='600', anchor='middle'))
        o.append('</g>')
    # answers: a bar across the line, then the holding
    bx = (xl + w + rx - 16) / 2
    for key, _, head, art in GROUNDS:
        o.append(f'<g data-ans="{key}"' + ('' if key == 'a' else ' display="none"') + '>')
        o.append(S.line(bx, ly - 22, bx, ly + 22, stroke=S.DIF, stroke_width=5))
        o.append(S.line(bx - 14, ly - 14, bx + 14, ly + 14, stroke=S.DIF, stroke_width=3))
        o.append(S.line(bx - 14, ly + 14, bx + 14, ly - 14, stroke=S.DIF, stroke_width=3))
        cx = 30 + 'abc'.index(key) * (bw + 15) + bw / 2
        o.append(S.line(cx, 244, cx, 268, stroke=S.DIF, stroke_width=2))
        o.append(S.rect(30, 268, 840, 96, fill=S.PAPER, stroke=S.DIF, stroke_width=2))
        o.append(T(54, 306, f'{head} · {art}', size=20, family=S.SANS, weight='650', fill=S.DIF))
        o.append(T(54, 340, 'O atraso na quitação não bastou, por si, para rescindir a avença.', size=16, family=S.SERIF))
        o.append('</g>')
    return S.svg(W, H, 'Atraso nas parcelas e limite à rescisão no ajuste verbal', o), []
