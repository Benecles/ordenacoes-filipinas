"""Unfilled receipt: the evidence of discharge, CC 319–320; Venosa p.93.

Field lengths are typographic, never amounts or a fictional transaction.
"""
from . import svg as S


def build(p):
    out = [S.rect(16, 16, 448, 300, fill=S.PAPER2, stroke=S.INK, stroke_width=1.5)]
    out.append(S.text(40, 53, 'Quitação', size=23, family=S.SERIF))
    for y, label in [(92, 'Valor e espécie da dívida'), (143, 'Devedor · ou quem pagou'),
                     (194, 'Tempo e lugar do pagamento')]:
        out.append(S.text(40, y, label, size=18, family=S.SERIF))
        out.append(S.line(40, y+18, 440, y+18, stroke=S.MUTED, stroke_width=1))
    out.append(S.line(150, 267, 440, 267, stroke=S.INK, stroke_width=1))
    out.append(S.text(150, 294, 'Assinatura do credor', size=18, family=S.SERIF))
    return S.svg(480, 332, 'Recibo de quitação: campos do art. 320, sem preenchimento', out), []
