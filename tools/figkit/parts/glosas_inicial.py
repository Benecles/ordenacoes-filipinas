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


def _limites(p):
    b = _sheet(18, 37, 183, 164)
    b += _sheet(285, 37, 141, 164)
    b += [_t(34, 64, "Petição inicial", 17, weight="600"),
          _t(302, 64, "Sentença", 17, weight="600"),
          _t(34, 94, "entrega da máquina", 14),
          _t(34, 137, "reembolso de aluguel", 14),
          _p("M34 108 H401", S.DIF, 2.4),
          _p("M34 151 H401", S.DIF, 2.4),
          S.circle(201, 108, 3, fill=S.DIF),
          S.circle(201, 151, 3, fill=S.DIF),
          _p("M274 88 h-9 v83 h9", S.CONC, 2.2),
          _t(264, 25, "limite do julgamento", 13, fill=S.CONC,
             anchor="middle"),
          _t(304, 185, "dispositivo", 13, fill=S.INK2),
          _t(263, 221, "arts. 141 e 492", 12, fill=S.CONC,
             anchor="middle", family=S.SANS)]
    # A detached line of proposed pleading remains outside this sheet. It
    # cannot silently become part of the judgment; no relief is granted here.
    b += [_t(34, 253, "novo pedido: dano", 15),
          _p("M34 264 H209 Q233 264 245 244 V231", S.INK2, 1.4),
          _p("M239 231 H251", S.CONC, 2),
          _t(316, 270, "fora desta demanda", 13, fill=S.INK2,
             anchor="middle")]
    return _svg(450, 300, p.get("title") or
                 "Os pedidos de entrega e reembolso delimitam o dispositivo; um novo pedido de dano fica fora desta demanda", b), []


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


def _estagios(p):
    """One fore-edge, four flags: stages belong to the same case file."""
    b = [_t(23, 25, "Conhecimento", 20, weight="600"),
         S.path("M23 49 H126 V327 H23 Z", fill=S.PAPER,
                stroke=S.INK, stroke_width=1.4),
         _p("M18 45 H131 V332 H18", S.INK2, .8)]
    for y in range(55, 326, 5):
        b.append(_p(f"M24 {y} H125", S.GRID, .8))
    stages = [(77, "postular", "inicial · defesa"),
              (147, "organizar", "questões · prova"),
              (217, "instruir", "produzir a prova"),
              (287, "decidir", "julgar o pedido")]
    for y, name, purpose in stages:
        b += [_p(f"M104 {y} H158 V{y - 8}", S.INK2, 1.2),
              S.circle(104, y, 2.5, fill=S.INK),
              _t(172, y - 3, name, 20, weight="600"),
              _t(172, y + 19, purpose, 14, fill=S.INK2)]
    b += [_t(23, 359, "a atividade predominante dá o nome", 14,
             fill=S.INK2)]
    return _svg(340, 380, p.get("title") or
                "Um só volume de autos: postular ouve as partes, organizar prepara as questões e a prova, instruir produz a prova, decidir julga o pedido; cada estágio recebe o nome de sua atividade predominante", b), []


def _causa(p):
    """Essential facts, juridical nexus and request on the same petition."""
    b = _sheet(31, 30, 267, 300)
    # A paper clip holds the argument to its concrete narrative.
    b += [_p("M50 45 V22 q0 -12 9 -12 q9 0 9 12 v43 q0 8 -6 8 q-6 0 -6 -8 V24", S.INK2, 1.1),
          _t(80, 61, "Causa de pedir", 21, weight="600"),
          _t(53, 105, "entrega para conserto", 17),
          _t(53, 132, "prazo vencido", 17),
          _t(53, 159, "sem devolução", 17),
          _p("M20 90 h-7 v76 h7 M13 128 H2", S.INK2, 1),
          _p("M280 91 V162 Q280 185 254 185 H54", S.INK2, 1.2),
          _t(53, 215, "dever de devolver", 17),
          _t(53, 239, "descumprido", 17),
          _p("M52 252 H273", S.GRID, .8),
          _t(53, 282, "entrega da máquina", 19, fill=S.DIF),
          _p("M53 293 H268", S.DIF, 1.8),
          _t(53, 316, "pedido", 13, fill=S.INK2),
          _t(31, 360, "nexo entre fato e efeito jurídico", 15, fill=S.INK2)]
    return _svg(340, 385, p.get("title") or
                "Na petição de Cecília, a entrega para conserto e o prazo vencido sem devolução sustentam a alegação de descumprimento do dever de devolver, da qual nasce o pedido de entrega da máquina", b), []


