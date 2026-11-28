"""Aula01 companion (elementos), in the course hand: art. 104's three requirements and what each failure does.

No params. Facts only from the companion's passages: CC art. 104 (agente capaz, objeto lícito possível determinado ou
determinável, forma prescrita ou não defesa), art. 497 (tutor), art. 426 (herança de pessoa viva), art. 107 and
Pereira p. 33 (forma essencial: o contrato não prevalece). Each requirement is a stretch of the cord; the failure is an
orange limit cutting it. Positions order the requirements; they measure nothing. Nothing is boxed.
"""
from . import svg as S
from . import tgc01_hand as H


def build(p):
    xa, xj, xe = 110, 300, 650
    ys = (62, 138, 214)
    ym = ys[1]
    o = [H.rule(f'M{xa + 8},{ym} H{xj}', S.INK, 2.0), H.mark(xa, ym, S.INK),
         H.name(xa, ym - 24, 'Negócio', anchor='middle'),
         H.gloss(xa, ym + 34, 'art. 104 · a validade requer', anchor='middle'),
         H.rule(f'M{xj},{ys[0]} V{ys[2]}', S.INK, 1.0), S.circle(xj, ym, 3.2, fill=S.INK, stroke=S.INK)]
    rows = [
        ('agente', 'Rastrear o requisito do agente capaz', 'I · agente capaz',
         'venda ao tutor do bem tutelado', 'art. 497, I: nulidade'),
        ('objeto', 'Rastrear o requisito do objeto lícito, possível e determinado', 'II · objeto lícito, possível, determinável',
         'herança de pessoa viva', 'art. 426: contrato vedado'),
        ('forma', 'Rastrear o requisito da forma prescrita ou não defesa', 'III · forma prescrita ou não defesa em lei',
         'forma exigida e não observada', 'art. 107: o contrato não prevalece'),
    ]
    for y, (key, lab, req, bad, art) in zip(ys, rows):
        o.append(H.wire(key, lab, [
            H.cord(xj, xe - 96, y), H.rule(f'M{xe - 86},{y - 16} V{y + 16}', S.CONC, 2.0),
            H.rule(f'M{xe - 86},{y} H{xe - 8}', S.CONC, 1.0), H.mark(xe, y, S.CONC),
            H.gloss(xj + 20, y - 20, req),
            H.name(xe + 20, y + 4, bad, S.CONC),
            H.art(xe + 20, y + 24, art)]))
    svg = S.svg(1080, 280, 'Os três requisitos de validade do art. 104 e a consequência de cada falha', o)
    return svg.replace('viewBox="0 0 1080 280"', 'viewBox="0 24 1080 240"', 1), []
