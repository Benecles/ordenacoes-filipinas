"""topica_cia: drawings for the Metodologia companion 01.2 (A tópica e a dialética), 12/11.

Every drawing keeps one received text in place and shows what is done round it. Writing is schematic: steady rules
are the received text, wavering rules are a hand writing in the margin or between the lines. Words only name what
the picture already shows.

Params:
  mode   oficina | arvore | comparar | colacao | oficio (required)
  state  arvore, colacao, oficio: 1..3 (the page puts each state inside a .panel, one per paragraph)

Canvases: oficina 1100x336; arvore 500x580; comparar 372x330; colacao 436x500; oficio 436x540.

oficina: the folio of the statute (Hespanha pp.470-479). Four marginal glosses (definir/dividir, causas, comparacao,
autoridades) tie to the same line; an interlinear extension sits on it (the procurator's presentation, p.469);
an objection crosses the marginal reading and returns to the line. Hovering a gloss lights its thread (page CSS).
arvore: genus/species ladder of pp.472-474: donation under contract; contract under legal relation; division back
down. The two criteria that divide contract hang apart from the species (they are not attached to them).
comparar: a pari (same feature, same extent, same consequence) and a fortiori (the feature stronger in the second
figure, its extent runs past the first, a reinforced reason for the same consequence). Ordinal only: no scale.
colacao: aligned excerpts of one passage across commentaries (pp.475-477). State 1 one expert's credit; 2 the same
reading repeated and orienting; 3 the counter-reading crosses it. No head count: the leaves are not authors.
oficio: Gribaldo's eight operations (pp.477-478) on one folio. State 1 praemitto; 2 scindo, summo, casumque figuro,
perlego; 3 do causas, connoto, et obiicio.
"""
from __future__ import annotations

from . import svg as S


def _t(x, y, words, size=20, fill=S.INK, family=S.SERIF, **kw):
    return S.text(x, y, words, size=size, fill=fill, family=family, **kw)


def _p(d, stroke=S.INK, width=1.5, **kw):
    return S.path(d, fill="none", stroke=stroke, stroke_width=width,
                  stroke_linecap="round", stroke_linejoin="round", **kw)


def _head(x, y, direction, colour=S.INK, width=1.6):
    d = {"right": f"M{x - 8} {y - 5} L{x} {y} L{x - 8} {y + 5}",
         "left": f"M{x + 8} {y - 5} L{x} {y} L{x + 8} {y + 5}",
         "up": f"M{x - 5} {y + 8} L{x} {y} L{x + 5} {y + 8}",
         "down": f"M{x - 5} {y - 8} L{x} {y} L{x + 5} {y - 8}"}[direction]
    return _p(d, colour, width)


def _dot(x, y, colour=S.INK, fill=S.PAPER, r=5):
    return S.circle(x, y, r, fill=fill, stroke=colour, stroke_width=1.6)


def _ruled(x, y, widths, gap=14, colour=S.INK2, sw=1.4, opacity=".8"):
    """Steady rules: printed or received text."""
    return [S.line(x, y + i * gap, x + w, y + i * gap, stroke=colour, stroke_width=sw,
                   stroke_linecap="round", opacity=opacity) for i, w in enumerate(widths)]


def _wave(x, y, w, colour=S.INK2, sw=1.3, amp=1.7, period=8):
    n = max(1, int(w / period))
    step = w / n
    d = f"M{x} {y}"
    for i in range(n):
        d += f" Q{x + step * i + step / 2:.1f} {y + (amp if i % 2 else -amp):.1f} {x + step * (i + 1):.1f} {y}"
    return _p(d, colour, sw)


def _hand(x, y, widths, gap=13, colour=S.INK2, sw=1.3):
    """Wavering rules: a hand writing."""
    return [_wave(x, y + i * gap, w, colour, sw) for i, w in enumerate(widths)]


def _leaf(x, y, w, h, colour=S.INK, sw=1.4):
    return [S.rect(x + 3, y + 4, w, h, fill=S.PAPER, stroke=S.GRID, stroke_width=1),
            S.rect(x, y, w, h, fill=S.PAPER, stroke=colour, stroke_width=sw)]


