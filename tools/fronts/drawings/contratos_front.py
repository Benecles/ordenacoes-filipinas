#!/usr/bin/env python3
"""Teoria Geral dos Contratos front: the course as one cord, "o vínculo".

  object   one cord of two strands (proposta in house blue, aceitação in ink) that comes in loose, is twisted into one,
           runs the whole course and ends three ways (distrato, resolução, resilição).
  facts    each lesson is a stretch of the cord as long as its reading time; its tag (number, title, articles) stands on
           a stem at its stretch and is the link. P1 | P2 is one orange cut mark at the half (270 of 540 minutes).
           Hover or focus lights the stretch and writes what the lesson trains you to do on the line below the cord.
  hand     ink, hairlines (1px) and the cord (2px); blue where the bond governs, orange only at limits and breaks;
           no boxes, no shadows. Marks (boa-fé band, loop and arras, anchor, loupe, handover, turnbuckle) are drawn in
           the cord's own frame: u along the cord, v across it, so the phone draws the same cord standing up.
usage: contratos_front.py   (rewrites the drawing in tools/fronts/data/teoria-geral-dos-contratos.json; then run front.py)
"""
import html
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import front  # noqa: E402  (reading time: the register's own clock)

SLUG = 'teoria-geral-dos-contratos'
DATA = HERE.parent / 'data' / f'{SLUG}.json'

ARTICLES = {
    'aula-01.html': 'CC 104 · CDC 2º–4º',
    'aula-02.html': 'CC 421 e 421-A',
    'aula-03.html': 'CC 422 · 427–435',
    'aula-04.html': 'CC 417–440 · 462–471',
    'aula-05.html': 'CC 107–109 · 441–461',
    'aula-06.html': 'CC 476–477 · CDC 54',
    'aula-07.html': 'CC 112–114 · 423',
    'aula-08.html': 'CC 299',
    'aula-09.html': 'CC 157 · 317 · 478–480',
    'aula-10.html': 'CC 472–475',
}

AMP = 8          # half-width of the twist
LOOSE = 120        # length of the loose strands before the twist, in px
SANS, SERIF, MONO = 'var(--sans)', 'var(--serif)', 'var(--mono)'


def esc(s):
    return html.escape(str(s), quote=True)


def num(x):
    return f'{x:.1f}'.rstrip('0').rstrip('.')


def wrap(text, width):
    lines, cur = [], ''
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f'{cur} {w}'.strip()
    return lines + ([cur] if cur else [])


def t(x, y, s, size, fam, weight=400, anchor='start', fill='var(--ink)', italic=False, track=0, cls=''):
    st = f'font-family:{fam};font-size:{size}px;font-weight:{weight};fill:{fill}'
    if italic:
        st += ';font-style:italic'
    if track:
        st += f';letter-spacing:{track}em'
    c = f' class="{cls}"' if cls else ''
    return f'<text{c} x="{num(x)}" y="{num(y)}" text-anchor="{anchor}" style="{st}">{esc(s)}</text>'


def smooth(f, a, b, step=2.0):
    n = max(2, int((b - a) / step))
    return [f(a + (b - a) * i / n) for i in range(n + 1)]


def path_of(pts):
    return 'M' + 'L'.join(f'{num(x)} {num(y)}' for x, y in pts)


