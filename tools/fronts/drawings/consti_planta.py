#!/usr/bin/env python3
"""Direito Constitucional I front: the Constitution as a surveyor's rod.

  object   time runs down the sheet into the CF/88. The charters before it sit on a thin line (1215 → 1967/69); at
           1988 the line becomes a rod banded by the nine Títulos, arts. 1 → 250, and every lesson hangs at the height
           of the article it applies. Art. 5, where half the course lives, is magnified into a second rod (incisos and
           §§). The lessons that read any article (types, efficacy, rules and principles, proportionality) sit under
           a lens. Numbers: ink = doctrine, blue = a decided case, orange = the limit (art. 60 §4).
  facts    every article and year is cited in its lesson's own text (checked 15/10 by counting citations per page).
usage: consti_planta.py   (writes the drawing into tools/fronts/data/direito-constitucional-i.json; then front.py)
"""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data', 'direito-constitucional-i.json')
E = html.escape

W, H = 1180, 700
X = 150                     # the main line / rod
R0, R1 = 252, 660           # rod: art. 1 → art. 250
def ya(a): return R0 + (a - 1) * (R1 - R0) / 249

TITULOS = [('I', 1, 4), ('II', 5, 17), ('III', 18, 43), ('IV', 44, 135), ('V', 136, 144), ('VI', 145, 169),
           ('VII', 170, 192), ('VIII', 193, 232), ('IX', 233, 250)]
YEARS = [(1215, 46, 'o'), (1689, 64, 'o'), (1787, 82, 'o'), (1791, 98, 'o'),
         (1824, 122, 'b'), (1891, 140, 'b'), (1934, 160, 'b'), (1937, 174, 'b'), (1946, 188, 'b'), ('1967/69', 202, 'b')]
Y1988 = 222

# (href, number, title, article, kind)  kind: doc | case | limit
MAIN = [
    ('aula-22.html', '22', 'Direitos sociais: exigibilidade', 6, 'doc'),
    ('aula-22-retrocesso.html', '22', 'Retrocesso e o teto de gastos', 6, 'doc'),
    ('aula-16-casos.html', '16', 'RE 778.889 e licença à adotante', 7, 'case'),
    ('aula-21-casos.html', '21', 'ADPF 132 e licença da adotante', 7, 'case'),
    ('aula-04-casos.html', '04', 'ADI 3.345 e o número de vereadores', 29, 'case'),
    ('aula-07-casos.html', '07', 'ADI 5.316 e aposentadoria aos 75', 40, 'case'),
    ('aula-05.html', '05', 'Poder constituinte e poder de reforma', 60, 'doc'),
    ('aula-06.html', '06', 'Reforma e limites da Constituição', 60, 'limit'),
    ('aula-06-casos.html', '06', 'Limites à reforma: ADI 2.096 e 5.316-MC', 60, 'case'),
    ('aula-06-casos-precatorios.html', '06', 'Precatórios e a EC 30/2000', 100, 'case'),
    ('aula-04.html', '04', 'Supremacia e guarda da Constituição', 102, 'doc'),
    ('aula-23.html', '23', 'Moradia: posse e política urbana', 183, 'doc'),
    ('aula-18.html', '18', 'Expressão: âmbito e censura', 220, 'doc'),
    ('aula-24.html', '24', 'Direito fundamental ao ambiente', 225, 'doc'),
    ('aula-21.html', '21', 'Liberdade sexual e a ADPF 132', 226, 'doc'),
    ('aula-15-casos.html', '15', 'ADPF 132 e ADI efeito horizontal', 226, 'case'),
    ('aula-25.html', '25', 'Identidade cultural dos povos indígenas', 231, 'doc'),
]
# art. 5, magnified: position 0 = caput, 1..79 = incisos, 101..103 = §§1–3
X5 = 700
I0, I1 = 300, 590            # caput → inciso LXXIX
P0 = 616                     # §1; §§ are 16 px apart
def yi(n):
    if n == 0: return I0 - 14
    if n > 100: return P0 + (n - 101) * 16
    return I0 + (n - 1) * (I1 - I0) / 78
