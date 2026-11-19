"""tgc06_planta: the planta part cropped to what Aula 06 of Teoria Geral dos Contratos draws.

The shared planta canvas (1180x472) reserves a ghost band and exits this lesson does not use; drawn full width its
labels fall under 10.5 px at 1000x650. Cropping to the content box keeps the same marks and larger letters.
params: planta params plus crop = [x, y, w, h].
"""
from __future__ import annotations

import re

from . import planta


def build(p: dict) -> tuple[str, list[dict]]:
    q = dict(p)
    x, y, w, h = q.pop("crop", [100, 14, 1030, 372])
    svg, objs = planta.build(q)
    svg = re.sub(r'viewBox="[^"]*"', f'viewBox="{x} {y} {w} {h}"', svg, count=1)
    # badge digits: 11 px shrinks under 10.5 px at 1000x650; widen the badge a little and set the digits at 12.5
    svg = re.sub(r'(<a href="#[^"]*"><rect x=")([\d.]+)(" y="[\d.]+" width=")26(" height=")18(.*?<text x=")([\d.]+)(" y=")([\d.]+)(" font-size=")11"',
                 lambda m: f'{m[1]}{float(m[2])-3:g}{m[3]}32{m[4]}20{m[5]}{float(m[6])+0:g}{m[7]}{float(m[8])+1:g}{m[9]}12.5"', svg)
    return svg, objs
