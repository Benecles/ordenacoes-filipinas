#!/usr/bin/env python3
"""Build the home-page changelog from changelog.json and source lesson figures."""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "changelog.json"
HOME = ROOT / "index.html"
START = "<!-- PATCHNOTES:START -->"
END = "<!-- PATCHNOTES:END -->"

sys.path.insert(0, str(ROOT / "tools" / "figkit"))
from figkit import line, svg, t  # noqa: E402


def extract_figure(page: str, panel: str) -> str:
    """Find a page/panel pair, handling the id-less opening hero by its class name."""
    raw = (ROOT / page).read_bytes()
    for match in re.finditer(rb"<svg\b[^>]*>.*?</svg\s*>", raw, re.DOTALL):
        element = match.group(0)
        if panel.encode("utf-8") in element.split(b">", 1)[0]:
            return element.decode("utf-8")
    raise ValueError(f"SVG panel {panel!r} not found in {page}")


def mini(kind: str) -> str:
    """Compose small vignettes only from the shared Figure Kit primitives."""
    o = ""
    if kind == "cascade":
        labels = ["FATO", "CONDUTA", "TIPICIDADE", "ANTIJURIDICIDADE", "CULPABILIDADE"]
        xs = [24, 156, 288, 420, 552]
        o += line(20, 92, 580, 92, tone="muted", w=1.2)
        for i, (x, label) in enumerate(zip(xs, labels)):
            o += line(x, 92, x, 62 if i % 2 == 0 else 122, tone="conc" if i == 4 else "ink", w=1.6)
            o += t(x, 48 if i % 2 == 0 else 143, label, size=10, anchor="middle", weight=700, fill="var(--conc)" if i == 4 else "var(--ink)")
    elif kind == "deadline":
        # A month-like calendar without invented month or date labels.
        x0, y0, cw, rh = 154, 38, 42, 32
        for i in range(8):
            o += line(x0 + i * cw, y0, x0 + i * cw, y0 + 5 * rh, tone="muted", w=0.8)
        for i in range(6):
            o += line(x0, y0 + i * rh, x0 + 7 * cw, y0 + i * rh, tone="muted", w=0.8)
        for i in range(28):
            row, col = divmod(i, 7)
            mark = "●" if i == 20 else "·"
            o += t(x0 + col * cw + cw / 2, y0 + row * rh + 21, mark, size=10.5, anchor="middle", weight=700 if i == 20 else 500, fill="var(--conc)" if i == 20 else "var(--ink-2)")
        o += t(16, 62, "CONTAGEM", size=10, weight=700, caps=True, fill="var(--ink-2)")
        o += line(16, 78, 128, 78, tone="conc", w=2)
        o += t(16, 100, "NO CALENDÁRIO", size=10, weight=700, caps=True, fill="var(--conc)")
    elif kind == "route":
        points = [(74, 116), (300, 62), (526, 116)]
        o += line(points[0][0], points[0][1], points[1][0], points[1][1], tone="conc", w=2)
        o += line(points[1][0], points[1][1], points[2][0], points[2][1], tone="conc", w=2)
        for (x, y), label in zip(points, ("BOLONHA", "COIMBRA", "OLINDA")):
            o += t(x, y - 13, "●", size=12, anchor="middle", fill="var(--conc)")
            o += t(x, y + 21, label, size=10, anchor="middle", weight=700)
    elif kind == "bookmark":
        o += line(246, 30, 246, 150, tone="conc", w=2)
        o += line(354, 30, 354, 150, tone="conc", w=2)
        o += line(246, 30, 354, 30, tone="conc", w=2)
        o += line(246, 150, 300, 122, tone="conc", w=2)
        o += line(354, 150, 300, 122, tone="conc", w=2)
        o += t(300, 88, "MARCA-TEXTO", size=10, anchor="middle", weight=700, fill="var(--conc)")
    elif kind == "register":
        for i, (y, left, right) in enumerate(((48, "O QUE VOCÊ FAZ", "AULA"), (92, "QUANTO LEVA", "LEITURA"), (136, "O QUE CAI", "PROVA"))):
            o += line(24, y + 7, 576, y + 7, tone="muted", w=0.9)
            o += t(30, y, left, size=10, weight=700)
            o += t(570, y, right, size=9, anchor="end", fill="var(--conc)" if i == 0 else "var(--ink-2)")
    elif kind == "nameplate":
        o += line(64, 51, 536, 51, tone="ink", w=1.5)
        o += line(64, 133, 536, 133, tone="ink", w=1.5)
        o += line(64, 51, 64, 133, tone="ink", w=1.5)
        o += line(536, 51, 536, 133, tone="ink", w=1.5)
        o += t(300, 91, "ORDENAÇÕES FILIPINAS", size=14, anchor="middle", weight=700, caps=True, ls=".12em")
        o += t(300, 116, "NOVO NOME", size=9.5, anchor="middle", weight=700, fill="var(--conc)")
    else:
        raise ValueError(f"Unknown mini kind: {kind}")
    return svg("0 0 600 180", o, cls="patch-mini")


