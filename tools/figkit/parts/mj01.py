"""mj01: the drawings of Metodologia Jurídica, Aula 01 (12/11), cast from the figure plan.

Every drawing is an arrangement the words only name: rails that cross, a text that stays while notes accumulate around
it, stacks whose order is the order of consultation, a balance that tips, a parcel two lines enclose without dividing.
No label sits in a box; no label carries an idea the drawing lacks. Text is only the names the prose already uses.

Params: mode (required) and, for stepped drawings, state (1-based).
  hero      1100x470  planta: three rails of sources through the schools to the sixteenth century
  consulta  1100x300  three stacks of volumes in the order of consultation (Novara, Modena, Sicília)
  volumes   372x430   the five school volumes; the Volumen parvum opened into its quires
  glosa     372x440   one folio, three states: glosses, cross-references, apparatus (1-3)
  parecer   372x350   two cities, the road across the border, the consilium sheet (1-3)
  terra     372x330   one parcel; two protections enclose all of it (1-3)
  vinculos  1100x390  two territories: land and acts stay, the person and the movables cross
  apresentacao 372x340 one document, two routes to one door; reason links them (1-2)
  autoridade 372x350  a balance: volumes against one contrary sheet (1-2)
  crise     1100x310  three desks, same two books, three orders of consultation
  depuracao 1100x290  layers lifted from the old text, the nucleus reappears
  vigencia  1100x370  only some lines of the Corpus find their match in use
  norma     372x336   a norm that is never repealed; the needs that drift from it; interpretation in the gap
  pontos    372x352   five stations sighting one question
  genero    372x372   nested circles: species in the contract in the legal relation
  razao     372x230   a pari and a fortiori on one threshold
  compilacoes 1100x250 the kingdoms' written compilations on a dated scale
  passo     1100x440  one passage of the Corpus under four tracing films, one per hand
  lin_glosa 372x376   the glosadores as a genealogy: master, disciples, the Glosa, Azo, the canonists
  lin_comenta 372x322 the comentadores in dated lifelines
  lin_humanismo 1100xN humanists and the usus modernus in dated lifelines
  jurisdicoes 1100x500 two shelves (civil, canon), two lands, the sin criterion routing a case; the local judge's road stops short
Colours are house tokens: blue = what governs / was decided, orange = the limit or the objection.
"""
from __future__ import annotations

import math

from . import svg as S

INK, INK2, MUTED, GRID, PAPER, PAPER2 = S.INK, S.INK2, S.MUTED, S.GRID, S.PAPER, S.PAPER2
BLUE, ORANGE = S.DIF, S.CONC


# ───────────────────────── helpers
def T(x, y, s, size=17, fill=INK, anchor=None, family=S.SERIF, **kw):
    return S.text(x, y, s, size=size, fill=fill, family=family, anchor=anchor, **kw)


def P(d, stroke=INK, w=1.6, fill="none", **kw):
    return S.path(d, fill=fill, stroke=stroke, stroke_width=w, stroke_linecap="round", stroke_linejoin="round", **kw)


def L(x1, y1, x2, y2, stroke=INK, w=1.4, **kw):
    return S.line(x1, y1, x2, y2, stroke=stroke, stroke_width=w, stroke_linecap="round", **kw)


def G(items, **kw):
    return f'<g {S.attrs(**kw)}>{"".join(items)}</g>'


def fade(items, on=True):
    return [G(items, class_="fade")] if on else list(items)


def curve(x0, y0, x1, y1):
    xm = (x0 + x1) / 2
    return f"M{x0} {y0} C{xm} {y0} {xm} {y1} {x1} {y1}"


def wave(x0, x1, y, amp=4.0, period=30):
    d, x, up = f"M{x0} {y}", x0, True
    while x < x1:
        nx = min(x + period / 2, x1)
        d += f" Q{(x + nx) / 2:.1f} {y - amp if up else y + amp:.1f} {nx:.1f} {y}"
        x, up = nx, not up
    return d


def writing(x, y, widths, gap=10, color=GRID, w=1.1):
    return [L(x, y + i * gap, x + wd, y + i * gap, color, w) for i, wd in enumerate(widths)]


def slab(x, y, w, h, dx=20, dy=-11, stroke=INK, sw=1.6, fill=PAPER, edge=True):
    """A volume lying flat: front, top and right faces. (x, y) is the front's top-left."""
    out = [S.path(f"M{x} {y} L{x + dx} {y + dy} H{x + w + dx} L{x + w} {y} Z", fill=fill, stroke=stroke, stroke_width=sw, stroke_linejoin="round"),
           S.path(f"M{x + w} {y} L{x + w + dx} {y + dy} V{y + h + dy} L{x + w} {y + h} Z", fill=fill, stroke=stroke, stroke_width=sw, stroke_linejoin="round"),
           S.rect(x, y, w, h, fill=fill, stroke=stroke, stroke_width=sw)]
    if edge:  # the page block: fine lines along the fore-edge
        out += [L(x + w + 5, y + 4, x + w + 5, y + h - 4 + dy + 0, INK2, .8)] if False else []
        out += [L(x + w + dx * .35, y + dy * .35 + 3, x + w + dx * .35, y + h + dy * .35 - 3, GRID, .8),
                L(x + w + dx * .7, y + dy * .7 + 3, x + w + dx * .7, y + h + dy * .7 - 3, GRID, .8)]
    return out


def sheet(x, y, w, h, skew=0, stroke=INK, sw=1.5, fill=PAPER):
    return S.path(f"M{x + skew} {y} H{x + w + skew} L{x + w} {y + h} H{x} Z", fill=fill, stroke=stroke, stroke_width=sw, stroke_linejoin="round")


def leaf(x, y, w, h, stroke=INK, sw=1.6, rows=0, gap=11, pad=10, color=GRID):
    out = [S.rect(x + 3, y + 4, w, h, fill=PAPER, stroke=GRID, stroke_width=1), S.rect(x, y, w, h, fill=PAPER, stroke=stroke, stroke_width=sw)]
    for i in range(rows):
        out.append(L(x + pad, y + pad + 4 + i * gap, x + w - pad - (7 if i % 3 == 2 else 0), y + pad + 4 + i * gap, color, 1.1))
    return out


def svg(w, h, title, body):
    return S.svg(w, h, title, body)


def carded(w, h, title, body):
    """A margin drawing on its own graph-paper card: offset shadow sheet, hairline edge, content inset 14 px."""
    frame = [S.rect(9, 10, w + 8, h + 8, fill=PAPER, stroke=GRID, stroke_width=1),
             S.rect(4, 4, w + 8, h + 8, fill=PAPER, stroke=INK2, stroke_width=1.3)]
    return svg(w + 22, h + 24, title, frame + [G(body, transform="translate(14 14)")])


def _state(p, n):
    s = int(p.get("state", 1))
    if not 1 <= s <= n:
        raise ValueError(f"mj01: state must be 1..{n}")
    return s


# ───────────────────────── hero: the planta
def _thread(key, label, hits, items):
    """One thread of the planta: the reader hovers or focuses any of its parts and the map lights the whole thread."""
    h = [P(d, "none", 22, class_="hit", pointer_events="stroke") for d in hits]
    return G(h + list(items), data_lk=key, tabindex=0, role="button", aria_label=label, class_="thread")


