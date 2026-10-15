"""Controle Aula 25 · medida cautelar na ADI/ADC, from the house families: art. 102, I, 'p' as text; the law's
track suspended provisionally and struck at the merits (tracks); the two requirements and the urgency
exception as forms; the two quorums as the eleven seats of the Plenário (8 present to sit, 6 to grant); the
effects as the struck track (ex nunc by rule, ex tunc by express decision); the dismissal as a stamped record.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a16 import say, track
from controle_a23 import form
from controle_a28 import law_track, axis
from controle_a24 import step
from controle_a09 import stamp


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def comp():
    o = head('CF · art. 102, I, “p”')
    o += '<rect x="40" y="70" width="520" height="120" style="fill:var(--paper-2)"/><rect x="40" y="70" width="3" height="120" style="fill:var(--dif)"/>'
    o += say(58, 104, 'Compete ao Supremo Tribunal Federal [...] processar', 15)
    o += say(58, 128, 'e julgar, originariamente, [...] o pedido de medida', 15)
    o += say(58, 152, 'cautelar das ações diretas de inconstitucionalidade.', 15)
    o += say(40, 250, 'Cabe quando é urgente afastar a aplicação')
    o += say(40, 274, 'da norma objeto da ADI.', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-comp',
               label='O texto do art. 102, inciso I, alínea p: compete ao STF julgar originariamente o pedido de medida cautelar nas ações diretas')


def adianta():
    o = head('A cautelar adianta a retirada')
    o += track(130, [(60, 260, 'on'), (260, 430, 'decided'), (430, 540, 'off')], 'a lei objeto da ADI')
    o += t(260, 186, 'cautelar · suspende', size=10, caps=True, fill='var(--dif)') + t(430, 202, 'mérito · retira', size=10, caps=True)
    o += say(40, 290, 'Suspende provisoriamente, sem esperar o mérito.')
    o += say(40, 330, 'A suspensão não encerra a ADI.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-adianta',
               label='A faixa da lei: a cautelar a suspende provisoriamente, em azul, e o julgamento de mérito a retira de vez')


def req():
    return form('p-req', 'Dois requisitos, os dois', [('Plausibilidade da inconstitucionalidade · fumus boni iuris', True), ('Perigo na demora · periculum in mora', True)],
                stamp=('pode suspender', 'var(--dif)', 250),
                notes=[('Faltou um, a cautelar é indeferida.', 'var(--conc)')],
                label='Formulário com duas caixas marcadas, fumus boni iuris e periculum in mora, e o carimbo pode suspender')


def fluxo():
    o = head('ADI / ADC · processamento')
    for i, (x, s) in enumerate([(40, 'ajuizamento'), (160, 'cautelar'), (290, 'mérito'), (430, 'julgamento')]):
        o += step(x, 110, 120, s, 'ouvidos antes' if s in ('cautelar', 'mérito') else '', fill=(s != 'cautelar'))
    o += say(40, 260, 'Cautelar e mérito: antes de decidir, as autoridades')
    o += say(40, 284, 'responsáveis pela norma, o PGR e a AGU (não na ADC).', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-fluxo',
               label='Quatro marcos do processamento, com a audiência prévia antes da cautelar e do mérito')


def urgente():
    return form('p-fluxo-urgente', 'Audiência prévia à cautelar', [('Excepcional urgência', True)],
                stamp=('pode decidir sem ouvir', 'var(--dif)', 206),
                notes=[('A regra manda ouvir as autoridades;', 'var(--ink)'), ('a urgência torna a manifestação facultativa.', 'var(--ink-2)')],
                label='Formulário com uma caixa, excepcional urgência, e o carimbo pode decidir sem ouvir')


def seats(present, votes=0, dashed=False):
    o = ''
    for i in range(11):
        x = 60 + i * 46
        if dashed:
            st = 'fill:none;stroke:var(--ink-2);stroke-width:1.2;stroke-dasharray:3 3'
        elif i < votes:
            st = 'fill:var(--dif)'
        elif i < present:
            st = 'fill:var(--ink)'
        else:
            st = 'fill:none;stroke:var(--ink);stroke-width:1.3'
        o += f'<circle cx="{x}" cy="150" r="15" style="{st}"/>'
    return o


def q8():
    o = head('Art. 22 · quórum da sessão') + seats(8)
    o += t(40, 200, '8 de 11 presentes', size=10.5, caps=True, fill='var(--ink-2)')
    o += say(40, 260, 'Oito ministros presentes instalam a sessão.')
    o += say(40, 284, 'Sessão presencial.', 16, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-q8', label='Onze cadeiras, oito ocupadas: o quórum de instalação do art. 22')


def q6():
    o = head('Art. 10 · quórum para deferir') + seats(8, 6)
    o += t(40, 200, '6 votos pela concessão · maioria absoluta', size=10.5, caps=True, fill='var(--dif)')
    o += say(40, 260, 'Com a sessão instalada, seis votos concedem')
    o += say(40, 284, 'a cautelar, ainda que dois divirjam.', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-q6',
               label='As mesmas cadeiras: oito presentes, seis em azul votando pela concessão, maioria absoluta do art. 10')


def virtual():
    o = head('Plenário virtual') + seats(0, dashed=True)
    o += say(40, 260, 'Sem sessão presencial, não há quórum de instalação:')
    o += say(40, 284, 'a distinção entre os dois quóruns perde força.', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-virtual', label='As cadeiras tracejadas: no plenário virtual não há sessão presencial a instalar')


def exnunc():
    o = head('Art. 11 · efeitos da cautelar')
    o += law_track(110, 360, 'regra · ex nunc: da cautelar em diante')
    o += law_track(200, 60, 'exceção · ex tunc: se o Tribunal decidir')
    o += axis(280).replace('JULGAMENTO', 'CAUTELAR')
    o += say(40, 370, 'Eficácia contra todos. A legislação anterior volta')
    o += say(40, 394, 'a valer, salvo manifestação em contrário (Aula 26).', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-exnunc',
               label='Duas faixas: pela regra, a lei é suspensa a partir da cautelar, ex nunc; por decisão expressa, desde a origem, ex tunc')


def indef():
    o = head('Se a cautelar for indeferida')
    o += '<path d="M40 70H546L560 84V230H40Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    o += t(60, 100, 'ADI · pedido de medida cautelar', size=11, weight=700, caps=True)
    o += ''.join(f'<line x1="60" y1="{124 + i * 16}" x2="{500 - (i % 2) * 80}" y2="{124 + i * 16}" style="stroke:var(--ink-2);stroke-width:1"/>' for i in range(4))
    o += stamp(420, 200, 'indeferida', 'var(--conc)')
    o += say(40, 300, 'O indeferimento não confirma a constitucionalidade')
    o += say(40, 324, 'nem produz efeito vinculante.')
    o += say(40, 368, 'Contra ele, não cabe reclamação.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-indef',
               label='O pedido de cautelar carimbado indeferida: sem efeito vinculante e sem reclamação')


def panels():
    return [comp(), adianta(), req(), fluxo(), urgente(), q8(), q6(), virtual(), exnunc(), indef()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-25.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
