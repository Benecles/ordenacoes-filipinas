"""Aula 12 release 4.2 opening bet and figure.form hero.

Bet claim source: Aula 12 compendium, CPC art. 129 and its sole paragraph,
captured in 30-supporting-005-cpc-lei-13105-capture-2026-09-28-Art.-129.txt.
Hero claim source: Aula 12 blueprint A4 claims 1-2 and A7 Fig. 1; CPC art. 125,
II, plus Didier, cap. 13, §§ 3.5.5-3.7 (printed pp. 570-572).
Run: python3 tools/figkit/processo_a12_release42.py
"""
from pathlib import Path

import figkit

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / 'courses' / 'processo-civil-i' / 'aula-12.html'
HERO_START, HERO_END = '<!-- A12_42_HERO_START -->', '<!-- A12_42_HERO_END -->'
BET_START, BET_END = '<!-- A12_42_BET_START -->', '<!-- A12_42_BET_END -->'
STYLE_START, STYLE_END = '/* A12_42_START */', '/* A12_42_END */'


def hero():
    o = figkit.t(34, 34, 'CÓDIGO DE PROCESSO CIVIL · DENUNCIAÇÃO DA LIDE', size=12,
                 fill='var(--ink-2)', weight=700)
    o += figkit.line(34, 47, 566, 47, tone='ink', w=1.4)
    o += '<rect x="42" y="64" width="516" height="119" rx="2" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    o += figkit.line(300, 64, 300, 183, tone='muted', w=1)
    o += figkit.t(60, 101, 'DEMANDA PRINCIPAL', size=10, fill='var(--ink-2)', weight=700)
    o += figkit.t(60, 132, 'Autor e réu', size=17, fill='var(--ink)', weight=700)
    o += figkit.t(60, 159, 'pedido principal', size=12, fill='var(--ink-2)')
    o += figkit.t(320, 101, 'DENUNCIAÇÃO', size=10, fill='var(--conc)', weight=700)
    o += figkit.t(320, 132, 'Denunciante e denunciado', size=12, fill='var(--conc)', weight=700)
    o += figkit.t(320, 159, 'pedido regressivo', size=12, fill='var(--ink-2)')
    o += figkit.line(42, 201, 558, 201, tone='muted', w=1)
    o += figkit.t(300, 231, 'DOIS PEDIDOS · UM PROCESSO', size=12, anchor='middle',
                  fill='var(--ink)', weight=700)
    return figkit.svg('18 16 564 248', o, cls='hero-form fig',
                      ident='pci-a12-claims-hero',
                      label='Duas relações e dois pedidos no mesmo processo: pedido principal entre autor e réu; pedido regressivo entre denunciante e denunciado').replace(
                          '<svg', '<svg data-family="figure.form"', 1)


def bet():
    return '''<div class="bet" id="a12-opening-bet"><div><span class="bet-k">Antes de ler · CPC, art. 129</span><p class="bet-q">Se o denunciante vencer a demanda principal, o juiz examina o pedido da denunciação?</p><div class="bet-opts"><button type="button" data-opt="0" aria-pressed="false">Sim. O pedido regressivo é julgado mesmo quando o denunciante vence a demanda principal.</button><button type="button" data-opt="1" data-court aria-pressed="false">Não. O pedido da denunciação não será examinado, sem prejuízo das verbas de sucumbência em favor do denunciado.</button></div><div class="bet-reveal"><p>Não. O parágrafo único do art. 129 determina que, se o denunciante vencer, o pedido da denunciação não será examinado; permanecem as verbas de sucumbência em favor do denunciado.</p></div><span class="src" hidden data-src="CPC, art. 129, parágrafo único; compendium/aula-12/30-supporting-005-cpc-lei-13105-capture-2026-09-28-Art.-129.txt."></span></div></div>'''


def _replace(source, start, end, content):
    if source.count(start) == 1 and source.count(end) == 1:
        a = source.index(start)
        b = source.index(end, a) + len(end)
        return source[:a] + start + content + end + source[b:]
    if source.count(start) or source.count(end):
        raise ValueError(f'partial or duplicate marker pair: {start}')
    return None


def build():
    figkit.WARN.clear()
    source = PAGE.read_text(encoding='utf-8')
    rendered_hero = '<figure class="hero-art">' + hero() + '<figcaption>A denunciação reúne no processo duas pretensões com sujeitos e pedidos próprios.</figcaption></figure>'
    replaced = _replace(source, HERO_START, HERO_END, rendered_hero)
    if replaced is None:
        anchor = ' <div class="titleblock label"'
        if source.count(anchor) != 1:
            raise ValueError('hero titleblock anchor is absent or duplicated')
        source = source.replace(anchor, '\n' + HERO_START + rendered_hero + HERO_END + '\n' + anchor, 1)
    else:
        source = replaced

    rendered_bet = bet()
    replaced = _replace(source, BET_START, BET_END, rendered_bet)
    if replaced is None:
        anchor = '</div>\n</header>\n\n<section class="chapter"'
        if source.count(anchor) != 1:
            raise ValueError('hero close anchor is absent or duplicated')
        source = source.replace(anchor, '</div>\n</header>' + BET_START + rendered_bet + BET_END + '\n\n<section class="chapter"', 1)
    else:
        source = replaced

    styles = ('.hero-art{max-width:900px;margin:24px 0 0}.hero-art svg{display:block;width:min(100%,620px);height:auto}'
              '.hero-art figcaption{font:500 11px/1.5 var(--mono);color:var(--ink-2);margin:8px 0 0}')
    replaced = _replace(source, STYLE_START, STYLE_END, styles)
    if replaced is None:
        if source.count('</style>') != 1:
            raise ValueError('inline style anchor is absent or duplicated')
        source = source.replace('</style>', STYLE_START + styles + STYLE_END + '</style>', 1)
    else:
        source = replaced
    PAGE.write_text(source, encoding='utf-8')
    print(f'updated {PAGE}')
    print('\n'.join(figkit.WARN) or 'no text warnings')


if __name__ == '__main__':
    build()
