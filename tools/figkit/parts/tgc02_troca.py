"""Aula 02, ch.4: when the exchange is preserved or revised, an instrument (language: the two-way cord; tgc01_hand).
Sources: REsp 803.481/GO (soy; predictable risk), REsp 1.102.848/SP (plano de saude; collectivity behind a company
is not enough), Windscheid's coronation cases (purpose frustrated, balconies still available), the rental clause
with proportional fine (transfer by employer + thirty days' written notice). Params: none."""
from . import svg as S
from .tgc01_hand import cord, rule, mark, name, gloss
from .tgc02_hand import W, frame

H = 410
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
    ax, bx, y, mid = 230, 850, 84, 540
    base = [cord(ax + 8, bx - 8, y - 7, amp=5, half=24, taper=30), cord(ax + 8, bx - 8, y + 9, amp=5, half=24, taper=30),
            mark(ax, y, S.DIF), mark(bx, y, S.DIF), name(ax, y - 28, 'parte', anchor='middle'), name(bx, y - 28, 'parte', anchor='middle'),
            gloss(mid, y - 20, 'prestação', anchor='middle'), gloss(mid, y + 36, 'contraprestação', anchor='middle')]
    over = {
        'a': [S.path(f'M{mid - 200},{y + 74} q25 -32 50 0 t50 0 t50 0 t50 0 t50 0 t50 0 t50 0 t50 0', fill='none', stroke=S.CONC, stroke_width=2),
              rule(f'M{mid - 200},{y + 54} V{y + 94}', S.CONC, 1.0), rule(f'M{mid + 200},{y + 54} V{y + 94}', S.CONC, 1.0),
              gloss(mid, y + 112, 'a oscilação já fazia parte do contrato', col=S.CONC, anchor='middle')],
        'b': [S.circle(bx, y, 30, fill='none', stroke=S.CONC, stroke_width=1.0)]
             + [mark(bx + dx, y + dy, S.MUTED, 4) for dx, dy in ((-44, -34), (-50, 6), (-36, 44), (44, -34), (52, 6), (38, 44))]
             + [rule(f'M{bx - 62},{y - 56} V{y + 66}', S.CONC, 2), gloss(bx - 20, y + 96, 'a coletividade fica fora do preço', col=S.CONC, anchor='middle')],
        'c': [S.circle(mid, y - 62, 14, fill=S.PAPER, stroke=S.DIF, stroke_width=2),
              rule(f'M{mid - 8},{y - 70} L{mid + 8},{y - 54} M{mid + 8},{y - 70} L{mid - 8},{y - 54}', S.DIF, 2),
              gloss(mid + 26, y - 58, 'o fim do contrato', col=S.DIF)],
        'd': [rule(f'M{ax + 60},{y + 70} H{ax + 420}', S.INK, 2), rule(f'M{ax + 60},{y + 60} V{y + 80} M{ax + 420},{y + 60} V{y + 80}', S.INK2, 1.0),
              rule(f'M{ax + 330},{y + 58} V{y + 82}', S.DIF, 2),
              gloss(ax + 60, y + 104, 'multa proporcional durante o prazo', col=S.INK2), gloss(ax + 330, y + 104, '30 dias de aviso', col=S.DIF, anchor='middle')],
    }
    return S.svg(W, H, 'A troca preservada ou revista: soja, plano de saúde, cortejo e locação',
                 frame(CH, AN, base, over, 226, 292, H)), []
