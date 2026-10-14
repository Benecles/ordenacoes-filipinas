"""Controle Aula 11 · Figs. 3 and 4: one petition drawn twice. In the via principal the constitutional
question is the pedido; in the via incidental it moves up into the direito, as the premise of a claim
between A and B. The position of the bracket is the whole point; colour keeps its house meaning
(blue = what the decision does, orange = its limit), never the system's name.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import Document, WARN, svg, t


def sheet(uid, title, parties, fatos, direito, pedido):
    return Document(uid, x=40, y=70, w=440, font_size=14.5, meta_size=12.5, label_size=10.5, lines=[
        ('title', title, 'title'),
        ('party', parties[0], 'p0'),
        ('party', parties[1], 'p1'),
        ('clause', ('Dos fatos', fatos), 'fatos'),
        ('clause', ('Do direito', direito), 'direito'),
        ('clause', ('Dos pedidos', pedido), 'pedido'),
        ('sign', ('Local e data', 'Advogado'), 'sig'),
    ], lead=27, indent=100)


def panel(ident, head, doc, at, sub, effect, limit, label):
    inner = t(40, 40, head, size=11.5, weight=700, caps=True, ls='.12em')
    inner += doc.paper() + doc.highlight([at], tone='muted') + ''.join(doc.parts)
    inner += doc.bracket([at], 'right', 'A questão', sub=sub, tone='ink', gap=14)
    y = doc.y + doc.h + 64
    inner += t(40, y, 'Se procedente', size=10, weight=700, caps=True, fill='var(--ink-2)')
    inner += t(40, y + 26, effect, size=15, weight=700, caps=True, fill='var(--dif)')
    if limit:
        inner += t(40, y + 50, limit, size=13, fill='var(--conc)')
    return svg('0 0 600 600', inner, cls='panel fig on', ident=ident, label=label)


def panels():
    conc = sheet('a11-p-conc', 'Exmo. Sr. Ministro Presidente do STF',
                 [('Requerente', 'um legitimado do art. 103 da CF'), ('Requerido', 'não há réu')],
                 'a Lei X foi publicada e está em vigor.',
                 'a Lei X contraria o art. Z da Constituição.',
                 'a declaração de inconstitucionalidade da Lei X.')
    dif = sheet('a11-p-dif', 'Exmo. Sr. Juiz de Direito',
                [('Autor', 'A'), ('Réu', 'B')],
                'B exige de A o que a Lei X determina.',
                'a Lei X contraria o art. Z da Constituição; logo, não obriga A.',
                'que A seja dispensado de cumprir o que B exige.')
    return [
        panel('p-conc', 'Via principal · ação direta', conc, 'pedido', 'é o pedido',
              'Contra todos · ex tunc', 'salvo modulação dos efeitos',
              'Petição de ação direta ao STF: não há réu, e a inconstitucionalidade da lei é o próprio pedido; se procedente, vale contra todos e, salvo modulação, desde a origem'),
        panel('p-dif', 'Via incidental · ação entre A e B', dif, 'direito', 'é premissa',
              'Entre A e B · ex tunc', '',
              'Petição de uma ação comum entre A e B: a inconstitucionalidade aparece nos fundamentos, como premissa do pedido; se acolhida, vale entre as partes'),
    ]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    ps = panels()
    n = inject('courses/controle-de-constitucionalidade/aula-11.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in ps})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
