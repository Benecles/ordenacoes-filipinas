#!/usr/bin/env python3
"""Processo Civil I front: the course as the autos, seen edge-on.

  object   the cover on top, then the folhas in the order the procedure adds them: one block per act, one bundle of
           folhas per lesson, each bundle as thick as the lesson's reading time (so the stack shows where the work
           is). Each lesson is a flag stuck into its own bundle; the flag is the link. The P1 cut is a ribbon.
  facts    acts and their order come from the docket the front carried before (`source_html`); lesson names are the
           register's titles (one name per lesson: the same string on the flag, the register row and the page h1).
usage: processo_autos.py   (rewrites the drawing in tools/fronts/data/processo-civil-i.json; then run front.py)
Ported 03/11 from the workshop's INSTRUMENT-2 bench script (work/house-style/instrument2/front_processo.py).
"""
import html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import front  # noqa: E402  (reading time: the register's own clock)

DATA = HERE.parent / 'data' / 'processo-civil-i.json'
ACT_NAMES = {'PETIÇÃO': 'Petição', 'JUÍZO INICIAL': 'Juízo inicial', 'SUJEITOS': 'Sujeitos', 'COMUNICAÇÃO': 'Comunicação',
             'RESPOSTA': 'Resposta', 'NULIDADES': 'Nulidades', 'SANEAMENTO': 'Saneamento', 'PROVA': 'Prova'}
W, SX, SW = 1040, 230, 330     # canvas, stack left edge, stack width
FLAG = 22                      # flag height
PER_MIN, BASE = 1.4, 10        # bundle thickness: BASE + minutes × PER_MIN (10′ → 24 px, 25′ → 45 px)
GAP, ACT_MIN = 10, 40          # gap between acts; an act is at least tall enough for its two labels


def acts_from(old_html):
    acts = []
    for p, body in re.findall(r'<li class="proc-phase (p\d)">(.*?)</li>', old_html, re.S):
        title = html.unescape(re.search(r'proc-phase-title">(.*?)<', body).group(1))
        sub = html.unescape(re.search(r'proc-phase-sub">(.*?)<', body).group(1))
        acts.append({'name': ACT_NAMES.get(title, title.title()), 'sub': sub, 'exam': p,
                     'lessons': re.findall(r'<a href="([^"]+)">', body)})
    return acts


def t(x, y, s, size, weight=500, fam='var(--mono)', anchor='start', fill='var(--ink)', italic=False):
    st = f'font-family:{fam};font-size:{size}px;font-weight:{weight};fill:{fill}' + (';font-style:italic' if italic else '')
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="{st}">{html.escape(s)}</text>'


