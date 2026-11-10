"""glosas_inicial: static marginal drawings for the opening of a civil cause.

Params:
  mode   reforma | origens | limites | tria | simetria | medida |
         estagios | causa | alcance | despacho (required)
  title  optional accessible description, replacing the mode's default

Canvases (width × height): reforma 520×390; origens 340×510;
limites 450×300; tria 300×240; simetria 300×250; medida 1080×660.
estagios 340×380; causa 340×385; alcance 340×400; despacho 340×405.
The medida receipt needs a full-width spread; it is not a 282px margin gloss.

These are reading notes, not selectors. The legal relations are carried by
books, string, loose pleadings and their binding. Paper has square corners;
the site's folded corner is reserved for backstage. There are no interactive
objects, invented dates, amounts, court outcomes or page numbers.

Legal provenance, recorded in the lesson's plan.md and notes.md:
  reforma: Marinoni, Novo curso v.2, pp.141–143; CPC/1973 arts.461-A,
    475-I; CPC/2015 art.318. Concentration began before the 2015 Code.
  origens: Barbosa Moreira, Temas, série4, pp.38–42, §§5–8 and notes12–14. The
    distinction concerns initiative/object versus facts/evidence; the Italian
    usage shown is specifically Liebman's. Marinoni v.2 p.141 supplies the
    separate Brazilian anchor, the Código Buzaid; no transmission from
    Liebman to Buzaid is asserted by the route between the places.
  limites: CPC arts.141 and492. Requested relief limits the judgment, without
    deciding whether either request will succeed.
  tria: CPC arts.337 §§1–4 and502. The branches state the prior case's condition;
    their consequences are explained in the adjacent prose.
  simetria: Mitidiero, Processo civil (2022), p.154, §5.2.1. Initial pleading
    and defense bear corresponding burdens of concrete argument.
  medida: CPC arts.292 II, V–VIII; 322; 324 §1; 327 §§1–3. Marinoni v.2
    pp.158–165; Didier v.1 pp.647–650. Open receipt entries represent a
    legally justified lack of quantification, never an invented amount.
  estagios: Marinoni v.2 pp.142–143, §1.3.1: the four stages name the
    predominant activity, not exclusive compartments.
  causa: Marinoni v.2 pp.153–154; CPC art.319 III. The fictional petition
    links its essential facts to a juridical consequence and to its request.
  alcance: Marinoni v.2 pp.155–158, §2.2.3: requested procedural relief
    serves the requested good. The machine is the running case's own object.
  despacho: CPC arts.219 and321; Didier v.1 pp.629–630: the precise order
    identifies a remediable omission and gives a chance to repair it.
"""
from __future__ import annotations

import re

from . import svg as S

def _svg(w, h, title, content):
    # Accessible naming without browser hover tooltips.
    return re.sub(r"<title\b[^>]*>.*?</title>", "", S.svg(w, h, title, content), flags=re.S)



def _t(x, y, s, size=14, fill=S.INK, family=S.SERIF, **kw):
    return S.text(x, y, s, size=size, family=family, fill=fill, **kw)


def _p(d, color=S.INK, width=1.5, **kw):
    return S.path(d, fill="none", stroke=color, stroke_width=width,
                  stroke_linecap="round", stroke_linejoin="round", **kw)


def _sheet(x, y, w, h, color=S.INK):
    return [S.rect(x + 3, y + 4, w, h, fill=S.PAPER, stroke=S.GRID,
                   stroke_width=1),
            S.rect(x, y, w, h, fill=S.PAPER, stroke=color,
                   stroke_width=1.4)]


def _writing(x, y, widths, gap=11):
    return [S.line(x, y + i * gap, x + w, y + i * gap,
                   stroke=S.GRID, stroke_width=1)
            for i, w in enumerate(widths)]