def hero(p):
    """The planta: time runs left to right at 1.55 px a year (1100 at x 150, 1700 at x 1080); three rails of sources; the
    schools' lives drawn to scale along the foot. Years are Hespanha's; no other date is drawn."""
    X0, K = 150, 1.55
    yx = lambda yr: X0 + (yr - 1100) * K
    rc, rr, rl = 112, 198, 288
    b = []
    # columns: Bolonha (to 1280), the Italian cities (to 1500), the sixteenth century on
    for x in (yx(1280), yx(1500)):
        b.append(L(x, 16, x, 346, GRID, 1, stroke_dasharray="2 6"))
    heads = [(290, "Bolonha · séc. XII–XIII", "glosadores"), (600, "Cidades italianas · séc. XIV–XV", "comentadores"),
             (925, "Séc. XVI em diante", "humanistas e usus modernus")]
    for cx, h1, h2 in heads:
        b += [T(cx, 24, h1, 13.5, family=S.SANS, anchor="middle", weight=600), T(cx, 41, h2, 12.5, fill=INK2, anchor="middle", font_style="italic")]
    dot = lambda y: S.circle(X0, y, 5, fill=PAPER, stroke=INK, stroke_width=2)
    lab = lambda y, s: T(X0 - 14, y + 4.5, s, 13.5, anchor="end")
    # canônico: the five collections as spines, then a rail bounded by the sin criterion
    can = [P(f"M{X0} {rc} H{X0 + 930}", INK, 2.6), dot(rc), lab(rc, "canônico")]
    for i in range(5):
        can += [S.rect(166 + i * 15, rc - 38, 11, 38, fill=PAPER, stroke=INK, stroke_width=1.5), L(166 + i * 15, rc - 28, 177 + i * 15, rc - 28, INK, 1), L(166 + i * 15, rc - 9, 177 + i * 15, rc - 9, INK, 1)]
    can += [T(252, rc - 38, "Decretum e Decretais,", 12.5), T(252, rc - 24, "Sexto, Clementinas,", 12.5), T(252, rc - 10, "Extravagantes", 12.5)]
    can += [T(166, rc + 22, "Hostiense · Penyafort", 12.5, fill=INK2, font_style="italic")]
    can += [L(436, rc - 7, 436, rc + 7, ORANGE, 3), T(444, rc - 12, "no pecado, prevalece o cânone", 12.5, fill=ORANGE)]
    # romano: the volumes of the school, the glossed text, the swap of lanes in the sixteenth century
    rom = [P(f"M{X0} {rr} H{yx(1500) + 10}", INK, 5), dot(rr), lab(rr, "romano")]
    for i, k in enumerate(("diag", "diag", "diag", "horiz", "cross")):
        rom += [S.rect(166 + i * 15, rr - 42, 11, 42, fill=PAPER, stroke=BLUE if i == 4 else INK, stroke_width=1.5)]
    rom += [T(166, rr + 22, "Corpus iuris civilis", 12.5, fill=INK2, font_style="italic")]
    fx0, fy0, fw, fh = 300, 152, 104, 88
    rom += [S.rect(fx0, fy0, fw, fh, fill=PAPER, stroke=INK, stroke_width=1.2)]
    for i in range(6):
        rom += [L(fx0 + 5, fy0 + 5 + i * 3.2, fx0 + fw - 5, fy0 + 5 + i * 3.2, GRID, 1), L(fx0 + 5, fy0 + fh - 22 + i * 3.2, fx0 + fw - 5, fy0 + fh - 22 + i * 3.2, GRID, 1)]
    for i in range(8):
        rom += [L(fx0 + 5 + i * 3.2, fy0 + 26, fx0 + 5 + i * 3.2, fy0 + fh - 26, GRID, 1), L(fx0 + fw - 28 + i * 3.4, fy0 + 26, fx0 + fw - 28 + i * 3.4, fy0 + fh - 26, GRID, 1)]
    nx0, ny0 = fx0 + 30, fy0 + 24
    rom += [S.rect(nx0, ny0, 44, 40, fill=PAPER, stroke=INK, stroke_width=2.2)] + writing(nx0 + 6, ny0 + 8, [32, 28, 32, 24, 32], 6.4, INK, 1.3)
    for i, yy in enumerate((ny0 + 10, ny0 + 23, ny0 + 35)):
        rom.append(P(wave(nx0 + 8, nx0 + 30 + i * 4, yy, 1.2, 6), BLUE, 1))
    rom += [T(fx0 + fw / 2, fy0 - 8, "Irnério", 13, anchor="middle"), T(fx0 + fw / 2, fy0 + fh + 16, "Magna Glosa · Acúrsio", 12.5, fill=INK2, anchor="middle")]
    # the swap: national law takes the heavy lane, the Roman text goes down and splits
    rom += [P(curve(yx(1500) + 10, rr, 842, rl), INK, 3), P(f"M842 {rl} H872", INK, 3),
            P(curve(872, rl, 904, 258), INK, 2.6), P("M904 258 H934", INK, 2.6), P(curve(872, rl, 904, 326), INK, 2.6), P("M904 326 H934", INK, 2.6),
            T(942, 256, "mos gallicus", 13.5), T(942, 271, "Cujas · Hotman · Doneau", 12.5, fill=INK2),
            T(942, 324, "usus modernus", 13.5), T(942, 339, "Stryk · Carpzov · Böhmer", 12.5, fill=INK2),
            T(858, 330, "subsidiário", 12.5, fill=INK2, anchor="middle")]
    # próprio: wavy while it keeps changing; it rises and is written down
    loc = [P(wave(X0, 800, rl, 5, 26), INK, 2.2), P(curve(800, rl, 846, rr), INK, 5), P(f"M846 {rr} H940", INK, 5), dot(rl), lab(rl, "direito próprio"),
           T(X0 + 14, rl + 26, "estatutos das cidades", 12.5, fill=INK2, font_style="italic"),
           T(948, rr - 6, "direitos nacionais", 13.5), T(948, rr + 10, "compilações régias", 12.5, fill=INK2)]
    # comentadores: ties among the three rails, then the consilium
    com = []
    for x in (490, 520, 550, 580):
        com.append(L(x, rc, x, rl, INK2, 1.2))
        for yy in (rc, rr, rl):
            com.append(S.circle(x, yy, 3.4, fill=INK, stroke=INK, stroke_width=1))
    com += [T(535, rl + 26, "concordar · distinguir", 12.5, fill=INK2, anchor="middle", font_style="italic")]
    sx, sy, sw_, sh = 650, 150, 84, 80
    com += [S.path(f"M{sx + 12} {sy} H{sx + sw_ + 12} L{sx + sw_} {sy + sh} H{sx} Z", fill=PAPER, stroke=INK, stroke_width=2)]
    com += [L(sx + 17 - i * 3, sy + 17 + i * 16, sx + sw_ - 2 - i * 3, sy + 17 + i * 16, INK, 1.3) for i in range(4)]
    com += [P(curve(606, rc, sx + 14, sy + 17), BLUE, 1.8), P(curve(606, rl, sx + 6, sy + 65), BLUE, 1.8),
            S.circle(sx + 14, sy + 17, 3.2, fill=BLUE, stroke=BLUE), S.circle(sx + 6, sy + 65, 3.2, fill=BLUE, stroke=BLUE)]
    com += [T(sx + 46, sy - 10, "consilium", 13.5, anchor="middle"), T(sx + 52, sy + sh + 20, "duplo domínio,", 12.5, fill=INK2, anchor="middle"), T(sx + 52, sy + sh + 35, "teoria estatutária", 12.5, fill=INK2, anchor="middle")]
    # lives, to scale
    bars = [(1100, 1150, 0, "Irnério · 1ª metade do séc. XII", "r", True), (1180, 1260, 1, "Acúrsio c. 1180–c. 1260", "l", False),
            (1270, 1336, 1, "Cino 1270–1336", "r", False), (1314, 1357, 2, "Bártolo 1314–1357", "r", False),
            (1327, 1400, 3, "Baldo 1327–1400", "r", False), (1435, 1519, 1, "Jasão del Maino 1435–1519", "r", False)]
    ys = (364, 378, 392)
    lives = []
    rowy = {0: ys[1], 1: ys[0], 2: ys[1], 3: ys[2]}
    for a, z, row, name, side, dashed in bars:
        y = rowy[row]
        x1, x2 = yx(a), yx(z)
        lives.append(S.rect(x1, y - 4, x2 - x1, 8, fill=PAPER if dashed else INK, stroke=INK, stroke_width=1.2, stroke_dasharray="3 3" if dashed else None))
        lives.append(T(x2 + 6 if side == "r" else x1 - 6, y + 4, name, 12.5, anchor=None if side == "r" else "end"))
    lives += [S.circle(yx(1441), ys[1], 4, fill=INK, stroke=INK), T(yx(1441) + 8, ys[1] + 4, "Paulo de Castro † 1441", 12.5)]
    lives += [L(X0, 410, X0 + 930, 410, INK, 1.4)]
    for yr in range(1100, 1701, 100):
        lives += [L(yx(yr), 406, yx(yr), 414, INK, 1.4), T(yx(yr), 428, str(yr), 12.5, fill=INK2, anchor="middle")]
    b += [_thread("mj-canonico", "Trilho canônico, contido pelo critério do pecado", [f"M{X0} {rc} H{X0 + 930}"], can),
          _thread("mj-proprio", "Trilho do direito próprio, que chega aos direitos nacionais", [wave(X0, 800, rl, 5, 26)], loc),
          _thread("mj-romano", "Trilho romano, da Magna Glosa ao mos gallicus e ao usus modernus", [f"M{X0} {rr} H296", f"M408 {rr} H{yx(1500)}"], rom),
          _thread("mj-comentadores", "Os comentadores: ligações entre os trilhos e o consilium", [f"M{x} {rc} V{rl}" for x in (490, 520, 550, 580)], com)]
    b += lives
    return svg(1100, 438, "Planta das escolas jurídicas: as fontes percorrem Bolonha e os comentadores até o século XVI, com as vidas dos juristas em escala", b)


# ───────────────────────── consulta: stacks in the order of consultation
def _stack(x, y0, tiers, gap=4):
    """tiers: list of items; item = (label, kind) kind: 'one' | 'two' (two volumes side by side) | 'lack' (top notch)"""
    out, y = [], y0
    for label, kind, wide in tiers:
        out += _tier(x, y, label, kind, wide)
        y += 44
    return out


def _tier(x, y, label, kind, w=150):
    """A volume lying in the stack; its name stands to the right, outside the drawing of the book."""
    h, dx = 36, 24
    if kind == "two":
        w1 = (w - 12) / 2
        return (slab(x, y, w1, h, dx=dx, dy=-13) + slab(x + w1 + 14, y, w1, h, dx=dx, dy=-13)
                + [T(x + w + dx + 12, y + 22, label, 18)])
    return slab(x, y, w, h, dx=dx, dy=-13) + [T(x + w + dx + 12, y + 22, label, 18)]


def consulta(p):
    b = []
    base, step = 196, 50
    xs = (30, 390, 730)
    titles = ("Novara · 1227", "Modena · 1327", "Sicília · 1231")
    for x in xs:
        b.append(L(x - 20, base + 40, x + 320, base + 40, INK2, 1.4))
    stacks = [
        [("estatuto", "one"), ("leis romanas", "one")],
        [("estatuto", "one"), ("direito erudito", "one")],
        [("constituições", "one"), ("costumes aprovados", "one"), ("longobardo e romano", "two")],
    ]
    for x, title, tiers in zip(xs, titles, stacks):
        n = len(tiers)
        y = base - step * (n - 1)
        ytop = y
        for label, kind in tiers:
            b += _tier(x, y, label, kind)
            y += step
        y = ytop
        for i in range(n - 1):
            nx = x + 120
            b += [S.rect(nx - 9, y + 1, 18, 3, fill=PAPER), P(f"M{nx} {y + 2} V{y + step - 5}", BLUE, 2.2),
                  P(f"M{nx - 4.5} {y + step - 12} L{nx} {y + step - 5} L{nx + 4.5} {y + step - 12}", BLUE, 2.2)]
            y += step
        b.append(T(x + 80, base + 78, title, 22, anchor="middle"))
    return svg(1100, 300, "Três pilhas de volumes na ordem em que o direito próprio manda consultar as fontes", b)


# ───────────────────────── volumes: the five books of the school
def _hatch_block(x, y, w, h, kind, color=INK2):
    out = []
    if kind == "diag":
        out += S.hatch(x, y, w, h, 7, stroke=color, stroke_width=1)
    elif kind == "horiz":
        out += [L(x + 3, y + k, x + w - 3, y + k, color, 1) for k in range(6, int(h), 7)]
    elif kind == "dots":
        for yy in range(int(y) + 8, int(y + h), 9):
            for xx in range(int(x) + 8, int(x + w), 10):
                out.append(S.circle(xx, yy, 1.1, fill=color))
    elif kind == "cross":
        out += S.hatch(x, y, w, h, 8, stroke=color, stroke_width=1)
        out += [L(x + 3, y + k, x + w - 3, y + k, color, .8) for k in range(8, int(h), 14)]
    return out


