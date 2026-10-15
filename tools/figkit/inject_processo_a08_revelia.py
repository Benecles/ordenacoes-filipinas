"""Install only the two Aula 08-revelia figkit instruments and specimen entry."""
from pathlib import Path
import sys
import re

from processo_a08_revelia import filing_form, case_timeline, specimen_entry

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / 'courses/processo-civil-i/aula-08-revelia.html'
SPECIMEN = ROOT / 'specimen/figuras.html'


def install_page(source):
    replacements = {
        '<!-- FIGKIT_A08_FORM -->': ('pci-a08r-filing-form',
            '<figure class="fig-wrap">' + filing_form()
            + '<figcaption>Marque os atos que aparecem na resposta de Dalvo.</figcaption></figure>'
        ),
        '<!-- FIGKIT_A08_TIMELINE -->': ('pci-a08r-case-timeline',
            '<figure class="fig-wrap">' + case_timeline()
            + '<figcaption>A escala fixa os dois dias indicados no enunciado; a primeira semana permanece como marco ordinal.</figcaption></figure>'
        ),
    }
    for marker, (ident, figure) in replacements.items():
        if source.count(marker) == 1:
            source = source.replace(marker, figure, 1)
        elif f'id="{ident}"' in source:
            pattern = re.compile(r'<figure class="fig-wrap">(?:(?!</figure>).)*?id="' + re.escape(ident) + r'".*?</figure>', re.S)
            source, count = pattern.subn(figure, source, count=1)
            if count != 1:
                raise ValueError(f'could not replace installed {ident} figure')
        else:
            raise ValueError(f'expected one {marker} marker or installed {ident} in Aula 08-revelia')
    return source


def install_specimen(source):
    if 'id="specimen-pci-a08r"' in source:
        pattern = re.compile(r'<section class="ref" id="specimen-pci-a08r">.*?</section>', re.S)
        source, count = pattern.subn(specimen_entry(), source, count=1)
        if count != 1:
            raise ValueError('could not replace installed Aula 08-revelia specimen')
        return source
    anchor = '<script src="../courses/processo-civil-i/assets/aula-17.js"></script>'
    if source.count(anchor) != 1:
        raise ValueError('figure specimen insertion anchor is absent or duplicated')
    return source.replace(anchor, specimen_entry() + '\n' + anchor, 1)


if __name__ == '__main__':
    page_before = PAGE.read_text(encoding='utf-8')
    page_after = install_page(page_before)
    PAGE.write_text(page_after, encoding='utf-8')
    specimen_before = SPECIMEN.read_text(encoding='utf-8')
    specimen_after = install_specimen(specimen_before)
    if specimen_after != specimen_before:
        SPECIMEN.write_text(specimen_after, encoding='utf-8')
    print(f'{PAGE}: 2 figures installed; specimen: {int(specimen_after != specimen_before)} updated')
