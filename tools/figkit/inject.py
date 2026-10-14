"""Put kit figures into lesson pages: replace whole <svg> elements by id (or the page's opening
drawing, key 'hero'), leaving every other byte of the page untouched.

Run: python3 tools/figkit/inject.py        (then offline_build, polish capture/check, check_all)
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import controle_a01, controle_a02, controle_a03, controle_a11, controle_a12, controle_a14, controle_a16, controle_a07, controle_a27, delito_u01, delito_u04, delito_u05, contratos_a01, latam_a02, consti_a04, processo_a01, processo_a12_house, processo_a13, processo_a14, processo_a16, proc_a10

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')


def by_ids(*svgs):
    return {re.search(r'id="([^"]+)"', s).group(1): s for s in svgs}


PAGES = {
    'courses/controle-de-constitucionalidade/aula-01.html': {'hero': controle_a01.hero(), **by_ids(controle_a01.fig1(), controle_a01.fig2(), controle_a01.fig3())},
    'courses/controle-de-constitucionalidade/aula-07.html': by_ids(controle_a07.linha_temporal()),
    'courses/controle-de-constitucionalidade/aula-11.html': by_ids(*controle_a11.panels(), *controle_a11.fig1(), controle_a11.fig5(), controle_a11.fig2(), controle_a11.fig2_quem()),
    'courses/controle-de-constitucionalidade/aula-12.html': by_ids(*controle_a12.panels()),
    'courses/controle-de-constitucionalidade/aula-03.html': by_ids(*controle_a03.panels()),
    'courses/controle-de-constitucionalidade/aula-14.html': by_ids(*controle_a14.panels()),
    'courses/controle-de-constitucionalidade/aula-16.html': by_ids(*controle_a16.panels()),
    'courses/controle-de-constitucionalidade/aula-27.html': by_ids(*controle_a27.panels()),
    'courses/teoria-do-delito/unidade-01.html': by_ids(*delito_u01.panels()),
    'courses/teoria-do-delito/unidade-04.html': by_ids(*delito_u04.panels()),
    'courses/teoria-do-delito/unidade-05.html': by_ids(*delito_u05.panels()),
    'courses/teoria-geral-dos-contratos/aula-01.html': {**by_ids(*contratos_a01.panels1(), *contratos_a01.panels2(), *contratos_a01.panels3()), '__remove__': ['p-esp']},
    'courses/direito-latino-americano/aula-02.html': by_ids(*latam_a02.panels()),
    'courses/direito-constitucional-i/aula-04.html': by_ids(*consti_a04.panels()),
    'courses/processo-civil-i/aula-01.html': by_ids(processo_a01.panel()),
    'courses/processo-civil-i/aula-10.html': {
        'a10_hero': proc_a10.hero(),
        **by_ids(proc_a10.statute_panel()),
        '__optional__': ['pci-a10-art356'],  # the lesson author locates the new panel
    },
    'courses/processo-civil-i/aula-12.html': by_ids(*processo_a12_house.panels()),
    'courses/processo-civil-i/aula-16.html': {
        **by_ids(processo_a16.panel(), processo_a16.excerpt_panel()),
        '__optional__': ['pci-a16-excerpt'],  # inserted by the page author inside §07
    },
    'courses/processo-civil-i/aula-14.html': {
        **by_ids(processo_a14.panel(), processo_a14.docket_panel()),
        '__optional__': ['pci-a14-docket'],  # installed by the page author after panel integration
    },
}


def element_span(s, start):
    """[start, end) of the <svg> element opening at `start`, nested svgs included."""
    depth, i = 0, start
    for m in re.compile(r'<svg\b|</svg>').finditer(s, start):
        depth += 1 if m.group(0) == '<svg' else -1
        if depth == 0:
            return start, m.end()
    raise ValueError('unclosed svg')


def inject(path, repl):
    p = os.path.join(ROOT, path)
    s = open(p).read()
    replaced = 0
    for ident in repl.get('__remove__', []):
        m = re.search(rf'<svg\b[^>]*\bid="{re.escape(ident)}"', s)
        if not m:
            raise SystemExit(f'{path}: no <svg> for removal: {ident}')
        a, b = element_span(s, m.start())
        s = s[:a] + s[b:]
    for key, new in repl.items():
        if key.startswith('__'):
            continue
        if key == 'hero':
            m = re.search(r'<svg\b[^>]*class="hero-fork[^"]*"', s)
        elif key == 'a10_hero':
            container = re.search(r'<figure\b[^>]*class="hero-figure[^"]*"[^>]*>', s)
            m = re.compile(r'<svg\b').search(s, container.end()) if container else None
        else:
            m = re.search(rf'<svg\b[^>]*\bid="{re.escape(key)}"', s)
            if not m and key == 'tdl-u01-s7':
                m = re.search(r'<svg\b[^>]*\baria-label="O mesmo fato passa por recortes normativos diferentes e gera juízos provisórios diferentes"', s)
        if not m and key in repl.get('__optional__', []):
            continue
        if not m:
            raise SystemExit(f'{path}: no <svg> for {key}')
        a, b = element_span(s, m.start())
        s = s[:a] + new + s[b:]
        replaced += 1
    open(p, 'w').write(s)
    return replaced


if __name__ == '__main__':
    for path, repl in PAGES.items():
        print(f'{path}: {inject(path, repl)} figures')
