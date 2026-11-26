"""Aula 10, chapter 5: when a failure lets the creditor resolve. An instrument.

Two prestações on one sheet (A's and B's) above a time axis with the due date. The reader picks the
failure; the sheet shows what was given, what is missing and when, and the answer says if it resolves.
Sources: Aguiar Júnior p.31 (mora qualificada; termo essencial; vestido da noiva); CC art. 395, parágrafo
único; Caio Mário p.141, Enunciados 361 (adimplemento substancial); Venosa p.99 (FGTS: quem não cumpriu o
próprio dever não resolve). Params: none. Positions ordinal.
"""
from . import svg as S

W, H = 1080, 470
CH = [
    ('a', 'vestido entregue após o casamento', 155),
    ('b', 'atraso que ainda atende ao fim', 417),
    ('c', 'quase todo o contrato cumprido', 679),
    ('d', 'autor sem cumprir o próprio dever', 941),
]
ANS = {
    'a': ('A resolução cabe', 'Termo essencial: depois do casamento o vestido perdeu a utilidade, e o art. 395, parágrafo único, permite recusar a prestação.', True),
    'b': ('A resolução não cabe', 'A mora simples ainda deixa prestar utilmente; só a mora qualificada, que frustra o interesse do credor, permite resolver.', False),
    'c': ('A resolução não cabe', 'Adimplemento substancial: resta ao credor a ação de cobrança, e a parcela faltante continua devida.', False),
    'd': ('A resolução não cabe', 'No caso do FGTS, quem não entregou a documentação do próprio dever não pode exigir o da outra parte nem resolver (Venosa, p. 99).', False),
}
X0, X1 = 150, 1010


def build(p):
    o = [S.text(24, 30, 'Falta de prestação · a resolução da parte lesada', size=13, family=S.MONO)]
    for k, lab, cx in CH:
        o.append(f'<g data-opt="{k}" tabindex="0" role="button" aria-label="{S.esc(lab)}">')
        o.append(S.rect(cx - 125, 56, 250, 44, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
        o.append(S.text(cx, 84, lab, size=13, family=S.SANS, weight='600', anchor='middle'))
        o.append('</g>')
    ya, yb, yt = 190, 250, 140
    # fixed: lane labels, outlines, axis
    for yy, lab in ((ya, 'A, credor'), (yb, 'B, devedor')):
        o.append(S.text(X0 - 14, yy + 17, lab, size=14, family=S.SANS, weight='600', anchor='end'))
        o.append(S.rect(X0, yy, X1 - X0, 24, fill='none', stroke=S.INK, stroke_width=1.6))
    o.append(S.line(X0, yt, X1, yt, stroke=S.GRID, stroke_width=3))
    o.append(S.circle(X0, yt, 7, fill=S.PAPER, stroke=S.INK, stroke_width=2))
    o.append(S.line(400, yt - 14, 400, yt + 14, stroke=S.INK, stroke_width=2.5))
    o.append(S.text(400, yt - 22, 'vencimento', size=13, family=S.SANS, weight='600', anchor='middle'))
    spec = {  # a_filled, b_fill_to, delivery x, fim x
        'a': (True, X1, 640, 400), 'b': (True, X1, 640, 860),
        'c': (True, 960, None, None), 'd': (False, None, None, None)}
    for k, lab, cx in CH:
        af, bto, dx, fim = spec[k]
        head, why, ok = ANS[k]
        col = S.DIF if ok else S.CONC
        o.append(f'<g data-ans="{k}"' + ('' if k == 'a' else ' display="none"') + '>')
        if af:
            o.append(S.rect(X0, ya, X1 - X0, 24, fill=S.DIF, stroke=S.INK, stroke_width=1.6))
        else:
            o += S.hatch(X0, ya, X1 - X0, 24, step=9, stroke=S.CONC, stroke_width=1.5)
            o.append(S.text(X1, ya - 8, 'por cumprir', size=13, family=S.SERIF, fill=S.CONC, anchor='end'))
        if bto:
            o.append(S.rect(X0, yb, bto - X0, 24, fill=S.DIF, stroke=S.INK, stroke_width=1.6))
            if bto < X1:
                o += S.hatch(bto, yb, X1 - bto, 24, step=6, stroke=S.CONC, stroke_width=1.8)
                o.append(S.text(X1, yb + 46, 'parcela faltante', size=13, family=S.SERIF, fill=S.CONC, anchor='end'))
        if fim:
            fc = S.CONC
            o.append(S.line(fim, yt, fim, yb + 24, stroke=fc, stroke_width=2.5, stroke_dasharray='6 5'))
            o.append(S.text(fim, yb + 46, 'fim contratado', size=13, family=S.SERIF, fill=fc, anchor='middle'))
        if dx:
            o.append(S.line(dx, yt, dx, yb + 24, stroke=S.INK, stroke_width=1.5))
            o.append(S.circle(dx, yt, 8, fill=S.INK, stroke='none'))
            o.append(S.text(dx, yt - 22, 'entrega', size=13, family=S.SANS, weight='600', anchor='middle'))
        o.append(S.text(60, 366, head, size=21, family=S.SANS, weight='650', fill=col))
        for i, ln in enumerate(S.wrap(why, 100)):
            o.append(S.text(60, 400 + i * 24, ln, size=16, family=S.SERIF))
        o.append('</g>')
    return S.svg(W, H, 'Falta de prestação: quando a parte lesada pode resolver', o), []
