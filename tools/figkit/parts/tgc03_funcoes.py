"""Aula 03, ch.1: the three functions of boa-fe objetiva applied to the consorcio facts, an instrument.
Sources: Pereira III pp. 20-21 (padrao de conduta, deveres positivos); Venosa pp. 11-13; CC arts. 113, 187, 422;
RI 71001586668 (TJRS). No durations or amounts. Params: none.
"""
from . import svg as S
from . import tgc01_hand as H
from .tgc03_mao import W, frame, cut, strike

CH = [('a', 'Sigilo violado, prestação paga'), ('b', 'Cobrança ao fim de boletos repetidos'),
      ('c', 'Sentido de uma declaração pelos usos')]
AN = {
    'a': ('Função integrativa', 'A boa-fé acrescenta deveres anexos: informação e sigilo, cuidado e segurança, prestar contas.',
          'Eles podem ser violados mesmo quando a prestação principal é cumprida.', True),
    'b': ('Função de controle', 'Limita o modo de exercer o direito: boletos repetidos sem ressalva justificaram esperar a liberação da garantia.',
          'O exercício manifestamente excessivo é abuso de direito, art. 187.', False),
    'c': ('Função interpretativa', 'O sentido das declarações se orienta pela boa-fé objetiva e pelos usos próprios do negócio.',
          'Os critérios do art. 113 estão em Interpretação dos contratos.', True),
}


def build(p):
    y, x0, x1 = 130, 150, 930
    cx = 540
    base = [H.cord(x0 + 8, x1 - 8, y), H.mark(x0, y, S.DIF), H.mark(x1, y, S.DIF),
            H.name(x0, y + 34, 'Prestação principal', anchor='start', size=13)]
    over = {'a': [], 'b': [], 'c': []}
    for nm, x in [('sigilo', 400), ('cuidado', 510), ('contas', 620), ('segurança', 730)]:
        over['a'] += [H.rule(f'M{x},{y + 8} V{y + 48}', S.DIF, 1.0), H.mark(x, y + 54, S.DIF, r=5.5, solid=False),
                      H.gloss(x, y + 84, nm, S.INK2, anchor='middle', size=14)]
    over['a'][0:0] = []
    for i in range(6):
        over['b'] += [H.mark(190 + i * 30, y, S.INK, r=5)]
    over['b'] += cut(368, y, 56) + [H.gloss(368, y - 44, 'cobrança ao fim', S.CONC, anchor='middle', size=14),
                  H.gloss(260, y + 40, 'boletos sem ressalva', S.INK2, anchor='middle', size=14),
                  H.gloss(x1, y + 40, 'garantia', S.INK2, anchor='middle', size=14)]
    for i in range(4):
        over['c'].append(H.rule(f'M{x0},{y - 100 + i * 15} H{x0 + 190 - (i % 2) * 40}', S.INK, 1.0))
    over['c'] += [H.rule(f'M{x0 + 205},{y - 78} C{x0 + 330},{y - 78} {cx - 60},{y - 50} {cx + 10},{y - 8}', S.DIF, 2.0),
                  H.gloss(cx + 20, y - 52, 'usos', S.DIF, size=14.5)]
    return S.svg(W, 400, 'As três funções da boa-fé objetiva: integrativa, de controle e interpretativa',
                 frame('Boa-fé objetiva · uma situação, uma função', CH, AN, base, over, 236, 296, 400)), []
