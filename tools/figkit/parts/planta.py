"""planta: a lesson's relational map, drawn as a railway plan (chairman 05/11, on the Controle front's "planta do
semestre": "something you can stop for a minute or two and look at, and go: ah, that makes sense"; "fundamentally,
relationships between concepts, how one thing leads to another").

The procedure is the rail; its acts are stations; the stages and phases bracket it from above. Above that, an older
law can sit as a ghost band, aligned with the stretch of today's rail that absorbed it, so the history reads as
position. Threads leave the origin station and run under the rail: each is one element the lesson follows, wavy where
it can still change and straight where the law fixes it (locks), with a tick where it governs an act. Exits branch
off a station to where the road ends early. Numbered badges link to the chapters that tell each part.

params:
  title     str
  stations  list  {id, x, name, art, kind: origin | station | minor | end, dashed: bool}
  phases    list  {label, from, to}            from/to = station ids; drawn as the top bracket row
  stages    list  {label, from, to}            the second bracket row
  ghost     dict  {label, sub, bars: [{label, from, to, row}]}   an older law, aligned to today's rail
  gate      dict  {label, art, note}          what stands before the origin (orange: a limit)
  threads   list  {id, label, acts: [{at, note, kind: ink | lim, row}]}
  locks     list  {at, label, row}            orange verticals across the threads; after the last, threads are fixed
  knot      dict  {at, lines: [str], head}    where the threads meet (blue: what the law decided)
  exits     dict  {at, loop: {label}, out: [{label, result}]}
  badges    list  {n, href, x, y}
Every position is computed from the station x values; nothing is placed by hand twice.
"""
from __future__ import annotations

from . import svg as S

W, H = 1180, 472
Y_GH = 42            # ghost band, first rail row (rows 26 px apart)
Y_PH, Y_ST = 128, 154
Y_NAME, Y_RAIL, Y_ART = 200, 222, 246
Y_LOCK = 274
Y_T0, DY_T = 300, 27
Y_NOTE = 390
Y_EXIT = 438


def _wave(x0, x1, y, amp, period=34):
    if amp <= 0:
        return f"M{x0:.1f},{y:.1f} L{x1:.1f},{y:.1f}"
    d, x, up = f"M{x0:.1f},{y:.1f}", x0, True
    while x < x1:
        nx = min(x + period / 2, x1)
        d += f" Q{(x + nx) / 2:.1f},{y - amp if up else y + amp:.1f} {nx:.1f},{y:.1f}"
        x, up = nx, not up
    return d


