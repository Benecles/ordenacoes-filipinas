#!/usr/bin/env python3
"""Teoria Geral dos Contratos front: one contract, open on the desk.

  object   a contract as a bound sheet laid open. The left leaf is everything before the signatures (the concept, the
           principles, the way the deal forms, the slip of arras, the boxes of its class), ending in the two signatures.
           The right leaf is what happens to the contract afterwards (reciprocal duties, a clause read, a signature
           replaced by an endorsement, a rider pasted over a clause, the closing stamp). The binding is the P1/P2 cut.
  links    each lesson is a notched tab poking out of the leaf edge, at the height of the moment it governs; the tab is
           the link. A tab's height follows the lesson's reading time (computed from the page, as the register does).
  facts    lesson names and goals are the register's; exam covers are `reg.exams`. No date, article or number is typed.
usage: contratos_front.py   (rewrites the drawing in tools/fronts/data/teoria-geral-dos-contratos.json; then run front.py)
"""
import html, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import front  # noqa: E402  (reading time: the register's own clock)

SLUG = 'teoria-geral-dos-contratos'
DATA = HERE.parent / 'data' / f'{SLUG}.json'
W, H = 1040, 640
TW = 200                       # tab length
LX0, LX1 = 210, 513            # left leaf
RX0, RX1 = 527, 830            # right leaf
PY0, PY1 = 40, 604             # leaf top, bottom
ANCHOR_L = [112, 202, 292, 388, 474]   # moment of the contract each left tab governs (tab centre)
ANCHOR_R = [112, 204, 300, 396, 492]
PER_MIN, BASE, TAB_MIN = 1.3, 12, 40   # tab height = max(TAB_MIN, BASE + minutes x PER_MIN)

INK, INK2 = 'var(--ink)', 'var(--ink-2)'


def t(x, y, s, size, weight=500, fam='var(--mono)', anchor='start', fill=INK):
    st = f'font-family:{fam};font-size:{size}px;font-weight:{weight};fill:{fill}'
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="{st}">{html.escape(s)}</text>'


def wrap(text, width):
    lines, cur = [], ''
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur); cur = w
        else:
            cur = f'{cur} {w}'.strip()
    return lines + ([cur] if cur else [])


def bars(x, y, widths, gap=9, h=3.2, fill=INK2, op=.55):
    """Ruled clause lines (the leaf's own text, not read): one bar per width."""
    return ''.join(f'<path d="M{x} {y + i * gap:.1f}h{w}" style="stroke:{fill};stroke-width:{h};opacity:{op};fill:none"/>'
                   for i, w in enumerate(widths))


def left_leaf():
    o, x = [], LX0 + 26
    # 01 the heading: what the document is called
    y = ANCHOR_L[0]
    o.append(f'<path d="M{x} {y - 26}h{LX1 - LX0 - 52}" style="stroke:{INK};stroke-width:2.4"/>')
    o.append(f'<path d="M{x} {y - 6}h184M{x} {y + 10}h118" style="stroke:{INK};stroke-width:9"/>')
    o.append(f'<path d="M{x} {y + 28}h{LX1 - LX0 - 52}" style="stroke:{INK};stroke-width:.9"/>')
    # 02 the recital under a margin rule: the principles frame every clause; the limit is the orange tick
    y = ANCHOR_L[1]
    o.append(bars(x + 14, y - 18, [250, 238, 244, 150]))
    o.append(f'<path d="M{x + 2} {y - 22}v46" style="stroke:{INK};stroke-width:1.6"/>')
    o.append(f'<path d="M{x - 4} {y + 24}h16" style="stroke:var(--conc);stroke-width:3"/>')
    # 03 how it forms: dashed talks, then the offer's lines, then the acceptance's blue mark
    y = ANCHOR_L[2]
    o.append(f'<path d="M{x} {y - 24}h96M{x} {y - 14}h138M{x} {y - 4}h72" style="stroke:{INK2};stroke-width:1.4;stroke-dasharray:4 4;fill:none"/>')
    o.append(bars(x, y + 10, [250, 214], 9))
    o.append(f'<path d="M{x + 130} {y + 36}h120" style="stroke:var(--dif);stroke-width:3.4"/>')
    # 04 a slip stapled to the leaf: the arras
    y = ANCHOR_L[3]
    sx, sy = x + 150, y - 30
    o.append(bars(x, y - 20, [120, 104, 112], 9))
    o.append(f'<path d="M{sx + 8} {sy + 8}h96v50h-96z" style="fill:var(--grid-major)"/>'
             f'<path d="M{sx} {sy}h96v50h-96z" style="fill:var(--paper);stroke:{INK};stroke-width:1.3"/>'
             f'<path d="M{sx + 14} {sy}v50" style="stroke:{INK2};stroke-width:1;stroke-dasharray:2 3"/>'
             f'<path d="M{sx + 28} {sy + 14}h54M{sx + 28} {sy + 26}h40" style="stroke:{INK2};stroke-width:2.4;opacity:.6"/>'
             f'<path d="M{sx + 40} {sy - 5}h22M{sx + 40} {sy - 1}h22" style="stroke:{INK};stroke-width:1.6"/>')
    # 05 the boxes of its class, two ticked
    y = ANCHOR_L[4]
    for i in range(4):
        by = y - 30 + i * 18
        fill = 'var(--dif)' if i in (0, 2) else 'none'
        o.append(f'<path d="M{x} {by}h11v11h-11z" style="fill:{fill};stroke:{INK};stroke-width:1.2"/>'
                 f'<path d="M{x + 22} {by + 5.5}h{150 - i * 18}" style="stroke:{INK2};stroke-width:3.2;opacity:.55"/>')
    # the two signatures, at the foot: what the leaf has been moving toward
    sy = 560
    o.append(f'<path d="M{x} {sy}h122M{x + 150} {sy}h122" style="stroke:{INK};stroke-width:1.2"/>')
    o.append(f'<path d="M{x + 6} {sy - 4}c10 -24 20 -22 24 -6s6 14 18 -4s14 -16 22 -2s20 6 32 -6" '
             'style="stroke:var(--dif);stroke-width:2;fill:none"/>')
    o.append(f'<path d="M{x + 158} {sy - 3}c8 -20 18 -26 22 -10s2 18 14 4s10 -18 20 -6s16 12 30 -2" '
             'style="stroke:var(--dif);stroke-width:2;fill:none"/>')
    return ''.join(o)


