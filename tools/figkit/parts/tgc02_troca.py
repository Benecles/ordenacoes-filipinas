"""Aula 02, ch.4: when the exchange is preserved or revised, an instrument (language: the two-way exchange line).
Sources: REsp 803.481/GO (soy; predictable risk), REsp 1.102.848/SP (plano de saude; collectivity behind a company
is not enough), Windscheid's coronation cases (purpose frustrated, balconies still available), the rental clause
with proportional fine (transfer by employer + thirty days' written notice). Params: none.
"""
from . import svg as S
from .tgc04_instr import W, dot, label, frame

H = 430
CH = [('a', 'Soja, preço em alta'), ('b', 'Plano de saúde'), ('c', 'Sacadas do cortejo'), ('d', 'Locação e transferência')]
AN = {
    'a': ('A troca fica como pactuada', 'No REsp 803.481/GO, a variação do preço da soja era risco previsível e próprio da venda de safra futura;',
          'não houve onerosidade excessiva, e o lucro maior do comprador não a produz.', False),
    'b': ('A troca fica como pactuada', 'No REsp 1.102.848/SP, a maioria rejeitou a revisão: o reajuste foi pactuado entre duas empresas;',
          'a coletividade por trás de uma delas não bastou em nenhum dos votos para justificar a revisão.', False),
    'c': ('O fim frustrado atinge o contrato', 'Nos coronation cases de Windscheid, o cancelamento do cortejo frustrou o fim do contrato,',
          'embora as sacadas continuassem à disposição: a função da troca importa, não só a prestação.', True),
    'd': ('A multa só cai com os pressupostos', 'Durante o prazo, a devolução paga multa proporcional; transferência de localidade pelo empregador e',
          'aviso escrito de trinta dias dispensam a multa. Sem eles, o fundamento especial desaparece.', True),
}


def build(p):
    ax, bx, y = 230, 850, 120
    base = [dot(ax, y), dot(bx, y), label(ax, y - 26, 'parte', 14, anchor='middle'), label(bx, y - 26, 'parte', 14, anchor='middle'),
            S.line(ax + 12, y - 8, bx - 12, y - 8, stroke=S.INK, stroke_width=2), S.line(bx - 12, y + 10, ax + 12, y + 10, stroke=S.INK, stroke_width=2),
            S.path(f'M{bx - 20},{y - 14} L{bx - 12},{y - 8} L{bx - 20},{y - 2}', fill='none', stroke=S.INK, stroke_width=2),
            S.path(f'M{ax + 20},{y + 4} L{ax + 12},{y + 10} L{ax + 20},{y + 16}', fill='none', stroke=S.INK, stroke_width=2),
            label(540, y - 20, 'prestação', 13, anchor='middle'), label(540, y + 32, 'contraprestação', 13, anchor='middle')]
    mid = 540
    over = {
        'a': [S.path(f'M{mid - 200},{y + 80} q25 -34 50 0 t50 0 t50 0 t50 0 t50 0 t50 0 t50 0 t50 0', fill='none', stroke=S.CONC, stroke_width=2),
              S.line(mid - 200, y + 52, mid - 200, y + 108, stroke=S.CONC, stroke_width=2), S.line(mid + 200, y + 52, mid + 200, y + 108, stroke=S.CONC, stroke_width=2),
              label(mid, y + 110, 'a oscilação já fazia parte do contrato', 13, anchor='middle', fill=S.CONC)],
        'b': [S.circle(bx, y, 30, fill='none', stroke=S.CONC, stroke_width=1.5, stroke_dasharray='3 4')]
             + [dot(bx + dx, y + dy, S.MUTED, r=4) for dx, dy in ((-44, -34), (-50, 6), (-36, 44), (44, -34), (52, 6), (38, 44))]
             + [S.line(bx - 62, y - 56, bx - 62, y + 66, stroke=S.CONC, stroke_width=3), label(bx - 20, y + 98, 'a coletividade fica fora do preço', 13, anchor='middle', fill=S.CONC)],
        'c': [S.circle(mid, y - 82, 15, fill=S.PAPER, stroke=S.DIF, stroke_width=2.4, stroke_dasharray='3 3'),
              S.line(mid - 12, y - 94, mid + 12, y - 70, stroke=S.DIF, stroke_width=2.6), S.line(mid + 12, y - 94, mid - 12, y - 70, stroke=S.DIF, stroke_width=2.6),
              label(mid + 30, y - 78, 'o fim do contrato', 13, fill=S.DIF)],
        'd': [S.rect(ax + 60, y + 58, 360, 18, fill='none', stroke=S.INK, stroke_width=1.6)] + S.hatch(ax + 60, y + 58, 360, 18, step=8, stroke=S.GRID, stroke_width=1)
             + [S.line(ax + 60, y + 90, ax + 420, y + 90, stroke=S.INK2, stroke_width=1.2), S.line(ax + 330, y + 82, ax + 330, y + 98, stroke=S.DIF, stroke_width=2.6),
                label(ax + 60, y + 114, 'multa proporcional durante o prazo', 13, fill=S.INK2), label(ax + 330, y + 114, '30 dias de aviso', 13, anchor='middle', fill=S.DIF)],
    }
    return S.svg(W, H, 'A troca preservada ou revista: soja, plano de saúde, cortejo e locação',
                 frame('A troca pactuada · o que a função social faz com ela', CH, AN, base, over, 236, 296, H)), []
