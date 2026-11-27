"""Aula 09, ch.5: which power answers which request, laid on the line of instalments (an instrument).
Sources: CC arts. 478-480, 317; Pereira III p. 150 (instalments paid before suit are not revisable; those given or
received pending the suit are subject to modification at execution of the sentence); Luis Renato p. 27 (offer must
be determinate); Venosa p. 71. Categorical positions, no scale. Params: none.
"""
from . import svg as S
from .tgc04_instr import W, label, frame

H = 450
CH = [('a', 'Devedor pede resolução'), ('b', 'Réu oferece modificação'), ('c', 'Só uma parte deve'),
      ('d', 'Parcelas na pendência da lide'), ('e', 'Valor defasado (art. 317)')]
AN = {
    'a': ('Resolução do contrato, com efeitos desde a citação', 'O devedor da prestação onerada pede, no art. 478, a resolução; a sentença retroage à data da citação.', 'A modificação das bases não é conferida ao devedor nem, de ofício, ao juiz (Marino).', True),
    'b': ('A resolução pode ser evitada', 'O art. 479 atribui ao réu oferecer a modificação equitativa; a oferta determinada permite aferir o conteúdo,', 'e a genérica remete ao juiz as condições. Vontade de conversar não define o novo contrato.', False),
    'c': ('Redução ou novo modo de execução', 'O art. 480 autoriza, quando as obrigações couberem a apenas uma das partes,', 'que ela peça a redução da prestação ou a alteração do modo de executá-la.', False),
    'd': ('Só as parcelas da lide ficam sujeitas à modificação', 'As pagas antes do ingresso em juízo não se revêem; as dadas ou recebidas na pendência da lide', 'podem ser modificadas na execução da sentença. O devedor não suspende pagamentos por conta própria.', False),
    'e': ('O juiz corrige o valor, a pedido da parte', 'Por motivos imprevisíveis, a desproporção manifesta entre o valor devido e o do momento da execução', 'autoriza corrigir a prestação (art. 317), de modo a assegurar o valor real.', False),
}


def build(p):
    y, s = 112, 42
    xs = [60 + i * 86 for i in range(8)]
    cut = (xs[3] + xs[4]) / 2 + 2
    base = [S.line(40, y + s / 2, 1040, y + s / 2, stroke=S.GRID, stroke_width=1.5)]
    for i, x in enumerate(xs):
        if i < 4:
            base.append(S.rect(x, y, s, s, fill=S.INK, stroke=S.INK, stroke_width=1.6))
        else:
            base.append(S.rect(x, y, s, s, fill=S.PAPER, stroke=S.INK, stroke_width=1.8, stroke_dasharray='4 3'))
    base += [S.line(cut, y - 30, cut, y + s + 30, stroke=S.INK, stroke_width=3),
             label(cut, y - 40, 'ingresso em juízo', 13, anchor='middle', weight='600'),
             label(60, y + s + 52, 'parcelas já pagas', 13), label(xs[4], y + s + 52, 'parcelas a vencer ou em disputa', 13)]
    over = {
        'a': [S.path(f'M{cut},{y + s + 70} H{xs[0]}', fill='none', stroke=S.DIF, stroke_width=0),
              S.line(cut, y - 12, 1040, y - 12, stroke=S.DIF, stroke_width=2.6),
              label(1040, y - 22, 'o vínculo se extingue', 13, anchor='end', fill=S.DIF)],
        'b': [S.circle(cut + 190, y - 12, 7, fill=S.PAPER, stroke=S.DIF, stroke_width=2.4),
              S.line(cut + 190, y - 5, cut + 190, y, stroke=S.DIF, stroke_width=2.4),
              label(cut + 204, y - 22, 'oferta do réu', 13, fill=S.DIF)],
        'c': [S.rect(xs[6], y - 6, s + 12, s + 12, fill='none', stroke=S.DIF, stroke_width=2.4),
              label(xs[6] + 24, y + s + 80, 'só esta prestação se reduz', 13, anchor='middle', fill=S.DIF)],
        'd': [S.rect(xs[4] - 6, y - 6, 3 * 86 + s + 12 - 86 + 86, s + 12, fill='none', stroke=S.DIF, stroke_width=2.4),
              S.rect(xs[0] - 6, y - 6, 3 * 86 + s + 12, s + 12, fill='none', stroke=S.CONC, stroke_width=2.4),
              label(xs[0] + 130, y + s + 80, 'fora do alcance', 13, anchor='middle', fill=S.CONC)],
        'e': [S.rect(xs[5] - 6, y - 6, s + 12, s + 12, fill='none', stroke=S.DIF, stroke_width=2.4),
              S.line(xs[5] + s / 2, y + s + 6, xs[5] + s / 2, y + s + 22, stroke=S.DIF, stroke_width=2.4),
              label(xs[5] + s / 2, y + s + 80, 'valor real', 13, anchor='middle', fill=S.DIF)],
    }
    return S.svg(W, H, 'Pedidos do art. 478 ao art. 480 e ao art. 317 sobre a linha de parcelas',
                 frame('Revisão e resolução · o que cada pedido alcança', CH, AN, base, over, 262, 322, H)), []
