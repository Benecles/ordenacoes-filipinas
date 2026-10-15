"""Teoria do Delito · Unidade 07 (imputação objetiva), Fig. 2: Roxin's three filters as one form answered for
the unit's own paired cases (8.1, the lightning; 8.2, the braking). Same conduct, A at 100 km/h where the limit
is 60; the rows fill one step per panel; the last panel stamps each column. This is the exemplar for the
Delito figure spec (work/design/specs/delito-figures.md): a box tree becomes a form with real facts.
Blue = imputed (what the analysis decides); orange = the limit where imputation stops.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a16 import say
from controle_a09 import stamp

ROWS = [('1 · Criar', 'risco proibido? (ex ante)', ('sim', 'sim')),
        ('2 · Realizar', 'o risco aparece no resultado? (ex post)', ('não', 'sim')),
        ('3 · Alcance', 'o tipo protege contra este resultado?', ('—', 'sim'))]
XA, XB = 330, 470


def mark(x, y, v):
    if v == 'sim':
        return (f'<rect x="{x - 11}" y="{y - 15}" width="22" height="22" style="fill:none;stroke:var(--ink);stroke-width:1.4"/>'
                f'<path d="M{x - 7} {y - 5} l5 6 l11 -15" style="fill:none;stroke:var(--ink);stroke-width:2.2"/>')
    if v == 'não':
        return (f'<rect x="{x - 11}" y="{y - 15}" width="22" height="22" style="fill:none;stroke:var(--conc);stroke-width:1.6"/>'
                f'<path d="M{x - 6} {y - 10} l12 12 m0 -12 l-12 12" style="stroke:var(--conc);stroke-width:2"/>')
    return t(x, y, '—', size=14, anchor='middle', fill='var(--ink-2)')


def panel(k):
    o = t(40, 40, 'Roxin · três filtros, dois casos', size=11.5, weight=700, caps=True, ls='.12em')
    o += say(40, 74, 'A dirige a 100 km/h onde o limite é 60. B morre.', 15)
    o += t(XA, 116, '8.1 · raio', size=11, anchor='middle', weight=700, caps=True) + t(XB, 116, '8.2 · frenagem', size=11, anchor='middle', weight=700, caps=True)
    o += say(XA, 136, 'árvore cai sobre B', 13, 'var(--ink-2)', True).replace('<text ', '<text text-anchor="middle" ', 1)
    o += say(XB, 136, 'não freia a tempo', 13, 'var(--ink-2)', True).replace('<text ', '<text text-anchor="middle" ', 1)
    o += '<line x1="40" y1="150" x2="560" y2="150" style="stroke:var(--ink);stroke-width:1.4"/>'
    for i, (name, q, (a, b)) in enumerate(ROWS):
        y = 196 + i * 64
        on = i <= k
        o += t(40, y - 6, name, size=11, weight=700, caps=True, fill='var(--ink)' if on else 'var(--ink-2)')
        o += say(40, y + 14, q, 13, 'var(--ink-2)')
        if on:
            o += mark(XA, y, a) + mark(XB, y, b)
        o += f'<line x1="40" y1="{y + 30}" x2="560" y2="{y + 30}" style="stroke:var(--ink-2);stroke-width:.6"/>'
    if k == 2:
        o += stamp(XA, 430, 'não imputa', 'var(--conc)') + stamp(XB, 430, 'imputa', 'var(--dif)')
        o += say(40, 500, 'A mesma violação do cuidado; só em 8.2 o risco', 15)
        o += say(40, 522, 'da velocidade se realiza no resultado.', 15)
    else:
        o += say(40, 470, 'Nexo físico nos dois casos; os filtros são normativos.', 15, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig' + (' on' if k == 0 else ''), ident=f'p-risk-{k}',
               label=f'Formulário dos três filtros de Roxin para dois casos de excesso de velocidade, até o filtro {k + 1}: no caso do raio o risco não se realiza; no da frenagem, sim')


def panels():
    return [panel(k) for k in range(3)]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/teoria-do-delito/unidade-07-imputacao.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
