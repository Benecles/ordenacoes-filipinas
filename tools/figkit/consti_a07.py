"""Direito Constitucional I Aula 07 · José Afonso da Silva's three classes as plumbing.

  object   three pipes leaving one tank (the CF/88, in force since 1988). Plena: an open pipe, full flow, no fitting a
           law can reach. Contida: an open pipe, full flow, and a valve on it that a restrictive law can turn (the
           flow stays full while no law has turned it). Limitada: a pipe with its middle section missing (the
           integrating law); until it's fitted only a drip comes through, the minimum effect every norm has: it
           invalidates the contrary law.
  behaves  hover the valve: its wheel turns and the contida flow narrows (the law restricts); hover the missing
           section: the integrating law fits, the pipe goes solid, and the limitada flow starts
  states   solid pipe = in force · dotted outline = the section a law must supply · orange = the limit (the
           restrictive valve) · flow = ink lines leaving the pipe mouth; a dashed narrower flow = what the law may cut
  facts    all from the lesson: classes and definitions (Silva via Tavares), art. 5º, XII (contida), art. 18, § 3º
           (limitada, institutiva), the minimum effect of invalidating contrary law (Tavares)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from figkit import t, line, svg

TX0, TX1 = 172, 230         # the tank
X0, X1 = 248, 690            # pipe from the tank to its mouth
XR = 806                     # right-hand labels
VX = 518                     # the restrictive valve
GA, GB = 420, 556            # the missing section
R = 9                        # pipe half-thickness
ROWS = [(118, 'PLENA'), (236, 'CONTIDA'), (354, 'LIMITADA')]


def pipe(y, xa, xb, dotted=False):
    st = 'fill:none;stroke:var(--ink);stroke-width:1.6' + (';stroke-dasharray:2 4' if dotted else '')
    return (f'<path d="M{xa} {y - R}H{xb}M{xa} {y + R}H{xb}" style="{st}"/>'
            + ('' if dotted else f'<path d="M{xa} {y - R + 3}H{xb}" style="fill:none;stroke:var(--ink-2);stroke-width:.6;opacity:.6"/>'))


def flow(y, x, n=3, spread=7, dash=None, length=96):
    """water leaving the pipe mouth: gently waving lines"""
    out = ''
    for k in range(n):
        dy = (k - (n - 1) / 2) * spread
        st = 'fill:none;stroke:var(--ink);stroke-width:1.3;stroke-linecap:round' + (f';stroke-dasharray:{dash}' if dash else '')
        out += (f'<path d="M{x} {y + dy:.1f}c{length * .25:.0f} -5 {length * .5:.0f} 5 {length * .75:.0f} 0'
                f's{length * .2:.0f} 4 {length * .25:.0f} 2" style="{st}"/>')
    return out


def valve(x, y):
    """a gate valve on the pipe, its wheel on a stem: the restrictive law's handle (orange: the limit)"""
    return (f'<path d="M{x - 14} {y - 13}L{x + 14} {y + 13}V{y - 13}L{x - 14} {y + 13}Z" style="fill:var(--paper);stroke:var(--conc);stroke-width:1.8;stroke-linejoin:round"/>'
            f'<path d="M{x} {y - 13}V{y - 34}" style="stroke:var(--conc);stroke-width:1.8"/>'
            f'<ellipse cx="{x}" cy="{y - 38}" rx="15" ry="4.5" style="fill:none;stroke:var(--conc);stroke-width:1.8"/>')