def right_leaf():
    o, x = [], RX0 + 26
    # 06 reciprocal duties: two columns, each bar held by its counterpart; below, pre-printed lines of one pattern
    y = ANCHOR_R[0]
    for i, w in enumerate((92, 108, 80)):
        o.append(f'<path d="M{x} {y - 30 + i * 13}h{w}M{x + 150} {y - 30 + i * 13}h{w - 6}" style="stroke:{INK2};stroke-width:3.2;opacity:.6"/>'
                 f'<path d="M{x + w + 4} {y - 30 + i * 13}h{150 - w - 8}" style="stroke:{INK};stroke-width:.9;stroke-dasharray:1 3"/>')
    o.append(f'<path d="M{x} {y + 18}h{RX1 - RX0 - 52}v34h-{RX1 - RX0 - 52}z" style="fill:var(--grid-major);opacity:.55"/>')
    o.append(''.join(f'<path d="M{x + 8} {y + 26 + k * 8}h{RX1 - RX0 - 68}" style="stroke:{INK2};stroke-width:1.6;opacity:.7"/>' for k in range(3)))
    # 07 a clause being read: the middle line underlined by hand, three ticks in the margin
    y = ANCHOR_R[1]
    o.append(bars(x + 14, y - 22, [244, 232, 240, 130]))
    o.append(f'<path d="M{x + 14} {y - 10}c40 5 80 -4 120 1s70 2 116 -3" style="stroke:var(--dif);stroke-width:2;fill:none"/>')
    o.append(f'<path d="M{x + 4} {y - 24}h-4v40h4" style="stroke:{INK};stroke-width:1.4;fill:none"/>')
    o.append(f'<path d="M{x - 8} {y - 12}h6M{x - 8} {y - 2}h6M{x - 8} {y + 8}h6" style="stroke:var(--dif);stroke-width:2"/>')
    # 08 a signature struck out and an endorsement strip pasted below it
    y = ANCHOR_R[2]
    o.append(f'<path d="M{x} {y - 8}h122" style="stroke:{INK};stroke-width:1.2"/>')
    o.append(f'<path d="M{x + 6} {y - 12}c10 -24 20 -22 24 -6s6 14 18 -4s14 -16 22 -2s20 6 32 -6" style="stroke:{INK2};stroke-width:1.8;fill:none;opacity:.7"/>')
    o.append(f'<path d="M{x - 4} {y - 22}l134 26" style="stroke:{INK};stroke-width:1.3"/>')
    o.append(f'<path d="M{x + 12} {y + 14}h246v38h-246z" style="fill:var(--grid-major)"/>'
             f'<path d="M{x + 6} {y + 8}h246v38h-246z" style="fill:var(--paper);stroke:{INK};stroke-width:1.3"/>'
             f'<path d="M{x + 20} {y + 36}h110" style="stroke:{INK};stroke-width:1.1"/>'
             f'<path d="M{x + 24} {y + 32}c8 -20 16 -22 20 -8s4 12 14 -2s10 -14 18 -4s14 8 26 -2" style="stroke:var(--dif);stroke-width:2;fill:none"/>'
             f'<path d="M{x + 150} {y + 20}h86M{x + 150} {y + 30}h60" style="stroke:{INK2};stroke-width:2.6;opacity:.55"/>')
    # 09 a rider pasted over a clause: the old lines show above and below it; the orange tape is the limit
    y = ANCHOR_R[3]
    o.append(bars(x, y - 30, [262, 250], 9))
    o.append(bars(x, y + 32, [258, 244], 9))
    o.append(f'<path d="M{x + 18} {y - 8}h232v46h-232z" style="fill:var(--grid-major)"/>'
             f'<path d="M{x + 12} {y - 14}h232v46h-232z" style="fill:var(--paper);stroke:{INK};stroke-width:1.3"/>'
             f'<path d="M{x + 28} {y}h176M{x + 28} {y + 11}h196M{x + 28} {y + 22}h120" style="stroke:{INK};stroke-width:3;opacity:.8"/>'
             f'<path d="M{x + 196} {y - 22}h30v14h-30z" style="fill:var(--conc-wash);stroke:var(--conc);stroke-width:1.2"/>')
    # 10 the end: the rest of the form struck through, the stamp in the corner
    y = ANCHOR_R[4]
    o.append(bars(x, y - 30, [250, 238, 244, 190], 10))
    o.append(f'<path d="M{x - 6} {y - 36}l{RX1 - RX0 - 40} 52" style="stroke:var(--conc);stroke-width:1.6"/>')
    sx, sy = x + 170, y + 22
    o.append(f'<path d="M{sx} {sy}h76v62h-76z" style="fill:none;stroke:var(--conc);stroke-width:3"/>'
             f'<path d="M{sx + 7} {sy + 7}h62v48h-62z" style="fill:none;stroke:var(--conc);stroke-width:1.2"/>'
             f'<path d="M{sx + 16} {sy + 22}h44M{sx + 16} {sy + 34}h44" style="stroke:var(--conc);stroke-width:4;opacity:.85"/>')
    o.append(bars(x, y + 40, [140, 120, 130], 9, fill=INK2, op=.3))
    return ''.join(o)


