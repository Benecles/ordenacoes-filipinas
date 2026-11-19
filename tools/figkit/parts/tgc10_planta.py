"""Extinção dos contratos: the planta. One valid contract runs into execution and fans into three lanes (the end is
fulfilled, willed or frustrated); each lane carries its doors; all lanes reach one terminal, the extinction.

params: title; origin {name, art}; hub {name, art}; terminal {name, art};
lanes: [{id, label, note, doors: [{x, name, art, n, href}]}]  (three lanes: top, middle, bottom)
Positions come from the x of each door and the lane index.
"""
from . import svg as S

W, H = 1100, 400
X0, XH, XL, XT = 50, 235, 330, 940
YS = [84, 200, 316]


def build(p):
    out = []
    T = S.text
    o, h, tm = p["origin"], p["hub"], p["terminal"]
    yc = YS[1]
    out.append(S.line(X0, yc, XH, yc, stroke=S.INK, stroke_width=5))
    out.append(S.rect(X0 - 13, yc - 13, 26, 26, fill=S.INK, stroke=S.INK))
    out.append(S.circle(XH, yc, 9, fill=S.PAPER, stroke=S.INK, stroke_width=2.6))
    out.append(T(X0 - 13, yc - 40, o["name"], size=15, family=S.SANS, weight="600"))
    out.append(T(X0 - 13, yc - 21, o["art"], size=13, family=S.SERIF, fill=S.INK2))
    out.append(T(XH - 6, yc - 32, h["name"], size=15, family=S.SANS, weight="600", anchor="middle"))
    out.append(T(XH + 10, yc + 32, h["art"], size=13, family=S.SERIF, fill=S.INK2, anchor="end"))
    for i, ln in enumerate(p["lanes"]):
        y = YS[i]
        b = []
        b.append(S.path(f"M{XH},{yc} C{XH+45},{yc} {XH+45},{y} {XL},{y}", fill="none", stroke=S.INK, stroke_width=2.4))
        b.append(S.line(XL, y, XT - 40, y, stroke=S.INK, stroke_width=2.4))
        b.append(S.path(f"M{XT-40},{y} C{XT-18},{y} {XT-18},{yc} {XT},{yc}", fill="none", stroke=S.INK, stroke_width=2.4))
        b.append(T(XL + 10, y - 18, ln["label"], size=15, family=S.SANS, weight="600"))
        b.append(T(XL + 10, y + 26, ln["note"], size=13, family=S.SERIF, fill=S.INK2))
        for d in ln["doors"]:
            x = d["x"]
            b.append(S.circle(x, y, 8, fill=S.PAPER, stroke=S.INK, stroke_width=2.4))
            b.append(T(x, y - 18, d["name"], size=14, family=S.SANS, weight="600", anchor="middle"))
            b.append(T(x, y + 28, d["art"], size=13, family=S.SERIF, fill=S.INK2, anchor="middle"))
        out.append(f'<g data-thread="{S.esc(ln["id"])}" tabindex="0" role="button" aria-label="{S.esc(ln["label"])}">' + "".join(b) + "</g>")
    for i, ln in enumerate(p["lanes"]):
        for d in ln["doors"]:
            bx, by = d["x"] - 17, YS[i] + 40
            out.append(f'<a href="{S.esc(d["href"])}">' + S.rect(bx, by, 34, 21, fill=S.PAPER, stroke=S.INK, stroke_width=1.2)
                       + T(d["x"], by + 15, d["n"], size=13, fill=S.INK, anchor="middle", weight="600") + "</a>")
    out.append(S.rect(XT - 10, yc - 10, 20, 20, fill=S.DIF, transform=f"rotate(45 {XT} {yc})"))
    out.append(T(XT + 22, yc + 5, tm["name"], size=15, family=S.SANS, weight="600", fill=S.DIF))
    out.append(T(XT + 22, yc + 25, tm["art"], size=13, family=S.SERIF, fill=S.INK2))
    return S.svg(W, H, p.get("title", "planta"), out), []
