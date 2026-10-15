"""Controle Aula 10 · Fig. 1: preventive and repressive control told by position on one law's life, not by
colour. The axis runs projeto → publicação → vacatio legis → vigência; the publication mark divides the
legislative process (left, preventive) from the existence of the act (right, repressive). The page's two
sentences that explained the old colours are rewritten to name the sides instead.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a16 import say

XA, XP, XV, XB, Y = 40, 300, 400, 560, 170


def axis(emph=False, vacatio=False):
    o = f'<rect x="{XA}" y="{Y - 26}" width="{XP - XA}" height="52" style="fill:var(--paper-2);stroke:none"/>'
    o += f'<rect x="{XP}" y="{Y - 26}" width="{XB - XP}" height="52" style="fill:none;stroke:var(--ink);stroke-width:1.2"/>'
    o += f'<line x1="{XA}" y1="{Y}" x2="{XB}" y2="{Y}" style="stroke:var(--ink);stroke-width:1.6"/>'
    for x, s in ((70, 'projeto'), (150, 'votação'), (230, 'sanção')):
        o += f'<line x1="{x}" y1="{Y - 6}" x2="{x}" y2="{Y + 6}" style="stroke:var(--ink);stroke-width:1.2"/>' + t(x, Y + 46, s, size=10, anchor='middle', fill='var(--ink-2)')
    o += f'<line x1="{XP}" y1="{Y - 60}" x2="{XP}" y2="{Y + 34}" style="stroke:var(--ink);stroke-width:{4 if emph else 2.5}"/>'
    o += t(XP, Y - 70, 'publicação no diário oficial', size=10.5, anchor='middle', weight=700, caps=True)
    o += t((XA + XP) / 2, Y - 34, 'processo legislativo · preventivo', size=10, anchor='middle', caps=True)
    o += t((XP + XB) / 2, Y - 34, 'o ato existe · repressivo', size=10, anchor='middle', caps=True)
    if vacatio:
        o += f'<path d="M{XP + 4} {Y + 14} V{Y + 22} H{XV} V{Y + 14}" style="fill:none;stroke:var(--conc);stroke-width:1.8"/>'
        o += t((XP + XV) / 2, Y + 46, 'vacatio legis', size=10, anchor='middle', caps=True, fill='var(--conc)')
        o += f'<line x1="{XV}" y1="{Y - 6}" x2="{XV}" y2="{Y + 6}" style="stroke:var(--ink);stroke-width:1.2"/>' + t(XV + 8, Y + 62, 'vigência', size=10, fill='var(--ink-2)')
    return o


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def defs():
    o = head('Preventivo × repressivo') + axis()
    o += say(40, 300, 'Preventivo: durante o processo legislativo,')
    o += say(40, 324, 'antes da publicação.', 16, 'var(--ink-2)')
    o += say(40, 368, 'Repressivo: a partir da publicação, durante toda')
    o += say(40, 392, 'a existência da lei.', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p10-defs',
               label='A vida de uma lei num eixo: à esquerda da publicação, o processo legislativo e o controle preventivo; à direita, a lei existente e o controle repressivo')


def linha():
    o = head('A publicação divide o eixo') + axis(emph=True)
    o += say(40, 310, 'O marco é a publicação, não o início da vigência.')
    o += say(40, 354, 'Daí em diante, a lei pode ser examinada', 16, 'var(--ink-2)', True)
    o += say(40, 378, 'durante toda a sua existência.', 16, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p10-linha',
               label='O mesmo eixo com a publicação destacada: ela separa o controle preventivo do repressivo')


def vacatio():
    o = head('Vacatio legis já é repressivo') + axis(vacatio=True)
    o += say(40, 320, 'Publicada, mas ainda sem obrigar: a lei já existe.')
    o += say(40, 344, 'O controle nesse intervalo é repressivo.', 16, 'var(--ink-2)')
    o += say(40, 388, 'A vigência é outro marco, posterior e distinto.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p10-vacatio',
               label='Logo depois da publicação, o intervalo da vacatio legis, à direita do marco: a lei já existe e o controle é repressivo; a vigência vem depois')


TEXT = [
    ('Continuando a Aula 09: <em class="dif">azul</em> ainda marca o <em class="dif">preventivo</em>, <em class="conc">vermelho</em> ainda marca o <em class="conc">repressivo</em>.',
     'Continuando a Aula 09: à esquerda da publicação, o <em>preventivo</em>; à direita, o <em>repressivo</em>.'),
    ('já se enquadra no lado vermelho do eixo.', 'já fica à direita da publicação, no lado repressivo do eixo.'),
]


def panels():
    return [defs(), linha(), vacatio()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    path = 'courses/controle-de-constitucionalidade/aula-10.html'
    n = inject(path, {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    p = os.path.join(os.path.dirname(__file__), '..', '..', path)
    h = open(p).read()
    for a, b in TEXT:
        if a not in h and b not in h:
            raise SystemExit(f'text not found: {a[:50]}')
        h = h.replace(a, b)
    open(p, 'w').write(h)
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
