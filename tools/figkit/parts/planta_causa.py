"""planta_causa: the planta of a cause in the fase de conhecimento (chairman 05/11: the hero is "a map you stop and look
at for a minute or two and go: ah, that makes sense"; Controle's planta is the bar).

Not a row of stations. The petition is a standing sheet whose seven requisites (art. 319) are hooks; the demand's own
elements leave it as threads that run through the stages and meet the other papers of the case. Position carries the
meaning: the stages are bands along the autos (the case file seen edge-on, base of the plan); the threads that can
still change are wavy and become straight where art. 329 fixes them (orange locks); the contestação lies across the
threads it answers; the pedido's blue thread is the only one that reaches the sentença's dispositivo and stops at the
ceiling of arts. 141 and 492; the shortcut is an orange dashed ribbon over the top; the fence stands before the
cumprimento (round 4: it marks the Buzaid code's original text, which kept execution in another process).

Side acts (citação, audiência, instrução, cumprimento) are marks on the threads (a ring and a lowercase word), aligned
with the flag that stands on the autos below; they are not boxes. The six pressable relations are one rail of text
buttons under the drawing, the same look as the lower figures' tabs; the drawing's own objects (petition rows, the
juiz's loop, the zone strip, the ribbon) answer the same press. Everything is computed from the constants below, so no
label is placed twice by hand.

Params (facts, never coordinates):
  title   optional accessible title
Objects (pressable; the page writes the answer in a fixed slot and toggles the matching state layer):
  pedido, causa, partes, emenda, alterar, atalho
Contract (same as abertura_civil): <g data-object=ID role=button tabindex=0> targets (several groups may share an ID),
<g data-object-state=ID data-state=active visibility=hidden> traces.
"""
from __future__ import annotations

from . import svg as S

W = 1140
ROWS = {"juizo": 0, "partes": 1, "causa": 2, "pedido": 3, "valor": 4, "provas": 5, "audiencia": 6}
SHEET_TOP = 104
Y0, DY = 148, 30
RY = {k: Y0 + DY * i for k, i in ROWS.items()}
SHEET_BOT = RY["audiencia"] + 22
SLAB_Y0, SLAB_Y1 = SHEET_BOT + 29, SHEET_BOT + 61
RAIL_Y, RAIL_H = SLAB_Y1 + 12, 32
H = RAIL_Y + RAIL_H + 4

SX0, SX1 = 30, 214                 # petition sheet
DX = 238                           # the juiz reads (diamond, emenda loop)
CITX = 300                         # the citação ring on the partes thread
LOCK1, LOCK2 = 322, 592            # art. 329, I and II
DEF0, DEF1 = 410, 556              # contestação sheet
FLD0, FLD1 = 610, 756              # saneamento field
INS0 = 766                         # instrução begins
SEN0, SEN1 = 892, 1004             # sentença sheet
FENCE = 1020
CUMX = 1034                        # cumprimento ring
SLAB_X1 = W - 4

_boxes: list[tuple[str, float, float, float, float]] = []   # text boxes, for the overlap check


def _tw(s: str, size: float, family: str) -> float:
    k = 0.61 if family == S.MONO else 0.5 if family == S.SERIF else 0.56
    return len(s) * size * k


def _t(x, y, s, size=12, family=S.MONO, fill=S.INK, weight=None, anchor="start", reg=True, **kw) -> str:
    w = _tw(s, size, family)
    x0 = x if anchor == "start" else x - w / 2 if anchor == "middle" else x - w
    if reg:
        _boxes.append((s, x0, y - size * 0.8, x0 + w, y + size * 0.25))
    return S.text(x, y, s, size=size, family=family, fill=fill, weight=weight,
                  anchor=None if anchor == "start" else anchor, **kw)


def overlaps() -> list[str]:
    """Pairs of registered labels whose boxes intersect, and labels that leave the canvas (dev check; run after build)."""
    out = []
    for i, a in enumerate(_boxes):
        if a[1] < 0 or a[3] > W:
            out.append(f"{a[0]!r} leaves the canvas")
        for b in _boxes[i + 1:]:
            if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                out.append(f"{a[0]!r} x {b[0]!r}")
    return out


