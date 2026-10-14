"""Controle Aula 15 · interpretação conforme: one norm, its readings, and the frame of what the text can mean.
Every panel draws the same object: the text on top, its possible readings as slips below, inside the frame
of the text's possible sense (the orange line is that limit). The court strikes only the reading that
collides with the Constitution (blue = what it decides); the others stay; a reading outside the frame would
be creation, not interpretation.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def say(x, y, s, size=16, fill='var(--ink)', italic=False):
    return f'<text x="{x}" y="{y}" style="font-family:var(--serif,serif);font-size:{size}px;fill:{fill}{";font-style:italic" if italic else ""}">{s}</text>'


def text_sheet(y=70):
    o = f'<path d="M40 {y}H546L560 {y + 14}V{y + 54}H40Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    o += t(54, y + 22, 'Texto · art. N da Lei X', size=10.5, caps=True, fill='var(--ink-2)')
    o += say(54, y + 44, 'Um só texto, mais de um sentido possível.', 15)
    return o


def frame(y0=150, y1=380, x1=560, label=True):
    o = f'<rect x="40" y="{y0}" width="{x1 - 40}" height="{y1 - y0}" style="fill:none;stroke:var(--conc);stroke-width:1.8"/>'
    if label:
        o += t(48, y0 - 8, 'o sentido possível do texto', size=10, caps=True, fill='var(--conc)')
    return o


def slip(x, y, name, sub, state='keep', w=150):
    """state: keep | struck | outside | open"""
    st = 'fill:var(--paper);stroke:var(--ink);stroke-width:1.3'
    if state == 'outside':
        st = 'fill:none;stroke:var(--ink-2);stroke-width:1.2;stroke-dasharray:4 4'
    o = f'<rect x="{x}" y="{y}" width="{w}" height="58" style="{st}"/>'
    o += t(x + 12, y + 22, name, size=11, weight=700, caps=True, fill='var(--ink)' if state != 'outside' else 'var(--ink-2)')
    o += say(x + 12, y + 44, sub, 14, 'var(--ink)' if state != 'outside' else 'var(--ink-2)')
    if state == 'struck':
        o += f'<line x1="{x - 6}" y1="{y + 29}" x2="{x + w + 6}" y2="{y + 29}" style="stroke:var(--dif);stroke-width:2.6"/>'
    return o


READS = [('Leitura 1', 'compatível'), ('Leitura 2', 'compatível'), ('Leitura 3', 'colide com a CF')]


def conceito():
    o = head('Interpretação conforme') + text_sheet() + frame()
    o += slip(56, 200, 'Leitura 1', 'compatível') + slip(222, 200, 'Leitura 2', 'compatível') + slip(388, 200, 'Leitura 3', 'colide com a CF', 'struck')
    o += say(56, 320, 'O texto fica. Afasta-se o sentido que colide.', 16)
    o += say(40, 430, 'Qualquer juízo, em qualquer instância.')
    o += say(40, 460, 'Sem reserva de plenário (art. 97 da CF):', 16, 'var(--ink-2)', True)
    o += say(40, 484, 'não declara a norma inconstitucional.', 16, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-conceito',
               label='O texto da norma e três leituras dentro da moldura do sentido possível; só a leitura que colide com a Constituição é riscada, e o texto fica')


def limite():
    o = head('O limite: continuar sendo interpretação') + text_sheet() + frame(x1=420)
    o += slip(56, 200, 'Leitura 1', 'cabe no texto') + slip(240, 200, 'Leitura 2', 'cabe no texto')
    o += slip(436, 200, 'Leitura 4', 'muda a escolha', 'outside', w=124)
    o += t(432, 300, 'criação normativa', size=10, caps=True, fill='var(--ink-2)')
    o += say(40, 430, 'Dentro da moldura: interpretação, que preserva')
    o += say(40, 454, 'a obra do legislador.')
    o += say(40, 498, 'Fora dela, o tribunal legislaria.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-limite',
               label='A moldura do sentido possível: leituras dentro dela são interpretação; uma leitura fora, que muda a escolha do legislador, seria criação normativa')


def pluralidade():
    o = head('Leituras da mesma norma') + text_sheet() + frame()
    o += slip(56, 200, 'Leitura 1', 'fica') + slip(222, 200, 'Leitura 2', 'fica') + slip(388, 200, 'Leitura 3', 'colide de frente', 'struck')
    o += say(40, 430, 'Só se afasta a leitura que colide de frente.')
    o += say(40, 458, 'As outras podem conviver com a do tribunal.', 16, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-pluralidade',
               label='Três leituras da mesma norma: duas ficam e convivem; só a que colide de frente com a interpretação do tribunal é afastada')


def abertura():
    o = head('Princípios abertos') + text_sheet() + frame()
    for i, (x, y) in enumerate([(56, 180), (222, 180), (388, 180), (139, 270), (305, 270)]):
        o += slip(x, y, f'Leitura {i + 1}', 'possível')
    o += say(40, 430, 'Sem erro evidente, várias alternativas cabem.')
    o += say(40, 458, 'O tribunal confia a escolha ao processo político:', 16, 'var(--ink-2)', True)
    o += say(40, 482, 'Legislativo e Executivo.', 16, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-abertura',
               label='Um princípio aberto com cinco leituras possíveis, nenhuma riscada: a escolha fica com o processo político')


def favor():
    o = head('Última palavra, sem exclusividade') + text_sheet() + frame()
    o += t(56, 190, 'Legislativo e Executivo · escolhem dentro', size=10.5, caps=True)
    o += slip(56, 210, 'Leitura 1', 'escolhida') + slip(222, 210, 'Leitura 2', 'possível')
    o += t(56, 312, 'Judiciário · guarda a moldura', size=10.5, caps=True, fill='var(--dif)')
    o += f'<path d="M40 330 H560" style="stroke:var(--dif);stroke-width:3"/>'
    o += say(40, 430, 'Espaço de apreciação para os outros Poderes;')
    o += say(40, 454, 'a última palavra, ao Judiciário.')
    o += say(40, 498, 'Favor legis: preserva a lei.', 16, 'var(--dif)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-favor',
               label='Legislativo e Executivo escolhem uma leitura dentro da moldura; o Judiciário guarda a borda e dá a última palavra; favor legis')


def panels():
    return [conceito(), limite(), pluralidade(), abertura(), favor()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-15.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
