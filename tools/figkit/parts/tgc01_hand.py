"""Shared hand for Aula 01 drawings (DIRECTION.md, o vínculo): ink on paper, nothing boxed.
Helpers only (no build): the two-strand cord, named marks, engraver's labels, hairline brackets."""
from __future__ import annotations
import math
from . import svg as S

T = S.text


def cord(x0, x1, y, amp=8.0, half=24, taper=34, col=S.DIF, w=2.0, **_):
    """A laid two-strand rope: diagonal strand segments that trade places at every crossing; the strand that goes
    under leaves a paper gap at the crossing. Strand A in full blue, strand B in a lighter blue. Ends tie into the marks."""
    out, k, x = [], 0, x0
    n = max(1, int((x1 - x0) // half))
    step = (x1 - x0) / n
    def amp_at(xx):
        return amp * max(0.0, min(1.0, (xx - x0) / taper, (x1 - xx) / taper))
    for k in range(n):
        xa, xb = x0 + k * step, x0 + (k + 1) * step
        sgn = 1 if k % 2 == 0 else -1
        ya0, ya1 = y - sgn * amp_at(xa), y + sgn * amp_at(xb)   # strand A runs one way, B the other
        yb0, yb1 = y + sgn * amp_at(xa), y - sgn * amp_at(xb)
        xm = (xa + xb) / 2
        def seg(c, y0, y1, ww, col2, op=None):
            return S.path(f'M{xa:.1f},{y0:.1f} C{xm:.1f},{y0:.1f} {xm:.1f},{y1:.1f} {xb:.1f},{y1:.1f}', fill='none',
                          stroke=c, stroke_width=ww, stroke_linecap='round', opacity=op)
        # over strand alternates: A over on even segments, B over on odd
        under = (seg(S.DIF, yb0, yb1, w, S.DIF, '0.5') if k % 2 == 0 else seg(S.DIF, ya0, ya1, w, S.DIF))
        over = (seg(S.DIF, ya0, ya1, w, S.DIF) if k % 2 == 0 else seg(S.DIF, yb0, yb1, w, S.DIF, '0.5'))
        halo = (seg(S.PAPER, ya0, ya1, w + 3.5, S.PAPER) if k % 2 == 0 else seg(S.PAPER, yb0, yb1, w + 3.5, S.PAPER))
        out += [under, halo, over]
    return ''.join(out)


def rule(d, col=S.INK, w=1.0, dash=None):
    return S.path(d, fill='none', stroke=col, stroke_width=w, stroke_dasharray=dash,
                  stroke_linecap='round', stroke_linejoin='round')


def mark(x, y, col=S.INK, r=6.5, solid=False):
    return S.circle(x, y, r, fill=col if solid else S.PAPER, stroke=col, stroke_width=1.8)


def name(x, y, s, col=S.INK, anchor=None, size=12.5):
    """Sans small-caps name of a party or stage."""
    return T(x, y, s.upper(), size=size, family=S.SANS, weight=600, fill=col, anchor=anchor, letter_spacing='0.08em')


def gloss(x, y, s, col=S.INK2, anchor=None, size=13):
    """Serif italic gloss."""
    return T(x, y, s, size=size, family=S.SERIF, fill=col, anchor=anchor, font_style='italic')


def art(x, y, s, col=S.INK2, anchor=None, size=11.5):
    return T(x, y, s, size=size, family=S.MONO, fill=col, anchor=anchor)


def bracket(x1, x2, y, up=True, col=S.INK2):
    d = 5 if up else -5
    return rule(f'M{x1},{y + d} V{y} H{x2} V{y + d}', col, 1.0)


def wire(key, label, body):
    return (f'<g data-thread="{key}" tabindex="0" role="button" aria-label="{S.esc(label)}" aria-pressed="false">'
            + ''.join(body) + '</g>')


def hit(x, y, w, h):
    """Invisible click target (fill=none + pointer-events=all so boxes.cjs skips it)."""
    return S.rect(x, y, w, h, fill='none', stroke='none', pointer_events='all')