def spine():
    o = [f'<path d="M{LX1} {PY0}h{RX0 - LX1}v{PY1 - PY0}h-{RX0 - LX1}z" style="fill:var(--grid-major)"/>']
    for sy in (PY0 + 110, PY1 - 126):   # the staples that bind the two leaves
        o.append(f'<path d="M{LX1 - 6} {sy}h{RX0 - LX1 + 12}v6h-{RX0 - LX1 + 12}z" style="fill:var(--ink)"/>')
    return ''.join(o)


def leaf(x0, x1):
    return (f'<path d="M{x0 + 7} {PY0 + 7}H{x1 + 7}V{PY1 + 7}H{x0 + 7}z" style="fill:var(--grid-major)"/>'
            f'<path d="M{x0} {PY0}H{x1}V{PY1}H{x0}z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.6"/>')


def tab(l, y, side):
    h = max(TAB_MIN, BASE + l['min'] * PER_MIN)
    fy = y - h / 2
    if side == 'L':
        e = LX0
        p = f'M{e} {fy:.1f}h-{TW}l8 {h / 2:.1f}l-8 {h / 2:.1f}h{TW}z'
        nx, tx = e - TW + 18, e - TW + 42
    else:
        e = RX1
        p = f'M{e} {fy:.1f}h{TW}l-8 {h / 2:.1f}l8 {h / 2:.1f}h-{TW}z'
        nx, tx = e + 14, e + 38
    lines = wrap(l['title'], 24)
    ty0 = y - 8 * (len(lines) - 1) + 4.5
    body = ''.join(t(tx, round(ty0 + 16 * k, 1), ln, 13, 500, 'var(--serif)') for k, ln in enumerate(lines))
    cls = 'tab-g tab-l' if side == 'L' else 'tab-g tab-r'
    return (f'<a class="tab" href="{l["href"]}" data-n="{l["n"]}" aria-label="Aula {l["n"]}: {html.escape(l["title"])}. '
            f'{html.escape(l["goal"])} {l["min"]} min."><g class="{cls}"><path d="{p}" style="stroke:var(--ink);stroke-width:1.3"/>'
            + t(nx, round(y + 4.5, 1), l['n'], 12, 700) + body + '</g></a>'), h


