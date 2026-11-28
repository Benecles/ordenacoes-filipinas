"""Aula 02, ch.3: who the contract reaches, an instrument (language: the cord and its limit; tgc01_hand).
Sources: Venosa pp. 84-85 (successors by death; legatee; cessao; propter rem; collective contract; stipulation for a
third party), Azevedo pp. 4-6 and REsp 1.316.149/SP (terceiro ofensor). Params: none."""
from . import svg as S
from .tgc01_hand import cord, rule, mark, name, gloss, bracket
from .tgc02_hand import W, frame

H = 410
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
    lx, ox, nx, y = 220, 620, 940, 78
    base = [cord(lx + 8, ox - 8, y, amp=7, half=24, taper=30), mark(lx, y, S.DIF), mark(ox, y, S.DIF), mark(nx, y, S.MUTED),
            name(lx, y - 22, 'contratante', anchor='middle'), name(ox, y - 22, 'contratante', anchor='middle'),
            name(nx, y - 22, 'estranho', col=S.MUTED, anchor='middle'), gloss(420, y - 14, 'contrato', anchor='middle'),
            bracket(lx, ox, y + 44, up=True), gloss(lx - 14, y + 52, 'vínculo', anchor='end', col=S.INK2), gloss(690, y - 42, 'limite do contrato', anchor='middle', col=S.INK2),
            rule(f'M690,{y - 36} V{y + 50}', S.INK2, 1.0)]
    over = {
        'a': [S.path(f'M{nx - 10},{y + 12} C{nx - 150},{y + 86} {lx + 90},{y + 86} {lx + 8},{y + 12}', fill='none', stroke=S.DIF, stroke_width=2),
              mark(lx, y, S.DIF, solid=True), gloss(560, y + 98, 'até as forças da herança', col=S.DIF, anchor='middle')],
        'b': [S.path(f'M{nx - 10},{y + 12} C{nx - 80},{y + 66} {ox + 40},{y + 66} {ox + 8},{y + 12}', fill='none', stroke=S.DIF, stroke_width=2),
              mark(ox, y, S.DIF, solid=True), gloss(ox + 30, y + 84, 'última vontade', col=S.DIF)],
        'c': [S.circle(ox, y + 6, 58, fill='none', stroke=S.DIF, stroke_width=1.0)]
             + [mark(ox + dx, y + 6 + dy, S.DIF, 4.5) for dx, dy in ((-34, -20), (-34, 20), (34, -20), (34, 20), (0, 32))]
             + [mark(ox, y, S.DIF, solid=True), gloss(ox, y + 90, 'todos os membros', col=S.DIF, anchor='middle')],
        'd': [cord(ox + 8, nx - 8, y, amp=7, half=24, taper=30), mark(nx, y, S.DIF), gloss(790, y - 14, 'prestação', col=S.DIF, anchor='middle'),
              S.path(f'M{lx},{y + 14} C{lx + 120},{y + 66} {ox - 120},{y + 66} {ox - 8},{y + 12}', fill='none', stroke=S.DIF, stroke_width=1.0),
              gloss(420, y + 82, 'o estipulante exige', col=S.DIF, anchor='middle')],
        'e': [S.path(f'M{nx - 10},{y + 4} L{ox + 70},{y + 36} L440,{y + 4}', fill='none', stroke=S.CONC, stroke_width=2),
              rule(f'M440,{y - 10} V{y + 14}', S.CONC, 2), mark(nx, y, S.CONC),
              gloss(810, y + 66, 'cruza o limite', col=S.CONC, anchor='middle')],
    }
    return S.svg(W, H, 'Quem o contrato alcança: sucessor, membro, favorecido e terceiro ofensor',
                 frame(CH, AN, base, over, 214, 282, H)), []
