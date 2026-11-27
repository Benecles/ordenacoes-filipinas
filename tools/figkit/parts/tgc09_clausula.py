"""Aula 09, ch.1: what becomes of the contract once an abusive clause is struck, an instrument.
Sources: CDC art. 51, IV and §§1-2; art. 39, IV; CC art. 184 (utile per inutile non vitiatur); Venosa p. 58;
Luis Renato p. 13 (abuse: a lawful act that turns unlawful in its concrete circumstances); cláusula mandato
(Venosa/Luis Renato: indispensable to a sequence of deals or powers unrelated to the contracted purpose).
Params: none.
"""
from . import svg as S
from .tgc04_instr import W, label, frame

H = 430
CH = [('a', 'Retirada sem ônus excessivo'), ('b', 'Retirada deixa ônus excessivo'),
      ('c', 'Cláusula mandato'), ('d', 'Exploração da fraqueza')]
AN = {
    'a': ('A cláusula cai e o contrato permanece', 'A nulidade não invalida o contrato (CDC, art. 51, §2º); a lacuna é integrada pelos arts. 112, 113 e 422,', 'e a parte separável sobrevive (CC, art. 184; utile per inutile non vitiatur).', True),
    'b': ('O contrato inteiro pode ser invalidado', 'Se, apesar dos esforços de integração, a ausência da cláusula impuser ônus excessivo a qualquer das partes,', 'o art. 51, §2º, do CDC admite a invalidação do contrato.', False),
    'c': ('Examina-se a relação com a finalidade contratada', 'A cláusula pode ser indispensável a uma sequência de negócios ou impor poderes sem relação com a finalidade;', 'a ausência de rol civil de cláusulas abusivas não impede esse controle.', False),
    'd': ('É o aspecto subjetivo da lesão no consumo', 'O art. 39, IV, descreve a exploração da fraqueza ou da ignorância do consumidor, segundo idade e saúde;', 'o aspecto objetivo está no art. 51, §1º, sem tarifamento de sobrepreço (Venosa).', False),
}


def build(p):
    y, h = 96, 46
    segs = [(40, 170), (220, 170), (400, 170), (590, 170), (780, 260)]
    cx = 400  # the clause (third segment)
    base = []
    for i, (x, w) in enumerate(segs):
        if i == 2:
            base += S.hatch(x, y, w, h, step=10, stroke=S.GRID, stroke_width=1)
            base.append(S.rect(x, y, w, h, fill='none', stroke=S.CONC, stroke_width=2.2, stroke_dasharray='5 3'))
        else:
            base.append(S.rect(x, y, w, h, fill=S.PAPER, stroke=S.INK, stroke_width=1.8))
    base += [label(40, y - 14, 'contrato', 14, weight='600'), label(cx + 85, y - 14, 'cláusula abusiva', 13, anchor='middle', fill=S.CONC)]
    yy = y + h + 38
    over = {
        'a': [S.path(f'M{cx},{y + h + 6} C{cx + 20},{yy} {cx + 150},{yy} {cx + 170},{y + h + 6}', fill='none', stroke=S.DIF, stroke_width=2.4, stroke_dasharray='4 4'),
              label(cx + 85, yy + 30, 'integração da lacuna', 13, anchor='middle', fill=S.DIF)],
        'b': [S.line(40, y + h / 2, 1040, y + h / 2, stroke=S.CONC, stroke_width=3),
              label(cx + 85, yy + 10, 'a ausência pesa sobre uma das partes', 13, anchor='middle', fill=S.CONC)],
        'c': [S.path(f'M{cx + 85},{y + h + 6} V{yy + 6} H{780}', fill='none', stroke=S.INK, stroke_width=1.6),
              S.circle(780, yy + 6, 6, fill=S.PAPER, stroke=S.INK, stroke_width=2),
              label(790, yy + 28, 'finalidade contratada', 13)],
        'd': [S.circle(cx + 85, yy, 7, fill=S.PAPER, stroke=S.INK, stroke_width=2), S.line(cx + 85, y + h + 6, cx + 85, yy - 7, stroke=S.INK, stroke_width=1.6),
              label(cx + 100, yy + 5, 'consumidor: idade, saúde, conhecimento', 13)],
    }
    return S.svg(W, H, 'Cláusula abusiva: o que ocorre com o contrato conforme a retirada e a conduta',
                 frame('Cláusula abusiva · o que acontece com o contrato', CH, AN, base, over, 252, 306, H)), []
