"""Aula 03, ch.4: oferta ao publico, proposta or convite, an instrument.
Sources: CC art. 429; CDC art. 30; Pereira III p. 37; Venosa pp. 104-109. No facts beyond the page. Params: none.
"""
from . import svg as S
from .tgc04_instr import W, label, frame

H = 372
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
    base = [S.rect(70, y - 34, 120, 68, fill=S.PAPER, stroke=S.INK, stroke_width=2.4)]
    for i in range(3):
        base.append(S.line(86, y - 18 + i * 17, 174 - (i == 2) * 40, y - 18 + i * 17, stroke=S.INK, stroke_width=1.3))
    pts = [(420, y - 34), (500, y + 22), (580, y - 38), (650, y + 34), (720, y - 30), (790, y + 18)]
    for x, yy in pts:
        base.append(S.circle(x, yy, 8, fill=S.PAPER, stroke=S.INK, stroke_width=2))
    base += [S.rect(930, y - 16, 32, 32, fill=S.PAPER, stroke=S.INK, stroke_width=2.2, stroke_dasharray='3 3'),
             label(946, y - 28, 'contrato', 13, anchor='middle', fill=S.INK2),
             label(130, y + 56, 'anúncio', 13, anchor='middle', fill=S.INK2),
             label(605, y + 66, 'público indeterminado', 13, anchor='middle', fill=S.INK2)]
    over = {'a': [], 'b': [], 'c': []}
    for x, yy in pts[:4]:
        over['a'] += [S.path(f'M{x - 12},{yy} L{200},{y}', fill='none', stroke=S.CONC, stroke_width=1.5, stroke_dasharray='3 5')]
    over['a'].append(label(300, y - 44, 'propostas voltam', 13, fill=S.CONC))
    over['b'] += [S.line(190, y, 930, y, stroke=S.DIF, stroke_width=2.4),
                  S.path('M918,%d L930,%d L918,%d' % (y - 9, y, y + 9), fill='none', stroke=S.DIF, stroke_width=2.4),
                  label(300, y - 14, 'qualquer aceitação conclui', 13, fill=S.DIF)]
    over['c'] += [S.path(f'M190,{y} H560', fill='none', stroke=S.DIF, stroke_width=2.2),
                  S.path(f'M560,{y - 18} V{y + 18} H690 L674,{y} L690,{y - 18} Z', fill=S.PAPER, stroke=S.DIF, stroke_width=2.2),
                  label(626, y + 4, 'aquecimento', 12, anchor='middle', fill=S.INK2),
                  S.path(f'M690,{y} H918', fill='none', stroke=S.DIF, stroke_width=2.2, stroke_dasharray='3 5'),
                  S.path('M918,%d L930,%d L918,%d' % (y - 9, y, y + 9), fill='none', stroke=S.DIF, stroke_width=2.2),
                  label(810, y - 14, 'integra o contrato', 13, anchor='middle', fill=S.DIF)]
    return S.svg(W, H, 'Oferta ao público: o anúncio como proposta, como convite ou como cláusula do contrato',
                 frame('Oferta ao público · o que o anúncio faz', CH, AN, base, over, 196, 250, H)), []
