#!/usr/bin/env python3
"""Build assets/search-index.json across all courses for the global Cmd+K study palette.

Indexes:
  - Courses (title, slug, href)
  - Lessons (title, course, reading time, deck snippet, href)
  - Chapters (h2 heading, parent lesson, #anchor)
  - Legal glossary terms (<span class="term" data-def="...">, deduplicated with lesson link)
  - Statute articles & Súmulas cited in lesson headers/chapters (e.g., art. 421, CDC 26, Súmula 413)

Usage: python3 tools/build_search.py
"""
from __future__ import annotations
import html, json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSES_DIR = ROOT / 'courses'
OUT = ROOT / 'assets' / 'search-index.json'

COURSE_NAMES = {
    'teoria-geral-dos-contratos': 'Teoria Geral dos Contratos',
    'processo-civil-i': 'Processo Civil I',
    'metodologia-juridica': 'Metodologia Jurídica',
    'direito-constitucional-i': 'Direito Constitucional I',
    'controle-de-constitucionalidade': 'Controle de Constitucionalidade',
    'direito-latino-americano': 'Direito Latino-americano',
    'teoria-do-delito': 'Teoria do Delito',
}


def strip_tags(s: str) -> str:
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def fold(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFKD', s.lower()) if not unicodedata.combining(c))


def build() -> dict:
    items = []
    seen_terms = set()
    courses_meta = []

    for cdir in sorted(COURSES_DIR.iterdir()):
        if not cdir.is_dir():
            continue
        slug = cdir.name
        cname = COURSE_NAMES.get(slug, slug.replace('-', ' ').title())
        courses_meta.append({'s': slug, 'n': cname})
        idx = cdir / 'index.html'
        if idx.exists():
            items.append({
                'k': 'c',  # course
                'c': slug,
                't': cname,
                'd': 'Página principal do curso',
                'u': f'courses/{slug}/index.html',
            })

        for fp in sorted(cdir.glob('*.html')):
            if fp.name in ('index.html', 'artigos.html', 'cartoes.html'):
                continue
            raw = fp.read_text(encoding='utf-8', errors='ignore')
            # Skip redirect stubs
            if re.search(r'<meta[^>]+http-equiv=["\']?refresh', raw[:1200], re.I):
                continue
            rel = f'courses/{slug}/{fp.name}'
            h1_m = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', raw, re.I)
            title = strip_tags(h1_m.group(1)) if h1_m else fp.stem
            deck_m = re.search(r'<p[^>]+class="[^"]*\bdeck\b[^"]*"[^>]*>([\s\S]*?)</p>', raw, re.I)
            deck = strip_tags(deck_m.group(1))[:150] if deck_m else ''
            # Lesson number prefix if aula-NN
            num_m = re.match(r'aula-(\d\d)(?:-(.+))?\.html$', fp.name)
            label = f'Aula {num_m.group(1)} · {title}' if num_m and not num_m.group(2) else title
            if num_m and num_m.group(2):
                label = f'Aula {num_m.group(1)} (comp.) · {title}'
            elif fp.name.startswith('revisao'):
                label = f'Revisão · {title}'

            items.append({
                'k': 'l',  # lesson
                'c': slug,
                't': label,
                'd': deck,
                'u': rel,
            })

            # Chapters & h3 subheadings
            seen_ch = set()
            for ch_m in re.finditer(r'<section[^>]+id="([^"]+)"[^>]*>(?:(?!</section>).){0,600}?<h2[^>]*>([\s\S]*?)</h2>', raw, re.I | re.S):
                cid, ch_title = ch_m.group(1), strip_tags(ch_m.group(2))
                if not ch_title or cid in seen_ch or cid in ('bibliografia', 'exercicio'):
                    continue
                seen_ch.add(cid)
                items.append({
                    'k': 'h',  # chapter heading
                    'c': slug,
                    't': ch_title,
                    'd': label,
                    'u': f'{rel}#{cid}',
                })
            for h3_m in re.finditer(r'<h3[^>]*>([\s\S]*?)</h3>', raw, re.I):
                h3_title = strip_tags(h3_m.group(1))
                if not h3_title or len(h3_title) > 90:
                    continue
                pos = h3_m.start()
                sec_ids = re.findall(r'<section[^>]+id="([^"]+)"', raw[:pos])
                anchor = f'#{sec_ids[-1]}' if sec_ids else ''
                k3 = (anchor, fold(h3_title))
                if k3 in seen_ch:
                    continue
                seen_ch.add(k3)
                items.append({
                    'k': 'h',
                    'c': slug,
                    't': h3_title,
                    'd': label,
                    'u': f'{rel}{anchor}',
                })

            # Legal glossary terms (<span class="term" data-def="...">Term</span>)
            for tm in re.finditer(r'<span[^>]+class="[^"]*\bterm\b[^"]*"[^>]+data-def="([^"]+)"[^>]*>([\s\S]*?)</span>', raw, re.I):
                defn, term = html.unescape(tm.group(1)).strip(), strip_tags(tm.group(2))
                if not term or not defn or len(term) > 70:
                    continue
                key = (slug, fold(term))
                if key in seen_terms:
                    continue
                seen_terms.add(key)
                # Find nearest preceding section id
                pos = tm.start()
                sec_ids = re.findall(r'<section[^>]+id="([^"]+)"', raw[:pos])
                anchor = f'#{sec_ids[-1]}' if sec_ids else ''
                items.append({
                    'k': 't',  # term
                    'c': slug,
                    't': term,
                    'd': f'{defn[:150]} — {label}',
                    'u': f'{rel}{anchor}',
                })

            # Key statutes & Súmulas in .fonte footers (dedup per lesson)
            seen_art = set()
            for fm in re.finditer(r'<aside[^>]+class="[^"]*\bfonte\b[^"]*"[\s\S]*?<footer>([\s\S]*?)</footer>', raw, re.I):
                ftxt = strip_tags(fm.group(1))
                for am in re.finditer(r'\b(arts?\.\s*\d+(?:\.\d+)?(?:\s*[a–-]\s*\d+(?:\.\d+)?)?|Súmula\s+\d+|REsp\s+[\d\.]+(?:/[A-Z]{2})?|ADI\s+[\d\.]+|ADPF\s+[\d\.]+|RE\s+[\d\.]+)\b', ftxt):
                    cite = re.sub(r'\s+', ' ', am.group(1)).strip()
                    ckey = fold(cite)
                    if ckey in seen_art:
                        continue
                    seen_art.add(ckey)
                    pos = fm.start()
                    sec_ids = re.findall(r'<section[^>]+id="([^"]+)"', raw[:pos])
                    anchor = f'#{sec_ids[-1]}' if sec_ids else ''
                    items.append({
                        'k': 'a',  # article / decision
                        'c': slug,
                        't': cite,
                        'd': f'{ftxt[:110]} — {label}',
                        'u': f'{rel}{anchor}',
                    })

    data = {'courses': courses_meta, 'items': items}
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    counts = {k: sum(1 for x in items if x['k'] == k) for k in ('c', 'l', 'h', 't', 'a')}
    print(f'search-index: {len(items)} items ({counts}), {OUT.stat().st_size / 1024:.1f} KB -> {OUT.relative_to(ROOT)}')
    return data


if __name__ == '__main__':
    build()
