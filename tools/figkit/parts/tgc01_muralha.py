"""Aula01, ch.2: plan of the wall that Roman law set around enforceable agreement, and what became of it.

No params. Gates counted from Gaio (four sources), the consensuais named in Pereira III pp. 9-10 and Venosa p. 3;
the breaches are the medieval canonists and mercantile customs (Pereira p. 18); the stubs are the contratos
formais and reais that survive the 1804 code (Pereira p. 10; Venosa p. 4). Width of the openings carries the
meaning (how much form the law asks), not a scale; no dates are plotted beyond the labelled ones.
"""
from . import svg as S


def build(p):
    o = []
    T = S.text
    W, H = 870, 370
    wy, wt = 172, 24  # wall band top and thickness
    seg = [(40, 330), (330, 590), (590, 830)]
    # the territory of the enforceable obligation
    for a, b in seg:
        o.append(S.path(f'M{a + 6},46 V40 H{b - 6} V46', fill='none', stroke=S.INK2, stroke_width=1))
    o.append(T(48, 30, 'obrigação exigível', size=14, family=S.SANS, weight='600'))
    for x in (330, 590):
        o.append(S.line(x, 40, x, 330, stroke=S.INK2, stroke_width=1))

    def wall(a, b):
        o.append(S.line(a, wy + wt / 2, b, wy + wt / 2, stroke=S.INK, stroke_width=6, stroke_linecap='butt'))

    def thread(x, color=S.DIF):
        o.append(S.line(x, 254, x, 150, stroke=color, stroke_width=2.4))
        o.append(S.circle(x, 144, 6, fill=S.PAPER, stroke=color, stroke_width=2))

    def dot(x, color=S.INK):
        o.append(S.circle(x, 262, 7, fill=S.PAPER, stroke=color, stroke_width=2))

    # Rome: a continuous wall with four gates
    gates = [75, 145, 215, 285]
    names = ['verbis', 'litteris', 're', 'consensu']
    edges = [40] + [g + t for g in gates for t in (-13, 13)] + [330]
    for i in range(0, len(edges), 2):
        wall(edges[i], edges[i + 1])
    for g, n in zip(gates, names):
        o.append(T(g, 126, n, size=13, family=S.SANS, anchor='middle', weight='600'))
        thread(g)
        dot(g)
    for x in (110, 250):
        dot(x)
    o.append(T(110, 290, 'pacto simples', size=12.5, anchor='middle', fill=S.INK2))
    o.append(T(48, 62, 'stipulatio: forma que dá força', size=12.5, fill=S.INK2))
    o.append(T(48, 80, 'só quatro consensuais: venda,', size=12.5, fill=S.INK2))
    o.append(T(48, 98, 'locação, mandato, sociedade', size=12.5, fill=S.INK2))
    # Middle ages: breaches
    for a, b in ((330, 378), (428, 472), (522, 563)):
        wall(a, b)
    for x in (403, 497, 578):
        thread(x)
        dot(x)
    for x in (352, 450, 543):
        dot(x)
    o.append(T(338, 62, 'canonistas: faltar à palavra', size=12.5, fill=S.INK2))
    o.append(T(338, 80, 'é pecado; costumes mercantis', size=12.5, fill=S.INK2))
    o.append(T(338, 98, 'e direito natural: consenso', size=12.5, fill=S.INK2))
    # Codes: two stubs only
    stubs = [(630, 'formais'), (770, 'reais')]
    for x, n in stubs:
        wall(x - 13, x + 13)
        dot(x, S.CONC)
        o.append(T(x, 126, n, size=13, family=S.SANS, anchor='middle', weight='600', fill=S.INK))
    for x in (610, 690, 720, 810):
        thread(x)
        dot(x)
    o.append(T(598, 62, 'Código francês de 1804:', size=12.5, fill=S.INK2))
    o.append(T(598, 80, 'consentir basta; restam', size=12.5, fill=S.INK2))
    o.append(T(598, 98, 'os de forma e de entrega', size=12.5, fill=S.INK2))
    for (a, b), n in zip(seg, ('Direito Romano', 'Idade Média', 'Códigos modernos')):
        o.append(S.line(a + 6, 318, b - 6, 318, stroke=S.INK, stroke_width=1.4))
        o.append(T((a + b) / 2, 340, n, size=14, family=S.SANS, anchor='middle', weight='600'))
    return S.svg(W, H, 'Planta de um muro: as portas do contrato romano, as brechas medievais, os restos dos códigos', o), []
