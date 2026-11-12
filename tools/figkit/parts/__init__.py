"""Figure parts: praised objects turned into reusable, parameterised instruments (27/10).

A writer casts a part by name and supplies facts; the part computes every position, count and number, and emits SVG
that tools/lesson_renderer.py accepts (whitelisted tags and attributes, declared objects, one active state per
object). New parts enter only after the chairman praises a bespoke drawing of that object: see README.md.
"""
from __future__ import annotations

from . import abertura_civil, autos, calendar, glosas_inicial, oficina_comum, percurso_instancias, mj01, pedidos_caderno, planta, planta_causa, topica_mj

PARTS = {"calendar": calendar.build, "autos": autos.build, "planta": planta.build,
         "abertura_civil": abertura_civil.build, "planta_causa": planta_causa.build, "glosas_inicial": glosas_inicial.build,
         "oficina_comum": oficina_comum.build, "topica_mj": topica_mj.build,
         "mj01": mj01.build, "percurso_instancias": percurso_instancias.build, "pedidos_caderno": pedidos_caderno.build}


def expand_block(block: dict) -> dict:
    """{"type": "figure", "part": NAME, "params": {...}, "caption": ...} -> a renderer figure block with svg + objects."""
    name = block.get("part")
    if name not in PARTS:
        raise ValueError(f"figure part {name!r} unknown; known: {', '.join(sorted(PARTS))}")
    svg, objects = PARTS[name](block.get("params") or {})
    out = {k: v for k, v in block.items() if k not in ("part", "params")}
    out.update(svg=svg, objects=objects)
    return out
