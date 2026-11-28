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
from .tgc01_hand import cord, rule, mark, name, gloss
RX, RY0, STEP = 40, 96, 52
SLOT = {True: 690, False: 900}
COL = {True: S.DIF, False: S.CONC}
LAB = {True: 'A garantia responde', False: 'A garantia não responde'}


def build(p):
    T = S.text
    o = [name(RX, 40, 'O que o adquirente fez ou sabia', size=13.5),
         name(SLOT[True], 40, 'Responde', col=S.DIF, anchor='middle', size=13.5),
         name(SLOT[False], 40, 'Não responde', col=S.CONC, anchor='middle', size=13.5)]
    for i, (k, lab, ok, *_r) in enumerate(ROWS):
        y = RY0 + i * STEP
        o.append(f'<g data-opt="{k}" tabindex="0" role="button" aria-label="{S.esc(lab)}">')
        o.append(S.rect(RX - 10, y - 24, 470, 44, fill=S.PAPER, opacity='0'))
        o.append(mark(RX + 6, y - 2, S.INK, 5.5))
        o.append(T(RX + 24, y + 3, lab, size=17, family=S.SANS, weight='500'))
        o.append(rule(f'M{RX + 24},{y + 14} H{RX + 440}', S.GRID, 1.0))
        for ok2 in (True, False):
            o.append(mark(SLOT[ok2], y - 2, S.MUTED, 5))
        o.append('</g>')
    for i, (k, lab, ok, l1, l2) in enumerate(ROWS):
        y = RY0 + i * STEP
        col = COL[ok]
        o.append(f'<g data-ans="{k}"' + ('' if k == 'f' else ' display="none"') + '>')
        o.append(mark(RX + 6, y - 2, col, 5.5, solid=True))
        o.append(rule(f'M{RX + 24},{y + 14} H{RX + 440}', col, 2.0))
        if ok:
            o.append(cord(RX + 470, SLOT[True] - 10, y - 2, amp=6.5, half=24, taper=30))
        else:
            o.append(rule(f'M{RX + 470},{y - 2} H{SLOT[False] - 10}', col, 2.0))
            o.append(S.path(f'M{SLOT[False] - 140},{y + 7} L{SLOT[False] - 130},{y - 11}', fill='none', stroke=col, stroke_width=2.4, stroke_linecap='round'))
        o.append(mark(SLOT[ok], y - 2, col, 6.5, solid=True))
        o.append(rule('M40,418 H1040', col, 1.0))
        o.append(name(40, 446, LAB[ok], col=col, size=13.5))
        o.append(T(40, 472, l1 + ' ' + l2, size=16, family=S.SERIF, font_style='italic'))
        o.append('</g>')
    return S.svg(W, H, p.get('title', 'Quando o alienante responde pela evicção'), o), []
