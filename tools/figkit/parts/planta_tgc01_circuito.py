"""Planta cast for Aula 01, in the course hand (DIRECTION.md): the seguro as one operation, drawn as the two-strand cord.

No params. Fixed facts: STJ local assigned reading p.4, REsp 1.176.019. The bond between transportadora (consumidora,
finalismo mitigado, art. 2º CDC) and seguradora is the cord; the cobertura (frota e danos a terceiros, against the
prêmio) spans part of it; the transportadora pays the dono do caminhão, claims reembolso along the cord, and the claim
stops at the orange cut (risco excluído, categoria fora da cobertura): pedido improcedente. The táxi is a hypothesis
(dashed), not a fourth party. Nothing is boxed.
"""
from . import svg as S
from . import tgc01_hand as H


def build(p):
    cy = 200
    xa, xb, xc = 120, 960, 700
    o = []
    o.append(H.wire('seguro', 'Rastrear a contratação e a cobertura do seguro', [
        H.cord(xa + 8, xb - 8, cy),
        H.mark(xa, cy, S.DIF), H.mark(xb, cy, S.DIF),
        H.name(xa, cy - 76, 'Transportadora', anchor='middle'),
        H.gloss(xa - 84, cy - 58, 'consumidora · finalismo mitigado · art. 2º CDC', S.INK2),
        H.name(xb, cy - 76, 'Seguradora', anchor='middle'),
        H.rule(f'M{xa + 14},{cy + 24} V{cy + 30} H{xc - 40} V{cy + 24}', S.DIF, 1.0),
        H.gloss((xa + xc - 40) / 2 + 7, cy + 52, 'prêmio pago · cobertura: frota e danos a terceiros', S.DIF, anchor='middle'),
    ]))
    o.append(H.wire('reembolso', 'Rastrear o reembolso pedido e por que foi negado', [
        H.rule(f'M{xa + 30},{cy - 34} H{xc - 14}', S.INK, 2.0),
        H.rule(f'M{xc - 22},{cy - 39} L{xc - 12},{cy - 34} L{xc - 22},{cy - 29}', S.INK, 2.0),
        H.gloss(440, cy - 44, 'reembolso pleiteado, do vínculo ao seguro  →', S.INK2, anchor='middle'),
        H.rule(f'M{xc},{cy - 46} V{cy + 46}', S.CONC, 2.0),
        H.rule(f'M{xc - 6},{cy - 46} H{xc + 6} M{xc - 6},{cy + 46} H{xc + 6}', S.CONC, 1.0),
        H.name(xc + 8, cy - 76, 'Risco excluído · fora da cobertura', S.CONC, anchor='end'),
        H.art(xc, cy + 74, 'REsp 1.176.019 · pedido improcedente', S.CONC, anchor='middle'),
    ]))
    yd = cy + 150
    o.append(H.wire('indenizacao', 'Rastrear o pagamento ao dono do caminhão particular', [
        H.rule(f'M{xa},{cy + 10} V{yd} H{xa + 150}', S.INK, 2.0),
        H.rule(f'M{xa + 138},{yd - 5} L{xa + 148},{yd} L{xa + 138},{yd + 5}', S.INK, 1.4),
        H.mark(xa + 160, yd, S.INK),
        H.name(xa + 178, yd + 5, 'Dono do caminhão · indenização paga', S.INK),
    ]))
    o.append(H.wire('hipotese', 'Rastrear a hipótese de categoria prevista (táxi)', [
        H.rule(f'M{xb},{cy + 10} V{yd} H{xb - 28}', S.INK2, 1.0, '3 5'),
        H.mark(xb - 40, yd, S.INK2),
        H.name(xb - 58, yd + 5, 'Táxi · categoria prevista', S.INK2, anchor='end'),
    ]))
    svg = S.svg(1080, 420,
        'O seguro como uma operação no REsp 1.176.019: cordão de duas fitas entre transportadora e seguradora, o reembolso parado no risco excluído, o dono do caminhão indenizado e a hipótese do táxi', o)
    return svg.replace('viewBox="0 0 1080 420"', 'viewBox="0 100 1080 300"', 1), []
