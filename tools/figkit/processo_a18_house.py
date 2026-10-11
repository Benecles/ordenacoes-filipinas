"""Aula 18 house figures: the real paternity case and the Q11 proof sequence."""
from pathlib import Path
import re
import inject
import figkit

PAGE = 'courses/processo-civil-i/aula-18.html'


def case_panel():
    """The cited REsp separates refusal of DNA from the minimum circumstantial indicia."""
    o = figkit.t(64, 36, 'STJ · REsp 692.242/MG', size=11, fill='var(--ink-2)', weight=700)
    o += figkit.line(64, 51, 536, 51, tone='ink', w=1.2)
    o += figkit.t(154, 90, 'DADO PROCESSUAL', size=10, fill='var(--conc)', anchor='middle', weight=700)
    o += figkit.t(154, 128, 'RECUSA AO', size=16, anchor='middle', weight=700, ls='.02em')
    o += figkit.t(154, 151, 'EXAME DE DNA', size=16, anchor='middle', weight=700, ls='.02em')
    o += figkit.t(300, 143, '≠', size=25, fill='var(--conc)', anchor='middle', weight=600, ls='0')
    o += figkit.t(446, 90, 'FATO A DEMONSTRAR', size=10, fill='var(--ink-2)', anchor='middle', weight=700)
    o += figkit.t(446, 128, 'RELAÇÃO ÍNTIMA', size=14, anchor='middle', weight=700, ls='.02em')
    o += figkit.t(446, 151, 'MÃE E SUPOSTO PAI', size=11, anchor='middle', weight=600, ls='.01em')
    o += figkit.line(64, 181, 536, 181, tone='ink', w=1)
    o += figkit.line(154, 173, 154, 189, tone='conc', w=2)
    o += figkit.line(446, 173, 446, 189, tone='dif', w=2)
    o += figkit.t(300, 225, 'INDÍCIOS CIRCUNSTANCIAIS MÍNIMOS', size=12, fill='var(--dif)', anchor='middle', weight=700)
    o += figkit.t(300, 250, 'A recusa não substitui esse suporte', size=11, fill='var(--ink-2)', anchor='middle', weight=500, ls='.01em')
    return figkit.svg('0 0 600 300', o, cls='fig', ident='pci-a18-case',
                      label='No REsp 692.242/MG, a recusa ao exame de DNA não substitui indícios mínimos de relação íntima na investigação de paternidade')


def three_questions_panel():
    """Accessible HTML instrument for locating the evidentiary stage."""
    return f'''<figure class="a18-panel a18-instrument" id="pci-a18-three-questions" aria-labelledby="a18-instrument-title">
<div class="a18-instrument__head"><span class="label">REsp 692.242/MG · decisão sobre prova</span>
<h3 id="a18-instrument-title">Qual pergunta está aberta?</h3></div>
{stage_sequence()}
<ol class="a18-stages">
<li><details open><summary>Antes da produção · o meio pode entrar?</summary><p>Identifique a afirmação factual e examine se o meio proposto é legal e moralmente legítimo. A recusa ao DNA, no caso, não eliminou a necessidade de indícios circunstanciais mínimos sobre a relação íntima.</p></details></li>
<li><details><summary>Antes da decisão · a medida é necessária?</summary><p>Relacione a diligência ao fato relevante e ao que falta para decidir o mérito. O pedido ou a iniciativa judicial não dispensa essa justificativa.</p></details></li>
<li><details><summary>Depois da produção · o que os autos sustentam?</summary><p>Avalie o conjunto e exponha as razões da conclusão. Se a dúvida permanecer, o ônus de prova trata dessa incerteza residual.</p></details></li>
</ol>
<figcaption>Instrumento · localize se a decisão examina a possibilidade do meio, a necessidade da diligência ou o resultado da prova.</figcaption>
</figure>'''


def stage_sequence():
    """Kit-drawn order line that accompanies the accessible HTML decision instrument."""
    o = figkit.line(74, 31, 846, 31, tone='ink', w=1.6)
    labels = (('01 · MEIO', 74, 'conc'), ('02 · MEDIDA', 460, 'mix'), ('03 · RESULTADO', 846, 'dif'))
    for label, x, tone in labels:
        o += f'<circle cx="{x}" cy="31" r="6" style="fill:var(--paper);stroke:var(--{tone});stroke-width:2"/>'
        o += figkit.t(x, 65, label, size=11, fill=f'var(--{tone})', anchor='middle', weight=700, ls='.04em')
    return figkit.svg('25 0 870 76', o, cls='fig', ident='pci-a18-three-question-sequence',
                      label='Sequência de exame do meio, necessidade da medida e avaliação do resultado')


def panels():
    figkit.WARN.clear()
    return [case_panel(), three_questions_panel()]


def install():
    case = case_panel()
    inject.inject(PAGE, {case.split('id="', 1)[1].split('"', 1)[0]: case})
    path = Path(__file__).resolve().parents[2] / PAGE
    source = path.read_text(encoding='utf-8')
    patterns = (r'<figure\b[^>]*\bid="pci-a18-three-questions"[\s\S]*?</figure>',
                r'<figure\b[^>]*>[\s\S]*?<svg\b[^>]*\bid="pci-a18-three-questions"[\s\S]*?</figure>')
    matches = [m for pattern in patterns for m in re.finditer(pattern, source)]
    matches = sorted({(m.start(), m.end()): m for m in matches}.values(), key=lambda m: m.start())
    if len(matches) != 1:
        raise SystemExit(f'expected one Aula 18 three-question figure; found {len(matches)}')
    match = matches[0]
    source = source[:match.start()] + three_questions_panel() + source[match.end():]
    path.write_text(source, encoding='utf-8')
    return path


def specimen_page():
    css = (Path(__file__).resolve().parents[2] /
           'courses' / 'processo-civil-i' / 'assets' / 'curso.css').as_uri()
    panels_html = ''.join(f'<section><h2>{svg}</h2><div class="sample">{panel}</div></section>'
                          for svg, panel in zip(('REsp 692.242/MG', 'A questão de exame'), panels()))
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Figkit · Processo Aula 18</title>
<link rel="stylesheet" href="{css}"><style>body{{max-width:1000px;margin:0 auto;padding:28px 18px;background:var(--paper);color:var(--ink)}}h1{{font:750 28px/1.1 var(--sans)}}h2{{font:600 13px var(--mono)}}.sample{{max-width:920px;margin:20px auto 32px;padding:12px;border:1.5px solid var(--ink);background:var(--paper)}}</style></head><body>
<h1>Processo · Aula 18 · figuras de apoio</h1>{panels_html}</body></html>'''


if __name__ == '__main__':
    import os
    probe = os.environ.get('FIGKIT_PROBE')
    if probe:
        Path(probe).write_text(specimen_page(), encoding='utf-8')
        print(probe)
    else:
        print(f'{install()} figure(s) installed')
    print('\n'.join(figkit.WARN) or 'no text warnings')
