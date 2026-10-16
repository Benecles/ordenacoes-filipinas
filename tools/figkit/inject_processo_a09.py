"""Install Aula 09's page-specific instruments without touching other lessons."""

from pathlib import Path
import re

from processo_a09 import case_record_panels, objection_folio, stj_record


ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / 'courses/processo-civil-i/aula-09.html'

SCROLL_START, SCROLL_END = '<!-- A09_SCROLLY_START -->', '<!-- A09_SCROLLY_END -->'
FOLIO_START, FOLIO_END = '<!-- A09_FOLIO_START -->', '<!-- A09_FOLIO_END -->'
STJ_START, STJ_END = '<!-- A09_STJ_START -->', '<!-- A09_STJ_END -->'
STYLE_START, STYLE_END = '/* A09_STYLE_START */', '/* A09_STYLE_END */'


def _replace_marked(source, start, end, content):
    pattern = re.compile(re.escape(start) + r'.*?' + re.escape(end), re.S)
    if source.count(start) == 1 and source.count(end) == 1:
        return pattern.sub(start + content + end, source, count=1)
    if source.count(start) or source.count(end):
        raise ValueError(f'partial or duplicate marker pair: {start}')
    return None


def _scrolly():
    panels = case_record_panels()
    ids = ('pci-a09-record-initial', 'pci-a09-record-delivery', 'pci-a09-record-dates')
    stages = (
        ('Primeira diligência',
         'O oficial não encontra Florinda e marca hora certa para o dia seguinte.',
         'primeira diligência'),
        ('Dia seguinte · mandado entregue à vizinha',
         'Valquíria recebe o mandado e espalha a notícia narrada no enunciado.',
         'dia seguinte · entrega'),
        ('V1 e V2 · comparecimento na data da juntada',
         'A advogada comparece na data da juntada: 5 de setembro na V1 e 6 na V2.',
         'V1 5 set. · V2 6 set.'),
    )
    figure = (
        '<div class="stage"><figure data-staged="true">' + ''.join(panels)
        + '<figcaption><span class="stage-count">primeira diligência</span><span class="stage-step">1 / 3</span></figcaption></figure></div>'
    )
    steps = []
    for i, (panel, (title, prose, slide)) in enumerate(zip(ids, stages)):
        source = '<span class="src">Processo Civil I · P1 2018/2 · questão 4</span>' if i == 0 else ''
        steps.append(
            f'<div class="step{" on" if i == 0 else ""}" data-panel="{panel}" data-slides="{slide}"><div class="card">'
            + source + f'<h3>{title}</h3><p>{prose}</p></div></div>'
        )
    return '<div class="scrolly a09-scrolly">' + figure + '<div class="steps">' + ''.join(steps) + '</div></div>'


def _folio():
    fig = objection_folio()
    return ('<figure class="figure-sheet" aria-labelledby="pci-a09-objection-cap">' + fig
            + '<figcaption id="pci-a09-objection-cap">Fig. 2 · A folha do art. 278 separa a primeira oportunidade e as exceções do parágrafo único.</figcaption></figure>')


def _stj():
    fig = stj_record()
    return ('<figure class="figure-sheet" aria-labelledby="pci-a09-stj-cap">' + fig
            + '<figcaption id="pci-a09-stj-cap">Fig. 3 · O alcance da ordem da origem e a resposta do STJ permanecem em linhas distintas.</figcaption></figure>')


def _style():
    return '.hero .a09-scrolly{max-width:100%;margin:30px 0 0;padding:0}.a09-scrolly .stage figure{aspect-ratio:564/390}.a09-scrolly .stage figure svg{display:block;width:100%;height:100%}.a09-scrolly .panel{object-fit:contain}.a09-record-note{font:500 11px/1.5 var(--mono);color:var(--ink-2)}'


def inject(source):
    for start, end, content in (
        (SCROLL_START, SCROLL_END, _scrolly()),
        (FOLIO_START, FOLIO_END, _folio()),
        (STJ_START, STJ_END, _stj()),
    ):
        updated = _replace_marked(source, start, end, content)
        if updated is not None:
            source = updated
        else:
            raise ValueError(f'missing page-specific marker pair: {start}')

    updated = _replace_marked(source, STYLE_START, STYLE_END, _style())
    if updated is None:
        anchor = '@media (max-width:560px) and (orientation:portrait)'
        if source.count(anchor) != 1:
            raise ValueError('Aula 09 responsive style insertion anchor is absent or duplicated')
        source = source.replace(anchor, STYLE_START + _style() + STYLE_END + anchor, 1)
    else:
        source = updated
    return source


if __name__ == '__main__':
    before = PAGE.read_text(encoding='utf-8')
    after = inject(before)
    PAGE.write_text(after, encoding='utf-8')
    print(f'{PAGE}: Aula 09 record, folio, and STJ docket installed')
