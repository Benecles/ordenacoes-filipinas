#!/usr/bin/env python3
"""usage: check_front.py <course-slug>...  Checks a rendered front in site/courses/<slug>/index.html.
FAIL: macro-order wrong, dead lesson link, a lesson page not linked, bibliografia missing. WARN: link text vs lesson <h1> mismatch."""
import html, json, os, re, sys, glob
SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'courses')
def txt(s): return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', s)).split())
bad = 0
for slug in sys.argv[1:]:
    d = os.path.join(SITE, slug); b = open(os.path.join(d, 'index.html'), encoding='utf-8').read()
    order = ['class="front-title', 'class="front-drawing', 'class="front-exam', 'class="front-lessons'] + (['id="bibliografia"'] if 'id="bibliografia"' in b else [])
    pos = [b.find(m) for m in order]
    need = [p for m, p in zip(order, pos) if m not in ('class="front-drawing', 'class="front-exam')]   # drawing and exam card are optional
    have = [p for p in pos if p != -1]
    if -1 in need or have != sorted(have): print(f'FAIL {slug}: macro-order/markers', dict(zip(order, pos))); bad += 1
    if b.count('id="bibliografia"') > 1: print(f'FAIL {slug}: bibliografia count'); bad += 1
    if 'href="#bibliografia"' in b and 'id="bibliografia"' not in b: print(f'FAIL {slug}: link to missing bibliografia'); bad += 1
    end = b.find('id="bibliografia"'); lessons = b[b.find('class="front-lessons'):end if end > 0 else len(b)]
    linked = set()
    for href, inner in re.findall(r'<a\b[^>]*href="([^"#?]+\.html)"[^>]*>(.*?)</a>', lessons, re.S):
        p = os.path.normpath(os.path.join(d, href)); linked.add(p)
        if not os.path.exists(p): print(f'FAIL {slug}: dead link {href}'); bad += 1; continue
        h1 = re.search(r'<h1\b[^>]*>(.*?)</h1>', open(p, encoding='utf-8').read(), re.S)
        t, h = txt(inner), txt(h1.group(1)) if h1 else ''
        if h and h.lower() not in t.lower(): print(f'WARN {slug}: {href} link "{t[:70]}" vs h1 "{h[:70]}"')
    pages = {os.path.normpath(p) for p in glob.glob(d + '/*.html') if not p.endswith('index.html') and not os.path.basename(p).startswith(('cartoes', 'revis'))}
    dj = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', slug + '.json')
    skip = {os.path.normpath(os.path.join(d, x['page'])) for x in (json.load(open(dj)).get('excluded_pages', []) if os.path.exists(dj) else [])}
    for p in sorted(pages - linked - skip): print(f'FAIL {slug}: lesson page not linked from grid and not in data excluded_pages: {os.path.basename(p)}'); bad += 1
    print(f'{slug}: {len(linked)} lesson links checked')
sys.exit(1 if bad else 0)
