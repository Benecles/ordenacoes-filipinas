#!/usr/bin/env python3
"""Modo avião packs (16/10). Deploy step only; the packs never enter git.

    python3 tools/offline_build.py && python3 tools/offline_packs.py OUTDIR

Bundles the files in offline-manifest.json into a few dozen packs so a reader saving the site makes ~40 requests
instead of ~1,300: text files go into JSON packs (GitHub Pages gzips them), images into binary packs with an index.
Packs are grouped by folder (a course, a backstage archive) and capped near 4 MB, and named by content hash, so an
update touches only the packs whose files changed. Writes OUTDIR/offline/*.json|bin and adds `packs` to
OUTDIR/offline-manifest.json; the service worker falls back to single files when a manifest has no packs.
"""
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else ROOT
TEXT = ('.html', '.css', '.js', '.json', '.svg')
CAP = 4_000_000
man = json.load(open(os.path.join(ROOT, 'offline-manifest.json')))


def real(p):
    return 'index.html' if p == './' else (p + 'index.html' if p.endswith('/') else p)


def group(p):
    parts = real(p).split('/')
    return '/'.join(parts[:3] if parts[0] == 'assets' and len(parts) > 3 else parts[:2]) if len(parts) > 1 else 'root'


groups = {}
for p in man['files']:
    kind = 'text' if real(p).lower().endswith(TEXT) else 'bin'
    groups.setdefault((group(p), kind), []).append(p)

os.makedirs(os.path.join(OUT, 'offline'), exist_ok=True)
packs = []
for (g, kind), files in sorted(groups.items()):
    chunk, size = [], 0
    def flush():
        global chunk, size
        if not chunk: return
        if kind == 'text':
            body = json.dumps({p: open(os.path.join(ROOT, real(p)), encoding='utf-8').read() for p in chunk},
                              ensure_ascii=False, separators=(',', ':')).encode()
            index = None
        else:
            blobs, index, off = [], [], 0
            for p in chunk:
                b = open(os.path.join(ROOT, real(p)), 'rb').read(); blobs.append(b); index.append([p, off, len(b)]); off += len(b)
            body = b''.join(blobs)
        name = f"offline/{g.replace('/', '-')}-{hashlib.sha1(body).hexdigest()[:10]}.{'json' if kind == 'text' else 'bin'}"
        open(os.path.join(OUT, name), 'wb').write(body)
        packs.append({'u': name, 'kind': kind, 'files': list(chunk), **({'index': index} if index else {})})
        chunk, size = [], 0
    for p in files:
        n = os.path.getsize(os.path.join(ROOT, real(p)))
        if chunk and size + n > CAP: flush()
        chunk.append(p); size += n
    flush()

# reader packs first, like the files
reader = set(man['files'][:man.get('reader', len(man['files']))])
packs.sort(key=lambda k: not any(f in reader for f in k['files']))
man['packs'] = packs
json.dump(man, open(os.path.join(OUT, 'offline-manifest.json'), 'w'), separators=(',', ':'))
print(f"offline packs: {len(packs)} packs for {len(man['files'])} files, "
      f"{sum(os.path.getsize(os.path.join(OUT, k['u'])) for k in packs) / 1e6:.1f} MB")