def _fade(items, on=True):
    return [f'<g class="fade">{"".join(items)}</g>'] if on else list(items)


def _state(p, n=3):
    s = p.get("state", 1)
    if not isinstance(s, int) or isinstance(s, bool) or not 1 <= s <= n:
        raise ValueError(f"topica_cia: state must be an integer from 1 to {n}")
    return s


# ── oficina ────────────────────────────────────────────────────────────────────────────────────────────────────────
def _oficina(p):
    FX, FW, FY, FH = 404, 292, 22, 300
    TY = 166                      # the line the whole drawing turns on
    b = [_t(FX + FW / 2, 14, "estatuto", 13, fill=S.INK2, anchor="middle", font_style="italic")]
    # the folio: the received text stays whole in the middle; the one line the page turns on is written out
    b += [S.rect(FX + 5, FY + 6, FW, FH, fill=S.PAPER, stroke=S.GRID, stroke_width=1),
          S.rect(FX, FY, FW, FH, fill=S.PAPER, stroke=S.INK, stroke_width=1.6)]
    ys = [44 + 11 * i for i in range(5)] + [TY + 46 + 11 * i for i in range(10)]
    w1 = (236, 224, 232, 200, 230, 214, 236, 188, 226, 140, 232)
    for k, y in enumerate(ys):
        b.append(S.line(FX + 28, y, FX + 28 + w1[k % 11], y, stroke=S.INK2, stroke_width=1.3, stroke_linecap="round", opacity=".55"))
    for i, ln in enumerate(("o estatuto que dispõe acerca da", "apresentação em processo de um", "documento ou de uma testemunha")):
        b.append(_t(FX + 28, TY - 12 + i * 15, ln, 12.5, anchor=None))
    b.append(S.line(FX + 28, TY + 40 - 8, FX + 28 + 236, TY + 40 - 8, stroke=S.INK, stroke_width=1.2, opacity=".0"))
    # the extension written between the lines: the procurator enters by a reading added to the rule
    b += [_t(FX + 28, TY - 62, "compreende quer a apresentação pelo", 12, fill=S.DIF, font_style="italic"),
          _t(FX + 28, TY - 47, "próprio, quer pelo procurador", 12, fill=S.DIF, font_style="italic"),
          _p(f"M{FX + 20} {TY - 38} L{FX + 28} {TY - 28} L{FX + 36} {TY - 38}", S.DIF, 1.6)]

    # left margin: four ways of asking the same line, each in its own words
    glosses = (("definir · dividir", 12, "fork", ("contrato: gênero e diferença", "divide em espécies: compra, locação, mútuo")),
               ("causas", 90, "chain", ("a vontade declarada, causa eficiente,", "e a finalidade, causa final")),
               ("comparação", 168, "pair", ("a pari: a mesma razão nas duas figuras", "a fortiori: razão ainda maior na segunda")),
               ("autoridades", 246, "leaves", ("doctor est peritus", "opinio communis doctorum")))
    for gid, (name, y, glyph, lines) in enumerate(glosses):
        g = []
        cy = y + 20
        g.append(S.line(10, y + 25, 342, y + 25, stroke=S.INK, stroke_width=70, opacity="0"))   # hit area
        if glyph == "fork":
            g += [_p(f"M34 {y + 30} V{y + 18} M34 {y + 18} L22 {y + 4} M34 {y + 18} V{y + 2} M34 {y + 18} L46 {y + 4}", S.INK, 1.5), _dot(34, y + 33, r=3.4)]
        elif glyph == "chain":
            g += [_dot(20, y + 18, S.INK, S.INK, 3.2), _p(f"M25 {y + 18} H46", S.INK, 1.5), _head(50, y + 18, "right")]
        elif glyph == "pair":
            g += [_p(f"M20 {y + 8} H48 M20 {y + 26} H48", S.INK, 2.6), _p(f"M34 {y + 12} V{y + 22}", S.INK2, 1.1)]
        else:
            g += [S.path(f"M26 {y + 32} L48 {y + 29} L46 {y + 11} L25 {y + 13} Z", fill=S.PAPER, stroke=S.INK2, stroke_width=1),
                  S.path(f"M21 {y + 26} L43 {y + 23} L42 {y + 6} L20 {y + 7} Z", fill=S.PAPER, stroke=S.INK, stroke_width=1.2)]
        g.append(_t(70, y + 14, name, 13.5, anchor=None))
        for i, ln in enumerate(lines):
            g.append(_t(70, y + 32 + i * 15, ln, 12, fill=S.INK2, anchor=None))
        g.append(_p(f"M344 {cy + 8} C376 {cy + 8} 372 {TY} {FX + 22} {TY}", S.INK2, 1.3, class_="th"))
        b.append(f'<g class="gl" data-thread="g{gid}" tabindex="0" role="button" aria-label="{S.esc(name)}">' + "".join(g) + "</g>")
    b.append(S.circle(FX + 22, TY, 3.2, fill=S.INK))

    # right margin: the reading that came out, and the objection that crosses it
    RX = 738
    LE = FX + 28 + 214                       # where the line ends
    b += [_p(f"M{LE + 4} {TY - 2} C{LE + 40} {TY - 2} {RX - 36} {TY - 38} {RX - 10} {TY - 38}", S.DIF, 1.6),
          _p(f"M{FX + FW + 6} {TY - 22} H{FX + FW + 12} V{TY + 8} H{FX + FW + 6}", S.DIF, 1.5),
          _t(RX + 8, TY - 42, "solução provável", 13.5, fill=S.DIF),
          _t(RX + 8, TY - 25, "o estatuto compreende também", 12, fill=S.DIF), _t(RX + 8, TY - 10, "a apresentação pelo procurador", 12, fill=S.DIF),
          _p(f"M{RX} {TY - 62} V{TY + 14}", S.DIF, 1.4)]
    OY = 250
    b += [_t(RX + 8, OY, "objeção", 13.5, fill=S.CONC),
          _t(RX + 8, OY + 18, "Cino de Pistóia: “ainda que mil o dissessem,", 12, fill=S.CONC), _t(RX + 8, OY + 33, "todos errariam”", 12, fill=S.CONC),
          _p(f"M{RX + 40} {OY - 22} V{TY + 22}", S.CONC, 1.8), _head(RX + 40, TY + 24, "up", S.CONC, 1.8),
          _p(f"M{RX - 6} {OY + 18} C{RX - 52} {OY + 18} {LE + 40} {TY + 46} {LE + 6} {TY + 5}", S.CONC, 1.8),
          _head(LE + 5, TY + 5, "left", S.CONC, 1.8)]
    return S.svg(1100, 336, p.get("title") or
                 "Um estatuto no centro do fólio: quatro modos de perguntar por ele escrevem à margem e voltam à mesma linha; uma extensão entre as linhas leva a uma solução provável, e uma objeção a atravessa e retorna à linha de partida", b), []


