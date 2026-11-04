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


# ── Floors a script can see (Aula 01 audit, 03/11): each was a written rule the hand-built page broke because nothing
# ran it. Every page: no hex colours, no plain bold, square corners, cuts marked "[...]". Lessons (kind: lesson) also: 3–6 chapters,
# 2,500–4,500 words, ≤ 5 links to other lessons outside the end nav, every chapter lede a question,
# no signposting ("esta aula responde…", "em quatro passos").
def lints(free: str, kind: str) -> list[str]:
    bad = []
    body = re.sub(r'(?is)<script\b.*?</script>', ' ', free)
    css_svg = re.findall(r'(?is)<style\b.*?</style>|<svg\b.*?</svg>|style="[^"]*"', body)
    for blob in css_svg:
        for hx in re.findall(r'#[0-9a-fA-F]{3,8}\b', re.sub(r'/\*.*?\*/', '', blob, flags=re.S)):
            bad.append(f'hex colour {hx}: use a house token (var(--ink), var(--dif)…) so dark mode works'); break
    if re.search(r'<(b|strong)>', body):
        bad.append('plain bold <b>/<strong> in running text: use .held, .limit or .runin')
    for r in re.findall(r'border-radius\s*:\s*([^;}"]+)', ' '.join(css_svg)):
        if r.strip() not in ('0', '0px', '50%'):
            bad.append(f'border-radius {r.strip()}: house paper objects have square corners (50% only for a dot)'); break
    if '[…]' in body:
        bad.append('cut marked "[…]": the house mark is "[...]"')
    if kind == 'lesson':
        text = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'(?is)<(style|svg|figure|nav)\b.*?</\1>', ' ', body)))
        words = len(text.split())
        chapters = re.findall(r'(?is)<section\b[^>]*class="[^"]*\bchapter\b[^"]*"[^>]*>(.*?)</section>', body)
        if not 3 <= len(chapters) <= 6: bad.append(f'{len(chapters)} chapters (want 3–6)')
        if not 2500 <= words <= 4500: bad.append(f'{words} words (want 2,500–4,500; split where the question changes)')
        for i, ch in enumerate(chapters, 1):
            lede = re.search(r'(?is)<p\b[^>]*class="[^"]*\blede\b[^"]*"[^>]*>(.*?)</p>', ch)
            if not lede or not html.unescape(re.sub(r'<[^>]+>', '', lede.group(1))).strip().endswith('?'):
                bad.append(f'chapter {i}: the lede must state the chapter\'s question (end with "?")')
        sign = re.search(r'(?i)\b(esta aula (responde|mostra|explica|trata)|este capítulo (responde|mostra|explica|trata)|a seguir, |em (dois|três|quatro|cinco|seis) passos|vamos ver (agora|a seguir))\b', text)
        if sign: bad.append(f'signpost "{sign.group(0)}": do the move instead of announcing it')
        links = re.findall(r'href="(aula-[^"#]+)', re.sub(r'(?is)<nav class="endnav".*?</nav>', '', body))
        if len(links) > 5: bad.append(f'{len(links)} links to other lessons (want ≤ 5)')
    return bad


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
    bad += lints(free, meta.get('kind', 'page'))
    if bad:
        raise SystemExit(f'shell gate: {src.relative_to(SRC)}\n  ' + '\n  '.join(bad))
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
