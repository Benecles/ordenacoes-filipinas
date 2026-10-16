"""Inline instruments for Direito Constitucional I's text-only lessons: each module gives block() (a
<figure class="instr" id=…>) and ANCHOR = (page, a sentence in the paragraph the figure follows[, a closing tag such as '</ol>' to follow instead]).
Idempotent: a figure already on the page is replaced in place, never duplicated. Run, then offline_build.
usage: python3 tools/figkit/consti_inline.py
"""
import importlib, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
MODULES = ['consti_a07', 'consti_a06', 'consti_a09', 'consti_a10', 'consti_a11']

for name in MODULES:
    m = importlib.import_module(name)
    page, anchor, *after = m.ANCHOR   # optional third item: insert after this closing tag (e.g. a list) instead of </p>
    p = os.path.join(ROOT, page); s = open(p).read(); b = m.block()
    fid = re.search(r'<figure class="instr" id="([^"]+)"', b).group(1)
    old = re.search(rf'<figure class="instr" id="{re.escape(fid)}">.*?</figure>', s, re.S)
    if old:
        s = s[:old.start()] + b + s[old.end():]
    else:
        i = s.find(anchor)
        if i < 0: raise SystemExit(f'{name}: anchor not found in {page}')
        end = after[0] if after else '</p>'; j = s.find(end, i) + len(end)
        s = s[:j] + b + s[j:]
    open(p, 'w').write(s); print(name, '→', page, 'replaced' if old else 'inserted')