# ── arvore ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def _arvore(p):
    s = _state(p)
    cx = 257
    y0, y1, ys = 96, 226, 376      # dots of the three levels
    xs = (100, 205, 310, 415)
    names = (("doação",), ("compra", "e venda"), ("locação",), ("mútuo",))
    ST = 292                        # horizontal bus of the species
    b = []
    up, dn = s < 3, s == 3
    DEF = S.DIF

    def elbow(i, colour, width, arrow=None):
        x = xs[i]
        out = [_p(f"M{cx} {y1 + 8} V{ST} H{x} V{ys - 8}", colour, width)]
        if arrow == "up":
            out.append(_head(cx, y1 + 10, "up", colour))
        if arrow == "down":
            out.append(_head(x, ys - 10, "down", colour))
        return out

    # level 1: the contract, always on
    b += [_t(cx - 20, y1 + 10, "contrato", 30, anchor="end"), _dot(cx, y1)]
    # species
    def species(i, colour=S.INK, ghost=False, tag=None):
        out = [_dot(xs[i], ys, colour, S.INK if i == 0 and not ghost else S.PAPER)]
        for k, w in enumerate(names[i]):
            out.append(_t(xs[i], ys + 34 + k * 22, w, 22 if k == 0 else 20, anchor="middle", fill=S.INK2 if ghost else S.INK))
        if tag:
            for k, w in enumerate(tag):
                out.append(_t(xs[i], ys + 34 + (len(names[i]) + k) * 20 + 4, w, 17, fill=S.INK2, anchor="middle", font_style="italic"))
        return out
    if s == 1:
        b += elbow(0, DEF, 2.2, "up")
        b += species(0, tag=("transferência", "gratuita"))
        b += [_p(f"M{cx} {ST} H{xs[1]} V{ys - 8}", S.GRID, 1.4, stroke_dasharray="4 5"), *species(1, ghost=True)]
        b += [_t(cx + 22, y1 + 4, "gênero", 19, fill=S.INK2, font_style="italic"),
              _t((cx + xs[0]) / 2 - 6, ST - 10, "definir", 20, fill=DEF, anchor="middle", font_style="italic")]
    if s == 2:
        b += elbow(0, DEF, 2.2, "up")
        b += species(0, tag=("transferência", "gratuita"))
        b += [_p(f"M{cx} {ST} H{xs[1]} V{ys - 8}", S.GRID, 1.4, stroke_dasharray="4 5"), *species(1, ghost=True)]
        up_new = [_t(cx - 20, y0 + 10, "relação jurídica", 30, anchor="end"), _dot(cx, y0),
                  _p(f"M{cx} {y1 - 8} V{y0 + 8}", DEF, 2.2), _head(cx, y0 + 10, "up", DEF),
                  _t(cx + 22, y0 + 4, "gênero", 19, fill=S.INK2, font_style="italic"),
                  _t((cx + xs[0]) / 2 - 6, ST - 10, "definir", 20, fill=DEF, anchor="middle", font_style="italic")]
        b += _fade(up_new)
        b.append(_t(cx + 22, y1 + 4, "espécie", 19, fill=S.INK2, font_style="italic"))
    if s == 3:
        b += [_t(cx - 20, y0 + 10, "relação jurídica", 30, anchor="end"), _dot(cx, y0),
              _p(f"M{cx} {y0 + 8} V{y1 - 8}", S.INK2, 1.5),
              _t(cx + 22, y1 + 4, "gênero", 19, fill=S.INK2, font_style="italic")]
        for i in range(4):
            b += elbow(i, S.INK2 if i else DEF, 1.6 if i else 2.2, "down" if i == 0 else None)
            b += species(i, tag=("transferência", "gratuita") if i == 0 else None)
        b += _fade([_head(xs[i], ys - 10, "down", S.INK2) for i in (1, 2, 3)]
                   + [_t(cx + 60, ST - 16, "dividir", 20, fill=DEF, font_style="italic")])  # clear of the elbows (measure CROSS, 13/11)
        # two other divisions of the same genus, by other criteria, hung apart from the species
        crit = [_p("M40 474 H460", S.GRID, 1),
                _t(cx, 504, "outros critérios de divisão do contrato", 19, fill=S.INK2, anchor="middle", font_style="italic")]
        for fx, a, c in ((125, "formais", "consensuais"), (385, "unilaterais", "bilaterais")):
            crit += [_dot(fx, 528), _p(f"M{fx} 534 C{fx} 546 {fx - 64} 542 {fx - 64} 554 M{fx} 534 C{fx} 546 {fx + 64} 542 {fx + 64} 554", S.INK2, 1.3),
                     _t(fx - 64, 582, a, 20, anchor="middle"), _t(fx + 64, 582, c, 20, anchor="middle")]
        b += _fade(crit)
    title = ["A doação enquadra-se no contrato, que se distingue de outras espécies pela transferência gratuita",
             "O contrato, por sua vez, é espécie de um gênero mais amplo, a relação jurídica",
             "A divisão percorre o caminho inverso: do contrato às suas espécies, e ainda outras divisões por critérios diferentes"][s - 1]
    return S.svg(500, 604, p.get("title") or title, b), []