def _spine(x, y, w, h, kind, sw=1.8, color=INK):
    out = [S.rect(x, y, w, h, fill=PAPER, stroke=color, stroke_width=sw)]
    out += _hatch_block(x + 5, y + 26, w - 10, h - 52, kind, INK2)
    out += [L(x, y + 14, x + w, y + 14, color, 1.4), L(x, y + h - 14, x + w, y + h - 14, color, 1.4)]
    return out


def volumes(p):
    b = []
    y, h = 18, 160
    xs = [26, 80, 134, 188]
    kinds = ["diag", "diag", "diag", "horiz"]
    names = ["Digesto Velho", "Infortiatum", "Digesto Novo", "Código"]
    for x, k in zip(xs, kinds):
        b += _spine(x, y, 46, h, k)
    b += _spine(242, y, 70, h, "cross", 2.6, BLUE)
    b += [L(14, y + h + 2, 326, y + h + 2, INK, 2)]
    # staggered names under the shelf, each with a leader
    for i, (x, n) in enumerate(zip(xs, names)):
        ly = y + h + 24 + (i % 2) * 22
        b += [L(x + 23, y + h + 4, x + 23, ly - 14, GRID, 1), T(x + 23, ly, n, 14, anchor="middle")]
    b += [L(277, y + h + 4, 277, y + h + 58, BLUE, 1.6), T(277, y + h + 76, "Volumen parvum", 16, fill=BLUE, anchor="middle")]
    # the opened Volumen parvum: five quires, each its own writing
    y0 = 306
    quires = ["tres libri", "Institutiones", "parte das Novelas", "Libri feudorum", "constituições do Sacro Império"]
    kinds2 = ["horiz", "dots", "diag", "cross", "horiz"]
    for i, (n, k) in enumerate(zip(quires, kinds2)):
        yy = y0 + i * 26
        b += slab(14, yy, 104, 18, dx=20, dy=-9, stroke=BLUE if i == 0 else INK, sw=1.5)
        b += _hatch_block(36, yy + 3, 138, 12, "horiz" if k in ("horiz", "dots") else "diag", INK2) if False else []
        b += [T(150, yy + 14, n, 14)]
    return carded(372, 446, "Os cinco volumes do Corpus na escola; o Volumen parvum aberto em cadernos de origens diferentes", b)



# ───────────────────────── glosa: one folio, three states
def glosa(p):
    st = _state(p, 3)
    X0, X1, Y0, Y1 = 24, 348, 14, 372
    nx0, nx1, ny0, rows, gap = 100, 272, 78, 10, 19
    b = [S.rect(X0 + 4, Y0 + 5, X1 - X0, Y1 - Y0, fill=PAPER, stroke=GRID, stroke_width=1),
         S.rect(X0, Y0, X1 - X0, Y1 - Y0, fill=PAPER, stroke=INK, stroke_width=1.8)]
    ys = [ny0 + 16 + k * gap for k in range(rows)]
    if st == 3:  # the apparatus wraps the text on all four sides
        for yy in range(28, 66, 6):
            b.append(L(40, yy, 332, yy, GRID, 1.1))
        for yy in range(300, 368, 6):
            b.append(L(40, yy, 332, yy, GRID, 1.1))
        for yy in range(70, 292, 6):
            b.append(L(40, yy, 84, yy, GRID, 1.1))
            b.append(L(288, yy, 332, yy, GRID, 1.1))
        b.append(S.rect(90, 64, 192, 232, fill="none", stroke=INK2, stroke_width=1))
    else:
        for yy, w in ((110, 40), (222, 40)):
            b += [L(44, yy + j * 9, 44 + w - (j % 2) * 8, yy + j * 9, GRID, 1.1) for j in range(3)]
        b += [L(290, 170 + j * 9, 330 - (j % 2) * 6, 170 + j * 9, GRID, 1.1) for j in range(3)]
    # the nucleus never moves
    for k, yy in enumerate(ys):
        b.append(L(nx0, yy, nx1 - (14 if k % 4 == 3 else 0), yy, INK, 2))
    gaps = [(ny0 + 16 + (k + .5) * gap) for k in (1, 4, 8)]
    for yy, ln in zip(gaps, (110, 130, 90)):
        b.append(P(wave(nx0 + 8, nx0 + 8 + ln, yy, 2.2, 10), BLUE, 1.2))
    if st >= 2:
        r1, r2, r3, r4 = ys[1], ys[6], ys[3], ys[8]
        b += fade([P(f"M{nx1 + 2} {r1} C{nx1 + 34} {r1} {nx1 + 34} {r2} {nx1 + 2} {r2}", BLUE, 1.8),
                   S.circle(nx1 + 2, r1, 3.4, fill=BLUE, stroke=BLUE), S.circle(nx1 + 2, r2, 3.4, fill=BLUE, stroke=BLUE),
                   P(f"M{nx0 - 2} {r3} C{nx0 - 34} {r3} {nx0 - 34} {r4} {nx0 - 2} {r4}", BLUE, 1.8),
                   S.circle(nx0 - 2, r3, 3.4, fill=BLUE, stroke=BLUE), S.circle(nx0 - 2, r4, 3.4, fill=BLUE, stroke=BLUE)], st == 2)
    label = ("entre as linhas e à margem", "outra passagem que esclareça", "Magna Glosa")[st - 1]
    b.append(T(186, 394, label, 17, fill=INK2, anchor="middle"))
    return svg(372, 404, ("Uma folha com glosas entre as linhas e à margem", "A glosa remete a outras passagens", "A Magna Glosa envolve o texto")[st - 1], b)


# ───────────────────────── parecer: cities, the road across the border, the consilium
def _town(x, y, r=24):
    out = [S.circle(x, y, r, fill=PAPER, stroke=INK, stroke_width=1.8), S.circle(x, y, r * .55, fill="none", stroke=INK2, stroke_width=1.1)]
    for k in range(12):
        a = k * math.pi / 6
        out.append(L(x + (r - 4) * math.cos(a), y + (r - 4) * math.sin(a), x + (r + 5) * math.cos(a), y + (r + 5) * math.sin(a), INK, 1.4))
    return out


def _statute_stack(x, y, n, revised=True):
    out = []
    for k in range(n - 1, -1, -1):
        out += leaf(x + k * 9, y - k * 7, 74, 54, INK if k == 0 else INK2, 1.5, rows=3 if k == 0 else 0, gap=11, pad=9)
    if revised:  # the front version carries a revised line: one struck out, its replacement beside it
        b = y + 12
        out += [L(x + 9, b + 11, x + 55, b + 11, ORANGE, 1.6), L(x + 9, b + 22, x + 45, b + 22, BLUE, 1.6)]
    return out


def parecer(p):
    st = _state(p, 3)
    b = []
    if st < 3:
        b += [S.path("M14 62 L172 54 L178 304 L16 312 Z", fill=PAPER, stroke=INK2, stroke_width=1.4, stroke_dasharray="6 5"),
              S.path("M178 54 L358 64 L356 298 L178 304 Z", fill=PAPER, stroke=INK2, stroke_width=1.4, stroke_dasharray="6 5"),
              P(wave(176, 178, 54, 0), INK, 0) if False else "",
              P("M175 56 L181 120 L172 196 L180 270 L176 322", INK, 3)]
        b += _town(92, 130) + _town(268, 140)
        b += _statute_stack(40, 262, 3) + _statute_stack(214, 262, 2)
    if st == 2:
        b += fade([P("M92 156 C130 214 218 214 268 166", INK, 2, stroke_dasharray="2 7"),
                   S.circle(178, 196, 6, fill=PAPER, stroke=INK, stroke_width=2),
                   *[x for x in slab(138, 40, 70, 20, dx=14, dy=-8, stroke=BLUE, sw=2)],
                   L(178, 62, 178, 190, BLUE, 1.4, stroke_dasharray="3 4"),
                   T(176, 24, "ius commune", 14, fill=BLUE, anchor="middle")])
    if st == 3:
        srcs = [(46, "romano"), (126, "canônico"), (206, "feudal"), (286, "estatuto")]
        for k, (x, name) in enumerate(srcs):
            if name in ("romano", "canônico"):
                b += slab(x, 40, 46, 26, dx=12, dy=-8) + [L(x + 8, 49, x + 38, 49, INK2, 1)]
            elif name == "feudal":
                b += [S.path(f"M{x} 66 V38 H{x + 8} V45 H{x + 16} V38 H{x + 24} V45 H{x + 32} V38 H{x + 40} V66 Z", fill=PAPER, stroke=INK, stroke_width=1.6)]
            else:
                b += leaf(x, 34, 46, 32, rows=2, gap=8, pad=7)
            b.append(T(x + 24, 92, name, 14, anchor="middle"))
        sx, sy = 44, 196
        for k in range(5):
            pass
        b += [S.path(f"M{sx + 30} {sy} H{sx + 288} L{sx + 258} {sy + 112} H{sx} Z", fill=PAPER, stroke=INK, stroke_width=2),
              S.path(f"M{sx + 30} {sy} H{sx + 288} L{sx + 258} {sy + 112} H{sx} Z", fill="none", stroke=GRID, stroke_width=1)]
        landing = []
        for k in range(5):
            yy = sy + 20 + k * 19
            xa, xb = sx + 30 - (yy - sy) * 30 / 112 + 14, sx + 288 - (yy - sy) * 30 / 112 - 14
            b.append(L(xa, yy, xb, yy, INK, 1.4))
            landing.append((xa + 30 + k * 18, yy))
        pts = [(landing[0][0] + 20, landing[0][1]), (landing[1][0] + 30, landing[1][1]), (landing[2][0] + 40, landing[2][1]), (landing[3][0] + 50, landing[3][1])]
        for (x, name), (lx, ly) in zip(srcs, pts):
            b += [P(f"M{x + 24} 100 C{x + 24} 150 {lx} 140 {lx} {ly - 2}", BLUE, 1.7), S.circle(lx, ly, 3.6, fill=BLUE, stroke=BLUE)]
        b.append(T(186, sy + 140, "consilium", 20, anchor="middle"))
    caption = ("muda a vida, muda o estatuto", "o comércio liga as cidades", "as fontes respondem juntas")[st - 1]
    if st < 3:
        b.append(T(186, 344, caption, 17, fill=INK2, anchor="middle"))
    return svg(372, 352, ("Cidades diferentes mudam seus estatutos", "O comércio atravessa a fronteira entre as cidades", "O parecer reúne fontes diferentes numa mesma folha")[st - 1], b)


