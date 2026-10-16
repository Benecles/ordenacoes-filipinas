"""Direito Constitucional I Aula 10 · reception as a filter at 1988, run on the lesson's own laws.

  object   a time line from 1965 to past 1988. At 1988 stands the filter the lesson names, with its two tests checked
           at the same time: (1) did the law exist on the eve? (2) is its content compatible? Each of the lesson's four
           laws runs as a lane from its year to the filter and either goes through (received: the content stays, the
           foundation becomes the new Constitution) or stops there.
  behaves  hover a lane: it thickens from its year to where it ends
  states   ink = a law's life · dotted = a law that no longer exists · ✓ / ✕ = the two tests (house badges) ·
           orange = where it stops
  facts    the 1965 law revoked in 1975, the 1970 associations law, the incompatible law (STF: revogação, ADI 2;
           Tavares: it doesn't exist; ADPF, not ADI) and the 1985 law invalid under the old order with no abstract
           ruling are all in the lesson
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from figkit import t, svg, badge

def X(y): return 70 + (y - 1965) * 26.5
XG = X(1988)                                   # the filter
Q1, Q2 = XG - 22, XG + 22                      # the two tests, side by side
LANES = [140, 222, 312, 414]


def stack(x, y, lines, anchor='start', size=9.5, lead=13, fill='var(--ink-2)', weight=500):
    return ''.join(t(x, y + k * lead, s, size, fill=fill, anchor=anchor, weight=weight) for k, s in enumerate(lines))


def figure():
    g = []
    # time axis
    g.append(f'<path d="M{X(1965)} 72H{XG + 290}" style="stroke:var(--ink-2);stroke-width:1"/>')
    for y in (1965, 1970, 1975, 1980, 1985):
        g.append(f'<path d="M{X(y)} 68V76" style="stroke:var(--ink-2);stroke-width:1"/>' + t(X(y), 60, str(y), 9.5, fill='var(--ink-2)', anchor='middle'))
    # the filter at 1988
    g.append(f'<path d="M{XG - 40} 84H{XG + 40}V{LANES[-1] + 30}H{XG - 40}Z" style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1.6"/>')
    g.append(f'<path d="M{XG} 84V{LANES[-1] + 30}" style="stroke:var(--ink);stroke-width:1;stroke-dasharray:2 3"/>')
    g.append(t(XG, 60, '1988', 11, anchor='middle', weight=600))
    g.append(t(Q1, 100, '1', 9.5, anchor='middle', weight=600) + t(Q2, 100, '2', 9.5, anchor='middle', weight=600))
    g.append(stack(XG - 46, LANES[-1] + 54, ['1 · existe juridicamente na véspera?', '2 · o conteúdo é compatível?'], anchor='start', fill='var(--ink)'))
    # lane 1: the 1965 law revoked in 1975 does not exist on the eve
    y = LANES[0]
    g.append(f'<g class="lane"><path d="M{X(1965)} {y}H{X(1975)}" style="stroke:var(--ink);stroke-width:2"/>'
             f'<path d="M{X(1975)} {y}H{Q1 - 14}" style="stroke:var(--ink-2);stroke-width:1.4;stroke-dasharray:1 5"/>'
             f'<path d="M{X(1975)} {y - 8}V{y + 8}" style="stroke:var(--ink);stroke-width:2"/></g>')
    g.append(t(X(1965), y - 12, 'lei de 1965', 10, weight=600) + t(X(1975) + 8, y + 18, 'revogada em 1975', 9.5, fill='var(--ink-2)'))
    g.append(badge(Q1, y, False, r=9))
    g.append(stack(XG + 52, y - 4, ['não volta com', 'a Constituição nova'], fill='var(--conc)'))
    # lane 2: the 1970 associations law, compatible: received
    y = LANES[1]
    g.append(f'<g class="lane"><path d="M{X(1970)} {y}H{XG + 270}" style="stroke:var(--ink);stroke-width:2"/></g>')
    g.append(t(X(1970), y - 12, 'lei de 1970 · registro de associações', 10, weight=600))
    g.append(badge(Q1, y, True, r=9) + badge(Q2, y, True, r=9))
    g.append(f'<path d="M{XG + 270} {y}l-8 -5v10z" style="fill:var(--ink)"/>')
    g.append(stack(XG + 52, y - 26, ['recebida: o conteúdo fica,', 'o fundamento passa a ser a CF/88']))
    # lane 3: a 1970 law, incompatible: it stops at the filter
    y = LANES[2]
    g.append(f'<g class="lane"><path d="M{X(1970)} {y}H{Q2 - 12}" style="stroke:var(--ink);stroke-width:2"/></g>')
    g.append(t(X(1970), y - 12, 'lei de 1970 · incompatível', 10, weight=600))
    g.append(badge(Q1, y, True, r=9) + badge(Q2, y, False, r=9))
    g.append(stack(XG + 52, y - 4, ['sai do ordenamento'], fill='var(--conc)', weight=600))
    g.append(stack(XG + 52, y + 12, ['STF (ADI 2): revogação', 'Tavares: não existe na ordem nova', 'contra ela: ADPF, não ADI']))
    # lane 4: the 1985 law, invalid under the old order, never struck in abstract review: received
    y = LANES[3]
    g.append(f'<g class="lane"><path d="M{X(1985)} {y}H{XG + 270}" style="stroke:var(--ink);stroke-width:2"/></g>')
    g.append(stack(X(1985) - 300, y - 12, ['lei de 1985 · inválida pela Constituição antiga,', 'sem decisão em controle abstrato'], fill='var(--ink)', weight=600))
    g.append(badge(Q1, y, True, r=9) + badge(Q2, y, True, r=9))
    g.append(f'<path d="M{XG + 270} {y}l-8 -5v10z" style="fill:var(--ink)"/>')
    g.append(stack(XG + 52, y - 26, ['recebida: aplicável', 'a partir de 1988']))
    return svg('0 0 1000 500', ''.join(g), label='A recepção como filtro em 1988, com as quatro leis da aula', ident='dci-a10-filtro')


def block():
    return ('<figure class="instr" id="fig-dci-a10-filtro">' + figure() +
            '<figcaption>Os dois requisitos valem ao mesmo tempo: existir na véspera e ser compatível. Quem passa conserva o '
            'conteúdo e troca de fundamento.</figcaption></figure>')


ANCHOR = ('courses/direito-constitucional-i/aula-10.html', 'A recepção tem dois requisitos, ambos exigidos ao mesmo tempo:', '</ol>')
