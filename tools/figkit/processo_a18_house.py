"""Aula 18 release 4.2 figures: case answer and staged proof instrument."""
from pathlib import Path
import re
import inject
import figkit

PAGE = 'courses/processo-civil-i/aula-18.html'
ROOT = Path(__file__).resolve().parents[2]


def case_panel():
    """The cited REsp separates a procedural fact from the fact to be shown."""
    o = figkit.t(64, 36, 'STJ · REsp 692.242/MG', size=11, fill='var(--ink-2)', weight=700)
    o += figkit.line(64, 51, 536, 51, tone='ink', w=1.2)
    o += figkit.t(154, 90, 'DADO PROCESSUAL', size=10, fill='var(--ink-2)', anchor='middle', weight=700)
    o += figkit.t(154, 128, 'RECUSA AO', size=16, anchor='middle', weight=700, ls='.02em')
    o += figkit.t(154, 151, 'EXAME DE DNA', size=16, anchor='middle', weight=700, ls='.02em')
    o += figkit.t(300, 143, '≠', size=25, fill='var(--ink)', anchor='middle', weight=600, ls='0')
    o += figkit.t(446, 90, 'FATO A DEMONSTRAR', size=10, fill='var(--ink-2)', anchor='middle', weight=700)
    o += figkit.t(446, 128, 'RELAÇÃO ÍNTIMA', size=14, anchor='middle', weight=700, ls='.02em')
    o += figkit.t(446, 151, 'MÃE E SUPOSTO PAI', size=11, anchor='middle', weight=600, ls='.01em')
    o += figkit.line(64, 181, 536, 181, tone='ink', w=1)
    o += figkit.line(154, 173, 154, 189, tone='ink', w=1)
    o += figkit.line(446, 173, 446, 189, tone='ink', w=1)
    o += figkit.t(300, 225, 'INDÍCIOS CIRCUNSTANCIAIS MÍNIMOS', size=12, fill='var(--conc)', anchor='middle', weight=700)
    o += figkit.t(300, 250, 'A recusa não substitui esse suporte', size=11, fill='var(--ink-2)', anchor='middle', weight=500, ls='.01em')
    return figkit.svg('0 0 600 300', o, cls='fig', ident='pci-a18-case', label='No REsp 692.242/MG, a recusa ao exame de DNA não substitui indícios mínimos de relação íntima na investigação de paternidade')


def hero_panel():
    """Case record: blue marks the decided answer, orange the limit."""
    o = figkit.t(40, 36, 'STJ · REsp 692.242/MG', size=11, fill='var(--ink-2)', weight=700)
    o += figkit.line(40, 51, 560, 51, tone='ink', w=1.2)
    o += figkit.t(300, 91, 'RECUSA AO EXAME DE DNA', size=14, fill='var(--ink)', anchor='middle', weight=700)
    o += figkit.line(90, 110, 510, 110, tone='ink', w=1)
    o += figkit.t(300, 151, 'NÃO DISPENSOU', size=17, fill='var(--dif)', anchor='middle', weight=700)
    o += figkit.t(300, 181, 'INDÍCIOS CIRCUNSTANCIAIS MÍNIMOS', size=12, fill='var(--conc)', anchor='middle', weight=700)
    o += figkit.t(300, 216, 'investigação de paternidade', size=11, fill='var(--ink-2)', anchor='middle', weight=500)
    return figkit.svg('0 0 600 240', o, cls='fig hero-form', ident='pci-a18-hero-case', label='No REsp 692.242/MG, a recusa ao exame de DNA não dispensou indícios circunstanciais mínimos na investigação de paternidade').replace('<svg', '<svg data-family="figure.autos"', 1)


def opening_bet():
    return '''<div class="bet" id="a18-opening-bet"><div><span class="bet-k">Antes de ler · REsp 692.242/MG · 3ª Turma · 28 jun. 2005</span><p class="bet-q">A recusa ao exame de DNA dispensou indícios mínimos de relação íntima na investigação de paternidade?</p><div class="bet-opts"><button type="button" data-opt="0" aria-pressed="false">Sim: a recusa basta para suprir o suporte factual.</button><button type="button" data-opt="1" data-court aria-pressed="false">Não: o acórdão exige indícios circunstanciais mínimos de relação íntima.</button></div><div class="bet-reveal"><p>Não. O STJ exige indícios circunstanciais mínimos de relação íntima entre a mãe e o suposto pai.</p></div></div></div>'''


