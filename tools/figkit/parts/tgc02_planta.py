"""tgc02_planta: the planta part cropped to what Aula 02 of Teoria Geral dos Contratos draws.

Three stations, three threads and no ghost band or exits: the shared 1180x472 canvas drawn whole leaves labels under
11 px at 1000x650, so the same drawing is cropped to its content box and labels keep their size.
params: planta params plus crop = [x, y, w, h].
"""
from __future__ import annotations

import re

from . import planta


def build(p: dict) -> tuple[str, list[dict]]:
    q = dict(p)
    x, y, w, h = q.pop("crop", [50, 104, 1083, 340])
    svg, objs = planta.build(q)
    svg = re.sub(r'viewBox="[^"]*"', f'viewBox="{x} {y} {w} {h}"', svg, count=1)
    # the cropped plate scales to ~0.85 at 1000x650: nothing may be set under 13 units, or it renders under 11 px
    svg = re.sub(r'font-size="(1[12](?:\.5)?)"', '*SIZE*', svg)
    svg = svg.replace('*SIZE*', 'font-size="13"')
    return svg, objs
