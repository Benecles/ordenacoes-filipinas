"""Aula 15: trace the record and compare a written assertion with an event.

Contract: inject(lesson_html: str) -> str. Pure, idempotent, Aula-15-only;
no disk writes or dependency on the all-pages injector. The docket is the
drawn hero; the documentary comparison is a single-panel scrolly stage.

Private sources: blueprint A4 #1 / Knijnik, PDF marker 7 (printed pp. 14–15);
A4 #10 / Moodle decision, autos 0321861-32.2015.8.24.0023, whole extract,
paragraph beginning “Ao ler a peça”, item 15 (f. 101). The initial petition's
content is not available: its search mark means a question, never absence.
"""
import re
from html import escape
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import processo_threads
from figkit import t, line, svg


def _paper(x, y, w, h, tone='ink'):
    """Folded sheet: a document surface, not a labelled box."""
    fold = 23
    return (f'<path d="M{x} {y}H{x+w-fold}L{x+w} {y+fold}V{y+h}H{x}Z" '
            f'style="fill:var(--paper);stroke:var(--{tone});stroke-width:1.6"/>'
            f'<path d="M{x+w-fold} {y}V{y+fold}H{x+w}" '
            f'style="fill:none;stroke:var(--{tone});stroke-width:1.2"/>')


def _manuscript(x, y, widths, tone='muted'):
    # Schematic prose texture; neither number of lines nor location is factual.
    return ''.join(line(x, y + i * 13, x + w, y + i * 13,
                        tone=tone, w=1.1) for i, w in enumerate(widths))


def assertion_panel():
    """The real judicial account is opened at the party's reported assertion."""
    o = t(28, 26, 'UM RELATO SOBRE O PASSADO', size=18, weight=700)
    o += _paper(28, 47, 544, 265)
    o += t(50, 78, 'A DECISÃO REGISTRA', size=16, fill='var(--ink-2)', weight=600, ls='.02em')
    o += _manuscript(50, 97, [465, 447, 459])
    o += t(50, 158, '“ao alegar que”', size=16, italic=True, ls='0')
    # The selected passage occupies the page's centre. A side brace marks its
    # scope; a closed quoted span remains visible with all text nodes removed.
    o += '<path d="M48 179H550V258H48Z" style="fill:var(--conc-wash);stroke:none"/>'
    o += line(48, 179, 48, 258, tone='conc', w=3)
    o += t(66, 207, 'inúmeras vezes tentou amigavelmente', size=20, ls='0', weight=600)
    o += t(66, 233, 'resolver o problema', size=20, ls='0', weight=600)
    o += '<path d="M38 177H18V260H38" style="fill:none;stroke:var(--conc);stroke-width:2"/>'
    o += _manuscript(50, 280, [447, 465])
    o += line(66, 331, 550, 331, tone='conc', w=2)
    o += line(66, 325, 66, 337, tone='conc', w=2)
    o += line(550, 325, 550, 337, tone='conc', w=2)
    o += t(308, 356, 'AFIRMAÇÃO · OBJETO DA PROVA', size=18, fill='var(--conc)', anchor='middle', weight=700)
    o += t(308, 381, 'O relato se refere ao acontecimento passado.', size=18, anchor='middle', ls='0')
    return svg('0 5 600 394', o, ident='pci-a15-assertion', cls='fig',
               label='Recorte esquemático da decisão: a oração sobre as tentativas amigáveis é destacada como afirmação do autor, objeto da prova; ela se refere a um acontecimento passado.')


def location_panel():
    """Compare the proposition shown in the judgment with the external event."""
    o = t(42, 48, 'O TEXTO DA PEÇA E O EVENTO NARRADO', size=23, weight=700)
    o += _paper(42, 68, 716, 216)
    o += t(72, 105, 'DECISÃO · IMPUGNAÇÃO · ITEM 15 · f. 101', size=17,
           fill='var(--ink-2)', weight=700, ls='.02em')
    o += t(72, 155, 'PERGUNTA SOBRE A LOCALIZAÇÃO NA INICIAL', size=22, weight=600, ls='0')
    o += t(72, 193, 'O juiz examina onde a alegação foi feita.', size=20, weight=500, ls='0')
    o += line(72, 220, 708, 220, tone='muted', w=1.2)
    o += t(42, 337, 'A IMPUGNAÇÃO CONTÉM A ALEGAÇÃO', size=19,
           fill='var(--dif)', weight=700, ls='.015em')
    o += line(42, 354, 42, 414, tone='dif', w=4)
    o += t(62, 380, 'Proposição textual identificada no registro.', size=19,
           fill='var(--ink)', weight=500, ls='0')
    o += t(62, 408, 'Decisão demonstrada', size=16, fill='var(--dif)', weight=700)
    o += t(42, 465, 'AS TENTATIVAS OCORRERAM', size=19,
           fill='var(--conc)', weight=700, ls='.015em')
    o += line(42, 482, 42, 542, tone='conc', w=4)
    o += t(62, 508, 'Proposição sobre acontecimento externo.', size=19,
           fill='var(--ink)', weight=500, ls='0')
    o += t(62, 536, 'Limite do registro', size=16, fill='var(--conc)', weight=700)
    o += t(710, 582, 'AZUL · DECISÃO     LARANJA · LIMITE', size=14,
           anchor='end', fill='var(--ink-2)', weight=700, ls='.04em')
    return svg('28 20 748 586', o, ident='pci-a15-location', cls='fig',
               label='Trecho da decisão pergunta onde a alegação foi feita na inicial. O registro identifica a proposição textual no item 15 da impugnação, folha 101; a ocorrência das tentativas é proposição distinta e não é decidida pelo texto da peça.')


def panels():
    return assertion_panel(), location_panel()


