#!/usr/bin/env python3
"""Every local link resolves: the file exists and, when it names a #fragment, an element with that id is in it.
HOUSE T2.4 ("links and navigation work"). Added 17/11: a page merge left "aula-01.html#topica-ponte" pointing nowhere."""
import re, sys
from pathlib import Path
from urllib.parse import unquote

root = Path(__file__).resolve().parents[1]
ids_cache = {}


def ids(p):
    if p not in ids_cache:
        ids_cache[p] = set(re.findall(r'\bid="([^"]+)"', p.read_text(encoding='utf-8', errors='ignore')))
    return ids_cache[p]


bad = 0
pages = sorted((root / 'courses').rglob('*.html')) + [root / 'index.html']
for page in pages:
    html = page.read_text(encoding='utf-8', errors='ignore')
    for href in re.findall(r'<a\b[^>]*\bhref="([^"]+)"', html):
        if re.match(r'^(https?:|mailto:|javascript:|data:|//)', href) or "'+" in href:  # JS-built links aren't static
            continue
        path, _, frag = href.partition('#')
        target = page if not path else (page.parent / unquote(path.split('?')[0])).resolve()
        if target.is_dir():
            target = target / 'index.html'
        if target.suffix != '.html':
            continue
        rel = page.relative_to(root)
        if not target.exists():
            bad += 1; print(f'FAIL {rel}: link to missing page {href}'); continue
        if frag and frag not in ids(target):
            bad += 1; print(f'FAIL {rel}: link to missing anchor {href}')
print(f"anchors: {'FAIL' if bad else 'PASS'} ({len(pages)} pages, {bad} dead link(s))")
sys.exit(1 if bad else 0)
