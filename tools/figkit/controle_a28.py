"""Controle Aula 28 · modulação de efeitos (art. 27 da Lei 9.868/1999). The vote condition is a form with
the 8-of-11 quorum drawn as seats; the effects are the tracks family: the declared law's track struck back to
its origin (ex tunc, the rule) or only from a chosen mark (trânsito em julgado or another date: the
exception). Blue = what the STF decides; orange = the limit. Replaces panels whose <em> inside <svg> broke
the drawing (see tools/svg_breakout_check.py).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a16 import say
from controle_a20 import tick

X0, XJ, X1 = 60, 360, 560


def art27():
    o = t(40, 44, 'Art. 27 · quando o STF pode modular', size=11.5, weight=700, caps=True, ls='.12em')
    o += '<path d="M40 70H546L560 84V200H40Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    o += tick(60, 112) + say(94, 112, 'Segurança jurídica  ou  excepcional interesse social', 15)
    o += tick(60, 160) + say(94, 160, 'Maioria de dois terços dos membros', 15)
    for i in range(11):
        filled = i < 8
        o += f'<circle cx="{70 + i * 30}" cy="250" r="9" style="{"fill:var(--ink)" if filled else "fill:none;stroke:var(--ink);stroke-width:1.4"}"/>'
    o += t(40, 286, '8 de 11 ministros', size=10.5, caps=True, fill='var(--ink-2)')
    o += say(40, 350, '“Poderá”: uma faculdade do STF.', 16, 'var(--dif)')
    o += say(40, 390, 'Faltou um requisito, não há modulação.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-art27',
               label='Formulário do art. 27: segurança jurídica ou excepcional interesse social, e dois terços dos membros, oito de onze cadeiras preenchidas; a modulação é faculdade')


def law_track(y, cut_from, label):
    o = t(X0, y - 10, label, size=10.5, caps=True, fill='var(--ink-2)')
    if cut_from > X0:
        o += f'<rect x="{X0}" y="{y}" width="{cut_from - X0}" height="22" style="fill:var(--ink)"/>'
    o += f'<rect x="{cut_from}" y="{y}" width="{X1 - cut_from}" height="22" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>'
    o += f'<line x1="{cut_from}" y1="{y + 11}" x2="{X1}" y2="{y + 11}" style="stroke:var(--dif);stroke-width:3"/>'
    o += f'<line x1="{cut_from}" y1="{y - 6}" x2="{cut_from}" y2="{y + 28}" style="stroke:var(--dif);stroke-width:2"/>'
    return o


def axis(y=330):
    o = f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" style="stroke:var(--ink-2);stroke-width:1"/>'
    for x, s in ((X0, 'a lei nasce'), (XJ, 'julgamento')):
        o += f'<line x1="{x}" y1="{y - 5}" x2="{x}" y2="{y + 5}" style="stroke:var(--ink);stroke-width:1.2"/>' + t(x, y + 22, s, size=10, anchor='middle' if x != X0 else 'start', caps=True)
    return o


def linha1():
    o = t(40, 44, 'Regra e exceção no tempo', size=11.5, weight=700, caps=True, ls='.12em')
    o += law_track(110, X0, 'regra · ex tunc: retroage à origem')
    o += law_track(200, XJ, 'exceção · ex nunc: vale daqui para frente')
    o += axis(280)
    o += say(40, 380, 'A regra apaga a lei desde que nasceu.')
    o += say(40, 404, 'Modulando, o STF fixa o marco do apagamento.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-linha1',
               label='Duas faixas da mesma lei: na regra, riscada desde a origem, ex tunc; na exceção, riscada só a partir do julgamento, ex nunc')


def linha2():
    o = t(40, 44, 'Um marco escolhido e justificado', size=11.5, weight=700, caps=True, ls='.12em')
    o += law_track(110, 430, 'efeitos diferidos · outra data fixada')
    o += f'<path d="M{XJ} 150 H430" style="stroke:var(--conc);stroke-width:1.6;stroke-dasharray:4 4"/>' + t(395, 166, 'intervalo', size=10, anchor='middle', caps=True, fill='var(--conc)')
    o += axis(240)
    o += say(40, 330, 'Trânsito em julgado ou outra data: o STF escolhe')
    o += say(40, 354, 'e justifica por que a retroação total comprometeria')
    o += say(40, 378, 'a segurança jurídica ou o interesse social.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-linha2',
               label='A faixa da lei riscada a partir de uma data posterior ao julgamento, escolhida e justificada pelo STF')


def panels():
    return [art27(), linha1(), linha2()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-28.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
