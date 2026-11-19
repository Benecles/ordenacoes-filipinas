"""tgc07_planta: the planta part cropped to what Aula 07 of Teoria Geral dos Contratos draws.

The shared planta canvas is 1180x472 with room for a ghost band and exits this lesson does not use; drawn full width
its labels shrink under 10 px at 1000x650. The same drawing is cropped to its content box, so labels keep their size.
params: planta params plus crop = [x, y, w, h].
"""
from __future__ import annotations

import re

from . import planta


def build(p: dict) -> tuple[str, list[dict]]:
    q = dict(p)
    x, y, w, h = q.pop("crop", [40, 100, 1010, 350])
    svg, objs = planta.build(q)
    svg = re.sub(r'viewBox="[^"]*"', f'viewBox="{x} {y} {w} {h}"', svg, count=1)
    return svg, objs
