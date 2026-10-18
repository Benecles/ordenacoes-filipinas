"""Aula 11-mérito: statutory convergence and the still-open cognitive phase.

All legal labels follow the captured CPC arts. 203 §§1–2 and 356 caput,
I–II and §§1–5 in the Aula 11-mérito compendium. The lengths are schematic;
they assert no quantity, duration, or order beyond the statutory relations.
"""

from pathlib import Path
import re

from figkit import line, svg, t


ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / 'courses/processo-civil-i/aula-11-merito.html'
HERO_START, HERO_END = '<!-- A11M_42_HERO_START -->', '<!-- A11M_42_HERO_END -->'
BET_START, BET_END = '<!-- A11M_42_BET_START -->', '<!-- A11M_42_BET_END -->'
TABLE_START, TABLE_END = '/* A11M_42_TABLE_START */', '/* A11M_42_TABLE_END */'


def _arrow(x, y, tone='ink'):
    """Open continuation, using the kit's line grammar."""
    return (line(x - 11, y - 7, x, y, tone=tone, w=2)
            + line(x - 11, y + 7, x, y, tone=tone, w=2))


def grounds_panel():
    """Art. 356 I–II converge on the caput's bounded object."""
    o = ''
    o += t(42, 48, 'ART. 356  /  DUAS CONDIÇÕES, UM RECORTE', size=14, weight=700)
    o += line(42, 64, 1038, 64, w=1.25)

    # The two alternative grounds are exactly the caput's incisos I–II.
    o += t(42, 111, 'I', size=16, fill='var(--conc)', weight=700)
    o += t(78, 111, 'INCONTROVERSO', size=13, weight=700)
    o += line(42, 130, 460, 130, tone='conc', w=3)
    o += t(42, 224, 'II', size=16, fill='var(--conc)', weight=700)
    o += t(78, 224, 'CONDIÇÕES DE IMEDIATO JULGAMENTO', size=13, weight=700)
    o += t(78, 244, 'nos termos do art. 355', size=11, fill='var(--ink-2)')
    o += line(42, 262, 460, 262, tone='conc', w=3)

    # Either ground reaches the same bounded decision; this is a path, not rows of text.
    o += line(460, 130, 570, 196, tone='conc', w=2.2)
    o += line(460, 262, 570, 196, tone='conc', w=2.2)
    o += line(570, 179, 570, 213, tone='dif', w=4)
    o += line(570, 196, 1008, 196, tone='dif', w=3)
    o += t(613, 177, 'DECISÃO PARCIAL DO MÉRITO', size=14, fill='var(--dif)', weight=700)
    o += t(1008, 225, 'ART. 356, CAPUT', size=10.5, anchor='end', fill='var(--ink-2)', weight=600)

    # The caput can cover whole requests or a portion. Other merits remain outside it.
    o += t(42, 319, 'UM OU MAIS PEDIDOS, OU PARCELA DELES', size=12, weight=700)
    o += line(42, 343, 1008, 343, tone='muted', w=1.3)
    o += line(42, 343, 570, 343, tone='dif', w=5)
    o += line(570, 330, 570, 357, tone='dif', w=2.4)
    o += line(570, 343, 1008, 343, tone='muted', w=2, dash='8 6')
    o += _arrow(1008, 343, tone='muted')
    o += t(42, 377, 'OBJETO DECIDIDO', size=11.5, fill='var(--dif)', weight=700)
    o += t(1008, 377, 'MÉRITO FORA DO OBJETO', size=11.5, anchor='end', fill='var(--ink-2)', weight=700)
    o += t(1008, 396, 'PERMANECE PENDENTE', size=11, anchor='end', fill='var(--ink-2)')
    return svg('24 25 1032 390', o, cls='fig', ident='pci-a11m-grounds',
               label='Artigo 356: o fundamento incontroverso e as condições de imediato julgamento convergem numa decisão parcial do mérito sobre objeto delimitado; o mérito fora dele permanece pendente')