ART5 = [
    ('aula-14.html', '14', 'Dimensões, funções e titulares', [0], 'doc'),
    ('aula-16.html', '16', 'Restrições aos direitos fundamentais', [0], 'doc'),
    ('aula-18-limites.html', '18', 'Discurso de ódio e sátira eleitoral', [(4, 5)], 'doc'),
    ('aula-18-casos.html', '18', 'ADPF 130 e liberdade de imprensa', [5], 'case'),
    ('aula-19-casos.html', '19', 'ADPF 130 e imprensa livre', [5], 'case'),
    ('aula-17.html', '17', 'Liberdade religiosa e objeção de consciência', [(6, 8)], 'doc'),
    ('aula-19.html', '19', 'Direito à informação e acesso à informação', [14, 33], 'doc'),
    ('aula-20.html', '20', 'Propriedade: função social e intervenção', [(22, 26)], 'doc'),
    ('aula-15.html', '15', 'Aplicação imediata e destinatários', [101], 'doc'),
    ('aula-13.html', '13', 'Catálogo aberto de direitos fundamentais', [102], 'doc'),
    ('aula-11.html', '11', 'Constituição no espaço e tratados', [103], 'doc'),
]
HISTORY = [
    ('aula-01.html', '01', 'Origens das constituições', 46, 98),
    ('aula-03.html', '03', 'Império e Primeira República', 122, 152),
    ('aula-03-republica.html', '03', 'De 1930 a 1988', 160, Y1988 - 4),
]
LENS = [('aula-02.html', '02', 'Tipos de Constituição'), ('aula-07.html', '07', 'Eficácia das normas constitucionais'),
        ('aula-08.html', '08', 'Regras e princípios constitucionais'), ('aula-09.html', '09', 'Proporcionalidade e restrição estatal'),
        ('aula-12.html', '12', 'Direitos humanos e direitos fundamentais')]

ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
def roman(n):
    tens = ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX']
    return tens[n // 10] + ROMAN[n % 10]


def place(ys, gap, lo):
    """1D label placement: keep order, push labels down until no two are closer than gap"""
    out, last = [], lo - gap
    for y in ys:
        y = max(y, last + gap); out.append(y); last = y
    return out


def label(href, num, title, ly, x, kind, ticks):
    """one lesson: the leader from its tick(s) on the rod to the label, the number, the title; the whole is the link"""
    cls = {'doc': '', 'case': ' case', 'limit': ' limit'}[kind]
    lead = ''.join(ticks)
    return (f'<a href="{href}" class="pin{cls}"><title>{E(title)}</title>{lead}'
            f'<text x="{x}" y="{ly + 4:.1f}"><tspan class="n">{num}</tspan><tspan class="t" dx="8">{E(title)}</tspan></text></a>')


def svg():
    g = []
    # the line before 1988 (origins in grey, Brazil in ink) and the 1988 node
    g.append(f'<path d="M{X} 40V104" class="ln o"/><path d="M{X} 116V{Y1988}" class="ln"/>')
    for y, yy, k in YEARS:
        g.append(f'<circle cx="{X}" cy="{yy}" r="3" class="yr {k}"/><text x="{X - 12}" y="{yy + 3.5}" class="yl {k}" text-anchor="end">{y}</text>')
    g.append(f'<circle cx="{X}" cy="{Y1988}" r="7" class="n88"/><text x="{X - 14}" y="{Y1988 + 4}" class="yl b88" text-anchor="end">1988</text>')
    g.append(f'<path d="M{X} {Y1988 + 7}V{R0 - 2}" class="ln"/>')
    # the rod: bands per Título, numerals to the left, article marks every 50
    for k, (r, a, b) in enumerate(TITULOS):
        y0, y1 = ya(a) - .8, ya(b) + .8
        g.append(f'<rect x="{X - 6}" y="{y0:.1f}" width="12" height="{y1 - y0:.1f}" class="band {"f" if k % 2 else "e"}"/>')
        ym = (y0 + y1) / 2 + (-5 if r == 'I' else 3 if r == 'II' else 0)
        g.append(f'<text x="{X - 16}" y="{ym + 3:.1f}" class="tn" text-anchor="end">{r}</text>')
    for a in (50, 100, 150, 200, 250):
        g.append(f'<path d="M{X - 46} {ya(a):.1f}H{X - 30}" class="tk"/><text x="{X - 50}" y="{ya(a) + 3.5:.1f}" class="al" text-anchor="end">{a}</text>')
    g.append(f'<text x="{X - 50}" y="{R0 + 3.5}" class="al" text-anchor="end">art. 1</text>')
    # art. 60 §4: the one limit on the rod
    g.append(f'<path d="M{X - 9} {ya(60):.1f}H{X + 9}" class="lim"/>')
    # recepção: the law in force in 1988 crosses into the new order (right of the line, from the 1988 node into art. 1)
    yr = (Y1988 + R0) / 2
    rec = (f'<path d="M{X + 7} {Y1988}C{X + 30} {Y1988 + 2} {X + 30} {R0 + 4} {X + 10} {R0 + 4}" class="rec" marker-end="url(#cpa)"/>'
           f'<path d="M{X + 27} {yr:.1f}H{X + 42}" class="ld"/>')
    g.append(label('aula-10.html', '10', 'Normas no tempo e recepção', yr, X + 48, 'doc', [rec]))
    # history lessons: a bracket on the right of the line
    for href, num, title, y0, y1 in HISTORY:
        ym = (y0 + y1) / 2
        br = f'<path d="M{X + 10} {y0}h6V{y1}h-6" class="br"/><path d="M{X + 16} {ym}H{X + 34}" class="ld"/>'
        g.append(label(href, num, title, ym, X + 40, 'doc', [br]))
    # main rod lessons
    ys = place([ya(a) for *_, a, _k in MAIN], 19, ya(5) + 16)   # below the art. 5 connector
    for (href, num, title, a, kind), ly in zip(MAIN, ys):
        y = ya(a)
        lead = (f'<circle cx="{X + 6}" cy="{y:.1f}" r="2.4" class="dot"/>'
                f'<path d="M{X + 8} {y:.1f}H{X + 22}L{X + 34} {ly:.1f}H{X + 42}" class="ld"/>')
        g.append(label(href, num, title, ly, X + 48, kind, [lead]))
    # art. 5 magnified: the connector, then its own rod
    y5 = ya(5)
    g.append(f'<path d="M{X + 6} {y5:.1f}H{X5 - 30}V{I0 - 26}H{X5}" class="zoom"/><text x="{X5 - 24}" y="{y5 - 6:.1f}" class="al">art. 5</text>')
    g.append(f'<path d="M{X5} {I0 - 26}V{I0 - 8}" class="ln"/>')
    g.append(f'<rect x="{X5 - 4}" y="{I0}" width="8" height="{I1 - I0}" class="band e"/>')
    for n in range(10, 80, 10):
        g.append(f'<path d="M{X5 - 4} {yi(n):.1f}H{X5 - 10}" class="tk"/><text x="{X5 - 14}" y="{yi(n) + 3.5:.1f}" class="al" text-anchor="end">{roman(n)}</text>')
    g.append(f'<text x="{X5 - 14}" y="{yi(1) + 3.5:.1f}" class="al" text-anchor="end">I</text>')
    g.append(f'<text x="{X5 - 14}" y="{yi(0) + 3.5:.1f}" class="al" text-anchor="end">caput</text>')
    for k in range(3):
        y = yi(101 + k)
        g.append(f'<circle cx="{X5}" cy="{y:.1f}" r="3.5" class="par"/><text x="{X5 - 14}" y="{y + 3.5:.1f}" class="al" text-anchor="end">§{k + 1}</text>')
    ys5 = place([yi(t[0] if isinstance(t[0], int) else t[0][0]) for *_, t, _k in ART5], 21, I0 - 20)
    for (href, num, title, ticks, kind), ly in zip(ART5, ys5):
        parts = []
        first = None
        for t in ticks:
            if isinstance(t, tuple):
                y0, y1 = yi(t[0]) - 1.5, yi(t[1]) + 1.5
                parts.append(f'<path d="M{X5 + 7} {y0:.1f}h4V{y1:.1f}h-4" class="br"/>')
                yy = (y0 + y1) / 2
            else:
                yy = yi(t)
                parts.append(f'<circle cx="{X5 + 7}" cy="{yy:.1f}" r="2.4" class="dot"/>')
            first = yy if first is None else first
        parts.append(f'<path d="M{X5 + 12} {first:.1f}H{X5 + 24}L{X5 + 36} {ly:.1f}H{X5 + 44}" class="ld"/>')
        g.append(label(href, num, title, ly, X5 + 50, kind, parts))
    # the lens: lessons that read any article
    lx, ly0 = X5 - 18, 52
    g.append(f'<g class="lens"><circle cx="{lx}" cy="{ly0 + 26}" r="17"/><path d="M{lx + 12} {ly0 + 38}l14 14"/></g>')
    for k, (href, num, title) in enumerate(LENS):
        g.append(label(href, num, title, ly0 + k * 22, X5 + 50, 'doc', []))
    defs = ('<defs><marker id="cpa" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
            '<path d="M0 0L10 5L0 10z" style="fill:var(--ink)"/></marker></defs>')
    return (f'<svg class="cpl" viewBox="0 0 {W} {H}" role="img" aria-label="A Constituição de 1988 artigo por artigo, '
            f'com cada aula no artigo que aplica">{defs}{"".join(g)}</svg>')


CSS = ('.cpl{width:100%;height:auto;display:block}'
       '.cpl text{font-family:var(--mono);font-size:11px;fill:var(--ink)}'
       '.cpl .ln{stroke:var(--ink);stroke-width:1.6;fill:none}.cpl .ln.o{stroke:var(--ink-2);stroke-dasharray:2 3}'
       '.cpl .yr{fill:var(--paper);stroke:var(--ink);stroke-width:1.4}.cpl .yr.o{stroke:var(--ink-2)}'
       '.cpl .yl{font-size:10.5px}.cpl .yl.o{fill:var(--ink-2)}.cpl .b88{font-weight:600;font-size:12px}'
       '.cpl .n88{fill:var(--ink)}'
       '.cpl .band.e{fill:var(--paper);stroke:var(--ink);stroke-width:1.2}.cpl .band.f{fill:var(--ink);stroke:var(--ink);stroke-width:1.2}'
       '.cpl .tn{font-size:9.5px;fill:var(--ink-2);letter-spacing:.06em}.cpl .al{font-size:9.5px;fill:var(--ink-2)}'
       '.cpl .tk{stroke:var(--ink-2);stroke-width:1}'
       '.cpl .lim{stroke:var(--conc);stroke-width:3}'
       '.cpl .rec{stroke:var(--ink);stroke-width:1.2;fill:none;stroke-dasharray:4 3}'
       '.cpl .zoom{stroke:var(--ink-2);stroke-width:1;fill:none;stroke-dasharray:1 3}'
       '.cpl .par{fill:var(--paper);stroke:var(--ink);stroke-width:1.3}'
       '.cpl .br{stroke:var(--ink);stroke-width:1.2;fill:none}.cpl .ld{stroke:var(--ink-2);stroke-width:.9;fill:none}'
       '.cpl .dot{fill:var(--ink)}'
       '.cpl .lens circle,.cpl .lens path{fill:none;stroke:var(--ink);stroke-width:2}'
       '.cpl .n{font-weight:600;font-size:11.5px}.cpl .case .n{fill:var(--dif)}.cpl .limit .n{fill:var(--conc)}'
       '.cpl .t{font-family:var(--sans);font-size:13px}'
       '.cpl a .ld,.cpl a .dot{transition:stroke .15s,fill .15s,stroke-width .15s}'
       '.cpl a:hover .t,.cpl a:focus-visible .t{text-decoration:underline;text-underline-offset:3px}'
       '.cpl a:hover .ld,.cpl a:focus-visible .ld{stroke:var(--ink);stroke-width:1.6}'
       '.cpl a:hover .br{stroke-width:2}')

if __name__ == '__main__':
    d = json.load(open(DATA))
    d['drawing'] = {'html': svg(), 'css': CSS}
    json.dump(d, open(DATA, 'w'), ensure_ascii=False, indent=2); open(DATA, 'a').write('\n')
    print('consti planta:', len(MAIN) + len(ART5) + len(HISTORY) + len(LENS) + 1, 'lessons pinned')
