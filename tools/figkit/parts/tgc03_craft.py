"""Objects for Aula 03, in the course hand (DIRECTION.md): ink on paper, nothing boxed; each mode is tied to the
passage beside its marker.

Sources: consórcio/TJRS; Zanetti's three times and three decisions; Asti/STJ; Eike/STJ; Versiani's well, manual and
farm; Benetti's sponsorship, CISG and invoices. The ruled marks represent writing, never invented document wording or
quantities. A sheet is a 2px head rule and hairline lines; a bond is the two-strand cord (loose strands where it has
not been formed); an orange cut is where the law stops it.
"""
from . import svg as S
from . import tgc01_hand as H
from .tgc03_mao import sheet, envelope, strands, cut, strike, arrow

T = S.text


def note(x, y, s, col=S.INK2, anchor=None, size=15):
    return H.gloss(x, y, s, col, anchor=anchor, size=size)


def build(p):
    mode = p['mode']
    o = []
    if mode == 'quitacao':
        # One continuous paid account carried on the cord, then a late charge that meets the cut.
        o += sheet(80, 30, 270, 9)
        for y in range(62, 195, 26):
            o.append(H.rule(f'M318,{y} l6,7 l13,-16', S.DIF, 2.0))
        o += [H.cord(86, 396, 262), H.mark(80, 262, S.DIF), note(80, 296, '36 parcelas pagas', S.DIF)]
        o += cut(412, 262, 56)
        o += sheet(440, 150, 120, 3, S.CONC) + strike(500, 190, 40, S.CONC)[:0] + [H.rule('M436,146 L566,236', S.CONC, 2.0),
              H.name(440, 124, 'cobrança tardia', S.CONC, size=14)]
    elif mode == 'continuidade':
        # The crease divides the codifications; three strands of the same writing cross it.
        o += [H.name(95, 60, 'Código de 1916', size=14), H.name(333, 60, 'Código de 2002', size=14)]
        for k, y in enumerate(range(96, 232, 27)):
            keep = k in (1, 3, 5)
            col, w = (S.DIF, 2.0) if keep else (S.INK2, 1.0)
            o += [H.rule(f'M95,{y} H282', col, w), H.rule(f'M318,{y} H525', col, w), H.rule(f'M282,{y} Q300,{y - 12} 318,{y}', col, w)]
        o += [H.rule('M300,76 V248', S.GRID, 1.0, '3 5'), note(95, 292, 'Interpretação, cooperação e controle atravessam a mudança.', S.INK)]
    elif mode == 'asti':
        state = int(p.get('state', 1))
        o += envelope(57, 73) + [note(57, 54, 'contatos preparatórios', S.INK)]
        o += strands(250, 520, 150, dashed=None if state >= 2 else '3 5')
        o += [H.mark(540, 150, S.INK2), note(540, 190, 'sem contrato', S.INK2, anchor='middle')]
        if state >= 2:
            for k in range(3):
                o += sheet(250 + k * 88, 62, 70, 4)
            o += [note(250, 44, 'preparativos da Asti', S.INK)]
        if state == 3:
            o += cut(470, 150, 80, S.CONC)
            o += [note(63, 307, 'Ruptura injustificada: reparação do prejuízo ligado à confiança.', S.CONC)]
        elif state == 2:
            o += [note(63, 307, 'A confiança cresce com os preparativos provocados.', S.INK)]
        else:
            o += [note(63, 307, 'O contato inicia deveres antes do consentimento.', S.INK)]
    elif mode == 'manuscrito':
        o += sheet(95, 35, 340, 6)
        for y in [183, 219, 253]:
            o.append(H.rule(f'M123,{y} H280', S.CONC, 1.4, '3 5'))
        o += [note(300, 188, 'objeto', S.INK), note(300, 224, 'quantidade', S.INK), note(300, 258, 'preço', S.INK),
              note(97, 311, 'O manuscrito de Eike deixa termos essenciais indeterminados.', S.INK)]
    elif mode == 'seguro':
        # A coverage perimeter crossed by the cord; the cut is where the cover stops.
        o += [H.rule('M110,40 H400 V185 Q400,256 255,287 Q110,256 110,185 Z', S.INK2, 1.0)]
        o += [H.cord(130, 392, 128), H.mark(122, 128, S.DIF), note(155, 101, 'cobertura contratada', S.DIF)]
        o += cut(404, 128, 60, S.CONC) + [note(426, 124, 'danos morais', S.INK), note(426, 150, 'excluídos', S.CONC)]
    elif mode == 'documentos':
        # Documentation lies across the open envelope: the obstacle to remittance.
        o += envelope(89, 128, 235, 133) + sheet(180, 42, 174, 8)
        o += [note(378, 91, 'documentação', S.INK), note(378, 116, 'a regularizar', S.CONC),
              note(89, 299, 'A cooperação do credor permite remeter o pagamento à Itália.', S.INK)]
    elif mode == 'faturas':
        for k in range(3):
            x = 50 + k * 190
            o += sheet(x, 40, 160, 7)
            o += [H.rule(f'M{x},{40 + 16 + 15 * 7 + 14} H{x + 160}', S.DIF, 2.0), note(x, 40 + 16 + 15 * 7 + 38, 'tarifa antiga', S.DIF)]
        o += [note(50, 320, 'Faturas sem ressalva sustentam a confiança no preço mantido.', S.INK)]
    elif mode == 'poco':
        # Literal cross-section: delivery exists, but the creditor cannot use it.
        o += [H.rule('M50,60 H218 V268 H383 V60 H550', S.INK, 1.0)]
        for x in (196, 396):
            for y in range(70, 260, 12):
                o.append(H.rule(f'M{x},{y + 8} l10,-8', S.GRID, 1.0))
        for j in range(3):
            for i in range(3):
                x, y = 232 + i * 45 + (j % 2) * 7, 218 + j * 16
                o.append(H.rule(f'M{x},{y} h40 v12 h-40 Z', S.INK, 1.0))
        o += [note(73, 40, 'entrega dos tijolos', S.INK), note(425, 216, 'no fundo', S.INK), note(425, 242, 'do poço', S.INK),
              note(73, 310, 'Entregar sem preservar a utilidade pode violar a boa-fé objetiva.', S.INK)]
    elif mode == 'manual':
        # A spread and the machine's operation drawn, not a label-filled book.
        o += [H.rule('M70,66 Q180,42 300,74 Q420,42 530,66 V267 Q410,245 300,276 Q180,245 70,267 Z', S.INK, 1.0), H.rule('M300,74 V276', S.INK2, 1.0)]
        for i in range(9):
            o.append(H.rule(f'M94,{104 + 15 * i} H{94 + 166 * (0.72 if i % 3 == 2 else 1)}', S.INK2, 1.0))
        o += [S.circle(411, 157, 43, fill='none', stroke=S.INK, stroke_width=2), H.rule('M411,157 L435,130', S.INK, 2.0),
              H.rule('M360,221 H472', S.INK, 1.0), note(88, 310, 'O manual torna possível o uso da máquina sem dano.', S.INK)]
    elif mode == 'fazenda':
        # Two contiguous inherited parcels; the neighbouring enterprise is spatial.
        o += [H.rule('M76,94 L306,52 L431,123 L393,258 L137,276 Z', S.INK, 2.0), H.rule('M306,52 L255,267', S.GRID, 1.0, '4 5')]
        o += [H.name(140, 180, 'irmão', size=14), H.name(319, 184, 'irmão', size=14), H.name(455, 72, 'mineradora', size=14)]
        o += [H.rule('M451,94 h85 v120 h-85 M451,124 h85 M451,154 h85 M451,184 h85', S.INK, 1.0),
              note(73, 311, 'A relação de confiança altera o dever de compartilhar informação.', S.INK)]
    elif mode == 'patrocinio':
        # A displayed banner beside an unanswered outgoing proposal; the strands never meet.
        o += [H.rule('M76,67 V256', S.INK2, 1.0), H.rule('M285,67 V256', S.INK2, 1.0)]
        o += sheet(76, 81, 209, 6) + [H.name(113, 141, 'Pizza Hut', size=15)]
        o += envelope(370, 104, 153, 95) + [note(366, 81, 'proposta sem resposta', S.INK)]
        o += [note(76, 305, 'A divulgação pelo clube não substitui a aceitação do patrocinador.', S.INK)]
    elif mode == 'recepcao':
        o += envelope(83, 102, 180, 108)
        o += [H.rule('M358,72 H527 V255 H358 M382,72 V255', S.INK, 1.0)]
        o += [H.rule('M285,100 H335', S.GRID, 1.0, '3 5'), H.rule('M285,210 H335', S.GRID, 1.0, '3 5')]
        o += [H.name(88, 68, 'aceitação', size=14), H.name(395, 105, 'proponente', size=14), note(395, 148, 'chegada'), note(395, 175, 'art. 18(2)'),
              note(83, 305, 'Na CISG, a regra é a eficácia com a recepção.', S.INK)]
    elif mode == 'fatura-posterior':
        o += sheet(70, 49, 227, 12)
        o += [H.rule('M94,222 H272', S.DIF, 2.0), note(86, 297, 'contrato já formado', S.DIF)]
        o += sheet(350, 101, 178, 8, S.CONC) + [note(360, 79, 'fatura posterior', S.INK), note(346, 297, 'honorários acrescidos', S.CONC)]
    else:
        raise ValueError(mode)
    return S.svg(620, 368, 'Boa-fé objetiva e formação: ' + mode, o), []