def draw(acts, lessons):
    seed = 7
    def jit():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) & 0x7fffffff
        return (seed % 7) - 3
    o, flags = [], []
    o.append(f'<path d="M{SX - 6} 30h{SW + 12}v26h-{SW + 12}z" style="fill:var(--grid-major);stroke:var(--ink);stroke-width:1.6"/>')
    o.append(t(SX + 14, 48, 'AUTOS · PROCEDIMENTO COMUM', 11.5, 700))
    o.append(t(SX + SW - 8, 48, 'DIR02002', 11, 500, anchor='end', fill='var(--ink-2)'))
    y, ribbon_y, prev = 70, None, acts[0]['exam']
    for a in acts:
        if a['exam'] != prev and ribbon_y is None:
            ribbon_y, y = y + 16, y + 52
        prev = a['exam']
        top = y
        bundles = []
        for href in a['lessons']:
            h = BASE + lessons[href]['min'] * PER_MIN
            bundles.append((href, y, h)); y += h
        if y - top < ACT_MIN:   # stretch the last bundle so the act's labels never collide with the next act
            href, by, bh = bundles[-1]; bundles[-1] = (href, by, bh + ACT_MIN - (y - top)); y = top + ACT_MIN
        g = [f'<path d="M{SX} {top:.1f}h{SW}v{y - top:.1f}h-{SW}z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>']
        for i, (href, by, bh) in enumerate(bundles):
            lines = [f'M{SX + jit() * .6:.1f} {by + 3 + k * 4.2:.1f}H{SX + SW + jit():.1f}' for k in range(int((bh - 2) / 4.2))]
            g.append(f'<path class="leaves" d="{"".join(lines)}" style="stroke:var(--ink-2);stroke-width:.6;opacity:.55;fill:none"/>')
            if i:   # the seam between two lessons' bundles
                g.append(f'<path d="M{SX} {by:.1f}h{SW}" style="stroke:var(--ink);stroke-width:.9"/>')
        o.append(f'<g class="act" data-act="{html.escape(a["name"])}">' + ''.join(g) + '</g>')
        o.append(t(SX - 22, top + 19, a['name'], 17, 600, 'var(--sans, var(--serif))', 'end'))
        o.append(t(SX - 22, top + 36, a['sub'], 12, 400, 'var(--serif)', 'end', 'var(--ink-2)', italic=True))
        for href, by, bh in bundles:
            l = lessons[href]
            fy = by + min(4, (bh - FLAG) / 2)
            w = 34 + len(l['title']) * 7.4
            flags.append(
                f'<a class="flag" href="{href}" aria-label="Aula {l["n"]}: {html.escape(l["title"])} · {l["min"]} min">'
                f'<g class="flag-g"><path d="M{SX + SW - 70} {fy:.1f}h{w + 70:.1f}l-8 {FLAG / 2}l8 {FLAG / 2}h-{w + 70:.1f}z" '
                'style="stroke:var(--ink);stroke-width:1.2"/>'
                + t(SX + SW + 10, round(fy + 15.5, 1), l['n'], 12, 700)
                + t(SX + SW + 36, round(fy + 15.5, 1), l['title'], 13, 500, 'var(--serif)') + '</g></a>')
        y += GAP
    if ribbon_y is not None:
        ry = ribbon_y
        o.append(f'<g class="ribbon"><path d="M{SX - 12} {ry - 7}H{SX + SW + 18}l10 7l-10 7H{SX - 12}z" style="fill:var(--conc);opacity:.92"/>'
                 + t(SX - 22, ry - 3, 'P1 · semanas 1–9', 11, 600, anchor='end', fill='var(--ink-2)')
                 + t(SX - 22, ry + 13, 'P2 · semanas 11–16', 11, 600, anchor='end', fill='var(--ink-2)') + '</g>')
    return (f'<svg class="autos" data-family="figure.autos" viewBox="0 0 {W} {y:.0f}" role="group" aria-label="Os autos do curso: '
            'cada aula é um maço de folhas, da espessura do seu tempo de leitura, marcado no ato do procedimento que ela '
            'estuda; a fita marca o corte da P1.">' + ''.join(flags) + ''.join(o) + '</svg>')


CSS = """
.proc-autos{margin:0}.proc-autos svg{display:block;width:100%;height:auto}
.proc-autos .flag-g path{fill:var(--paper);transition:transform .25s ease, fill .2s}
.proc-autos .flag-g{transition:transform .25s ease}
.proc-autos .flag:hover .flag-g,.proc-autos .flag:focus-visible .flag-g{transform:translateX(14px)}
.proc-autos .flag:hover .flag-g path,.proc-autos .flag:focus-visible .flag-g path{fill:var(--grid-major)}
.proc-autos .flag:focus-visible{outline:none}
.proc-autos .flag:focus-visible .flag-g path{stroke:var(--dif);stroke-width:2.2}
.proc-autos figcaption{font:400 15px/1.5 var(--serif);color:var(--ink-2);margin:6px 0 0}
@media (prefers-reduced-motion:reduce){.proc-autos .flag-g{transition:none}}
"""


def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    src = data['drawing']['source_html']
    acts = acts_from(src)
    order = [l for u in data['units'] for l in u['lessons']]
    lessons = {l['href']: {'title': l['title'], 'n': f'{i:02d}', 'min': front._minutes('processo-civil-i', l['href']) or 15}
               for i, l in enumerate(order, 1)}
    assert sorted(h for a in acts for h in a['lessons']) == sorted(lessons), 'docket and register disagree on lessons'
    fig = ('<figure class="proc-autos">' + draw(acts, lessons)
           + '<figcaption>Cada maço de folhas é uma aula; a espessura é o tempo de leitura. '
             'A aferição final é cumulativa, conforme o cronograma.</figcaption></figure>')
    data['drawing'] = {'html': fig, 'css': CSS, 'source_html': src}
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('processo front: the autos redrawn; now run tools/fronts/front.py processo-civil-i')


if __name__ == '__main__':
    main()
