"""Controle Aula 21 · requisitos da petição e limites do pedido. The rite's four steps (the strip from Aulas
24–25); the hearing as a form; the open causa de pedir as a petition whose fundamento the STF may swap (art. Z
→ art. Y); the closed pedido (adstrição) and its exception (arrastamento) as struck norms, the same drawing as
Aula 14.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a16 import say
from controle_a24 import step
from controle_a23 import form
from controle_a14 import sheet


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def fases():
    o = head('Processamento · Lei 9.868/1999')
    for x, s in [(40, 'ajuizamento'), (160, 'cautelar'), (290, 'mérito'), (430, 'julgamento')]:
        o += step(x, 110, 120, s, 'manifestações' if s in ('cautelar', 'mérito') else '', fill=(s != 'cautelar'))
    o += say(40, 260, 'A urgência só dispensa a audiência na cautelar.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-fases', label='As quatro fases do rito, com manifestações na cautelar e no mérito')


def manif():
    return form('p-manif', 'Manifestações · cautelar e mérito',
                [('Autoridades responsáveis pela norma', True), ('Procurador-Geral da República', True), ('Advogado-Geral da União (não na ADC)', True)],
                notes=[('Se urgente, na cautelar, a manifestação é facultativa;', 'var(--ink)'), ('no mérito, continua prevista.', 'var(--ink-2)')],
                label='Formulário das manifestações: autoridades responsáveis, PGR e AGU, esta não na ADC; a urgência só dispensa a audiência na cautelar')


def parametro():
    o = head('Parâmetro: a causa de pedir é aberta')
    o += '<path d="M40 70H546L560 84V250H40Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    o += t(60, 100, 'ADI · petição inicial', size=11, weight=700, caps=True)
    o += t(60, 136, 'Pedido', size=10, caps=True, fill='var(--ink-2)') + say(160, 136, 'inconstitucionalidade da Lei X', 15)
    o += t(60, 176, 'Fundamento', size=10, caps=True, fill='var(--ink-2)') + say(160, 176, 'viola o art. Z da CF', 15)
    o += '<line x1="156" y1="171" x2="320" y2="171" style="stroke:var(--ink-2);stroke-width:1.6"/>'
    o += say(160, 214, 'viola o art. Y da CF', 15, 'var(--dif)') + t(350, 214, 'o STF pode aplicar', size=10, caps=True, fill='var(--dif)')
    o += say(40, 320, 'O STF pode julgar a Lei X inconstitucional por outro')
    o += say(40, 344, 'artigo da Constituição: o fundamento é aberto.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-parametro',
               label='Uma petição de ADI: o pedido contra a Lei X fica; o fundamento indicado, art. Z, pode dar lugar ao art. Y, que o STF aplica')


def objeto():
    o = head('Objeto: o pedido é fechado')
    s1, _ = sheet(40, 70, 250, 'Lei X · impugnada', ['Art. 1º …'], struck=[0])
    s2, _ = sheet(310, 70, 250, 'Lei Y · não impugnada', ['Art. 1º …'])
    o += s1 + s2 + t(310, 190, 'adstrição: fica', size=10, caps=True, fill='var(--conc)')
    o += say(40, 280, 'Questionada a Lei X, o STF não declara de ofício')
    o += say(40, 304, 'a Lei Y; o mesmo vale entre dispositivos.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-objeto',
               label='Duas leis: a Lei X impugnada, riscada; a Lei Y, não impugnada, intocada pela regra da adstrição')


def arrasta():
    o = head('A exceção: arrastamento')
    s, _ = sheet(40, 70, 400, 'Lei X', ['Disp. A · impugnado', 'Disp. B · conexo, depende de A'], struck=[0], dashed=[1])
    o += s + t(452, 124, 'pedido', size=10, caps=True, fill='var(--dif)') + t(452, 150, 'cai junto', size=10, caps=True, fill='var(--dif)')
    o += say(40, 260, 'Pela interdependência, o STF alcança B de ofício:')
    o += say(40, 284, 'inconstitucionalidade por arrastamento (Aula 14).', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-arrasta',
               label='Na mesma lei, o dispositivo A impugnado e riscado; o B, conexo, riscado com ele, tracejado: arrastamento')


def panels():
    return [fases(), manif(), parametro(), objeto(), arrasta()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-21.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
