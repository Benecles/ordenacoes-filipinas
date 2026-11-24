"""Objects for Aula 03; each mode is tied to the passage beside its marker.

Sources: consórcio/TJRS; Zanetti's three times and three decisions; Asti/STJ;
Eike/STJ; Versiani's well, manual and farm; Benetti's sponsorship, CISG and invoices.
The ruled marks represent writing, never invented document wording or quantities.
"""
from . import svg as S
import textwrap


def ln(a, b, c, d, ink=None, **kw):
    return S.line(a, b, c, d, stroke=ink or S.INK, stroke_width=1.5, **kw)


def txt(x, y, text, **kw):
    width = max(10, int((570 - x) / 10.6))
    return ''.join(S.text(x, y+22*i, row, size=18, family=S.SERIF, **kw)
                   for i, row in enumerate(textwrap.wrap(text, width)))


def paper(x, y, w, h, ink=None):
    return [S.rect(x, y, w, h, fill=S.PAPER, stroke=ink or S.INK, stroke_width=1.4)]


def writing(x, y, w, rows=4):
    return [ln(x, y + 15*i, x + w*(1 if i % 3 else .73), y + 15*i, S.GRID) for i in range(rows)]


def envelope(x, y, w=160, h=95):
    return paper(x, y, w, h) + [S.path(f'M{x},{y} l{w/2},{h*.55} l{w/2},{-h*.55}', fill='none', stroke=S.INK, stroke_width=1.5)]