# ── comparar ───────────────────────────────────────────────────────────────────────────────────────────────────────
def _comparar(p):
    b = []
    FX = 322

    def strip(y, name, ext, colour=S.DIF, extra=0):
        out = [_t(20, y - 12, name, 17, fill=S.INK2, font_style="italic"),
               S.line(20, y, 262, y, stroke=S.GRID, stroke_width=1.2),
               S.line(20, y, 20 + ext, y, stroke=colour, stroke_width=6, stroke_linecap="round")]
        if extra:
            out += [S.line(20 + ext, y, 20 + ext + extra, y, stroke=colour, stroke_width=6, stroke_linecap="round", opacity=".42"),
                    *S.hatch(20 + ext, y - 11, extra, 22, 7, stroke=colour, stroke_width=1)]
        end = 20 + ext + extra
        out += [_p(f"M{end + 12} {y} H{FX - 14}", S.INK2, 1.3), _head(FX - 8, y, "right", S.INK2)]
        return out
    # a pari: same feature, same extent
    b += [_t(20, 36, "a pari", 25, font_style="italic"),
          *strip(88, "uma figura", 90), *strip(142, "outra figura", 90),
          _p(f"M{FX} 62 V160", S.INK, 2.4), _t(FX + 20 - 20, 52, "a mesma consequência", 17, fill=S.INK2, anchor="end", font_style="italic")]
    # a fortiori: the second figure's feature runs past the first
    b += [_t(20, 212, "a fortiori", 25, font_style="italic"),
          *strip(264, "uma figura", 90), *strip(318, "outra figura", 90, extra=82),
          _p(f"M{FX} 238 V336", S.INK, 2.4),
          _t(20 + 172 + 14, 346, "razão reforçada", 17, fill=S.DIF, font_style="italic", anchor="start")]
    return S.svg(372, 360, p.get("title") or
                 "Na comparação a pari duas figuras com a mesma característica e a mesma extensão levam à mesma consequência; na a fortiori a característica da segunda se estende além da primeira, o que dá uma razão reforçada para a mesma consequência", b), []