def figure():
    g = []
    # the tank: the Constitution, in force since 1988
    g.append(f'<path d="M{TX0} 70H{TX1}V402H{TX0}Z" style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1.8"/>')
    g.append(t((TX0 + TX1) / 2, 60, 'CF/88', 11, anchor='middle', weight=600))
    g.append(t((TX0 + TX1) / 2, 420, 'em vigor', 9.5, fill='var(--ink-2)', anchor='middle'))
    for y, name in ROWS:
        g.append(f'<path d="M{TX1} {y - R}H{X0}M{TX1} {y + R}H{X0}" style="stroke:var(--ink);stroke-width:1.6"/>')
        g.append(t(28, y - 2, name, 11.5, weight=600))
    # plena: open pipe, full flow
    y = ROWS[0][0]
    g.append(pipe(y, X0, X1) + f'<path d="M{X1} {y - R - 4}V{y + R + 4}" style="stroke:var(--ink);stroke-width:2.4"/>' + flow(y, X1 + 4))
    g.append(t(28, y + 14, 'não depende de lei', 9.5, fill='var(--ink-2)'))
    g.append(t(XR, y - 4, 'efeitos principais', 10.5, weight=600))
    g.append(t(XR, y + 11, 'desde a vigência', 9.5, fill='var(--ink-2)'))
    # contida: open pipe, full flow, a valve the restrictive law may turn
    y = ROWS[1][0]
    g.append(pipe(y, X0, X1) + f'<path d="M{X1} {y - R - 4}V{y + R + 4}" style="stroke:var(--ink);stroke-width:2.4"/>'
             + f'<g class="fl-c" style="transform-origin:{X1}px {y}px">{flow(y, X1 + 4)}</g>')
    g.append(f'<g class="valve"><rect x="{VX - 22}" y="{y - 48}" width="44" height="64" style="fill:transparent"/>{valve(VX, y)}</g>')
    g.append(t(VX, y - 54, 'LEI RESTRITIVA', 9.5, fill='var(--conc)', anchor='middle', weight=600))
    g.append(t(VX, y + 32, 'pode reduzir o alcance', 9.5, fill='var(--ink-2)', anchor='middle'))
    g.append(t(28, y + 14, 'não depende de lei', 9.5, fill='var(--ink-2)'))
    g.append(t(XR, y - 4, 'efeitos principais', 10.5, weight=600))
    g.append(t(XR, y + 11, 'sem restrição até a lei vir', 9.5, fill='var(--ink-2)'))
    g.append(t(XR, y + 26, 'art. 5º, XII', 9.5, fill='var(--ink-2)'))
    # limitada: the middle section is missing until the integrating law fits it
    y = ROWS[2][0]
    g.append(pipe(y, X0, GA) + pipe(y, GB, X1) + f'<path d="M{X1} {y - R - 4}V{y + R + 4}" style="stroke:var(--ink);stroke-width:2.4"/>'
             + f'<g class="fl-l">{flow(y, X1 + 4)}</g>'
             + f'<g class="gap"><rect x="{GA}" y="{y - 30}" width="{GB - GA}" height="54" style="fill:transparent"/>{pipe(y, GA, GB, dotted=True)}</g>')
    g.append(f'<path d="M{GA} {y - R - 3}V{y + R + 3}M{GB} {y - R - 3}V{y + R + 3}" style="stroke:var(--ink);stroke-width:2.4"/>')
    g.append(t((GA + GB) / 2, y - 20, 'LEI INTEGRADORA', 9.5, anchor='middle', weight=600))
    g.append(t((GA + GB) / 2, y + 30, 'falta a peça', 9.5, fill='var(--ink-2)', anchor='middle'))
    g.append(f'<path d="M{GA + 5} {y + R + 2}q-3 8 0 12q3-4 0-12" style="fill:var(--ink);stroke:none"/>')   # the drip
    g.append(t(28, y + 14, 'depende de lei', 9.5, fill='var(--ink-2)'))
    g.append(t(XR, y - 4, 'efeitos principais', 10.5, weight=600))
    g.append(t(XR, y + 11, 'só com a lei', 9.5, fill='var(--ink-2)'))
    g.append(t(XR, y + 26, 'art. 18, § 3º', 9.5, fill='var(--ink-2)'))
    g.append(f'<path d="M{GA + 5} {y + R + 18}V{y + 52}H{GA + 18}" style="fill:none;stroke:var(--ink-2);stroke-width:.9"/>')
    g.append(t(GA + 22, y + 55.5, 'mínimo: invalida a lei contrária', 9.5, fill='var(--ink-2)'))
    return svg('0 0 1010 440', ''.join(g), label='Eficácia plena, contida e limitada como três canos que saem da Constituição', ident='dci-a07-canos')


def block():
    return ('<figure class="instr" id="fig-dci-a07-canos">' + figure() +
            '<figcaption>A contida já corre e pode ser estreitada; a limitada só corre inteira quando a lei integradora '
            'completa o cano.</figcaption></figure>')


# where it goes: after the paragraph that names the confusion it resolves
ANCHOR = ('courses/direito-constitucional-i/aula-07.html', 'A confusão mais frequente é entre “contida” e “limitada”.')
