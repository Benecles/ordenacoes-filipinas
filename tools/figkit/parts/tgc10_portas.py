"""Two doors for CC 474: each has two bolts. The first is already drawn back (the legal prerequisite is
present: a specific clause, a definitive breach); the second is engaged until the reader turns its key
(the creditor's declaration; the constitutive judgment). Buttons operate distinct locks; they never
switch drawing versions. No factual parameters.
Sources: Terra/Nanni pp.145-146, 157-160; roteiro pp.20-22; CC 474.
"""
from . import svg as S


def _door():
    fx, fy, fw, fh = 104, 62, 176, 226
    out = []
    # the doorway: jamb, the opening behind the leaf, the sill
    out.append(S.rect(fx, fy, fw, fh, fill='none', stroke=S.INK, stroke_width=3))
    out.append(S.rect(fx + 8, fy + 8, fw - 16, fh - 16, fill=S.PAPER, stroke=S.INK, stroke_width=1))
    out += S.hatch(fx + 9, fy + 9, fw - 18, fh - 18, step=14, stroke=S.GRID, stroke_width=1)
    out.append(S.line(14, fy + fh, 300, fy + fh, stroke=S.INK, stroke_width=1.5))
    # the leaf: hinged on the right, so it closes toward the hinge side when opened
    lx, ly, lw, lh = fx + 8, fy + 8, fw - 16, fh - 16
    leaf = S.rect(lx, ly, lw, lh, fill=S.PAPER2, stroke=S.INK, stroke_width=1.5)
    for cx in (lx + 20, lx + 20 + 66 + 12):
        for cy in (ly + 16, ly + 16 + 92 + 12):
            leaf += S.rect(cx, cy, 66, 92, fill='none', stroke=S.INK, stroke_width=1.2)
    for hy in (ly + 14, ly + lh / 2 - 12, ly + lh - 38):
        leaf += S.rect(lx + lw - 8, hy, 10, 24, fill=S.PAPER, stroke=S.INK, stroke_width=1.5)
    leaf += S.circle(lx + 11, ly + lh / 2, 4, fill=S.PAPER, stroke=S.INK, stroke_width=1.5)
    out.append('<g class="door-leaf">' + leaf + '</g>')
    # two locks on the jamb side: plate, keyhole, bolt, key
    for py, engaged in ((fy + 40, False), (fy + 120, True)):
        out.append(S.rect(24, py, 54, 66, fill=S.PAPER2, stroke=S.INK, stroke_width=2))
        kx, ky = 51, py + 30
        out.append(S.circle(kx, ky, 7, fill=S.INK, stroke='none'))
        out.append(S.path(f'M{kx},{ky} v18', fill='none', stroke=S.INK, stroke_width=4))
        bolt = S.line(78, ky, 106 if engaged else 88, ky, stroke=S.INK, stroke_width=6)
        out.append('<g class="bolt-move">' + bolt + '</g>' if engaged else bolt)
        key = S.rect(kx - 5, ky - 20, 10, 40, fill=S.PAPER, stroke=S.INK, stroke_width=2)
        key += S.circle(kx, ky, 3, fill=S.INK, stroke='none')
        if engaged:
            out.append('<g class="turning-key">' + key + '</g>')
        else:
            out.append(f'<g transform="rotate(90 {kx} {ky})">' + key + '</g>')
    return out


def build(p):
    doors = []
    for key, name, fixed, act, answer in [
        ('expressa', 'Expressa', 'Cláusula específica', 'Declarar a resolução', 'A declaração do credor produz a extinção sem sentença constitutiva.'),
        ('tacita', 'Tácita', 'Inadimplemento definitivo', 'Constituir em juízo', 'A sentença constitui o efeito extintivo fundado na cláusula tácita.'),
    ]:
        out = [S.text(20, 22, name, size=18, family=S.SANS, weight='600'),
               S.text(20, 44, fixed, size=14, family=S.SERIF)]
        out += _door()
        doors.append(f'<div class="door-unit" data-door="{key}">' + S.svg(310, 300, 'Via ' + name + ' da resolução', out)
                     + f'<button type="button" class="door-act" aria-pressed="false">{act}</button>'
                     + f'<p class="door-answer" aria-live="polite">{answer}</p></div>')
    return '<div class="tgc10-doors">' + ''.join(doors) + '</div>', []