# ── colacao ────────────────────────────────────────────────────────────────────────────────────────────────────────
def _words(x, y, lens, colour, sw=3.2, opacity=".55", gap=7):
    """A line of text as word shapes standing on a rule; returns (elements, end x)."""
    out = []
    for w in lens:
        out.append(S.line(x, y, x + w, y, stroke=colour, stroke_width=sw, stroke_linecap="round", opacity=opacity))
        x += w + gap
    return out, x - gap


def _colacao(p):
    s = _state(p)
    X0, X1 = 30, 408
    PRE = ((38, 24, 44), (26, 40, 40), (44, 30, 32), (30, 44, 32), (40, 22, 44), (34, 38, 34))
    SUF = ((28, 40, 30), (36, 24, 44), (30, 34, 22), (40, 26, 36), (24, 44, 28), (32, 30, 40))
    PHR = (30, 22, 38)
    ys = [196 + 52 * i for i in range(6)]
    top = 112
    b = []
    shifts = {1: (0, 44, -12, 26, -8, 58), 2: (0, 44, 0, 0, 0, 0), 3: (0, 44, 0, 0, 0, 0)}[s]
    A0 = X0 + 106 + 14 + 7                   # where the shared phrase starts when the readings agree
    A1 = A0 + sum(PHR) + 14

    def row(y, i, pre_shift, colour, phrase_col, sw=3.2, dissent=False):
        out = [S.line(X0, y + 8, X1, y + 8, stroke=S.GRID, stroke_width=1)]
        pre = list(PRE[i]); pre[0] = max(14, pre[0] + pre_shift)
        e, x = _words(X0, y, pre, S.INK2, 3.0)
        out += e
        if dissent:
            return out, x
        e, x = _words(x + 7, y, PHR, phrase_col, sw, "1" if phrase_col != S.INK2 else ".55")
        out += e
        e, x = _words(x + 7, y, SUF[i], S.INK2, 3.0)
        return out + e, x

    # the working book's own line, with the stretch under examination
    r, _ = row(top, 0, 0, S.INK, S.INK, 4.2)
    b += r + [S.line(X0, top + 28, X1 - 70, top + 28, stroke=S.GRID, stroke_width=1)]
    for i, y in enumerate(ys):
        pick = s == 1 and i == 0
        agree = s >= 2 and i != 1 and not (s == 3 and i == 5)
        col = S.DIF if pick else (S.INK if agree else S.INK2)
        sw = 4.2 if (pick or agree) else 3.2
        if s == 3 and i == 5:
            r, x = row(y, i, shifts[i], S.INK2, S.INK2, dissent=True)
            b += r
            # another hand: the same place written differently, off the axis
            e, x2 = _words(A0 + 22, y + 10, (26, 34, 18, 30), S.CONC, 4.6, "1")
            b += e
            continue
        r, _ = row(y, i, shifts[i], col, col, sw)
        b += r
    if s == 1:
        b += [S.line(A0 + 52, top + 10, A0 + 52, ys[0] - 10, stroke=S.DIF, stroke_width=1.6, stroke_dasharray="3 5"),
              _t(X1, 40, "parecer de um perito", 24, anchor="end"),
              _t(X1, 66, "o número ainda não decide", 19, fill=S.INK2, anchor="end")]
    if s >= 2:
        last = ys[4] + 20 if s == 3 else ys[5] + 20
        ax = [S.line(A0 - 6, top - 14, A0 - 6, last, stroke=S.INK2, stroke_width=1.2, stroke_dasharray="3 5"),
              S.line(A1 + 6, top - 14, A1 + 6, last, stroke=S.INK2, stroke_width=1.2, stroke_dasharray="3 5")]
        b += _fade(ax, s == 2)
    if s == 2:
        b += _fade([_t(X1, 40, "opinio communis", 24, anchor="end", font_style="italic"),
                    _t(X1, 66, "uma direção compartilhada", 19, fill=S.INK2, anchor="end")])
    if s == 3:
        y5 = ys[5]
        cut = [_p(f"M{A0 - 16} {y5 - 14} L{A0 + 8} {y5 - 26} M{A0 - 16} {y5} L{A0 + 8} {y5 - 12}", S.CONC, 2.4),
               _p(f"M{A0 + 112} {y5 + 9} C{X1 + 20} {y5 + 9} {X1 + 26} {top + 14} {A1 + 14} {top - 2}", S.CONC, 1.9),
               _head(A1 + 14, top - 2, "left", S.CONC, 1.9),
               _t(X1, 40, "concordância admite erro", 24, fill=S.CONC, anchor="end"),
               _t(X1, 66, "uma razão melhor a corrige", 19, fill=S.CONC, anchor="end")]
        b += _fade(cut)
    title = ["Um parecer de perito entre outros comentários sobre o mesmo trecho: o número ainda não decide",
             "A mesma leitura repetida em vários comentários forma uma direção compartilhada para o trecho",
             "Uma contra-leitura rompe a direção compartilhada e volta ao trecho: a concordância admite correção"][s - 1]
    return S.svg(436, 520, p.get("title") or title, b), []


