"""Aula 02, ch.3: who the contract reaches, an instrument (language: the contract thread and its boundary).
Sources: Venosa pp. 84-85 (successors by death; legatee; cessao; propter rem; collective contract; stipulation for a
third party), Azevedo pp. 4-6 and REsp 1.316.149/SP (terceiro ofensor). Params: none.
"""
from . import svg as S
from .tgc04_instr import W, dot, label, frame

H = 430
CH = [('a', 'Herdeiro'), ('b', 'Legatário'), ('c', 'Membro de entidade'), ('d', 'Terceiro favorecido'), ('e', 'Agência África')]
AN = {
    'a': ('Entra na posição do morto', 'O sucessor a título universal toma o lugar do falecido, como credor e como devedor, até as forças da herança;',
          'a obrigação personalíssima se extingue com a morte. Deixa de ser terceiro.', True),
    'b': ('Pode ocupar a posição do morto', 'O legatário, sucessor singular causa mortis, assume a posição do morto no contrato por disposição de última',
          'vontade. Passa a integrar a relação que antes lhe era alheia.', True),
    'c': ('Integra o conceito ampliado de parte', 'No contrato coletivo, o acordo se faz entre duas pessoas jurídicas e repercute em todos os membros;',
          'a representação exercida pela entidade determina a amplitude do efeito (CDC, art. 107).', True),
    'd': ('Recebe a prestação sem ser parte', 'Na estipulação em favor de terceiro, a prestação do promitente é devida a ele; o estipulante pode exigir',
          'o cumprimento. O favorecido não se torna devedor nem parte do contrato.', False),
    'e': ('Continua terceiro, e deve respeitar', 'O contrato existe como fato para todos: quem interfere indevidamente na relação alheia, como a África ao',
          'aliciar o cantor, é terceiro ofensor e responde (REsp 1.316.149/SP). Não vira parte.', False),
}


def build(p):
    lx, ox, nx, y = 220, 620, 940, 118
    base = [S.rect(150, 66, 540, 104, fill='none', stroke=S.INK2, stroke_width=1.3, stroke_dasharray='6 4'),
            S.line(lx, y, ox, y, stroke=S.INK, stroke_width=2), dot(lx, y), dot(ox, y), dot(nx, y, S.MUTED, dashed=True),
            label(lx, y - 24, 'contratante', 14, anchor='middle'), label(ox, y - 24, 'contratante', 14, anchor='middle'),
            label(nx, y - 24, 'estranho', 14, anchor='middle', fill=S.MUTED), label(420, y + 26, 'contrato', 13, anchor='middle'),
            label(150, 188, 'vínculo', 13, fill=S.INK2)]
    over = {
        'a': [S.circle(lx, y, 13, fill='none', stroke=S.MUTED, stroke_width=1.5, stroke_dasharray='3 3'),
              S.path(f'M{nx - 10},{y + 12} C{nx - 150},{y + 90} {lx + 90},{y + 90} {lx + 8},{y + 12}', fill='none', stroke=S.DIF, stroke_width=2.6),
              dot(lx, y, S.DIF), label(560, y + 98, 'até as forças da herança', 13, anchor='middle', fill=S.DIF)],
        'b': [S.circle(ox, y, 13, fill='none', stroke=S.MUTED, stroke_width=1.5, stroke_dasharray='3 3'),
              S.path(f'M{nx - 10},{y + 12} C{nx - 80},{y + 70} {ox + 40},{y + 70} {ox + 8},{y + 12}', fill='none', stroke=S.DIF, stroke_width=2.6),
              dot(ox, y, S.DIF), S.rect(ox + 70, y + 54, 14, 14, fill=S.PAPER, stroke=S.DIF, stroke_width=2),
              label(ox + 94, y + 66, 'última vontade', 13, fill=S.DIF)],
        'c': [S.rect(ox - 70, y - 46, 140, 92, fill='none', stroke=S.DIF, stroke_width=2, stroke_dasharray='3 4')]
             + [dot(ox + dx, y + dy, S.DIF, r=5) for dx, dy in ((-44, -22), (-44, 22), (44, -22), (44, 22), (0, 30))]
             + [dot(ox, y, S.DIF), label(ox, y + 66, 'todos os membros', 13, anchor='middle', fill=S.DIF)],
        'd': [S.line(ox, y, nx - 8, y, stroke=S.DIF, stroke_width=2.6), dot(nx, y, S.DIF),
              label(790, y - 12, 'prestação', 13, anchor='middle', fill=S.DIF),
              S.path(f'M{lx},{y + 14} C{lx + 120},{y + 70} {ox - 120},{y + 70} {ox - 8},{y + 12}', fill='none', stroke=S.DIF, stroke_width=1.6, stroke_dasharray='3 5'),
              label(420, y + 80, 'o estipulante exige', 13, anchor='middle', fill=S.DIF)],
        'e': [S.path(f'M{nx - 10},{y + 4} L{ox + 70},{y + 40} L440,{y + 4}', fill='none', stroke=S.CONC, stroke_width=2.6),
              S.line(440, y - 8, 440, y + 16, stroke=S.CONC, stroke_width=3),
              S.line(690, 70, 690, 166, stroke=S.CONC, stroke_width=4), dot(nx, y, S.CONC),
              label(810, y + 66, 'cruza o limite', 13, anchor='middle', fill=S.CONC)],
    }
    return S.svg(W, H, 'Quem o contrato alcança: sucessor, membro, favorecido e terceiro ofensor',
                 frame('O contrato e seu limite · quem a relação alcança', CH, AN, base, over, 236, 296, H)), []
