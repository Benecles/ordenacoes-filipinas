"""Aula 04 instruments in the course's hand (DIRECTION.md): no boxes. Choices are hollow marks on a hairline; the answer
is a verdict, two serif lines and a hairline above them. Selection is styled by the page ([data-opt][aria-pressed=true]).
Helpers only (no build)."""
from . import svg as S
from .tgc01_hand import cord, rule, mark, hit

W = 1080
T = S.text


def dot(x, y, col=S.INK, r=6.5, dashed=False):
    return S.circle(x, y, r, fill=S.PAPER, stroke=col, stroke_width=1.8, stroke_dasharray='3 3' if dashed else None)


def label(x, y, s, size=14, **kw):
    return T(x, y, s, size=size, family=S.SANS, **kw)


def frame(title, choices, answers, base, over, y_choice, y_ans, H):
    """choices: [(key, label)]; answers: {key: (verdict, line1, line2, ok)}; base/over: svg strings."""
    o = [T(30, 28, title.upper(), size=12, family=S.SANS, weight=600, letter_spacing='0.08em', fill=S.INK2)] + list(base)
    n = len(choices)
    gap = 28 if n < 5 else 14
    w = (W - 60 - gap * (n - 1)) / n
    fs, fw = (14, 600) if n < 5 else (12, 500)
    for i, (k, lab) in enumerate(choices):
        x = 30 + i * (w + gap)
        o.append(f'<g data-opt="{k}" tabindex="0" role="button" aria-pressed="{"true" if i == 0 else "false"}" aria-label="{S.esc(lab)}">'
                 + hit(x, y_choice - 22, w, 44)
                 + S.circle(x + 6, y_choice - 1, 5.5, fill=S.PAPER, stroke=S.INK, stroke_width=1.6)
                 + T(x + 18, y_choice + 4, lab, size=fs, family=S.SANS, weight=fw)
                 + S.line(x, y_choice + 16, x + w, y_choice + 16, stroke=S.INK2, stroke_width=1) + '</g>')
    for i, (k, lab) in enumerate(choices):
        verdict, l1, l2, ok = answers[k]
        col = S.DIF if ok else S.CONC
        o.append(f'<g data-ans="{k}"' + ('' if i == 0 else ' display="none"') + '>')
        o += over.get(k, [])
        o.append(S.line(30, y_ans - 24, 230, y_ans - 24, stroke=col, stroke_width=2))
        o.append(T(30, y_ans + 8, verdict, size=21, family=S.SANS, weight='650', fill=col))
        o.append(T(30, y_ans + 38, l1, size=15, family=S.SERIF))
        if l2:
            o.append(T(30, y_ans + 60, l2, size=15, family=S.SERIF))
        o.append('</g>')
    return o