# ── oficio ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def _oficio(p):
    s = _state(p)
    FX, FW, FY, FH = 150, 170, 28, 410
    X0, X1 = FX + 16, FX + FW - 16
    groups = ((58, 4), (138, 5), (230, 5), (322, 4))     # y of first rule, number of rules
    wid = (136, 128, 132, 112, 134, 124, 130, 118, 136, 100)
    b = [S.rect(FX + 5, FY + 6, FW, FH, fill=S.PAPER, stroke=S.GRID, stroke_width=1),
         S.rect(FX, FY, FW, FH, fill=S.PAPER, stroke=S.INK, stroke_width=1.6)]
    for g, (y, n) in enumerate(groups):
        b += [S.line(X0, y + 14 * k, X0 + wid[(g * 3 + k) % 10], y + 14 * k, stroke=S.INK2, stroke_width=1.4,
                     stroke_linecap="round", opacity=".7") for k in range(n)]
    L = FX - 14                              # right edge of the left margin
    R = FX + FW + 12                         # left edge of the right margin
    name = lambda x, y, w, col=S.INK, a=None: _t(x, y, w, 20, fill=col, font_style="italic", anchor=a)
    # 1 praemitto: the literal reading enters at the first line
    b += [_p(f"M{FX - 22} 58 H{X0 - 8}", S.INK, 1.8), _head(X0 - 6, 58, "right"), name(L - 22, 63, "praemitto", S.INK, "end")]
    if s >= 2:
        two = []
        # 2 scindo: the text is divided into its logical parts
        for (y, n) in groups:
            two.append(_p(f"M{X0 - 4} {y - 8} H{X0 - 10} V{y + 14 * (n - 1) + 8} H{X0 - 4}", S.INK, 1.6))
        two.append(name(L - 22, 148, "scindo", S.INK, "end"))
        # 3 summo: the parts are re-ordered into one construction
        mids = [y + 7 * (n - 1) for (y, n) in groups]
        two += [_p(f"M{FX - 10} {mids[0]} V{mids[3]}", S.INK2, 1.3)]
        two += [_p(f"M{X0 - 10} {m} H{FX - 10}", S.INK2, 1.3) for m in mids]
        two += [_dot(FX - 10, (mids[1] + mids[2]) / 2, S.INK, S.INK, 3.2), name(L - 22, 210, "summo", S.INK, "end")]
        # 4 casumque figuro: parallel cases at the foot of the text
        for k in range(3):
            two += _leaf(X0 + 6 + k * 44, 452 + (k % 2) * 4, 34, 44, S.INK, 1.2)
            two += _ruled(X0 + 12 + k * 44, 466 + (k % 2) * 4, (22, 18), 1, S.INK2, 1.1, ".7")
        two += [_p(f"M{X0 + 70} 448 V{groups[3][0] + 14 * 3 + 12}", S.INK2, 1.3),
                name(R + 4, 486, "casumque figuro", S.INK)]
        # 5 perlego: the whole text read through
        two += [_p(f"M{FX + FW + 6} 58 V{FY + FH - 24}", S.INK, 2.2), _head(FX + FW + 6, FY + FH - 22, "down"),
                name(R + 8, 244, "perlego", S.INK)]
        b += _fade(two, s == 2)
    if s >= 3:
        three = []
        # 6 do causas: four marks written beside the divided text (nature, features, origin, end)
        yc = groups[1][0] + 4
        three += [_p(f"M{FX + FW + 2} {yc + 8} H{R + 36}", S.DIF, 1.4),
                  *_hand(R + 38, yc, (66, 54, 62, 46), 13, S.DIF, 1.4), name(R + 92, yc - 12, "do causas", S.DIF, "end")]  # ends before the obiicio curve (measure CROSS, 13/11)
        # 7 connoto: observations added in the margin
        yn = groups[2][0] + 22
        three += [_p(f"M{X0 - 10} {yn + 10} H{FX - 24}", S.INK2, 1.3), *_hand(28, yn + 8, (86, 70, 80), 13, S.INK2, 1.4),
                  name(L - 22, yn - 6, "connoto", S.INK, "end")]
        # 8 et obiicio: another hand writes against the result and the answer returns to the first line
        yo = groups[3][0] - 2
        three += [*_hand(R + 38, yo + 12, (66, 50, 58), 13, S.CONC, 1.5), name(R + 38, yo, "et obiicio", S.CONC),
                  _p(f"M{R + 34} {yo + 24} C{R + 2} {yo + 24} {FX + FW - 2} {groups[2][0] + 26} {X1 + 2} {groups[2][0] + 26}", S.CONC, 1.7),
                  _p(f"M{R + 5} {yo + 15} L{R + 17} {yo + 33} M{R + 14} {yo + 11} L{R + 26} {yo + 29}", S.CONC, 1.5),
                  _p(f"M{R + 94} {yo - 18} C{R + 112} {yo - 120} {R + 112} {groups[0][0] + 100} {R + 104} 58 H{FX + FW - 2}", S.CONC, 1.7, stroke_dasharray="1 0"),
                  _head(X1 + 4, 58, "left", S.CONC, 1.7)]
        b += _fade(three)
    title = ["Praemitto: a primeira leitura literal introduz um texto que permanece o mesmo",
             "O texto é dividido, reordenado, acompanhado de casos paralelos e lido por inteiro",
             "Causas, observações e objeções escritas à margem; a objeção retorna ao texto lido"][s - 1]
    return S.svg(520, 540, p.get("title") or title, b), []


MODES = {"oficina": _oficina, "arvore": _arvore, "comparar": _comparar, "colacao": _colacao, "oficio": _oficio}


def build(p: dict) -> tuple[str, list[dict]]:
    mode = p.get("mode")
    if mode not in MODES:
        raise ValueError(f"topica_cia: mode must be one of {', '.join(MODES)}")
    return MODES[mode](p)
