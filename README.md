# Ordenações Filipinas

A paper-inspired reading collection for law-school study guides.

Live: https://benecles.dev/

## Courses

`courses/controle-de-constitucionalidade/` contains a 36-lesson guide built from the course slides and organized by the nine blocks of the syllabus. Its semester map links the lessons in syllabus order, and each page gives slide references, redrawn diagrams, review questions and source notes. The source slide PDFs and visual digests remain outside this public repository. Where the slides present a debated position, the guide labels it as the source's position; Aula 29 also links to official STF material on the scope of binding effect.

`courses/teoria-do-delito/` contains the full selected Teoria do Delito guide: 15 study units, five doctrinal supplements, the course map and the master study guide. The index groups the reading by the six blocks in the supplied 2026/2 syllabus. Individual week divisions are editorial; they are not verified classroom dates.

`courses/teoria-geral-dos-contratos/` contains 17 lessons on contract theory (concept, principles, formation, classification and the rest of the semester), P1 and P2 review pages, an article reference page and review cards.

`courses/direito-latino-americano/` contains a nine-lesson guide to Direito Latino-americano (DIR03057, UFRGS 2026/2), covering constitutionalism, courts, transitional justice, popular sovereignty and structural litigation in Latin America, plus an activity review page and review cards.

`courses/processo-civil-i/`, `courses/direito-constitucional-i/` and `courses/metodologia-juridica/` were initially built on 2026-09-29 from receipt-checked drafts; new lessons are built through `tools/shell/shell.py` and the workshop lesson machine (`work/lesson-machine/run.py`): Processo Civil I-a has Aulas 01–18, Direito Constitucional I has Aulas 01–18, and Metodologia Jurídica has the lessons whose texts are posted (01–09, 14, 15).

The public editorial page and provenance JSON explain the source/version decisions, input hashes, transformations and bounded review. Source PDFs/books are not distributed by this repository.

## Build

The static chapter builder reads private Markdown inputs and emits standalone HTML, a search index, a catalogue and provenance. See [tools/README.md](tools/README.md). Visitors do not need the build runtime. Reading and links work without JavaScript; search and reading preferences are optional enhancements.

## Design archive

- `experiments/` holds the whole-page material studies and earlier feature experiments.
- `prototype-folio.html` preserves the original illustrated prototype homepage.
- The original standalone prototype pages and alternate homepages remain intact.
- `VISUAL_CRAFT_NOTES.md` records the design process and owner feedback.
