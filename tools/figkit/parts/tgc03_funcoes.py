"""Aula 03, ch.1: the three functions of boa-fe objetiva applied to the consorcio facts, an instrument.
Sources: Pereira III pp. 20-21 (padrao de conduta, deveres positivos); Venosa pp. 11-13; CC arts. 113, 187, 422;
RI 71001586668 (TJRS). No durations or amounts. Params: none.
"""
from . import svg as S
from .tgc04_instr import W, label, frame

H = 372
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


def sq(x, y, s, col, dashed=False):
    return S.rect(x, y, s, s, fill=S.PAPER, stroke=col, stroke_width=2.2, stroke_dasharray='3 3' if dashed else None)


def build(p):
    cx, y0, bw, bh = 540, 64, 300, 64
    base = [S.rect(cx - bw / 2, y0, bw, bh, fill=S.PAPER, stroke=S.INK, stroke_width=2.6),
            S.text(cx, y0 + 38, 'prestação principal', size=15, family=S.SANS, anchor='middle', weight='600')]
    over = {
        'a': [],
        'b': [],
        'c': [],
    }
    # a: deveres anexos as small squares tied to the main box; the prestacao itself stays whole
    for i, (nm, x) in enumerate([('sigilo', 430), ('cuidado', 510), ('contas', 590), ('segurança', 670)]):
        over['a'] += [S.line(x + 10, y0 + 32, cx - bw / 2 if x < cx else cx + bw / 2, y0 + 32, stroke=S.DIF, stroke_width=1.6, stroke_dasharray='3 4') if False else '',
                      sq(x - 10 + (0 if i else 0), y0 + bh + 22, 20, S.DIF, dashed=(i == 0)),
                      S.line(x, y0 + bh, x, y0 + bh + 22, stroke=S.DIF, stroke_width=1.6),
                      label(x, y0 + bh + 58, nm, 13, anchor='middle', fill=S.INK2)]
    over['a'] += [S.line(300, y0 + bh + 11, 330, y0 + bh + 11, stroke=S.CONC, stroke_width=3)] if False else []
    over['a'] += S.hatch(320, y0 + bh + 12, 20, 20, step=6, stroke=S.CONC, stroke_width=1.4) if False else []
    # b: repeated boletos as hollow dots on a ruled line, then the late charge cuts across; the garantia is held
    for i in range(6):
        x = 120 + i * 44
        over['b'].append(S.circle(x, y0 + 32, 7, fill=S.PAPER, stroke=S.DIF, stroke_width=2.2))
    over['b'] += [S.line(120, y0 + 32, 340, y0 + 32, stroke=S.DIF, stroke_width=1.2),
                  S.line(368, y0 - 6, 368, y0 + 70, stroke=S.CONC, stroke_width=4),
                  label(368, y0 + 90, 'cobrança ao fim', 13, anchor='middle', fill=S.INK2),
                  label(230, y0 + 60, 'boletos sem ressalva', 13, anchor='middle', fill=S.INK2),
                  sq(870, y0 + 18, 28, S.DIF), label(884, y0 + 70, 'garantia', 13, anchor='middle', fill=S.INK2),
                  S.line(cx + bw / 2, y0 + 32, 870, y0 + 32, stroke=S.DIF, stroke_width=2, stroke_dasharray='3 5')]
    # c: a declaration drawn as ruled lines, read through a notched flag of usos
    for i in range(4):
        over['c'].append(S.line(150, y0 + 10 + i * 15, 150 + 190 - (i % 2) * 40, y0 + 10 + i * 15, stroke=S.INK, stroke_width=1.4))
    over['c'] += [S.rect(140, y0, 210, 66, fill='none', stroke=S.INK, stroke_width=1.6),
                  S.path(f'M{cx + bw / 2},{y0 + 32} H{cx + bw / 2 + 60}', fill='none', stroke=S.DIF, stroke_width=2),
                  S.path(f'M{cx + bw / 2 + 60},{y0 + 8} V{y0 + 56} H{cx + bw / 2 + 150} L{cx + bw / 2 + 134},{y0 + 32} L{cx + bw / 2 + 150},{y0 + 8} Z',
                         fill=S.PAPER, stroke=S.DIF, stroke_width=2.2),
                  label(cx + bw / 2 + 98, y0 + 38, 'usos', 14, anchor='middle', fill=S.INK2),
                  S.line(350, y0 + 32, cx - bw / 2, y0 + 32, stroke=S.INK, stroke_width=1.5)]
    return S.svg(W, H, 'As três funções da boa-fé objetiva: integrativa, de controle e interpretativa',
                 frame('Boa-fé objetiva · uma situação, uma função', CH, AN, base, over, 196, 250, H)), []
