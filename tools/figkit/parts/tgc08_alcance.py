"""Aula 08, chapter 2: what travels when the vendedor of a compra e venda transfers something.
Params: none. A clickable instrument (data-opt / data-ans, wired by casa.js).
The comprador is a spine; each right the comprador holds hangs off it as a row and ends at whoever holds it.
Choices: cedo as promissórias (only the crédito moves, the vendedor keeps the duties), cedo a posição
(every row moves to the cessionário), cedo a posição sem a anuência do cedido (the ajuste waits, rows stay).
Sources: Luis Renato Ferreira da Silva pp. 3-7 (cessão de crédito x cessão da posição, anuência do cedido).
"""
from . import svg as S

W, H = 1080, 560
XV, XC, XT = 150, 540, 930
ROWS = (('crédito pelo preço', 190), ('vício redibitório', 258), ('evicção', 326))
CHOICES = (('cred', 'Cedo as promissórias'), ('pos', 'Cedo a posição de vendedor'), ('sem', 'Cedo a posição sem o comprador'))
# holder of each row per choice: V vendedor, T terceiro
HOLD = {'cred': 'TVV', 'pos': 'TTT', 'sem': 'VVV'}
ANS = {
    'cred': ('Só o crédito circula', 'O vendedor continua vinculado ao contrato e responde por vício redibitório e evicção.',
             'O comprador mantém contra ele pretensão e ação; transferir créditos não transfere a posição.', True),
    'pos': ('A posição inteira passa', 'O cessionário assume a participação completa do vendedor, com direitos e deveres.',
            'As demandas por vício redibitório ou evicção passam a ser dirigidas a ele.', True),
    'sem': ('O ajuste aguarda o comprador', 'A cessão da posição exige as três vontades: cedente, cessionário e cedido.',
            'Até a anuência do comprador o vendedor segue vinculado e as pretensões ficam com ele.', False),
}


def _t(x, y, s, size=17, **kw):
    return S.text(x, y, s, size=size, family=S.SANS, **kw)


def _dot(x, y, col, r=8, fill=None, dash=None):
    return S.circle(x, y, r, fill=fill or S.PAPER, stroke=col, stroke_width=2.2, stroke_dasharray=dash)


def _actor(x, name, col, dashed=False):
    return [S.rect(x - 80, 52, 160, 44, fill=S.PAPER, stroke=col, stroke_width=1.8, stroke_dasharray='5 4' if dashed else None),
            _t(x, 80, name, 18, weight='600', anchor='middle', fill=col)]


def build(p):
    base = [S.text(24, 28, 'o que acompanha a transferência do vendedor', size=13, family=S.MONO)]
    base += _actor(XC, 'Comprador', S.INK)
    base.append(S.line(XC, 96, XC, 340, stroke=S.MUTED, stroke_width=1.2, stroke_dasharray='2 5'))
    for name, y in ROWS:
        base += [S.rect(XC - 110, y - 22, 220, 44, fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
                 _t(XC, y + 6, name, 17, anchor='middle')]
    o = list(base)
    n = len(CHOICES)
    cw = (W - 60 - 12 * (n - 1)) / n
    yc, yb = 382, 442
    for i, (k, lab) in enumerate(CHOICES):
        x = 30 + i * (cw + 12)
        o.append(f'<g data-opt="{k}" tabindex="0" role="button" aria-label="{S.esc(lab)}">')
        o.append(S.rect(x, yc, cw, 44, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
        o.append(S.text(x + cw / 2, yc + 27, lab, size=17, family=S.SANS, weight='600', anchor='middle'))
        o.append('</g>')
    for i, (k, lab) in enumerate(CHOICES):
        verdict, l1, l2, ok = ANS[k]
        col = S.DIF if ok else S.CONC
        o.append(f'<g data-ans="{k}"' + ('' if i == 0 else ' display="none"') + '>')
        held = HOLD[k]
        v_out = k == 'pos'
        t_wait = k == 'sem'
        o += _actor(XV, 'Vendedor', S.CONC if v_out else S.INK, dashed=v_out)
        o += _actor(XT, 'Terceiro', S.CONC if t_wait else S.DIF, dashed=t_wait)
        if v_out:
            o.append(_t(XV, 118, 'sai do contrato', 16, anchor='middle', fill=S.CONC))
        if t_wait:
            o.append(_t(XT, 118, 'aguarda a anuência', 16, anchor='middle', fill=S.CONC))
        for (name, y), h in zip(ROWS, held):
            if h == 'T':
                o.append(S.line(XC + 110, y, XT, y, stroke=S.DIF, stroke_width=2.4))
                o.append(_dot(XT, y, S.DIF, fill=S.DIF))
            else:
                o.append(S.line(XC - 110, y, XV, y, stroke=S.INK, stroke_width=2.4))
                o.append(_dot(XV, y, S.INK, fill=S.INK))
        if k == 'cred':
            o.append(_t(XT, 222, 'recebe só as parcelas', 16, anchor='middle', fill=S.DIF))
        o.append(S.rect(30, yb, W - 60, 106, fill=S.PAPER, stroke=col, stroke_width=2))
        o.append(S.text(54, yb + 38, verdict, size=24, family=S.SANS, weight='650', fill=col))
        o.append(S.text(54, yb + 68, l1, size=18, family=S.SERIF))
        o.append(S.text(54, yb + 92, l2, size=18, family=S.SERIF))
        o.append('</g>')
    return S.svg(W, H, 'Alcance da transferência: o crédito, a posição e a posição sem anuência', o), []
