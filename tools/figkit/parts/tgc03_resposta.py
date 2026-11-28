"""Aula 03, ch.5: what the response does to a proposta, an instrument (language: time line of the offer's life).
Sources: CC arts. 430, 431, 433; Pereira III pp. 40-42. No durations: positions only order the arrivals. Params: none.
"""
from . import svg as S
from . import tgc01_hand as H
from .tgc03_mao import W, frame, arrow, cut, strike

H_ = 384
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


def build(p):
    xp, xe, xr, y = 90, 640, 960, 100
    base = [H.rule(f'M{xp},{y} H{xr}', S.INK, 1.0)]
    for i in range(12):
        x = xp + i * (xe - xp) / 11
        base.append(H.rule(f'M{x},{y - (6 if i % 11 else 12)} V{y + (6 if i % 11 else 12)}', S.INK, 1.0))
    base += [H.mark(xp, y, S.INK, r=7, solid=True), H.gloss(xp, y - 24, 'proposta', S.INK2, anchor='middle', size=14),
             H.rule(f'M{xe},{y - 28} V{y + 28}', S.INK, 2.0), H.gloss(xe, y - 36, 'fim da oferta vigente', S.INK2, anchor='middle', size=14)]
    def dot(x, col, filled=False):
        return H.mark(x, y, col, r=7, solid=filled)
    over = {
        'a': [dot(400, S.CONC), H.gloss(416, y + 30, 'resposta com termos alterados', S.CONC, size=14),
              H.mark(400, y + 62, S.DIF, r=6)] + arrow(412, 700, y + 62, S.DIF, 1.6, '3 5') +
             [H.gloss(430, y + 88, 'nova proposta: o proponente inicial decide', S.DIF, size=14)],
        'b': [dot(790, S.CONC), H.gloss(790, y - 22, 'chega depois', S.CONC, anchor='middle', size=14),
              H.mark(790, y + 40, S.DIF, r=6), H.gloss(790, y + 72, 'nova proposta', S.DIF, anchor='middle', size=14)],
        'c': [dot(330, S.DIF), H.gloss(330, y - 24, 'expedida no prazo', S.DIF, anchor='middle', size=14),
              H.rule(f'M338,{y + 22} H746', S.INK, 1.2, '3 5'), H.gloss(540, y + 44, 'atraso imprevisto', S.INK2, anchor='middle', size=14),
              dot(756, S.CONC), H.gloss(756, y - 22, 'chega tarde', S.CONC, anchor='middle', size=14)] +
             arrow(760, 1000, y + 76, S.DIF, 2.0) + [H.gloss(880, y + 100, 'comunicação imediata', S.DIF, anchor='middle', size=14)],
        'd': [dot(400, S.DIF, True), H.art(400, y - 18, '1', S.INK, anchor='middle', size=14), H.gloss(400, y + 34, 'retratação', S.DIF, anchor='middle', size=14),
              dot(520, S.CONC), H.art(520, y - 18, '2', S.INK, anchor='middle', size=14)] + strike(520, y, 10) +
             [H.gloss(520, y + 34, 'aceitação', S.CONC, anchor='middle', size=14),
              H.gloss(640, y + 74, 'ordem de chegada ao proponente', S.INK2, anchor='middle', size=14)],
    }
    return S.svg(W, H_, 'A resposta à proposta: contraproposta, atraso, retratação e o que cada artigo faz com ela',
                 frame('Resposta · o que acontece com a oferta', CH, AN, base, over, 212, 272, H_)), []
