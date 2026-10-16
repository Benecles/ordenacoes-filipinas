"""Direito Constitucional I Aula 09 · proportionality as two sieves and a scale, run on the lesson's own square.

  object   three measures from the lesson's running example (the municipal square at night) are dropped from the top.
           A lid first (lawful means and end), then the adequação sieve (coarse: it only holds back a means that can't
           contribute at all), then the necessidade sieve (fine: it holds back a means when an equally apt, less
           burdensome one exists), then a scale for the strict sense. Each measure falls straight down; where a sieve
           holds it, its line stops on the mesh with a small cross.
  behaves  hover the scale: it rocks, because the lesson leaves the weighing to the facts (benefit to rest vs. cost
           to assembly). Nothing else moves
  states   ink = a measure's path · orange = where the test stops it (a limit) · mesh holes are drawn only where a
           measure passes
  facts    all three measures, the reasons each one stops, and the four questions are the lesson's (Tavares;
           Canotilho for necessity); the scale's two pans are the lesson's own goods
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from figkit import t, svg

XS = {'b': 210, 'a': 400, 'c': 590}        # the three measures' columns
YL, YA, YN, YS = 132, 228, 330, 440        # lid, adequação, necessidade, scale
SX0, SX1 = 120, 680


def stack(x, y, lines, anchor='middle', size=9.5, lead=13, fill='var(--ink-2)', weight=500):
    return ''.join(t(x, y + k * lead, s, size, fill=fill, anchor=anchor, weight=weight) for k, s in enumerate(lines))


def mesh(y, holes, hole_w):
    """a sieve: a solid bar with holes only where a measure passes, and the wire's cross-hatching"""
    xs = sorted(XS[h] for h in holes)
    segs, x = [], SX0
    for hx in xs:
        segs.append((x, hx - hole_w / 2)); x = hx + hole_w / 2
    segs.append((x, SX1))
    bar = ''.join(f'<path d="M{a:.0f} {y}H{b:.0f}" style="stroke:var(--ink);stroke-width:3.2"/>' for a, b in segs)
    wire = ''.join(f'<path d="M{v} {y - 4}V{y + 4}" style="stroke:var(--ink-2);stroke-width:.8"/>' for v in range(SX0 + 6, SX1, 12)
                   if not any(abs(v - hx) < hole_w / 2 + 2 for hx in xs))
    return bar + wire


def stop(x, y):
    return (f'<path d="M{x} {y - 2}V{y - 6}" style="stroke:var(--ink);stroke-width:1.4"/>'
            f'<path d="M{x - 6} {y - 18}l12 12M{x + 6} {y - 18}l-12 12" style="stroke:var(--conc);stroke-width:2.2;stroke-linecap:round"/>')


def path(x, y0, y1):
    return f'<path d="M{x} {y0}V{y1}" style="stroke:var(--ink);stroke-width:1.4;stroke-dasharray:5 4"/>'


def figure():
    g = []
    # the three measures, as the lesson states them
    g.append(stack(XS['b'], 34, ['proibir reuniões silenciosas', 'em praça fechada,', 'sem casas por perto'], fill='var(--ink)'))
    g.append(stack(XS['a'], 34, ['proibir toda reunião', 'após as 21h'], fill='var(--ink)'))
    g.append(stack(XS['c'], 34, ['só caixas de som', 'junto a residências,', 'das 22h às 6h'], fill='var(--ink)'))
    for k, x in XS.items():
        g.append(f'<circle cx="{x}" cy="86" r="5" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.6"/>')
    # the lid: lawful means and end (all three pass)
    g.append(f'<path d="M{SX0} {YL}H{SX1}" style="stroke:var(--ink-2);stroke-width:1.2;stroke-dasharray:1 4"/>')
    g.append(t(SX1 + 50, YL + 4, 'meio e fim lícitos?', 10, weight=600))
    # adequação: only the totally unfit means is held back
    g.append(path(XS['b'], 92, YA - 2) + stop(XS['b'], YA))
    g.append(mesh(YA, ['a', 'c'], 34))
    g.append(stack(XS['b'] - 64, YA + 22, ['meio totalmente', 'inviável para o fim'], anchor='start', fill='var(--conc)'))
    g.append(t(SX1 + 50, YA - 6, 'ADEQUAÇÃO', 10.5, weight=600))
    g.append(stack(SX1 + 50, YA + 10, ['o meio pode', 'contribuir para o fim?'], anchor='start'))
    # necessidade: the general ban is held back, an equally apt and milder means exists
    g.append(path(XS['a'], 92, YN - 2) + stop(XS['a'], YN))
    g.append(mesh(YN, ['c'], 26))
    g.append(stack(XS['a'] - 64, YN + 22, ['há meio igualmente apto', 'e menos gravoso'], anchor='start', fill='var(--conc)'))
    g.append(t(SX1 + 50, YN - 6, 'NECESSIDADE', 10.5, weight=600))
    g.append(stack(SX1 + 50, YN + 10, ['material · espacial', 'temporal · pessoal'], anchor='start'))
    # strict sense: the scale, level, waiting for the facts
    cx = XS['c']
    g.append(path(cx, 92, YS - 34))
    g.append(f'<g class="scale" style="transform-origin:{cx}px {YS - 28}px">'
             f'<rect x="{cx - 110}" y="{YS - 50}" width="220" height="70" style="fill:transparent"/>'
             f'<path d="M{cx - 92} {YS - 28}H{cx + 92}" style="stroke:var(--ink);stroke-width:2.4"/>'
             f'<path d="M{cx - 92} {YS - 28}l-16 30h32zM{cx + 92} {YS - 28}l-16 30h32z" style="fill:none;stroke:var(--ink);stroke-width:1.4;stroke-linejoin:round"/>'
             + t(cx - 92, YS + 18, 'descanso', 10, anchor='middle', weight=600) + t(cx + 92, YS + 18, 'reunião', 10, anchor='middle', weight=600)
             + '</g>')
    g.append(f'<path d="M{cx} {YS - 28}V{YS + 44}M{cx - 20} {YS + 44}h40" style="stroke:var(--ink);stroke-width:2"/>')
    g.append(t(cx, YS + 2, '?', 14, anchor='middle', weight=600))
    g.append(t(SX1 + 50, YS - 6, 'SENTIDO ESTRITO', 10.5, weight=600))
    g.append(stack(SX1 + 50, YS + 10, ['o ganho justifica', 'o sacrifício?'], anchor='start'))
    return svg('0 0 920 500', ''.join(g), label='Três medidas da praça passam pela adequação, pela necessidade e pela balança', ident='dci-a09-peneiras')


def block():
    return ('<figure class="instr" id="fig-dci-a09-peneiras">' + figure() +
            '<figcaption>As três medidas da praça. Só a regra das caixas de som chega à balança, e o resultado depende dos fatos.</figcaption></figure>')


ANCHOR = ('courses/direito-constitucional-i/aula-09.html', 'Adequação examina a conexão entre o meio escolhido e o objetivo declarado.')
