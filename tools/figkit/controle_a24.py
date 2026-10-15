"""Controle Aula 24 · processamento da ADI/ADC. The two rites as strips (the abbreviated rite's deadlines to
scale: informações 10 days, AGU 5, PGR 5, then the Plenário), and the requirement panels as forms (rito
abreviado, amicus curiae, fact-finding). Ink; blue = what the rule lets the court do; orange = its limit.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a16 import say
from controle_a23 import form


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def step(x, w, y, label, sub='', fill=True):
    st = 'fill:var(--ink)' if fill else 'fill:var(--paper);stroke:var(--ink);stroke-width:1.3'
    o = f'<rect x="{x}" y="{y}" width="{w}" height="30" style="{st}"/>'
    o += t(x + 8, y + 20, label, size=10, caps=True, weight=700, fill='var(--paper)' if fill else 'var(--ink)')
    if sub:
        o += t(x, y + 48, sub, size=10, fill='var(--ink-2)')
    return o


def ordinario():
    o = head('Rito ordinário')
    xs = [(40, 'ajuizamento'), (160, 'cautelar'), (290, 'mérito'), (430, 'julgamento')]
    for i, (x, s) in enumerate(xs):
        o += step(x, 110, 120, s, 'tempo próprio', fill=(i != 1))
    o += '<line x1="40" y1="200" x2="560" y2="200" style="stroke:var(--ink-2);stroke-width:1"/>'
    o += say(40, 280, 'Etapas sucessivas, cada uma com seu calendário.')
    o += say(40, 304, 'A cautelar é decidida em separado.', 16, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-ordinario',
               label='Quatro etapas em sequência: ajuizamento, cautelar decidida em separado, mérito e julgamento, cada uma no seu tempo')


def abreviado():
    o = head('Rito abreviado · art. 12 da Lei 9.868/1999')
    day = 20                                            # px per day
    x0 = 40
    o += step(x0, 10 * day, 120, 'informações', '10 dias', fill=False)
    o += step(x0 + 10 * day, 5 * day, 120, 'AGU', '5 dias', fill=False)
    o += step(x0 + 15 * day, 5 * day, 120, 'PGR', '5 dias', fill=False)
    o += f'<rect x="{x0 + 20 * day + 12}" y="112" width="134" height="46" style="fill:var(--dif)"/>'
    o += t(x0 + 20 * day + 79, 132, 'Plenário', size=10.5, anchor='middle', weight=700, caps=True, fill='var(--paper)')
    o += t(x0 + 20 * day + 79, 148, 'cautelar + mérito', size=9.5, anchor='middle', caps=True, fill='var(--paper)')
    o += '<line x1="40" y1="200" x2="440" y2="200" style="stroke:var(--ink-2);stroke-width:1"/>' + t(40, 218, '0', size=10, fill='var(--ink-2)') + t(440, 218, '20 dias', size=10, anchor='end', fill='var(--ink-2)')
    o += say(40, 290, 'O relator leva o processo direto ao Plenário,')
    o += say(40, 314, 'que julga em definitivo: cautelar e mérito fundidos.', 16, 'var(--dif)')
    o += say(40, 358, 'Em matéria relevante, a cautelar de uma só cabeça', 16, 'var(--conc)', True)
    o += say(40, 382, 'pode ser desaconselhável.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-abreviado',
               label='Uma faixa de vinte dias em escala: informações em dez dias, AGU e PGR em cinco cada; depois o Plenário julga cautelar e mérito juntos')


def condicoes():
    return form('p-condicoes', 'Rito abreviado · condições',
                [('Relevância da matéria', True), ('Especial significado social e para a segurança jurídica', True), ('Faculdade do relator de conferir o rito', True)],
                notes=[('Previsto para a ADI; cabível também na ADC:', 'var(--ink)'), ('ações “com sinal trocado”.', 'var(--ink-2)')],
                label='Formulário com três caixas marcadas para o rito abreviado: relevância, especial significado e faculdade do relator; cabe também na ADC')


def amicus():
    return form('p-amicus', 'Amicus curiae · art. 7º, § 2º',
                [('Relevância da matéria', True), ('Representatividade dos postulantes', True)],
                stamp=('despacho irrecorrível', 'var(--dif)', 250),
                notes=[('O relator pode admitir a manifestação', 'var(--ink)'), ('de outros órgãos ou entidades.', 'var(--ink)')],
                label='Formulário do amicus curiae com duas caixas, relevância e representatividade, e o carimbo despacho irrecorrível')


def mitigacao():
    return form('p-mitigacao', 'Quando os fatos entram na ADI',
                [('Precisa esclarecer matéria de fato?', True), ('Ou as informações dos autos são insuficientes?', False)],
                stamp=('prazo comum: 30 dias', 'var(--ink)', 250),
                notes=[('Basta uma das duas caixas.', 'var(--ink)'), ('O relator pode requisitar dados, designar perícia', 'var(--ink)'), ('ou ouvir em audiência pública (arts. 9º e 20, § 1º).', 'var(--ink)')],
                label='Formulário: basta uma das caixas, fatos a esclarecer ou informação insuficiente, para o relator requisitar dados, perícia ou audiência pública, em prazo comum de trinta dias')


def panels():
    return [ordinario(), abreviado(), condicoes(), amicus(), mitigacao()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-24.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
