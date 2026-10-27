"""autos: the case file seen from the side, each act a band of numbered folhas (chairman-praised specimen 07/10; the
Processo front's object, praised 26/10).

params:
  heading  str   top line, e.g. "2015/1 · Avaliação 2 · Jesse Valadão × Dalvo Fritz e Serotonina da Silva"
  quote    str   optional second line (a statute sentence in italics is the usual one)
  acts     list  oldest first: {id, title, sheets, kind, meta: [≤2 short lines], note}
                 kind: act (juntado) | key (the act the question turns on) | gap (should be here, isn't) | next (still to come)
                 note: the sentence shown when the act is pressed
Folha numbers are computed (capa = fl. 1); "next" acts have no numbers yet. Sheet jitter is seeded, so the drawing is
the same on every build.
"""
from __future__ import annotations

import random

from . import svg as S

KIND_STROKE = {"act": S.INK, "key": S.DIF, "gap": S.CONC, "next": S.MUTED}


def build(p: dict) -> tuple[str, list[dict]]:
    acts = p["acts"]
    if not acts:
        raise ValueError("autos: acts must not be empty")
    for a in acts:
        if a.get("kind", "act") not in KIND_STROKE:
            raise ValueError(f"autos: unknown kind {a.get('kind')!r}")
    rng = random.Random(p.get("seed", 207))
    total = sum(max(1, int(a["sheets"])) for a in acts)
    P = max(6, min(11, 470 // max(total, 1)))  # sheet pitch shrinks so any case fits the frame
    SH = max(4, P - 3)
    W, SX, SW = 1080, 262, 380
    top_text = 96 if p.get("quote") else 70
    stack_h = total * P
    BOT = top_text + 40 + stack_h
    band_y = BOT + 60
    H = band_y + 62

    b = [S.text(40, 34, p["heading"], size=12, fill=S.INK2)]
    if p.get("quote"):
        b.append(S.text(40, 60, p["quote"], size=15, family=S.SERIF, fill=S.INK2))
    b.append(S.rect(SX - 6, BOT, SW + 14, 18, rx=2, fill=S.PAPER2, stroke=S.INK, stroke_width=1.5))
    b.append(S.text(SX - 26, BOT + 14, "1", size=13, fill=S.INK2, anchor="end"))
    b.append(S.text(SX - 26, BOT + 36, "fls.", size=11, fill=S.INK2, anchor="end"))

    bands, y, fl = [], BOT, 2
    for a in acts:
        n, kind = max(1, int(a["sheets"])), a.get("kind", "act")
        top = y - n * P
        if kind == "gap":
            b.append(S.rect(SX, top + 2, SW, n * P - 4, fill="none", stroke=S.CONC, stroke_width=1.5, stroke_dasharray="6 5"))
            b += S.hatch(SX, top + 2, SW, n * P - 4, step=10, stroke=S.CONC, stroke_width=1.2, opacity="0.45")
        else:
            for k in range(n):
                sy = y - (k + 1) * P + (P - SH)
                dx, dw = rng.uniform(-3, 3), rng.uniform(-4, 2)
                if kind == "next":
                    b.append(S.rect(SX + dx, sy, SW + dw, SH, fill="none", stroke=S.MUTED, stroke_width=1, stroke_dasharray="4 4"))
                else:
                    b.append(S.rect(SX + dx, sy, SW + dw, SH, fill=S.PAPER, stroke=KIND_STROKE[kind], stroke_width=1.8 if k == 0 or kind == "key" else 1))
            if kind != "next":
                b.append(S.text(SX - 26, (top + y) / 2 + 5, str(fl) if n == 1 else f"{fl}–{fl + n - 1}", size=13, fill=S.INK2, anchor="end"))
                fl += n
        bands.append((a, top, y))
        y = top
    stop = y
    # binding cord along the sheets that exist (not along acts still to come)
    real_top = min(t for a, t, _ in bands if a.get("kind", "act") != "next")
    b.append(S.line(SX + 14, real_top + 4, SX + 14, BOT + 14, stroke=S.INK, stroke_width=1.5))
    for yy in range(int(real_top) + 16, int(BOT), 46):
        b.append(S.line(SX + 8, yy, SX + 20, yy, stroke=S.INK, stroke_width=2.5))
    # growth rail: each juntada goes on top
    b.append(S.line(70, BOT + 10, 70, stop + 6, stroke=S.INK, stroke_width=1.5))
    b.append(S.path(f"M63 {stop + 18} L70 {stop + 4} L77 {stop + 18}", fill="none", stroke=S.INK, stroke_width=1.5))
    b.append(S.text(0, 0, "cada ato juntado entra por cima", size=11, fill=S.INK2, anchor="middle",
                    transform=f"translate(56 {(BOT + stop) / 2:.0f}) rotate(-90)"))

    # labels in the clear column, relaxed so they never overlap, each with a leader to its band
    LX, LINE = 724, 19
    want = []
    for a, top, bot in bands:
        h = 20 + LINE * len((a.get("meta") or [])[:2])
        want.append([(top + bot) / 2 - h / 2 + 14, h])
    order = sorted(range(len(want)), key=lambda i: -want[i][0])  # bottom-up
    prev = None
    for i in order:
        if prev is not None:
            want[i][0] = min(want[i][0], want[prev][0] - want[i][1] - 14)
        prev = i
    objects, targets, states = [], [], []
    for (a, top, bot), (ly, _h) in zip(bands, want):
        kind = a.get("kind", "act")
        col = KIND_STROKE[kind]
        mid = (top + bot) / 2
        b.append(S.path(f"M{SX + SW + 8} {mid:.1f} L{LX - 14} {ly - 5:.1f}", fill="none", stroke=S.GRID, stroke_width=1))
        b.append(S.text(LX, ly, a["title"], size=17, family=S.SANS, fill=S.INK if kind != "next" else S.MUTED, weight="600"))
        for j, m in enumerate((a.get("meta") or [])[:2]):
            b.append(S.text(LX, ly + 20 + j * LINE, m, size=15, family=S.SERIF, fill=col if kind in ("key", "gap") else S.INK2))
        oid = a["id"]
        note = a.get("note") or a["title"]
        objects.append({"id": oid, "label": a["title"], "description": note})
        targets.append(f'<g data-object="{oid}">{S.hit(SX - 40, top, LX - SX + 340, max(bot - top, 16))}</g>')
        ring = S.rect(SX - 8, top - 2, SW + 18, bot - top + 4, fill="none", stroke=S.CONC, stroke_width=3)
        states.append(f'<g data-object-state="{oid}" data-state="active">{ring}{"".join(S.callout(40, band_y, W - 80, note))}</g>')
    b += S.callout_band(40, band_y, W - 80, "Toque num ato da pilha para ver o que ele faz nos autos.")
    title = p.get("title") or "Os autos vistos de lado: cada ato juntado entra por cima, com as folhas numeradas"
    return S.svg(W, H, title, b + targets + states), objects