# ───────────────────────── terra: one parcel, two protections
def _plank(x, y, w, depth, dx, dy, color, wash, sw=2.0, lit=False):
    """A tier of hold: a thin slab with the parcel's own footprint, seen from a little above."""
    sw = sw + (1.0 if lit else 0)
    return [S.path(f"M{x} {y} L{x + dx} {y + dy} H{x + w + dx} L{x + w} {y} Z", fill=wash, stroke=color, stroke_width=sw, stroke_linejoin="round"),
            S.path(f"M{x + w} {y} L{x + w + dx} {y + dy} V{y + dy + depth} L{x + w} {y + depth} Z", fill=color, stroke=color, stroke_width=sw, stroke_linejoin="round"),
            S.rect(x, y, w, depth, fill=color, stroke=color, stroke_width=sw)]


def _action(x_tail, x_head, y, color, label):
    """An action: it comes in from outside and lands on the whole edge of the tier it protects."""
    return [P(f"M{x_tail} {y} H{x_head + 8}", color, 3.2),
            S.path(f"M{x_head} {y} L{x_head + 14} {y - 8} V{y + 8} Z", fill=color, stroke=color, stroke_width=1.5, stroke_linejoin="round"),
            T(x_tail, y - 12, label, 17, fill=color if color == BLUE else INK2, anchor="end")]


def terra(p):
    """One parcel in perspective, ploughed; above it two tiers of hold, each with exactly the parcel's footprint and
    all of it: the same ground under both, nothing divided. Each action comes in from outside and lands on its tier."""
    st = _state(p, 3)
    x, w, dx, dy = 32, 176, 58, -40          # footprint: front edge, width, and the slant of the depth
    soil = 322
    up, low = 128, 232                        # front edge of each tier
    # the ground, ploughed in lines that follow the perspective
    g = [S.path(f"M{x} {soil} L{x + dx} {soil + dy} H{x + w + dx} L{x + w} {soil} Z", fill=PAPER, stroke=INK, stroke_width=2, stroke_linejoin="round")]
    for k in range(1, 6):
        t = k / 6
        g.append(L(x + dx * t + 3, soil + dy * t, x + w + dx * t - 3, soil + dy * t, GRID, 1.2))
    g.append(S.path(f"M{x} {soil} V{soil + 9} H{x + w} V{soil}", fill=PAPER2, stroke=INK, stroke_width=2, stroke_linejoin="round"))
    g.append(S.path(f"M{x + w} {soil} L{x + w + dx} {soil + dy} V{soil + dy + 9} L{x + w} {soil + 9} Z", fill=PAPER2, stroke=INK, stroke_width=2, stroke_linejoin="round"))
    b = []
    top = up if st >= 1 else soil
    # the same corners, carried up: the footprint is one
    for cx, cy in ((x, soil), (x + w, soil), (x + w + dx, soil + dy)):
        b.append(L(cx, top + (0 if cx != x + w + dx else dy), cx, cy, GRID, 1.2, stroke_dasharray="2 5"))
    b += g
    b += _plank(x, up, w, 8, dx, dy, INK, PAPER2, 2.0, lit=st == 3)
    if st >= 2:
        lower = _plank(x, low, w, 8, dx, dy, BLUE, "var(--dif-wash)", 2.0, lit=st == 3)
        b += fade(lower, st == 2)
        b += fade([T(x + 4, low + dy - 14, "dominium utile", 19, fill=BLUE), T(x + 4, up + dy - 14, "dominium directum", 19)], st == 2)
    if st == 3:
        b += _action(366, x + w + dx + 8, up + dy / 2 + 4, INK, "actio directa")
        b += _action(366, x + w + dx + 8, low + dy / 2 + 4, BLUE, "actio utilis")
    b.append(T(x + (w + dx) / 2, soil + 38, "a mesma terra", 19, anchor="middle"))
    return svg(372, 372, ("Uma posição cobre toda a terra", "Uma segunda posição cobre a mesma terra; nenhuma linha reparte o solo", "A actio directa e a actio utilis alcançam cada posição")[st - 1], b)


# ───────────────────────── vinculos: what stays, what crosses
def _post(x, ground, h, mark, color=INK):
    return [L(x, ground, x, ground - h, color, 2.2)] + mark


def vinculos(p):
    g = 296
    b = []
    b += [P("M556 24 L544 90 L562 160 L546 230 L558 310", INK, 2.6)]
    for x0, x1 in ((30, 536), (572, 1070)):
        b.append(L(x0, g, x1, g, INK2, 2))
        for k in range(int(x0) + 6, int(x1), 14):
            b.append(L(k, g, k - 6, g + 8, GRID, 1))

    def person(x, y):
        return [S.circle(x, y, 18, fill=PAPER, stroke=BLUE, stroke_width=2.6), S.circle(x, y, 6, fill=BLUE, stroke=BLUE)]

    def chest(x, y):
        return slab(x, y, 44, 28, dx=13, dy=-9, stroke=BLUE, sw=1.8)
    b += person(210, 140) + chest(266, 148) + [L(228, 146, 266, 158, BLUE, 2.4)]
    b += [T(186, 146, "proprietário", 17, fill=BLUE, anchor="end"), T(290, 198, "móveis", 17, fill=BLUE, anchor="middle")]
    b += [L(210, 158, 210, g, BLUE, 2.2, stroke_dasharray="1 6"), T(210, g + 36, "naturalidade", 17, fill=BLUE, anchor="middle")]
    b += [P("M232 112 C340 40 620 40 764 112", BLUE, 2.2, stroke_dasharray="2 7"), P("M756 102 L766 114 L752 116", BLUE, 2.2)]
    b += person(790, 140) + chest(846, 148) + [L(808, 146, 846, 158, BLUE, 2.4)]
    b += [T(868, 198, "móveis", 17, fill=BLUE, anchor="middle")]
    b += [S.path(f"M596 {g} L696 {g} L714 {g - 34} L614 {g - 34} Z", fill=PAPER, stroke=INK, stroke_width=2)]
    b += [L(622 + k * 16, g - 4, 636 + k * 16, g - 32, GRID, 1.2) for k in range(5)]
    b += [T(655, g + 36, "imóvel", 17, anchor="middle")]
    b += [L(750, g, 750, g - 78, INK, 2.4), L(736, g - 106, 764, g - 78, INK, 3.2), L(764, g - 106, 736, g - 78, INK, 3.2), T(750, g + 36, "delito", 17, anchor="middle")]
    b += [L(940, g, 940, g - 46, INK, 2.4), *leaf(913, g - 108, 54, 62, rows=4, gap=10, pad=9), T(940, g + 36, "contrato", 17, anchor="middle")]
    fx = 1030
    b += [L(fx - 36, g, fx + 36, g, INK, 2), P(f"M{fx - 38} {g - 62} L{fx} {g - 92} L{fx + 38} {g - 62} Z", INK, 2, PAPER),
          L(fx - 26, g - 62, fx - 26, g, INK, 3.4), L(fx, g - 62, fx, g, INK, 3.4), L(fx + 26, g - 62, fx + 26, g, INK, 3.4),
          T(fx, g + 36, "foro", 17, anchor="middle")]
    return svg(1100, 350, "Dois territórios: a terra, o delito, o contrato e o foro ficam onde estão; o proprietário e seus móveis atravessam", b)


# ───────────────────────── apresentacao: one document, two routes, one door
def apresentacao(p):
    st = _state(p, 2)
    wx = 238
    b = [L(wx, 24, wx, 120, INK, 4), L(wx, 214, wx, 316, INK, 4),
         P(f"M{wx - 8} 120 H{wx + 8} M{wx - 8} 214 H{wx + 8}", INK, 4)]
    b += [P(f"M{wx + 22} 150 L{wx + 22} 184", INK2, 1.2)] if False else []
    # the court side: where the document is received
    b += leaf(284, 142, 56, 44, rows=3, gap=9, pad=8)
    # the party (the person themself) and the procurador
    b += [S.circle(44, 100, 16, fill=PAPER, stroke=INK, stroke_width=2.4), S.circle(44, 100, 5, fill=INK, stroke=INK),
          S.circle(44, 244, 16, fill=PAPER, stroke=BLUE, stroke_width=2.4), S.rect(40, 240, 8, 8, fill=BLUE, stroke=BLUE)]
    b += [T(44, 70, "o próprio", 16, anchor="middle"), T(44, 288, "procurador", 16, fill=BLUE, anchor="middle")]
    # route 1: the document the person presents goes through the opening
    b += [P(f"M62 100 C140 100 150 160 {wx - 6} 160 H300", INK, 2.6), P("M290 154 L300 160 L290 166", INK, 2.6)]
    b += [S.rect(120, 114, 24, 18, fill=PAPER, stroke=INK, stroke_width=1.6)]
    if st == 1:
        b += [P(f"M62 244 C120 244 150 224 {wx - 40} 224", INK2, 2, stroke_dasharray="3 6"), L(wx - 40, 214, wx - 40, 234, INK2, 3)]
        b += [T(140, 190, "verba", 17, fill=INK2, anchor="middle", font_style="italic")]
    if st == 2:
        b += fade([P(f"M62 244 C130 244 160 190 {wx - 6} 176 H300", BLUE, 2.6), P("M290 170 L300 176 L290 182", BLUE, 2.6),
                   S.rect(118, 226, 24, 18, fill=PAPER, stroke=BLUE, stroke_width=1.6),
                   P("M44 118 C-4 170 -4 190 28 232", BLUE, 1.6, stroke_dasharray="3 5"),
                   T(172, 134, "ratio", 17, fill=BLUE, anchor="middle", font_style="italic")])
    return svg(372, 340, ("O documento apresentado pelo próprio passa pela abertura", "O procurador chega à mesma abertura pela ratio")[st - 1], b)


