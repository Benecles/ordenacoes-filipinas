"""Release 4.2 opening bet and hero for Processo Civil I, Aula 04."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import line, svg, t


def bet():
    return '''<div class="bet" id="a04-opening-bet"><div>
  <span class="bet-k">Antes de ler · escolha o vínculo</span>
  <p class="bet-q">Na ação de despejo, qual relação explica a assistência simples do sublocatário?</p>
  <div class="bet-opts">
    <button type="button" data-opt="0" aria-pressed="false">A relação de sublocação com o locatário, que pode ser atingida reflexamente pela sentença.</button>
    <button type="button" data-opt="1" data-court aria-pressed="false">A relação entre locador e locatário, porque o sublocatário é titular da pretensão de despejo.</button>
    <button type="button" data-opt="2" aria-pressed="false">O interesse econômico em que o locatário vença, mesmo sem relação jurídica entre eles.</button>
  </div>
  <div class="bet-reveal"><p>A relação de sublocação liga o sublocatário ao locatário. A sentença discute a relação entre locador e locatário; sua repercussão na sublocação fundamenta o interesse reflexo.</p></div>
</div></div>'''


def hero():
    """A process record links the sublocatário's petition to the despejo case."""
    o = ''
    o += '<path d="M68 94H185l22 22h325v150H68Z" style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1.8"/>'
    o += '<path d="M94 46H500V218H94Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.8"/>'
    o += '<path d="M94 82H500" style="fill:none;stroke:var(--grid-major);stroke-width:1.2"/>'
    o += t(118, 70, 'AÇÃO DE DESPEJO', size=18, fill='var(--ink)', weight=700)
    o += t(118, 111, 'LOCADOR', size=15, fill='var(--conc)', weight=700)
    o += t(476, 111, 'LOCATÁRIO', size=15, fill='var(--conc)', anchor='end', weight=700)
    o += line(214, 106, 380, 106, tone='conc', w=2)
    o += t(118, 157, 'PEDIDO DE INGRESSO', size=15, fill='var(--ink-2)', weight=700)
    o += t(118, 187, 'SUBLOCATÁRIO', size=14, fill='var(--dif)', weight=700)
    o += t(96, 257, 'RELAÇÃO PRÓPRIA · SUBLOCAÇÃO', size=14, fill='var(--ink-2)', weight=700)
    return svg('48 30 520 250', o, cls='hero-form', label='Registro da ação de despejo entre locador e locatário e do pedido de ingresso do sublocatário para assistir o locatário.').replace('<svg', '<svg data-family="figure.form"', 1)


def inject():
    page = os.path.join(os.path.dirname(__file__), '../../courses/processo-civil-i/aula-04.html')
    with open(page, encoding='utf-8') as f:
        source = f.read()
    if source.count('id="a04-opening-bet"') == 0:
        anchor = '<section class="chapter" aria-labelledby="c1">'
        if source.count(anchor) != 1:
            raise ValueError('Aula 04 opening chapter anchor not found exactly once')
        source = source.replace(anchor, bet() + '\n\n' + anchor, 1)
    elif source.count('id="a04-opening-bet"') != 1:
        raise ValueError('Aula 04 opening bet anchor is duplicated')
    hero_block = '<figure class="hero-drawing" id="a04-release42-hero">' + hero() + '<figcaption class="caption">O sublocatário pede ingresso para assistir o locatário na ação de despejo.</figcaption></figure>'
    if source.count('id="a04-release42-hero"') > 1:
        raise ValueError('Aula 04 hero anchor is duplicated')
    if source.count('id="a04-release42-hero"') == 1:
        start = source.index('<figure class="hero-drawing" id="a04-release42-hero">')
        end = source.index('</figure>', start) + len('</figure>')
        source = source[:start] + source[end:]
    hero_start = source.find('<header class="hero">')
    hero_end = source.find('</header>', hero_start)
    if hero_start < 0 or hero_end < 0:
        raise ValueError('Aula 04 hero header not found')
    source = source[:hero_end] + hero_block + '\n' + source[hero_end:]
    with open(page, 'w', encoding='utf-8') as f:
        f.write(source)


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in {'bet', 'hero', 'inject'}:
        raise SystemExit('usage: python3 tools/figkit/processo_a04_release42.py bet|hero|inject')
    if sys.argv[1] == 'bet':
        print(bet())
    elif sys.argv[1] == 'hero':
        print(hero())
    else:
        inject()
        print('injected A04 release 4.2 opening bet and figure.form hero')
