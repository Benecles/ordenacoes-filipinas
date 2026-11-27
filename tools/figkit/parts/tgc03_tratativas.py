"""Aula 03, ch.3: the desistencia of tratativas, an instrument (language: time strip).
Sources: REsp 1.367.955/SP (Asti: expectativa justificada, despesas comprovadas, lucro estimado excluido); Venosa pp.80-83
(justa causa; TJSP, imovel sem titulo de dominio; test drive, cheque de garantia). No dates or sums. Params: none.
"""
from . import svg as S
from .tgc04_instr import W, label, frame

H = 372
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
    base = [S.line(x0, y, xr, y, stroke=S.INK, stroke_width=1.6)]
    for x in (150, 270, 390, 510):
        base.append(S.circle(x, y, 7, fill=S.PAPER, stroke=S.INK, stroke_width=2.2))
    base += [S.line(xr, y - 30, xr, y + 30, stroke=S.INK, stroke_width=4),
             S.line(xr, y, xc - 14, y, stroke=S.INK, stroke_width=1.4, stroke_dasharray='3 6'),
             S.rect(xc - 14, y - 14, 28, 28, fill=S.PAPER, stroke=S.INK, stroke_width=2, stroke_dasharray='3 3'),
             label(xr, y - 40, 'ruptura', 13, anchor='middle', fill=S.INK2),
             label(xc, y - 26, 'contrato', 13, anchor='middle', fill=S.INK2),
             label(330, y - 24, 'tratativas', 13, anchor='middle', fill=S.INK2)]
    over = {
        'a': S.hatch(150, y + 18, 360, 26, step=9, stroke=S.DIF, stroke_width=1.2) +
             [S.rect(150, y + 18, 360, 26, fill='none', stroke=S.DIF, stroke_width=2),
              label(330, y + 66, 'despesas comprovadas', 13, anchor='middle', fill=S.DIF),
              S.line(xc - 24, y + 24, xc + 24, y - 24, stroke=S.CONC, stroke_width=2.6) if False else '',
              S.line(xc - 22, y + 30, xc + 22, y + 30, stroke=S.CONC, stroke_width=2.6),
              label(xc, y + 54, 'lucro estimado', 13, anchor='middle', fill=S.CONC),
              label(xc, y + 70, 'fica de fora', 13, anchor='middle', fill=S.CONC)],
        'b': [S.rect(90, y - 62, 22, 22, fill=S.PAPER, stroke=S.CONC, stroke_width=2.4),
              S.line(86, y - 66, 116, y - 36, stroke=S.CONC, stroke_width=2.4),
              label(124, y - 46, 'título de domínio', 13, fill=S.CONC),
              S.line(xr, y - 30, xr, y + 30, stroke=S.CONC, stroke_width=4),
              S.path(f'M{xr - 8},{y + 40} H{x0} ', fill='none', stroke=S.DIF, stroke_width=1.8, stroke_dasharray='3 5'),
              S.path(f'M{x0 + 10},{y + 34} L{x0},{y + 40} L{x0 + 10},{y + 46}', fill='none', stroke=S.DIF, stroke_width=1.8),
              label(370, y + 62, 'volta ao momento anterior', 13, anchor='middle', fill=S.DIF)],
        'c': [S.circle(510, y, 14, fill=S.PAPER, stroke=S.CONC, stroke_width=2.6),
              S.line(500, y - 10, 520, y + 10, stroke=S.CONC, stroke_width=2.4),
              label(510, y + 40, 'defeito', 13, anchor='middle', fill=S.CONC),
              S.rect(xr - 70, y + 52, 56, 24, fill=S.PAPER, stroke=S.DIF, stroke_width=2),
              label(xr - 42, y + 69, 'cheque', 12, anchor='middle', fill=S.INK2),
              S.path(f'M{xr - 74},{y + 64} H{x0 + 10}', fill='none', stroke=S.DIF, stroke_width=1.8, stroke_dasharray='3 5'),
              S.path(f'M{x0 + 20},{y + 58} L{x0 + 10},{y + 64} L{x0 + 20},{y + 70}', fill='none', stroke=S.DIF, stroke_width=1.8)],
    }
    return S.svg(W, H, 'A desistência das tratativas: indenização quando faltou justa causa, restituição quando houve',
                 frame('Tratativas · a ruptura e sua razão', CH, AN, base, over, 196, 250, H)), []