# ───────────────────────── autoridade: the balance
def _pan(cx, cy, w=92, color=INK):
    return [L(cx, cy - 74, cx - w / 2, cy, color, 1.2), L(cx, cy - 74, cx + w / 2, cy, color, 1.2),
            P(f"M{cx - w / 2 - 6} {cy} Q{cx} {cy + 22} {cx + w / 2 + 6} {cy}", color, 2.4)]


def autoridade(p):
    st = _state(p, 2)
    piv = (186, 112)
    th = math.radians(14) * (1 if st == 1 else -1)  # state 1: the volumes side is down
    half = 120
    lx, ly = piv[0] - half * math.cos(th), piv[1] + half * math.sin(th)
    rx, ry = piv[0] + half * math.cos(th), piv[1] - half * math.sin(th)
    b = [P(f"M{piv[0] - 36} 330 L{piv[0]} {piv[1] + 8} L{piv[0] + 36} 330", INK, 2.2), L(piv[0] - 56, 330, piv[0] + 56, 330, INK, 3)]
    b += [L(lx, ly, rx, ry, INK, 4.5), S.circle(piv[0], piv[1], 8, fill=PAPER, stroke=INK, stroke_width=2.4)]
    b += _pan(lx, ly + 76) + _pan(rx, ry + 76)
    # the pan of authorities: many volumes
    cy = ly + 76
    for k in range(4):
        b += slab(lx - 30, cy - 16 - k * 17, 56, 15, dx=9, dy=-6, sw=1.4)
    # the contrary reason: one sheet, orange (the limit)
    cy2 = ry + 76
    b += [sheet(rx - 34, cy2 - 8, 68, 8, 10, ORANGE, 1.8, PAPER)]
    b += [T(lx, 348, "opinio communis", 16, anchor="middle") if False else "", T(8, 24, "opinio communis", 16, anchor="start"), T(364, 24, "objeção melhor", 16, fill=ORANGE, anchor="end")]
    return svg(372, 352, ("As opiniões dos doutores pesam mais que uma só razão", "Uma razão melhor pesa mais que as opiniões dos doutores")[st - 1], b)


# ───────────────────────── crise: three orders of consultation
def crise(p):
    b = []
    xs = (40, 400, 760)
    cap = [("predomínio universal do comum",), ("equilíbrio com os direitos próprios",), ("autonomia dos próprios; o comum, subsidiário",)]
    for i, x in enumerate(xs):
        top = 150
        b += [L(x, top, x + 300, top, INK, 4), L(x + 24, top, x + 24, top + 66, INK, 3), L(x + 276, top, x + 276, top + 66, INK, 3), L(x + 24, top + 40, x + 276, top + 40, GRID, 1.2)]
        w, h = 112, 40
        if i == 0:      # the common book on top of the local one
            low, high = ("próprio", x + 94, top - h), ("comum", x + 94, top - 2 * h - 6)
            b += slab(low[1], low[2], w, h, stroke=INK) + [T(low[1] + w / 2 + 8, low[2] + 26, "próprio", 17, anchor="middle")]
            b += slab(high[1], high[2], w, h, stroke=BLUE, sw=2.4) + [T(high[1] + w / 2 + 8, high[2] + 26, "comum", 17, fill=BLUE, anchor="middle")]
        elif i == 1:    # side by side, level
            b += slab(x + 26, top - h, w, h, stroke=BLUE, sw=2.4) + [T(x + 26 + w / 2 + 8, top - h + 26, "comum", 17, fill=BLUE, anchor="middle")]
            b += slab(x + 168, top - h, w, h, stroke=BLUE, sw=2.4) + [T(x + 168 + w / 2 + 8, top - h + 26, "próprio", 17, fill=BLUE, anchor="middle")]
        else:           # the local book on top, the common one beneath
            b += slab(x + 94, top - h, w, h, stroke=INK) + [T(x + 94 + w / 2 + 8, top - h + 26, "comum", 17, anchor="middle")]
            b += slab(x + 94, top - 2 * h - 6, w, h, stroke=BLUE, sw=2.4) + [T(x + 94 + w / 2 + 8, top - 2 * h - 6 + 26, "próprio", 17, fill=BLUE, anchor="middle")]
        b.append(T(x + 156, top + 100, cap[i][0], 17, fill=INK2, anchor="middle"))
    b += [P("M352 90 H392 M384 84 L392 90 L384 96", INK2, 1.6), P("M712 90 H752 M744 84 L752 90 L744 96", INK2, 1.6)]
    return svg(1100, 270, "Três mesas de consulta com os mesmos dois volumes em ordens diferentes", b)


# ───────────────────────── depuracao: layers lifted from the old text
def _nucleus(x, y, w=96, rows=8, gap=10, color=INK, sw=1.8):
    return [L(x, y + k * gap, x + w - (14 if k % 4 == 3 else 0), y + k * gap, color, sw) for k in range(rows)]


def _frame_lines(x, y, w, h, inset_x, inset_y, color=GRID):
    """Dense apparatus between an outer frame and the nucleus window."""
    out = []
    for yy in range(int(y + 6), int(y + h - 4), 6):
        if yy < y + inset_y or yy > y + h - inset_y:
            out.append(L(x + 6, yy, x + w - 6, yy, color, 1.1))
        else:
            out += [L(x + 6, yy, x + inset_x - 4, yy, color, 1.1), L(x + w - inset_x + 4, yy, x + w - 6, yy, color, 1.1)]
    return out


def depuracao(p):
    b = []
    # stage 1: the received text, wrapped, with corrections inside it
    x, y, w, h = 70, 40, 230, 200
    b += [S.rect(x, y, w, h, fill=PAPER, stroke=INK, stroke_width=1.8)] + _frame_lines(x, y, w, h, 64, 52)
    b += _nucleus(x + 72, y + 62, 90, 8, 11)
    for k in (1, 5):
        b += [L(x + 72 + 20, y + 62 + k * 11, x + 72 + 62, y + 62 + k * 11, ORANGE, 2.6)]
    b += [T(x + w / 2, 268, "glosas e comentários", 17, anchor="middle")]
    b += [P("M312 140 H356 M348 134 L356 140 L348 146", INK, 1.8)]
    # stage 2: the apparatus lifted away, the corrections lifted out
    x2 = 400
    b += [S.rect(x2 + 40, 62, 150, 104, fill=PAPER, stroke=INK, stroke_width=1.8)]
    b += _nucleus(x2 + 66, 86, 86, 7, 11)
    b += [S.rect(x2 - 18, 6, 230, 206, fill="none", stroke=INK2, stroke_width=1.2, stroke_dasharray="4 5")]
    b += [P(f"M{x2 + 40} 82 L{x2 - 18} 40 M{x2 + 190} 82 L{x2 + 212} 40 M{x2 + 190} 166 L{x2 + 212} 212 M{x2 + 40} 166 L{x2 - 18} 212", GRID, 1, stroke_dasharray="2 4")]
    b += [P(wave(x2 - 6, x2 + 54, 26, 2.2, 10), INK2, 1.3), P(wave(x2 + 120, x2 + 200, 20, 2.2, 10), INK2, 1.3),
          P(wave(x2 - 6, x2 + 40, 192, 2.2, 10), INK2, 1.3), P(wave(x2 + 130, x2 + 200, 198, 2.2, 10), INK2, 1.3)]
    b += [L(x2 + 232, 52, x2 + 278, 44, ORANGE, 2.8), L(x2 + 232, 70, x2 + 270, 64, ORANGE, 2.8),
          P(f"M{x2 + 116} 128 C{x2 + 160} 120 {x2 + 200} 80 {x2 + 224} 62", ORANGE, 1.1, stroke_dasharray="2 4")]
    b += [T(x2 + 130, 268, "interpolações retiradas", 17, anchor="middle")] if False else [T(x2 + 130, 268, "depuração histórico-filológica", 17, anchor="middle")]
    b += [P("M720 140 H764 M756 134 L764 140 L756 146", INK, 1.8)]
    # stage 3: the old text alone, and an edition
    x3 = 800
    b += [S.rect(x3, 62, 130, 140, fill=PAPER, stroke=BLUE, stroke_width=2.4)]
    b += _nucleus(x3 + 18, 86, 92, 8, 14, INK, 1.8)
    b += slab(x3 + 150, 156, 92, 46, dx=16, dy=-10, stroke=BLUE, sw=2)
    b += [T(x3 + 120, 268, "edição crítica", 17, fill=BLUE, anchor="middle")]
    return svg(1100, 290, "A depuração afasta glosas e correções e o núcleo antigo reaparece", b)


