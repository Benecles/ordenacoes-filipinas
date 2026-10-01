"""Put kit figures into lesson pages: replace whole <svg> elements by id (or the page's opening
drawing, key 'hero'), leaving every other byte of the page untouched.

Run: python3 tools/figkit/inject.py        (then offline_build, polish capture/check, check_all)
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import controle_a01, controle_a27, delito_u04, delito_u05, contratos_a01, latam_a02

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')


def by_ids(*svgs):
    return {re.search(r'id="([^"]+)"', s).group(1): s for s in svgs}


PAGES = {
    'courses/controle-de-constitucionalidade/aula-01.html': {'hero': controle_a01.hero(), **by_ids(controle_a01.fig1(), controle_a01.fig2(), controle_a01.fig3())},
    'courses/controle-de-constitucionalidade/aula-27.html': by_ids(*controle_a27.panels()),
    'courses/teoria-do-delito/unidade-04.html': by_ids(*delito_u04.panels()),
    'courses/teoria-do-delito/unidade-05.html': by_ids(*delito_u05.panels()),
    'courses/teoria-geral-dos-contratos/aula-01.html': {'hero': '', **by_ids(*contratos_a01.panels1(), *contratos_a01.panels2(), *contratos_a01.panels3())},
    'courses/direito-latino-americano/aula-02.html': by_ids(*latam_a02.panels()),
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
    for key, new in repl.items():
        if key == 'hero':
            m = re.search(r'<svg\b[^>]*class="hero-fork[^"]*"', s)
        else:
            m = re.search(rf'<svg\b[^>]*\bid="{re.escape(key)}"', s)
        if not m:
            raise SystemExit(f'{path}: no <svg> for {key}')
        a, b = element_span(s, m.start())
        s = s[:a] + new + s[b:]
    open(p, 'w').write(s)
    return len(repl)


if __name__ == '__main__':
    for path, repl in PAGES.items():
        print(f'{path}: {inject(path, repl)} figures')
