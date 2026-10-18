"""Render one requested Processo case-thread view from shared, source-tagged data.

The pure injection contract replaces the contents of one position-specific marker block.
It validates the requested page path and never reads, sweeps, or writes other course pages.
"""

from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path

from figkit import line, svg, t


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = Path(__file__).with_suffix(".json")
DATA = json.loads(DATA_PATH.read_text(encoding="utf-8"))
PAGE_ROOT = ROOT / "courses" / "processo-civil-i"


def _position_key(position: int | str) -> str:
    try:
        number = int(position)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid study position: {position!r}") from exc
    key = str(number)
    if key not in DATA["positions"]:
        raise ValueError(f"unknown study position: {number}")
    return key


def _text(x: float, y: float, value: str, **kwargs: object) -> str:
    """Use the figure kit's text primitive with XML-safe source strings."""
    return t(x, y, escape(str(value), quote=False), **kwargs)


def _wrap(value: str, width: int = 112) -> list[str]:
    words = value.split()
    rows: list[str] = []
    row = ""
    for word in words:
        candidate = f"{row} {word}".strip()
        if row and len(candidate) > width:
            rows.append(row)
            row = word
        else:
            row = candidate
    if row:
        rows.append(row)
    return rows or [""]


def render_position(position: int | str) -> str:
    """Return the kit-generated accessible SVG for exactly one study position."""
    key = _position_key(position)
    number = int(key)
    location = DATA["positions"][key]
    thread = DATA["threads"][location["thread"]]
    events = [item for item in thread["events"] if item["from"] <= number]
    steps = [item for item in thread["steps"] if item["position"] <= number]

    o = ""
    o += _text(42, 42, thread["title"], size=17, fill="var(--ink)", weight=700, ls=".02em")
    o += _text(42, 67, f"{thread['case_label']} · POSIÇÃO {number:02}",
               size=11, fill="var(--ink-2)", weight=600)
    o += line(42, 82, 1038, 82, tone="ink", w=1.3)

    note_lines = _wrap(thread["source_note"], 128)
    y = 105
    for row in note_lines:
        o += _text(42, y, row, size=10.5, fill="var(--ink-2)", weight=500, ls=".02em")
        y += 15

    timeline_top = y + 24
    event_gap = 57
    if events:
        o += line(73, timeline_top - 9, 73,
                  timeline_top + (len(events) - 1) * event_gap + 7,
                  tone="ink", w=1.8)
    for index, event in enumerate(events):
        ey = timeline_top + index * event_gap
        tone = "conc" if event["when"].startswith("P1 · V") else "ink"
        o += f'<circle cx="73" cy="{ey - 3}" r="5.5" style="fill:var(--paper);stroke:var(--{tone});stroke-width:1.8"/>'
        o += _text(97, ey, event["heading"], size=13, fill="var(--ink)", weight=700, ls=".015em")
        o += _text(1038, ey, event["when"], size=10.5, fill=f"var(--{tone})",
                   anchor="end", weight=700, ls=".035em")
        o += _text(97, ey + 17, event["detail"], size=11, fill="var(--ink-2)",
                   weight=500, ls=".015em")

    step_top = timeline_top + max(len(events), 1) * event_gap + 6
    o += line(42, step_top, 1038, step_top, tone="muted", w=1.1)
    o += _text(42, step_top + 20, "CAMADA ANALÍTICA", size=10.5,
               fill="var(--ink-2)", weight=700, ls=".07em")
    step_y = step_top + 47
    for step in steps:
        tone = "conc" if step["status"] == "hypothesis" else "dif"
        marker_y = step_y - 4
        o += line(48, marker_y, 72, marker_y, tone=tone, w=2.4)
        status = "HIPÓTESE CONSTRUÍDA" if step["status"] == "hypothesis" else "REGISTRO"
        o += _text(88, step_y, f"{status} · {step['label']}", size=11.5,
                   fill=f"var(--{tone})", weight=700, ls=".02em")
        detail_rows = _wrap(step["detail"], 124)
        for offset, row in enumerate(detail_rows, start=1):
            o += _text(88, step_y + 16 * offset, row, size=10.5,
                       fill="var(--ink-2)", weight=500, ls=".015em")
        step_y += 24 + len(detail_rows) * 16

    accessible = "; ".join([thread["title"], *[event["heading"] for event in events],
                            *[step["label"] for step in steps]])
    ident = f"pci-thread-{location['thread']}-{number:02}"
    return svg(f"28 20 1038 {step_y + 5}", o, cls="fig", ident=ident,
               label=escape(f"Registro progressivo na posição {number}: {accessible}", quote=True))


def inject_single_page(position: int | str, page_path: str | Path,
                       lesson_html: str) -> str:
    """Replace one existing marker block in one explicitly requested lesson string.

    The caller supplies the page text and the study position. The expected path is
    checked before any replacement, preventing a position from targeting another page.
    This function is pure: callers decide whether and where to write its return value.
    """
    key = _position_key(position)
    expected = (ROOT / DATA["positions"][key]["page"]).resolve()
    requested = Path(page_path).resolve()
    if requested != expected:
        raise ValueError(f"position {int(key):02} belongs only to {expected}")
    marker = DATA["positions"][key]["marker"]
    start = f"<!-- {marker}:start -->"
    end = f"<!-- {marker}:end -->"
    pattern = re.compile(re.escape(start) + r"[\s\S]*?" + re.escape(end))
    matches = list(pattern.finditer(lesson_html))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {marker} block; found {len(matches)}")
    replacement = f"{start}{render_position(key)}{end}"
    return pattern.sub(lambda _: replacement, lesson_html, count=1)


def self_check() -> None:
    """Dry-run every writable position against an in-memory single-page fixture.

    Position 20 (Aula 16) is deliberately excluded from execution; its renderer remains
    available for a later explicit call after the page owner authorizes integration.
    """
    for key, contract in DATA["positions"].items():
        if key == "20":
            continue
        marker = contract["marker"]
        fixture = f"before<!-- {marker}:start -->placeholder<!-- {marker}:end -->after"
        result = inject_single_page(key, PAGE_ROOT / Path(contract["page"]).name, fixture)
        if "placeholder" in result or result.count(f"<!-- {marker}:start -->") != 1:
            raise AssertionError(f"position {key}: marker replacement failed")
        if f'id="pci-thread-{contract["thread"]}-{int(key):02}"' not in result:
            raise AssertionError(f"position {key}: expected SVG missing")


if __name__ == "__main__":
    if sys.argv[1:] != ["--self-check"]:
        raise SystemExit("usage: processo_threads.py --self-check")
    self_check()
    print("dry-run passed for positions 01, 11–19 except 20; no lesson files read or written")