def phase_panel():
    """An art. 356 merits chapter ends while the art. 203 cognitive phase continues."""
    o = ''
    o += t(42, 48, 'ARTS. 203 + 356  /  DUAS EXTENSÕES AO MESMO TEMPO', size=14, weight=700)
    o += line(42, 64, 1038, 64, w=1.25)

    # Art. 203 §1: sentence requires the end of the cognitive phase.
    o += t(42, 105, 'CRITÉRIO DA SENTENÇA · ART. 203, § 1º', size=11, fill='var(--ink-2)', weight=700)
    o += t(42, 125, 'fim da fase cognitiva', size=13, weight=600)
    o += line(42, 154, 1008, 154, tone='ink', w=2)
    o += _arrow(1008, 154)
    o += t(1008, 136, 'FASE COGNITIVA AINDA EM CURSO', size=11, anchor='end', fill='var(--ink-2)', weight=700)

    # At the same position in the proceeding, one object has been resolved.
    o += t(42, 226, 'PEDIDO OU PARCELA DECIDIDA', size=11.5, fill='var(--dif)', weight=700)
    o += line(42, 249, 570, 249, tone='dif', w=5)
    o += line(570, 231, 570, 267, tone='dif', w=3)
    o += t(601, 246, 'MÉRITO RESOLVIDO', size=13, fill='var(--dif)', weight=700)
    o += t(601, 267, 'decisão interlocutória · art. 203, § 2º', size=11, fill='var(--ink-2)')

    # The remaining object stays on an open course, so the phase cannot be over.
    o += t(42, 340, 'MÉRITO FORA DA DECISÃO', size=11.5, fill='var(--conc)', weight=700)
    o += line(42, 362, 1008, 362, tone='conc', w=3)
    o += _arrow(1008, 362, tone='conc')
    o += t(1008, 339, 'CONTINUA', size=11.5, anchor='end', fill='var(--conc)', weight=700)
    return svg('24 25 1032 362', o, cls='fig', ident='pci-a11m-phase',
               label='Artigos 203 e 356: uma parcela do mérito foi resolvida por decisão interlocutória enquanto o mérito restante e a fase cognitiva continuam')


def case_hero():
    """The existing Florinda petition as the hero's real procedural object."""
    o = ''
    o += t(38, 38, 'PETIÇÃO · FLORINDA', size=14, weight=700)
    o += line(38, 53, 562, 53, w=1.4)
    o += t(58, 90, 'PEDIDO 1', size=11, fill='var(--ink-2)', weight=700)
    o += t(58, 116, 'Nulidade do contrato de empréstimo', size=15, weight=600)
    o += t(542, 116, 'ADAMASTOR', size=11, anchor='end', weight=700)
    o += line(58, 134, 542, 134, w=1)
    o += t(58, 176, 'PEDIDO 2', size=11, fill='var(--ink-2)', weight=700)
    o += t(58, 202, 'Indenização · dano moral · R$ 5.000', size=15, weight=600)
    o += t(542, 202, 'VALQUÍRIA', size=11, anchor='end', weight=700)
    drawing = svg('22 15 556 216', o, cls='hero-form fig',
                  ident='pci-a11m-petition-hero',
                  label='Petição de Florinda: pedido de nulidade do contrato contra Adamastor e pedido de indenização por dano moral contra Valquíria.')
    drawing = drawing.replace('<svg', '<svg data-family="figure.form"', 1)
    return ('<figure class="hero-art a11m-case-hero" aria-label="Petição de Florinda, com dois pedidos">'
            '<div style="padding:14px;background:var(--paper);border:1.5px solid var(--ink);'
            'box-shadow:6px 6px 0 var(--grid-major)">'
            '<style>#pci-a11m-petition-hero{display:block;width:min(100%,780px);height:auto}</style>'
            + drawing + '</div><figcaption>Os dois pedidos da petição de Florinda têm réus distintos.</figcaption></figure>')


def opening_bet():
    return '''<div class="bet" id="a11m-opening-bet"><div><span class="bet-k">Antes de ler · Avaliação 2 · 2015/1 · questão 10</span><p class="bet-q">Na variação de Florinda, um pedido está pronto para julgamento e o outro ainda depende de prova. O juiz pode decidir o primeiro e prosseguir quanto ao segundo?</p><div class="bet-opts"><button type="button" data-opt="0" data-court aria-pressed="false">Sim. O primeiro pedido pode ser decidido agora, enquanto a instrução do outro continua.</button><button type="button" data-opt="1" aria-pressed="false">Não. Os dois pedidos precisam chegar juntos ao julgamento.</button></div><div class="bet-reveal"><p>Sim. O art. 356 permite decidir o pedido ou parcela que está pronta e manter em curso o mérito que ficou fora da decisão.</p></div></div></div>'''


def mobile_table_style():
    return ('@media(max-width:560px) and (orientation:portrait){'
            'table.compare{table-layout:fixed}'
            '.compare th,.compare td{padding:8px 6px}'
            '.compare thead th{font-size:13px}'
            '.compare tbody th{width:16%}'
            '.compare td{overflow-wrap:break-word}'
            '}')


