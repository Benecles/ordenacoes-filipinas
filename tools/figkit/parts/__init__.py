"""Figure parts: praised objects turned into reusable, parameterised instruments (27/10).

A writer casts a part by name and supplies facts; the part computes every position, count and number, and emits SVG
that tools/lesson_renderer.py accepts (whitelisted tags and attributes, declared objects, one active state per
object). New parts enter only after the chairman praises a bespoke drawing of that object: see README.md.
"""
from __future__ import annotations

from . import tgc01_figuras, tgc01_planta
from . import tgc06_figuras, tgc06_planta
from . import tgc09_planta, tgc09_revisao, tgc08_cessao, tgc08_planta, tgc_cessao, tgc_interpretacao, tgc07_planta
from . import extincao10
from . import tgc10_extincao, tgc10_planta

from . import mj01_atlas, abertura_civil, autos, calendar, glosas_inicial, mj01, oficina_comum, percurso_instancias, pedidos_folhas, planta, planta_causa, topica_cia, topica_mj

PARTS = {"tgc01_figuras": tgc01_figuras.build, "tgc01_planta": tgc01_planta.build, "tgc06_figuras": tgc06_figuras.build, "tgc06_planta": tgc06_planta.build, "tgc10_extincao": tgc10_extincao.build, "tgc10_planta": tgc10_planta.build, "extincao10": extincao10.build, "tgc09_planta": tgc09_planta.build, "tgc09_revisao": tgc09_revisao.build,"tgc08_cessao": tgc08_cessao.build, "tgc08_planta": tgc08_planta.build, "tgc_cessao": tgc_cessao.build, "tgc_interpretacao": tgc_interpretacao.build, "mj01_atlas": mj01_atlas.build, "calendar": calendar.build, "autos": autos.build, "planta": planta.build, "tgc07_planta": tgc07_planta.build,
         "abertura_civil": abertura_civil.build, "planta_causa": planta_causa.build, "glosas_inicial": glosas_inicial.build,
         "oficina_comum": oficina_comum.build, "topica_mj": topica_mj.build, "topica_cia": topica_cia.build,
         "mj01": mj01.build, "percurso_instancias": percurso_instancias.build,
         "pedidos_folhas": pedidos_folhas.build}


def expand_block(block: dict) -> dict:
    """{"type": "figure", "part": NAME, "params": {...}, "caption": ...} -> a renderer figure block with svg + objects."""
    name = block.get("part")
    if name not in PARTS:
        raise ValueError(f"figure part {name!r} unknown; known: {', '.join(sorted(PARTS))}")
    svg, objects = PARTS[name](block.get("params") or {})
    out = {k: v for k, v in block.items() if k not in ("part", "params")}
    out.update(svg=svg, objects=objects)
    return out
