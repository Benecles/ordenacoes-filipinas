"""Aula 15: select an assertion; locate it in the written record.

Contract: inject(lesson_html: str) -> str. Pure, idempotent, Aula-15-only;
no disk writes or dependency on the all-pages injector. The two panels follow
chapters c01 and c05. Document outlines are schematic, never facsimiles.

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
    """Read two document surfaces; do not infer the event from the assertion."""
    o = t(28, 26, 'ONDE A AFIRMAÇÃO FOI FEITA?', size=18, weight=700)
    for x, title in [(28, 'INICIAL'), (328, 'IMPUGNAÇÃO')]:
        o += _paper(x, 49, 244, 241)
        o += t(x+20, 81, title, size=18, weight=700)
        o += _manuscript(x+20, 103, [185, 191, 174, 185])
        o += _manuscript(x+20, 248, [184, 171])
    # A search lens is deliberately open/questioned. It must not read as an
    # absent assertion: the decision asks where, and supplies no initial text.
    o += '<circle cx="140" cy="193" r="35" style="fill:var(--paper-2);stroke:var(--ink-2);stroke-width:2;stroke-dasharray:4 4"/>'
    o += line(164, 220, 191, 244, tone='muted', w=5)
    o += t(140, 207, '?', size=34, anchor='middle', weight=600)
    # Actual locator, not an invented page layout: a highlighted assertion at
    # the specified item, with its known sheet number in a separate gutter.
    o += '<path d="M348 160H552V228H348Z" style="fill:var(--conc-wash);stroke:none"/>'
    o += line(348, 160, 348, 228, tone='conc', w=3)
    o += t(364, 183, 'ITEM 15', size=18, weight=700, fill='var(--conc)')
    o += t(364, 206, 'tentativas amigáveis', size=16, ls='0')
    o += t(550, 281, 'f. 101', size=16, anchor='end', weight=600)
    o += t(150, 316, 'LOCALIZAÇÃO QUESTIONADA', size=16, anchor='middle', ls='.02em', fill='var(--ink-2)')
    o += t(450, 316, 'ALEGAÇÃO REGISTRADA', size=16, anchor='middle', ls='.02em', fill='var(--conc)', weight=700)
    # The documentary inspection covers the sheets, and ends at their edge.
    # It does not bridge the gutter to the unresolved occurrence below.
    o += '<path d="M28 330V342H572V330" style="fill:none;stroke:var(--conc);stroke-width:1.8"/>'
    o += t(300, 367, 'PEÇAS · SE E ONDE FOI ALEGADO', size=18, fill='var(--conc)', anchor='middle', weight=700)
    o += line(28, 390, 572, 390, tone='muted', w=1, dash='3 5')
    o += t(28, 418, 'AS TENTATIVAS OCORRERAM?', size=18, weight=700)
    o += t(28, 442, 'Meio de prova não indicado no excerto.', size=18, fill='var(--ink-2)', ls='0')
    o += '<circle cx="548" cy="425" r="23" style="fill:none;stroke:var(--ink-2);stroke-width:2;stroke-dasharray:4 4"/>'
    o += t(548, 433, '?', size=23, anchor='middle', fill='var(--ink-2)', weight=600)
    return svg('8 5 584 458', o, ident='pci-a15-location', cls='fig',
               label='Duas peças esquemáticas: a localização na inicial é questionada; a decisão registra a alegação na impugnação, item 15, folha 101. Consultar as peças localiza a alegação; o excerto não identifica meio para provar a ocorrência das tentativas.')


def panels():
    return assertion_panel(), location_panel()


def _figure(ident, drawing, source):
    return (f'<!-- {ident}:start -->\n<div class="wide"><figure id="{ident}" '
            'style="max-width:760px;margin:22px 0 32px">'
             + (('<!-- processo-thread-19:start -->' + drawing.replace(' viewBox=', ' style="display:block;width:100%;height:auto" viewBox=', 1) + '<!-- processo-thread-19:end -->') if ident == 'a15-figure-assertion' else drawing.replace(' viewBox=', ' style="display:block;width:100%;height:auto" viewBox=', 1))
            + (f'<figcaption>Fig. 1 · A decisão localiza a afirmação nas peças e pergunta onde ela foi alegada.</figcaption>' if ident == 'a15-figure-assertion' else '')
            + f'</figure><span class="src" hidden data-src="{escape(source, quote=True)}"></span></div>\n'
            + f'<!-- {ident}:end -->')


def inject(lesson_html):
    """Return Aula 15 with exactly these two panels; preserve all other bytes.

    Placement: directly after the chapter sections containing c01 and c05.
    Raises ValueError when the expected target sections are missing/ambiguous.
    The function has no file-system side effects; repeat calls are idempotent.
    """
    html = lesson_html
    targets = [
        ('c01', 'a15-figure-assertion', assertion_panel(),
         'Blueprint A4 #1; Knijnik, cap. I, PDF 7, pp. 14–15; decisão Moodle, autos 0321861-32.2015.8.24.0023, trecho “Ao ler a peça”.'),
        ('c05', 'a15-figure-location', location_panel(),
         'Blueprint A4 #10; decisão Moodle, autos 0321861-32.2015.8.24.0023, item 15 (f. 101), excerto integral; CPC arts. 369–370.'),
    ]
    for chapter, ident, drawing, source in targets:
        block = _figure(ident, drawing, source)
        old = re.compile(r'<!-- ' + ident + r':start -->.*?<!-- ' + ident + r':end -->', re.S)
        if old.search(html):
            html = old.sub(lambda _: block, html)
            continue
        anchor = re.compile(r'<section\b[^>]*>(?:(?!</section>).)*<h2\b[^>]*\bid=["\']'
                            + chapter + r'["\'][^>]*>.*?</section>', re.S)
        matches = list(anchor.finditer(html))
        if len(matches) != 1:
            raise ValueError(f'Aula 15: expected one chapter {chapter}; found {len(matches)}')
        end = matches[0].end()
        html = html[:end] + '\n' + block + html[end:]
    return processo_threads.inject_single_page(19, Path(__file__).resolve().parents[2] / 'courses' / 'processo-civil-i' / 'aula-15.html', html)


def specimen_section():
    cells = ''.join('<div class="s">' + p + '</div>' for p in panels())
    return ('<!-- processo-a15-specimen:start --><section class="ref" id="processo-a15-specimen">'
            '<header><span class="g">Documento · recorte e localização</span>'
            '<span class="v">verbos · delimitar / localizar</span></header>'
            '<h2>Processo · Aula 15 · objeto da prova</h2>'
            '<p>O recorte delimita a afirmação relatada na decisão. A comparação das peças distingue '
            'a localização conhecida da pergunta sobre a inicial e da ocorrência das tentativas.</p>'
            '<p class="r">primeira ocorrência · pci-a15-assertion / pci-a15-location · documentos esquemáticos</p>'
            '<div class="grid">' + cells + '</div></section><!-- processo-a15-specimen:end -->')


if __name__ == '__main__':
    print(specimen_section())
