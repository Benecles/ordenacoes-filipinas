"""tgc08_planta: the planta part cropped to the content box of Aula 08 (Cessão da posição contratual).

The shared planta canvas has room for a ghost band and exits this lesson does not use; drawn full width its labels
shrink. The same drawing is cropped to its content, so labels keep their size.
params: planta params plus crop = [x, y, w, h].
"""
from __future__ import annotations

import re

from . import planta


def build(p: dict) -> tuple[str, list[dict]]:
    q = dict(p)
    x, y, w, h = q.pop("crop", [40, 60, 900, 390])
    svg, objs = planta.build(q)
    svg = re.sub(r'viewBox="[^"]*"', f'viewBox="{x} {y} {w} {h}"', svg, count=1)
    # the smallest planta labels (11 to 12 px) read under 10.5 px at 1000 px wide: lift them one step
    bump = {"11": "12.5", "11.5": "12.5", "12": "13", "12.5": "13"}
    svg = re.sub(r'font-size="([\d.]+)"', lambda m: f'font-size="{bump.get(m.group(1), m.group(1))}"', svg)
    # the origin's caption sits beside the thread spine, not across it
    svg = re.sub(r'<text x="([\d.]+)"([^>]*?) text-anchor="middle">(cedente e cedido)</text>',
                 lambda m: f'<text x="{float(m.group(1)) + 18:g}"{m.group(2)} text-anchor="start">{m.group(3)}</text>', svg)
    return svg, objs
