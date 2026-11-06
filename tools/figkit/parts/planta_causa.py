"""planta_causa: the planta of a cause in the fase de conhecimento (chairman 05/11: the hero is "a map you stop and look
at for a minute or two and go: ah, that makes sense"; Controle's planta is the bar).

Not a row of stations. The petition is a standing sheet whose seven requisites (art. 319) are hooks; the demand's own
elements leave it as threads that run through the stages and meet the other papers of the case. Position carries the
meaning: the stages are bands along the autos (the case file seen edge-on, base of the plan); the threads that can
still change are wavy and become straight where art. 329 fixes them (orange locks); the contestação lies across the
threads it answers; the pedido's blue thread is the only one that reaches the sentença's dispositivo and stops at the
ceiling of arts. 141 and 492; the shortcut is an orange dashed ribbon over the top; the 1973 fence stands before the
cumprimento. Everything is computed from the constants below, so no label is placed twice by hand.

Params (facts, never coordinates):
  title   optional accessible title
Objects (pressable; the page writes the answer in a fixed slot and toggles the matching state layer):
  pedido, causa, partes, emenda, alterar, atalho
Contract (same as abertura_civil): <g data-object=ID role=button tabindex=0> targets, <g data-object-state=ID
data-state=active visibility=hidden> traces.
"""
from __future__ import annotations

from . import svg as S

W, H = 1140, 552
ROWS = {"juizo": 0, "partes": 1, "causa": 2, "pedido": 3, "valor": 4, "provas": 5, "audiencia": 6}
Y0, DY = 196, 36
RY = {k: Y0 + DY * i for k, i in ROWS.items()}

SX0, SX1 = 30, 214                 # petition sheet
DX = 238                           # the juiz reads (diamond, emenda loop)
CX0, CX1 = 262, 350                # citação box
LOCK1, LOCK2 = 374, 592            # art. 329, I and II
DEF0, DEF1 = 410, 556              # contestação sheet
FLD0, FLD1 = 610, 756              # saneamento field
INS0, INS1 = 766, 880              # instrução box
SEN0, SEN1 = 896, 1010             # sentença sheet
FENCE = 1032
CUM0, CUM1 = 1048, 1134
SLAB_Y0, SLAB_Y1 = 478, 514
SHEET_TOP = 152

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
    """Pairs of registered labels whose boxes intersect (dev check; run after build)."""
    out = []
    for i, a in enumerate(_boxes):
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


def _halo(x, y, w, h):
    return S.rect(x, y, w, h, fill=S.PAPER)


def _group(body, **attrs):
    return f'<g {S.attrs(**attrs)}>{"".join(body)}</g>'


def _writing(x, y, widths, gap=12):
    return [S.line(x, y + i * gap, x + w, y + i * gap, stroke=S.GRID, stroke_width=1) for i, w in enumerate(widths)]


def _paper(x0, y0, x1, y1, stroke=S.INK, sw=1.5, fold=14):
    return [S.path(f"M{x0},{y0} H{x1 - fold} L{x1},{y0 + fold} V{y1} H{x0} Z", fill=S.PAPER, stroke=stroke, stroke_width=sw,
                   stroke_linejoin="round"),
            S.path(f"M{x1 - fold},{y0} V{y0 + fold} H{x1}", fill="none", stroke=stroke, stroke_width=1)]


def _badge(n, href, x, y):
    return (f'<a href="{href}">' + S.rect(x, y, 26, 18, fill=S.PAPER, stroke=S.INK, stroke_width=1.2)
            + S.text(x + 13, y + 13, n, size=11, fill=S.INK, anchor="middle", weight="600") + "</a>")


def _hit(x, y, w, h, mark=False):
    return S.rect(x, y, w, h, fill="none", stroke=S.MUTED if mark else "none", stroke_width=1, stroke_dasharray="3 4", pointer_events="all", class_="object-mark hit")