def _alcance(p):
    """The requested order reaches the requested object: two faces of relief."""
    from .abertura_civil import _machine
    b = [_t(27, 25, "Pede-se ao juízo", 17, fill=S.INK2)]
    edge = "M25 43 H308 V151"
    for i, x in enumerate(range(308, 24, -10)):
        edge += f" L{x} {151 if i % 2 else 156}"
    edge += " L25 151 Z"
    b += [S.path(edge, fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
          _p("M280 59 V37 q0 -9 7 -9 q7 0 7 9 v35 q0 7 -5 7 q-5 0 -5 -7 V39", S.INK2, 1),
          _t(46, 66, "Requer-se", 13, fill=S.INK2),
          _t(46, 96, "ordem de entrega", 23, weight="600"),
          _t(46, 126, "pedido imediato", 16, fill=S.INK2),
          _p("M240 137 q13 -6 23 -1 t27 -1", S.INK2, .8),
          _p("M166 157 V184", S.DIF, 1.8),
          _p("M161 176 l5 8 l5 -8", S.DIF, 1.8),
          _machine(76, 192, 1.05),
          _t(168, 353, "máquina", 23, fill=S.DIF, anchor="middle"),
          _t(168, 380, "bem da vida · pedido mediato", 16,
             fill=S.INK2, anchor="middle")]
    return _svg(340, 400, p.get("title") or
                "O pedido imediato de uma ordem de entrega serve para obter o pedido mediato, a máquina: a providência processual deve ser adequada à obtenção do bem da vida", b), []


def _despacho(p):
    """A precise order and its corrected entry, joined by the legal period."""
    # The order is an actual short document, with an unturned corner and a
    # handwritten signature; the lower folio is the same initial completed.
    b = _sheet(20, 28, 298, 122)
    b += [_t(38, 55, "Despacho", 19, weight="600"),
          _t(38, 87, "Indique o valor da causa,", 17),
          _t(38, 112, "considerando os pedidos cumulados.", 15),
          _p("M240 136 q13 -7 23 -1 t28 -2", S.INK2, .8),
          _p("M168 153 V182 M168 244 V265", S.DIF, 1.6),
          _p("M163 257 l5 8 l5 -8", S.DIF, 1.6),
          _t(168, 209, "15 dias úteis", 26, fill=S.DIF, anchor="middle"),
          _t(168, 232, "arts. 219 e 321", 12, fill=S.INK2,
             anchor="middle")]
    b += _sheet(34, 277, 270, 96)
    b += [_t(52, 305, "Petição inicial", 17, weight="600"),
          _t(52, 335, "Valor da causa:", 16),
          _t(52, 359, "soma dos pedidos", 18, fill=S.DIF),
          _p("M51 363 q104 -3 184 0", S.DIF, .9)]
    return _svg(340, 405, p.get("title") or
                "O despacho identifica a falta do valor da causa, abre quinze dias úteis e permite completar a mesma petição, mantendo os pedidos apresentados", b), []


def build(p: dict) -> tuple[str, list[dict]]:
    """Emit one named, static glossa; reject misspellings instead of guessing."""
    modes = {"reforma": _reforma, "origens": _origens, "limites": _limites,
             "tria": _tria, "simetria": _simetria, "medida": _medida,
             "estagios": _estagios, "causa": _causa,
             "alcance": _alcance, "despacho": _despacho}
    mode = p.get("mode")
    if mode not in modes:
        raise ValueError("glosas_inicial mode must be reforma, origens, limites, tria, simetria, medida, estagios, causa, alcance or despacho")
    return modes[mode](p)
