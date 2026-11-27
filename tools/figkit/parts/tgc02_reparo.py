"""Aula 02, ch.5: what the STJ restored and what it sent to liquidation, an instrument (language: ledger bars).
Sources: REsp 1.316.149/SP (moral compensation 500,000 and 100,000 restored; evidence of loss of prestige set aside for
the legal person in exceptional cases; lucros cessantes by both criteria of LPI art. 210, relator outvoted).
Bars use the page's 5:1 ratio; the liquidation bar has no amount because the source gives none. Params: none.
"""
from . import svg as S
from .tgc04_instr import W, label, frame

H = 430
CH = [('a', 'Dano moral das agências'), ('b', 'Lucros cessantes'), ('c', 'Prova do prestígio')]
AN = {
    'a': ('Restabelecida a compensação moral', 'O STJ restabeleceu R$ 500.000,00 à Fischer e R$ 100.000,00 à All-E: a campanha foi tratada com menoscabo,',
          'e isso bastou para evidenciar a violação da honra objetiva das duas pessoas jurídicas.', True),
    'b': ('Fica para liquidação, pelos dois critérios', 'Os lucros cessantes serão liquidados segundo ambos os critérios do art. 210 da Lei de Propriedade Industrial,',
          'para que o credor escolha o mais favorável; o relator ficou vencido nesse ponto. Sem valor fixado.', True),
    'c': ('Dispensada a prova direta, em casos excepcionais', 'Para a pessoa jurídica, o STJ admite dispensar a prova direta quando as circunstâncias tornam o dano',
          'indiscutível, como no protesto indevido de título já pago. O tribunal de origem exigira essa prova.', False),
}


def build(p):
    base0, k, bw = 214, .26, 70
    xf, xa, xl = 300, 470, 720
    bars = [S.line(120, base0, 820, base0, stroke=S.INK, stroke_width=1.5)]
    for v in (0, 100, 200, 300, 400, 500):
        yy = base0 - v * k
        bars += [S.line(120, yy, 820, yy, stroke=S.GRID, stroke_width=1), label(108, yy + 5, str(v), 12, anchor='end', fill=S.INK2)]
    bars += [label(820, 52, 'compensação moral · R$ mil', 13, anchor='end', fill=S.INK2),
             label(xf + bw / 2, base0 + 22, 'Fischer', 14, anchor='middle'), label(xa + bw / 2, base0 + 22, 'All-E', 14, anchor='middle'),
             label(xl + bw / 2, base0 + 22, 'lucros cessantes', 14, anchor='middle')]
    bars += [S.rect(xf, base0 - 500 * k, bw, 500 * k, fill='none', stroke=S.MUTED, stroke_width=1.5, stroke_dasharray='4 3'),
             S.rect(xa, base0 - 100 * k, bw, 100 * k, fill='none', stroke=S.MUTED, stroke_width=1.5, stroke_dasharray='4 3'),
             S.rect(xl, base0 - 300 * k, bw, 300 * k, fill='none', stroke=S.MUTED, stroke_width=1.5, stroke_dasharray='4 3')]
    over = {
        'a': [S.rect(xf, base0 - 500 * k, bw, 500 * k, fill=S.DIF), S.rect(xa, base0 - 100 * k, bw, 100 * k, fill=S.DIF),
              label(xf + bw / 2, base0 - 500 * k - 10, '500', 15, anchor='middle', fill=S.INK), label(xa + bw / 2, base0 - 100 * k - 10, '100', 15, anchor='middle', fill=S.INK)],
        'b': [S.line(xl - 20, base0 - 300 * k, xl + bw + 20, base0 - 300 * k, stroke=S.DIF, stroke_width=2.4),
              S.line(xl - 20, base0 - 150 * k, xl + bw + 20, base0 - 150 * k, stroke=S.DIF, stroke_width=2.4),
              S.line(xl + bw + 30, base0 - 300 * k, xl + bw + 30, base0 - 150 * k, stroke=S.DIF, stroke_width=1.5),
              label(xl + bw + 40, base0 - 220 * k, 'o credor escolhe', 13, fill=S.DIF), label(xl + bw / 2, base0 - 300 * k - 12, 'art. 210 LPI', 13, anchor='middle', fill=S.INK2)],
        'c': [S.path(f'M{xf - 30},{base0 - 80} V72 H{xa + bw + 30} V{base0 - 80}', fill='none', stroke=S.CONC, stroke_width=2.2, stroke_dasharray='6 4'),
              S.line(xf + 40, 72, xf + 120, 72, stroke=S.PAPER, stroke_width=6), label(xf - 30, 62, 'prova do prestígio exigida na origem', 13, fill=S.CONC),
              S.path(f'M{xf + 80},72 V{base0 - 80 - 40}', fill='none', stroke=S.CONC, stroke_width=2.2),
              label(xf + 92, 118, 'exceção: dano indiscutível', 13, fill=S.CONC)],
    }
    return S.svg(W, H, 'Compensação moral restabelecida e lucros cessantes em liquidação',
                 frame('A reparação · o que o STJ fixou e o que ficou para depois', CH, AN, bars, over, 250, 306, H)), []
