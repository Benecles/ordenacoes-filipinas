#!/usr/bin/env python3
"""Modo avião build step. Run from the repo root after changing any page:

    python3 tools/offline_build.py

1. Adds the offline.js and highlight.js <script defer> tags to every HTML page that lacks them, and turn.js in <head>.
2. Writes offline-manifest.json: every public file, plus directory URLs for index pages,
   and a content hash as the version (so saved copies refresh when the site changes).
"""
import hashlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sanitize
sanitize.run()   # no visible sourcing, whatever generated the page
import landscape
landscape.run()   # a sideways phone gets the desktop layout: narrow rules also require portrait
import assetver
assetver.run()   # course CSS/JS links carry a hash of the file, so edits reach cached phones

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEEP = ('.html', '.css', '.js', '.json', '.svg', '.ico', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.woff', '.woff2')
SKIP_DIRS = {'.git', 'tools', 'node_modules', '.claude', 'offline'}  # offline/: deploy-built packs
SKIP_FILES = {'offline-size.json', 'offline-manifest.json', 'sw.js'}

# Retired prototypes and alternate homepages kept for the design archive (Issue #80).
# Readers in modo avião do not need to download these (~240 KB).
# Inactive Processo aliases remain as redirects on the web but are not offline content.
OFFLINE_EXCLUDED_ROUTES = {
    'courses/processo-civil-i/aula-05-casos.html',
    'courses/processo-civil-i/aula-07-preclusao.html',
}

ARCHIVE_PAGES = {
    'index-alt-a.html',
    'index-alt-b.html',
    'index-alt-c.html',
    'index-before-folio.html',
    'prototype-folio.html',
    'a-terra-muda-de-dono.html',
    'bifurcacao-constitucional.html',
    'dossie-do-delito.html',
    'glossario-ancorado.html',
}

def public_files():
    out = []
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.startswith('.')]
        for f in files:
            if f.startswith('.') or f in SKIP_FILES or not f.lower().endswith(KEEP):
                continue
            rel = os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, '/')
            if rel in ARCHIVE_PAGES or rel in OFFLINE_EXCLUDED_ROUTES:
                continue
            out.append(rel)
    return sorted(out)

SCRIPTS = ('assets/offline.js', 'assets/highlight.js', 'assets/highlight-panel.js')

HEAD_SCRIPT = 'assets/turn.js'   # the turn (reader <-> backstage) must run in <head> so an arriving page can join it

def add_script(path):
    full = os.path.join(ROOT, path)
    s = open(full, encoding='utf-8').read()
    if '</body>' not in s:
        return False
    depth = path.count('/')
    head = False
    if HEAD_SCRIPT not in s and re.search(r'<head[^>]*>', s):
        s = re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + f'\n<script src="{"../" * depth}{HEAD_SCRIPT}"></script>', s, count=1)
        head = True
    missing = [x for x in SCRIPTS if x not in s]
    if not missing:
        if head:
            open(full, 'w', encoding='utf-8').write(s)
        return head
    tags = ''.join(f'<script src="{"../" * depth}{x}" defer></script>\n' for x in missing)
    s = s.replace('</body>', tags + '</body>', 1)
    open(full, 'w', encoding='utf-8').write(s)
    return True

files = public_files()
added = [p for p in files if p.endswith('.html') and add_script(p)]
# Reader pages first, the backstage last: the service worker reports "ready to read" once the reader half is saved
# (16/10). Each file carries a content hash so an update copies unchanged files from the saved copy.
def backstage(p): return p.startswith(('backstage/', 'assets/backstage/', 'experiments/', 'specimen/'))
files = sorted(files, key=lambda p: (backstage(p), p))
h = hashlib.sha1()
entries, hashes = [], {}
reader = 0
for p in files:
    data = open(os.path.join(ROOT, p), 'rb').read()
    h.update(p.encode()); h.update(data)
    fh = hashlib.sha1(data).hexdigest()[:10]
    entries.append(p); hashes[p] = fh
    if p == 'index.html' or p.endswith('/index.html'):
        d = p[:-len('index.html')] or './'
        entries.append(d); hashes[d] = fh
    if not backstage(p): reader = len(entries)
size = sum(os.path.getsize(os.path.join(ROOT, p)) for p in files)
man = {'version': h.hexdigest()[:12], 'bytes': size, 'reader': reader, 'files': entries, 'hash': hashes}
json.dump(man, open(os.path.join(ROOT, 'offline-manifest.json'), 'w'), indent=0, separators=(',', ':'))
# what the airplane popup says before you press it: the real size, rewritten on every build (16/10: it said 8 MB at 50)
# ...and what it rotates through while saving: facts counted from the site itself, plus a few hints (16/10)
def _facts():
    lessons, words, figs, blocks, courses, longest = 0, 0, 0, 0, set(), (0, '')
    for p in files:
        if not re.match(r'courses/[^/]+/(aula|unidade)-[^/]+\.html$', p): continue
        t = open(os.path.join(ROOT, p), encoding='utf-8', errors='replace').read()
        if 'http-equiv="refresh"' in t[:3000]: continue
        body = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', t)
        n = len(re.sub(r'<[^>]+>', ' ', re.sub(r'(?is)<svg\b.*?</svg>', ' ', body)).split())
        lessons += 1; words += n; courses.add(p.split('/')[1])
        # a drawing, not an icon: a visible svg with real content in it
        figs += sum(1 for m in re.finditer(r'(?is)<svg\b([^>]*)>(.*?)</svg>', body) if 'width="0"' not in m.group(1) and len(m.group(2)) > 1500)
        blocks += len(re.findall(r'class="fonte\b', t))
        if n > longest[0]:
            m = re.search(r'<title>([^<·]+)', t); longest = (n, (m.group(1).strip() if m else p))
    hours = round(words / 230 / 60)
    return [
        f'{lessons} aulas em {len(courses)} disciplinas: cerca de {hours} horas de leitura.',
        f'{figs} desenhos, todos feitos em código, nenhum de banco de imagens.',
        f'{blocks} trechos de livros, leis e decisões, citados palavra por palavra.',
        f'A aula mais longa tem {longest[0]:,} palavras: {longest[1]}.'.replace(',', '.'),
        f'O site inteiro pesa {round(size / 1e6)} MB: cabe em {-(-size // 1_440_000)} disquetes.',
        'Toda página tem um verso. Procure um canto que dobra.',
        '⌘⇧K vira a página.',
        'Na página inicial, quatro quadradinhos do quadriculado guardam um segredo.',
        'Marque um trecho com o marca-texto: ele aparece no Meu caderno.',
        'Alguns desenhos fazem o que a coisa desenhada faz. Passe o mouse.',
    ]
json.dump({'mb': round(size / 1e6), 'files': len(files), 'facts': _facts()}, open(os.path.join(ROOT, 'offline-size.json'), 'w'), ensure_ascii=False)
print(f'offline: {len(files)} files, {size/1e6:.1f} MB, version {man["version"]}; script added to {len(added)} pages')