def _wave(x0, x1, y, amp, period=30):
    if amp <= 0:
        return f"M{x0:.1f},{y:.1f} L{x1:.1f},{y:.1f}"
    d, x, up = f"M{x0:.1f},{y:.1f}", x0, True
    while x < x1 - 0.1:
        nx = min(x + period / 2, x1)
        d += f" Q{(x + nx) / 2:.1f},{y - amp if up else y + amp:.1f} {nx:.1f},{y:.1f}"
        x, up = nx, not up
    return d


def _group(body, **attrs):
    return f'<g {S.attrs(**attrs)}>{"".join(body)}</g>'


def _paper(x0, y0, x1, y1, stroke=S.INK, sw=1.5, fold=14):
    return [S.path(f"M{x0},{y0} H{x1 - fold} L{x1},{y0 + fold} V{y1} H{x0} Z", fill=S.PAPER, stroke=stroke, stroke_width=sw,
                   stroke_linejoin="round"),
            S.path(f"M{x1 - fold},{y0} V{y0 + fold} H{x1}", fill="none", stroke=stroke, stroke_width=1)]


def _hit(x, y, w, h):
    return S.rect(x, y, w, h, fill="none", stroke="none", stroke_width=1, pointer_events="all", class_="hit")


def _ring(x, y, r=6):
    return S.circle(x, y, r, fill=S.PAPER, stroke=S.INK, stroke_width=2)


