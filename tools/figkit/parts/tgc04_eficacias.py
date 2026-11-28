"""Aula 04, ch.4: registry of the preliminary, an instrument.
The reader picks the situation; the rings answer. Sources: Pereira III p. 84, Venosa p. 45 (registry gives effect
against third parties, its absence leaves the effect between the parties; compromisso imobiliário registered gives
real right of aquisição, CC arts. 1.417 and 1.418; adjudicação compulsória lies against the promitente without prior
registry). Params: none.
"""
from . import svg as S
from .tgc04_instr import W, dot, label, frame
from .tgc01_hand import cord

H = 420
CH = [('a', 'Sem registro'), ('b', 'Com registro'), ('c', 'Adjudicação compulsória')]
AN = {
    'a': ('Eficácia entre as partes', 'A falta de registro do preliminar não lhe tira a eficácia entre os contratantes.', 'O direito real à aquisição não nasce sem o registro do compromisso imobiliário.', False),
    'b': ('Direito real e efeitos perante terceiros', 'O registro competente dá ao preliminar efeitos perante terceiros;', 'no compromisso imobiliário, atribui direito real à aquisição (arts. 1.417 e 1.418).', True),
    'c': ('A adjudicação não espera o registro', 'Substitui a outorga recusada e pode ser obtida contra o promitente independentemente de registro prévio.', 'A eficácia obrigacional e a real têm alcances diferentes.', True),
}


def build(p):
    cx, cy = 540, 128
    base = [S.circle(cx, cy, 62, fill='none', stroke=S.INK, stroke_width=1),
            cord(cx - 22, cx + 22, cy, amp=5, half=11, taper=10),
            dot(cx - 28, cy), dot(cx + 28, cy), label(cx, cy - 18, 'partes', 13, anchor='middle'),
            dot(860, cy), label(860, cy - 20, 'terceiro', 13, anchor='middle')]
    over = {
        'a': [S.circle(cx, cy, 98, fill='none', stroke=S.MUTED, stroke_width=1, stroke_dasharray='4 6')],
        'b': [S.circle(cx, cy, 98, fill='none', stroke=S.DIF, stroke_width=2),
              S.line(cx + 98, cy, 852, cy, stroke=S.DIF, stroke_width=2)],
        'c': [S.circle(cx, cy, 98, fill='none', stroke=S.MUTED, stroke_width=1, stroke_dasharray='4 6'),
              S.path(f'M{cx - 28},{cy + 8} C{cx - 100},{cy + 80} {cx - 200},{cy + 80} 250,{cy + 8}', fill='none',
                     stroke=S.DIF, stroke_width=2, stroke_dasharray='3 5'),
              S.rect(240, cy - 10, 20, 20, fill=S.PAPER, stroke=S.DIF, stroke_width=2),
              label(250, cy - 22, 'bem', 13, anchor='middle', fill=S.DIF)],
    }
    return S.svg(W, H, 'Registro do preliminar: efeitos entre as partes, direito real, adjudicação',
                 frame('Compromisso de compra e venda · o que o registro muda', CH, AN, base, over, 252, 306, H)), []
