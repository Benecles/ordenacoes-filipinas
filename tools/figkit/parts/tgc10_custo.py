"""Aula 10, chapter 4: what leaving unilaterally costs. An instrument on a time axis.

The reader picks how the denúncia was given; the axis answers where the effect lands against the clause's
minimum notice, and what it costs. Sources: REsp 1.112.796/PR (prazo respeitado: sem lucros cessantes);
TJSP Ap 1102157-74.2013.8.26.0100 (aviso desrespeitado: multa contratual); CC art. 473, parágrafo único
(investimentos consideráveis: efeito após prazo compatível); TJPR Ap 616.115-5 (investimentos nascidos da
demanda, sem exigência: parágrafo único afastado). Params: none. Positions ordinal, no time scale.
"""
from . import svg as S

W, H = 1080, 440
CH = [
    ('a', 'respeita o prazo da cláusula', 155),
    ('b', 'rompe antes do prazo da cláusula', 417),
    ('c', 'investimentos consideráveis', 679),
    ('d', 'investimentos nascidos da demanda', 941),
]
X0, XM, XEND = 100, 560, 1010
# key: (effect x, bar colour, extension?, head, why, ok)
ANS = {
    'a': (560, 'dif', False, 'Sem indenização por lucros cessantes',
          'Respeitado o prazo convencionado para a denúncia, não há lucros cessantes nem despesas das rescisões de empregados da contratada (REsp 1.112.796/PR).', True),
    'b': (330, 'conc', False, 'A multa contratual é devida',
          'Quem resilir contrato de serviços sem respeitar o prazo de aviso da cláusula deve a multa prevista (TJSP, Ap 1102157-74).', False),
    'c': (820, 'dif', True, 'A denúncia só produz efeito depois',
          'O art. 473, parágrafo único, adia o efeito até prazo compatível com a natureza e o vulto dos investimentos feitos para executar o contrato.', True),
    'd': (560, 'dif', False, 'O parágrafo único não protege',
          'Investimentos nascidos do aumento da demanda, sem exigência do contratante, numa relação de sete anos resilida aos quatro: o TJPR afastou o art. 473, parágrafo único.', False),
}


def build(p):
    o = [S.text(24, 30, 'Denúncia · quando produz efeito e o que custa · sem escala de tempo', size=13, family=S.MONO)]
    for k, lab, cx in CH:
        o.append(f'<g data-opt="{k}" tabindex="0" role="button" aria-label="{S.esc(lab)}">')
        o.append(S.rect(cx - 125, 56, 250, 44, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
        o.append(S.text(cx, 84, lab, size=13, family=S.SANS, weight='600', anchor='middle'))
        o.append('</g>')
    y = 190
    # fixed axis
    o.append(S.line(X0, y, 1020, y, stroke=S.GRID, stroke_width=3))
    o.append(S.circle(X0, y, 9, fill=S.PAPER, stroke=S.INK, stroke_width=2))
    o.append(S.text(X0, y - 24, 'notificação', size=14, family=S.SANS, weight='600', anchor='middle'))
    o.append(S.line(XM, y - 20, XM, y + 20, stroke=S.CONC, stroke_width=2.5))
    o.append(S.text(XM, y + 44, 'mínimo da cláusula', size=13, family=S.SERIF, fill=S.CONC, anchor='middle'))
    for k, lab, cx in CH:
        ex, col, ext, head, why, ok = ANS[k]
        c = S.DIF if col == 'dif' else S.CONC
        vc = S.DIF if ok else S.CONC
        o.append(f'<g data-ans="{k}"' + ('' if k == 'a' else ' display="none"') + '>')
        o.append(S.line(X0 + 9, y, ex, y, stroke=c, stroke_width=7))
        if k == 'b':
            o.append(S.line(ex, y, XM, y, stroke=S.CONC, stroke_width=3, stroke_dasharray='4 7'))
        if ext:
            o.append(S.line(XM, y, ex, y, stroke=S.DIF, stroke_width=7))
            o += S.hatch(XM, y - 16, ex - XM, 32, step=10, stroke=S.DIF, stroke_width=1)
            o.append(S.text((XM + ex) / 2, y + 70, 'prazo compatível com o vulto dos investimentos', size=13, family=S.SERIF, fill=S.DIF, anchor='middle'))
        o.append(S.circle(ex, y, 12, fill=c, stroke=S.INK, stroke_width=2))
        o.append(S.text(ex, y - 28, 'efeito' , size=14, family=S.SANS, weight='600', anchor='middle', fill=c))
        o.append(S.text(60, 332, head, size=21, family=S.SANS, weight='650', fill=vc))
        for i, ln in enumerate(S.wrap(why, 100)):
            o.append(S.text(60, 366 + i * 24, ln, size=16, family=S.SERIF))
        o.append('</g>')
    return S.svg(W, H, 'Denúncia: o efeito e o custo conforme o aviso dado', o), []
