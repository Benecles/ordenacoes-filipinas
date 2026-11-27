"""Aula 03, ch.5: what the response does to a proposta, an instrument (language: time line of the offer's life).
Sources: CC arts. 430, 431, 433; Pereira III pp. 40-42. No durations: positions only order the arrivals. Params: none.
"""
from . import svg as S
from .tgc04_instr import W, label, frame

H = 384
CH = [('a', 'Termos alterados'), ('b', 'Fora do prazo'), ('c', 'Atraso imprevisto no envio'), ('d', 'Retratação chega antes')]
AN = {
    'a': ('Nova proposta', 'Art. 431: a resposta com adições, restrições ou modificações importa nova proposta.',
          'O proponente inicial pode recusar os novos termos.', False),
    'b': ('Nova proposta', 'Art. 431: a aceitação fora do prazo também importa nova proposta.',
          'Ela não encontra a oferta anterior vigente.', False),
    'c': ('Dever de comunicar', 'Art. 430: a aceitação chega tarde por circunstância imprevista, e o proponente comunica o fato imediatamente.',
          'A omissão pode gerar responsabilidade por perdas e danos.', True),
    'd': ('Aceitação inexistente', 'Art. 433: a retratação que chega antes da aceitação, ou junto com ela, torna a aceitação inexistente.',
          'A eficácia da retratação depende da ordem de chegada ao proponente.', True),
}


def arrow(x1, x2, y, col, dashed=False, w=2.4):
    d = 1 if x2 > x1 else -1
    return [S.line(x1, y, x2, y, stroke=col, stroke_width=w, stroke_dasharray='3 5' if dashed else None),
            S.path(f'M{x2 - 10 * d},{y - 8} L{x2},{y} L{x2 - 10 * d},{y + 8}', fill='none', stroke=col, stroke_width=w)]


def dot(x, y, col, filled=False):
    return S.circle(x, y, 8, fill=col if filled else S.PAPER, stroke=col, stroke_width=2.4)


def build(p):
    xp, xe, xr, y = 90, 640, 960, 100
    base = [S.line(xp, y, xr, y, stroke=S.INK, stroke_width=1.6)]
    for i in range(0, 12):
        x = xp + i * (xe - xp) / 11
        base.append(S.line(x, y - 6 if i % 11 else y - 14, x, y + 6 if i % 11 else y + 14, stroke=S.INK, stroke_width=1))
    base += [S.rect(xp - 12, y - 12, 24, 24, fill=S.PAPER, stroke=S.INK, stroke_width=2.4),
             S.line(xe, y - 30, xe, y + 30, stroke=S.INK, stroke_width=4),
             label(xp, y - 24, 'proposta', 13, anchor='middle', fill=S.INK2),
             label(xe, y - 38, 'fim da oferta vigente', 13, anchor='middle', fill=S.INK2)]
    over = {
        'a': [dot(400, y, S.CONC)] + S.hatch(386, y + 14, 28, 18, step=6, stroke=S.CONC, stroke_width=1.3) +
             [S.rect(386, y + 14, 28, 18, fill='none', stroke=S.CONC, stroke_width=1.8),
              label(430, y + 28, 'resposta com termos alterados', 13, fill=S.CONC),
              S.rect(386, y + 52, 28, 18, fill=S.PAPER, stroke=S.DIF, stroke_width=2.2, stroke_dasharray='3 3')] +
             arrow(418, 700, y + 61, S.DIF, dashed=True) + [label(430, y + 88, 'nova proposta: o proponente inicial decide', 13, fill=S.DIF)],
        'b': [dot(790, y, S.CONC), label(790, y - 22, 'chega depois', 13, anchor='middle', fill=S.CONC),
              S.rect(776, y + 30, 28, 18, fill=S.PAPER, stroke=S.DIF, stroke_width=2.2, stroke_dasharray='3 3'),
              label(790, y + 72, 'nova proposta', 13, anchor='middle', fill=S.DIF)],
        'c': [dot(330, y, S.DIF), label(330, y - 24, 'expedida no prazo', 13, anchor='middle', fill=S.DIF),
              S.path(f'M338,{y + 22} H746', fill='none', stroke=S.INK, stroke_width=1.6, stroke_dasharray='3 5'),
              label(540, y + 42, 'atraso imprevisto', 13, anchor='middle', fill=S.INK2),
              dot(756, y, S.CONC), label(756, y - 22, 'chega tarde', 13, anchor='middle', fill=S.CONC)] +
             arrow(760, 1000, y + 74, S.DIF) + [label(880, y + 98, 'comunicação imediata', 13, anchor='middle', fill=S.DIF)],
        'd': [dot(400, y, S.DIF, True), S.text(400, y - 18, '1', size=14, family=S.SANS, anchor='middle', fill=S.INK),
              label(400, y + 34, 'retratação', 13, anchor='middle', fill=S.DIF),
              dot(520, y, S.CONC), S.text(520, y - 18, '2', size=14, family=S.SANS, anchor='middle', fill=S.INK),
              S.line(508, y - 12, 532, y + 12, stroke=S.CONC, stroke_width=2.6), S.line(508, y + 12, 532, y - 12, stroke=S.CONC, stroke_width=2.6),
              label(520, y + 34, 'aceitação', 13, anchor='middle', fill=S.CONC),
              label(640, y + 74, 'ordem de chegada ao proponente', 13, anchor='middle', fill=S.INK2)],
    }
    return S.svg(W, H, 'A resposta à proposta: contraproposta, atraso, retratação e o que cada artigo faz com ela',
                 frame('Resposta · o que acontece com a oferta', CH, AN, base, over, 212, 262, H)), []
