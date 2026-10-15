"""Controle Aula 17 · ato interposto. The defect sits in how an act is used, not in its text: the act's sheet
passes every formal check (ticked), yet its use opens a second route to an effect the Constitution forbids.
Drawn as the act on paper plus a route map: the direct route blocked (orange bar), the detour through the
act (dashed) reaching the forbidden effect.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a16 import say
from controle_a20 import tick


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def cadeia():
    o = head('O ato serve de instrumento')
    o += '<path d="M40 70H306L320 84V230H40Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    o += t(56, 98, 'Ato · aparentemente válido', size=10.5, weight=700, caps=True)
    o += tick(56, 140) + say(90, 140, 'competência', 15) + tick(56, 180) + say(90, 180, 'procedimento', 15)
    o += '<path d="M330 150 H400" style="stroke:var(--ink);stroke-width:1.4;stroke-dasharray:5 4"/><path d="M394 145 l7 5 l-7 5" style="fill:none;stroke:var(--ink);stroke-width:1.4"/>'
    o += '<rect x="410" y="110" width="150" height="80" style="fill:none;stroke:var(--conc);stroke-width:2"/>'
    o += t(424, 140, 'efeito vedado', size=10.5, weight=700, caps=True, fill='var(--conc)') + say(424, 168, 'pela Constituição', 14, 'var(--ink-2)')
    o += say(40, 290, 'O texto passa em todos os testes de forma;')
    o += say(40, 314, 'o vício está no uso: o ato viabiliza o que,')
    o += say(40, 338, 'por si só, seria inconstitucional.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-cadeia',
               label='Um ato com competência e procedimento marcados como válidos, cujo uso leva, tracejado, a um efeito vedado pela Constituição')


def contorno():
    o = head('Duas rotas até o efeito')
    o += '<circle cx="80" cy="200" r="12" style="fill:var(--ink)"/>' + t(80, 236, 'quem age', size=10, anchor='middle', caps=True)
    o += '<rect x="470" y="180" width="90" height="40" style="fill:none;stroke:var(--conc);stroke-width:2"/>' + t(515, 205, 'efeito', size=10.5, anchor='middle', caps=True, fill='var(--conc)')
    o += '<path d="M96 200 H260" style="stroke:var(--ink);stroke-width:2"/>'
    o += '<rect x="262" y="176" width="10" height="48" style="fill:var(--conc)"/>' + t(267, 166, 'rota direta bloqueada', size=10, anchor='middle', caps=True, fill='var(--conc)')
    o += '<path d="M90 186 C 160 80, 360 80, 468 188" style="fill:none;stroke:var(--ink);stroke-width:1.6;stroke-dasharray:6 5"/>'
    o += '<rect x="226" y="88" width="88" height="32" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>' + t(270, 109, 'o ato', size=10.5, anchor='middle', weight=700, caps=True)
    o += say(40, 320, 'A análise segue o contexto e o efeito: é preciso')
    o += say(40, 344, 'mostrar que o uso do ato conduziu ao resultado vedado.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-contorno',
               label='Um mapa com duas rotas até o efeito vedado: a direta, bloqueada; a indireta, tracejada, passando pelo ato interposto')


def panels():
    return [cadeia(), contorno()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-17.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
