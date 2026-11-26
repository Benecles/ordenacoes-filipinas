"""Aula 04 instruments: shared frame (choices, answer box) for the four tgc04 instrument parts.
Not a part itself (no build)."""
from . import svg as S

W = 1080


def dot(x, y, col=S.INK, r=8, dashed=False):
    return S.circle(x, y, r, fill=S.PAPER, stroke=col, stroke_width=2.2, stroke_dasharray='3 3' if dashed else None)


def label(x, y, s, size=14, **kw):
    return S.text(x, y, s, size=size, family=S.SANS, **kw)


def frame(title, choices, answers, base, over, y_choice, y_box, H):
    """choices: [(key, label)]; answers: {key: (verdict, line1, line2, ok)}; base: list of svg strings;
    over: {key: [svg strings]}."""
    o = [S.text(24, 28, title, size=13, family=S.MONO)] + list(base)
    n = len(choices)
    w = (W - 60 - 12 * (n - 1)) / n
    for i, (k, lab) in enumerate(choices):
        x = 30 + i * (w + 12)
        o.append(f'<g data-opt="{k}" tabindex="0" role="button" aria-label="{S.esc(lab)}">')
        o.append(S.rect(x, y_choice, w, 44, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
        o.append(S.text(x + w / 2, y_choice + 27, lab, size=14, family=S.SANS, weight='600', anchor='middle'))
        o.append('</g>')
    for i, (k, lab) in enumerate(choices):
        verdict, l1, l2, ok = answers[k]
        col = S.DIF if ok else S.CONC
        o.append(f'<g data-ans="{k}"' + ('' if i == 0 else ' display="none"') + '>')
        o += over.get(k, [])
        o.append(S.rect(30, y_box, W - 60, 104, fill=S.PAPER, stroke=col, stroke_width=2))
        o.append(S.text(54, y_box + 38, verdict, size=21, family=S.SANS, weight='650', fill=col))
        o.append(S.text(54, y_box + 66, l1, size=15, family=S.SERIF))
        if l2:
            o.append(S.text(54, y_box + 88, l2, size=15, family=S.SERIF))
        o.append('</g>')
    return o