def build(p: dict) -> tuple[str, list[dict]]:
    _boxes.clear()
    o: list[str] = []
    ry = RY

    # ── 1. the scale along the top: phase, stages, and how free the demand is to change
    xa, xb = SX0, 1010
    o.append(S.path(f"M{xa},{40} V34 H{xb} V40", fill="none", stroke=S.DIF, stroke_width=1.4))
    o.append(_t((xa + xb) / 2, 26, "FASE DE CONHECIMENTO", 12.5, fill=S.DIF, anchor="middle", letter_spacing=".1em"))
    stages = [("POSTULAR", xa, LOCK2), ("ORGANIZAR", LOCK2, 764), ("INSTRUIR", 764, 888), ("DECIDIR", 888, xb)]
    for lab, a, b in stages:
        o.append(S.path(f"M{a + 2},{70} V64 H{b - 2} V70", fill="none", stroke=S.INK2, stroke_width=1.1))
        o.append(_t((a + b) / 2, 56, lab, 12, fill=S.INK2, anchor="middle", letter_spacing=".08em"))
    zones = [(xa, LOCK1, "ALTERA SOZINHA", "art. 329, I · citação"),
             (LOCK1, LOCK2, "ALTERA COM O RÉU", "art. 329, II · saneamento"),
             (LOCK2, xb, "FECHADA", "salvo acordo · art. 190")]
    for a, b, head, art in zones:
        o.append(S.line(a + 2, 88, b - 2, 88, stroke=S.CONC, stroke_width=1.6))
        o.append(S.line(a + 2, 88, a + 2, 96, stroke=S.CONC, stroke_width=1.6))
        o.append(_t(a + 10, 110, head, 12.5, family=S.SANS, fill=S.CONC, weight="600", data_color_role="limit"))
        o.append(_t(a + 10, 126, art, 11.5, fill=S.MUTED))
    o.append(S.line(xb - 2, 88, xb - 2, 96, stroke=S.CONC, stroke_width=1.6))

    # ── 2. the autos edge-on, the base of the plan; the stage flags stand on it
    SLAB_X1 = CUM1
    o.append(S.rect(SX0, SLAB_Y0, SLAB_X1 - SX0, SLAB_Y1 - SLAB_Y0, fill=S.PAPER2, stroke=S.INK, stroke_width=1.4))
    xk = SX0 + 4
    while xk < SLAB_X1 - 2:
        o.append(S.line(xk, SLAB_Y0 + 1, xk, SLAB_Y1 - 1, stroke=S.GRID, stroke_width=1))
        xk += 4
    for fx in (SX1, CX0 - 8, DEF0 - 8, LOCK2, 764, 888, FENCE):
        o.append(S.line(fx, SLAB_Y0, fx, SLAB_Y1, stroke=S.INK, stroke_width=1.6))
    o.append(S.rect(SX0, SLAB_Y1 + 6, 232, 22, fill=S.INK))
    o.append(_t(SX0 + 12, SLAB_Y1 + 21, "AUTOS · PROCEDIMENTO COMUM", 11.5, fill=S.PAPER, letter_spacing=".06em"))
    flags = [("PETIÇÃO", SX0 + 6), ("CITAÇÃO", CX0 - 8), ("CONTESTAÇÃO", DEF0 - 8), ("SANEAMENTO", LOCK2 + 4),
             ("INSTRUÇÃO", 768), ("SENTENÇA", 892), ("CUMPRIMENTO", FENCE)]
    for lab, fx in flags:
        o.append(S.line(fx, SLAB_Y0 - 22, fx, SLAB_Y0, stroke=S.INK, stroke_width=1.4))
        w = len(lab) * 7.2 + 16
        o.append(S.path(f"M{fx},{SLAB_Y0 - 22} h{w} l-7,9 l7,9 h-{w} Z", fill=S.PAPER, stroke=S.INK, stroke_width=1.2))
        o.append(_t(fx + 8, SLAB_Y0 - 9, lab, 11.5, fill=S.INK, letter_spacing=".04em"))

    # ── 3. the petition sheet: seven requisites, each a hook the threads leave from
    o += _paper(SX0, SHEET_TOP, SX1, Y0 + DY * 6 + 22, stroke=S.DIF, sw=1.8)
    o.append(_t(SX0 + 16, SHEET_TOP + 26, "Petição inicial", 18, family=S.SERIF, fill=S.INK, weight="600", reg=True))
    names = [("I", "juízo", "juizo"), ("II", "partes", "partes"), ("III", "causa de pedir", "causa"),
             ("IV", "pedido", "pedido"), ("V", "valor", "valor"), ("VI", "provas", "provas"),
             ("VII", "audiência", "audiencia")]
    for i, (rom, nm, key) in enumerate(names):
        y = ry[key]
        if i:
            o.append(S.line(SX0 + 12, y - DY / 2, SX1 - 12, y - DY / 2, stroke=S.GRID, stroke_width=1))
        o.append(_t(SX0 + 16, y + 5, rom, 11, fill=S.MUTED))
        o.append(_t(SX0 + 52, y + 5, nm, 15.5, family=S.SERIF, fill=S.INK))
        o.append(S.circle(SX1, y, 4.5, fill=S.INK))
    
    # ── 4. the threads
    # juízo reads the petition: diamond, then the citação; the emenda loop returns to the sheet's top
    yj, yp, yc, yd = ry["juizo"], ry["partes"], ry["causa"], ry["pedido"]
    o.append(S.path(f"M{SX1},{yj} H{CX0}", fill="none", stroke=S.INK, stroke_width=2.2))
    o.append(S.path(f"M{DX},{yj - 9} L{DX + 9},{yj} L{DX},{yj + 9} L{DX - 9},{yj} Z", fill=S.PAPER, stroke=S.INK, stroke_width=2.2))
    o.append(S.path(f"M{DX + 2},{yj - 10} C{DX + 4},{yj - 52} {SX1 - 40},{yj - 52} {SX1 - 34},{SHEET_TOP + 3}", fill="none",
                    stroke=S.INK, stroke_width=1.6))
    o.append(S.path(f"M{SX1 - 40},{SHEET_TOP - 8} L{SX1 - 34},{SHEET_TOP + 2} L{SX1 - 27},{SHEET_TOP - 7}", fill="none", stroke=S.INK, stroke_width=1.6,
                    stroke_linecap="round", stroke_linejoin="round"))
    # citação box: receives juízo and partes
    o.append(S.rect(CX0, yj - 24, CX1 - CX0, yp - yj + 48, fill=S.PAPER, stroke=S.INK, stroke_width=1.5))
    o.append(_t(CX0 + 10, yj - 6, "CITAÇÃO", 12.5, fill=S.INK, weight="600"))
    o.append(_t(CX0 + 10, yj + 14, "art. 238", 11.5, fill=S.MUTED))
    o.append(_t(CX0 + 10, yp + 14, "a ré é chamada", 13, family=S.SERIF, fill=S.INK2))
    # partes: straight, thin, from the sheet through the citação to the sentença
    o.append(S.path(f"M{SX1},{yp} H{CX0}", fill="none", stroke=S.INK, stroke_width=2.2))
    o.append(S.path(f"M{CX1},{yp} H{SEN0}", fill="none", stroke=S.INK, stroke_width=2.2))
    # causa and pedido: wavy where they can still change, straight where art. 329 fixes them
    for key, col, sw in (("causa", S.INK, 2.4), ("pedido", S.DIF, 3.2)):
        y = ry[key]
        d = " ".join([_wave(SX1, LOCK1, y, 5.5), _wave(LOCK1, LOCK2, y, 2.6)[len(f"M{LOCK1:.1f},{y:.1f}"):],
                      f"L{SEN0},{y}"])
        o.append(S.path(d, fill="none", stroke=col, stroke_width=sw, stroke_linejoin="round"))
    for xl in (LOCK1, LOCK2):
        o.append(S.line(xl, yc - 22, xl, ry["valor"] - 4, stroke=S.CONC, stroke_width=2.6))
        o.append(S.line(xl, 132, xl, yc - 22, stroke=S.CONC, stroke_width=1, stroke_dasharray="2 4"))
    # thread names, in the clear stretch after the citação
    for key, lab, col, lx in (("partes", "partes", S.INK, FLD1 + 24), ("causa", "causa de pedir", S.INK, FLD1 + 24),
                              ("pedido", "pedido", S.DIF, FLD1 + 24)):
        o.append(_t(lx, ry[key] - 9, lab, 13, family=S.SANS, fill=col, weight="600"))
    # valor: a short thread that ends in the contestação (the réu may impugn it)
    yv = ry["valor"]
    o.append(S.path(f"M{SX1},{yv} H{DEF0}", fill="none", stroke=S.INK, stroke_width=1.6))
    # provas: under the contestação, to the instrução
    ypv = ry["provas"]
    o.append(S.path(f"M{SX1},{ypv} H{INS0}", fill="none", stroke=S.INK, stroke_width=1.6))
    o.append(_t(DEF0 - 2, ypv + 22, "documentos já com a inicial · art. 320", 11.5, fill=S.MUTED))
    # audiência: a box before the contestação
    ya = ry["audiencia"]
    o.append(S.path(f"M{SX1},{ya} H{CX0}", fill="none", stroke=S.INK, stroke_width=1.6))
    o.append(S.rect(CX0, ya - 15, 168, 30, fill=S.PAPER, stroke=S.INK, stroke_width=1.5))
    o.append(_t(CX0 + 10, ya + 4, "AUDIÊNCIA · art. 334", 12, fill=S.INK))

    # ── 5. the contestação lies across the threads it answers
    top, bot = yp - 46, yv + 22
    o += _paper(DEF0, top, DEF1, bot, stroke=S.INK, sw=1.5)
    o.append(_t(DEF0 + 14, top + 24, "Contestação", 17, family=S.SERIF, fill=S.INK, weight="600"))
    for key, lab in (("partes", "partes"), ("causa", "fatos"), ("pedido", "pedido"), ("valor", "valor")):
        y = ry[key]
        o.append(S.circle(DEF0, y, 3.5, fill=S.PAPER, stroke=S.INK, stroke_width=1.4))
        if key != "valor":
            o.append(S.circle(DEF1, y, 3.5, fill=S.PAPER, stroke=S.INK, stroke_width=1.4))
        o.append(_t(DEF0 + 16, y + 4.5, lab, 13.5, family=S.SERIF, fill=S.INK2, font_style="italic"))
    o.append(_t(DEF1 - 16, yv + 4.5, "impugna", 13.5, family=S.SERIF, fill=S.INK2, anchor="end", font_style="italic"))
    # the réu's own thread joins the saneamento field
    yf0, yf1 = yc - 18, yd + 18
    o.append(S.path(f"M{DEF1},{yv - 8} C{DEF1 + 24},{yv - 8} {FLD0 - 24},{yd + 8} {FLD0},{yd + 8}", fill="none", stroke=S.INK2,
                    stroke_width=3, stroke_linecap="round"))

    # ── 6. the saneamento field: where the two stories become the questions to decide
    o.append(S.rect(FLD0, yf0, FLD1 - FLD0, yf1 - yf0, fill=S.PAPER2, stroke=S.DIF, stroke_width=1.4, stroke_dasharray="5 4"))
    o.append(_t(FLD0 + 8, (yc + yd) / 2 + 5, "fatos controvertidos", 13, family=S.SERIF, fill=S.DIF, weight="600",
                data_color_role="decided"))
    # repaint the two threads over the field's fill
    for key, col, sw in (("causa", S.INK, 2.4), ("pedido", S.DIF, 3.2)):
        y = ry[key]
        o.append(S.path(f"M{FLD0 - 2},{y} H{FLD1 + 2}", fill="none", stroke=col, stroke_width=sw))
    # from the field to the instrução, and the instrução to the sentença
    yi = ypv
    o.append(S.rect(INS0, yi - 18, INS1 - INS0, 36, fill=S.PAPER, stroke=S.INK, stroke_width=1.5))
    o.append(_t(INS0 + 10, yi - 2, "INSTRUÇÃO", 12.5, fill=S.INK, weight="600"))
    o.append(_t(INS0 + 10, yi + 12, "arts. 369 ss.", 11, fill=S.MUTED))
    o.append(S.path(f"M{FLD1 - 6},{yf1} V{yi}",
                    fill="none", stroke=S.INK2, stroke_width=2))
    o.append(S.circle(FLD1 - 6, yi, 4, fill=S.INK2))

    # ── 7. the sentença sheet and the ceiling
    sb = yd + 30
    o += _paper(SEN0, yp - 46, SEN1, sb, stroke=S.INK, sw=1.6)
    o.append(_t(SEN0 + 14, yp - 22, "Sentença", 17, family=S.SERIF, fill=S.INK, weight="600"))
    for key in ("partes", "causa"):
        o.append(S.circle(SEN0, ry[key], 3.8, fill=S.INK))
    o.append(S.circle(SEN0, yd, 4.5, fill=S.DIF))
    o.append(S.path(f"M{SEN0 + 6},{yd + 6} H{SEN1 - 14}", fill="none", stroke=S.DIF, stroke_width=2.4))
    o.append(_t(SEN0 + 14, yd + 22, "dispositivo", 13, family=S.SERIF, fill=S.DIF, data_color_role="decided"))
    o.append(S.path(f"M{INS1},{yi} C{INS1 + 34},{yi} {SEN0 + 34},{sb + 4} {SEN0 + 34},{sb}", fill="none", stroke=S.INK2,
                    stroke_width=2))
    # the ceiling: an orange bar across the pedido's thread at the sheet's edge, and its words
    o.append(S.line(SEN0 - 14, yd - 14, SEN0 - 14, yd + 14, stroke=S.CONC, stroke_width=3))
    o.append(S.line(SEN0 - 8, yd - 14, SEN0 - 8, yd + 14, stroke=S.CONC, stroke_width=3))
    o.append(_t(SEN0 - 24, yd + 30, "o pedido é o teto", 13, family=S.SERIF, fill=S.CONC, anchor="end", data_color_role="limit"))
    o.append(_t(SEN0 - 24, yd + 46, "arts. 141 e 492", 11.5, fill=S.CONC, anchor="end", data_color_role="limit"))

    # ── 8. the shortcut: over the top, conditioned
    a0, a1 = DEF1 - 30, SEN0 + 40
    ytop = yp - 46
    o.append(S.path(f"M{a0},{ytop} C{a0 + 30},{ytop - 46} {a1 - 30},{ytop - 46} {a1},{ytop}", fill="none", stroke=S.CONC,
                    stroke_width=2.2, stroke_dasharray="7 5"))
    o.append(S.path(f"M{a1 - 8},{ytop - 9} L{a1},{ytop} L{a1 - 11},{ytop - 2}", fill="none", stroke=S.CONC, stroke_width=2.2,
                    stroke_linecap="round", stroke_linejoin="round"))
    lab = "julgamento antecipado · art. 355"
    xm = (a0 + a1) / 2
    o.append(_halo(xm - _tw(lab, 12, S.MONO) / 2 - 6, ytop - 41, _tw(lab, 12, S.MONO) + 12, 17))
    o.append(_t(xm, ytop - 28, lab, 12, fill=S.CONC, anchor="middle", data_color_role="limit"))

    # ── 9. the 1973 fence and the cumprimento
    o.append(S.line(FENCE, 150, FENCE, SLAB_Y0, stroke=S.MUTED, stroke_width=1.4, stroke_dasharray="3 5"))
    o.append(S.path(f"M{SEN1},{yp + 8} H{CUM0}", fill="none", stroke=S.INK, stroke_width=1.8, stroke_dasharray="8 4"))
    o.append(S.rect(CUM0, yp - 12, CUM1 - CUM0, 40, fill=S.PAPER, stroke=S.INK, stroke_width=1.5))
    o.append(_t(CUM0 + 8, yp + 4, "CUMPRIMENTO", 11.5, fill=S.INK, weight="600"))
    o.append(_t(CUM0 + 8, yp + 20, "art. 513", 11, fill=S.MUTED))
    for i, ln in enumerate(["em 1973,", "outro processo;", "hoje, os", "mesmos autos"]):
        o.append(_t(FENCE + 16, yp + 76 + i * 17, ln, 13, family=S.SERIF, fill=S.MUTED, font_style="italic"))

    # ── 10. chapter badges: the plan is the lesson's table of contents
    for n, href, bx, by in (("01", "#conhecer", FENCE + 16, ry["partes"] + 38), ("02", "#demanda", SX0, SHEET_TOP - 24),
                            ("03", "#peticao", SX1 + 10, ry["audiencia"] + 24),
                            ("04", "#pedidos", CX1 + 14, ry["valor"] + 8),
                            ("05", "#emenda", DX + 22, ry["juizo"] - 52),
                            ("06", "#alteracao", xb - 36, 100)):
        o.append(_badge(n, href, bx, by))
    o.append(_t(DX + 54, ry["juizo"] - 37, "emenda", 12, fill=S.INK))

    # ── 12. the pressable relations and their traces
    objects: list[dict] = []
    traces = {
        "pedido": [S.path(f"M{SX1},{yd} " + f"H{SEN0}", fill="none", stroke=S.DIF, stroke_width=6, opacity=".35"),
                   S.rect(SX0 + 6, yd - 17, SX1 - SX0 - 12, 34, fill="none", stroke=S.DIF, stroke_width=2)],
        "causa": [S.path(f"M{SX1},{yc} H{FLD1}", fill="none", stroke=S.DIF, stroke_width=6, opacity=".35"),
                  S.rect(SX0 + 6, yc - 17, SX1 - SX0 - 12, 34, fill="none", stroke=S.DIF, stroke_width=2),
                  S.rect(FLD0, yf0, FLD1 - FLD0, yf1 - yf0, fill="none", stroke=S.DIF, stroke_width=2.4)],
        "partes": [S.path(f"M{SX1},{yp} H{SEN0}", fill="none", stroke=S.DIF, stroke_width=6, opacity=".35"),
                   S.rect(SX0 + 6, yp - 17, SX1 - SX0 - 12, 34, fill="none", stroke=S.DIF, stroke_width=2),
                   S.rect(CX0, yj - 24, CX1 - CX0, yp - yj + 48, fill="none", stroke=S.DIF, stroke_width=2.4)],
        "emenda": [S.path(f"M{DX + 2},{yj - 10} C{DX + 4},{yj - 52} {SX1 - 40},{yj - 52} {SX1 - 34},{155}", fill="none",
                          stroke=S.DIF, stroke_width=3.4),
                   S.path(f"M{DX},{yj - 9} L{DX + 9},{yj} L{DX},{yj + 9} L{DX - 9},{yj} Z", fill=S.DIF, stroke=S.DIF)],
        "alterar": [S.line(LOCK1, 132, LOCK1, ry["valor"] - 4, stroke=S.CONC, stroke_width=5, opacity=".45"),
                    S.line(LOCK2, 132, LOCK2, ry["valor"] - 4, stroke=S.CONC, stroke_width=5, opacity=".45"),
                    S.line(xa + 2, 88, xb - 2, 88, stroke=S.CONC, stroke_width=4)],
        "atalho": [S.path(f"M{a0},{ytop} C{a0 + 30},{ytop - 46} {a1 - 30},{ytop - 46} {a1},{ytop}", fill="none", stroke=S.CONC,
                          stroke_width=5, opacity=".5")],
    }
    hits = {
        "pedido": (SX0 + 6, yd - 17, SX1 - SX0 - 12, 34, "Pedido: o que a petição pede é o teto da sentença."),
        "causa": (SX0 + 6, yc - 17, SX1 - SX0 - 12, 34, "Causa de pedir: os fatos que a ré enfrenta e que o saneamento organiza."),
        "partes": (SX0 + 6, yp - 17, SX1 - SX0 - 12, 34, "Partes: quem a citação chama e quem a sentença alcança."),
        "emenda": (DX - 14, yj - 54, SX1 - DX + 8, 70, "Emenda: o juiz devolve a petição para correção antes de citar."),
        "alterar": (xa, 80, xb - xa, 50, "Alteração: quando o pedido e a causa de pedir ainda podem mudar."),
        "atalho": (a0, ytop - 56, a1 - a0, 60, "Julgamento antecipado: quando a causa dispensa a instrução."),
    }
    for oid, layer in traces.items():
        o.append(_group(layer, data_object_state=oid, data_state="active", visibility="hidden"))
    for n, (oid, (hx, hy, hw, hh, label)) in enumerate(hits.items(), 1):
        o.append(_group([_hit(hx, hy, hw, hh, mark=oid in ("pedido", "causa", "partes"))], data_object=oid, role="button", tabindex="0", aria_label=label))
        objects.append({"id": oid, "label": label.split(":")[0], "description": label})
    title = p.get("title") or ("Planta da causa: a petição inicial entrega à causa seus fios (partes, causa de pedir, pedido); "
                               "a contestação responde por cima deles; o pedido chega ao dispositivo da sentença e a limita")
    return S.svg(W, H, title, o), objects
