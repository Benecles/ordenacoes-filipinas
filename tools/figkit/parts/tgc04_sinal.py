"""Aula 04, ch.5: the sinal as a measured length, an instrument.
Sources: CC arts. 418-420; Pereira III pp. 90-91. The unit is the sinal itself, never an amount. Params: none.
"""
from . import svg as S
from .tgc04_instr import W, label, frame

H = 420
CH = [('a', 'Confirmatórias'), ('b', 'Penitenciais, com arrependimento'), ('c', 'Inexecução de quem recebeu')]
AN = {
    'a': ('Taxa mínima de indenização', 'Art. 419: a parte inocente pode pedir indenização suplementar, se provar maior prejuízo,', 'ou exigir a execução do contrato com perdas e danos.', True),
    'b': ('O sinal é o limite', 'Art. 420: com direito de arrependimento expresso, o sinal é unicamente indenizatório;', 'quem o exerce perde o dado ou devolve o recebido mais o equivalente, sem suplemento.', False),
    'c': ('Devolução e equivalente', 'Art. 418: a parte inocente desfaz o contrato e exige o que deu mais o equivalente,', 'além de atualização monetária, juros e honorários de advogado.', True),
}


def build(p):
    y = 100
    base = [S.rect(60, y, 200, 44, fill=S.PAPER, stroke=S.INK, stroke_width=2.4),
            S.text(160, y + 28, 'sinal', size=15, family=S.SANS, anchor='middle'),
            S.line(60, y + 70, 1020, y + 70, stroke=S.GRID, stroke_width=1)]
    over = {
        'a': [S.line(260, y + 22, 1010, y + 22, stroke=S.DIF, stroke_width=2.2, stroke_dasharray='3 5'),
              S.path(f'M1000,{y + 12} L1010,{y + 22} L1000,{y + 32}', fill='none', stroke=S.DIF, stroke_width=2.2),
              label(280, y - 10, 'suplemento, se provado o prejuízo maior', 14, fill=S.DIF)],
        'b': S.hatch(266, y, 754, 44, step=12, stroke=S.GRID, stroke_width=1) +
             [S.line(260, y - 18, 260, y + 62, stroke=S.CONC, stroke_width=4),
              label(280, y - 10, 'nenhuma indenização além do sinal', 14, fill=S.CONC)],
        'c': [S.rect(264, y, 200, 44, fill=S.PAPER, stroke=S.DIF, stroke_width=2.4),
              S.text(364, y + 28, 'equivalente', size=15, family=S.SANS, anchor='middle', fill=S.DIF),
              S.line(464, y + 22, 760, y + 22, stroke=S.DIF, stroke_width=2, stroke_dasharray='3 5'),
              label(480, y - 10, 'atualização, juros e honorários', 14, fill=S.DIF)],
    }
    return S.svg(W, H, 'O sinal: piso nas confirmatórias, teto nas penitenciais, dobro quando quem o recebeu inadimple',
                 frame('Arras · o sinal medido contra o prejuízo', CH, AN, base, over, 252, 306, H)), []