def tile_markup(tile: dict) -> str:
    visual = tile["visual"]
    label = {"figure": "FIGURA", "stat": "DADO", "mini": "GUIA"}[visual["type"]]
    if visual["type"] == "figure":
        artwork = extract_figure(visual["page"], visual["panel"])
    elif visual["type"] == "stat":
        artwork = (
            f'<strong class="patch-stat__value">{html.escape(visual["value"])}</strong>'
            f'<span class="patch-stat__label">{html.escape(visual["label"])}</span>'
        )
    elif visual["type"] == "mini":
        artwork = mini(visual["kind"])
    else:
        raise ValueError(f"Unknown visual type: {visual['type']}")
    sub = f'<p class="patch-tile__sub">{html.escape(tile["sub"])}</p>' if tile["sub"] else ""
    size = html.escape(tile["size"])
    return (
        f'<a class="patch-tile patch-tile--{size}" href="{html.escape(tile["href"], quote=True)}">'
        f'<div class="patch-tile__visual">{artwork}</div>'
        f'<div class="patch-tile__content"><span class="patch-tile__label">{label}</span>'
        f'<h3 class="patch-tile__title">{html.escape(tile["title"])}</h3>{sub}</div></a>'
    )


def build_markup(data: dict) -> str:
    periods = []
    for period in data["periods"]:
        tiles = "".join(tile_markup(tile) for tile in period["tiles"])
        periods.append(
            '<section class="patch-bento-period" aria-label="'
            + html.escape(period["label"], quote=True)
            + '"><h2 class="patch-bento-period__title">'
            + html.escape(period["label"])
            + '</h2><div class="patch-bento-grid">'
            + tiles
            + "</div></section>"
        )
    history = data["history_html"]
    return (
        '<link rel="stylesheet" href="assets/changelog.css">'
        '<section id="patch-notes-bento" class="patch-bento" aria-labelledby="patch-title">'
        '<span class="label">Notas de atualização</span><div class="patch-bento-head"><h2 id="patch-title" class="patch-bento-heading">O que mudou</h2><button type="button" class="patch-all label" aria-controls="patch-notes-bento" aria-expanded="false" hidden>Abrir tudo</button></div>'
        + "".join(periods)
        + '<details class="patch-history"><summary>Histórico</summary>'
        + history
        + '</details></section><script>(()=>{const s=document.querySelector(".patch-bento"),b=s&&s.querySelector(".patch-all");if(!s||!b)return;const all=()=>[...s.querySelectorAll("details")],sync=()=>{const shut=all().some(d=>!d.open);b.textContent=shut?"Abrir tudo":"Fechar tudo";b.setAttribute("aria-expanded",String(!shut))};b.hidden=false;b.onclick=()=>{const open=all().some(d=>!d.open);all().forEach(d=>d.open=open);sync()};s.addEventListener("toggle",sync,true);sync()})();</script>'
    )


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    original = HOME.read_bytes()
    start_marker, end_marker = START.encode(), END.encode()
    if original.count(start_marker) != 1 or original.count(end_marker) != 1:
        raise SystemExit("Expected exactly one pair of PATCHNOTES markers")
    start = original.index(start_marker) + len(start_marker)
    end = original.index(end_marker)
    rendered = original[:start] + build_markup(data).encode("utf-8") + original[end:]
    HOME.write_bytes(rendered)
    print(f"Built {HOME.relative_to(ROOT)} from {DATA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
