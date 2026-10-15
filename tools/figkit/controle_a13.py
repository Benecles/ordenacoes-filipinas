"""Controle Aula 13 · estado de coisas inconstitucional. One timeline to scale (1997 → 2025) that grows across
the steps: Colombia's origin, ADPF 347 (09/09/2015), its extensions, and the 2022 environmental decisions that
use the logic without the label. The test is a form with three boxes; all three must be ticked.
Blue = what the STF declared; orange = the limit (a box left empty, the risk); dashed = the logic without the label.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t

Y0, Y1, XA, XB = 1995, 2025, 50, 550


def X(y):
    return XA + (XB - XA) * (y - Y0) / (Y1 - Y0)


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def say(x, y, s, size=16, fill='var(--ink)', italic=False):
    return f'<text x="{x}" y="{y}" style="font-family:var(--serif,serif);font-size:{size}px;fill:{fill}{";font-style:italic" if italic else ""}">{s}</text>'


def axis(y=300):
    o = f'<line x1="{XA}" y1="{y}" x2="{XB}" y2="{y}" style="stroke:var(--ink);stroke-width:1.6"/>'
    for yr in range(1995, 2026, 5):
        o += f'<line x1="{X(yr):.1f}" y1="{y - 5}" x2="{X(yr):.1f}" y2="{y + 5}" style="stroke:var(--ink);stroke-width:1"/>'
        o += t(X(yr), y + 22, str(yr), size=10, anchor='middle', fill='var(--ink-2)')
    return o


def event(yr, label, sub='', up=1, tone='var(--ink)', dashed=False, lane=0, y=300):
    x = X(yr); top = y - 40 - lane * 52
    o = f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{top + 6}" style="stroke:{tone};stroke-width:1.3{";stroke-dasharray:3 4" if dashed else ""}"/>'
    o += f'<circle cx="{x:.1f}" cy="{y}" r="5" style="fill:{"none" if dashed else tone};stroke:{tone};stroke-width:1.5"/>'
    anchor = 'end' if x > 380 else 'start'
    dx = -6 if anchor == 'end' else 6
    o += t(x + dx, top, label, size=11, weight=700, caps=True, anchor=anchor, fill=tone)
    if sub:
        o += t(x + dx, top + 15, sub, size=10, anchor=anchor, fill='var(--ink-2)')
    return o


def origem():
    o = head('De onde vem o instituto') + axis()
    o += event(1997, 'Colômbia', 'Corte Constitucional')
    o += event(2015.69, 'ADPF 347 · cautelar', '09/09/2015 · Min. Marco Aurélio', tone='var(--dif)', lane=1)
    o += say(40, 400, 'O STF declara o estado de coisas inconstitucional')
    o += say(40, 424, 'do sistema prisional.')
    o += say(40, 468, 'Objeto: violações de direitos dos presos.', 16, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-origem',
               label='Linha do tempo em escala: a Corte Constitucional da Colômbia em 1997 e a cautelar da ADPF 347 em 9 de setembro de 2015')


def pressupostos():
    o = head('Teste cumulativo')
    o += '<path d="M40 70H546L560 84V330H40Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    items = ['Violação massiva e generalizada de direitos', 'Falhas estruturais e políticas públicas falidas', 'Omissão prolongada das autoridades']
    for i, s in enumerate(items):
        y = 120 + i * 62
        o += f'<rect x="64" y="{y - 18}" width="24" height="24" style="fill:none;stroke:var(--ink);stroke-width:1.5"/>'
        o += f'<path d="M69 {y - 6} l6 7 l12 -16" style="fill:none;stroke:var(--ink);stroke-width:2.4"/>'
        o += say(104, y, s, 16)
    o += '<g transform="rotate(-5 300 300)"><rect x="196" y="280" width="208" height="34" rx="3" style="fill:none;stroke:var(--dif);stroke-width:2.2"/>'
    o += t(300, 303, 'ECI configurado', size=14, anchor='middle', weight=700, caps=True, ls='.14em', fill='var(--dif)') + '</g>'
    o += say(40, 400, 'Os três, ao mesmo tempo.')
    o += say(40, 444, 'Uma caixa vazia, e não há ECI.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-pressupostos',
               label='Um formulário com três caixas marcadas: violação massiva, falhas estruturais e omissão prolongada; só com as três o carimbo diz ECI configurado')


def consequencia():
    o = head('Depois do reconhecimento')
    cols = [('Normativas', ['corrigir ou', 'criar normas']), ('Administrativas', ['corrigir ou', 'criar políticas']), ('Orçamentárias', ['alocar', 'recursos'])]
    for i, (h, s) in enumerate(cols):
        x = 40 + i * 176
        o += f'<rect x="{x}" y="90" width="160" height="150" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.3"/>'
        o += t(x + 12, 116, h, size=11, weight=700, caps=True)
        o += ''.join(say(x + 12, 146 + k * 20, ln, 15) for k, ln in enumerate(s))
    o += say(40, 300, 'Medidas complexas e abrangentes, de vários')
    o += say(40, 324, 'órgãos ao mesmo tempo.')
    o += say(40, 380, 'O risco: congestionar o Judiciário.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-consequencia',
               label='Três frentes de medidas depois do reconhecimento do ECI: normativas, administrativas e orçamentárias; o risco é congestionar o Judiciário')


def socioed():
    o = head('A ADPF 347 se estende') + axis()
    o += event(1997, 'Colômbia', '', tone='var(--ink-2)')
    o += event(2015.69, 'ADPF 347', 'sistema prisional', tone='var(--dif)')
    o += event(2022.3, 'ADPF 976/DF', 'população em situação de rua', tone='var(--dif)', lane=1)
    o += say(40, 400, 'Depois: habeas corpus coletivos levam a lógica')
    o += say(40, 424, 'ao socioeducativo (Ceará, Espírito Santo).')
    o += say(40, 468, 'Superlotação em unidades para adolescentes.', 16, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-socioed',
               label='A mesma linha do tempo cresce: a ADPF 347 em 2015 e a ADPF 976 em 2022, sobre a população em situação de rua')


def ambiental():
    o = head('A mesma lógica, sem o rótulo') + axis()
    o += event(2015.69, 'ADPF 347', '', tone='var(--dif)')
    o += event(2022.4, 'ADPF 708', 'Fundo Clima', dashed=True, lane=0)
    o += event(2022.4, 'ADPF 651', 'Fundo Amazônia', dashed=True, lane=1)
    o += event(2022.4, 'ADPF 760 + ADO 54', 'desmatamento', dashed=True, lane=2)
    o += say(40, 400, 'Em 2022, decisões ambientais estruturais tratam')
    o += say(40, 424, 'a omissão sistêmica como no ECI,')
    o += say(40, 448, 'sem declará-lo expressamente.', 16, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-ambiental',
               label='Em 2022, ADPF 708, ADPF 651 e ADPF 760 com ADO 54, tracejadas: decisões que seguem a lógica do ECI sem declará-lo')


def panels():
    return [origem(), pressupostos(), consequencia(), socioed(), ambiental()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-13.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
