"""Controle Aula 18 · mutação constitucional and backlash. Mutação uses the frame family of Aula 15: the same
fixed text, its reading in 1988 and today as slips inside the frame of possible sense; a reading outside the
frame needs an amendment. Backlash is two parallel tracks (the STF's decision, society's reaction) with no
line between them: the reaction says nothing about whether the decision was right.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a16 import say
from controle_a15 import frame, slip


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def text_fixed(y=70):
    o = f'<path d="M40 {y}H546L560 {y + 14}V{y + 54}H40Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    o += t(54, y + 22, 'Texto constitucional · intocado', size=10.5, caps=True, fill='var(--ink-2)')
    o += say(54, y + 44, 'A letra fica a mesma.', 15)
    return o


def mutacao1():
    o = head('Muda o sentido, não o texto') + text_fixed() + frame()
    o += slip(56, 200, 'Leitura de 1988', 'o sentido de então', 'keep', w=220)
    o += slip(316, 200, 'Leitura de hoje', 'o mesmo texto, relido', 'keep', w=220)
    o += f'<path d="M282 229 H310" style="stroke:var(--ink);stroke-width:1.4"/><path d="M304 224 l6 5 l-6 5" style="fill:none;stroke:var(--ink);stroke-width:1.4"/>'
    o += say(40, 430, 'A norma “muta-se” pela interpretação, dentro do texto.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-mutacao1',
               label='O mesmo texto constitucional, intocado, com a leitura de 1988 e a de hoje dentro da moldura do sentido possível')


def mutacao2():
    o = head('Por que a norma se muta') + text_fixed() + frame()
    o += slip(56, 200, 'Leitura de hoje', 'abrange o novo', 'keep', w=220)
    o += t(316, 222, 'realidades novas', size=10.5, caps=True, fill='var(--ink-2)') + say(316, 246, 'inimagináveis em 1988', 14, 'var(--ink-2)', True)
    o += say(40, 430, 'Para abranger o que não se imaginava; o texto fica.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-mutacao2', label='A leitura de hoje alcança realidades novas, inimagináveis em 1988, sem tocar o texto')


def helice1():
    o = head('A Constituição aberta ao tempo') + text_fixed() + frame()
    for i, y in enumerate([1988, 'depois', 'depois', 'hoje']):
        o += slip(56 + i * 124, 220, str(y), 'leitura', 'keep', w=110)
    o += say(40, 430, 'Relida a cada tempo, conserva a força normativa.', 16, 'var(--dif)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-helice1', label='Quatro leituras sucessivas do mesmo texto dentro da moldura: a Constituição aberta ao tempo')


def helice2():
    o = head('O limite da mutação') + text_fixed() + frame(x1=420)
    o += slip(56, 200, 'Leitura', 'cabe no texto', 'keep', w=160) + slip(236, 200, 'Leitura', 'cabe no sistema', 'keep', w=160)
    o += slip(436, 200, 'Leitura', 'contra o texto', 'outside', w=124)
    o += t(432, 300, 'só por emenda', size=10, caps=True, fill='var(--conc)')
    o += say(40, 430, 'Limites semânticos, sistemáticos e institucionais.')
    o += say(40, 458, 'Além deles, a via é a alteração formal (art. 60).', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-helice2',
               label='A moldura do sentido possível: leituras dentro dela são mutação; uma leitura contra o texto fica fora e exige emenda')


def backlash():
    o = head('Backlash · reação, não veredito')
    for y, name in ((130, 'STF · decisão interpretativa'), (250, 'Sociedade · reação')):
        o += t(60, y - 12, name, size=10.5, caps=True, fill='var(--ink-2)')
        o += f'<line x1="60" y1="{y + 10}" x2="540" y2="{y + 10}" style="stroke:var(--ink);stroke-width:1.4"/>'
    o += '<rect x="200" y="128" width="80" height="24" style="fill:var(--dif)"/>' + t(240, 145, 'decide', size=10, anchor='middle', weight=700, caps=True, fill='var(--paper)')
    o += ''.join(f'<line x1="{300 + k * 10}" y1="{246}" x2="{300 + k * 10}" y2="{274}" style="stroke:var(--ink);stroke-width:2.4"/>' for k in range(4))
    o += t(300, 300, 'reação contrária', size=10, caps=True)
    o += say(40, 380, 'Duas linhas, sem traço entre elas: a reação')
    o += say(40, 404, 'não diz se a decisão acertou ou errou.')
    o += say(40, 448, 'Ex.: uniões homoafetivas; transfobia como racismo.', 15, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-backlash',
               label='Duas linhas paralelas no tempo, a decisão do STF e a reação da sociedade, sem ligação entre elas')


def panels():
    return [mutacao1(), mutacao2(), helice1(), helice2(), backlash()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-18.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