def stage_sequence(active):
    """A three-step instrument; semantic color is reserved for the case result and limit."""
    titles = ('MEIO DE PROVA', 'MEDIDA PROBATÓRIA', 'RESULTADO')
    body = ('legal e moralmente legítimo', 'necessária ao mérito', 'NÃO DISPENSOU')
    o = figkit.t(42, 38, 'REsp 692.242/MG · DECISÃO SOBRE PROVA', size=11, fill='var(--ink-2)', weight=700)
    o += figkit.line(42, 54, 558, 54, tone='ink', w=1.2)
    o += '<text x="300" y="105" text-anchor="middle" style="font-family:var(--sans);font-size:21px;font-weight:650;fill:var(--ink)">Qual pergunta está aberta?</text>'
    o += figkit.t(300, 166, titles[active], size=15, fill='var(--ink)', anchor='middle', weight=700)
    o += figkit.t(300, 218, body[active], size=18 if active < 2 else 17,
                  fill='var(--dif)' if active == 2 else 'var(--ink)', anchor='middle', weight=700)
    if active == 2:
        o += figkit.line(120, 242, 480, 242, tone='ink', w=1)
        o += figkit.t(300, 284, 'INDÍCIOS CIRCUNSTANCIAIS MÍNIMOS', size=12,
                      fill='var(--conc)', anchor='middle', weight=700)
    o += figkit.t(300, 347, ('CPC · ART. 369' if active == 0 else 'CPC · ART. 370' if active == 1 else 'AVALIAÇÃO DA PROVA'), size=11, fill='var(--ink-2)', anchor='middle', weight=700)
    labels_for_screenreader = (
        'Questão 1: possibilidade de produzir o meio.',
        'Questão 2: necessidade da medida para decidir o mérito.',
        'Questão 3: avaliação do resultado; a recusa ao exame de DNA não dispensou indícios mínimos.'
    )
    return figkit.svg('0 0 600 390', o, cls='panel' + (' on' if active == 0 else ''), ident=f'pci-a18-three-question-{active + 1}', label=labels_for_screenreader[active]).replace('<svg', '<svg data-family="figure.timeline"', 1)


def staged_instrument():
    specs = (
        ('Antes da produção · o meio pode entrar?', 'Examine se o meio é legal e moralmente legítimo. No caso, o acórdão considerou o suporte indiciário mínimo.'),
        ('Antes da decisão · a medida é necessária?', 'Relacione a diligência ao fato relevante e ao que falta para decidir o mérito.'),
        ('Depois da produção · o que os autos sustentam?', 'Avalie a prova e exponha as razões. No REsp 692.242/MG, os indícios circunstanciais mínimos sustentaram a inferência.'),
    )
    panels = ''.join(stage_sequence(i) for i in range(3))
    steps = ''.join(f'<div class="step{" on" if i == 0 else ""}" data-panel="pci-a18-three-question-{i+1}" data-slides="{title}"><div class="card"><h3>{title}</h3><p>{body}</p></div></div>' for i, (title, body) in enumerate(specs))
    return f'''<div class="scrolly a18-scrolly" id="pci-a18-three-questions" aria-label="Três perguntas sobre produção, necessidade e avaliação da prova"><div class="stage" aria-hidden="true"><figure class="a18-panel a18-instrument">{panels}<figcaption id="a18-instrument-caption">Instrumento · localize se a decisão examina a possibilidade do meio, a necessidade da diligência ou o resultado da prova. <span class="stage-count">1 / 3</span></figcaption></figure></div><div class="steps">{steps}</div></div>'''


