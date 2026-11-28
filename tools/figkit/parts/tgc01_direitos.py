"""Aula 01, ch.5: the basic rights of CDC art. 6 as a ruler the reader reads by situation (instrumento).

Eleven incisos stand on a ruler in statutory order (V and IX are not drawn: V is outside the quoted block, IX was
vetoed). The reader picks a situation; the ruler lights the inciso(s) that answer it and the drawing says what the
text asks. Facts only from CDC art. 6 as quoted in the chapter: I, III, IV, VI, VII, VIII, XI, XII; lei 14.181/2021
added XI-XIII; VIII needs a judge's decision (verossimilhanca da alegacao ou hipossuficiencia). Params: none.
"""
from . import svg as S
from .tgc01_hand import hit as hitbox

W, H = 1080, 420
RULER = ['I', 'II', 'III', 'IV', 'VI', 'VII', 'VIII', 'X', 'XI', 'XII', 'XIII']
CHOICES = [
    ('a', ['Produto perigoso', 'vendido sem aviso do risco']),
    ('b', ['Publicidade enganosa', 'ou cláusula abusiva']),
    ('c', ['Dano sofrido', 'e porta do juízo']),
    ('d', ['Consumidor pede a', 'inversão do ônus da prova']),
    ('e', ['Dívidas que ameaçam', 'o mínimo existencial']),
]
ANS = {
    'a': (['I', 'III'], 'art. 6º, I e III',
          ['Protege a vida, a saúde e a segurança contra riscos de práticas no fornecimento de produtos perigosos ou nocivos,',
           'e exige informação adequada e clara sobre os riscos que o produto apresenta.']),
    'b': (['IV'], 'art. 6º, IV',
          ['Protege contra a publicidade enganosa e abusiva, os métodos comerciais coercitivos ou desleais',
           'e as práticas e cláusulas abusivas ou impostas no fornecimento.']),
    'c': (['VI', 'VII'], 'art. 6º, VI e VII',
          ['Garante a prevenção e a reparação de danos patrimoniais e morais, individuais, coletivos e difusos,',
           'e o acesso aos órgãos judiciários e administrativos, com proteção aos necessitados.']),
    'd': (['VIII'], 'art. 6º, VIII',
          ['Facilita a defesa do consumidor, mas a inversão depende de decisão do juiz:',
           'alegação verossímil ou hipossuficiência, segundo as regras ordinárias de experiência.']),
    'e': (['XI', 'XII'], 'art. 6º, XI e XII (Lei 14.181/2021)',
          ['Garante crédito responsável, educação financeira e tratamento do superendividamento,',
           'com preservação do mínimo existencial na repactuação de dívidas e na concessão de crédito.']),
}


def build(p):
    o = []
    T = S.text
    o.append(T(24, 28, 'Art. 6º do CDC · direitos básicos em ordem legal', size=13, family=S.MONO))
    # situations
    cw, gap, x0 = 200, 20, 10
    for i, (key, lab) in enumerate(CHOICES):
        x = x0 + i * (cw + gap)
        cx = x + cw / 2
        o.append(f'<g data-opt="{key}" tabindex="0" role="button" aria-label="{S.esc(" ".join(lab))}">')
        o.append(hitbox(x, 44, cw, 70))
        o.append(S.line(x + 10, 108, x + cw - 10, 108, stroke=S.INK2, stroke_width=1))
        o.append(T(cx, 76, lab[0], size=13.5, family=S.SANS, weight='600', anchor='middle'))
        o.append(T(cx, 95, lab[1], size=13.5, family=S.SANS, weight='600', anchor='middle'))
        o.append('</g>')
    # ruler
    ry = 196
    xs = {n: 70 + i * 94 for i, n in enumerate(RULER)}
    o.append(S.line(40, ry, 1040, ry, stroke=S.INK, stroke_width=2))
    for n, x in xs.items():
        o.append(S.circle(x, ry, 6, fill=S.PAPER, stroke=S.INK, stroke_width=1.8))
        o.append(T(x, ry - 22, n, size=14, family=S.MONO, anchor='middle', fill=S.INK2))
    o.append(T(70, ry + 38, 'vida, informação, proteção', size=12.5, family=S.SERIF, fill=S.MUTED))
    o.append(T(70 + 6 * 94, ry + 38, 'prova', size=12.5, family=S.SERIF, fill=S.MUTED, anchor='middle'))
    o.append(T(70 + 9 * 94, ry + 38, 'Lei 14.181/2021', size=12.5, family=S.SERIF, fill=S.MUTED, anchor='middle'))
    # answers
    for key, _ in CHOICES:
        marks, head, lines = ANS[key]
        o.append(f'<g data-ans="{key}"' + ('' if key == 'a' else ' display="none"') + '>')
        for n in marks:
            x = xs[n]
            o.append(S.circle(x, ry, 6.5, fill=S.DIF, stroke=S.DIF, stroke_width=1.8))
            o.append(S.line(x, ry + 10, x, 268, stroke=S.DIF, stroke_width=2))
        xa, xb = xs[marks[0]], xs[marks[-1]]
        o.append(S.line(xa, 268, xb, 268, stroke=S.DIF, stroke_width=2))
        o.append(S.line(40, 290, 40, 400, stroke=S.DIF, stroke_width=2))
        o.append(T(64, 316, head, size=22, family=S.SANS, weight='650', fill=S.DIF))
        for j, ln in enumerate(lines):
            o.append(T(64, 354 + j * 28, ln, size=16, family=S.SERIF))
        o.append('</g>')
    return S.svg(W, H, p.get('title', 'Direitos básicos do art. 6º do CDC por situação'), o), []
