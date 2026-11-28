"""Aula 03 helpers in the course hand (DIRECTION.md): ink on paper, nothing boxed. Not a part (no build).

Imports the shared hand from tgc01_hand (never edited) and adds what Aula 03's drawings need: a ruled sheet with no
frame, an envelope without a box, two loose strands, and the instrument frame (choices as ruled text, answer as a
vertical rule with its verdict)."""
from __future__ import annotations
from . import svg as S
from . import tgc01_hand as H

T = S.text
W = 1080


def sheet(x, y, w, rows=5, col=S.INK, step=15, ragged=True):
    """A written sheet: a 2px head rule and hairline lines of writing; no frame."""
    o = [H.rule(f'M{x},{y} H{x + w}', col, 2.0)]
    for i in range(rows):
        e = w * (0.72 if (ragged and i % 3 == 2) else 1.0)
        o.append(H.rule(f'M{x},{y + 16 + step * i} H{x + e:.1f}', S.INK2 if col == S.INK else col, 1.0))
    return o


def envelope(x, y, w=150, h=90, col=S.INK):
    """An envelope as its flap and fold lines; no outline box."""
    return [H.rule(f'M{x},{y} L{x + w / 2},{y + h * .55} L{x + w},{y}', col, 1.6),
            H.rule(f'M{x},{y + h} L{x + w * .38},{y + h * .38} M{x + w},{y + h} L{x + w * .62},{y + h * .38}', col, 1.0),
            H.rule(f'M{x},{y} V{y + h} H{x + w} V{y}', col, 1.0)]


def strands(x0, x1, y, gap=26, col=S.DIF, dashed=None, w=1.6):
    """Two loose strands that do not meet (a bond not yet formed)."""
    return [H.rule(f'M{x0},{y - gap / 2} C{x0 + (x1 - x0) * .4},{y - gap / 2 - 5} {x0 + (x1 - x0) * .6},{y - gap / 2 + 5} {x1},{y - gap / 2}', col, w, dashed),
            H.rule(f'M{x0},{y + gap / 2} C{x0 + (x1 - x0) * .4},{y + gap / 2 + 5} {x0 + (x1 - x0) * .6},{y + gap / 2 - 5} {x1},{y + gap / 2}', col, w, dashed)]


def cut(x, y, h=46, col=S.CONC):
    """The orange cut mark: a 2px rule with hairline serifs."""
    return [H.rule(f'M{x},{y - h / 2} V{y + h / 2}', col, 2.0), H.rule(f'M{x - 6},{y - h / 2} H{x + 6} M{x - 6},{y + h / 2} H{x + 6}', col, 1.0)]


def arrow(x1, x2, y, col=S.INK, w=2.0, dashed=None):
    d = 1 if x2 > x1 else -1
    return [H.rule(f'M{x1},{y} H{x2}', col, w, dashed), H.rule(f'M{x2 - 9 * d},{y - 5} L{x2},{y} L{x2 - 9 * d},{y + 5}', col, w)]


def strike(x, y, r=9, col=S.CONC):
    return [H.rule(f'M{x - r},{y - r} L{x + r},{y + r} M{x - r},{y + r} L{x + r},{y - r}', col, 2.0)]


def frame(title, choices, answers, base, over, y_choice, y_box, H_):
    """choices: [(key, label)]; answers: {key: (verdict, line1, line2, ok)}; base/over: svg strings.
    Choices are ruled text; the answer sits under a vertical rule of its colour."""
    o = [T(24, 28, title, size=13, family=S.MONO)] + list(base)
    n = len(choices)
    w = (W - 40) / n
    for i, (k, lab) in enumerate(choices):
        x = 20 + i * w
        o.append(f'<g data-opt="{k}" tabindex="0" role="button" aria-label="{S.esc(lab)}">')
        o.append(H.hit(x, y_choice - 8, w - 10, 50))
        o.append(H.rule(f'M{x + 10},{y_choice + 30} H{x + w - 20}', S.INK2, 1.0))
        o.append(T(x + w / 2 - 5, y_choice + 18, lab, size=14, family=S.SANS, weight=600, anchor='middle'))
        o.append('</g>')
    for i, (k, lab) in enumerate(choices):
        verdict, l1, l2, ok = answers[k]
        col = S.DIF if ok else S.CONC
        o.append(f'<g data-ans="{k}"' + ('' if i == 0 else ' display="none"') + '>')
        o += over.get(k, [])
        o.append(H.rule(f'M30,{y_box} V{y_box + (92 if l2 else 70)}', col, 2.0))
        o.append(T(54, y_box + 24, verdict, size=21, family=S.SANS, weight=650, fill=col))
        o.append(T(54, y_box + 52, l1, size=15.5, family=S.SERIF))
        if l2:
            o.append(T(54, y_box + 76, l2, size=15.5, family=S.SERIF))
        o.append('</g>')
    return o