def _reforma(p):
    b = [_t(24, 23, "CPC de 1973", 16, family=S.SANS, weight="600")]
    # Three volumes rest on the same shelf. The narrow spine, page fore-edge,
    # and stitching make these books rather than three conceptual containers.
    for x, name in [(24, "conhecimento"), (190, "execução"), (356, "cautelar")]:
        b += [S.path(f"M{x} 48 Q{x + 7} 43 {x + 15} 48 H{x + 130} V171 H{x + 15} Q{x + 6} 166 {x} 172 Z",
                     fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
              _p(f"M{x + 15} 48 V171", S.INK2, 1),
              _p(f"M{x + 23} 54 H{x + 124} V164 H{x + 23}", S.GRID, 1),
              _p(f"M{x + 9} 72 h5 m-5 68 h5", S.INK2, 1),
              _t(x + 28, 102, name, 15),
              _t(x + 28, 125, "processo", 12, fill=S.INK2),
              _p(f"M{x + 130} 56 l5 -4 v111 l-5 8", S.INK2, 1)]
    b.append(_p("M19 180 H498", S.INK2, 1))
    # Three distinct process functions converge in the same case file. The
    # early junction is expressly situated under the previous Code.
    b += [_p("M91 174 C91 218 170 232 260 251", S.INK, 1.9),
          _p("M257 174 C257 208 254 228 260 251", S.DIF, 2.1),
          _p("M423 174 C423 218 350 232 260 251", S.INK, 1.9),
          S.circle(260, 251, 5, fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
          _t(24, 270, "reformas ainda no CPC de 1973", 13,
             fill=S.INK2),
          _p("M260 257 V286", S.INK, 2)]
    # A stitched file, edge-on below the cover; no folded corner.
    b += [S.path("M89 289 H196 L207 280 H432 V363 H89 Z",
                 fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
          _p("M89 358 H432 M94 363 V369 H438 V291 H432", S.INK2, 1),
          _p("M101 362 v5 m7 -5 v5 m7 -5 v5 m7 -5 v5 m7 -5 v5 m7 -5 v5", S.GRID, 1),
          _t(109, 309, "CPC de 2015", 12, fill=S.INK2, family=S.SANS),
          _t(109, 334, "procedimento comum", 21, weight="600"),
          _t(109, 353, "conhecer · efetivar · proteger", 13, fill=S.INK2)]
    return _svg(520, 390, p.get("title") or
                 "Os três processos do Código de 1973: reformas já concentram funções antes do procedimento comum de 2015", b), []


def _origens(p):
    # Three recognisable country outlines in a student's unscaled atlas.
    # The route orders the reading, not a claim of direct doctrinal descent.
    germany = "M36 28 l14 -5 l7 10 l15 -4 l7 10 l-6 10 l10 9 l-6 11 l4 12 l-11 7 l4 14 l-11 10 l-5 -7 l-13 2 l-4 -11 l-12 -6 l7 -11 l-3 -12 l6 -9 l-4 -11 Z"
    italy = "M243 177 l17 -4 l12 8 l-6 9 l-5 12 l8 13 l11 9 l2 12 l13 6 l6 11 l-7 5 l-10 -8 l-10 -1 l-4 12 l-8 4 l-5 -9 l5 -13 l-8 -13 l-9 -8 l-5 -15 l-9 -11 Z"
    brazil = "M38 337 l19 -9 l16 4 l7 -9 l13 8 l17 -1 l10 11 l19 6 l-4 14 l-10 9 l-5 19 l-13 8 l-8 16 l-13 10 l-8 18 l-8 -5 l1 -17 l-12 -8 l-3 -15 l-11 -7 l-3 -16 l-13 -13 l2 -14 Z"
    b = [S.path(germany, fill="none", stroke=S.INK2, stroke_width=1.3,
                stroke_linejoin="round"),
         _t(104, 31, "Alemanha", 19, weight="600"),
         _t(104, 59, "Dispositionsmaxime", 16, font_style="italic"),
         _t(104, 81, "iniciar · delimitar", 16),
         _t(104, 113, "Verhandlungsmaxime", 16, font_style="italic"),
         _t(104, 135, "fatos · prova", 16),
         _p("M64 124 C76 164 185 146 242 177", S.DIF, 1.7),
         _p("M234 169 l8 8 l-11 -1", S.DIF, 1.7),
         S.path(italy, fill="none", stroke=S.INK2, stroke_width=1.3,
                stroke_linejoin="round"),
         # Sicily and Sardinia identify the boot without political detail.
         _p("M265 273 l17 -3 l-4 9 Z M231 231 l3 13 l-5 7 l-3 -12 Z", S.INK2, 1),
         _t(15, 193, "Itália · Liebman", 19, weight="600"),
         _t(15, 223, "principio della", 17, font_style="italic"),
         _t(15, 246, "domanda", 17, font_style="italic"),
         _t(15, 275, "início · objeto", 17),
         _p("M249 286 C231 329 131 295 98 332", S.DIF, 1.7),
         _p("M108 328 l-10 4 l3 -11", S.DIF, 1.7),
         S.path(brazil, fill="none", stroke=S.INK2, stroke_width=1.3,
                stroke_linejoin="round"),
         _t(151, 344, "Brasil", 19, weight="600"),
         _t(151, 374, "Código Buzaid · 1973", 16),
         _t(151, 396, "processos separados", 16),
         _t(151, 425, "Barbosa Moreira", 17, weight="600"),
         _t(151, 449, "critica o rótulo único", 15.5),
         _p("M143 432 Q123 433 117 419", S.INK2, 1),
         _t(151, 474, "demanda ≠ fatos e prova", 15.5),
         _t(15, 504, "lugares e distinções · sem escala", 12, fill=S.INK2)]
    return _svg(340, 510, p.get("title") or
                 "Esboço geográfico: a Alemanha distingue iniciativa e objeto de fatos e prova; Liebman na Itália reúne início e objeto no principio della domanda; no Brasil, o Código Buzaid e a crítica de Barbosa Moreira ao rótulo genérico", b), []


def _tria(p):
    b = [_t(12, 29, "partes", 16),
         _t(12, 78, "causa", 16),
         _t(12, 127, "pedido", 16),
         _p("M77 26 C126 26 110 72 151 96", S.INK, 1.8),
         _p("M77 75 C114 75 126 89 151 106", S.INK, 1.8),
         _p("M77 124 C111 124 128 119 151 116", S.DIF, 2),
         # One knot, made by all three strands; their identity is joint.
         _p("M150 95 C177 72 181 107 151 117 C128 129 138 92 161 98 C184 103 163 132 151 113 C139 94 170 89 174 112", S.INK, 1.7),
         _p("M174 108 H185", S.INK2, 1.2),
         S.path("M186 84 L199 75 H286 V137 H199 L186 126 Z",
                fill=S.PAPER, stroke=S.INK, stroke_width=1.2),
         S.circle(195, 106, 2.5, fill="none", stroke=S.INK2,
                  stroke_width=1),
         _t(242, 101, "mesma", 16, anchor="middle"),
         _t(242, 122, "demanda", 16, anchor="middle"),
         _p("M162 126 V153 Q162 167 145 167 H73 V185 M162 153 Q162 167 179 167 H237 V185", S.INK2, 1.2),
         _t(73, 207, "em curso", 15, anchor="middle"),
         _t(237, 207, "mérito", 15, anchor="middle"),
         _t(237, 227, "+ trânsito", 14, fill=S.INK2, anchor="middle")]
    return _svg(300, 240, p.get("title") or
                 "Partes, causa e pedido identificam a mesma demanda; a demanda anterior pode estar em curso ou julgada com mérito e trânsito em julgado", b), []


def _simetria(p):
    b = [_t(150, 23, "alegar · responder", 16, anchor="middle"),
         # Shared binding over two loose pleadings. Each line on one sheet
         # meets an answering line on the other, through the open gutter.
         _p("M34 51 V43 H266 V51", S.INK2, 1.2)]
    b += _sheet(12, 61, 127, 145)
    b += _sheet(162, 61, 126, 145)
    b += [_t(25, 86, "Inicial", 17, weight="600"),
          _t(175, 86, "Defesa", 17, weight="600"),
          _t(25, 112, "fatos", 14, fill=S.INK2),
          _t(175, 112, "resposta", 14, fill=S.INK2)]
    for y, left_end, right_end in [(130, 116, 264), (154, 104, 251), (178, 121, 270)]:
        b += [_p(f"M26 {y} H{left_end}", S.INK, 1.5),
              _p(f"M{left_end} {y} C143 {y - 12} 152 {y + 12} 177 {y}", S.INK2, 1.2),
              _p(f"M177 {y} H{right_end}", S.INK, 1.5)]
    b += [_t(75, 234, "alegação", 14, anchor="middle"),
          _t(225, 234, "impugnação", 14, anchor="middle")]
    return _svg(300, 250, p.get("title") or
                 "As alegações concretas da inicial recebem respostas concretas na defesa: os ônus de argumentar se correspondem", b), []


def _medida(p):
    """One annotated value receipt: identify, join, then measure the requests.

    Wide only (1080×660). The torn receipt takes no invented amount. Two
    actual claim slips feed its sum; the alternative and subsidiary rows
    show different selection rules. Marginal hooks locate the admissibility
    tests and the lawful reasons for leaving the extent unspecified.
    """
    # One receipt, with perforations and a torn foot, is the shared object.
    edge = "M365 27 H797 V616"
    for x in range(797, 364, -12):
        edge += f" L{x} {616 if (797-x) % 24 else 622}"
    edge += " L365 616 Z"
    b = [S.path(edge, fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
         _t(394, 64, "Valor da causa", 25, weight="600"),
         _t(394, 90, "na data da propositura", 15, fill=S.INK2),
         _p("M393 106 H766", S.INK2, .8)]
    for y in range(48, 600, 22):
        b.append(S.circle(379, y, 1.4, fill=S.GRID))

    # A pencil ruler at the open entry measures scope, not physical money.
    b += [_t(18, 46, "O pedido identifica o bem", 19, weight="600"),
          _t(18, 73, "e dimensiona seu alcance.", 18),
          _t(18, 99, "certo · determinado · arts. 322 e 324", 13, fill=S.INK2),
          _p("M19 122 H317 M19 117 V127 M317 117 V127", S.INK2, .9)]
    for x in range(39, 317, 20):
        b.append(_p(f"M{x} 122 v{-8 if (x-39) % 40 == 0 else -4}", S.INK2, .8))
    b += [_p("M316 122 C341 122 339 142 365 142", S.INK2, 1),
          _t(18, 165, "A extensão pode ficar em aberto", 18),
          _t(18, 190, "quando faltam elementos:", 18),
          _t(18, 225, "ações universais: conjunto de bens", 16),
          _t(18, 248, "que ainda não se podem individuar;", 16),
          _t(18, 279, "consequências do ato ou fato", 17),
          _t(18, 302, "ainda indetermináveis;", 17),
          _t(18, 333, "objeto ou valor dependente", 17),
          _t(18, 356, "de ato a ser praticado pelo réu.", 17),
          _t(18, 382, "pedido genérico · art. 324, § 1º", 13, fill=S.INK2),
          _p("M338 199 h9 v159 h-9 M347 278 H365", S.INK2, 1)]

    # The receipt's three operations answer how the already defined claims
    # are valued. Blank rules stand for values; none is a case amount.
    b += [_t(395, 143, "Pedidos cumulados", 19, weight="600"),
          _p("M404 175 H515 M565 175 H718", S.INK, 1.4),
          _t(540, 182, "+", 25, fill=S.DIF, anchor="middle"),
          _p("M404 197 H718 M404 202 H718", S.DIF, 1.5),
          _t(404, 226, "soma de todos os valores", 18, fill=S.DIF),
          _t(752, 226, "VI", 13, fill=S.INK2, anchor="end"),
          _p("M393 246 H766", S.GRID, .8),
          _t(395, 278, "Pedidos alternativos", 19, weight="600"),
          _p("M404 308 H486 M532 308 H718", S.INK, 1.4),
          _p("M530 320 v7 H720 v-7", S.DIF, 1.5),
          _t(404, 354, "entra o de maior valor", 18, fill=S.DIF),
          _t(752, 354, "VII", 13, fill=S.INK2, anchor="end"),
          _p("M393 375 H766", S.GRID, .8),
          _t(395, 407, "Pedido subsidiário", 19, weight="600"),
          _t(404, 441, "principal", 17, fill=S.DIF),
          _p("M510 436 H718 M510 442 H718", S.DIF, 1.5),
          _t(404, 471, "reserva", 16, fill=S.INK2),
          _p("M510 466 H646", S.INK2, 1),
          _t(404, 506, "entra o valor do principal", 18, fill=S.DIF),
          _t(752, 506, "VIII", 13, fill=S.INK2, anchor="end"),
          _p("M393 527 H766", S.INK2, .8),
          _t(394, 560, "art. 292 · a relação muda a conta", 15, fill=S.INK2),
          _t(394, 591, "O valor acompanha o pedido apresentado.", 16)]

    # A marginal binder catches the receipt only when the claims can share
    # the file. No boxes: the three tests are written at its actual binding.
    b += [_p("M339 427 q-21 -15 -21 13 v120 q0 19 12 19 q12 0 12 -18 V440 q0 -12 -7 -12 q-7 0 -7 12 v105", S.INK2, 1.3),
          _t(18, 432, "Para caberem nos mesmos autos", 18, weight="600"),
          _t(18, 463, "pedidos compatíveis entre si;", 17),
          _t(18, 488, "mesmo juízo absolutamente", 17),
          _t(18, 511, "competente para todos;", 17),
          _t(18, 536, "mesmo procedimento adequado.", 17),
          _t(18, 564, "art. 327, § 1º", 13, fill=S.INK2),
          _t(18, 588, "A compatibilidade é dispensada", 16),
          _t(18, 611, "nas cumulações do art. 326", 16),
          _t(18, 634, "(art. 327, § 3º).", 14, fill=S.INK2)]

    # Right-hand calculations qualify the economic entry; short hooks
    # connect them to the receipt instead of forming separate note cards.
    b += [_p("M797 145 h24 M815 140 v10", S.INK2, 1),
          _t(839, 142, "Cada parcela tem sua regra", 18, weight="600"),
          _t(839, 175, "Negócio jurídico:", 17),
          _t(839, 200, "valor do ato ou da", 17),
          _t(839, 224, "parte controvertida.", 17),
          _t(839, 249, "art. 292, II", 13, fill=S.INK2),
          _t(839, 287, "Indenização, inclusive", 17),
          _t(839, 311, "por dano moral:", 17),
          _t(839, 335, "valor pretendido.", 17),
          _t(839, 360, "art. 292, V", 13, fill=S.INK2),
          _p("M797 449 h24 M815 444 v10", S.INK2, 1),
          _t(839, 445, "Procedimentos diferentes", 17, weight="600"),
          _t(839, 475, "o autor adota o comum;", 16),
          _t(839, 499, "técnicas especiais", 16),
          _t(839, 522, "compatíveis permanecem.", 16),
          _t(839, 548, "art. 327, § 2º", 13, fill=S.INK2),
          _t(839, 582, "Exige que o procedimento", 15.5),
          _t(839, 605, "especial aceite conversão.", 15.5)]
    return _svg(1080, 660, p.get("title") or
                 "Um recibo do valor da causa: o pedido precisa identificar o bem e medir o alcance, admitidas três hipóteses de generalidade; a cumulação exige compatibilidade, competência absoluta e procedimento adequado; o valor soma os pedidos, toma o maior alternativo ou apenas o principal subsidiário", b), []




# ── Stepped glosses ─────────────────────────────────────────────────────────
# A pinned gloss changes as the reader's text passes the reading line (chairman 10/11: "diagrams that scroll down
# ought to be animated and change as you scroll"). Each gloss is a list of layers; state k holds layers 0..k-1 and
# layer k-1 fades in. `stepped` emits one <svg class="panel"> per state, stacked by the page's CSS; curso.js turns
# the panel on when its .step[data-panel] text reaches the reading line. Without script the first state shows.

def _fd(items, d, animate):
    """One group of a raw layer, faded in after `d` seconds (staggered entry)."""
    return [f'<g class="fade" style="--d:{d}s">' + "".join(items) + "</g>"] if animate else list(items)


_FAMILY = {"estagios": "figure.autos", "limites": "figure.document", "causa": "figure.document",
           "alcance": "figure.instrument", "despacho": "figure.document"}


def _stepped(w, h, title, layers, pid, family):
    out = []
    n = len(layers)
    for k in range(1, n + 1):
        body = []
        for i, lay in enumerate(layers[:k]):
            cur = i == k - 1 and k > 1
            if isinstance(lay, tuple):
                items = lay[1](cur)
            elif cur:
                items = ['<g class="fade">' + "".join(lay) + "</g>"]
            else:
                items = lay
            body.append("".join(items))
        aria = (f' role="img" aria-label="{S.esc(title)}"' if k == n else ' aria-hidden="true"')
        out.append(f'<svg id="{pid}-{k}" data-family="{family}" class="panel{" on" if k == 1 else ""}" viewBox="0 0 {w} {h}"{aria}>'
                   + "".join(body) + "</svg>")
    return "".join(out)


def _flat(w, h, title, layers):
    items = []
    for lay in layers:
        items += lay[1](False) if isinstance(lay, tuple) else lay
    return _svg(w, h, title, items)


def _slip(x, y, w, h, label, size=15, color=S.INK):
    return [S.rect(x + 3, y + 4, w, h, fill=S.PAPER, stroke=S.GRID, stroke_width=1),
            S.rect(x, y, w, h, fill=S.PAPER, stroke=color, stroke_width=1.2),
            _t(x + w / 2, y + h / 2 + size * .33, label, size, anchor="middle")]


def _head(x, y, dx, dy, color=S.INK, width=1.6):
    """A small open arrowhead whose tip is (x, y) and which points along (dx, dy)."""
    import math
    n = math.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    def pt(a):
        c, s = math.cos(a), math.sin(a)
        return (x - 8 * (ux * c - uy * s), y - 8 * (ux * s + uy * c))
    (ax, ay), (bx, by) = pt(.5), pt(-.5)
    return _p(f"M{ax:.1f} {ay:.1f} L{x} {y} L{bx:.1f} {by:.1f}", color, width)


_ESTAGIOS = "Um só volume de autos: postular ouve as partes, organizar prepara as questões e a prova, instruir produz a prova, decidir julga o pedido; o volume corre sobre o trilho do procedimento comum, que desde 2015 é um só"


def _lay_estagios():
    book = [_t(23, 25, "Conhecimento", 20, weight="600"),
            _t(23, 47, "decidir o pedido", 12.5, fill=S.INK2, font_style="italic"),
            S.path("M23 90 H126 V367 H23 Z", fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
            _p("M18 86 H131 V371 H18", S.INK2, .8)]
    for y in range(96, 367, 5):
        book.append(_p(f"M24 {y} H125", S.GRID, .8))
    book += _slip(172, 8, 78, 30, "alegações") + _slip(262, 8, 62, 30, "provas")
    book += [_p("M211 38 C211 74 120 62 112 90", S.INK, 1.5),
             _p("M293 38 C293 84 140 70 121 90", S.INK, 1.5),
             S.circle(112, 90, 2.5, fill=S.INK), S.circle(121, 90, 2.5, fill=S.INK)]
    stages = [(118, "postular", "inicial · defesa"), (188, "organizar", "questões · prova"),
              (258, "instruir", "produzir a prova"), (328, "decidir", "julgar o pedido")]

    def flags(animate):
        out = []
        for i, (y, name, purpose) in enumerate(stages):
            out += _fd([_p(f"M104 {y} H158 V{y - 8}", S.INK2, 1.2), S.circle(104, y, 2.5, fill=S.INK),
                        _t(172, y - 3, name, 20, weight="600"), _t(172, y + 19, purpose, 14, fill=S.INK2)],
                       round(i * .22, 2), animate)
        return out
    organiza = [_p("M172 193 H262", S.INK, 1.3), _t(278, 171, "art. 357", 12.5, fill=S.INK2, family=S.SANS),
                _p("M266 178 H322", S.INK, 1.3), _p("M322 178 V328 H310 M322 258 H310", S.INK, 1.3),
                _head(308, 258, -1, 0, S.INK, 1.3), _head(308, 328, -1, 0, S.INK, 1.3)]
    rail = [_p("M8 382 H332", S.INK, 1.9, class_="grow"), _p("M8 390 H332", S.INK, 1.9, class_="grow")]
    rail += [_p(f"M{x} 379 V393", S.INK2, 1) for x in range(14, 332, 12)]
    rail += [_t(23, 421, "procedimento comum", 20, weight="600"), _t(332, 421, "art. 318", 12.5, fill=S.INK2, family=S.SANS, anchor="end"),
             _t(23, 443, "toda causa sem rito próprio;", 14, fill=S.INK2),
             _t(23, 462, "subsidiário nos especiais e na execução", 14, fill=S.INK2)]
    ghost = [_p("M8 494 H150 M8 501 H150 M190 494 H332 M190 501 H332", S.INK2, 1.3, stroke_dasharray="5 4"),
             _t(79, 523, "ordinário", 16, anchor="middle", font_style="italic", fill=S.INK2),
             _t(261, 523, "sumário", 16, anchor="middle", font_style="italic", fill=S.INK2),
             _t(23, 548, "CPC de 1973 · arts. 271 e 272 · hoje um só", 13, fill=S.INK2)]
    return 340, 560, _ESTAGIOS, [book, ("raw", flags), organiza, rail, ghost]


_LIMITES = "Os pedidos de entrega e reembolso delimitam o dispositivo; um novo pedido de dano fica fora desta demanda"


def _lay_limites():
    base = _sheet(18, 37, 183, 164) + _sheet(285, 37, 141, 164)
    base += [_t(34, 64, "Petição inicial", 17, weight="600"), _t(302, 64, "Sentença", 17, weight="600"),
             _t(34, 94, "entrega da máquina", 14), _t(34, 137, "reembolso de aluguel", 14),
             _p("M34 108 H401", S.DIF, 2.4), _p("M34 151 H401", S.DIF, 2.4),
             S.circle(201, 108, 3, fill=S.DIF), S.circle(201, 151, 3, fill=S.DIF)]
    limit = [_p("M274 88 h-9 v83 h9", S.CONC, 2.2),
             _t(264, 25, "limite do julgamento", 13, fill=S.CONC, anchor="middle"),
             _t(264, 221, "art. 141", 12, fill=S.CONC, anchor="middle", family=S.SANS)]
    disp = [_t(304, 185, "dispositivo", 13, fill=S.INK2), _t(355, 221, "art. 492", 12, fill=S.CONC, anchor="middle", family=S.SANS)]
    for cx, kind, word, gloss in [(308, "ultra", "ultra", "além"), (355, "extra", "extra", "fora"), (402, "citra", "citra", "aquém")]:
        tick = _p(f"M{cx + 8} 232 v16", S.CONC, 1.6)
        if kind == "ultra":
            line = _p(f"M{cx - 16} 240 H{cx + 20}", S.INK, 1.8)
        elif kind == "citra":
            line = _p(f"M{cx - 16} 240 H{cx - 1}", S.INK, 1.8)
        else:
            line = _p(f"M{cx + 12} 246 H{cx + 24}", S.INK, 1.8)
        disp += [tick, line, _t(cx, 266, word, 13, anchor="middle", font_style="italic"),
                 _t(cx, 281, gloss, 12, fill=S.INK2, anchor="middle", family=S.SANS)]
    fora = [_t(34, 253, "novo pedido: dano", 15), _p("M34 264 H209 Q233 264 245 244 V231", S.INK2, 1.4),
            _p("M239 231 H251", S.CONC, 2), _t(34, 287, "fora desta demanda", 13, fill=S.INK2)]
    return 450, 300, _LIMITES, [base, limit, disp, fora]


_CAUSA = "Na petição de Cecília, a entrega para conserto e o prazo vencido sem devolução sustentam a alegação de descumprimento do dever de devolver, da qual nasce o pedido de entrega da máquina; o juiz pode reenquadrar juridicamente os fatos, mantidos fato e pedido"


def _lay_causa():
    base = _sheet(12, 30, 208, 300)
    base += [_p("M31 45 V22 q0 -12 9 -12 q9 0 9 12 v43 q0 8 -6 8 q-6 0 -6 -8 V24", S.INK2, 1.1),
             _t(58, 61, "Causa de pedir", 21, weight="600"),
             _t(32, 105, "entrega para conserto", 17), _t(32, 132, "prazo vencido", 17), _t(32, 159, "sem devolução", 17),
             _p("M25 90 h-7 v76 h7 M18 128 H8", S.INK2, 1)]
    fund = [_p("M204 91 V162 Q204 185 180 185 H33", S.INK2, 1.2),
            _t(32, 215, "dever de devolver", 17), _t(32, 239, "descumprido", 17),
            _t(32, 259, "fundamento jurídico", 12.5, fill=S.INK2, family=S.SANS)]
    art = [S.path("M138 224 H214 V248 H138 L130 236 Z", fill=S.PAPER, stroke=S.INK, stroke_width=1.2),
           _t(176, 240, "art. 319, III", 12, anchor="middle", family=S.SANS),
           _p("M130 236 H122", S.INK2, 1, stroke_dasharray="3 3")]
    reenq = [S.path("M232 196 H334 V244 H232 Z", fill="none", stroke=S.INK, stroke_width=1.2, stroke_dasharray="5 4"),
             _t(283, 216, "outro", 14, anchor="middle"), _t(283, 234, "enquadramento", 12.5, anchor="middle"),
             _p("M172 212 H228", S.INK, 1.4), _head(228, 212, 1, 0, S.INK, 1.4), _head(176, 212, -1, 0, S.INK, 1.4),
             _t(232, 262, "ouvidas as partes", 12, fill=S.INK2, family=S.SANS), _t(232, 278, "art. 10", 12, fill=S.INK2, family=S.SANS),
             _p("M32 272 H202", S.GRID, .8),
             _t(32, 299, "entrega da máquina", 19, fill=S.DIF), _p("M32 309 H202", S.DIF, 1.8), _t(32, 322, "pedido", 12.5, fill=S.INK2),
             S.circle(6, 128, 3, fill=S.DIF), S.circle(22, 295, 3, fill=S.DIF)]
    return 340, 385, _CAUSA, [base + fund, art, reenq]


_ALCANCE = "O pedido imediato, a ordem de entrega e a condenação ao reembolso, serve para obter o pedido mediato, a máquina e o dinheiro do aluguel: a providência processual deve ser adequada à obtenção do bem da vida"


def _lay_alcance():
    from .abertura_civil import _machine, _money
    goods = [_machine(18, 193, .64), *_money(190, 205, 112, 62),
             _p("M10 279 H330", S.INK2, 1.2),
             _t(74, 304, "máquina", 18, anchor="middle"), _t(252, 304, "aluguel", 18, anchor="middle")]
    slips = []
    for x in (14, 186):
        slips += [S.rect(x + 3, 50, 140, 62, fill=S.PAPER, stroke=S.GRID, stroke_width=1),
                  S.rect(x, 46, 140, 62, fill=S.PAPER, stroke=S.INK, stroke_width=1.2),
                  _t(x + 70, 66, "pedido", 12.5, fill=S.INK2, anchor="middle", family=S.SANS)]
    slips += [_p("M74 112 V182", S.DIF, 1.8), _head(74, 182, 0, 1, S.DIF, 1.8),
              _p("M252 112 V190", S.DIF, 1.8), _head(252, 190, 0, 1, S.DIF, 1.8)]
    imed = [_t(84, 88, "ordem de entrega", 15, anchor="middle"),
            _t(256, 84, "condenação ao", 14.5, anchor="middle"), _t(256, 100, "reembolso", 14.5, anchor="middle"),
            _p("M14 30 H326 M14 30 V37 M326 30 V37", S.INK2, 1),
            _t(170, 22, "pedido imediato · o que se pede ao juiz", 14, fill=S.INK2, anchor="middle")]
    med = [_p("M24 318 V326 H316 V318", S.INK2, 1.2), _p("M170 326 V336", S.INK2, 1.2),
           _t(170, 359, "bem da vida · pedido mediato", 17, fill=S.DIF, anchor="middle")]
    ido = [_t(86, 152, "idôneo", 13.5, font_style="italic", fill=S.INK2), _t(264, 152, "idôneo", 13.5, font_style="italic", fill=S.INK2),
           _t(170, 386, "com a menor restrição possível ao réu", 14, fill=S.INK2, anchor="middle")]
    return 340, 400, _ALCANCE, [goods, slips, imed, med, ido]


_DESPACHO = "O despacho identifica a falta do valor da causa, abre quinze dias úteis e permite completar a mesma petição, mantendo os pedidos apresentados"


def _lay_despacho():
    folio = _sheet(14, 22, 282, 118)
    folio += [_t(32, 50, "Petição inicial", 17, weight="600")] + _writing(32, 66, [210, 150], 12)
    folio += [_t(32, 114, "Valor da causa:", 16), _p("M146 117 H276", S.INK2, 1, stroke_dasharray="2 5")]
    gap = [_p("M138 128 l8 -11 l8 11", S.INK, 1.5)]
    desp = _sheet(30, 210, 282, 104)
    desp += [_t(48, 238, "Despacho", 17, weight="600"), _t(48, 264, "Indique o valor da causa,", 16),
             _t(48, 286, "considerando os pedidos cumulados.", 14.5),
             _p("M230 302 q13 -7 23 -1 t28 -2", S.INK2, .8),
             _p("M212 130 V204", S.DIF, 1.8), _head(212, 204, 0, 1, S.DIF, 1.8)]
    vague = [S.path("M30 336 H170 V376 H30 Z", fill="none", stroke=S.INK2, stroke_width=1.1, stroke_dasharray="5 4"),
             _t(100, 360, "Regularize a inicial.", 14, anchor="middle", fill=S.INK2),
             _p("M36 372 L164 340", S.CONC, 1.8),
             _t(184, 360, "não aponta o defeito", 12.5, fill=S.INK2, family=S.SANS)]
    done = [_t(148, 113, "soma dos pedidos", 16, fill=S.DIF), _p("M146 119 q60 -3 130 0", S.DIF, 1),
            _p("M312 266 H326 V80 H300", S.DIF, 1.8), _head(300, 80, -1, 0, S.DIF, 1.8)]
    prazo = [_t(28, 180, "15 dias úteis", 24, fill=S.DIF), _t(28, 197, "arts. 219 e 321", 12, fill=S.INK2),
             _t(240, 172, "10 dias", 14, fill=S.INK2, font_style="italic"), _p("M236 167 H286", S.CONC, 1.6),
             _t(240, 188, "CPC de 1973", 12, fill=S.INK2, family=S.SANS)]
    return 340, 420, _DESPACHO, [folio, gap, desp, vague, done, prazo]


_STEPPED = {"estagios": _lay_estagios, "limites": _lay_limites, "causa": _lay_causa,
            "alcance": _lay_alcance, "despacho": _lay_despacho}


def build(p: dict) -> tuple[str, list[dict]]:
    """Emit one named glossa; reject misspellings instead of guessing.

    `stepped` (a panel id prefix) casts the stepped modes as stacked panels for the page's scrollytelling; without
    it every mode is a single static drawing (the final state)."""
    modes = {"reforma": _reforma, "origens": _origens, "tria": _tria, "simetria": _simetria, "medida": _medida}
    mode = p.get("mode")
    if mode in _STEPPED:
        w, h, title, layers = _STEPPED[mode]()
        title = p.get("title") or title
        return (_stepped(w, h, title, layers, p["stepped"], _FAMILY[mode]) if p.get("stepped") else _flat(w, h, title, layers)), []
    if mode not in modes:
        raise ValueError("glosas_inicial mode must be reforma, origens, limites, tria, simetria, medida, estagios, causa, alcance or despacho")
    return modes[mode](p)
