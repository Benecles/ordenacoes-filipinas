"""Aula 04, ch.1: what happens to the beneficiary's right, an instrument.
Sources: Venosa pp. 86-87 (exceções oponíveis; REsp 1.086.989/RS), Pereira III pp. 97-98 (recusa sem substituto,
substituição por endosso ou testamento, benefício recusado). Params: none.
"""
from . import svg as S
from .tgc04_instr import W, dot, label, frame

H = 420
CH = [('a', 'O beneficiário adere'), ('b', 'O beneficiário recusa'), ('c', 'O estipulante o substitui'),
      ('d', 'Promitente quer resolver')]
AN = {
    'a': ('Ação direta, com os limites do contrato', 'O beneficiário cobra a prestação diretamente do promitente, que conserva as exceções contratuais;', 'se o estipulante não cumpriu a sua parte, essa defesa pode alcançar a cobrança.', True),
    'b': ('Sem substituto, desaparece o objeto', 'A aquisição não se impõe ao terceiro, que pode recusar o benefício.', 'O promitente devolve o que recebeu, sob pena de injusto enriquecimento.', False),
    'c': ('O promitente continua devedor', 'Muda quem recebe, não quem deve: a reserva permite trocar o beneficiário por ato entre vivos,', 'como o endosso da apólice, ou por testamento, sem nova concordância do promitente.', True),
    'd': ('A resolução não cabe', 'Com a adesão, a beneficiária já adquirira o direito material prometido (REsp 1.086.989/RS, 23/02/2010);', 'a resolução a privaria desse direito por via indireta.', False),
}


def build(p):
    ex, px, bx, y = 150, 540, 930, 120
    base = [S.line(ex, y, px, y, stroke=S.INK, stroke_width=2), dot(ex, y), dot(px, y), dot(bx, y),
            label(ex, y - 22, 'estipulante', 14, anchor='middle'), label(px, y - 22, 'promitente', 14, anchor='middle'),
            label(bx, y - 22, 'beneficiário', 14, anchor='middle'), label((ex + px) / 2, y + 26, 'acordo', 13, anchor='middle')]
    over = {
        'a': [S.line(px, y, bx - 10, y, stroke=S.DIF, stroke_width=2.6), label((px + bx) / 2, y + 26, 'prestação', 13, anchor='middle', fill=S.DIF)],
        'b': [S.path(f'M{px},{y + 10} C{px - 100},{y + 90} {ex + 100},{y + 90} {ex},{y + 10}', fill='none', stroke=S.CONC, stroke_width=2.2, stroke_dasharray='3 5'),
              label((ex + px) / 2, y + 86, 'restituição', 13, anchor='middle', fill=S.CONC)],
        'c': [S.path(f'M{px},{y + 6} C{px + 120},{y + 60} {bx - 60},{y + 70} {bx},{y + 70}', fill='none', stroke=S.DIF, stroke_width=2.6),
              dot(bx, y + 70, S.DIF), label(bx + 14, y + 100, 'novo beneficiário', 13, anchor='end', fill=S.DIF)],
        'd': [S.line(px, y, bx - 10, y, stroke=S.DIF, stroke_width=2.6),
              S.line(735, y - 22, 735, y + 22, stroke=S.CONC, stroke_width=4), label(735, y + 44, 'resolução', 13, anchor='middle', fill=S.CONC)],
    }
    return S.svg(W, H, 'O direito do beneficiário: adesão, recusa, substituição, resolução',
                 frame('Estipulação em favor de terceiro · quatro lances', CH, AN, base, over, 252, 306, H)), []
