"""Aula 09, ch.5: which power answers which request, laid on the line of instalments (an instrument).
Sources: CC arts. 478-480, 317; Pereira III p. 150 (instalments paid before suit are not revisable; those given or
received pending the suit are subject to modification at execution of the sentence); Luis Renato p. 27 (offer must
be determinate); Venosa p. 71. Categorical positions, no scale. Params: none.
"""
from . import svg as S
from .tgc04_instr import W, label, frame

H = 476
CH = [('a', 'Devedor pede resolução'), ('b', 'Réu oferece modificação'), ('c', 'Só uma parte deve'),
      ('d', 'Parcelas na pendência da lide'), ('e', 'Valor defasado (art. 317)')]
AN = {
    'a': ('Resolução do contrato, com efeitos desde a citação', 'O devedor da prestação onerada pede, no art. 478, a resolução; a sentença retroage à data da citação.', 'A modificação das bases não é conferida ao devedor nem, de ofício, ao juiz (Marino).', True),
    'b': ('A resolução pode ser evitada', 'O art. 479 atribui ao réu oferecer a modificação equitativa; a oferta determinada permite aferir o conteúdo,', 'e a genérica remete ao juiz as condições. Vontade de conversar não define o novo contrato.', False),
    'c': ('Redução ou novo modo de execução', 'O art. 480 autoriza, quando as obrigações couberem a apenas uma das partes,', 'que ela peça a redução da prestação ou a alteração do modo de executá-la.', False),
    'd': ('Só as parcelas da lide ficam sujeitas à modificação', 'As pagas antes do ingresso em juízo não se revêem; as dadas ou recebidas na pendência da lide', 'podem ser modificadas na execução da sentença. O devedor não suspende pagamentos por conta própria.', False),
    'e': ('O juiz corrige o valor, a pedido da parte', 'Por motivos imprevisíveis, a desproporção manifesta entre o valor devido e o do momento da execução', 'autoriza corrigir a prestação (art. 317), de modo a assegurar o valor real.', False),
}


def _stub(x, y, w, h, paid, col=S.INK):
    o = [S.rect(x, y, w, h, fill=S.INK if paid else S.PAPER, stroke=col, stroke_width=1.8, stroke_dasharray=None if paid else '4 3'),
         S.line(x + 16, y, x + 16, y + h, stroke=S.PAPER if paid else S.GRID, stroke_width=1.4, stroke_dasharray='2 3'),
         S.circle(x + 8, y + h / 2, 3, fill=S.PAPER, stroke=S.PAPER if paid else S.GRID, stroke_width=1.2)]
    return o


