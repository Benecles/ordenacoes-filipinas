"""Aula 09, ch.1: what becomes of the contract once an abusive clause is struck, an instrument.
Sources: CDC art. 51, IV and §§1-2; art. 39, IV; CC art. 184 (utile per inutile non vitiatur); Venosa p. 58;
Luis Renato p. 13 (abuse: a lawful act that turns unlawful in its concrete circumstances); cláusula mandato
(Venosa/Luis Renato: indispensable to a sequence of deals or powers unrelated to the contracted purpose).
Params: none.
"""
from . import svg as S
from .tgc04_instr import W, label, frame

H = 470
CH = [('a', 'Retirada sem ônus excessivo'), ('b', 'Retirada deixa ônus excessivo'),
      ('c', 'Cláusula mandato'), ('d', 'Exploração da fraqueza')]
AN = {
    'a': ('A cláusula cai e o contrato permanece', 'A nulidade não invalida o contrato (CDC, art. 51, §2º); a lacuna é integrada pelos arts. 112, 113 e 422,', 'e a parte separável sobrevive (CC, art. 184; utile per inutile non vitiatur).', True),
    'b': ('O contrato inteiro pode ser invalidado', 'Se, apesar dos esforços de integração, a ausência da cláusula impuser ônus excessivo a qualquer das partes,', 'o art. 51, §2º, do CDC admite a invalidação do contrato.', False),
    'c': ('Examina-se a relação com a finalidade contratada', 'A cláusula pode ser indispensável a uma sequência de negócios ou impor poderes sem relação com a finalidade;', 'a ausência de rol civil de cláusulas abusivas não impede esse controle.', False),
    'd': ('É o aspecto subjetivo da lesão no consumo', 'O art. 39, IV, descreve a exploração da fraqueza ou da ignorância do consumidor, segundo idade e saúde;', 'o aspecto objetivo está no art. 51, §1º, sem tarifamento de sobrepreço (Venosa).', False),
}


def _sheet(x, y, w, rows=5, bad=2, state='plain', col=None):
    """A contract sheet: header bar, ruled clause lines; row `bad` is the abusive clause."""
    o = [S.rect(x, y, w, 188, fill=S.PAPER, stroke=S.INK, stroke_width=1.8),
         S.rect(x + 14, y + 12, w * 0.4, 8, fill=S.INK, stroke='none')]
    for i in range(rows):
        ry = y + 40 + i * 28
        if i == bad:
            if state == 'plain':
                o += S.hatch(x + 10, ry - 12, w - 20, 24, step=8, stroke=S.GRID, stroke_width=1)
                o.append(S.rect(x + 10, ry - 12, w - 20, 24, fill='none', stroke=S.CONC, stroke_width=2.2, stroke_dasharray='5 3'))
            elif state == 'gap':
                o.append(S.rect(x + 10, ry - 12, w - 20, 24, fill='none', stroke=col or S.DIF, stroke_width=2, stroke_dasharray='3 4'))
            continue
        o.append(S.line(x + 18, ry, x + w - 18, ry, stroke=S.GRID, stroke_width=2))
        o.append(S.line(x + 18, ry, x + w - 18 - (i * 37 % 60), ry, stroke=S.INK2, stroke_width=3))
    return o


