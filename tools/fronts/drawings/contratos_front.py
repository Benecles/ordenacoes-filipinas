#!/usr/bin/env python3
"""Generate the Contratos course index as two bound leaves, one per exam."""
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import front  # noqa: E402

SLUG = 'teoria-geral-dos-contratos'
DATA = HERE.parent / 'data' / f'{SLUG}.json'

# Each note points to the provision's home in the approved course blueprint.
CLAUSES = {
    'aula-01.html': ('Contrato e relação de consumo', 'CC 104 · CDC 2º–4º'),
    'aula-02.html': ('Liberdade, vínculo e terceiros', 'CC 421 e 421-A'),
    'aula-03.html': ('Da proposta à aceitação', 'CC 422 e 427–435'),
    'aula-04.html': ('Terceiros, preliminar e arras', 'CC 417–420, 436–440 e 462–471'),
    'aula-05.html': ('Forma, risco e garantias', 'CC 107–109 e 441–461'),
    'aula-06.html': ('Prestações recíprocas e adesão', 'CC 476–477 · CDC 54'),
    'aula-07.html': ('O sentido da declaração', 'CC 112–114 e 423 · CDC 46–47'),
    'aula-08.html': ('A posição passa a outra parte', 'CC 299, por analogia'),
    'aula-09.html': ('Lesão, imprevisão e base do negócio', 'CC 157, 317 e 478–480'),
    'aula-10.html': ('Cumprimento, distrato e resolução', 'CC 472–475'),
}


def row(lesson, number):
    esc = html.escape
    href, title = lesson['href'], lesson['title']
    topic, provision = CLAUSES[href]
    minutes = front._minutes(SLUG, href)
    time_id = f'vida-time-{number}'
    time = f'<span class="vida-time" id="{time_id}">{minutes} min</span>' if minutes is not None else ''
    details = f'vida-note-{number}' + (f' {time_id}' if time else '')
    return (
        f'<li><a class="vida-row" href="{esc(href)}" aria-labelledby="vida-title-{number}"'
        f' aria-describedby="{details}">'
        '<span class="vida-tab">'
        f'<span class="vida-heading" id="vida-title-{number}"><span class="vida-number">{number:02d}</span>'
        f'<span>{esc(title)}</span></span>{time}</span>'
        f'<span class="vida-clause" id="vida-note-{number}"><span class="vida-topic">{esc(topic)}</span>'
        f'<span class="vida-law">{esc(provision)}</span></span></a></li>'
    )


def leaf(exam, lessons, position, title, start):
    label = html.escape(exam['label'])
    rows = ''.join(row(lessons[href], number) for number, href in enumerate(exam['covers'], start))
    return (
        f'<section class="vida-leaf vida-{position}" aria-labelledby="vida-{label}">'
        f'<h2 id="vida-{label}"><span class="vida-exam">{label}</span> {title}</h2>'
        f'<ol start="{start}">{rows}</ol></section>'
    )


def draw(data):
    lessons = {lesson['href']: lesson for unit in data['units'] for lesson in unit['lessons']}
    exams = data['reg']['exams']
    if [exam['label'] for exam in exams] != ['P1', 'P2']:
        raise ValueError('The open contract requires both exam leaves in study order.')
    if [href for exam in exams for href in exam['covers']] != list(lessons) or set(lessons) != CLAUSES.keys():
        raise ValueError('The exam leaves, register and clause notes must cover the same lessons.')
    return (
        '<figure id="aulas" class="vida-fig" aria-label="Índice das aulas" data-genre="instrumento" '
        'data-does="abrir · o leitor escolhe uma aba → a cláusula correspondente se destaca e dá acesso à aula">'
        '<div class="vida-titleblock" aria-hidden="true"><span>Instrumento contratual</span>'
        f'<span>{html.escape(data["code"])}</span></div>'
        '<div class="vida-spread">'
        + leaf(exams[0], lessons, 'left', 'Formação e vínculo', 1)
        + leaf(exams[1], lessons, 'right', 'Execução e extinção', 1 + len(exams[0]['covers']))
        + '</div></figure>'
    )


