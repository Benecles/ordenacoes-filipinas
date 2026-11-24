"""Figure parts: praised objects turned into reusable, parameterised instruments (27/10).

A writer casts a part by name and supplies facts; the part computes every position, count and number, and emits SVG
that tools/lesson_renderer.py accepts (whitelisted tags and attributes, declared objects, one active state per
object). New parts enter only after the chairman praises a bespoke drawing of that object: see README.md.
"""
from __future__ import annotations

import importlib, pkgutil

PARTS = {}  # filled at the end of this file, once the helpers modules import are defined


def expand_block(block: dict) -> dict:
    """{"type": "figure", "part": NAME, "params": {...}, "caption": ...} -> a renderer figure block with svg + objects."""
    name = block.get("part")
    if name not in PARTS:
        raise ValueError(f"figure part {name!r} unknown; known: {', '.join(sorted(PARTS))}")
    svg, objects = PARTS[name](block.get("params") or {})
    out = {k: v for k, v in block.items() if k not in ("part", "params")}
    out.update(svg=svg, objects=objects)
    return out

from . import tgc04_incidentes, planta_incidentes
PARTS.update(tgc04_incidentes=tgc04_incidentes.build, planta_incidentes=planta_incidentes.build)
from . import tgc03_planta
PARTS.update(tgc03_planta=tgc03_planta.build)
from . import tgc05_regimes, tgc05_planta
PARTS.update(tgc05_regimes=tgc05_regimes.build, tgc05_planta=tgc05_planta.build)
from . import tgc03_desenhos
PARTS.update(tgc03_desenhos=tgc03_desenhos.build)
from . import tgc05_desenhos
PARTS.update(tgc05_desenhos=tgc05_desenhos.build)


# Every module in this folder with a `build` is a part, under its module name (CEO 20/11: two writers editing a
# hand-kept registry dropped an import on 19/11; nobody edits this file to add a part any more).
for _m in pkgutil.iter_modules(__path__):
    if not _m.name.startswith('_'):
        _mod = importlib.import_module(f'{__name__}.{_m.name}')
        if callable(getattr(_mod, 'build', None)):
            PARTS[_m.name] = _mod.build