# ───────────────────────── vigencia: only some lines are proved
def vigencia(p):
    b = []
    rows = 8
    y0, dy = 70, 32
    cols = (60, 440, 820)
    hit = (1, 4, 6)
    # the Corpus: every line
    x = cols[0]
    b += leaf(x, 40, 220, rows * dy + 16, rows=0)
    for k in range(rows):
        b.append(L(x + 18, y0 + k * dy, x + 190 - (30 if k % 3 == 1 else 0), y0 + k * dy, INK, 2))
    b.append(T(x + 110, 358, "Corpus", 18, anchor="middle"))
    # the register of application: marks only against the proved lines
    x = cols[1]
    b += leaf(x, 40, 220, rows * dy + 16, rows=0)
    for k in range(rows):
        b.append(L(x + 18, y0 + k * dy, x + 190, y0 + k * dy, GRID, 1.3))
    for k in hit:
        b += [L(x + 18, y0 + k * dy, x + 170, y0 + k * dy, INK, 2), S.circle(x + 196, y0 + k * dy, 4.4, fill=BLUE, stroke=BLUE)]
    b.append(T(x + 110, 358, "aplicação prática", 18, anchor="middle"))
    # the book in use
    x = cols[2]
    b += slab(x, 110, 200, 160, dx=26, dy=-16, sw=2)
    for j, k in enumerate(hit):
        yy = 134 + j * 40
        b.append(L(x + 18, yy, x + 176, yy, INK, 2))
    b += [L(x + 18, 134 + 40, x + 176, 134 + 40, ORANGE, 0)]
    b.append(T(x + 100, 358, "direito usado", 18, anchor="middle"))
    # threads: line by line, only where the match is proved
    for j, k in enumerate(hit):
        yy = y0 + k * dy
        b += [P(f"M{cols[0] + 224} {yy} C{cols[0] + 300} {yy} {cols[1] - 70} {yy} {cols[1] - 4} {yy}", BLUE, 1.8)]
        ty = 134 + j * 40
        b += [P(f"M{cols[1] + 224} {yy} C{cols[1] + 300} {yy} {cols[2] - 70} {ty} {cols[2] - 6} {ty}", BLUE, 1.8),
              S.circle(cols[2] - 4, ty, 3.6, fill=BLUE, stroke=BLUE)]
    # a line with no match stops; a received line is struck out by a later custom
    b += [P(f"M{cols[0] + 224} {y0 + 2 * dy} H{cols[0] + 300}", INK2, 1.6, stroke_dasharray="3 5"), L(cols[0] + 300, y0 + 2 * dy - 7, cols[0] + 300, y0 + 2 * dy + 7, INK2, 2.4)]
    sy = 134 + 80 + 38
    b += [L(cols[2] + 14, 134 + 40, cols[2] + 186, 134 + 40, ORANGE, 3.2)]
    b += leaf(cols[2] + 130, 286, 62, 46, ORANGE, 1.6, rows=2, gap=9, pad=8)
    b += [P(f"M{cols[2] + 160} 286 C{cols[2] + 160} 250 {cols[2] + 140} 190 {cols[2] + 120} 178", ORANGE, 1.6, stroke_dasharray="3 4"), T(cols[2] + 120, 316, "costume", 17, fill=ORANGE, anchor="end")]
    return svg(1100, 372, "Só algumas linhas do Corpus encontram correspondência no uso e entram no direito usado; um costume pode afastar uma delas", b)


# ───────────────────────── jurisdicoes: two shelves, two lands, the rule that routes a case
def _book(x, y, w, h, kind, color=INK, sw=1.8):
    return _spine(x, y, w, h, kind, sw, color)


def _arrow_up(x, y, color=BLUE, w=2.2):
    return [P(f"M{x - 5} {y + 9} L{x} {y} L{x + 5} {y + 9}", color, w)]


def jurisdicoes(p):
    b = []
    sh = 212  # the plank
    # the civil shelf: the Corpus, a set of volumes
    cx = [78, 126, 174, 222]
    for x, k in zip(cx, ("diag", "diag", "diag", "horiz")):
        b += _book(x, sh - 148, 42, 148, k)
    b += _book(272, sh - 148, 64, 148, "cross", INK, 2.6)
    b += slab(58, sh, 300, 8, dx=14, dy=-6, sw=1.8)
    b.append(T(208, 30, "Corpus iuris civilis", 21, anchor="middle"))
    # the canonical shelf: collections that follow one another, and papers that stayed outside them
    kx = [(690, 62, "cross"), (758, 46, "horiz"), (810, 36, "diag"), (852, 36, "dots"), (894, 26, "horiz")]
    for x, w, k in kx:
        b += _book(x, sh - 148, w, 148, k)
    b += slab(670, sh, 360, 8, dx=14, dy=-6, sw=1.8)
    # loose papers: one leaning on the last volume, two lying on the plank
    b += [S.path(f"M{924} {sh} L{936} {sh - 78} L{972} {sh - 74} L{962} {sh} Z", fill=PAPER, stroke=INK2, stroke_width=1.4, stroke_linejoin="round")]
    b += [L(940 + k * 1.2, sh - 64 + k * 12, 964 + k * 1.2, sh - 61 + k * 12, GRID, 1.1) for k in range(4)]
    for k, (dx0, sk) in enumerate(((968, 8), (984, -6))):
        b.append(sheet(dx0, sh - 6 - k * 5, 44, 6, skew=sk, stroke=INK2, sw=1.3))
    b.append(T(860, 30, "direito canônico", 21, anchor="middle"))
    # the two lands and the strip between them
    ey, cy = 330, 332
    for pts in ("M36 334 L496 322 L488 470 L24 482 Z", "M584 322 L1064 336 L1078 482 L592 470 Z"):
        b.append(S.path(pts, fill=PAPER2, stroke=INK2, stroke_width=1.4, stroke_dasharray="6 5"))
    b += _hatch_block(54, 346, 420, 100, "horiz", GRID)
    b += _hatch_block(612, 346, 440, 100, "dots", GRID)
    b += [P("M496 322 L489 380 L497 430 L488 470", INK, 3), P("M584 322 L590 380 L583 430 L592 470", INK, 3)]
    b += [T(176, 460, "terras do Império", 19, anchor="middle"), T(838, 456, "terras da Igreja", 19, anchor="middle")]
    # three cases, each a leaf, each walking to a shelf
    def case(x, y):
        return leaf(x, y, 38, 48, rows=3, gap=9, pad=8) + [S.circle(x + 19, y + 48, 4.5, fill=PAPER, stroke=BLUE, stroke_width=2)]
    # 1: an ordinary case in the Empire's land goes to the civil shelf
    b += case(90, 372) + [P("M109 368 V228", BLUE, 2.2)] + _arrow_up(109, 224)
    # 2: here observing the civil law would lead to sin: that road is struck out, the case crosses to the canon shelf
    b += case(318, 392)
    b += [P("M333 380 V300 Q333 268 365 268 H762 Q794 268 794 240 V230", BLUE, 2.2)] + _arrow_up(794, 226)
    b += [P("M333 268 V240", ORANGE, 1.8, stroke_dasharray="3 5"),
          L(324, 234, 342, 252, ORANGE, 3.2), L(342, 234, 324, 252, ORANGE, 3.2),
          T(356, 252, "pecado", 17, fill=ORANGE)]
    # 3: a case in the Church's land goes to the canon shelf
    b += case(952, 372) + [P("M971 368 V228", BLUE, 2.2)] + _arrow_up(971, 224)
    # the limit: a local judge's road toward the learned shelves ends short
    b += _town(540, 410, 18)
    b += [P("M540 386 V338", INK2, 1.8, stroke_dasharray="2 6"), L(528, 334, 552, 334, ORANGE, 3.2),
          T(540, 312, "juízes concelhios", 16, fill=ORANGE, anchor="middle")]
    return svg(1100, 500, "Duas prateleiras de livros, o civil e o canônico; abaixo, as terras do Império e da Igreja, e o caminho que leva cada caso a uma delas, com o pecado desviando o caso civil para o canônico e o caminho dos juízes concelhios acabando antes das prateleiras", b)


# ───────────────────────── norma: the fixed text and the needs that drift away from it
def norma(p):
    x0, x1, y0 = 24, 300, 120
    b = [L(x0, 296, x1, 296, INK2, 1.4), P(f"M{x1 - 8} 290 L{x1} 296 L{x1 - 8} 302", INK2, 1.4),
         L(x1, 290, x1, 302, INK2, 1.4), T(x1, 322, "momento da aplicação", 15, fill=INK2, anchor="end", font_style="italic")]
    b += [L(x1, y0 + 8, x1, 290, GRID, 1, stroke_dasharray="2 5")]
    b += [P(f"M{x0} {y0} H{x1}", INK, 5), S.circle(x0, y0, 5.5, fill=PAPER, stroke=INK, stroke_width=2), T(x0, y0 - 18, "norma estabelecida", 17)]
    b += [L(252, y0 - 10, 252, y0 + 10, ORANGE, 3.4), T(x1 + 6, y0 - 18, "sem derrogação", 15, fill=ORANGE, anchor="end")]
    b += [P(f"M{x0} {y0} C{x0 + 120} {y0 + 6} {x0 + 190} {y0 + 60} {x1} {y0 + 150}", BLUE, 2.4), S.circle(x1, y0 + 150, 4.4, fill=BLUE, stroke=BLUE),
          T(x0, y0 + 86, "necessidades da época", 17, fill=BLUE)]
    b += [P(f"M{x1 + 14} {y0} H{x1 + 22} V{y0 + 150} H{x1 + 14}", BLUE, 2), T(x1 + 38, y0 + 75, "interpretação", 16, fill=BLUE, anchor="middle", transform=f"rotate(90 {x1 + 38} {y0 + 70})")]
    b += [L(S_x, 290, S_x, 302, INK2, 1.2) for S_x in (80, 130, 180, 230, 280)]
    return carded(358, 336, "Uma norma que não se derroga e necessidades que se afastam dela até o momento da aplicação; a interpretação ocupa a distância", b)