CSS = """
header.front-title { padding-block: clamp(20px, 3vh, 32px) 14px; }
header.front-title h1 { max-width: none; font-size: clamp(34px, 4.25vw, 58px); margin-block: 10px 8px; }
header.front-title .front-deck { max-width: 68ch; }
.vida-fig { margin: 0; }
.vida-titleblock {
  display: flex; justify-content: space-between; gap: 1em;
  padding: 8px 14px; background: var(--ink); color: var(--paper);
  font: 600 11px/1.4 var(--mono); letter-spacing: .09em; text-transform: uppercase;
}
.vida-spread { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; position: relative; }
.vida-spread::before, .vida-spread::after {
  content: ""; position: absolute; left: 50%; z-index: 1; width: 24px; height: 4px;
  transform: translateX(-50%); background: var(--ink); pointer-events: none;
}
.vida-spread::before { top: 22%; }
.vida-spread::after { bottom: 16%; }
.vida-leaf {
  min-width: 0; display: grid; grid-template-rows: auto 1fr;
  background: var(--paper); border: 1px solid var(--ink); padding-block: 15px;
  box-shadow: 3px 4px 0 var(--grid-major);
}
.vida-leaf h2 {
  display: flex; align-items: baseline; gap: 9px; margin: 0 16px 9px;
  padding: 0 0 10px; border-bottom: 1px solid var(--ink);
  font: 700 clamp(17px, 1.65vw, 23px)/1.15 var(--sans);
}
.vida-exam { font: 600 11px/1 var(--mono); letter-spacing: .07em; color: var(--ink-2); }
.vida-leaf ol {
  list-style: none; margin: 0; padding: 0;
  display: grid; grid-template-rows: repeat(5, minmax(80px, 1fr));
}
.vida-row {
  display: grid; grid-template-columns: minmax(0, .86fr) minmax(0, 1fr);
  align-items: stretch; min-height: 100%; color: var(--ink);
  text-decoration: none; cursor: pointer;
}
.vida-right .vida-row { grid-template-columns: minmax(0, 1fr) minmax(0, .86fr); }
.vida-tab {
  box-sizing: border-box; display: grid; align-content: center; row-gap: 6px; align-self: center;
  background: var(--paper-2); padding: 9px 12px; border: 1px solid var(--ink);
  margin-inline: -5px 0; box-shadow: 2px 2px 0 var(--grid-major);
}
.vida-right .vida-tab { grid-column: 2; grid-row: 1; margin-inline: 0 -5px; }
.vida-heading { display: grid; grid-template-columns: 19px 1fr; gap: 6px; align-items: baseline; font: 650 15px/1.22 var(--sans); }
.vida-number, .vida-time, .vida-law { color: var(--ink-2); font: 500 11.5px/1.35 var(--mono); }
.vida-time { margin-inline-start: 25px; }
.vida-clause {
  min-width: 0; display: grid; align-content: center; gap: 4px;
  margin: 0 13px 0 0; padding: 8px 9px 8px 13px;
  border-bottom: 1px solid var(--rule);
}
.vida-right .vida-clause { grid-column: 1; grid-row: 1; margin-inline: 13px 0; }
.vida-topic { font: 500 clamp(15px, 1.5vw, 17px)/1.24 var(--serif); }
.vida-row:is(:hover, :focus-visible) .vida-clause {
  background: var(--paper-2); box-shadow: inset 0 -1px 0 var(--ink);
}
.vida-row:is(:hover, :focus-visible) .vida-heading > :last-child {
  text-decoration: underline; text-underline-offset: .19em;
}
.vida-row:focus-visible { position: relative; outline: 2px solid var(--ink); outline-offset: 2px; z-index: 2; }
.vida-review { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px 24px; width: 100%; }
.front-exam:has(.vida-review) .front-exam-content,
.front-exam-content > .front-exam-card:has(.vida-review) { width: 100%; }
.front-exam-card:has(.vida-review) h2 { font: 700 23px/1.15 var(--sans); margin: 0 0 14px; }
.vida-review .front-review { font-size: 15px; }
.front-exam-card .vida-resume { margin-top: 14px; }
@media (max-width: 860px) and (orientation:portrait) {
  .vida-spread { grid-template-columns: minmax(0, 1fr); gap: 13px; }
  .vida-spread::before, .vida-spread::after { display: none; }
  .vida-leaf ol { grid-template-rows: none; grid-auto-rows: minmax(82px, auto); }
  .vida-right .vida-row { grid-template-columns: minmax(0, .86fr) minmax(0, 1fr); }
  .vida-right .vida-tab { grid-column: 1; margin-inline: -5px 0; }
  .vida-right .vida-clause { grid-column: 2; margin-inline: 0 13px; }
}
@media (max-width: 520px) and (orientation:portrait) {
  .vida-row, .vida-right .vida-row { grid-template-columns: minmax(0, 1fr); }
  .vida-leaf ol { gap: 8px; }
  .vida-tab, .vida-right .vida-tab { grid-column: 1; grid-row: 1; margin-right: 13px; grid-template-columns: 1fr auto; align-items: baseline; }
  .vida-tab .vida-time { margin-inline-start: 0; white-space: nowrap; }
  .vida-clause, .vida-right .vida-clause { grid-column: 1; grid-row: 2; margin-inline: 13px; }
  .vida-review { grid-template-columns: minmax(0, 1fr); }
}
"""


def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    data['drawing'] = {'html': draw(data), 'css': CSS}
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Updated the contract drawing in {DATA.name}')


if __name__ == '__main__':
    main()
