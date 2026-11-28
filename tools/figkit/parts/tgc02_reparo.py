"""Aula 02, ch.5: what the STJ restored and what it sent to liquidation, an instrument (language: stems on a ruled
scale; tgc01_hand, no filled bars). Sources: REsp 1.316.149/SP (moral compensation 500,000 and 100,000 restored; evidence
of loss of prestige set aside for the legal person in exceptional cases; lucros cessantes by both criteria of LPI art. 210,
relator outvoted). Stems use the page's 5:1 ratio; the liquidation stem has no amount because the source gives none."""
from . import svg as S
from .tgc01_hand import rule, mark, name, gloss, art
from .tgc02_hand import W, frame

H = 400
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
    base0, k = 158, .2
    xf, xa, xl = 300, 470, 720
    b = [rule(f'M120,{base0} H820', S.INK, 1.0)]
    for v in (100, 200, 300, 400, 500):
        yy = base0 - v * k
        b += [rule(f'M120,{yy} H820', S.GRID, 1.0), art(108, yy + 4, str(v), anchor='end', size=13)]
    b += [gloss(820, 18, 'compensação moral · R$ mil', anchor='end'),
          name(xf, base0 + 20, 'Fischer', anchor='middle'), name(xa, base0 + 20, 'All-E', anchor='middle'), name(xl, base0 + 20, 'Lucros cessantes', anchor='middle')]
    for x, v in ((xf, 500), (xa, 100), (xl, 300)):
        b += [rule(f'M{x},{base0} V{base0 - v * k}', S.MUTED, 1.0), mark(x, base0 - v * k, S.MUTED, 4.5)]
    over = {
        'a': [rule(f'M{xf},{base0} V{base0 - 500 * k}', S.DIF, 2), mark(xf, base0 - 500 * k, S.DIF, 5.5, solid=True),
              rule(f'M{xa},{base0} V{base0 - 100 * k}', S.DIF, 2), mark(xa, base0 - 100 * k, S.DIF, 5.5, solid=True),
              name(xf + 14, base0 - 500 * k + 4, '500', col=S.INK), name(xa + 14, base0 - 100 * k + 4, '100', col=S.INK)],
        'b': [rule(f'M{xl - 20},{base0 - 300 * k} H{xl + 20}', S.DIF, 2), rule(f'M{xl - 20},{base0 - 150 * k} H{xl + 20}', S.DIF, 2),
              rule(f'M{xl + 30},{base0 - 300 * k} V{base0 - 150 * k}', S.DIF, 1.0),
              gloss(xl + 40, base0 - 220 * k + 4, 'o credor escolhe', col=S.DIF), art(xl, base0 - 300 * k - 12, 'art. 210 LPI', anchor='middle')],
        'c': [rule(f'M{xf - 30},{base0 - 80} V34 H{xa + 30} V{base0 - 80}', S.CONC, 1.5),
              gloss(xf - 30, 28, 'prova do prestígio exigida na origem', col=S.CONC),
              gloss(xf + 92, 104, 'exceção: dano indiscutível', col=S.CONC), rule(f'M{xf + 80},34 V92', S.CONC, 2)],
    }
    return S.svg(W, H, 'Compensação moral restabelecida e lucros cessantes em liquidação',
                 frame(CH, AN, b, over, 224, 292, H)), []
