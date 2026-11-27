"""Aula 04, ch.3: who is bound after the reserve of nomination, an instrument.
Sources: CC arts. 467-471; Pereira III p. 106; Venosa (art. 470: no indication, refusal, insolvent nominee unknown to the
other party keep the contract between the originals; art. 468 sole paragraph: same form; art. 469: retroactive).
Params: none.
"""
from . import svg as S
from .tgc04_instr import W, dot, label, frame

H = 420
CH = [('a', 'Aceita na forma, em cinco dias'), ('b', 'Ninguém é indicado'), ('c', 'A indicada recusa'),
      ('d', 'Aceitação informal'), ('e', 'Insolvente e ignorada')]
AN = {
    'a': ('A nomeada ocupa a posição desde a celebração', 'A substituição eficaz retroage (art. 469): o contrato já existia entre pessoas identificadas,', 'e a nomeada assume por inteiro direitos e obrigações.', True),
    'b': ('O contrato fica entre os originários', 'Sem indicação, o contrato produz efeitos entre os contratantes originários (art. 470).', 'A reserva já integrava o contrato; nada foi transferido.', False),
    'c': ('O vínculo permanece com a lojista', 'Se a pessoa nomeada recusa, o contrato fica entre os originários (art. 470);', 'a reserva de nomeação não libera por si a lojista que contratou.', False),
    'd': ('A aceitação fica sem eficácia', 'O parágrafo único do art. 468 exige para a aceitação a mesma forma usada no contrato;', 'na locação escrita, a aceitação informal não vale: é a atração da forma.', False),
    'e': ('O contrato fica entre os originários', 'Insolvente e desconhecida como tal da outra parte na indicação, a nomeada não substitui (art. 470);', 'Pereira dispensa a ciência da outra parte, Venosa destaca o desconhecimento.', False),
}


def build(p):
    lx, ox, nx, y = 150, 540, 930, 120
    base = [S.line(lx, y, ox, y, stroke=S.INK, stroke_width=2), dot(lx, y), dot(ox, y), dot(nx, y, S.MUTED, dashed=True),
            label(lx, y - 22, 'lojista', 14, anchor='middle'), label(ox, y - 22, 'outra parte', 14, anchor='middle'),
            label(nx, y - 22, 'nomeada', 14, anchor='middle'), label((lx + ox) / 2, y + 26, 'locação', 13, anchor='middle')]
    wall = lambda lab: [S.line(735, y - 22, 735, y + 22, stroke=S.CONC, stroke_width=4), label(735, y + 44, lab, 13, anchor='middle', fill=S.CONC)]
    stub = [S.line(ox, y, 735, y, stroke=S.DIF, stroke_width=2, stroke_dasharray='3 5')]
    over = {
        'a': [S.circle(lx, y, 12, fill='none', stroke=S.MUTED, stroke_width=1.5, stroke_dasharray='3 3'),
              S.path(f'M{lx},{y + 14} C{lx + 100},{y + 70} {nx - 200},{y + 70} {nx - 12},{y + 8}', fill='none', stroke=S.DIF, stroke_width=2.6),
              dot(nx, y, S.DIF), label(540, y + 78, 'desde a celebração', 13, anchor='middle', fill=S.DIF)],
        'b': wall('sem indicação'),
        'c': stub + wall('recusa'),
        'd': stub + wall('forma diversa'),
        'e': stub + wall('insolvência'),
    }
    return S.svg(W, H, 'Pessoa a declarar: quem fica vinculado conforme a indicação',
                 frame('Contrato com pessoa a declarar · o que acontece na indicação', CH, AN, base, over, 252, 306, H)), []
