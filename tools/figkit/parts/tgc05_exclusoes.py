"""Aula 05, chapter 4: when the evicção guarantee holds, an instrument.

Six facts the reader can pick; each is wired to one of two bins (the alienante responde / não responde)
and the drawing answers with the ground. Facts: Pereira p.127 (a: perda por furto, fato das coisas ou dos
homens; b: sabia a coisa alheia; c: sabia litigiosa; d: risco assumido expressamente, emptio spei);
CC arts. 447, 448, 449 e 457; STJ REsp 1.332.112/GO (perda por vício anterior ao negócio oneroso).
Params: none. Positions are ordinal rows, not a scale.
"""
from . import svg as S

W, H = 1080, 500
ROWS = [
    ('a', 'Furto depois da compra', False,
     'Não responde: o alienante deve a integridade jurídica do objeto,',
     'não o resguardo contra o fato das coisas ou dos homens (Pereira, p. 127).'),
    ('b', 'Sabia que a coisa era alheia', False,
     'Não responde (art. 457): o adquirente seria cúmplice do apropriamento',
     'e não funda pretensão jurídica na própria conduta ilícita (Pereira, p. 127).'),
    ('c', 'Sabia que a coisa era litigiosa', False,
     'Não responde (art. 457): sabia que a prestação do outro dependia de',
     'acertamento judicial que lhe podia ser desfavorável (Pereira, p. 127).'),
    ('d', 'Assumiu o risco expressamente', False,
     'Não responde: o contrato seria aleatório, e o adquirente não reclama',
     'se nada vier a existir da coisa, como na emptio spei (Pereira, p. 127).'),
    ('e', 'Cláusula de exclusão, risco ignorado', True,
     'Responde pelo preço (art. 449): a exclusão da garantia conserva o',
     'direito do adquirente ao preço quando desconhecia o risco ou não o assumiu.'),
    ('f', 'Vandir: direito anterior, perda iminente', True,
     'Responde (art. 447): a perda por vício anterior ao negócio oneroso é o',
     'fator determinante, sem esperar trânsito em julgado (REsp 1.332.112/GO).'),
]
RX, RW, RH, RY0, STEP = 40, 400, 44, 64, 54
BX, BW = 640, 400
BIN = {True: (64, 'A garantia responde', S.DIF), False: (176, 'A garantia não responde', S.CONC)}


def build(p):
    T = S.text
    o = []
    o.append(T(24, 30, 'O que o adquirente fez ou sabia', size=13, family=S.MONO))
    o.append(T(BX, 30, 'O que a lei responde ao evicto', size=13, family=S.MONO))
    for ok, (by, lab, col) in BIN.items():
        o.append(S.rect(BX, by, BW, 92, fill=S.PAPER, stroke=col, stroke_width=2))
        o.append(T(BX + 24, by + 54, lab, size=22, family=S.SANS, weight='650', fill=col))
    for i, (k, lab, ok, *_r) in enumerate(ROWS):
        y = RY0 + i * STEP
        o.append(f'<g data-opt="{k}" tabindex="0" role="button" aria-label="{S.esc(lab)}">')
        o.append(S.rect(RX, y, RW, RH, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
        o.append(T(RX + 16, y + 28, lab, size=15, family=S.SANS, weight='600'))
        o.append('</g>')
    for i, (k, lab, ok, l1, l2) in enumerate(ROWS):
        y = RY0 + i * STEP + RH / 2
        by, _, col = BIN[ok]
        o.append(f'<g data-ans="{k}"' + ('' if k == 'f' else ' display="none"') + '>')
        o.append(S.rect(RX, RY0 + i * STEP, RW, RH, fill='none', stroke=col, stroke_width=3.2))
        o.append(S.path(f'M{RX + RW},{y} C{RX + RW + 90},{y} {BX - 90},{by + 46} {BX},{by + 46}', fill='none', stroke=col, stroke_width=2.4))
        o.append(S.rect(BX, by, BW, 92, fill='none', stroke=col, stroke_width=4))
        o.append(S.line(40, 410, 1040, 410, stroke=col, stroke_width=1.5))
        o.append(T(40, 444, l1, size=16, family=S.SERIF))
        o.append(T(40, 476, l2, size=16, family=S.SERIF))
        o.append('</g>')
    return S.svg(W, H, p.get('title', 'Quando o alienante responde pela evicção'), o), []
