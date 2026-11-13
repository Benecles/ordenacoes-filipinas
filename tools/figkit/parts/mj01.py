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
Colours are house tokens: blue = what governs / was decided, orange = the limit or the objection.
"""
from __future__ import annotations

import math

from . import svg as S

INK, INK2, MUTED, GRID, PAPER = S.INK, S.INK2, S.MUTED, S.GRID, S.PAPER
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
    lane_c, lane_r, lane_l = 108, 196, 290
    x0 = 176
    b = []
    for x in (512, 812):
        b.append(L(x, 70, x, 392, GRID, 1, stroke_dasharray="2 6"))
    b += [T(392, 28, "Bolonha · XII–XIII", 19, family=S.SANS, anchor="middle"),
          T(392, 50, "Irnério → Acúrsio", 17, fill=INK2, anchor="middle"),
          T(662, 28, "cidades italianas · XIV–XV", 19, family=S.SANS, anchor="middle"),
          T(662, 50, "Cino · Bártolo · Baldo", 17, fill=INK2, anchor="middle"),
          T(950, 28, "século XVI", 19, family=S.SANS, anchor="middle")]
    dot = lambda y: S.circle(x0, y, 5.5, fill=PAPER, stroke=INK, stroke_width=2)
    # the canonical limit: a ceiling that bounds the rail
    can = [P(f"M300 {lane_c} V84 H812 V{lane_c}", ORANGE, 1.8), T(556, 74, "limite canônico", 16, fill=ORANGE, anchor="middle"),
           P(f"M{x0} {lane_c} H940", INK, 2.6), dot(lane_c), T(x0 - 16, lane_c + 6, "canônico", 20, anchor="end")]
    # local rail: wavy while it keeps changing, then it rises and is written down (straight, heavy)
    loc = [P(wave(x0, 830, lane_l, 5, 26), INK, 2.2), P(curve(830, lane_l, 880, lane_r), INK, 5), P(f"M880 {lane_r} H940", INK, 5),
           dot(lane_l), T(x0 - 16, lane_l + 6, "direito próprio", 20, anchor="end"), T(956, lane_r + 6, "direitos nacionais", 17)]
    # roman rail: heavy until the sixteenth century, then it drops to the lower lane and thins; it splits in two
    rom = [P(f"M{x0} {lane_r} H830", INK, 5), P(curve(830, lane_r, 880, lane_l), INK, 3), P(f"M880 {lane_l} H892", INK, 3),
           P(curve(892, lane_l, 934, 252), INK, 2.6), P("M934 252 H946", INK, 2.6),
           P(curve(892, lane_l, 934, 352), INK, 2.6), P("M934 352 H946", INK, 2.6),
           S.circle(855, (lane_r + lane_l) / 2, 5, fill=PAPER, stroke=INK, stroke_width=1.6),
           dot(lane_r), T(x0 - 16, lane_r + 6, "romano", 20, anchor="end"),
           T(956, 258, "mos gallicus", 20), T(956, 280, "sentido histórico", 16, fill=INK2),
           T(956, 358, "usus modernus", 20), T(956, 380, "vigência prática", 16, fill=INK2),
           T(855, 336, "subsidiário", 16, fill=INK2, anchor="middle")]
    # Bolonha: the fixed text and its apparatus, laid over the roman rail
    nx0, ny0, nw, nh = 352, 164, 70, 64
    rom += [S.rect(298, 132, 176, 128, fill=PAPER, stroke=INK, stroke_width=1.2)]
    for i in range(7):
        rom.append(L(304, 138 + i * 3.2, 468, 138 + i * 3.2, GRID, 1))
        rom.append(L(304, 240 + i * 3, 468, 240 + i * 3, GRID, 1))
    for i in range(9):
        rom.append(L(304 + i * 3.2, 160, 304 + i * 3.2, 236, GRID, 1))
        rom.append(L(440 + i * 3.4, 160, 440 + i * 3.4, 236, GRID, 1))
    rom += [S.rect(nx0, ny0, nw, nh, fill=PAPER, stroke=INK, stroke_width=2.4)]
    rom += writing(nx0 + 8, ny0 + 11, [54, 50, 54, 46, 54, 40], 9.4, INK, 1.4)
    for i, yy in enumerate((ny0 + 15.7, ny0 + 34.5, ny0 + 53.3)):
        rom.append(P(wave(nx0 + 12, nx0 + 46 + i * 6, yy, 1.6, 8), BLUE, 1.1))
    rom += [T(386, 284, "Magna Glosa", 17, fill=INK2, anchor="middle")]
    # Comentadores: ties among the rails, then the consilium sheet
    com = []
    for x in (548, 584, 620, 656):
        com.append(L(x, lane_c, x, lane_l, INK2, 1.2))
        for yy in (lane_c, lane_r, lane_l):
            com.append(S.circle(x, yy, 3.6, fill=INK, stroke=INK, stroke_width=1))
    com += [T(602, 334, "concordar · distinguir", 16, fill=INK2, anchor="middle", font_style="italic")]
    sx, sy, sw_, sh = 712, 150, 96, 92
    com += [S.path(f"M{sx + 14} {sy} H{sx + sw_ + 14} L{sx + sw_} {sy + sh} H{sx} Z", fill=PAPER, stroke=INK, stroke_width=2),
            *[L(sx + 20 - i * 3.5, sy + 20 + i * 18, sx + sw_ - 2 - i * 3.5, sy + 20 + i * 18, INK, 1.3) for i in range(4)]]
    com += [P(curve(684, lane_c, sx + 18, sy + 20), BLUE, 1.8), P(curve(684, lane_l, sx + 8, sy + 74), BLUE, 1.8),
            S.circle(sx + 18, sy + 20, 3.4, fill=BLUE, stroke=BLUE), S.circle(sx + 8, sy + 74, 3.4, fill=BLUE, stroke=BLUE)]
    com += [T(sx + 54, 266, "consilium", 18, anchor="middle")]
    b += [_thread("mj-canonico", "Trilho canônico, contido pelo limite canônico", [f"M{x0} {lane_c} H940"], can),
          _thread("mj-proprio", "Trilho do direito próprio, que chega aos direitos nacionais", [wave(x0, 830, lane_l, 5, 26)], loc),
          _thread("mj-romano", "Trilho romano, da Magna Glosa ao mos gallicus e ao usus modernus", [f"M{x0} {lane_r} H296", f"M476 {lane_r} H830"], rom),
          _thread("mj-comentadores", "Os comentadores: ligações entre os trilhos e o consilium",
                  [f"M{x} {lane_c} V{lane_l}" for x in (548, 584, 620, 656)], com)]
    return svg(1100, 404, "Planta das escolas jurídicas: as fontes percorrem Bolonha e os comentadores até o século XVI", b)


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
    titles = ("Novara", "Modena", "Sicília")
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
    b += [P(f"M277 {y + h + 4} V{y + h + 90} H150", BLUE, 1.6), T(14, y + h + 96, "Volumen parvum", 16, fill=BLUE, anchor="start")]
    # the opened Volumen parvum: five quires, each its own writing
    y0 = 306
    quires = ["tres libri", "Institutiones", "parte das Novelas", "Libri feudorum", "constituições do Sacro Império"]
    kinds2 = ["horiz", "dots", "diag", "cross", "horiz"]
    for i, (n, k) in enumerate(zip(quires, kinds2)):
        yy = y0 + i * 26
        b += slab(14, yy, 104, 18, dx=20, dy=-9, stroke=BLUE if i == 0 else INK, sw=1.5)
        b += _hatch_block(36, yy + 3, 138, 12, "horiz" if k in ("horiz", "dots") else "diag", INK2) if False else []
        b += [T(150, yy + 14, n, 14)]
    return svg(372, 446, "Os cinco volumes do Corpus na escola; o Volumen parvum aberto em cadernos de origens diferentes", b)



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
def terra(p):
    """One strip of soil; each hold is a bar whose posts reach every part of it. The posts of the second hold fall
    between those of the first: both cover the whole and nothing divides the ground."""
    st = _state(p, 3)
    x0, x1, soil = 36, 336, 276
    up_y, low_y = 104, 196
    b = [S.rect(30, soil, 312, 34, fill=PAPER, stroke=INK, stroke_width=2.2)]
    b += S.hatch(34, soil + 4, 304, 26, 9, stroke=GRID, stroke_width=1)
    b.append(T(186, 346, "a mesma terra", 19, anchor="middle"))
    n = 9
    step = (x1 - x0) / (n - 1)
    ups = [x0 + k * step for k in range(n)]
    lows = [x0 + step / 2 + k * step for k in range(n - 1)]
    if st >= 2:
        b += [L(x, low_y, x, soil, BLUE, 2) for x in lows]
        b += [L(x, soil, x, soil + 0, BLUE, 2) for x in []]
    b += [L(x, up_y, x, soil, INK, 2) for x in ups]
    if st >= 2:
        b += [S.rect(x0 - 6, low_y - 3, x1 - x0 + 12, 6, fill=BLUE, stroke=BLUE, stroke_width=1)]
    b += [S.rect(x0 - 6, up_y - 3, x1 - x0 + 12, 6, fill=INK, stroke=INK, stroke_width=1)]
    if st >= 2:
        b += fade([T(x0 - 6, up_y - 38, "dominium directum", 19), T(x0 - 6, low_y - 38, "dominium utile", 19, fill=PAPER, stroke=PAPER, stroke_width=7, stroke_linejoin="round"), T(x0 - 6, low_y - 38, "dominium utile", 19, fill=BLUE)], st == 2)
    if st == 3:
        b += [T(x1 + 6, up_y - 38, "actio directa", 17, fill=INK2, anchor="end"), T(x1 + 6, low_y - 38, "actio utilis", 17, fill=PAPER, stroke=PAPER, stroke_width=7, stroke_linejoin="round", anchor="end"), T(x1 + 6, low_y - 38, "actio utilis", 17, fill=BLUE, anchor="end")]
        for y, col in ((up_y, INK), (low_y, BLUE)):
            b += fade([P(f"M{x0 + 4} {y - 16} H{x1 - 6}", col, 2.2), P(f"M{x1 - 16} {y - 22} L{x1 - 6} {y - 16} L{x1 - 16} {y - 10}", col, 2.2)])
    return svg(372, 362, ("Uma posição cobre toda a terra", "Uma segunda posição cobre a mesma terra; nenhuma linha reparte o solo", "A actio directa e a actio utilis correm ao longo de cada posição")[st - 1], b)


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
    b += [T(210, 104, "proprietário", 17, fill=BLUE, anchor="middle"), T(290, 198, "móveis", 17, fill=BLUE, anchor="middle")]
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


MODES = {"hero": hero, "consulta": consulta, "volumes": volumes, "glosa": glosa, "parecer": parecer, "terra": terra,
         "vinculos": vinculos, "apresentacao": apresentacao, "autoridade": autoridade, "crise": crise,
         "depuracao": depuracao, "vigencia": vigencia}


def build(p: dict) -> tuple[str, list[dict]]:
    mode = p.get("mode")
    if mode not in MODES:
        raise ValueError(f"mj01: mode must be one of {', '.join(MODES)}")
    return MODES[mode](p), []
