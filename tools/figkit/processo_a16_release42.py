"""Install Aula 20's source-backed opening bet and reserved decision-form hero."""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figkit import line, svg, t

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "courses/processo-civil-i/aula-16.html"
HERO_START, HERO_END = "<!-- A16_42_HERO_START -->", "<!-- A16_42_HERO_END -->"
BET_START, BET_END = "<!-- A16_42_BET_START -->", "<!-- A16_42_BET_END -->"
STYLE_START, STYLE_END = "/* A16_42_START */", "/* A16_42_END */"


def _replace_marked(source, start, end, content):
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if source.count(start) == 1 and source.count(end) == 1:
        return pattern.sub(start + content + end, source, count=1)
    if source.count(start) or source.count(end):
        raise ValueError(f"partial or duplicate marker pair: {start}")
    return None


def hero():
    """A decision sheet connecting its two located dates to its recorded result."""
    o = '<rect x="9" y="9" width="762" height="220" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
    o += t(28, 35, 'DECISÃO · 15 JAN. 2016', size=12, weight=700)
    o += line(28, 47, 752, 47, tone='ink', w=1.2)

    o += t(30, 70, 'COMPRA DO APARELHO', size=10.5, fill='var(--ink-2)', weight=700)
    o += t(30, 94, 'contestação', size=12, weight=600)
    o += t(355, 94, 'NOV. 2012', size=13, anchor='end', fill='var(--ink)', weight=700)
    o += line(30, 105, 355, 105, tone='ink', w=1.2)

    o += t(425, 70, 'AJUIZAMENTO', size=10.5, fill='var(--ink-2)', weight=700)
    o += t(425, 94, 'última página da inicial', size=12, weight=600)
    o += t(750, 94, '18 AGO. 2015', size=13, anchor='end', fill='var(--ink)', weight=700)
    o += line(425, 105, 750, 105, tone='ink', w=1.2)

    o += line(192, 119, 192, 139, tone='dif', w=2)
    o += line(588, 119, 588, 139, tone='dif', w=2)
    o += line(192, 139, 588, 139, tone='dif', w=2)
    o += line(390, 139, 390, 156, tone='dif', w=2)
    o += '<rect x="218" y="156" width="344" height="46" style="fill:var(--dif-wash);stroke:var(--dif);stroke-width:1.5"/>'
    o += t(390, 184, 'DECADÊNCIA RECONHECIDA', size=13, anchor='middle', fill='var(--dif)', weight=700)
    drawing = svg('0 0 780 238', o, cls='hero-form', ident='pci-a16-decision-hero',
                  label='Folha de decisão de 15 de janeiro de 2016: a compra, localizada na contestação em novembro de 2012, e o ajuizamento, localizado na última página da inicial em 18 de agosto de 2015, conduzem ao reconhecimento da decadência.')
    return drawing.replace('<svg', '<svg data-family="figure.form"', 1)


def _hero_block():
    return ('<figure class="a16-hero-art" id="a16-release42-hero">' + hero()
            + '<figcaption>A decisão conecta dois marcos localizados nas peças ao resultado que enuncia.</figcaption></figure>')


def bet():
    return '''<div class="bet" id="a16-opening-bet"><div>
  <span class="bet-k">Antes de ler · decida pelo registro</span>
  <p class="bet-q">Que comparação a decisão de Florianópolis registra antes de reconhecer a decadência?</p>
  <div class="bet-opts">
    <button type="button" data-opt="0" aria-pressed="false">A alegação de tentativas amigáveis do item 15 e uma resposta da loja.</button>
    <button type="button" data-opt="1" data-court aria-pressed="false">A compra em novembro de 2012, localizada na contestação, e o ajuizamento em 18 de agosto de 2015, localizado na inicial.</button>
    <button type="button" data-opt="2" aria-pressed="false">O desinteresse do autor na manutenção do produto, mencionado no item 16, e a data da compra.</button>
  </div>
  <div class="bet-reveal"><p>A decisão localiza a compra em novembro de 2012 na contestação e o ajuizamento em 18 de agosto de 2015 na última página da inicial. Em seguida, reconhece a decadência. O item 15 registra outra pergunta: onde estavam a prova das tentativas amigáveis e sua alegação na inicial?</p></div>
</div></div>'''


def _style():
    return ('.a16-hero-art{max-width:900px;margin:22px auto 24px;padding:0 clamp(16px,4vw,48px)}'
            '.a16-hero-art svg{display:block;width:min(100%,780px);height:auto}'
            '.a16-hero-art figcaption{max-width:780px;margin:8px 0 0;font:500 11px/1.5 var(--mono);color:var(--ink-2)}')


def build():
    source = PAGE.read_text(encoding='utf-8')

    hero_marked = _replace_marked(source, HERO_START, HERO_END, _hero_block())
    if hero_marked is not None:
        source = hero_marked
    elif 'id="a16-release42-hero"' not in source:
        anchor = '<div class="titleblock label"'
        if source.count(anchor) != 1:
            raise ValueError('hero titleblock anchor is absent or duplicated')
        source = source.replace(anchor, HERO_START + _hero_block() + HERO_END + anchor, 1)
    else:
        raise ValueError('hero drawing exists without its marker pair')

    bet_marked = _replace_marked(source, BET_START, BET_END, bet())
    if bet_marked is not None:
        source = bet_marked
    elif 'id="a16-opening-bet"' not in source:
        matches = list(re.finditer(r'<aside class="bet"[^>]*>.*?</aside>', source, re.S))
        if len(matches) != 1:
            raise ValueError(f'expected one existing opening bet, found {len(matches)}')
        m = matches[0]
        source = source[:m.start()] + BET_START + bet() + BET_END + source[m.end():]
    else:
        raise ValueError('opening bet exists without its marker pair')

    # Keep the complete choice before the first chapter heading; the decision
    # is the opening act, not an exercise inside the explanatory section.
    bet_pattern = re.compile(re.escape(BET_START) + r".*?" + re.escape(BET_END), re.S)
    bet_match = bet_pattern.search(source)
    chapter_match = re.search(r'<section\b[^>]*class=["\'][^"\']*\bchapter', source, re.I)
    if not bet_match or not chapter_match:
        raise ValueError('opening bet or first chapter anchor is absent')
    bet_block = bet_match.group(0)
    source = source[:bet_match.start()] + source[bet_match.end():]
    source = source.replace('\n  \n  <p>A decisão, nos autos', '\n  <p>A decisão, nos autos', 1)
    chapter_match = re.search(r'<section\b[^>]*class=["\'][^"\']*\bchapter', source, re.I)
    source = source[:chapter_match.start()] + bet_block + '\n\n' + source[chapter_match.start():]

    style_marked = _replace_marked(source, STYLE_START, STYLE_END, _style())
    if style_marked is not None:
        source = style_marked
    else:
        if source.count('</style>') != 1:
            raise ValueError('expected one inline style block')
        source = source.replace('</style>', STYLE_START + _style() + STYLE_END + '</style>', 1)

    PAGE.write_text(source, encoding='utf-8')
    print(f'updated {PAGE}')


if __name__ == '__main__':
    build()
