"""Aula 02 chapter instruments in the course's hand (DIRECTION.md): no boxes. Choices are hollow marks on a hairline;
the answer is a verdict, two serif lines and a hairline above them. Selection is styled by the page
([data-opt][aria-pressed=true]). Helpers only (no build)."""
from . import svg as S
from .tgc01_hand import cord, rule, mark, name, gloss, art, bracket, hit

W = 1080
T = S.text


def frame(choices, answers, base, over, y_choice, y_ans, H):
    """choices: [(key, label)]; answers: {key: (verdict, line1, line2, ok)}; base/over: svg strings."""
    o = list(base)
    n = len(choices)
    w = (W - 60 - 28 * (n - 1)) / n
    for i, (k, lab) in enumerate(choices):
        x = 30 + i * (w + 28)
        o.append(f'<g data-opt="{k}" tabindex="0" role="button" aria-pressed="{"true" if i == 0 else "false"}" aria-label="{S.esc(lab)}">'
                 + hit(x, y_choice - 22, w, 44)
                 + S.circle(x + 6, y_choice - 1, 5.5, fill=S.PAPER, stroke=S.INK, stroke_width=1.6)
                 + T(x + 20, y_choice + 4, lab, size=14, family=S.SANS, weight='600')
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
