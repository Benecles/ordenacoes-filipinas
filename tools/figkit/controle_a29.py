"""Controle Aula 29 · eficácia e efeito vinculante, as the document family: a decision drawn as paper with
its two parts. The dispositivo (what is decided, blue) has general effect; the fundamentos (the ratio) explain
why. Transcendence is the same ratio passage carried into a second decision on another subject, dashed,
because the lesson presents it as a theory, never as the STF's general rule.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a16 import say


def decision(x, y, w, title, ratio, dispositivo, ratio_style='solid', disp=True):
    h = 250
    o = f'<path d="M{x} {y}H{x + w - 14}L{x + w} {y + 14}V{y + h}H{x}Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    o += t(x + 14, y + 26, title, size=10.5, weight=700, caps=True)
    o += t(x + 14, y + 58, 'Fundamentos', size=9.5, caps=True, fill='var(--ink-2)')
    dash = ';stroke-dasharray:5 4' if ratio_style == 'dashed' else ''
    o += f'<rect x="{x + 10}" y="{y + 68}" width="{w - 20}" height="58" style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1.2{dash}"/>'
    o += say(x + 20, y + 92, 'ratio decidendi', 13, 'var(--ink-2)', True) + say(x + 20, y + 114, ratio, 14)
    o += ''.join(f'<line x1="{x + 14}" y1="{y + 142 + i * 12}" x2="{x + w - 30 - (i % 2) * 30}" y2="{y + 142 + i * 12}" style="stroke:var(--ink-2);stroke-width:1"/>' for i in range(3))
    if disp:
        o += t(x + 14, y + 196, 'Dispositivo', size=9.5, caps=True, fill='var(--dif)')
        o += f'<rect x="{x + 10}" y="{y + 204}" width="{w - 20}" height="34" style="fill:none;stroke:var(--dif);stroke-width:2"/>'
        o += say(x + 20, y + 226, dispositivo, 14, 'var(--dif)')
    return o


def p_decisao():
    o = t(40, 44, 'A decisão · duas partes', size=11.5, weight=700, caps=True, ls='.12em')
    o += decision(40, 70, 520, 'ADI · acórdão', 'por que a lei é inconstitucional', 'a lei é inconstitucional')
    o += say(40, 380, 'A eficácia contra todos alcança o dispositivo:')
    o += say(40, 404, 'a conclusão, com força de lei, desde a ata.', 16, 'var(--dif)')
    o += say(40, 448, 'Os fundamentos explicam o porquê.', 16, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-decisao',
               label='Um acórdão desenhado com duas partes: os fundamentos, a ratio, e o dispositivo em azul, a conclusão com eficácia geral')


def p_transc():
    o = t(40, 44, 'Transcendência dos motivos · hipótese', size=11.5, weight=700, caps=True, ls='.12em')
    o += decision(40, 70, 250, 'Processo A · assunto X', 'o Estado é laico', 'decide X')
    o += decision(310, 70, 250, 'Processo B · assunto Y', 'o Estado é laico', '', ratio_style='dashed', disp=False)
    o += '<path d="M290 167 C 300 160, 300 160, 316 167" style="fill:none;stroke:var(--ink);stroke-width:1.4"/><path d="M310 163 l7 4 l-7 4" style="fill:none;stroke:var(--ink);stroke-width:1.4"/>'
    o += say(40, 380, 'A teoria: a ratio de A orientaria B, noutro assunto.')
    o += say(40, 424, 'Exemplo hipotético; uma proposta teórica,', 16, 'var(--conc)', True)
    o += say(40, 448, 'fora da regra geral do STF.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-transc',
               label='Dois acórdãos: o fundamento do processo A, o Estado é laico, aparece tracejado no processo B, sobre outro assunto; hipótese teórica, não regra do STF')


def panels():
    return [p_decisao(), p_transc()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-29.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