def build(p: dict) -> tuple[str, list[dict]]:
    st = {s["id"]: s for s in p["stations"]}
    X = lambda sid: st[sid]["x"]
    out: list[str] = []
    T = S.text

    # ── the older law, ghosted, aligned with what absorbed it
    g = p.get("ghost")
    if g:
        out.append(T(20, Y_GH - 30, g["label"], size=12, fill=S.MUTED, letter_spacing=".08em"))
        for b in g["bars"]:
            y = Y_GH + b.get("row", 0) * 26
            x0, x1 = X(b["from"]), X(b["to"])
            xi = X(b["into"]) if b.get("into") else x0
            out.append(S.path(f"M{x0},{y + 6} C{x0},{y + 70} {xi},{Y_RAIL - 120} {xi},{Y_RAIL - 34}", fill="none", stroke=S.MUTED, stroke_width=1.2, stroke_dasharray="2 4"))
            out.append(S.line(x0, y, x1, y, stroke=S.GRID, stroke_width=5))
            for xb in (x0, x1):
                out.append(S.line(xb, y - 8, xb, y + 8, stroke=S.MUTED, stroke_width=2.5))
            if x1 - x0 < 7.2 * len(b["label"]) + 20:   # a short rail carries its name ending at its right buffer
                out.append(T(x1, y - 10, b["label"], size=12, fill=S.MUTED, anchor="end"))
            else:
                out.append(T(x0 + 10, y - 10, b["label"], size=12, fill=S.MUTED))
        out.append(T(20, Y_PH - 28, g["sub"], size=12, fill=S.INK2, letter_spacing=".08em", weight="600"))

    # ── phase and stage brackets
    def bracket(y, a, b, label, size, fill, weight=None):
        x0, x1 = X(a), X(b)
        out.append(S.path(f"M{x0 + 2},{y + 8} L{x0 + 2},{y} L{x1 - 2},{y} L{x1 - 2},{y + 8}", fill="none", stroke=fill, stroke_width=1.2))
        out.append(S.rect((x0 + x1) / 2 - 4.2 * len(label) - 8, y - 18, 8.4 * len(label) + 16, 18, fill=S.PAPER))
        out.append(T((x0 + x1) / 2, y - 5, label, size=size, fill=fill, anchor="middle", weight=weight, letter_spacing=".06em"))
    for ph in p.get("phases", []):
        bracket(Y_PH, ph["from"], ph["to"], ph["label"], 12, S.INK, "600")
    for sg in p.get("stages", []):
        bracket(Y_ST, sg["from"], sg["to"], sg["label"], 11.5, S.INK2)

    # ── the gate before the origin (the judge does not start)
    o = next(s for s in p["stations"] if s.get("kind") == "origin")
    gt = p.get("gate")
    if gt:
        out.append(S.line(24, Y_RAIL, o["x"] - 14, Y_RAIL, stroke=S.MUTED, stroke_width=1.5, stroke_dasharray="2 5"))
        gx = 70
        out.append(S.line(gx, Y_RAIL - 14, gx, Y_RAIL + 14, stroke=S.CONC, stroke_width=3))
        out.append(S.line(gx + 7, Y_RAIL - 14, gx + 7, Y_RAIL + 14, stroke=S.CONC, stroke_width=3))
        out.append(T(gx + 3, Y_NAME, gt["label"], size=13, family=S.SANS, weight="600", fill=S.CONC, anchor="middle", data_color_role="limit"))
        out.append(T(gx + 3, Y_ART, gt["art"], size=11.5, fill=S.MUTED, anchor="middle"))
        out.append(T(gx + 3, Y_ART + 17, gt["note"], size=12.5, family=S.SERIF, fill=S.INK2, anchor="middle", font_style="italic"))

    # ── the rail and its stations
    xs = [s["x"] for s in p["stations"]]
    solid_end = max(s["x"] for s in p["stations"] if not s.get("dashed") or s.get("kind") == "end")
    out.append(S.line(o["x"], Y_RAIL, solid_end, Y_RAIL, stroke=S.INK, stroke_width=5))
    for s in p["stations"]:
        k, x = s.get("kind", "station"), s["x"]
        if k == "origin":
            out.append(S.rect(x - 13, Y_RAIL - 13, 26, 26, fill=S.INK, stroke=S.INK))
        elif k == "minor":
            out.append(S.path(f"M{x},{Y_RAIL - 9} L{x + 9},{Y_RAIL} L{x},{Y_RAIL + 9} L{x - 9},{Y_RAIL} Z", fill=S.PAPER, stroke=S.INK, stroke_width=2.2))
        else:
            out.append(S.circle(x, Y_RAIL, 9, fill=S.PAPER, stroke=S.INK, stroke_width=2.6, stroke_dasharray="3 2" if s.get("dashed") else None))
        if s.get("name"):
            out.append(T(x, Y_NAME, s["name"], size=14 if k != "origin" else 15, family=S.SANS, weight="600", fill=S.INK if not s.get("dashed") else S.MUTED, anchor="middle"))
        if s.get("art"):
            out.append(T(x, Y_ART, s["art"], size=12, fill=S.MUTED, anchor="middle"))

    # ── the emenda loop over its station, and the exits below
    ex = p.get("exits")
    if ex:
        x = X(ex["at"])
        if ex.get("loop"):
            out.append(S.path(f"M{x + 2},{Y_RAIL - 9} C{x + 6},{Y_RAIL - 58} {o['x'] + 14},{Y_RAIL - 58} {o['x'] + 8},{Y_RAIL - 16}", fill="none", stroke=S.INK, stroke_width=1.5))
            out.append(S.path(f"M{o['x'] + 2},{Y_RAIL - 24} L{o['x'] + 8},{Y_RAIL - 15} L{o['x'] + 15},{Y_RAIL - 23}", fill="none", stroke=S.INK, stroke_width=1.5))
            out.append(T(x + 14, Y_RAIL - 46, ex["loop"]["label"], size=13, family=S.SANS, weight="600", fill=S.INK, anchor="middle"))
        nthreads = len(p.get("threads", []))
        y_end = Y_EXIT + 26 * (len(ex["out"]) - 1)
        out.append(S.line(x, Y_RAIL + 9, x, y_end, stroke=S.INK, stroke_width=1.6, stroke_dasharray="5 3"))
        for i, e in enumerate(ex["out"]):
            y = Y_EXIT + 26 * i
            out.append(S.line(x, y, x + 22, y, stroke=S.INK, stroke_width=1.6))
            out.append(S.rect(x + 22, y - 5, 10, 10, fill=S.INK))
            out.append(T(x + 42, y + 5, e["label"], size=14, family=S.SANS, weight="600", fill=S.INK))
            out.append(T(x + 42 + 7.9 * len(e["label"]) + 12, y + 5, e["result"], size=13.5, family=S.SERIF, fill=S.INK2, font_style="italic"))

    # ── threads: from the origin, down a spine, then along the rail; wavy until the last lock
    th = p.get("threads", [])
    locks = sorted(p.get("locks", []), key=lambda l: X(l["at"]))
    knot = p.get("knot")
    xk = X(knot["at"]) + 30 if knot else xs[-1]
    ky = Y_T0 + DY_T * (len(th) - 1) / 2
    spine = o["x"]
    out.append(S.line(spine, Y_RAIL + 11, spine, Y_T0 + DY_T * (len(th) - 1), stroke=S.INK, stroke_width=1.6))
    for i, t in enumerate(th):
        y = Y_T0 + i * DY_T
        segs, x0 = [], spine
        amps = [6, 3][:len(locks)] + [0]
        for j, lk in enumerate(locks + [None]):
            x1 = X(lk["at"]) if lk else X(knot["at"]) - 30 if knot else xs[-1]
            segs.append(_wave(x0, x1, y, amps[j]))
            x0 = x1
        body = [S.path(" ".join(segs), fill="none", stroke=S.INK, stroke_width=2.4)]
        if knot:   # converge into the knot
            body.append(S.path(f"M{x0:.1f},{y} C{x0 + 18:.1f},{y} {xk - 18:.1f},{ky} {xk:.1f},{ky}", fill="none", stroke=S.INK, stroke_width=2.4))
        body.append(T(spine - 14, y + 5, t["label"], size=14, family=S.SANS, weight="600", fill=S.INK, anchor="end"))
        for a in t.get("acts", []):
            ax = X(a["at"])
            col = S.CONC if a.get("kind") == "lim" else S.INK
            ny = Y_NOTE + 24 * a.get("row", 0)
            body.append(S.circle(ax, y, 4.5, fill=col))
            body.append(S.line(ax, y + 6, ax, ny - 13, stroke=col, stroke_width=1, stroke_dasharray="2 3"))
            body.append(T(ax - 4, ny, a["note"], size=13.5, family=S.SERIF, fill=col if col == S.CONC else S.INK2, data_color_role="limit" if col == S.CONC else None))
        body.append(S.rect(spine - 120, y - 12, 116, 22, fill=S.PAPER, opacity="0"))
        out.append(f'<g data-thread="{S.esc(t["id"])}" tabindex="0" role="button" aria-label="{S.esc(t["label"])}">' + "".join(body) + "</g>")
    for lk in locks:
        x = X(lk["at"])
        out.append(S.line(x, Y_LOCK + 8, x, Y_T0 + DY_T * (len(th) - 1) + 16, stroke=S.CONC, stroke_width=2.5))
        out.append(T(x + 7, Y_LOCK, lk["label"], size=12.5, fill=S.CONC, data_color_role="limit"))
    if knot:
        out.append(S.rect(xk - 9, ky - 9, 18, 18, fill=S.DIF, transform=f"rotate(45 {xk} {ky})"))
        out.append(T(xk + 22, ky - 34, knot["head"], size=14, family=S.SANS, weight="600", fill=S.DIF, data_color_role="decided"))
        for i, ln in enumerate(knot["lines"]):
            out.append(T(xk + 22, ky - 12 + i * 20, ln, size=13.5, family=S.SERIF, fill=S.INK2))

    # ── chapter badges: the map is the lesson's table of contents
    for b in p.get("badges", []):
        out.append(f'<a href="{S.esc(b["href"])}">' + S.rect(b["x"], b["y"], 26, 18, fill=S.PAPER, stroke=S.INK, stroke_width=1.2)
                   + T(b["x"] + 13, b["y"] + 13, b["n"], size=11, fill=S.INK, anchor="middle", weight="600") + "</a>")
    return S.svg(W, H, p.get("title", "planta"), out), []