def slip(l, y, h, side):
    lines = wrap(l['goal'], 38)
    sh = 20 + 17 * len(lines) + 24
    sw = 292
    sx = LX0 + 22 if side == 'L' else RX1 - 22 - sw
    sy = y + h / 2 + 8
    if sy + sh > PY1:
        sy = y - h / 2 - sh - 8
    body = ''.join(t(sx + 14, round(sy + 24 + 17 * k, 1), ln, 13, 400, 'var(--serif)') for k, ln in enumerate(lines))
    return (f'<g class="slip" data-n="{l["n"]}" aria-hidden="true">'
            f'<path d="M{sx + 6} {sy + 6:.1f}h{sw}v{sh}h-{sw}z" style="fill:var(--grid-major)"/>'
            f'<path d="M{sx} {sy:.1f}h{sw}v{sh}h-{sw}z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
            + body + t(sx + 14, round(sy + sh - 10, 1), f'AULA {l["n"]} · {l["min"]} MIN DE LEITURA', 12, 600, fill=INK2)
            + '</g>')


def draw(lessons, left, right):
    tabs, slips = [], []
    for side, group, anchors in (('L', left, ANCHOR_L), ('R', right, ANCHOR_R)):
        assert len(group) == len(anchors), f'{side}: {len(group)} lessons for {len(anchors)} moments'
        prev = -1
        for href, y in zip(group, anchors):
            a, h = tab(lessons[href], y, side)
            assert y - h / 2 > prev + 4, f'tabs overlap at {href}'
            prev = y + h / 2
            tabs.append(a); slips.append(slip(lessons[href], y, h, side))
    heads = (t(LX0 + 26, PY0 + 20, 'P1', 12, 700, fill=INK2) + t(LX1 - 26, PY0 + 20, 'ANTES DAS ASSINATURAS', 12, 500, anchor='end', fill=INK2)
             + t(RX0 + 26, PY0 + 20, 'P2', 12, 700, fill=INK2) + t(RX1 - 26, PY0 + 20, 'DEPOIS DELAS', 12, 500, anchor='end', fill=INK2))
    return (f'<svg class="vida" data-family="figure.contrato" viewBox="0 26 {W} {H - 26}" role="group" aria-label="Um contrato aberto sobre a mesa: '
            'a folha da esquerda vai até as assinaturas, a da direita guarda o que acontece depois; cada aula é uma aba na altura do '
            'momento do contrato que ela governa.">'
            + leaf(LX0, LX1) + leaf(RX0, RX1) + spine() + left_leaf() + right_leaf() + heads
            + ''.join(tabs) + ''.join(slips) + '</svg>')


CSS = """
.vida-fig{margin:0}.vida-fig svg{display:block;width:100%;height:auto}
.vida-fig .tab-g path{fill:var(--paper);transition:fill .2s}
.vida-fig .tab-g{transition:transform .25s ease}
.vida-fig .tab:hover .tab-l,.vida-fig .tab:focus-visible .tab-l{transform:translateX(-10px)}
.vida-fig .tab:hover .tab-r,.vida-fig .tab:focus-visible .tab-r{transform:translateX(10px)}
.vida-fig .tab:hover .tab-g path,.vida-fig .tab:focus-visible .tab-g path{fill:var(--paper-2)}
.vida-fig .tab:focus-visible{outline:none}
.vida-fig .tab:focus-visible .tab-g path{stroke:var(--dif);stroke-width:2.4}
.vida-fig figcaption{font:400 15px/1.5 var(--serif);color:var(--ink-2);margin:6px 0 0}
.vida-fig .slip{opacity:0;pointer-events:none;transition:opacity .15s ease}
@media (prefers-reduced-motion:reduce){.vida-fig .tab-g,.vida-fig .slip{transition:none}}
""" + ''.join(f'.vida-fig .vida:has(.tab[data-n="{n:02d}"]:is(:hover,:focus-visible)) .slip[data-n="{n:02d}"]{{opacity:1}}' for n in range(1, 21)) + '\n'


def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    order = [l for u in data['units'] for l in u['lessons']]
    lessons = {l['href']: {'title': l['title'], 'href': l['href'], 'n': f'{i:02d}',
                           'min': front._minutes(SLUG, l['href']) or 15, 'goal': (l.get('reg') or {}).get('does', '')}
               for i, l in enumerate(order, 1)}
    exams = data['reg']['exams']
    assert [e['label'] for e in exams] == ['P1', 'P2'], 'front draws two leaves: P1 and P2'
    left, right = exams[0]['covers'], exams[1]['covers']
    assert left + right == list(lessons), 'exam covers and register order disagree'
    fig = ('<figure class="vida-fig">' + draw(lessons, left, right)
           + '</figure>')
    data['drawing'] = {'html': fig, 'css': CSS}
    data['index'] = 'drawing'   # the open contract is the lesson index: front.py skips the register list
    data['deck'] = ('No Código Civil de 2002, o título dos contratos em geral abre com o art. 421: '
                    'a liberdade contratual é exercida nos limites da função social do contrato.')
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('contratos front: the open contract redrawn; now run tools/fronts/front.py', SLUG)


if __name__ == '__main__':
    main()