def build(p):
    mode = p['mode']
    o = []
    if mode == 'quitacao':
        # One continuous paid account, then an incompatible late addition.
        o += paper(95, 30, 265, 235) + writing(120, 70, 210, 9)
        for y in range(68, 199, 26):
            o.append(S.path(f'M314,{y} l6,7 l13,-16', fill='none', stroke=S.DIF, stroke_width=2))
        o += [ln(117, 222, 338, 222, S.DIF), txt(120, 248, '36 parcelas pagas', fill=S.DIF)]
        o += paper(392, 154, 135, 105, S.CONC) + writing(410, 181, 95, 3)
        o += [ln(385, 145, 535, 266, S.CONC), txt(390, 117, 'cobrança tardia', fill=S.CONC)]
    elif mode == 'continuidade':
        # A crease divides the codifications, while the same writing survives it.
        o += paper(70, 44, 460, 216)
        for y in range(100, 225, 24):
            o += [ln(95, y, 282, y), ln(318, y, 503, y)]
            o.append(S.path(f'M282,{y} Q300,{y-12} 318,{y}', fill='none', stroke=S.INK, stroke_width=1.5))
        o += [ln(300, 58, 300, 245, S.GRID, stroke_dasharray='3 5'), txt(106, 79, 'Código de 1916'), txt(333, 79, 'Código de 2002'), txt(88, 297, 'Interpretação, cooperação e controle atravessam a mudança.')]
    elif mode == 'asti':
        state = int(p.get('state', 1))
        o += envelope(57, 73)
        o += [txt(53, 53, 'contatos preparatórios')]
        if state >= 2:
            for k in range(3):
                o += paper(241+k*13, 94-k*13, 170, 145)
            o += writing(285, 99, 120, 6)
            o += [txt(240, 273, 'preparativos da Asti')]
        else:
            o += [ln(255, 200, 430, 200, S.GRID, stroke_dasharray='4 5')]
        o += [S.rect(466, 64, 92, 174, fill='none', stroke=S.GRID, stroke_dasharray='5 5'), txt(454, 273, 'sem contrato')]
        if state == 3:
            o += [ln(268, 77, 425, 236, S.CONC), ln(425, 77, 268, 236, S.CONC), txt(63, 307, 'Ruptura injustificada: reparação do prejuízo ligado à confiança.', fill=S.CONC)]
        elif state == 2:
            o += [txt(63, 307, 'A confiança cresce com os preparativos provocados.')]
        else:
            o += [txt(63, 307, 'O contato inicia deveres antes do consentimento.')]
    elif mode == 'manuscrito':
        o += paper(95, 35, 340, 245) + writing(121, 75, 280, 5)
        for y in [183, 219, 253]:
            o += [ln(123, y, 280, y, S.CONC, stroke_dasharray='3 5')]
        o += [txt(453, 183, 'objeto'), txt(453, 219, 'quantidade'), txt(453, 253, 'preço'), txt(97, 311, 'O manuscrito de Eike deixa termos essenciais indeterminados.')]
    elif mode == 'seguro':
        # A coverage perimeter with an explicit aperture: no invented risk amounts.
        o += [S.path('M110,40 H400 V185 Q400,256 255,287 Q110,256 110,185 Z', fill='none', stroke=S.INK, stroke_width=2)]
        o += [ln(151, 128, 360, 128), txt(155, 101, 'cobertura contratada')]
        o += [S.path('M210,175 H400 V229 H210 Z', fill=S.PAPER, stroke=S.CONC, stroke_width=1.5)]
        o += S.hatch(218, 183, 174, 38, stroke=S.GRID)
        o += [txt(426, 194, 'danos morais'), txt(426, 220, 'excluídos', fill=S.CONC)]
    elif mode == 'documentos':
        # Documentation sits across the open envelope: the obstacle to remittance.
        o += envelope(89, 128, 235, 133)
        o += paper(180, 42, 174, 165) + writing(203, 78, 125, 7)
        o += [txt(378, 91, 'documentação'), txt(378, 116, 'a regularizar'), txt(89, 299, 'A cooperação do credor permite remeter o pagamento à Itália.')]
    elif mode == 'faturas':
        for k in range(3):
            x, y = 65+k*120, 40+k*38
            o += paper(x, y, 166, 165) + writing(x+17, y+34, 130, 5)
            o += [ln(x+15, y+132, x+150, y+132, S.DIF), txt(x+20, y+155, 'tarifa antiga', fill=S.DIF)]
        o += [txt(75, 310, 'Faturas sem ressalva sustentam a confiança no preço mantido.')]
    elif mode == 'poco':
        # Literal cross-section: delivery exists, but the creditor cannot use it.
        o += [ln(50, 60, 218, 60), ln(383, 60, 550, 60), ln(218, 60, 218, 268), ln(383, 60, 383, 268), ln(218, 268, 383, 268)]
        o += S.hatch(200, 64, 15, 204, stroke=S.GRID)
        o += S.hatch(387, 64, 15, 204, stroke=S.GRID)
        for j in range(3):
            for i in range(3):
                o += paper(232+i*45+(j%2)*7, 214+j*16, 40, 13)
        o += [txt(73, 40, 'entrega dos tijolos'), txt(425, 216, 'no fundo'), txt(425, 242, 'do poço'), txt(73, 310, 'Entregar sem preservar a utilidade pode violar a boa-fé objetiva.')]
    elif mode == 'manual':
        # A spread and its physical operation drawing, not a label-filled book.
        o += [S.path('M70,66 Q180,42 300,74 Q420,42 530,66 V267 Q410,245 300,276 Q180,245 70,267 Z', fill=S.PAPER, stroke=S.INK, stroke_width=1.5), ln(300, 74, 300, 276)]
        o += writing(94, 104, 166, 9)
        o += [S.circle(411, 157, 43, fill='none', stroke=S.INK, stroke_width=2), ln(411, 157, 435, 130), ln(360, 221, 472, 221), txt(88, 310, 'O manual torna possível o uso da máquina sem dano.')]
    elif mode == 'fazenda':
        # Two contiguous inherited parcels; the neighbouring enterprise is spatial.
        o += [S.path('M76,94 L306,52 L431,123 L393,258 L137,276 Z', fill='none', stroke=S.INK, stroke_width=2), ln(306, 52, 255, 267, S.GRID, stroke_dasharray='4 5')]
        o += [txt(140, 180, 'irmão'), txt(319, 184, 'irmão'), txt(455, 72, 'mineradora')]
        o += [S.path('M451,94 h85 v120 h-85 M451,124 h85 M451,154 h85 M451,184 h85', fill='none', stroke=S.INK, stroke_width=1.5), txt(73, 311, 'A relação de confiança altera o dever de compartilhar informação.')]
    elif mode == 'patrocinio':
        # A displayed banner beside an unanswered outgoing proposal.
        o += [ln(76, 67, 76, 256), ln(285, 67, 285, 256)]
        o += paper(76, 81, 209, 106) + [txt(113, 141, 'Pizza Hut')]
        o += envelope(370, 104, 153, 95)
        o += [txt(366, 81, 'proposta sem resposta'), txt(76, 305, 'A divulgação pelo clube não substitui a aceitação do patrocinador.')]
    elif mode == 'recepcao':
        o += envelope(83, 102, 180, 108)
        o += [S.path('M358,72 H527 V255 H358 M382,72 V255', fill='none', stroke=S.INK, stroke_width=2)]
        o += [ln(285, 100, 335, 100, S.GRID, stroke_dasharray='3 5'), ln(285, 210, 335, 210, S.GRID, stroke_dasharray='3 5')]
        o += [txt(88, 68, 'aceitação'), txt(395, 105, 'proponente'), txt(395, 148, 'chegada'), txt(395, 175, 'art. 18(2)'), txt(83, 305, 'Na CISG, a regra é a eficácia com a recepção.')]
    elif mode == 'fatura-posterior':
        o += paper(70, 49, 227, 215) + writing(94, 87, 180, 7)
        o += [ln(94, 222, 272, 222, S.DIF), txt(86, 297, 'contrato já formado')]
        o += paper(350, 101, 178, 160) + writing(371, 135, 135, 4)
        o += [ln(368, 220, 507, 220, S.CONC), txt(360, 79, 'fatura posterior'), txt(346, 297, 'honorários acrescidos', fill=S.CONC)]
    else:
        raise ValueError(mode)
    return S.svg(620, 340, 'Boa-fé objetiva e formação: ' + mode, o), []