def install():
    case = case_panel()
    inject.inject(PAGE, {case.split('id="', 1)[1].split('"', 1)[0]: case})
    path = ROOT / PAGE
    source = path.read_text(encoding='utf-8')
    stage_start, stage_end = '<!-- A18R_STAGE_START -->', '<!-- A18R_STAGE_END -->'
    stage_block = stage_start + staged_instrument() + stage_end
    if stage_start in source and stage_end in source:
        source = re.sub(re.escape(stage_start) + r'.*?' + re.escape(stage_end), lambda _: stage_block, source, count=1, flags=re.S)
    else:
        old = re.compile(r'<figure class="a18-panel a18-instrument" id="pci-a18-three-questions"[\s\S]*?</figure>')
        source, count = old.subn(stage_block, source, count=1)
        if count != 1:
            raise SystemExit(f'expected one original Aula 18 staged figure; found {count}')
    if '<!-- A18R_BET_START -->' not in source:
        source = source.replace('</header>', '</header><!-- A18R_BET_START -->' + opening_bet() + '<!-- A18R_BET_END -->', 1)
    else:
        source = re.sub(r'<!-- A18R_BET_START -->.*?<!-- A18R_BET_END -->', '<!-- A18R_BET_START -->' + opening_bet() + '<!-- A18R_BET_END -->', source, count=1, flags=re.S)
    if '<!-- A18R_HERO_START -->' not in source:
        hero = '<figure class="hero-art">' + hero_panel() + '<figcaption>REsp 692.242/MG · recusa ao DNA e indícios circunstanciais mínimos.</figcaption></figure>'
        source = source.replace('<div class="titleblock label"', '<!-- A18R_HERO_START -->' + hero + '<!-- A18R_HERO_END --><div class="titleblock label"', 1)
    else:
        hero = '<figure class="hero-art">' + hero_panel() + '<figcaption>REsp 692.242/MG · recusa ao DNA e indícios circunstanciais mínimos.</figcaption></figure>'
        source = re.sub(r'<!-- A18R_HERO_START -->.*?<!-- A18R_HERO_END -->', '<!-- A18R_HERO_START -->' + hero + '<!-- A18R_HERO_END -->', source, count=1, flags=re.S)
    style = '.hero-art{max-width:900px;margin:24px auto 0}.hero-art svg{display:block;width:min(100%,720px);height:auto}.hero-art figcaption{max-width:720px;margin:8px auto 0;font:500 11px/1.5 var(--mono);color:var(--ink-2)}.a18-scrolly .stage figure{aspect-ratio:600/390}.a18-scrolly .stage figure svg{display:block;width:100%;height:auto}.a18-scrolly .steps .card{max-width:54ch}@media(max-width:560px){.a18-scrolly .stage figure{aspect-ratio:600/450}}'
    if '/* A18R_CSS_START */' not in source:
        source = source.replace('</style></head>', '/* A18R_CSS_START */' + style + '/* A18R_CSS_END */</style></head>', 1)
    else:
        source = re.sub(r'/\* A18R_CSS_START \*/.*?/\* A18R_CSS_END \*/', '/* A18R_CSS_START */' + style + '/* A18R_CSS_END */', source, count=1, flags=re.S)
    limit_sentence = 'A pergunta prática é se a prova indicada ajuda a decidir o mérito. A lei manda indeferir diligências inúteis ou meramente protelatórias'
    marked_limit = 'A pergunta prática é se a prova indicada ajuda a decidir o mérito. A lei manda indeferir <span class="limit">diligências inúteis ou meramente protelatórias</span>'
    source = source.replace(limit_sentence, marked_limit, 1)
    path.write_text(source, encoding='utf-8')
    return path


def specimen_page():
    css = (ROOT / 'courses/processo-civil-i/assets/curso.css').as_uri()
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Figkit · Processo Aula 18</title><link rel="stylesheet" href="{css}"></head><body>{hero_panel()}{case_panel()}{staged_instrument()}</body></html>'''


if __name__ == '__main__':
    import os
    probe = os.environ.get('FIGKIT_PROBE')
    if probe:
        Path(probe).write_text(specimen_page(), encoding='utf-8')
        print(probe)
    else:
        print(f'{install()} figures installed')
    print('\n'.join(figkit.WARN) or 'no text warnings')