# ───────────────────────── pontos: five stations sighting one question
def pontos(p):
    cx, cy, R = 172, 176, 122
    b = [S.circle(cx, cy, 52, fill="none", stroke=GRID, stroke_width=1.2, stroke_dasharray="2 5")]
    b += [L(cx - 70, cy, cx + 70, cy, GRID, 1), L(cx, cy - 70, cx, cy + 70, GRID, 1)]
    names = ["definição", "causas", "analogia", "exemplos", "autoridade"]
    angs = [-90, -18, 54, 126, 198]
    for nm, a in zip(names, angs):
        r = math.radians(a)
        sx, sy = cx + R * math.cos(r), cy + R * math.sin(r)
        ex, ey = cx + 20 * math.cos(r), cy + 20 * math.sin(r)
        b += [L(sx - 4 * math.cos(r), sy - 4 * math.sin(r), ex, ey, INK, 1.8)]
        ax, ay = cx + 20 * math.cos(r), cy + 20 * math.sin(r)
        b += [P(f"M{ax + 9 * math.cos(r) - 5 * math.sin(r):.1f} {ay + 9 * math.sin(r) + 5 * math.cos(r):.1f} L{ax:.1f} {ay:.1f} L{ax + 9 * math.cos(r) + 5 * math.sin(r):.1f} {ay + 9 * math.sin(r) - 5 * math.cos(r):.1f}", INK, 1.8)]
        b += [S.path(f"M{sx - 6 * math.sin(r):.1f} {sy + 6 * math.cos(r):.1f} L{sx + 6 * math.sin(r):.1f} {sy - 6 * math.cos(r):.1f} L{sx + 11 * math.cos(r):.1f} {sy + 11 * math.sin(r):.1f} Z", fill=PAPER, stroke=INK, stroke_width=1.8, stroke_linejoin="round")]
        ly = sy - 18 if a in (-90, -18, 198) else sy + 28
        b.append(T(sx, ly, nm, 17, anchor="middle"))
    b += [S.circle(cx, cy, 15, fill=PAPER, stroke=BLUE, stroke_width=2.6), S.circle(cx, cy, 4.5, fill=BLUE, stroke=BLUE), T(cx, cy + 74, "a questão", 16, fill=BLUE, anchor="middle")]
    return carded(344, 352, "Cinco lugares de onde se visa a mesma questão: definição, causas, analogia, exemplos e autoridade", b)


# ───────────────────────── genero: containment, read upward (define) and downward (divide)
def genero(p):
    b = [S.circle(186, 186, 174, fill="none", stroke=INK2, stroke_width=1.6), T(186, 44, "relação jurídica", 17, fill=INK2, anchor="middle"),
         S.circle(186, 214, 122, fill=PAPER2, stroke=INK, stroke_width=2.4), T(186, 118, "contrato", 20, anchor="middle")]
    for (x, y, l1, l2) in ((186, 172, "compra", "e venda"), (126, 246, "locação", ""), (246, 246, "mútuo", "")):
        b.append(S.circle(x, y, 44, fill=PAPER, stroke=BLUE, stroke_width=2))
        if l2:
            b += [T(x, y - 2, l1, 15, anchor="middle"), T(x, y + 16, l2, 15, anchor="middle")]
        else:
            b.append(T(x, y + 5, l1, 15, anchor="middle"))
    b += [P("M342 346 V310", INK, 2), P("M336 318 L342 308 L348 318", INK, 2), T(342, 366, "definir", 14, fill=INK2, anchor="middle"),
          P("M30 310 V346", INK, 2), P("M24 338 L30 348 L36 338", INK, 2), T(30, 366, "dividir", 14, fill=INK2, anchor="middle")]
    return carded(372, 380, "Espécies dentro do contrato e o contrato dentro da relação jurídica: definir sobe, dividir desce", b)


# ───────────────────────── razao: the same reason on one rule, equal and greater
def razao(p):
    thr = 140
    b = [L(thr, 36, thr, 214, ORANGE, 1.6, stroke_dasharray="3 5"), T(thr, 24, "a razão da consequência", 15, fill=ORANGE, anchor="middle")]
    for y, name in ((86, "a pari"), (176, "a fortiori")):
        b += [L(22, y + 16, 350, y + 16, INK2, 1.4)]
        b += [S.circle(thr, y, 10, fill=PAPER, stroke=INK, stroke_width=2.2)]
        b.append(T(22, y - 28, name, 19, anchor="start"))
    b += [S.circle(thr + 0, 86 - 22, 8, fill=BLUE, stroke=BLUE), T(thr + 18, 86 - 18, "mesma razão", 15, fill=BLUE)]
    b += [S.circle(270, 176, 10, fill=BLUE, stroke=BLUE), P(f"M{thr + 14} 176 H252", BLUE, 2.2), P("M244 170 L254 176 L244 182", BLUE, 2.2), T(206, 160, "mais razão", 15, fill=BLUE, anchor="middle")]
    b += [T(thr + 14, 118, "figura conhecida", 14, fill=INK2, anchor="start"), T(270, 210, "figura comparada", 14, fill=INK2, anchor="middle")]
    return carded(372, 232, "A pari: a figura comparada tem a mesma razão da conhecida. A fortiori: tem razão maior", b)


# ───────────────────────── compilacoes: the dated writing-down of the kingdoms' laws
def compilacoes(p):
    X = lambda yr: 60 + (yr - 1470) * 6.5
    ay = 150
    b = [L(60, ay, 1040, ay, INK, 1.8)]
    for yr in range(1470, 1621, 10):
        b.append(L(X(yr), ay - (6 if yr % 20 == 0 else 3), X(yr), ay + (6 if yr % 20 == 0 else 3), INK, 1.4))
        if yr % 20 == 0 and 1480 <= yr <= 1620:
            b.append(T(X(yr), ay + 24, str(yr), 14, fill=INK2, anchor="middle"))
    up = [(1518, 36, "Baviera · reforma que reúne as fontes do direito bávaro"),
          (1520, 74, "Baviera · ordenação que unifica o processo"), (1531, 112, "Holanda · recolha escrita do direito local, por Carlos V")]
    for yr, top, lab in up:
        b += [L(X(yr), ay, X(yr), top, BLUE, 1.8), S.circle(X(yr), top, 4.6, fill=BLUE, stroke=BLUE), T(X(yr) + 11, top + 5, f"{yr}", 14, family=S.MONO, fill=BLUE),
              T(X(yr) + 50, top + 5, lab, 15)]
    dn = [(1484, 192, "Castela · Ordenanzas Reales", "r"), (1567, 192, "Castela · compilação da legislação régia", "r"), (1611, 226, "Bélgica · Édit Perpétuel, a recolha do direito local", "l")]
    for yr, bot, lab, side in dn:
        b += [L(X(yr), ay, X(yr), bot, BLUE, 1.8), S.circle(X(yr), bot, 4.6, fill=BLUE, stroke=BLUE)]
        if side == "r":
            b += [T(X(yr) + 11, bot + 5, f"{yr}", 14, family=S.MONO, fill=BLUE), T(X(yr) + 50, bot + 5, lab, 15)]
        else:
            b += [T(X(yr) - 10, bot + 5, lab, 15, anchor="end"), T(X(yr) + 11, bot + 5, f"{yr}", 14, family=S.MONO, fill=BLUE)]
    return svg(1100, 250, "Compilações dos reinos entre 1484 e 1611: Castela, Baviera, Holanda e Bélgica passam o direito local para o escrito", b)


# ───────────────────────── passo: the one text under four films
def _pt(x, y, w, h, skew, u, v):
    return x + skew * (1 - v / h) + u, y + v


def _poly(x, y, w, h, skew, pts):
    return [_pt(x, y, w, h, skew, u, v) for u, v in pts]