def _figure(ident, drawing, source):
    svg_markup = drawing.replace(' viewBox=', ' style="display:block;width:100%;height:auto" viewBox=', 1)
    if ident == 'a15-figure-assertion':
        svg_markup = '<!-- processo-thread-19:start -->' + svg_markup + '<!-- processo-thread-19:end -->'
        frame = ('<figure id="a15-figure-assertion" class="hero-fork hero-map">' + svg_markup
                 + '<figcaption>Registro de Florianópolis · passo da posição 19</figcaption></figure>')
        return (f'<!-- {ident}:start -->\n' + frame
                + f'<span class="src" hidden data-src="{escape(source, quote=True)}"></span>\n'
                + f'<!-- {ident}:end -->')
    frame = ('<figure id="a15-figure-location" class="document-figure">'
             + svg_markup
             + '<figcaption>O item 15 localiza a afirmação; a pergunta sobre a inicial fica no plano do texto.</figcaption>'
             '</figure>')
    return (f'<!-- {ident}:start -->\n' + frame
            + f'<span class="src" hidden data-src="{escape(source, quote=True)}"></span>\n'
            + f'<!-- {ident}:end -->')


def inject(lesson_html):
    """Return Aula 15 with the generated record and document figures.

    Placement: directly after the chapter section containing c05.
    Raises ValueError when the expected target sections are missing/ambiguous.
    The function has no file-system side effects; repeat calls are idempotent.
    """
    html = lesson_html
    targets = [
        ('c05', 'a15-figure-location', location_panel(),
         'Aula 19; decisão de Florianópolis, autos 0321861-32.2015.8.24.0023, item 15 (f. 101).'),
    ]
    for chapter, ident, drawing, source in targets:
        block = _figure(ident, drawing, source)
        old = re.compile(r'<!-- ' + ident + r':start -->.*?<!-- ' + ident + r':end -->', re.S)
        if old.search(html):
            html = old.sub(lambda _: block, html)
            continue
        if ident == 'a15-figure-assertion':
            anchor = re.compile(r'<header\b[^>]*class=["\']hero["\'][^>]*>.*?</header>', re.S)
        else:
            anchor = re.compile(r'<section\b[^>]*>(?:(?!</section>).)*<h2\b[^>]*\bid=["\']'
                                + chapter + r'["\'][^>]*>.*?</section>', re.S)
        matches = list(anchor.finditer(html))
        if len(matches) != 1:
            raise ValueError(f'Aula 15: expected one chapter {chapter}; found {len(matches)}')
        if ident == 'a15-figure-assertion':
            end = matches[0].end() - len('</header>')
            html = html[:end] + '\n' + block + html[end:]
        else:
            end = matches[0].end()
            html = html[:end] + '\n' + block + html[end:]
    rendered = processo_threads.inject_single_page(
        19, Path(__file__).resolve().parents[2] / 'courses' / 'processo-civil-i' / 'aula-15.html', html)
    # Tag the shared real-record figure for the 4.2 structure checker, and keep its
    # title clear of the cropped top edge. These page-local changes leave other
    # study-position renderers untouched.
    thread = re.compile(r'(<svg\b(?=[^>]*\bid="pci-thread-florianopolis-19")[^>]*)(>)')
    rendered, tagged = thread.subn(r'\1 data-family="figure.autos"\2', rendered, count=1)
    if tagged != 1:
        raise ValueError('Aula 15: expected the generated Florianópolis record figure')
    rendered, source_note = re.subn(
        r'A compra é datada apenas por mês; a pergunta judicial não prova que as tentativas ocorreram ou deixaram de ocorrer\.',
        'No item 15, o autor relata tentativas de solução; o juiz pergunta onde essa alegação aparece na inicial.',
        rendered, count=1)
    if source_note != 1:
        raise ValueError('Aula 15: expected the shared thread note to replace with its local reading')
    for old, new in (
        ('O registro informa apenas o mês da compra.', 'A compra ocorreu em novembro de 2012.'),
        ('Usar o mesmo arquivo para uma comparação atual; a hipótese não altera o resultado histórico de 2016.',
         'Hipótese de comparação pelo CPC atual, formulada sobre a decisão de 2016.'),
        ('A inicial e a impugnação localizam a alegação; o excerto não identifica meio de prova proposto.',
         'O item 15 localiza a alegação na impugnação; o juiz pergunta pela inicial.'),
    ):
        if old not in rendered:
            raise ValueError(f'Aula 15: expected shared thread detail {old!r}')
        rendered = rendered.replace(old, new, 1)
    title = re.compile(r'(<svg\b(?=[^>]*\bid="pci-thread-florianopolis-19")[^>]*>.*?<text x="42" y=")42(")', re.S)
    rendered, changed = title.subn(r'\g<1>47\2', rendered, count=1)
    if changed != 1:
        raise ValueError('Aula 15: expected the generated Florianópolis timeline title')
    return rendered


def specimen_section():
    cells = ''.join('<div class="s">' + p + '</div>' for p in panels())
    return ('<!-- processo-a15-specimen:start --><section class="ref" id="processo-a15-specimen">'
            '<header><span class="g">Autos · tempo medido / Documento · alcance</span>'
            '<span class="v">verbos · traçar / comparar</span></header>'
            '<h2>Processo · Aula 15 · objeto da prova</h2>'
            '<p>O registro compartilhado acrescenta a pergunta sobre a alegação. O recorte da decisão '
            'separa o conteúdo da peça da ocorrência externa narrada.</p>'
            '<p class="r">primeira ocorrência · pci-thread-florianopolis-19 / pci-a15-location</p>'
            '<div class="grid">' + cells + '</div></section><!-- processo-a15-specimen:end -->')


if __name__ == '__main__':
    print(specimen_section())
