"""Install only Aula 08-revelia's 4.2 hero, opening bet, and staged record."""
from pathlib import Path
import re

from processo_a08_revelia import filing_form, case_timeline_panels, specimen_entry

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / 'courses/processo-civil-i/aula-08-revelia.html'
SPECIMEN = ROOT / 'specimen/figuras.html'

HERO_START, HERO_END = '<!-- A08R_HERO_START -->', '<!-- A08R_HERO_END -->'
BET_START, BET_END = '<!-- A08R_BET_START -->', '<!-- A08R_BET_END -->'
TIME_START, TIME_END = '<!-- A08R_TIME_START -->', '<!-- A08R_TIME_END -->'
STYLE_START, STYLE_END = '/* A08R_42_START */', '/* A08R_42_END */'


def _replace_marked(source, start, end, content):
    pattern = re.compile(re.escape(start) + r'.*?' + re.escape(end), re.S)
    if source.count(start) == 1 and source.count(end) == 1:
        return pattern.sub(start + content + end, source, count=1)
    if source.count(start) or source.count(end):
        raise ValueError(f'partial or duplicate marker pair: {start}')
    return None


def _hero_block():
    return (
        '<figure class="hero-art">' + filing_form()
        + '<figcaption>Contestação e reconvenção têm funções distintas; a linha laranja marca o requisito de conexão.</figcaption></figure>'
    )


def _bet_block():
    return '''<div class="bet" id="a08r-opening-bet"><div><span class="bet-k">Antes de ler · Avaliação 2 · 2015/1 · questão 3</span><p class="bet-q">A ação originária de Jesse e a reconvenção de Dalvo podem ter os dois pedidos julgados integralmente procedentes ao mesmo tempo?</p><div class="bet-opts"><button type="button" data-opt="0" data-court aria-pressed="false">Sim: a ação e a reconvenção contêm pedidos próprios, examinados por seus fundamentos.</button><button type="button" data-opt="1" aria-pressed="false">Não: a reconvenção só pode ser julgada procedente se a ação de Jesse for improcedente.</button></div><div class="bet-reveal"><p>Sim. A alternativa C da questão admite a procedência integral dos dois pedidos. A contestação enfrenta a cobrança de Jesse; a reconvenção apresenta uma pretensão própria de Dalvo.</p></div></div></div>'''


def _timeline_block():
    panels = case_timeline_panels()
    ids = ('pci-a08r-time-hearing', 'pci-a08r-time-contestation', 'pci-a08r-time-supplement')
    stages = (
        ('01/04/2015 · audiência', 'Jesse, Dalvo e Serotonina comparecem à audiência preliminar, sem acordo.', 'registro'),
        ('Primeira semana · contestação', 'Dalvo apresenta a contestação na primeira semana do prazo. A anotação ordinal acompanha o mesmo caso.', 'contestação'),
        ('13/04/2015 · complementação', 'Ao perceber que alguns fatos não tinham sido expressamente impugnados, Dalvo protocola de pronto complemento à contestação.', 'complementação'),
    )
    figure = (
        '<div class="stage"><figure data-staged="true">' + ''.join(panels)
        + '<figcaption><span class="stage-count">01/04 → 13/04 · caso</span><span class="stage-step">1 / 3</span></figcaption></figure></div>'
    )
    steps = []
    for i, (panel, (title, prose, slide)) in enumerate(zip(ids, stages)):
        source = '<span class="src">Avaliação 2 · Processo Civil I · 2015/1 · questão 3</span>' if i == 0 else ''
        steps.append(
            f'<div class="step{" on" if i == 0 else ""}" data-panel="{panel}" data-slides="{slide}"><div class="card">'
            + source + f'<h3>{title}</h3><p>{prose}</p></div></div>'
        )
    return '<div class="scrolly a08-scrolly">' + figure + '<div class="steps">' + ''.join(steps) + '</div></div>'


def _style_block():
    return ('.hero-art{max-width:900px;margin:26px 0 0}.hero-art svg{display:block;width:min(100%,760px);height:auto}.hero-art figcaption{font:500 11px/1.5 var(--mono);color:var(--ink-2);margin:8px 0 0}.a08-scrolly .stage figure{aspect-ratio:540/340}.a08-scrolly .stage figure svg{display:block}')


def install_page(source):
    # Replace old live figure(s) once, then use explicit markers for subsequent generations.
    hero = _replace_marked(source, HERO_START, HERO_END, _hero_block())
    if hero is not None:
        source = hero
    else:
        # The previous single-state form lived in chapter 02; the approved build places it in the hero.
        old_form = re.compile(r'<figure\b(?:(?!</figure>).)*?id="pci-a08r-filing-form"(?:(?!</figure>).)*?</figure>', re.S)
        if 'id="pci-a08r-filing-form"' in source and 'id="pci-a08r-filing-form"' not in source.split('</header>', 1)[0]:
            source, count = old_form.subn('', source, count=1)
            if count != 1:
                raise ValueError('could not move the existing filing form into the hero')
        if 'id="pci-a08r-filing-form"' not in source.split('</header>', 1)[0]:
            anchor = '<div class="titleblock label"'
            if source.count(anchor) != 1:
                raise ValueError('Aula 08-revelia hero title block anchor is absent or duplicated')
            source = source.replace(anchor, HERO_START + _hero_block() + HERO_END + anchor, 1)
        else:
            in_hero = re.compile(r'<figure\b(?:(?!</figure>).)*?id="pci-a08r-filing-form"(?:(?!</figure>).)*?</figure>', re.S)
            source, count = in_hero.subn(HERO_START + _hero_block() + HERO_END, source, count=1)
            if count != 1:
                raise ValueError('could not refresh the hero form')

    bet = _replace_marked(source, BET_START, BET_END, _bet_block())
    if bet is not None:
        source = bet
    elif 'id="a08r-opening-bet"' not in source:
        anchor = '</header>'
        if anchor not in source:
            raise ValueError('hero closing header is absent for the opening bet')
        before, after = source.split(anchor, 1)
        source = before + anchor + BET_START + _bet_block() + BET_END + after
    else:
        raise ValueError('opening bet exists without the page-specific marker pair')

    timeline = _replace_marked(source, TIME_START, TIME_END, _timeline_block())
    if timeline is not None:
        source = timeline
        # The timeline belongs between prose sections, so lift it out of its former .wide wrapper.
        marked = re.compile(re.escape(TIME_START) + r'(.*?)' + re.escape(TIME_END) + r'\s*</div>', re.S)
        if marked.search(source):
            source = marked.sub('</div>' + TIME_START + r'\1' + TIME_END, source, count=1)
    else:
        old_timeline = re.compile(r'<figure\b(?:(?!</figure>).)*?id="pci-a08r-case-timeline"(?:(?!</figure>).)*?</figure>\s*</div>', re.S)
        source, count = old_timeline.subn('</div>' + TIME_START + _timeline_block() + TIME_END, source, count=1)
        if count != 1:
            raise ValueError('could not replace the existing case timeline')

    css = _replace_marked(source, STYLE_START, STYLE_END, _style_block())
    if css is not None:
        source = css
    else:
        anchor = '@media (max-width:560px) and (orientation:portrait)'
        if source.count(anchor) != 1:
            raise ValueError('Aula 08-revelia style insertion anchor is absent or duplicated')
        source = source.replace(anchor, STYLE_START + _style_block() + STYLE_END + anchor, 1)
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
    print(f'{PAGE}: 4.2 hero, bet, and 3 timeline panels installed; specimen: {int(specimen_after != specimen_before)} updated')