def build(p):
    y, h, w = 92, 64, 108
    xs = [50 + i * 122 for i in range(8)]
    cut = xs[4] - 7
    base = ['<g transform="translate(0,14)">', label(24, 42, 'carnê de parcelas', 13, weight='600')]
    for i, x in enumerate(xs):
        base += _stub(x, y, w, h, i < 4)
        base.append(label(x + w / 2 + 6, y + h / 2 + 5, str(i + 1), 16, anchor='middle', weight='600', fill=S.PAPER if i < 4 else S.INK))
    base += [S.line(cut, y - 30, cut, y + h + 14, stroke=S.INK, stroke_width=3),
             label(cut, y - 40, 'ingresso em juízo', 13, anchor='middle', weight='600'),
             label(xs[0], y + h + 32, 'pagas antes da ação', 13, fill=S.INK2),
             label(xs[4], y + h + 32, 'na pendência da lide', 13, fill=S.INK2),
             S.line(xs[0], y + h + 40, cut - 12, y + h + 40, stroke=S.INK, stroke_width=1.4),
             S.line(xs[4], y + h + 40, xs[7] + w, y + h + 40, stroke=S.INK, stroke_width=1.4, stroke_dasharray='4 3'), '</g>']
    by = y + h + 62
    end = xs[7] + w
    over = {
        # a: resolution runs back to the citation and ends the bond
        'a': [S.line(cut, by, end, by, stroke=S.DIF, stroke_width=3), S.path(f'M{cut + 10},{by - 7} L{cut},{by} L{cut + 10},{by + 7}', fill='none', stroke=S.DIF, stroke_width=3),
              *[S.line(x + 8, y + 8, x + w - 8, y + h - 8, stroke=S.DIF, stroke_width=2.4) for x in xs[4:]],
              *[S.line(x + 8, y + h - 8, x + w - 8, y + 8, stroke=S.DIF, stroke_width=2.4) for x in xs[4:]],
              label(end, by + 20, 'o vínculo se extingue', 13, anchor='end', fill=S.DIF),
              label(cut + 14, by + 20, 'retroage à citação', 13, fill=S.DIF)],
        # b: the defendant offers a new schedule, laid under the old one
        'b': [*[S.rect(x + 14, by - 6, w - 28, 30, fill=S.PAPER, stroke=S.DIF, stroke_width=2, stroke_dasharray='5 3') for x in xs[4:]],
              *[S.line(x + w / 2, y + h + 2, x + w / 2, by - 8, stroke=S.DIF, stroke_width=1.4) for x in xs[4:]],
              label(xs[4], by + 42, 'oferta do réu: nova condição para as parcelas abertas', 13, fill=S.DIF)],
        # c: only one party owes; its single instalment is cut down, or its mode changed
        'c': [S.rect(xs[6], y + 18, w, h - 18, fill=S.PAPER, stroke=S.DIF, stroke_width=2.4),
              S.rect(xs[6], y - 4, w, 22, fill='none', stroke=S.DIF, stroke_width=1.6, stroke_dasharray='3 3'),
              S.line(xs[6] + w / 2, y + h + 6, xs[6] + w / 2, by - 6, stroke=S.DIF, stroke_width=1.4),
              label(xs[6] + w / 2, by + 8, 'redução da prestação', 13, anchor='middle', fill=S.DIF),
              S.path(f'M{xs[4]},{by + 30} H{xs[5] + w}', fill='none', stroke=S.DIF, stroke_width=2.4, stroke_dasharray='2 5'),
              S.path(f'M{xs[5] + w - 10},{by + 23} L{xs[5] + w},{by + 30} L{xs[5] + w - 10},{by + 37}', fill='none', stroke=S.DIF, stroke_width=2.4),
              label(xs[4], by + 52, 'ou novo modo de execução', 13, fill=S.DIF)],
        # d: what the sentence can still modify, and what stays out of reach
        'd': [S.rect(xs[0] - 8, y - 8, xs[3] + w - xs[0] + 16, h + 16, fill='none', stroke=S.CONC, stroke_width=2.4),
              label(xs[0], by + 8, 'parcelas já pagas: fora do alcance', 13, fill=S.CONC),
              S.rect(xs[4] - 8, y - 8, xs[7] + w - xs[4] + 16, h + 16, fill='none', stroke=S.DIF, stroke_width=2.4),
              S.line(xs[4], by, xs[7] + w, by, stroke=S.DIF, stroke_width=2.4),
              label(xs[4], by + 28, 'modificáveis na execução da sentença', 13, fill=S.DIF)],
        # e: art. 317, the nominal sum against the real one
        'e': [S.rect(xs[6], y - 30, w, h + 30, fill='none', stroke=S.DIF, stroke_width=2.4),
              S.line(xs[6], y, xs[6] + w, y, stroke=S.INK, stroke_width=1.4, stroke_dasharray='4 3'),
              S.line(xs[6] + w + 14, y, xs[6] + w + 14, y - 30, stroke=S.DIF, stroke_width=2.4),
              S.path(f'M{xs[6] + w + 8},{y - 22} L{xs[6] + w + 14},{y - 30} L{xs[6] + w + 20},{y - 22}', fill='none', stroke=S.DIF, stroke_width=2.4),
              label(xs[6] + w / 2, by + 8, 'valor real da prestação', 13, anchor='middle', fill=S.DIF),
              S.line(xs[6] + w / 2, y + h + 6, xs[6] + w / 2, by - 8, stroke=S.DIF, stroke_width=1.4),
              label(xs[4], by + 36, 'por motivos imprevisíveis, a desproporção manifesta é corrigida', 13, fill=S.DIF)],
    }
    over = {k: ['<g transform="translate(0,14)">'] + v + ['</g>'] for k, v in over.items()}
    return S.svg(W, H, 'Pedidos do art. 478 ao art. 480 e ao art. 317 sobre o carnê de parcelas',
                 frame('Revisão e resolução · o que cada pedido alcança', CH, AN, base, over, 296, 352, H)), []
