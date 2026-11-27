"""Aula 02, ch.2: what the binding force answers when a party wants out, an instrument (language: the held thread).
Sources: Pereira III (pacta sunt servanda; who prefers another deal stays bound or pays perdas e danos), REsp 803.481/GO
(variation in the soy price is a foreseeable risk; a larger resale margin is not extraordinary), CC 1.417-1.418
(registro da promessa for execucao especifica with eficacia real). Params: none.
"""
from . import svg as S
from .tgc04_instr import W, dot, label, frame

H = 430
CH = [('a', 'Prefere outro negócio'), ('b', 'Dólar sobe e a safra encarece'), ('c', 'Comprador revende com lucro maior')]
AN = {
    'a': ('Continua obrigado ou indeniza', 'A força obrigatória torna a prestação exigível: quem prefere outro negócio depois cumpre o contrato',
          'ou responde pelas perdas e danos. A segurança jurídica limita o arrependimento.', False),
    'b': ('Não há onerosidade excessiva', 'No REsp 803.481/GO, a variação do preço da soja era risco previsível e fazia parte do contrato de safra futura;',
          'eleição e guerra no oriente médio não a tornaram imprevisível. O vendedor entrega o prometido.', False),
    'c': ('O lucro alheio não rompe a troca', 'O simples fato de o comprador obter maior margem na revenda não é fato extraordinário,',
          'e decorre da natureza da venda de safra futura. O vínculo permanece como pactuado.', False),
}


def build(p):
    lx, rx, y = 260, 820, 118
    base = [S.line(lx, y, rx, y, stroke=S.INK, stroke_width=5), dot(lx, y), dot(rx, y),
            label(lx, y - 28, 'devedor', 14, anchor='middle'), label(rx, y - 28, 'credor', 14, anchor='middle'),
            label(540, y - 16, 'pacta sunt servanda', 13, anchor='middle', fill=S.INK2)]
    cut = lambda: [S.line(520, y + 70, 540, y + 14, stroke=S.CONC, stroke_width=2.6), S.line(560, y + 70, 540, y + 14, stroke=S.CONC, stroke_width=2.6)]
    over = {
        'a': cut() + [S.line(lx + 10, y + 34, rx - 10, y + 34, stroke=S.CONC, stroke_width=1.6, stroke_dasharray='4 5'),
                      label(540, y + 98, 'ou perdas e danos', 13, anchor='middle', fill=S.CONC)],
        'b': [S.path(f'M{lx + 40},{y + 52} q22 -32 44 0 t44 0 t44 0 t44 0 t44 0 t44 0 t44 0 t44 0 t44 0', fill='none', stroke=S.CONC, stroke_width=2),
              S.line(lx + 40, y + 24, lx + 40, y + 80, stroke=S.CONC, stroke_width=2), S.line(rx - 40, y + 24, rx - 40, y + 80, stroke=S.CONC, stroke_width=2),
              label(540, y + 104, 'oscilação prevista dentro do contrato', 13, anchor='middle', fill=S.CONC)],
        'c': [dot(rx + 100, y, S.MUTED, dashed=True), S.line(rx + 12, y, rx + 88, y, stroke=S.MUTED, stroke_width=1.6, stroke_dasharray='3 5'),
              label(rx + 100, y - 28, 'revenda', 13, anchor='middle', fill=S.MUTED), S.line(540, y - 2, 540, y + 2, stroke=S.CONC, stroke_width=0),
              label(rx + 100, y + 34, 'margem', 13, anchor='middle', fill=S.CONC)],
    }
    return S.svg(W, H, 'A força obrigatória diante de quem quer sair: outro negócio, câmbio e lucro alheio',
                 frame('O vínculo mantido · o que o devedor alega e a resposta', CH, AN, base, over, 236, 296, H)), []
