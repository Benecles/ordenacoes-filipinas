"""Three-party assembly for cessão da posição contratual.

Luis Renato Ferreira da Silva, PDF pp. 3–4 and 6–7: the cedente and
cessionário agree, while the cedido's consent completes the substitution.
The same contract continues with the cessionário in the cedente's place.
"""
from . import svg as S


def build(p):
    state = int(p.get('state', 1))
    if state not in (1, 2, 3):
        raise ValueError('state must be 1, 2 or 3')
    label = S.esc(p.get('label', 'Cedente, cessionário e cedido'))
    out = []

    def path(d, color=S.INK, width=1.7, **kw):
        out.append(S.path(d, fill='none', stroke=color, stroke_width=width, **kw))

    def line(x, y, xx, yy, color=S.INK, width=1.5, **kw):
        out.append(S.line(x, y, xx, yy, stroke=color, stroke_width=width, **kw))

    def dot(x, y, r=8, color=S.INK, hollow=True):
        out.append(S.circle(x, y, r, fill=S.PAPER if hollow else color,
                            stroke=color, stroke_width=1.8))

    def text(x, y, words, **kw):
        kw.setdefault('size', 19)
        kw.setdefault('family', S.SANS)
        out.append(S.text(x, y, words, **kw))

    text(420, 28, 'o mesmo contrato-base', size=19, anchor='middle')
    # The contract's two places and its connecting line stay fixed in every state.
    if state < 3:
        left_name = 'cedente'
        left_color = S.INK
    else:
        left_name = 'cessionário'
        left_color = S.DIF
    line(190, 205, 650, 205, S.INK, 2.3)
    dot(190, 205, 9, left_color)
    dot(650, 205, 9, S.INK)
    text(190, 244, left_name, anchor='middle', fill=left_color)
    text(650, 244, 'cedido · permanece', anchor='middle')
    # At first, the prospective holder is outside the relation.
    if state == 1:
        dot(420, 94, 8, S.MUTED)
        text(420, 72, 'cessionário · fora', anchor='middle', fill=S.INK2)
        path('M420 107 V174', S.MUTED, 1.4, stroke_dasharray='4 5')
        text(420, 326, 'dois contratantes na relação de origem', anchor='middle', fill=S.INK2)
    elif state == 2:
        # A second line records the transfer agreement; the blocked square
        # shows that the relation still awaits the cedido's assent.
        line(190, 105, 420, 105, S.INK2, 1.8)
        dot(190, 105, 7, S.INK2)
        dot(420, 105, 7, S.DIF)
        line(190, 113, 190, 195, S.MUTED, 1.2, stroke_dasharray='3 4')
        text(190, 78, 'cedente', anchor='middle', fill=S.INK2)
        text(420, 78, 'cessionário', anchor='middle', fill=S.DIF)
        text(305, 137, 'ajuste da transferência', anchor='middle', fill=S.INK2)
        line(650, 105, 650, 169, S.CONC, 1.8)
        out.append(S.rect(641, 160, 18, 18, fill=S.PAPER,
                          stroke=S.CONC, stroke_width=2))
        text(650, 144, 'anuência pendente', anchor='middle', fill=S.CONC)
        text(420, 326, 'o ajuste entre dois ainda aguarda quem permanece', anchor='middle', fill=S.INK2)
    else:
        # The departed holder remains as a pale trace; the newcomer now
        # occupies the original endpoint and the cedido stays in place.
        path('M190 218 V268', S.MUTED, 1.4, stroke_dasharray='3 4')
        out.append(S.circle(190, 282, 8, fill=S.PAPER, stroke=S.MUTED,
                            stroke_width=1.6, stroke_dasharray='3 4'))
        text(190, 320, 'cedente · sai', anchor='middle', fill=S.INK2)
        out.append(S.rect(641, 160, 18, 18, fill=S.CONC,
                          stroke=S.CONC, stroke_width=1.8))
        text(650, 144, 'consente', anchor='middle', fill=S.CONC)
        text(420, 351, 'cessionário ocupa a posição · o contrato continua',
             anchor='middle', fill=S.DIF)
    # A drafting line and registration marks make the relation read as one
    # continuing instrument rather than three free-standing person cards.
    path('M112 185 H164 M676 185 H728', S.MUTED, 1.0)
    for x in (112, 728):
        line(x, 179, x, 191, S.MUTED, 1)
    return (f'<svg viewBox="0 0 840 360" role="img" aria-label="{label}">'
            + ''.join(out) + '</svg>', [])