def _replace_marked(source, start, end, content):
    pat = re.compile(re.escape(start) + r'.*?' + re.escape(end), re.S)
    if source.count(start) == 1 and source.count(end) == 1:
        return pat.sub(start + content + end, source, count=1)
    if source.count(start) or source.count(end):
        raise ValueError(f'partial or duplicate marker pair: {start}')
    return None


def recolor_case_figure(source):
    """Keep party labels/bars in ink and semantic accents limited to their meanings."""
    begin, end = '<!-- processo-thread-17:start -->', '<!-- processo-thread-17:end -->'
    if source.count(begin) != 1 or source.count(end) != 1:
        raise ValueError('expected the existing case figure marker pair exactly once')
    a = source.index(begin)
    b = source.index(end, a) + len(end)
    block = source[a:b]
    block = block.replace('stroke:var(--conc);stroke-width:1.8', 'stroke:var(--ink);stroke-width:1.8')
    block = block.replace('fill:var(--conc)"></text>', 'fill:var(--ink)"></text>')
    for frag in (
        'M48 478L72 478', 'M48 518L72 518',
    ):
        old = f'<path d="{frag}" style="fill:none;stroke:var(--dif);stroke-width:2.4"/>'
        new = f'<path d="{frag}" style="fill:none;stroke:var(--ink);stroke-width:2.4"/>'
        block = block.replace(old, new)
    block = block.replace('fill:var(--dif)">Pedidos de Florinda', 'fill:var(--ink)">Pedidos de Florinda')
    block = block.replace('fill:var(--dif)">Citação por hora certa', 'fill:var(--ink)">Citação por hora certa')
    source = source[:a] + block + source[b:]

    # The statutory reading form uses orange only for the limit mark, blue for the result.
    source = source.replace('.grounds input{accent-color:var(--conc);', '.grounds input{accent-color:var(--ink);')
    source = source.replace('border-left-color:var(--conc);background:color-mix(in srgb,var(--conc) 8%,var(--paper))', 'border-left-color:var(--ink)')
    return source


def build_release42():
    source = PAGE.read_text(encoding='utf-8')
    hero = _replace_marked(source, HERO_START, HERO_END, case_hero())
    if hero is None:
        anchor = '  <div class="art356-form"'
        if source.count(anchor) != 1:
            raise ValueError('existing art. 356 hero-form anchor is absent or duplicated')
        source = source.replace(anchor, HERO_START + case_hero() + HERO_END + '\n' + anchor, 1)
    else:
        source = hero
    bet = _replace_marked(source, BET_START, BET_END, opening_bet())
    if bet is None:
        anchor = '</header>\n\n<aside class="fonte"'
        if source.count(anchor) != 1:
            raise ValueError('hero close/source block anchor is absent or duplicated')
        source = source.replace(anchor, '</header>\n' + BET_START + opening_bet() + BET_END + '\n\n<aside class="fonte"', 1)
    else:
        source = bet
    source = recolor_case_figure(source)
    table_style = _replace_marked(source, TABLE_START, TABLE_END, mobile_table_style())
    if table_style is None:
        if '</style>' not in source:
            raise ValueError('page style block is absent')
        source = source.replace('</style>', TABLE_START + mobile_table_style() + TABLE_END + '</style>', 1)
    else:
        source = table_style
    PAGE.write_text(source, encoding='utf-8')
    print(f'updated release 4.2 hero, opening bet, and figure colours in {PAGE}')


def panels():
    return grounds_panel(), phase_panel()


def specimen_entry():
    a, b = panels()
    return ('<section class="ref" id="specimen-pci-a11m"><header><span class="g">'
            'Percursos · fundamento e fase</span><span class="v">verbo · delimitar</span></header>\n'
            '<h2>Processo · Aula 11-mérito · art. 356</h2>'
            '<p>Os dois fundamentos chegam à decisão sobre um objeto delimitado; '
            'a parcela decidida termina enquanto o restante mantém a fase cognitiva em curso.</p>'
            '<p class="r">novos componentes · pci-a11m-grounds / pci-a11m-phase</p>'
            f'<div class="wide"><div class="s">{a}</div><div class="s" '
            f'style="margin-top:18px">{b}</div></div></section>')


if __name__ == '__main__':
    if len(__import__('sys').argv) == 2 and __import__('sys').argv[1] == 'release42':
        build_release42()
    else:
        print('\n'.join(panels()))
