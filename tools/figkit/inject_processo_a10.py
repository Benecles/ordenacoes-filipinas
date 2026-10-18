"""Page-scoped Aula 10 figure integration and specimen entry.

Run from the site root: python3 tools/figkit/inject_processo_a10.py
The shared injector's byte-preserving replacement function is called directly; its
all-pages registry is not changed. The specimen section is updated idempotently.
"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import proc_a10
from inject import by_ids, element_span, inject
import re

PAGE = 'courses/processo-civil-i/aula-10.html'
BEGIN = '<!-- figkit:processo-a10:begin -->'
END = '<!-- figkit:processo-a10:end -->'
ANCHOR = '<script src="../courses/processo-civil-i/assets/aula-17.js"></script>'


def specimen_entry():
    actual, variation = proc_a10.decision_panels(specimen=True)
    return (f'{BEGIN}<section class="ref" id="pci-a10-decision-form"><header>'
            '<span class="g">Documento · decisão conforme o estado do processo</span>'
            '<span class="v">verbo · escolher</span></header>'
            '<h2>Processo · Aula 10 · a mesma ação e uma única mudança</h2>'
            '<p>O registro de Florianópolis termina por decadência. Na variação identificada, só o ajuizamento passa a ser tempestivo; a alegação do item 15, a pergunta sobre prova, o pedido do item 16 e as peças permanecem iguais.</p>'
            '<p class="r">novo componente · pci-a10-decision-record + pci-a10-decision-variation</p>'
            f'<div class="grid"><div class="s">{actual}</div><div class="s">{variation}</div></div>'
            '</section>' + END)


def add_specimen():
    path = ROOT / 'specimen/figuras.html'
    page = path.read_text(encoding='utf-8')
    # Keep the existing F1 catalog entry byte-local while refreshing its generated art.
    matches = list(re.finditer(r'<svg\b[^>]*\bid="pci-a10-docket"', page))
    if len(matches) != 1:
        raise ValueError(f'expected one Aula 10 docket specimen, found {len(matches)}')
    start, end = element_span(page, matches[0].start())
    page = page[:start] + proc_a10.timeline_panel(specimen=True) + page[end:]
    page = page.replace('Compra informada por mês, ajuizamento e decisão por dia: a escala preserva a precisão de cada registro.',
                        'O registro compartilhado cresce da posição 13 até esta escolha e conserva a precisão das datas, peças e resultado.')
    entry = specimen_entry()
    if BEGIN in page and END in page:
        a = page.index(BEGIN)
        b = page.index(END, a) + len(END)
        page = page[:a] + entry + page[b:]
    else:
        if page.count(ANCHOR) != 1:
            raise ValueError(f'expected one specimen insertion anchor, found {page.count(ANCHOR)}')
        page = page.replace(ANCHOR, entry + ANCHOR, 1)
    path.write_text(page, encoding='utf-8')


def main():
    replacements = {
        'a10_hero': proc_a10.hero(),
        **by_ids(proc_a10.timeline_panel(), *proc_a10.decision_panels()),
    }
    count = inject(PAGE, replacements)
    add_specimen()
    print(f'{PAGE}: {count} figures; specimen entry updated')


if __name__ == '__main__':
    main()
