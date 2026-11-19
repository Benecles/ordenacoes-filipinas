"""Conceito de contrato: the hero planta, cast from `planta` and cropped to its own width.

The course's through-line (a contract's life from contact to extinction) runs along the rail; three threads cross it.
Same params as `planta`; the part only narrows the canvas to `width` (default 990) so labels render at reading size
and enlarges the chapter badges. Nothing here asserts a quantity: positions order the phases, they do not time them.
"""
from __future__ import annotations
import re
from . import planta

def build(p: dict):
    svg, objs = planta.build(p)
    w = int(p.get("width", 990))
    svg = re.sub(r'viewBox="0 0 1180 (\d+)"', lambda m: f'viewBox="0 0 {w} {m.group(1)}"', svg, count=1)
    svg = re.sub(r'(<a href=.*?</a>)', lambda m: m.group(1).replace('font-size="11"', 'font-size="12.5"'), svg, flags=re.S)
    # notes sit to the right of their stem, so stems of lower rows never cross the notes above
    svg = re.sub(r'<text x="([\d.]+)"( y="[\d.]+" font-size="13.5")', lambda m: f'<text x="{float(m.group(1)) + 10:g}"{m.group(2)}', svg)
    # the origin's gloss would sit across the thread spine: set it to the left of the spine
    o = next((st for st in p["stations"] if st.get("kind") == "origin"), None)
    if o and o.get("art"):
        svg = re.sub(r'<text x="%g"([^>]*?) text-anchor="middle"([^>]*>%s</text>)' % (o["x"], re.escape(o["art"])),
                     lambda m: f'<text x="{o["x"] - 14}"{m.group(1)} text-anchor="end"{m.group(2)}', svg, count=1)
    return svg, objs