def _pg(pts, **kw):
    return S.path("M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts) + " Z", **kw)


def passo(p):
    W, H, SK = 560, 62, 110
    x0, step, base = 30, 84, 362
    cores = {}
    b = []
    for i in range(5):
        y = base - i * step
        film = i > 0
        pts = _poly(x0, y, W, H, SK, [(0, 0), (W, 0), (W, H), (0, H)])
        b.append(_pg(pts, fill=PAPER if not film else "none", stroke=INK if not film else INK2, stroke_width=1.9 if not film else 1.5, stroke_linejoin="round"))
        cu0, cu1, cv0, cv1 = 220, 340, 14, H - 14
        cores[i] = [_pt(x0, y, W, H, SK, cu0, cv0), _pt(x0, y, W, H, SK, cu1, cv0), _pt(x0, y, W, H, SK, cu1, cv1), _pt(x0, y, W, H, SK, cu0, cv1)]
        for k in range(4):
            v = cv0 + 6 + k * 11
            xa, ya = _pt(x0, y, W, H, SK, cu0 + 8, v)
            xb, yb = _pt(x0, y, W, H, SK, cu1 - 8 - (14 if k == 3 else 0), v)
            b.append(L(xa, ya, xb, yb, INK if i == 0 else (BLUE if i == 4 else GRID), 1.8 if i in (0, 4) else 1.1))
        if i == 0:
            b.append(_pg(cores[0], fill="none", stroke=INK, stroke_width=1.6))
        if i == 1:
            for k in range(3):
                xa, ya = _pt(x0, y, W, H, SK, cu0 + 12, cv0 + 11 + k * 11)
                b.append(P(wave(xa, xa + 74 - k * 8, ya, 2.2, 8), BLUE, 1.8))
            for (u, v, ln) in ((46, 20, 94), (400, 38, 90)):
                xa, ya = _pt(x0, y, W, H, SK, u, v)
                b.append(P(wave(xa, xa + ln, ya, 1.8, 8), BLUE, 1.3))
        if i == 2:
            for v in range(8, H - 6, 6):
                for (ua, ub) in ((20, 200), (360, 540)):
                    xa, ya = _pt(x0, y, W, H, SK, ua, v)
                    xb, yb = _pt(x0, y, W, H, SK, ub, v)
                    b.append(L(xa, ya, xb, yb, INK2, 1.2))
            for v in (6, H - 6):
                xa, ya = _pt(x0, y, W, H, SK, 200, v)
                xb, yb = _pt(x0, y, W, H, SK, 360, v)
                b.append(L(xa, ya, xb, yb, GRID, 1.1))
        if i == 3:
            for (ua, ub) in ((34, 150), (410, 526)):
                q = _poly(x0, y, W, H, SK, [(ua, 12), (ub, 12), (ub, H - 12), (ua, H - 12)])
                b.append(_pg(q, fill=PAPER, stroke=INK, stroke_width=1.5))
                for k in range(3):
                    xa, ya = _pt(x0, y, W, H, SK, ua + 12, 26 + k * 9)
                    xb, yb = _pt(x0, y, W, H, SK, ub - 12, 26 + k * 9)
                    b.append(L(xa, ya, xb, yb, GRID, 1.1))
            for (ua, ub) in ((150, 220), (340, 410)):
                xa, ya = _pt(x0, y, W, H, SK, ua, H / 2)
                xb, yb = _pt(x0, y, W, H, SK, ub, H / 2)
                b.append(L(xa, ya, xb, yb, BLUE, 2.0))
        if i == 4:
            for (ua, ub) in ((20, 200), (360, 540)):
                q = _poly(x0, y, W, H, SK, [(ua, 8), (ub, 8), (ub, H - 8), (ua, H - 8)])
                b.append(_pg(q, fill="none", stroke=INK2, stroke_width=1.1, stroke_dasharray="4 5"))
                for v in (22, 40):
                    xa, ya = _pt(x0, y, W, H, SK, ua + 18, v + 8)
                    xb, yb = _pt(x0, y, W, H, SK, ub - 18, v - 12)
                    b.append(L(xa, ya, xb, yb, ORANGE, 2.4))
            b.append(_pg(cores[4], fill="none", stroke=BLUE, stroke_width=2.4))
    for k in (0, 1):
        for i in range(4):
            a, c = cores[i][k], cores[i + 1][k]
            b.append(L(a[0], a[1], c[0], c[1], BLUE, 1.2, stroke_dasharray="2 5"))
    names = [("O texto de Justiniano", "o passo, como saiu da compilação"), ("Irnério", "a glosa entre as linhas e à margem"),
             ("Acúrsio", "a Magna Glosa envolve o texto"), ("Bártolo", "o parecer o reúne a outras fontes"), ("Um humanista", "o aparato retirado, o texto de volta")]
    for i, (n1, n2) in enumerate(names):
        y = base - i * step + H / 2
        xs, xr = x0 + W + SK / 2 + 8, x0 + W + SK + 40
        b += [L(xs, y, xr - 10, y, GRID, 1.2), T(xr, y - 3, n1, 19), T(xr, y + 18, n2, 15, fill=INK2)]
    return svg(1100, 440, "O mesmo passo do Corpus sob quatro películas: a glosa de Irnério, a Magna Glosa de Acúrsio, o parecer de Bártolo e a leitura do humanista, cada mão acrescentando uma camada ao mesmo texto", b)


# ───────────────────────── linhagens: the schools as genealogies (dated where the book dates)
def _dot(x, y, filled=False, r=5):
    return S.circle(x, y, r, fill=INK if filled else PAPER, stroke=INK, stroke_width=1.8)


def lin_glosa(p):
    b = []
    cx = 40
    b += [T(20, 28, "civilistas", 14, fill=INK2), T(192, 28, "canonistas", 14, fill=INK2)]
    b += [P(f"M{cx} 62 V262", INK, 1.8), _dot(cx, 62, True, 6), T(cx + 14, 67, "Irnério", 17)]
    for k, n in enumerate(["Martinho", "Búlgaro", "Jacobus", "Hugo"]):
        yy = 112 + k * 28
        b += [L(cx, yy, cx + 24, yy, INK, 1.6), _dot(cx + 24, yy), T(cx + 38, yy + 5, n, 16)]
    b += [S.circle(cx, 262, 7, fill=BLUE, stroke=BLUE), T(cx + 14, 260, "Acúrsio", 17), T(cx + 14, 280, "Magna Glosa", 14.5, fill=BLUE)]
    b += [P(f"M{cx} 269 V338", INK, 1.6), _dot(cx, 338), T(cx + 14, 336, "Azo", 17), T(cx + 14, 356, "Summa codicis", 14.5, fill=INK2)]
    c0 = 192
    b += [_dot(c0, 62, True, 6), T(c0 + 14, 67, "Hostiense", 17), T(c0 + 14, 86, "Henrique de Susa", 14, fill=INK2)]
    b += [L(c0, 68, c0, 300, GRID, 1.2, stroke_dasharray="2 5")]
    b += [T(c0 + 14, 140, "Decretum", 15.5, fill=INK2, font_style="italic")]
    for k, n in enumerate(("João Hispano", "Lourenço Hispano")):
        b += [_dot(c0, 164 + k * 24, r=4), T(c0 + 14, 169 + k * 24, n, 15.5)]
    b += [T(c0 + 14, 240, "Decretais", 15.5, fill=INK2, font_style="italic")]
    for k, n in enumerate(("Vicente Hispano", "Raimundo de Penyafort")):
        b += [_dot(c0, 264 + k * 24, r=4), T(c0 + 14, 269 + k * 24, n, 15.5)]
    return carded(372, 376, "Os glosadores: Irnério e seus quatro discípulos diretos, Acúrsio, que reuniu o que fizeram, Azo; e os canonistas em torno do Decretum e das Decretais", b)


def lin_comenta(p):
    yr0, yr1, x0, x1 = 1250, 1530, 14, 358
    X = lambda y: x0 + (y - yr0) * (x1 - x0) / (yr1 - yr0)
    b = []
    rows = [("Cino de Pistóia", 1270, 1336), ("Bártolo de Sassoferrato", 1314, 1357), ("Baldo de Ubaldis", 1327, 1400), ("Paulo de Castro", None, 1441), ("Jasão del Maino", 1435, 1519)]
    top, rh = 46, 54
    for yr in range(1300, 1501, 50):
        b += [L(X(yr), top - 8, X(yr), top + 5 * rh - 6, GRID, 1, stroke_dasharray="2 5"), T(X(yr), top - 16, str(yr), 13, fill=INK2, anchor="middle", family=S.MONO)]
    for k, (n, a, z) in enumerate(rows):
        yy = top + 36 + k * rh - 12
        start = X(a) if a else X(1395)
        nx = max(x0, min(start - 4, 358 - 8.4 * len(n)))
        b.append(T(nx, yy - 12, n, 16))
        if a is None:
            b += [P(f"M{X(1395)} {yy} H{X(z)}", INK, 3.4, stroke_dasharray="3 6"), _dot(X(z), yy, True, 4.4)]
        else:
            b += [P(f"M{X(a)} {yy} H{X(z)}", BLUE if k == 1 else INK, 6 if k == 1 else 3.4), _dot(X(a), yy, k == 0, 4.4), _dot(X(z), yy, False, 4.4)]
    yb = top + 5 * rh + 24
    b += [T(24, yb, "Rafaele Fulgosio, João de Andrea e", 15), T(24, yb + 20, "Nicolau de Tudeschi, o Abade Panormitano", 15), P(f"M14 {yb - 14} V{yb + 24}", INK2, 1.4)]
    return carded(372, int(yb + 20), "Os comentadores em suas vidas datadas: Cino, que fundou a escola, Bártolo, o mais influente, Baldo, Paulo de Castro e Jasão del Maino; três nomes sem datas", b)


def lin_humanismo(p):
    yr0, yr1, x0, x1 = 1450, 1760, 330, 1070
    X = lambda y: x0 + (y - yr0) * (x1 - x0) / (yr1 - yr0)
    groups = [
        ("precursores", [("Policiano e Lourenço Valla", None, None), ("Zasius", 1461, 1535), ("Budé", 1467, 1540), ("Alciato", 1492, 1550), ("António de Gouveia", None, 1566)]),
        ("escola culta", [("Cujas", 1532, 1590), ("Hotman", 1524, 1590), ("Doneau, Duarenus e Brissonius", None, None)]),
        ("geração posterior", [("Grócio", 1583, 1645), ("Vinnius, Voet e Noodt", None, None)]),
        ("usus modernus", [("Carpzov", 1595, 1666), ("Struve", 1619, 1692), ("Stryk", 1640, 1710), ("Böhmer", 1674, 1749), ("Leyser", 1683, 1752), ("Heineccius", None, None)]),
        ("sistematizadores", [("Chansonette, Hegendorff, Derrer, Freigio e Donnello", None, None)]),
    ]
    b = []
    top, rh = 50, 25
    n = sum(len(g[1]) for g in groups) + (len(groups) - 1) * 0.6
    bot = top + n * rh - 6
    for yr in range(1450, 1761, 50):
        b += [L(X(yr), top - 14, X(yr), bot, GRID, 1, stroke_dasharray="2 5"), T(X(yr), top - 22, str(yr), 14, fill=INK2, anchor="middle", family=S.MONO)]
    yy = top
    for gi, (g, rows) in enumerate(groups):
        if gi:
            b.append(L(8, yy - 14, x1, yy - 14, GRID, 1))
        b.append(T(8, yy + 5, g, 15, fill=INK2))
        for (nm, a, z) in rows:
            if a is None and z is None:
                b.append(T(190, yy + 5, nm, 16, fill=INK2))
            else:
                b.append(T(190, yy + 5, nm, 16))
                if a is None:
                    b += [P(f"M{X(z) - 36} {yy} H{X(z)}", INK, 3.4, stroke_dasharray="3 6"), _dot(X(z), yy, True, 4.4)]
                else:
                    b += [P(f"M{X(a)} {yy} H{X(z)}", INK, 3.4), _dot(X(a), yy, False, 4.4), _dot(X(z), yy, False, 4.4)]
            yy += rh
        yy += rh * 0.6
    return svg(1100, int(bot + 14), "O humanismo e o usus modernus em vidas datadas: os precursores, a escola culta, a geração posterior, os alemães do usus modernus e os primeiros sistematizadores", b)


MODES = {"hero": hero, "consulta": consulta, "volumes": volumes, "glosa": glosa, "parecer": parecer, "terra": terra,
         "vinculos": vinculos, "apresentacao": apresentacao, "autoridade": autoridade, "crise": crise,
         "depuracao": depuracao, "vigencia": vigencia, "jurisdicoes": jurisdicoes,
         "norma": norma, "lin_glosa": lin_glosa, "lin_comenta": lin_comenta, "lin_humanismo": lin_humanismo, "pontos": pontos, "genero": genero, "razao": razao, "compilacoes": compilacoes, "passo": passo}


def build(p: dict) -> tuple[str, list[dict]]:
    mode = p.get("mode")
    if mode not in MODES:
        raise ValueError(f"mj01: mode must be one of {', '.join(MODES)}")
    return MODES[mode](p), []
