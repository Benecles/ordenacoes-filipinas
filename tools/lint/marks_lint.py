#!/usr/bin/env python3
"""CASA-1 marks linter: enforces Writing Standard C10b/D8 on the raw HTML (slop_lint strips tags, so it can't).
  python3 protocols/tools/marks_lint.py PAGE.html [...]   exit 1 on any violation
Rules: <=1 .held and <=1 .limit per paragraph; each <=8 words; <=1 .mark per chapter; .term needs data-def;
no plain <strong>/<b> in running text (allowed: hero deck, .eixo/.fonte/.bet labels, table heads); no colour set inline on text spans."""
import re, sys, os

def words(s): return len(re.findall(r'\w+', re.sub(r'<[^>]+>', '', s), re.U))

def check(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    s = re.sub(r'(?is)<(script|style|svg|head)\b.*?</\1>', '', s)
    out = []
    def line(pos): return s.count('\n', 0, pos) + 1
    # per paragraph
    for pm in re.finditer(r'(?is)<p\b[^>]*>(.*?)</p>', s):
        body = pm.group(1)
        for cls, cap in (('held', 1), ('limit', 1)):
            hits = re.findall(r'(?is)<span class="%s">(.*?)</span>' % cls, body)
            if len(hits) > cap: out.append((line(pm.start()), f'{cls}-per-paragraph', f'{len(hits)} in one paragraph (max {cap})'))
            for h in hits:
                if words(h) > 8: out.append((line(pm.start()), f'{cls}-too-long', f'"{re.sub("<[^>]+>", "", h)[:60]}" is {words(h)} words (max 8)'))
    # per chapter
    parts = re.split(r'(?i)<section class="chapter"', s)
    pos = 0
    for part in parts:
        n = len(re.findall(r'class="mark"', part))
        if n > 1: out.append((line(pos), 'mark-per-chapter', f'{n} highlighter marks in one chapter (max 1)'))
        pos += len(part) + 24
    for m in re.finditer(r'(?is)<span class="term"(?![^>]*data-def)', s): out.append((line(m.start()), 'term-no-def', '.term without data-def'))
    for m in re.finditer(r'(?is)<aside class="fonte[^>]*>.*?</aside>', s):
        if 'class="mark"' in m.group(0): out.append((line(m.start()), 'mark-in-fonte', 'use .key inside source blocks'))
    # plain bold: strip allowed containers first
    t = s
    for opener, closer in ((r'<header\b', r'</header>'), (r'<p class="deck"', r'</p>'), (r'<p class="eixo"', r'</p>'), (r'<div class="bet"', r'</div></div>'),
                           (r'<aside class="fonte', r'</aside>'), (r'<div class="titleblock', r'</div></div>'), (r'<table\b', r'</table>'), (r'<summary\b', r'</summary>'), (r'<nav\b', r'</nav>')):
        t = re.sub(r'(?is)' + opener + r'.*?' + closer, lambda m: '#' * len(m.group(0)), t)
    for m in re.finditer(r'(?is)<(strong|b)\b(?![^>]*class="(?:held|limit|runin)")[^>]*>(?!\s*\w+(?: \w+){0,2}\.\s*</)', t):   # run-in labels like <strong>Tese.</strong> stay
        out.append((line(m.start()), 'plain-bold', 'plain bold retired; use .held/.limit, italics or nothing'))
    for m in re.finditer(r'(?is)<span[^>]*style="[^"]*\bcolor\s*:', s): out.append((line(m.start()), 'inline-colour', 'colour comes from .held/.limit only'))
    return sorted(out)

if __name__ == '__main__':
    bad = 0
    for p in sys.argv[1:]:
        r = check(p)
        print(('FAIL' if r else 'PASS'), p, f'({len(r)} findings)')
        for ln, rule, msg in r: print(f'  line {ln} {rule}: {msg}')
        bad += bool(r)
    sys.exit(1 if bad else 0)
