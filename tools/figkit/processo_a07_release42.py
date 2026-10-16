"""Install Aula 07's release 4.2 hero and opening bet from its live record."""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figkit import line, svg, t

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "courses/processo-civil-i/aula-07.html"
HERO_START, HERO_END = "<!-- A07_42_HERO_START -->", "<!-- A07_42_HERO_END -->"
BET_START, BET_END = "<!-- A07_42_BET_START -->", "<!-- A07_42_BET_END -->"
STYLE_START, STYLE_END = "/* A07_42_START */", "/* A07_42_END */"


def _replace_marked(source, start, end, content):
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if source.count(start) == 1 and source.count(end) == 1:
        return pattern.sub(start + content + end, source, count=1)
    if source.count(start) or source.count(end):
        raise ValueError(f"partial or duplicate marker pair: {start}")
    return None


def _hero():
    o = t(28, 32, "NOTA Nº 1690/2015 · EDIÇÃO 5561", size=14, weight=700)
    o += line(28, 48, 572, 48, tone="ink", w=1.4)
    o += t(28, 83, "DISPONIBILIZAÇÃO", size=11, fill="var(--ink-2)", weight=700)
    o += t(572, 83, "21/05/2015", size=17, anchor="end", fill="var(--conc)", weight=700)
    o += line(28, 96, 572, 96, tone="ink", w=1)
    o += t(28, 128, "PUBLICAÇÃO · PRIMEIRO DIA ÚTIL SEGUINTE", size=11, fill="var(--ink-2)", weight=700)
    o += t(572, 155, "22/05/2015", size=17, anchor="end", weight=700)
    o += line(28, 168, 572, 168, tone="ink", w=1)
    o += t(28, 200, "1º DIA CONTADO", size=11, fill="var(--ink-2)", weight=700)
    o += t(572, 227, "25/05/2015", size=17, anchor="end", fill="var(--dif)", weight=700)
    drawing = svg("0 0 600 250", o,
                  cls="hero-form fig",
                  label="Nota 1690/2015: disponibilização em 21 de maio, publicação no primeiro dia útil seguinte em 22 de maio e primeiro dia contado em 25 de maio.",
                  ident="pci-a07-deadline-hero").replace("<svg", '<svg data-family="figure.form"', 1)
    return ('<figure class="hero-art">' + drawing
            + '<figcaption>A mesma certidão, agora com o primeiro dia da contagem localizado.</figcaption></figure>')


def _bet():
    return '''<div class="bet" id="a07-opening-bet"><div><span class="bet-k">Antes de ler · 2025/2 P1 · Sérgio Mattos</span><p class="bet-q">Com os embargos de declaração opostos em 10/09/2025, quando vence o prazo da apelação?</p><div class="bet-opts"><button type="button" data-opt="0" data-court aria-pressed="false">Em 06/10/2025: os embargos tempestivos interrompem o prazo, que recomeça integralmente após a nova intimação.</button><button type="button" data-opt="1" aria-pressed="false">Em 22/09/2025: os embargos apenas suspendem o prazo, que retoma o saldo restante.</button></div><div class="bet-reveal"><p>Em 06/10/2025. Os embargos foram apresentados dentro do prazo e interromperam o prazo recursal; após a nova intimação, correu o período integral de quinze dias úteis.</p></div></div></div>'''


def _style():
    return ('.hero-art{max-width:900px;margin:26px 0 0}.hero-art svg{display:block;width:min(100%,780px);height:auto}'
            '.hero-art figcaption{font:500 11px/1.5 var(--mono);color:var(--ink-2);margin:8px 0 0}')


def build():
    source = PAGE.read_text()
    current = re.search(re.escape(HERO_START) + r"(.*?)" + re.escape(HERO_END), source, re.S)
    if current:
        source = source[:current.start()] + HERO_START + _hero() + HERO_END + source[current.end():]
    else:
        anchor = '<div class="titleblock label"'
        if source.count(anchor) != 1:
            raise ValueError("hero titleblock anchor is absent or duplicated")
        source = source.replace(anchor, HERO_START + _hero() + HERO_END + anchor, 1)

    bet = _replace_marked(source, BET_START, BET_END, _bet())
    if bet is not None:
        source = bet
    elif 'id="a07-opening-bet"' not in source:
        anchor = "</header>\n<!-- CPC_HOME_QUOTE_PENDING: art. 229 -->"
        if source.count(anchor) != 1:
            raise ValueError("hero close anchor is absent or duplicated")
        source = source.replace(anchor, "</header>" + BET_START + _bet() + BET_END + "\n<!-- CPC_HOME_QUOTE_PENDING: art. 229 -->", 1)
    else:
        raise ValueError("opening bet exists without its marker pair")

    style = _replace_marked(source, STYLE_START, STYLE_END, _style())
    if style is not None:
        source = style
    else:
        anchor = "</style>"
        # The page has one compact inline style block; append the hero rules before it closes.
        if source.count(anchor) != 1:
            raise ValueError("inline style anchor is absent or duplicated")
        source = source.replace(anchor, STYLE_START + _style() + STYLE_END + anchor, 1)
    PAGE.write_text(source)
    print(f"updated {PAGE}")


if __name__ == "__main__":
    build()
