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
SKIP_DIRS = {'.git', 'tools', 'node_modules', '.claude'}
SKIP_FILES = {'offline-manifest.json', 'sw.js'}

# Retired prototypes and alternate homepages kept for the design archive (Issue #80).
# Readers in modo avião do not need to download these (~240 KB).
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
            if rel in ARCHIVE_PAGES:
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
h = hashlib.sha1()
entries = []
for p in files:
    h.update(p.encode()); h.update(open(os.path.join(ROOT, p), 'rb').read())
    entries.append(p)
    if p == 'index.html' or p.endswith('/index.html'):
        entries.append(p[:-len('index.html')] or './')
man = {'version': h.hexdigest()[:12], 'files': entries}
json.dump(man, open(os.path.join(ROOT, 'offline-manifest.json'), 'w'), indent=0)
size = sum(os.path.getsize(os.path.join(ROOT, p)) for p in files)
print(f'offline: {len(files)} files, {size/1e6:.1f} MB, version {man["version"]}; script added to {len(added)} pages')
