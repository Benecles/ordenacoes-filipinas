"""Aula 03, ch.4: oferta ao publico, proposta or convite, an instrument.
Sources: CC art. 429; CDC art. 30; Pereira III p. 37; Venosa pp. 104-109. No facts beyond the page. Params: none.
"""
from . import svg as S
from . import tgc01_hand as H
from .tgc03_mao import W, frame, arrow, sheet

CH = [('a', 'Anúncio sem os requisitos essenciais'), ('b', 'Anúncio com os requisitos essenciais'),
      ('c', 'Publicidade que descreve o imóvel')]
AN = {
    'a': ('Invitatio ad offerendum', 'O anúncio traduz uma sugestão para que venham propostas: quem responde é que propõe.',
          'Sem os requisitos essenciais ao contrato, o art. 429 não o trata como proposta.', False),
    'b': ('Proposta', 'Art. 429: a oferta ao público equivale a proposta quando encerra os requisitos essenciais ao contrato.',
          'O público pode aceitar sucessivamente, e a recusa só se justifica por motivo legítimo.', True),
    'c': ('Cláusula do contrato', 'Art. 30 do CDC: a informação suficientemente precisa obriga o fornecedor e integra o contrato.',
          'O aquecimento central descrito na publicidade vincula; o elogio genérico da moradia não.', True),
}


def build(p):
    y = 104
    base = sheet(70, y - 28, 120, 3) + [H.gloss(130, y + 40, 'anúncio', S.INK2, anchor='middle', size=14)]
    pts = [(420, y - 34), (500, y + 22), (580, y - 38), (650, y + 34), (720, y - 30), (790, y + 18)]
    for x, yy in pts:
        base.append(H.mark(x, yy, S.INK, r=6.5))
    base += [H.mark(946, y, S.INK2), H.gloss(946, y - 24, 'contrato', S.INK2, anchor='middle', size=14),
             H.gloss(605, y + 66, 'público indeterminado', S.INK2, anchor='middle', size=14)]
    over = {'a': [], 'b': [], 'c': []}
    for x, yy in pts[:4]:
        over['a'].append(H.rule(f'M{x - 10},{yy} L200,{y}', S.CONC, 1.0, '3 5'))
    over['a'].append(H.gloss(300, y - 44, 'propostas voltam', S.CONC, size=14))
    over['b'] += arrow(196, 930, y, S.DIF, 2.0) + [H.gloss(300, y - 14, 'qualquer aceitação conclui', S.DIF, size=14)]
    over['c'] += [H.rule(f'M196,{y} H560', S.DIF, 2.0), H.bracket(560, 690, y + 22, up=False, col=S.DIF),
                  H.gloss(626, y + 50, 'aquecimento', S.INK2, anchor='middle', size=14)] + \
                 arrow(690, 930, y, S.DIF, 2.0, '3 5') + [H.gloss(810, y - 14, 'integra o contrato', S.DIF, anchor='middle', size=14)]
    return S.svg(W, 372, 'Oferta ao público: o anúncio como proposta, como convite ou como cláusula do contrato',
                 frame('Oferta ao público · o que o anúncio faz', CH, AN, base, over, 196, 262, 372)), []