def build(p):
    base = ['<g transform="translate(0,20)">'] + _sheet(40, 52, 360)
    base += [label(40, 44, 'contrato', 14, weight='600'), label(222, 44, 'cláusula abusiva', 13, anchor='middle', fill=S.CONC)]
    base += [S.line(404, 146, 440, 146, stroke=S.INK, stroke_width=1.4), S.path('M432,140 L440,146 L432,152', fill='none', stroke=S.INK, stroke_width=1.4), '</g>']
    R = 470  # right sheet
    over = {}
    # a: clause lifted out, gap closed by integration; sheet stays
    s_a = _sheet(R, 52, 300, state='gap', col=S.DIF)
    over['a'] = s_a + [
        S.rect(R + 330, 76, 200, 34, fill=S.PAPER, stroke=S.CONC, stroke_width=2, stroke_dasharray='5 3'),
        S.line(R + 330, 93, R + 530, 93, stroke=S.CONC, stroke_width=2),
        S.path(f'M{R + 322},93 C{R + 300},93 {R + 306},148 {R + 288},148', fill='none', stroke=S.CONC, stroke_width=1.4, stroke_dasharray='3 3'),
        label(R + 430, 70, 'retirada', 13, anchor='middle', fill=S.CONC),
        label(R + 340, 160, 'arts. 112, 113 e 422', 13, fill=S.DIF), label(R + 340, 180, 'integram a lacuna', 13, fill=S.DIF),
        label(R + 340, 214, 'art. 184: o útil não se vicia pelo inútil', 13, fill=S.INK2)]
    # b: whole sheet struck, weight on one side
    s_b = _sheet(R, 52, 300, state='gap', col=S.CONC)
    over['b'] = s_b + [
        S.line(R, 52, R + 300, 240, stroke=S.CONC, stroke_width=3), S.line(R + 300, 52, R, 240, stroke=S.CONC, stroke_width=3),
        S.path(f'M{R + 340},200 L{R + 520},200 L{R + 500},176 L{R + 360},176 Z', fill=S.PAPER, stroke=S.CONC, stroke_width=2.2),
        S.path(f'M{R + 340},200 L{R + 520},200', fill='none', stroke=S.INK, stroke_width=3),
        label(R + 430, 166, 'ônus excessivo', 13, anchor='middle', fill=S.CONC),
        S.line(R + 340, 232, R + 520, 232, stroke=S.INK, stroke_width=2), S.circle(R + 340, 232, 6, fill=S.PAPER, stroke=S.INK, stroke_width=2),
        S.circle(R + 520, 232, 6, fill=S.PAPER, stroke=S.INK, stroke_width=2),
        label(R + 340, 252, 'uma parte', 12), label(R + 520, 252, 'a outra', 12, anchor='end'),
        label(R + 420, 108, 'invalidação', 14, anchor='middle', weight='600', fill=S.CONC)]
    # c: clause strip with threads to other deals and powers; the contracted purpose stays apart
    over['c'] = [
        S.rect(R, 98, 150, 34, fill=S.PAPER, stroke=S.CONC, stroke_width=2.2, stroke_dasharray='5 3'),
        *S.hatch(R + 4, 102, 142, 26, step=8, stroke=S.GRID, stroke_width=1),
        label(R + 75, 90, 'cláusula mandato', 13, anchor='middle', fill=S.CONC),
        S.path(f'M{R + 150},108 C{R + 230},108 {R + 230},62 {R + 330},62', fill='none', stroke=S.INK, stroke_width=1.8),
        S.path(f'M{R + 150},115 H{R + 330}', fill='none', stroke=S.INK, stroke_width=1.8),
        S.path(f'M{R + 150},122 C{R + 230},122 {R + 230},170 {R + 330},170', fill='none', stroke=S.INK, stroke_width=1.8),
        S.rect(R + 330, 46, 200, 32, fill=S.PAPER, stroke=S.INK, stroke_width=1.6), label(R + 430, 67, 'negócio 2', 13, anchor='middle'),
        S.rect(R + 330, 99, 200, 32, fill=S.PAPER, stroke=S.INK, stroke_width=1.6), label(R + 430, 120, 'negócio 3', 13, anchor='middle'),
        S.rect(R + 330, 154, 200, 32, fill=S.PAPER, stroke=S.INK, stroke_width=1.6), label(R + 430, 175, 'poderes do mandato', 13, anchor='middle'),
        S.path(f'M{R + 75},134 V222', fill='none', stroke=S.CONC, stroke_width=1.6, stroke_dasharray='4 4'),
        S.circle(R + 75, 224, 8, fill=S.PAPER, stroke=S.INK, stroke_width=2.2),
        label(R + 96, 229, 'finalidade contratada', 13)]
    # d: consumer weakness; subjective (art. 39) and objective (art. 51 par. 1) aspects
    cx = R + 40
    over['d'] = [
        label(cx - 10, 64, 'consumidor', 14, weight='600'),
        *[o for i, (lab, pos) in enumerate([('idade', 40), ('saúde', 70), ('conhecimento', 30)]) for o in (
            label(cx - 10, 100 + i * 46, lab, 13), S.line(cx - 10, 112 + i * 46, cx + 170, 112 + i * 46, stroke=S.GRID, stroke_width=2.4),
            S.line(cx - 10, 106 + i * 46, cx - 10, 118 + i * 46, stroke=S.INK2, stroke_width=1.6),
            S.line(cx + 170, 106 + i * 46, cx + 170, 118 + i * 46, stroke=S.INK2, stroke_width=1.6),
            S.circle(cx - 10 + pos * 1.8, 112 + i * 46, 7, fill=S.PAPER, stroke=S.DIF, stroke_width=2.4))],
        S.rect(R + 250, 50, 240, 70, fill=S.PAPER, stroke=S.DIF, stroke_width=2.4),
        label(R + 370, 78, 'subjetivo · art. 39, IV', 14, anchor='middle', weight='600', fill=S.DIF),
        label(R + 370, 100, 'exploração da fraqueza', 13, anchor='middle'),
        S.rect(R + 250, 140, 240, 70, fill=S.PAPER, stroke=S.INK, stroke_width=1.6, stroke_dasharray='4 3'),
        label(R + 370, 168, 'objetivo · art. 51, §1º', 14, anchor='middle', weight='600'),
        label(R + 370, 190, 'sem tarifa de sobrepreço', 13, anchor='middle', fill=S.INK2),
        S.path(f'M{R + 190},112 H{R + 250}', fill='none', stroke=S.DIF, stroke_width=2.2)]
    over = {k: ['<g transform="translate(0,20)">'] + v + ['</g>'] for k, v in over.items()}
    return S.svg(W, H, 'Cláusula abusiva: o que ocorre com o contrato conforme a retirada e a conduta',
                 frame('Cláusula abusiva · o que acontece com o contrato', CH, AN, base, over, 292, 346, H)), []
