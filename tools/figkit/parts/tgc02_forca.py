"""Aula 02, ch.2: what the binding force answers when a party wants out, an instrument (language: the held cord).
Sources: Pereira III (pacta sunt servanda; who prefers another deal stays bound or pays perdas e danos), REsp 803.481/GO
(variation in the soy price is a foreseeable risk; a larger resale margin is not extraordinary), CC 1.417-1.418
(registro da promessa for execucao especifica with eficacia real). Params: none. Hand: tgc01_hand / tgc02_hand."""
from . import svg as S
from .tgc01_hand import cord, rule, mark, name, gloss
from .tgc02_hand import W, frame

H = 380
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
    lx, rx, y = 260, 820, 78
    base = [cord(lx + 8, rx - 8, y, amp=7, half=24, taper=30), mark(lx, y, S.DIF), mark(rx, y, S.DIF),
            name(lx, y - 20, 'devedor', anchor='middle'), name(rx, y - 20, 'credor', anchor='middle'),
            gloss(540, y - 14, 'pacta sunt servanda', anchor='middle')]
    cut = [rule(f'M520,{y + 46} L540,{y + 8} L560,{y + 46}', S.CONC, 2)]
    over = {
        'a': cut + [rule(f'M{lx + 10},{y + 30} H{rx - 10}', S.CONC, 1.0, '2 5'), gloss(540, y + 68, 'ou perdas e danos', col=S.CONC, anchor='middle')],
        'b': [S.path(f'M{lx + 40},{y + 36} q22 -30 44 0 t44 0 t44 0 t44 0 t44 0 t44 0 t44 0 t44 0 t44 0', fill='none', stroke=S.CONC, stroke_width=2),
              rule(f'M{lx + 40},{y + 16} V{y + 56}', S.CONC, 1.0), rule(f'M{rx - 40},{y + 16} V{y + 56}', S.CONC, 1.0),
              gloss(540, y + 78, 'oscilação prevista dentro do contrato', col=S.CONC, anchor='middle')],
        'c': [mark(rx + 100, y, S.MUTED), rule(f'M{rx + 12},{y} H{rx + 90}', S.MUTED, 1.2, '2 5'),
              name(rx + 100, y - 20, 'revenda', col=S.MUTED, anchor='middle'), gloss(rx + 100, y + 30, 'margem maior', col=S.CONC, anchor='middle')],
    }
    return S.svg(W, H, 'A força obrigatória diante de quem quer sair: outro negócio, câmbio e lucro alheio',
                 frame(CH, AN, base, over, 190, 262, H)), []
