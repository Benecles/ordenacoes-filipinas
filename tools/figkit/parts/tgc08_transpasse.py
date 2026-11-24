"""Tracing registration of the whole position, in three reading states.

Luis Renato Ferreira da Silva, PDF pp. 3–4: the same contractual relation
continues with a successor; rights, duties and defences travel together.
The outlines and registration crosses are drawing tools, not case facts.
"""
from . import svg as S


def build(p):
    state = int(p.get('state', 1))
    if state not in (1, 2, 3):
        raise ValueError('state must be 1, 2 or 3')
    out = []

    def path(d, color=S.MUTED, **kw):
        out.append(S.path(d, fill='none', stroke=color, stroke_width=1.5, **kw))

    def text(x, y, words, **kw):
        out.append(S.text(x, y, words, size=18, family=S.SERIF, **kw))

    text(195, 24, 'O mesmo contrato', anchor='middle')
    # Fixed drawing sheet and its registration marks.
    path('M24 46 H344 V276 H24 Z')
    for x, y in ((38, 60), (330, 60), (38, 262), (330, 262)):
        path(f'M{x-5} {y} H{x+5} M{x} {y-5} V{y+5}')
    for y, word in ((106, 'direitos'), (164, 'deveres'), (222, 'defesas')):
        path(f'M55 164 H78 V{y} H304')
        text(115, y-10, word)
        out.append(S.circle(304, y, 5, fill=S.PAPER, stroke=S.MUTED))
    # The original holder is withdrawn only in the completed transfer.
    path('M290 84 H318 V244 H290', stroke_dasharray='3 4',
         opacity='.18' if state == 3 else '1')
    text(195, 307, 'cedente · posição original', anchor='middle',
         fill=S.MUTED if state == 3 else S.INK)
    # One sheet carries every contact: no independent assignments.
    dx, dy = (20, 15) if state == 1 else (0, 0)
    out.append(f'<g transform="translate({dx} {dy})" opacity="{.45 if state == 1 else 1}">')
    path('M38 60 H330 V262 H38 Z', S.DIF)
    for y in (106, 164, 222):
        path(f'M55 164 H78 V{y} H304', S.DIF)
        out.append(S.circle(304, y, 5, fill=S.PAPER, stroke=S.DIF, stroke_width=2))
    path('M284 78 H324 V250 H284', S.DIF)
    out.append('</g>')
    words = ('cessionário · fora de registro', 'anuência do cedido', 'cessionário · posição recebida')
    text(195, 343, words[state-1], anchor='middle', fill=S.CONC if state == 2 else S.DIF)
    return ('<svg viewBox="0 0 390 366" role="img" aria-label="' +
            S.esc(words[state-1]) + '">' + ''.join(out) + '</svg>', [])
