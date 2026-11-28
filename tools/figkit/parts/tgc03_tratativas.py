"""Aula 03, ch.3: the desistencia of tratativas, an instrument (language: time strip).
Sources: REsp 1.367.955/SP (Asti: expectativa justificada, despesas comprovadas, lucro estimado excluido); Venosa pp.80-83
(justa causa; TJSP, imovel sem titulo de dominio; test drive, cheque de garantia). No dates or sums. Params: none.
"""
from . import svg as S
from . import tgc01_hand as H
from .tgc03_mao import W, frame, cut, strands, arrow, strike

CH = [('a', 'Cancelamento após os preparativos'), ('b', 'Vendedor sem título de domínio'),
      ('c', 'Test drive revela defeito')]
AN = {
    'a': ('Dever de indenizar', 'O STJ manteve a responsabilidade: houve expectativa justificada de contratação e despesas comprovadas.',
          'Os lucros apenas estimados ficam fora da indenização (REsp 1.367.955/SP).', True),
    'b': ('Justa causa', 'Faltava ao vendedor o título de domínio do imóvel, motivo suficiente para romper as negociações.',
          'A desistência não gera o dever de indenizar; as partes voltam ao momento anterior à contratação.', False),
    'c': ('Justa causa', 'O problema mecânico constatado no test drive justifica desistir da compra do automóvel.',
          'O adquirente tem direito de ver restituído o cheque emitido apenas em garantia.', False),
}


def build(p):
    x0, xr, xc, y = 90, 640, 860, 110
    base = strands(x0, xr, y) + [H.rule(f'M{xr},{y} H{xc - 14}', S.INK2, 1.0, '3 6'),
            H.mark(xc, y, S.INK2), H.gloss(xc, y - 24, 'contrato', S.INK2, anchor='middle', size=14),
            H.gloss(330, y - 34, 'tratativas', S.INK2, anchor='middle', size=14)]
    for x in (150, 270, 390, 510):
        base.append(H.mark(x, y, S.INK, r=5))
    base += cut(xr, y, 60, S.INK) + [H.gloss(xr, y - 40, 'ruptura', S.INK2, anchor='middle', size=14)]
    over = {
        'a': [H.bracket(150, 510, y + 36, up=False, col=S.DIF), H.gloss(330, y + 68, 'despesas comprovadas', S.DIF, anchor='middle', size=14),
              H.rule(f'M{xc - 24},{y + 30} H{xc + 24}', S.CONC, 2.0),
              H.gloss(xc, y + 52, 'lucro estimado fica de fora', S.CONC, anchor='middle', size=14)],
        'b': [H.mark(100, y - 66, S.CONC, r=7)] + strike(100, y - 66, 7) + [
              H.gloss(118, y - 61, 'título de domínio', S.CONC, size=14)] + cut(xr, y, 60, S.CONC) + arrow(xr - 10, x0 + 10, y + 46, S.DIF, 1.4, '3 5') +
             [H.gloss(370, y + 70, 'volta ao momento anterior', S.DIF, anchor='middle', size=14)],
        'c': [H.mark(510, y, S.CONC, r=12)] + strike(510, y, 8) + [H.gloss(510, y + 42, 'defeito', S.CONC, anchor='middle', size=14),
              H.rule(f'M{xr - 70},{y + 60} h56', S.DIF, 2.0), H.gloss(xr - 42, y + 80, 'cheque', S.INK2, anchor='middle', size=14)] +
             arrow(xr - 76, x0 + 10, y + 60, S.DIF, 1.4, '3 5'),
    }
    return S.svg(W, 372, 'A desistência das tratativas: indenização quando faltou justa causa, restituição quando houve',
                 frame('Tratativas · a ruptura e sua razão', CH, AN, base, over, 196, 262, 372)), []
