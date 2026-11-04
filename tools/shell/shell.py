#!/usr/bin/env python3
"""The page shell: every reader page's locked frame, generated, so nobody (model or human) writes it again.

  python3 tools/shell/shell.py build            # render every source in tools/shell/src/ to its page
  python3 tools/shell/shell.py check            # fail if any page differs from its source + frame (a hand edit)

A source is `tools/shell/src/<site path>.html`: a front-matter comment, then the page's free part (its own <style>,
its content, its own <script>). The frame (head, fonts and house stylesheets, the paper-and-grid background, the top
bar with the night toggle, the reader scripts the offline build would inject) comes from here and nowhere else.

    <!--shell
    course: processo-civil-i
    title: Porquês · amostra para a Aula 01
    bar: Amostra · Aula 01 · Petição inicial, demanda e emenda
    -->
    <style>…</style>
    <div class="wrap">…</div>
    <script>…</script>

Locked: everything this file writes. Free: everything in the source. Dials live in the source as CSS custom
properties of the house (`--col`, accents), within the ranges in the workshop's HOUSE.md.
"""
import html, re, sys
from html.parser import HTMLParser
from pathlib import Path

R = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parent / 'src'
COURSE_NAMES = {'processo-civil-i': 'Processo Civil I-a'}


def meta_of(text):
    m = re.match(r'\s*<!--shell\n(.*?)\n-->\n', text, re.S)
    if not m:
        raise SystemExit('source lacks a <!--shell … --> header')
    meta = dict(l.split(':', 1) for l in m.group(1).splitlines() if ':' in l)
    return {k.strip(): v.strip() for k, v in meta.items()}, text[m.end():]


# ── The instrument gate (chairman 03/11: "I don't like it when you make visual things that are not instruments").
# Every visual (figure, svg, canvas, stage, illustration) must say, in data-does, what the READER does and what the
# page answers: "verbo · o leitor <ação> → <o que a página responde>". Scrolling, looking and reading are not
# reader actions: a picture that only plays while you scroll is narration, not an instrument.
VISUAL = re.compile(r'^(figure|svg|canvas)$')
DOES = re.compile(r'^\s*\S+ · o leitor (?P<act>.+?) → (?P<ans>.{8,})$')
PASSIVE = re.compile(r'\b(rola|rolar|desce|descer|olha|olhar|v[eê]|ver|l[eê]|ler|assiste|assistir|scroll)\b', re.I)


class _Gate(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack, self.bad, self.n = [], [], 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        visual = bool(VISUAL.match(tag)) or 'stage' in (a.get('class') or '').split()
        covered = any(self.stack)
        if visual and not covered:
            self.n += 1
            m = DOES.match(a.get('data-does') or '')
            line = self.getpos()[0]
            if not m:
                self.bad.append(f'line {line}: <{tag}> has no data-does "verbo · o leitor <ação> → <resposta>"')
            elif PASSIVE.search(m.group('act')):
                self.bad.append(f'line {line}: <{tag}> data-does names a passive action ({m.group("act")!r}): not an instrument')
        if tag not in ('br', 'img', 'input', 'meta', 'link', 'hr', 'wbr', 'source'):
            self.stack.append(visual)
    def handle_startendtag(self, tag, attrs):   # <rect/>, <path/>: nothing to push or pop
        pass
    def handle_endtag(self, tag):
        if self.stack: self.stack.pop()


def gate(free: str):
    g = _Gate(); g.feed(free); return g.n, g.bad


PART = re.compile(r'<!--part (\w+) (\{.*?\})-->', re.S)


def cast_parts(free: str) -> str:
    """<!--part autos {params}--> becomes the house part's drawing: positions, counts and numbers are computed."""
    import json
    sys.path.insert(0, str(R))
    from tools.figkit.parts import PARTS
    return PART.sub(lambda m: PARTS[m.group(1)](json.loads(m.group(2)))[0], free)


def render(src: Path) -> tuple[Path, str]:
    meta, free = meta_of(src.read_text(encoding='utf-8'))
    if re.search(r'<svg\b', free):
        raise SystemExit(f'drawing gate: {src.relative_to(SRC)} hand-types an <svg>; cast a part instead (<!--part NAME {{params}}-->, tools/figkit/parts)')
    free = cast_parts(free)
    n, bad = gate(free)
    if bad:
        raise SystemExit(f'instrument gate: {src.relative_to(SRC)}\n  ' + '\n  '.join(bad))
    rel = src.relative_to(SRC)
    up = '../' * (len(rel.parts) - 1)
    course = meta['course']
    cdir = f'{up}courses/{course}'
    e = lambda s: html.escape(s, quote=False)
    page = f'''<!doctype html>
<html lang="pt-BR">
<head>
<script src="{up}assets/turn.js"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(meta['title'])}</title>
<link rel="stylesheet" href="{cdir}/assets/curso.css">
<link rel="stylesheet" href="{up}assets/casa.css">
<script src="{cdir}/assets/curso.js"></script>
<script src="{up}assets/casa.js" defer></script>
</head>
<body>
<nav class="topbar"><a href="{cdir}/index.html">← {e(COURSE_NAMES.get(course, course))}</a><span>{e(meta['bar'])}</span><button class="theme-toggle" type="button" aria-pressed="false" title="Alternar modo noite"><span class="tt-track" aria-hidden="true"><span class="tt-knob"></span></span><span class="tt-label">Modo noite</span></button></nav>
{free.strip()}
<script src="{up}assets/offline.js" defer></script>
<script src="{up}assets/highlight.js" defer></script>
<script src="{up}assets/highlight-panel.js" defer></script>
</body>
</html>
'''
    return R / rel, page


def main(cmd):
    bad = 0
    srcs = sorted(SRC.rglob('*.html'))
    for s in srcs:
        out, page = render(s)
        if cmd == 'build':
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page, encoding='utf-8')
        elif not out.is_file() or out.read_text(encoding='utf-8') != page:
            print(f'FAIL shell: {out.relative_to(R)} differs from tools/shell/src/{s.relative_to(SRC)} + frame (edit the source, then build)')
            bad += 1
    print(f'shell: {len(srcs)} page(s) {"built" if cmd == "build" else "checked"}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'check'))
