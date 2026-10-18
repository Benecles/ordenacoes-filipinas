"""Release 4.2 figures for Processo Civil I, Aula 01."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import line, svg, t


def hero():
    """A filed initial petition is the first record in the autos."""
    o = ''
    # The bound case file is the object; the petition is the visible first sheet.
    o += '<path d="M64 72H190l20 20h386v194H64Z" style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1.6"/>'
    o += '<path d="M88 42H516V226H88Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.6"/>'
    o += '<path d="M88 74H516" style="fill:none;stroke:var(--grid-major);stroke-width:1.2"/>'
    o += t(112, 64, 'PETIÇÃO INICIAL', size=20, fill='var(--ink)', weight=700)
    o += t(112, 103, 'DEMANDA', size=16, fill='var(--ink-2)', weight=700)
    o += t(112, 129, 'sujeitos · causa · pedido', size=20, fill='var(--ink)')
    o += line(112, 146, 485, 146, tone='ink', w=1)
    o += t(112, 168, 'protocolo', size=17, fill='var(--dif)', weight=700)
    o += t(112, 204, 'propositura da ação', size=20, fill='var(--ink)')
    o += t(86, 264, 'AUTOS · REGISTRO INICIAL', size=16, fill='var(--ink-2)', weight=700)
    return svg('48 28 544 278', o, cls='hero-form', label='Petição inicial registrada nos autos; o protocolo marca a propositura da ação.').replace('<svg', '<svg data-family="figure.autos"', 1)


def timeline_panel(n):
    """One art. 329 state, with earlier and later positions visible for comparison."""
    xs = [85, 300, 515]
    labels = ['PROTOCOLO', 'CITAÇÃO', 'SANEAMENTO']
    o = t(40, 42, 'CPC · ART. 329', size=18, fill='var(--ink-2)', weight=700)
    o += line(40, 58, 560, 58, tone='ink', w=1.2)
    # The process line is a measured sequence, not an arrow diagram.
    if n == 0:
        o += line(xs[0], 232, xs[1], 232, tone='dif', w=6)
        o += line(xs[1], 232, xs[2], 232, tone='conc', w=6)
        active = 0
        o += t(300, 126, 'SEM CONSENTIMENTO', size=18, fill='var(--dif)', anchor='middle', weight=700)
        o += t(300, 151, 'até a citação', size=18, fill='var(--ink)', anchor='middle')
    elif n == 1:
        o += line(xs[0], 232, xs[1], 232, tone='dif', w=6)
        o += line(xs[1], 232, xs[2], 232, tone='conc', w=6)
        active = 1
        o += t(418, 126, 'CONSENTIMENTO DO RÉU', size=17, fill='var(--conc)', anchor='middle', weight=700)
        o += t(418, 151, 'manifestação por 15 dias', size=17, fill='var(--ink)', anchor='middle')
        o += t(380, 176, 'requerimento de prova suplementar', size=18, fill='var(--ink)', anchor='middle')
    else:
        o += line(xs[0], 232, xs[1], 232, tone='dif', w=6)
        o += line(xs[1], 232, xs[2], 232, tone='conc', w=6)
        active = 2
        o += t(418, 126, 'JANELA ENCERRADA', size=18, fill='var(--conc)', anchor='middle', weight=700)
        o += t(418, 151, 'depois do saneamento', size=18, fill='var(--ink)', anchor='middle')
    for i, x in enumerate(xs):
        if i == active:
            o += f'<circle cx="{x}" cy="232" r="12" style="fill:{"var(--dif)" if n == 0 else "var(--conc)"};stroke:var(--paper);stroke-width:3"/>'
        else:
            tone = 'var(--ink-2)' if i < active else 'var(--conc)'
            o += f'<circle cx="{x}" cy="232" r="9" style="fill:var(--paper);stroke:{tone};stroke-width:2"/>'
        o += t(x, 269, labels[i], size=18, fill='var(--ink)', anchor='middle', weight=700)
    o += t(300, 352, 'PEDIDO OU CAUSA DE PEDIR', size=17, fill='var(--ink-2)', anchor='middle', weight=700)
    return svg('0 0 600 400', o, cls='panel', label=[
        'Art. 329: até a citação, pedido ou causa de pedir podem ser alterados sem consentimento do réu.',
        'Art. 329: entre citação e saneamento, a alteração exige consentimento do réu, contraditório por pelo menos 15 dias e possibilidade de prova suplementar.',
        'Art. 329: encerrado o saneamento, termina a janela legal de alteração do pedido ou da causa de pedir.'
    ][n]).replace('<svg', '<svg data-family="figure.timeline"', 1)


def scrolly():
    specs = [
        ('p-a01-art329-1', 'Até a citação', 'O autor pode aditar ou alterar o pedido ou a causa de pedir sem consentimento do réu.'),
        ('p-a01-art329-2', 'Da citação ao saneamento', 'A alteração exige consentimento do réu, contraditório por pelo menos 15 dias e possibilidade de requerer prova suplementar.'),
        ('p-a01-art329-3', 'Depois do saneamento', 'A janela do art. 329 se encerra com o saneamento do processo.'),
    ]
    panels = ''.join(timeline_panel(i).replace('class="panel figkit"', f'class="panel figkit{" on" if i == 0 else ""}"').replace('aria-label=', f'id="{specs[i][0]}" aria-label=') for i in range(3))
    steps = ''.join(
        f'<div class="step{" on" if i == 0 else ""}" data-panel="{specs[i][0]}" data-slides="{specs[i][1]}"><div class="card"><span class="label">Art. 329</span><h3>{specs[i][1]}</h3><p>{specs[i][2]}</p></div></div>'
        for i in range(3)
    )
    return (
        '<div class="scrolly" aria-labelledby="fig2cap"><div class="stage" aria-hidden="true"><figure>' + panels +
        '<figcaption id="fig2cap"><span>A janela para alterar pedido ou causa de pedir depende do estágio do processo.</span><span class="stage-count">1 / 3</span></figcaption></figure></div>' +
        '<div class="steps">' + steps + '</div></div>'
    )


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in {'hero', 'scrolly'}:
        raise SystemExit('usage: python3 tools/figkit/processo_a01_release42.py hero|scrolly')
    print(hero() if sys.argv[1] == 'hero' else scrolly())
