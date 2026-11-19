"""tgc09_planta: the planta part cropped to Aula 09's content (Revisão dos contratos).

Four threads need a lower note band than the shared canvas gives, so the notes start lower and the crop follows.
Small planta labels read under 10 px at 1000 px wide: lifted one step, as in tgc08_planta.
params: planta params plus crop = [x, y, w, h].
"""
from __future__ import annotations

import re

from . import planta


def build(p: dict) -> tuple[str, list[dict]]:
    q = dict(p)
    x, y, w, h = q.pop("crop", [0, 92, 1130, 420])
    old = planta.Y_NOTE
    planta.Y_NOTE = int(q.pop("note_y", 420))
    try:
        svg, objs = planta.build(q)
    finally:
        planta.Y_NOTE = old
    svg = re.sub(r'viewBox="[^"]*"', f'viewBox="{x} {y} {w} {h}"', svg, count=1)
    bump = {"11": "12.5", "11.5": "12.5", "12": "13", "12.5": "13", "13": "13.5"}
    svg = re.sub(r'font-size="([\d.]+)"', lambda m: f'font-size="{bump.get(m.group(1), m.group(1))}"', svg)
    return svg, objs