def build(p: dict) -> tuple[str, list[dict]]:
    _boxes.clear()
    o: list[str] = []
    ry = RY
    xa, xb = SX0, SEN1

    # ── 1. the scale along the top: phase, stages, and how free the demand is to change
    o.append(S.path(f"M{xa},{25} V19 H{xb} V25", fill="none", stroke=S.DIF, stroke_width=1.4))
    o.append(_t((xa + xb) / 2, 13, "FASE DE CONHECIMENTO", 12.5, fill=S.DIF, anchor="middle", letter_spacing=".1em"))
    stages = [("POSTULAR", xa, LOCK2), ("ORGANIZAR", LOCK2, 764), ("INSTRUIR", 764, 888), ("DECIDIR", 888, xb)]
    for lab, a, b in stages:
        o.append(S.path(f"M{a + 2},{52} V46 H{b - 2} V52", fill="none", stroke=S.INK2, stroke_width=1.1))
        o.append(_t((a + b) / 2, 40, lab, 12, fill=S.INK2, anchor="middle", letter_spacing=".08em"))
    zones = [(xa, LOCK1, "ALTERA SOZINHA", ""),
             (LOCK1, LOCK2, "ALTERA SE A RÉ CONCORDA", ""),
             (LOCK2, xb, "FECHADA", "para o autor · acordo só para Marinoni (art. 190)")]
    for a, b, head, rest in zones:
        o.append(S.line(a + 2, 64, b - 2, 64, stroke=S.CONC, stroke_width=1.6))
        o.append(S.line(a + 2, 64, a + 2, 71, stroke=S.CONC, stroke_width=1.6))
        o.append(_t(a + 10, 85, head, 12.5, family=S.SANS, fill=S.CONC, weight="600", data_color_role="limit"))
        if rest:
            o.append(_t(a + 24 + len(head) * 12.5 * 0.7, 85, rest, 11, fill=S.MUTED))
    o.append(S.line(xb - 2, 64, xb - 2, 71, stroke=S.CONC, stroke_width=1.6))

    # ── 2. the autos edge-on, the base of the plan; the flags stand on it, each above the mark it belongs to
    o.append(S.rect(SX0, SLAB_Y0, SLAB_X1 - SX0, SLAB_Y1 - SLAB_Y0, fill=S.PAPER2, stroke=S.INK, stroke_width=1.4))
    xk = SX0 + 4
    while xk < SLAB_X1 - 2:
        o.append(S.line(xk, SLAB_Y0 + 1, xk, SLAB_Y1 - 1, stroke=S.GRID, stroke_width=1))
        xk += 4
    flags = [("PETIÇÃO", SX0 + 6), ("CITAÇÃO", CITX), ("CONTESTAÇÃO", DEF0), ("SANEAMENTO", LOCK2),
             ("INSTRUÇÃO", INS0), ("SENTENÇA", SEN0), ("CUMPRIMENTO", CUMX)]
    for fx in [SX1] + [f[1] for f in flags[1:]]:
        o.append(S.line(fx, SLAB_Y0, fx, SLAB_Y1, stroke=S.INK, stroke_width=1.6))
    o.append(S.rect(SX0 + 6, SLAB_Y0 + 6, 198, SLAB_Y1 - SLAB_Y0 - 12, fill=S.INK))
    o.append(_t(SX0 + 16, SLAB_Y0 + 21, "AUTOS · PROCEDIMENTO COMUM", 11, fill=S.PAPER, letter_spacing=".04em"))
    for lab, fx in flags:
        o.append(S.line(fx, SLAB_Y0 - 22, fx, SLAB_Y0, stroke=S.INK, stroke_width=1.4))
        w = len(lab) * 7.4 + 20
        o.append(S.path(f"M{fx},{SLAB_Y0 - 22} h{w:.1f} l-7,9 l7,9 h-{w:.1f} Z", fill=S.PAPER, stroke=S.INK, stroke_width=1.2))
        o.append(_t(fx + 8, SLAB_Y0 - 9, lab, 11.5, fill=S.INK, letter_spacing=".04em"))

    # ── 3. the petition sheet: seven requisites, each a hook the threads leave from
    o += _paper(SX0, SHEET_TOP, SX1, SHEET_BOT, stroke=S.DIF, sw=1.8)
    o.append(_t(SX0 + 16, SHEET_TOP + 26, "Petição inicial", 18, family=S.SERIF, fill=S.INK, weight="600"))
    names = [("juízo", "juizo"), ("partes", "partes"), ("causa de pedir", "causa"), ("pedido", "pedido"),
             ("valor", "valor"), ("provas", "provas"), ("audiência", "audiencia")]
    for i, (nm, key) in enumerate(names):
        y = ry[key]
        if i:
            o.append(S.line(SX0 + 12, y - DY / 2, SX1 - 12, y - DY / 2, stroke=S.GRID, stroke_width=1))
        o.append(_t(SX0 + 20, y + 5, nm, 15.5, family=S.SERIF, fill=S.INK))
        o.append(S.circle(SX1, y, 4.5, fill=S.INK))

    # ── 4. the threads
    yj, yp, yc, yd = ry["juizo"], ry["partes"], ry["causa"], ry["pedido"]
    # juízo reads the petition (diamond), orders the citação (it drops onto the partes thread), or sends it back (emenda loop)
    o.append(S.path(f"M{SX1},{yj} H{DX - 9}", fill="none", stroke=S.INK, stroke_width=2.2))
    o.append(S.path(f"M{DX},{yj - 9} L{DX + 9},{yj} L{DX},{yj + 9} L{DX - 9},{yj} Z", fill=S.PAPER, stroke=S.INK, stroke_width=2.2))
    o.append(S.path(f"M{DX + 9},{yj} H{CITX - 18} Q{CITX},{yj} {CITX},{yj + 18} V{yp - 6}", fill="none", stroke=S.INK, stroke_width=2.2))
    o.append(S.path(f"M{DX + 2},{yj - 10} C{DX + 4},{yj - 52} {SX1 - 40},{yj - 52} {SX1 - 34},{SHEET_TOP + 3}", fill="none",
                    stroke=S.INK, stroke_width=1.6))
    o.append(S.path(f"M{SX1 - 40},{SHEET_TOP - 8} L{SX1 - 34},{SHEET_TOP + 2} L{SX1 - 27},{SHEET_TOP - 7}", fill="none", stroke=S.INK, stroke_width=1.6,
                    stroke_linecap="round", stroke_linejoin="round"))
    o.append(_t(DX + 24, SHEET_TOP + 20, "emenda", 13, family=S.SERIF, fill=S.INK2, font_style="italic"))
    # partes: straight from the sheet, through the citação, to the sentença
    o.append(S.path(f"M{SX1},{yp} H{SEN0}", fill="none", stroke=S.INK, stroke_width=2.2))
    o.append(_ring(CITX, yp))
    o.append(_t(CITX - 12, yp - 9, "citação", 13, family=S.SERIF, fill=S.INK2, anchor="end", font_style="italic"))
    # causa and pedido: wavy where they can still change, straight where art. 329 fixes them
    for key, col, sw in (("causa", S.INK, 2.4), ("pedido", S.DIF, 3.2)):
        y = ry[key]
        d = " ".join([_wave(SX1, LOCK1, y, 5.5), _wave(LOCK1, LOCK2, y, 2.6)[len(f"M{LOCK1:.1f},{y:.1f}"):], f"L{SEN0},{y}"])
        o.append(S.path(d, fill="none", stroke=col, stroke_width=sw, stroke_linejoin="round"))
    for xl in (LOCK1, LOCK2):
        o.append(S.line(xl, yc - 22, xl, ry["valor"] - 4, stroke=S.CONC, stroke_width=2.6))
        o.append(S.line(xl, 92, xl, yc - 22, stroke=S.CONC, stroke_width=1, stroke_dasharray="2 4"))
    # thread names, in the clear stretch after the saneamento
    for key, lab, col in (("partes", "partes", S.INK), ("causa", "causa de pedir", S.INK), ("pedido", "pedido", S.DIF)):
        o.append(_t(FLD1 + 24, ry[key] - 9, lab, 13, family=S.SANS, fill=col, weight="600"))
    # valor: a short thread that ends in the contestação (the réu may impugn it)
    yv = ry["valor"]
    o.append(S.path(f"M{SX1},{yv} H{DEF0}", fill="none", stroke=S.INK, stroke_width=1.6))
    # provas: under the contestação, begins the instrução, then runs up into the sentença
    ypv = ry["provas"]
    sb = yd + 30
    o.append(S.path(f"M{SX1},{ypv} H{INS0} H{INS0 + 90} C{INS0 + 124},{ypv} {SEN0 + 34},{sb + 8} {SEN0 + 34},{sb}", fill="none",
                    stroke=S.INK, stroke_width=1.8))
    o.append(_ring(INS0, ypv))
    o.append(_t(INS0 + 12, ypv - 9, "instrução", 13, family=S.SERIF, fill=S.INK2, font_style="italic"))
    # audiência: a mark on its own thread, after the citação
    ya = ry["audiencia"]
    o.append(S.path(f"M{SX1},{ya} H{CITX + 50}", fill="none", stroke=S.INK, stroke_width=1.6))
    o.append(_ring(CITX + 50, ya))
    o.append(_t(CITX + 62, ya + 4.5, "audiência", 13, family=S.SERIF, fill=S.INK2, font_style="italic"))

    # ── 5. the contestação lies across the threads it answers
    top, bot = yp - 40, yv + 22
    o += _paper(DEF0, top, DEF1, bot, stroke=S.INK, sw=1.5)
    o.append(_t(DEF0 + 14, top + 22, "Contestação", 17, family=S.SERIF, fill=S.INK, weight="600"))
    for key, lab in (("partes", "partes"), ("causa", "fatos"), ("pedido", "pedido"), ("valor", "valor")):
        y = ry[key]
        o.append(S.circle(DEF0, y, 3.5, fill=S.PAPER, stroke=S.INK, stroke_width=1.4))
        if key != "valor":
            o.append(S.circle(DEF1, y, 3.5, fill=S.PAPER, stroke=S.INK, stroke_width=1.4))
        o.append(_t(DEF0 + 16, y + 4.5, lab, 13.5, family=S.SERIF, fill=S.INK2, font_style="italic"))
    # the réu's own thread joins the saneamento field
    yf0, yf1 = yc - 18, yd + 18
    o.append(S.path(f"M{DEF1},{yv - 8} C{DEF1 + 24},{yv - 8} {FLD0 - 24},{yd + 8} {FLD0},{yd + 8}", fill="none", stroke=S.INK2,
                    stroke_width=3, stroke_linecap="round"))

    # ── 6. the saneamento field: where the two stories become the questions to decide
    o.append(S.rect(FLD0, yf0, FLD1 - FLD0, yf1 - yf0, fill=S.PAPER2, stroke=S.DIF, stroke_width=1.4, stroke_dasharray="5 4"))
    o.append(_t(FLD0 + 10, (yc + yd) / 2 + 4.5, "questões de fato", 13, family=S.SERIF, fill=S.DIF, weight="600",
                data_color_role="decided"))
    for key, col, sw in (("causa", S.INK, 2.4), ("pedido", S.DIF, 3.2)):   # repaint the threads over the field's fill
        y = ry[key]
        o.append(S.path(f"M{FLD0 - 2},{y} H{FLD1 + 2}", fill="none", stroke=col, stroke_width=sw))
    o.append(S.path(f"M{FLD1 - 6},{yf1} V{ypv}", fill="none", stroke=S.INK2, stroke_width=2))
    o.append(S.circle(FLD1 - 6, ypv, 4, fill=S.INK2))

    # ── 7. the sentença sheet and the ceiling
    o += _paper(SEN0, yp - 40, SEN1, sb, stroke=S.INK, sw=1.6)
    o.append(_t(SEN0 + 14, yp - 18, "Sentença", 17, family=S.SERIF, fill=S.INK, weight="600"))
    for key in ("partes", "causa"):
        o.append(S.circle(SEN0, ry[key], 3.8, fill=S.INK))
    o.append(S.circle(SEN0, yd, 4.5, fill=S.DIF))
    o.append(S.path(f"M{SEN0 + 6},{yd + 6} H{SEN1 - 14}", fill="none", stroke=S.DIF, stroke_width=2.4))
    o.append(_t(SEN0 + 14, yd + 22, "dispositivo", 13, family=S.SERIF, fill=S.DIF, data_color_role="decided"))
    o.append(S.line(SEN0 - 14, yd - 14, SEN0 - 14, yd + 14, stroke=S.CONC, stroke_width=3))
    o.append(S.line(SEN0 - 8, yd - 14, SEN0 - 8, yd + 14, stroke=S.CONC, stroke_width=3))
    o.append(_t(SEN0 - 24, yd + 31, "arts. 141 e 492", 11.5, fill=S.CONC, anchor="end", data_color_role="limit"))

    # ── 8. the shortcut: over the top, conditioned
    a0, a1 = DEF1 - 30, SEN0 + 40
    ytop = yp - 40
    o.append(S.path(f"M{a0},{ytop} C{a0 + 30},{ytop - 46} {a1 - 30},{ytop - 46} {a1},{ytop}", fill="none", stroke=S.CONC,
                    stroke_width=2.2, stroke_dasharray="7 5"))
    o.append(S.path(f"M{a1 - 8},{ytop - 9} L{a1},{ytop} L{a1 - 11},{ytop - 2}", fill="none", stroke=S.CONC, stroke_width=2.2,
                    stroke_linecap="round", stroke_linejoin="round"))
    lab = "julgamento antecipado · art. 355"
    xm = (a0 + a1) / 2
    o.append(S.rect(xm - _tw(lab, 12, S.MONO) / 2 - 16, ytop - 41, _tw(lab, 12, S.MONO) + 28, 17, fill=S.PAPER))
    o.append(_t(xm, ytop - 28, lab, 12, fill=S.CONC, anchor="middle", data_color_role="limit"))

    # ── 9. the fence and the cumprimento: a ring on a dashed thread, then what the original Buzaid text did
    o.append(S.line(FENCE, SHEET_TOP - 6, FENCE, SLAB_Y0, stroke=S.MUTED, stroke_width=1.4, stroke_dasharray="3 5"))
    o.append(S.path(f"M{SEN1},{yp + 8} H{CUMX - 6}", fill="none", stroke=S.INK, stroke_width=1.8, stroke_dasharray="8 4"))
    o.append(_ring(CUMX, yp + 8))
    o.append(_t(FENCE + 10, yp - 5, "cumprimento", 13, family=S.SERIF, fill=S.INK2, font_style="italic"))
    for i, ln in enumerate(["no texto original", "de 1973, outro", "processo; hoje,", "os mesmos autos"]):
        o.append(_t(FENCE + 12, yp + 56 + i * 16, ln, 12.5, family=S.SERIF, fill=S.MUTED, font_style="italic"))

    # ── 10. the rail: one row of text buttons, the lower figures' look; the page lights the pressed one
    rail = [("pedido", "Pedido"), ("causa", "Causa de pedir"), ("partes", "Partes"), ("emenda", "Emenda"),
            ("alterar", "Alteração"), ("atalho", "Julgamento antecipado")]
    rail_nodes: dict[str, str] = {}
    rx = SX0
    for oid, lab in rail:
        bw = round(_tw(lab, 15.5, S.SANS) + 32)
        rail_nodes[oid] = (S.rect(rx, RAIL_Y, bw, RAIL_H, fill=S.PAPER, stroke=S.INK, stroke_width=1, class_="rail")
                           + S.text(rx + bw / 2, RAIL_Y + 21, lab, size=15.5, family=S.SANS, weight="500", fill=S.INK,
                                    anchor="middle", class_="rail-t"))
        rx += bw + 9

    # ── 11. the pressable relations and their traces
    objects: list[dict] = []
    row = lambda y: (SX0 + 6, y - 14, SX1 - SX0 - 12, 28)
    traces = {
        "pedido": [S.path(f"M{SX1},{yd} H{SEN0}", fill="none", stroke=S.DIF, stroke_width=6, opacity=".35"),
                   S.rect(*row(yd), fill="none", stroke=S.DIF, stroke_width=2)],
        "causa": [S.path(f"M{SX1},{yc} H{FLD1}", fill="none", stroke=S.DIF, stroke_width=6, opacity=".35"),
                  S.rect(*row(yc), fill="none", stroke=S.DIF, stroke_width=2),
                  S.rect(FLD0, yf0, FLD1 - FLD0, yf1 - yf0, fill="none", stroke=S.DIF, stroke_width=2.4)],
        "partes": [S.path(f"M{SX1},{yp} H{SEN0}", fill="none", stroke=S.DIF, stroke_width=6, opacity=".35"),
                   S.rect(*row(yp), fill="none", stroke=S.DIF, stroke_width=2),
                   S.circle(CITX, yp, 10, fill="none", stroke=S.DIF, stroke_width=2.4)],
        "emenda": [S.path(f"M{DX + 2},{yj - 10} C{DX + 4},{yj - 52} {SX1 - 40},{yj - 52} {SX1 - 34},{SHEET_TOP + 3}", fill="none",
                          stroke=S.DIF, stroke_width=3.4),
                   S.path(f"M{DX},{yj - 9} L{DX + 9},{yj} L{DX},{yj + 9} L{DX - 9},{yj} Z", fill=S.DIF, stroke=S.DIF)],
        "alterar": [S.line(LOCK1, 92, LOCK1, ry["valor"] - 4, stroke=S.CONC, stroke_width=5, opacity=".45"),
                    S.line(LOCK2, 92, LOCK2, ry["valor"] - 4, stroke=S.CONC, stroke_width=5, opacity=".45"),
                    S.line(xa + 2, 64, xb - 2, 64, stroke=S.CONC, stroke_width=4)],
        "atalho": [S.path(f"M{a0},{ytop} C{a0 + 30},{ytop - 46} {a1 - 30},{ytop - 46} {a1},{ytop}", fill="none", stroke=S.CONC,
                          stroke_width=5, opacity=".3")],
    }
    labels = {
        "pedido": "Pedido: o que a petição pede limita a sentença.",
        "causa": "Causa de pedir: os fatos que a ré enfrenta e que o saneamento organiza.",
        "partes": "Partes: quem a citação chama e quem a sentença alcança.",
        "emenda": "Emenda: o juiz devolve a petição para correção.",
        "alterar": "Alteração: quando o pedido e a causa de pedir ainda podem mudar.",
        "atalho": "Julgamento antecipado: quando a causa dispensa a instrução.",
    }
    hits = {
        "pedido": row(yd), "causa": row(yc), "partes": row(yp),
        "emenda": (SX1 - 50, SHEET_TOP - 10, 100, yj + 14 - SHEET_TOP + 10),
        "alterar": (xa, 56, xb - xa, 36),
        "atalho": (a0, ytop - 56, a1 - a0, 60),
    }
    for oid, layer in traces.items():
        o.append(_group(layer, data_object_state=oid, data_state="active", visibility="hidden"))
    for oid, _lab in rail:
        o.append(_group([rail_nodes[oid]], data_object=oid, role="button", tabindex="0", aria_label=labels[oid]))
    for oid, (hx, hy, hw, hh) in hits.items():
        o.append(_group([_hit(hx, hy, hw, hh)], data_object=oid, role="button", tabindex="0", aria_label=labels[oid]))
        objects.append({"id": oid, "label": labels[oid].split(":")[0], "description": labels[oid]})
    title = p.get("title") or ("Planta da causa: a petição inicial entrega à causa seus fios (partes, causa de pedir, pedido); "
                               "a contestação responde por cima deles; o pedido chega ao dispositivo da sentença e a limita")
    return S.svg(W, H, title, o), objects
