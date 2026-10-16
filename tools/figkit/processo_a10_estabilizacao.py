"""Aula 10: pair each factual issue with evidence and burden; mark § 1's window.

Sources: the Aula 10 compendium's CPC art. 357, II–III and § 1, and art. 373.
The first panel is a reusable relation, with no case facts filled in. The second
shows order and duration only: there is no implied calendar date or appeal route.
"""
from pathlib import Path
import re

from figkit import line, svg, t


def hero():
    """The procedural fork that frames this lesson, drawn with the figure kit."""
    o = ''
    o += line(52, 78, 1028, 78, tone='muted', w=2)
    o += line(52, 78, 784, 78, tone='ink', w=2.5)
    for x, title, note, anchor in (
        (52, 'RESPOSTA', 'providências', 'start'),
        (375, 'ART. 353', 'estado do processo', 'middle'),
        (704, 'ART. 357', 'organização da instrução', 'middle'),
        (1028, 'INSTRUÇÃO', 'provas organizadas', 'end'),
    ):
        o += f'<circle cx="{x}" cy="78" r="6" style="fill:var(--paper);stroke:var(--ink);stroke-width:2"/>'
        o += t(x, 39 if x in (52, 704) else 119, title, size=12, weight=700, anchor=anchor)
        o += t(x, 56 if x in (52, 704) else 137, note, size=11, fill='var(--ink-2)', anchor=anchor)
    return svg('0 0 1080 170', o, cls='hero-fork',
               label='Percurso do pós-resposta à organização da instrução pelos arts. 353 e 357').replace(
                   'class="hero-fork figkit"', 'class="hero-fork figkit" data-family="figure.autos"')


def issue_links_panel():
    """An issue's two attached determinations, drawn as one branching relation."""
    o = ''
    o += t(38, 51, 'ART. 357 · II–III', size=13, weight=700, fill='var(--ink-2)')
    o += t(962, 51, 'PARA CADA QUESTÃO', size=12, weight=700,
           fill='var(--ink-2)', anchor='end')

    # One fork per factual issue: its two ends stay visibly joined to that issue.
    # The circle is an empty statutory slot, not a fictional case fact.
    o += line(256, 164, 433, 164, tone='ink', w=4)
    o += f'<path d="M433 164Q472 164 510 129L578 94" style="fill:none;stroke:var(--conc);stroke-width:4;stroke-linecap:round"/>'
    o += f'<path d="M433 164Q472 164 510 199L578 234" style="fill:none;stroke:var(--dif);stroke-width:4;stroke-linecap:round"/>'
    o += f'<circle cx="198" cy="164" r="58" style="fill:var(--paper);stroke:var(--ink);stroke-width:3"/>'
    o += f'<circle cx="198" cy="164" r="38" style="fill:none;stroke:var(--ink-2);stroke-width:1.5;stroke-dasharray:3 5"/>'
    o += f'<circle cx="600" cy="85" r="18" style="fill:var(--conc-wash);stroke:var(--conc);stroke-width:3"/>'
    o += f'<circle cx="600" cy="243" r="18" style="fill:var(--dif-wash);stroke:var(--dif);stroke-width:3"/>'
    o += t(198, 169, 'FATO', size=16, weight=700, anchor='middle')
    o += t(198, 251, 'QUESTÃO DE FATO', size=13, weight=700, anchor='middle')
    o += t(639, 82, 'MEIOS DE PROVA', size=15, weight=700, fill='var(--conc)')
    o += t(639, 105, 'ADMITIDOS', size=12, weight=600, fill='var(--conc)')
    o += t(639, 240, 'ÔNUS DA PROVA', size=15, weight=700, fill='var(--dif)')
    o += t(639, 263, 'ART. 373', size=12, weight=600, fill='var(--dif)')
    return svg('20 24 960 266', o, cls='fig', ident='pci-a10-issue-links',
               label='Cada questão de fato se liga aos meios de prova admitidos e à definição do ônus da prova, observado o art. 373')


def stability_panel(stage='stable'):
    """The common five-day adjustment window follows sanitation; stability closes it."""
    o = ''
    o += t(36, 48, 'ART. 357 · § 1º', size=13, weight=700, fill='var(--ink-2)')
    # The interval begins at sanitation and its endpoint is the statutory stability point.
    o += line(95, 161, 953, 161, tone='conc', w=2.5)
    end_tone = 'dif' if stage == 'stable' else 'muted'
    for x, tone in ((95, 'ink'), (953, end_tone)):
        o += line(x, 136, x, 186, tone=tone, w=2.5)
        o += f'<circle cx="{x}" cy="161" r="5" style="fill:var(--paper);stroke:var(--{tone});stroke-width:2"/>'
    o += f'<path d="M95 96V108H953V96" style="fill:none;stroke:var(--conc);stroke-width:2;stroke-linejoin:round"/>'
    o += t(524, 83, 'PRAZO COMUM · 5 DIAS', size=14, weight=700,
           fill='var(--conc)', anchor='middle')
    o += t(524, 204, 'PEDIR ESCLARECIMENTOS OU SOLICITAR AJUSTES',
           size=11.5, weight=600, anchor='middle')
    o += t(95, 218, 'SANEAMENTO', size=12, weight=700, anchor='start')
    o += t(95, 238, 'REALIZADO', size=11, weight=600, anchor='start')
    o += t(953, 218, 'DECISÃO ESTÁVEL', size=12, weight=700,
           fill='var(--dif)' if stage == 'stable' else 'var(--ink-2)', anchor='end')
    o += t(953, 238, 'FINDO O PRAZO', size=11, weight=600,
           fill='var(--dif)' if stage == 'stable' else 'var(--ink-2)', anchor='end')
    label = ('Após o saneamento, abre-se prazo comum de cinco dias para pedir esclarecimentos ou ajustes'
             if stage == 'open' else
             'Findo o prazo comum de cinco dias, a decisão de saneamento se torna estável')
    ident = 'pci-a10-stability-open' if stage == 'open' else 'pci-a10-stability-stable'
    return svg('20 24 960 236', o, cls='panel on' if stage == 'open' else 'panel', ident=ident,
               label=label).replace('class="panel on figkit"' if stage == 'open' else 'class="panel figkit"',
                                    ('class="panel on figkit" data-family="figure.timeline"' if stage == 'open'
                                     else 'class="panel figkit" data-family="figure.timeline"'))


def case_timeline_panel():
    """Apply the supported colour rule to the existing, source-backed case docket."""
    page = Path(__file__).resolve().parents[2] / 'courses/processo-civil-i/aula-10-estabilizacao.html'
    source = page.read_text(encoding='utf-8')
    match = re.search(r'<svg\b[^>]*\bid="pci-thread-jesse-14"[^>]*>.*?</svg>', source, re.S)
    if not match:
        raise ValueError('Aula 10 case docket SVG was not found')
    drawing = match.group(0)
    # The current exam record supplies no decided result; its two blue bars
    # therefore cannot encode an answer. Keep all conclusion marks in ink.
    drawing = drawing.replace('var(--dif)', 'var(--ink)')
    drawing = drawing.replace('class="fig figkit"', 'class="fig figkit" data-family="figure.autos"')
    return drawing


def replacement_mapping():
    """Pass to inject.inject for this page alone once same-id SVG slots exist."""
    return {'hero': hero(),
            'pci-thread-jesse-14': case_timeline_panel(),
            'pci-a10-stability-open': stability_panel('open'),
            'pci-a10-stability-stable': stability_panel('stable')}
