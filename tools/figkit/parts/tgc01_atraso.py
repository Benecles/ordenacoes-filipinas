"""Aula 01, chapter 4: the appeal's verbal installment agreement and the limit on rescission.

The instrument asks whether late payment alone justified rescission. The TJSP appeal
held it did not, invoking objective good faith, social function and the ban on unjust
enrichment (CC arts. 421, 422 and 884). No number or schedule of installments is asserted.
"""
from . import svg as S


def build(p):
    o = []
    W, H = 900, 350
    T = S.text
    # One verbal agreement: the obligation continues through installments; no count or timing is supplied.
    o += [S.path('M130,83 H770 M130,83 V112 M770,83 V112', fill='none', stroke=S.INK, stroke_width=2),
          S.text(450, 62, 'ajuste verbal', size=15, family=S.SANS, weight='600', anchor='middle'),
          S.line(180, 132, 720, 132, stroke=S.INK2, stroke_width=1.5),
          S.circle(180, 132, 7, fill=S.PAPER, stroke=S.INK, stroke_width=2),
          S.circle(720, 132, 7, fill=S.PAPER, stroke=S.CONC, stroke_width=2),
          T(180, 159, 'parcelas do financiamento', size=14, family=S.SANS, anchor='middle'),
          T(720, 159, 'atraso na quitação', size=14, family=S.SANS, anchor='middle'),
          T(450, 202, 'O atraso, por si, bastou para rescindir?', size=16, family=S.SANS, weight='600', anchor='middle')]
    choices = [('a', 'Sim'), ('b', 'Não')]
    for i, (key, label) in enumerate(choices):
        x = 250 + i * 220
        o.append(f'<g data-opt="{key}" tabindex="0" role="button" aria-label="{label}">')
        o.append(S.rect(x, 220, 180, 42, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
        o.append(T(x + 90, 247, label, size=14, family=S.SANS, weight='600', anchor='middle'))
        o.append('</g>')
    for i, (key, label) in enumerate(choices):
        color = S.CONC if key == 'a' else S.DIF
        o.append(f'<g data-ans="{key}"' + ('' if i == 0 else ' display="none"') + '>')
        o.append(S.line(450, 262, 450, 278, stroke=color, stroke_width=2))
        o.append(S.rect(100, 278, 700, 54, fill=S.PAPER, stroke=color, stroke_width=2))
        answer = 'A decisão afastou a rescisão fundada apenas no atraso.' if key == 'b' else 'A decisão não considerou o atraso suficiente, por si, para rescindir.'
        o.append(T(450, 311, answer, size=14, family=S.SANS, weight='600', fill=color, anchor='middle'))
        o.append('</g>')
    return S.svg(W, H, 'Atraso no pagamento das parcelas e limite à rescisão no ajuste verbal', o), []