def cord(centre, off, wl, over_from=0, over_first='B', halo_w=6):
    """Two strands along `centre` (list of (u, v) points). off(s, i) is strand B's signed offset (A mirrors it);
    crossings (off changes sign, past over_from) alternate which strand passes over. Returns svg pieces."""
    pts, s = [], 0.0
    for i, p in enumerate(centre):
        if i:
            s += math.hypot(p[0] - centre[i - 1][0], p[1] - centre[i - 1][1])
        pts.append(s)
    n = len(centre)
    def normal(i):
        a, b = centre[max(i - 1, 0)], centre[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        return -dy / d, dx / d
    A_, B_ = [], []
    for i, (u, v) in enumerate(centre):
        nx, ny = normal(i)
        o = off(pts[i], i)
        B_.append((u + nx * o, v + ny * o))
        A_.append((u - nx * o, v - ny * o))
    # crossings: windows of ±3 samples around a sign change
    cross, prev = [], None
    for i in range(n):
        if pts[i] < over_from:
            prev = None
            continue
        o = off(pts[i], i)
        if prev is not None and (o > 0) != (prev > 0) and abs(o) + abs(prev) > 0.4:
            cross.append(i)
        prev = o
    out = [f'<path class="sa" d="{path_of(A_)}"/>', f'<path class="sb" d="{path_of(B_)}"/>']
    order = [over_first, 'A' if over_first == 'B' else 'B']
    for k, i in enumerate(cross):
        who = order[k % 2]
        if who == 'B':
            continue          # B is already on top: only A needs lifting at its crossings
        lo, hi = max(i - 2, 0), min(i + 3, n)
        seg = path_of(A_[lo:hi])
        out.append(f'<path class="halo" d="{seg}"/><path class="sa" d="{seg}"/>')
    return out, A_, B_, cross


# ------------------------------------------------------------------ the cord scene in its own frame (u along, v across)

HALF = 24      # same lay as the Aula 01 hero rope (tools/figkit/parts/tgc01_hand.py): half-wave 24, amp 8, 2px, paper gap


def rope(u0, u1, amp_at, spans=None, y=0.0):
    """Laid two-strand rope along the u axis: S-curve strand segments that trade places at every crossing; the strand
    that goes under leaves a paper gap. Strand A full blue, strand B lighter blue. Segments carry their lesson (data-n)."""
    n = max(1, round((u1 - u0) / HALF))
    step = (u1 - u0) / n
    out = []
    for k in range(n):
        xa, xb = u0 + k * step, u0 + (k + 1) * step
        xm = (xa + xb) / 2
        sgn = 1 if k % 2 == 0 else -1
        a0, a1 = y - sgn * amp_at(xa), y + sgn * amp_at(xb)
        b0, b1 = y + sgn * amp_at(xa), y - sgn * amp_at(xb)
        def seg(y0, y1):
            return f'M{num(xa)} {num(y0)}C{num(xm)} {num(y0)} {num(xm)} {num(y1)} {num(xb)} {num(y1)}'
        A, B = seg(a0, a1), seg(b0, b1)
        if k % 2 == 0:
            body = f'<path class="rb" d="{B}"/><path class="halo" d="{A}"/><path class="ra" d="{A}"/>'
        else:
            body = f'<path class="ra" d="{A}"/><path class="halo" d="{B}"/><path class="rb" d="{B}"/>'
        n_les = ''
        if spans:
            mid_ = (xa + xb) / 2
            for i, (a, b) in enumerate(spans):
                if a <= mid_ < b:
                    n_les = f' data-n="{i + 1:02d}"'
        out.append(f'<g class="seg"{n_les}>{body}</g>')
    return ''.join(out)


def scene(k, spans, ext):
    """k px per minute. spans: [(u0, u1)] per lesson; ext: extra rope after the last lesson (to the cut)."""
    L = spans[-1][1]
    knot0, knot1 = spans[3][0], spans[3][1]

    def amp_at(u):
        if knot0 < u < knot1:        # the knot left open: the twist slackens
            return AMP + 4 * math.sin(math.pi * (u - knot0) / (knot1 - knot0))
        return AMP

    out = []
    # --- the loose strands that come in (proposta, aceitação) and join the twist
    for sgn, cls in ((-1, 'ra'), (1, 'rb')):
        y0 = sgn * (AMP + 24)
        out.append(f'<path class="{cls} loose" d="M{-LOOSE} {y0}C{-LOOSE * .45} {y0} {-LOOSE * .4} {sgn * AMP} 0 {sgn * AMP}"/>')
    # --- boa-fé: a hairline band along the formation, 03 and 04
    bf0, bf1 = spans[2][0] - 10, spans[3][1] + 10
    out.append(f'<path class="band" d="M{num(bf0)} -22H{num(bf1)}M{num(bf0)} 22H{num(bf1)}M{num(bf0)} -26V-18M{num(bf1)} -26V-18M{num(bf0)} 18V26M{num(bf1)} 18V26"/>')
    out.append(f'<g class="cord">{rope(0, L + ext, amp_at, spans)}</g>')
    stitches = ''.join(f'M{num(u)} -12V12' for u in sorted({s[0] for s in spans[1:]}))
    out.append(f'<path class="stitch" d="{stitches}"/>')
    # --- P1 | P2: one fine orange cut at the half
    cut = spans[5][0]
    out.append(f'<path class="cut" d="M{num(cut)} -34V34"/>')
    # --- loose ends: hollow dots
    for sgn, nm in ((-1, 'a'), (1, 'b')):
        out.append(f'<circle class="dot {nm}" cx="{-LOOSE}" cy="{sgn * (AMP + 24)}" r="4.6"/>')
    return '', ''.join(out), None, L


def marks(spans, side):
    """Small marks beside the cord. side(i) = -1 above / +1 below (the side without the tag)."""
    m = []
    mid = lambda i: (spans[i][0] + spans[i][1]) / 2

    # 02 · liberdade e função social: an orange bracket, the limit on the strand
    u, s = mid(1), side(1)
    a, b = spans[1][0] + 12, spans[1][1] - 12
    m.append(('02', f'<path class="lim" d="M{num(a)} {s * 24}V{s * 31}H{num(b)}V{s * 24}"/>',
              (u, s * 31 + s * 4)))
    # 04 · knots left open: an open loop with the arras tied on as a token
    u, s = mid(3), side(3)
    m.append(('04', f'<path class="loop" d="M{num(u - 20)} {s * 14}C{num(u - 40)} {s * 48} {num(u + 40)} {s * 48} {num(u + 20)} {s * 14}"/>'
                    f'<path class="hair" d="M{num(u)} {s * 37}V{s * 30}"/><circle class="tok" cx="{num(u)}" cy="{s * 26}" r="4.4"/>',
              (u, s * 44)))
    # 05 · what the cord is made of: evicção as the anchor
    u, s = mid(4) - 14, side(4)
    m.append(('05', f'<path class="hair" d="M{num(u)} {s * 14}V{s * 44}M{num(u - 8)} {s * 22}H{num(u + 8)}'
                    f'M{num(u - 13)} {s * 36}Q{num(u - 13)} {s * 48} {num(u)} {s * 48}Q{num(u + 13)} {s * 48} {num(u + 13)} {s * 36}"/>'
                    f'<circle class="ring" cx="{num(u)}" cy="{s * 17}" r="2.6"/>', (u, s * 48)))
    # 06 · two strands pulling together; the exception holds one back
    u, s = mid(5), side(5)
    y = s * 26
    m.append(('06', f'<path class="pull" d="M{num(u - 26)} {y}H{num(u - 5)}M{num(u - 11)} {y - 4}L{num(u - 5)} {y}L{num(u - 11)} {y + 4}'
                    f'M{num(u + 26)} {y}H{num(u + 5)}M{num(u + 11)} {y - 4}L{num(u + 5)} {y}L{num(u + 11)} {y + 4}"/>'
                    f'<path class="lim" d="M{num(u + 26)} {y - 6}V{y + 6}"/>', (u, s * 41)))
    # 07 · reading the knot: a loupe over a crossing
    u, s = mid(6), side(6)
    m.append(('07', f'<circle class="hair" cx="{num(u)}" cy="0" r="15" style="fill:none"/>'
                    f'<path class="hair" d="M{num(u + 10.6)} {s * 10.6}L{num(u + 21)} {s * 21}" style="stroke-width:2"/>', None))
    # 08 · one end handed to a new holder
    u, s = mid(7), side(7)
    m.append(('08', f'<path class="hair" d="M{num(u - 14)} -10Q{num(u - 18)} 0 {num(u - 14)} 10M{num(u + 14)} -10Q{num(u + 18)} 0 {num(u + 14)} 10"/>'
                    f'<circle class="ring" cx="{num(u - 25)}" cy="{s * 24}" r="4.4"/><circle class="solid" cx="{num(u + 25)}" cy="{s * 24}" r="4.4"/>'
                    f'<path class="pull" d="M{num(u - 18)} {s * 28}Q{num(u)} {s * 40} {num(u + 18)} {s * 28}M{num(u + 13)} {s * 29}L{num(u + 18)} {s * 28}L{num(u + 17)} {s * 33}"/>',
              (u, s * 46)))
    # 09 · the cord re-tensioned: a turnbuckle
    u = mid(8)
    m.append(('09', f'<path class="turn" d="M{num(u - 25)} 0L{num(u - 16)} -9H{num(u + 16)}L{num(u + 25)} 0L{num(u + 16)} 9H{num(u - 16)}z"/>'
                    f'<path class="hair" d="M{num(u)} -9V9M{num(u - 36)} 0H{num(u - 29)}M{num(u + 29)} 0H{num(u + 36)}"/>'
                    f'<path class="pull" d="M{num(u - 38)} 0H{num(u - 46)}M{num(u - 43)} -3.5L{num(u - 46)} 0L{num(u - 43)} 3.5'
                    f'M{num(u + 38)} 0H{num(u + 46)}M{num(u + 43)} -3.5L{num(u + 46)} 0L{num(u + 43)} 3.5"/>', None))
    return m


def fan(L, mode, ext):
    """The three ends. Rope runs on to `ext` and is cut (resolução); above it the two strands part and lie loose
    (distrato); below it one strand is released while the other goes on briefly and stops (resilição)."""
    cfg = {'desk': dict(d=100, s=74, dv=(-52, 58)), 'phone': dict(d=66, s=306, dv=(-54, 58))}[mode]
    R = L + ext
    out = []
    # distrato: two loose strands parting from the top of the cord, no knots
    d, dv = cfg['d'], cfg['dv'][0]
    out.append(f'<path class="ra" d="M{num(L - 6)} {-AMP}C{num(L + 30)} {-AMP} {num(L + 40)} {dv - 10} {num(L + d)} {dv - 10}"/>'
               f'<path class="rb" d="M{num(L - 6)} {-AMP + 3}C{num(L + 36)} {-AMP + 3} {num(L + 44)} {dv + 8} {num(L + d - 6)} {dv + 8}"/>')
    ends = [('Distrato', 'desatado', (L + d, dv))]
    # resolução: a clean cut through the cord
    out.append(f'<path class="cutline" d="M{num(R + 3)} -15L{num(R + 9)} 15"/>')
    ends.append(('Resolução', 'cortado', (R + 9, 0)))
    # resilição: one strand released, the other goes on briefly and stops
    s, dv2 = cfg['s'], cfg['dv'][1]
    out.append(f'<path class="ra" d="M{num(L - 6)} {AMP}C{num(L + 12)} {AMP} {num(L + 26)} {AMP + 12} {num(L + 48)} {AMP + 14}"/>'
               f'<path class="rb" d="M{num(L - 6)} {AMP - 3}C{num(L + 24)} {AMP - 3} {num(L + 28)} {dv2 - 22} {num(L + s * .62)} {dv2}"/>')
    ends.append(('Resilição', 'solto', (L + s * .62, dv2)))
    return ''.join(out), ends


def lesson_rows(data):
    lessons = [l for u in data['units'] for l in u['lessons']]
    rows = []
    for i, l in enumerate(lessons, 1):
        m = front._minutes(SLUG, l['href']) or 50
        rows.append({'n': i, 'href': l['href'], 'title': l['title'], 'does': l['reg']['does'], 'min': m,
                     'arts': ARTICLES[l['href']]})
    return rows


def aria(r):
    return f'Aula {r["n"]:02d}: {r["title"]}. {r["does"]} {r["min"]} min de leitura. {r["arts"]}.'


def spans_for(rows, k):
    out, u = [], 0.0
    for r in rows:
        out.append((u, u + r['min'] * k))
        u += r['min'] * k
    return out


def build_desktop(rows):
    W, H, X0, CY = 1100, 520, 162, 212
    k, PITCH = 1.36, 19
    spans = spans_for(rows, k)
    lights, body, wl, L = scene(k, spans, 84)
    side = lambda i: 1 if i % 2 == 0 else -1          # side of the MARK; the tag takes the other
    mk = marks(spans, side)
    fan_svg, ends = fan(L, 'desk', 84)
    g = lambda u, v: (X0 + u, CY + v)
    o = []
    mark_svg = ''.join(m[1] for m in mk)
    o.append(f'<g class="scene" transform="translate({X0} {CY})">{lights}{body}{fan_svg}{mark_svg}</g>')
    # words on the marks and loose ends
    words = []
    words.append(t(X0 - LOOSE, CY - 24 - AMP - 14, 'PROPOSTA', 11.5, SANS, 700, 'middle', 'var(--dif)', track=.1))
    words.append(t(X0 - LOOSE, CY + 24 + AMP + 22, 'ACEITAÇÃO', 11.5, SANS, 700, 'middle', 'var(--ink)', track=.1))
    gl = {'02': 'função social', '04': 'arras', '05': 'evicção', '06': 'exceção', '08': 'cedente → cessionário'}
    for nn, _svg, anchor in mk:
        if nn in gl and anchor:
            u, v = anchor
            s = 1 if v > 0 else -1
            words.append(t(X0 + u, CY + v + (13 if s > 0 else -5), gl[nn], 12.5, SERIF, 400, 'middle', 'var(--ink-2)', italic=True))
    words.append(t(X0 + (spans[2][0] - 10), CY + 40, 'BOA-FÉ', 11.5, SANS, 700, 'start', 'var(--dif)', track=.1))
    # P1 | P2 at the cut
    cx = X0 + spans[5][0]
    words.append(t(cx, CY + 50, 'P1 | P2', 11.5, MONO, 600, 'middle', 'var(--conc)'))
    o.append(''.join(words))
    # ends
    end_words = []
    ex = max(g(eu, ev)[0] for _n, _g, (eu, ev) in ends) + 14
    for nm, gloss, (eu, ev) in ends:
        x, y = g(eu, ev)
        x = ex - 14
        end_words.append(t(x + 14, y - 1, nm.upper(), 11.5, SANS, 700, 'start', 'var(--conc)' if nm == 'Resolução' else 'var(--ink)', track=.08))
        end_words.append(t(x + 14, y + 14, gloss, 13, SERIF, 400, 'start', 'var(--ink-2)', italic=True))
    # tags
    tags, does = [], []
    for i, r in enumerate(rows):
        a, b = spans[i]
        u = (a + b) / 2
        x = X0 + u
        sd = -side(i)               # tag side: -1 above
        STEM = 74 if (i // 2) % 2 == 0 else 134
        title = wrap(r['title'], 21)
        lines = [('AULA ' + f'{r["n"]:02d}', 12, SANS, 700, 'lab-n', .1)] + [(ln, 17, SERIF, 500, 'lab-t', 0) for ln in title] \
            + [(r['arts'], 12, MONO, 400, 'lab-a', 0)]
        txt = []
        if sd < 0:
            y = CY - STEM
            for kline in reversed(lines):
                txt.append((kline, y))
                y -= PITCH if kline[4] != 'lab-n' else PITCH
            txt = txt[::-1]
            stem = f'M{num(x)} {CY - 16}V{CY - STEM + 6}'
            hit = (x - 72, y + 4, 144, CY - 10 - (y + 4))
        else:
            y = CY + STEM + 12
            for kline in lines:
                txt.append((kline, y))
                y += PITCH
            stem = f'M{num(x)} {CY + 16}V{CY + STEM - 2}'
            hit = (x - 72, CY + 10, 144, y - CY - 10 - 6)
        svg_t = ''.join(t(x, yy, ln[0], ln[1], ln[2], ln[3], 'middle', 'var(--ink-2)' if ln[4] != 'lab-t' else 'var(--ink)', track=ln[5], cls=ln[4])
                        for ln, yy in txt)
        tags.append(
            f'<a class="tag" href="{r["href"]}" data-n="{r["n"]:02d}" aria-label="{esc(aria(r))}">'
            f'<rect class="hit" x="{num(hit[0])}" y="{num(hit[1])}" width="{num(hit[2])}" height="{num(hit[3])}"/>'
            f'<path class="stem" d="{stem}"/>{svg_t}</a>')
        does.append(
            f'<g class="does" data-n="{r["n"]:02d}" aria-hidden="true">'
            + t(W / 2, H - 46, f'AULA {r["n"]:02d} · {r["title"]} · {r["min"]} MIN', 12, SANS, 700, 'middle', 'var(--dif)', track=.06)
            + t(W / 2, H - 22, r['does'], 16, SERIF, 400, 'middle', 'var(--ink)', italic=True) + '</g>')
    idle = ('<g class="idle" aria-hidden="true">' + t(W / 2, H - 30, 'Obligatio est iuris vinculum', 17, SERIF, 400, 'middle', 'var(--ink-2)', italic=True)
            + t(W / 2 + 142, H - 30, 'Inst. 3.13', 11.5, MONO, 400, 'start', 'var(--ink-2)') + '</g>')
    ends_g = f'<g class="tag-ends">{"".join(end_words)}</g>'
    # the end words belong to the last tag: put them inside its link
    tags[-1] = tags[-1].replace('</a>', ends_g + '</a>')
    return (f'<svg class="cord-svg" viewBox="0 0 {W} {H}" role="group" aria-label="O vínculo: um cordão de duas fios, proposta e aceitação, '
            f'torcidos em um só; as dez aulas são os trechos do cordão, cada um do tamanho do seu tempo de leitura, e o cordão termina em distrato, '
            f'resolução ou resilição.">' + ''.join(o) + ''.join(tags) + idle + ''.join(does) + '</svg>')


def build_phone(rows):
    W, OX, OY, k, PITCH = 360, 104, 168, 1.7, 17
    spans = spans_for(rows, k)
    lights, body, wl, L = scene(k, spans, 120)
    mk = marks(spans, lambda i: 1)
    fan_svg, ends = fan(L, 'phone', 120)
    H = int(OY + L + 190)
    # in rotate(90) the local (u, v) lands at (OX - v, OY + u): v>0 is to the left
    o = []
    mark_svg = ''.join(m[1] for m in mk if m[0] not in ('09',)) + ''.join(m[1] for m in mk if m[0] == '09')
    o.append(f'<g class="scene" transform="translate({OX} {OY}) rotate(90)">{lights}{body}{fan_svg}{mark_svg}</g>')
    G = lambda u, v: (OX - v, OY + u)
    words = []
    px, py = G(-LOOSE, -(AMP + 24))
    words.append(t(px + 8, py - 12, 'PROPOSTA', 11.5, SANS, 700, 'start', 'var(--dif)', track=.1))
    px, py = G(-LOOSE, AMP + 24)
    words.append(t(px - 30, py - 12, 'ACEITAÇÃO', 11.5, SANS, 700, 'start', 'var(--ink)', track=.1))
    gl = {'02': 'função social', '04': 'arras', '05': 'evicção', '06': 'exceção', '08': 'cedente'}
    for nn, _s, anchor in mk:
        if nn in gl and anchor:
            u, v = anchor
            x, y = G(u, v)
            words.append(t(x - 6, y + 4, gl[nn], 12.5, SERIF, 400, 'end', 'var(--ink-2)', italic=True))
    bx, by = G(spans[2][0] + 8, 0)
    words.append(t(bx - 30, by + 18, 'BOA-FÉ', 11.5, SANS, 700, 'end', 'var(--dif)', track=.1))
    cx, cy = G(spans[5][0], 0)
    words.append(t(cx - 40, cy + 4, 'P1 | P2', 11.5, MONO, 600, 'end', 'var(--conc)'))
    o.append(''.join(words))
    tags, end_words = [], []
    for nm, gloss, (eu, ev) in ends:
        x, y = G(eu, ev)
        end_words.append(t(x + 14, y + 1, nm.upper(), 11.5, SANS, 700, 'start', 'var(--conc)' if nm == 'Resolução' else 'var(--ink)', track=.08))
        end_words.append(t(x + 14, y + 16, gloss, 13, SERIF, 400, 'start', 'var(--ink-2)', italic=True))
    TX = OX + 44
    for i, r in enumerate(rows):
        a, b = spans[i]
        yc = OY + (a + b) / 2
        title = wrap(r['title'], 27)
        lines = [(f'AULA {r["n"]:02d} · {r["min"]} MIN', 11.5, SANS, 700, 'lab-n', .1)] + [(ln, 15, SERIF, 500, 'lab-t', 0) for ln in title] \
            + [(r['arts'], 11.5, MONO, 400, 'lab-a', 0)]
        y = yc - (len(lines) - 1) * PITCH / 2 + 4
        svg_t = ''
        for ln in lines:
            svg_t += t(TX, y, ln[0], ln[1], ln[2], ln[3], 'start', 'var(--ink-2)' if ln[4] != 'lab-t' else 'var(--ink)', track=ln[5], cls=ln[4])
            y += PITCH
        h = len(lines) * PITCH + 6
        tags.append(
            f'<a class="tag" href="{r["href"]}" data-n="{r["n"]:02d}" aria-label="{esc(aria(r))}">'
            f'<rect class="hit" x="{OX + 14}" y="{num(yc - h / 2)}" width="{W - OX - 14}" height="{num(h)}"/>'
            f'<path class="stem" d="M{OX + 16} {num(yc)}H{TX - 8}"/>{svg_t}</a>')
    tags[-1] = tags[-1].replace('</a>', f'<g class="tag-ends">{"".join(end_words)}</g></a>')
    return (f'<svg class="cord-svg" viewBox="0 0 {W} {H}" role="group" aria-label="O vínculo: um cordão de duas fios, proposta e aceitação, '
            f'torcidos em um só; as dez aulas são os trechos do cordão, e ele termina em distrato, resolução ou resilição.">'
            + ''.join(o) + ''.join(tags) + '</svg>')


CSS = """
header.front-title { padding-block: clamp(20px, 3vh, 34px) 6px; }
header.front-title h1 { max-width: none; font-size: clamp(34px, 4.25vw, 58px); margin-block: 10px 8px; }
header.front-title .front-deck { max-width: 68ch; }
.front-drawing { padding-top: 0; padding-bottom: 14px; }
.cord-fig { margin: 0; padding: 4px 0 0; border: 0; box-shadow: none; }
.cord-svg { display: block; width: 100%; height: auto; overflow: visible; }
.cord-fig .ra, .cord-fig .rb { fill: none; stroke: var(--dif); stroke-width: 2; stroke-linecap: round; }
.cord-fig .rb { opacity: .5; }
.cord-fig .hair, .cord-fig .ring, .cord-fig .turn, .cord-fig .stem, .cord-fig .stitch { fill: none; stroke: var(--ink); stroke-width: 1; }
.cord-fig .stitch { stroke: var(--ink-2); opacity: .55; }
.cord-fig .ring { fill: var(--paper); }
.cord-fig .turn { fill: var(--paper); stroke-width: 1.4; }
.cord-fig .solid { fill: var(--dif); stroke: var(--dif); stroke-width: 1.4; }
.cord-fig .tie { fill: var(--dif); stroke: var(--paper); stroke-width: 2; }
.cord-fig .dot { fill: var(--paper); stroke-width: 2; }
.cord-fig .dot.a { stroke: var(--dif); }
.cord-fig .dot.b { stroke: var(--dif); stroke-opacity: .5; }
.cord-fig .tok { fill: var(--paper); stroke: var(--ink); stroke-width: 1.4; }
.cord-fig .loop { fill: none; stroke: var(--dif); stroke-width: 1; }
.cord-fig .pull { fill: none; stroke: var(--dif); stroke-width: 1.3; stroke-linecap: round; stroke-linejoin: round; }
.cord-fig .lim, .cord-fig .cutline { fill: none; stroke: var(--conc); stroke-width: 1.4; stroke-linecap: round; }
.cord-fig .cutline { stroke-width: 2; }
.cord-fig .cut { fill: none; stroke: var(--conc); stroke-width: 1; }
.cord-fig .band { fill: none; stroke: var(--dif); stroke-width: 1; opacity: .7; }
.cord-fig .tag { cursor: pointer; outline: none; }
.cord-fig .tag .hit { fill: transparent; stroke: none; pointer-events: all; }
.cord-fig .tag .stem { transition: stroke .2s; }
.cord-fig .tag text { transition: fill .2s; }
.cord-fig .tag:is(:hover, :focus-visible) .stem { stroke: var(--dif); stroke-width: 1.6; }
.cord-fig .tag:is(:hover, :focus-visible) :is(.lab-n, .lab-t, .lab-a) { fill: var(--dif) !important; }
.cord-fig .tag:focus-visible .lab-t { text-decoration: underline; text-underline-offset: 3px; }
.cord-fig .does { opacity: 0; transition: opacity .2s ease; pointer-events: none; }
.cord-fig .idle { transition: opacity .2s ease; }
.cord-fig:has(.tag:is(:hover, :focus-visible)) .idle { opacity: 0; }
/* below the drawing, the same hand: hairline-ruled sections, no boxes, no shadows */
.front-exam-card, .front-exam .exam-card { border: 0 !important; box-shadow: none !important; background: transparent !important; padding: 18px 0 0 !important; border-top: 1px solid var(--ink) !important; width: 100% !important; max-width: none !important; }
.front-exam-content { display: block; }
.front-exam-card h2 { font: 700 23px/1.15 var(--sans); margin: 0 0 8px; }
.vida-review { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 48px; max-width: 820px; }
.vida-review .front-review { font-size: 16px; }
.vida-resume { margin-top: 12px; }
@media (max-width: 560px) { .vida-review { grid-template-columns: minmax(0, 1fr); } }
@media (prefers-reduced-motion: reduce) { .cord-fig * { transition: none !important; } }
""" + ''.join(
    f'.cord-fig:has(.tag[data-n="{n:02d}"]:is(:hover,:focus-visible)) .seg[data-n="{n:02d}"] :is(.ra,.rb){{stroke-width:3.4;opacity:1}}'
    f'.cord-fig:has(.tag[data-n="{n:02d}"]:is(:hover,:focus-visible)) .does[data-n="{n:02d}"]{{opacity:1}}\n' for n in range(1, 11))


def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    rows = lesson_rows(data)
    assert [r['href'] for r in rows] == [f'aula-{i:02d}.html' for i in range(1, 11)]
    desk = '<figure id="aulas" class="cord-fig" aria-label="Índice das aulas">' + build_desktop(rows) + '</figure>'
    phone = '<figure class="cord-fig phone-fig" aria-label="Índice das aulas">' + build_phone(rows) + '</figure>'
    data['drawing'] = {'html': desk, 'phone_html': phone, 'css': CSS}
    data['index'] = 'drawing'
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Updated the contract cord in {DATA.name}')


if __name__ == '__main__':
    main()
