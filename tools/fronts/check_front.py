#!/usr/bin/env python3
"""usage: check_front.py <course-slug>... Checks rendered fronts and lesson registers."""
import html, json, os, re, sys, glob
SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'courses')

# C2 of work/pipeline/processo-civil-i/course-blueprint.md. Keeping this sequence
# in the blocking check makes the reader-facing study positions independent of
# URL numbers and prevents page reordering from silently changing the register.
PROCESSO_STUDY_ORDER = [
    'aula-01.html', 'aula-02.html', 'aula-03.html', 'aula-04.html',
    'aula-12.html', 'aula-05.html', 'aula-06-citacao.html', 'aula-06.html',
    'aula-07.html', 'aula-08.html', 'aula-08-revelia.html', 'aula-09.html',
    'aula-13.html', 'aula-10-estabilizacao.html', 'aula-10.html', 'aula-11.html',
    'aula-11-merito.html', 'aula-14.html', 'aula-15.html', 'aula-16.html',
    'aula-17.html', 'aula-18.html',
]
def txt(s): return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', s)).split())
bad = 0
for slug in sys.argv[1:]:
    d = os.path.join(SITE, slug); b = open(os.path.join(d, 'index.html'), encoding='utf-8').read()
    dj = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', slug + '.json')
    data = json.load(open(dj, encoding='utf-8')) if os.path.exists(dj) else {}
    register_lessons = [l for u in data.get('units', []) for l in u.get('lessons', [])]
    if slug == 'processo-civil-i':
        actual_order = [l.get('href') for l in register_lessons]
        if actual_order != PROCESSO_STUDY_ORDER:
            print(f'FAIL {slug}: register order differs from course blueprint C2')
            bad += 1
    order = ['class="front-title', 'class="front-drawing', 'class="front-exam', 'class="front-lessons'] + (['id="bibliografia"'] if 'id="bibliografia"' in b else [])
    pos = [b.find(m) for m in order]
    need = [p for m, p in zip(order, pos) if m not in ('class="front-drawing', 'class="front-exam')]   # drawing and exam card are optional
    have = [p for p in pos if p != -1]
    if -1 in need or have != sorted(have): print(f'FAIL {slug}: macro-order/markers', dict(zip(order, pos))); bad += 1
    if b.count('id="bibliografia"') > 1: print(f'FAIL {slug}: bibliografia count'); bad += 1
    if 'href="#bibliografia"' in b and 'id="bibliografia"' not in b: print(f'FAIL {slug}: link to missing bibliografia'); bad += 1
    end = b.find('id="bibliografia"'); lessons = b[b.find('class="front-lessons'):end if end > 0 else len(b)]
    linked = set()
    by_href = {l.get('href'): l for l in register_lessons}
    for href, inner in re.findall(r'<a\b[^>]*href="([^"#?]+\.html)"[^>]*>(.*?)</a>', lessons, re.S):
        p = os.path.normpath(os.path.join(d, href)); linked.add(p)
        if not os.path.exists(p): print(f'FAIL {slug}: dead link {href}'); bad += 1; continue
        page_html = open(p, encoding='utf-8').read()
        h1 = re.search(r'<h1\b[^>]*>(.*?)</h1>', page_html, re.S)
        t, h = txt(inner), txt(h1.group(1)) if h1 else ''
        if h and h.lower() not in t.lower(): print(f'WARN {slug}: {href} link "{t[:70]}" vs h1 "{h[:70]}"')
        if slug == 'processo-civil-i' and href in by_href:
            lesson = by_href[href]
            expected_number = f'{PROCESSO_STUDY_ORDER.index(href) + 1:02d}'
            expected_label = f'Aula {expected_number}'
            if lesson.get('label') != expected_label:
                print(f'FAIL {slug}: {href} front label {lesson.get("label")!r} != {expected_label!r}')
                bad += 1
            if h and txt(lesson.get('title', '')) != h:
                print(f'FAIL {slug}: {href} front title {lesson.get("title")!r} != page H1 {h!r}')
                bad += 1
            titleblock = re.search(r'<div class="titleblock label"[^>]*>(.*?)</header>', page_html, re.S)
            position = re.search(r'<div role="listitem">(?:Posição|Aula)\s*<b>(.*?)</b>', titleblock.group(1), re.S) if titleblock else None
            hero_label = re.search(r'\bAula\s*(\d{1,2})\b', txt(position.group(1))) if position else None
            if not hero_label or hero_label.group(1).zfill(2) != expected_number:
                found = f'Aula {hero_label.group(1).zfill(2)}' if hero_label else 'missing'
                print(f'FAIL {slug}: {href} hero label {found} != {expected_label}')
                bad += 1
            rendered_row = re.search(r'<a class="reg-row"[^>]*href="' + re.escape(href) + r'"[^>]*>(.*?)</a>', lessons, re.S)
            if rendered_row:
                number = re.search(r'<span class="reg-n">(.*?)</span>', rendered_row.group(1), re.S)
                reg_title = re.search(r'<span class="reg-t">(.*?)</span>', rendered_row.group(1), re.S)
                if not number or txt(number.group(1)) != expected_number:
                    print(f'FAIL {slug}: {href} rendered register label differs from {expected_label}')
                    bad += 1
                if not reg_title or txt(reg_title.group(1)) != h:
                    print(f'FAIL {slug}: {href} rendered register title differs from page H1')
                    bad += 1
    pages = {os.path.normpath(p) for p in glob.glob(d + '/*.html') if not p.endswith('index.html') and not os.path.basename(p).startswith(('cartoes', 'revis'))}
    skip = {os.path.normpath(os.path.join(d, x['page'])) for x in data.get('excluded_pages', [])}
    for p in sorted(pages - linked - skip): print(f'FAIL {slug}: lesson page not linked from grid and not in data excluded_pages: {os.path.basename(p)}'); bad += 1
    print(f'{slug}: {len(linked)} lesson links checked')
sys.exit(1 if bad else 0)
