"""glosas_inicial: static marginal drawings for the opening of a civil cause.

Params:
  mode   reforma | origens | limites | tria | simetria (required)
  title  optional accessible description, replacing the mode's default

Canvases (width × height): reforma 520×390; origens 340×380;
limites 450×300; tria 300×240; simetria 300×250.

These are reading notes, not selectors. The legal relations are carried by
books, string, loose pleadings and their binding. Paper has square corners;
the site's folded corner is reserved for backstage. There are no interactive
objects, invented dates, amounts, court outcomes or page numbers.

Legal provenance, recorded in the lesson's plan.md and notes.md:
  reforma: Marinoni, Novo curso v.2, pp.141–143; CPC/1973 arts.461-A,
    475-I; CPC/2015 art.318. Concentration began before the 2015 Code.
  origens: Barbosa Moreira, Temas, série4, §§5–6 and notes12–14. The
    distinction concerns initiative/object versus facts/evidence; the Italian
    usage shown is specifically Liebman's.
  limites: CPC arts.141 and492. Requested relief limits the judgment, without
    deciding whether either request will succeed.
  tria: CPC art.337 §§1–4. The branches state the prior case's condition;
    their consequences are explained in the adjacent prose.
  simetria: Mitidiero, Processo civil (2022), p.154, §5.2.1. Initial pleading
    and defense bear corresponding burdens of concrete argument.
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
          _t(260, 210, "reformas ainda no CPC de 1973", 13,
             fill=S.INK2, anchor="middle"),
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
    # A bibliographic branch in a reader's margin: two German terms keep
    # distinct forks; Liebman's usage joins the first pair, not both pairs.
    b = [_t(24, 26, "Tradição alemã", 17, weight="600"),
         _p("M25 38 V209 M25 68 Q25 76 42 76 M25 155 Q25 163 42 163", S.INK2, 1.3),
         _t(49, 80, "Dispositionsmaxime", 18, font_style="italic"),
         _p("M51 92 V106 H279 V92 M165 106 V117", S.INK2, 1),
         _t(65, 134, "abertura", 16),
         _t(210, 134, "objeto", 16),
         _t(49, 167, "Verhandlungsmaxime", 18, font_style="italic"),
         _p("M51 179 V193 H279 V179 M165 193 V204", S.INK2, 1),
         _t(65, 221, "fatos", 16),
         _t(210, 221, "prova", 16),
         _t(24, 267, "Liebman · uso italiano", 17, weight="600"),
         _p("M25 279 V299 Q25 306 42 306", S.INK2, 1.3),
         _t(49, 310, "principio della domanda", 17, font_style="italic"),
         _p("M51 323 V336 H279 V323 M165 336 V347", S.INK2, 1),
         _t(65, 364, "abertura", 16),
         _t(210, 364, "objeto", 16)]
    return _svg(340, 380, p.get("title") or
                 "Dois termos alemães separam abertura e objeto de fatos e prova; o principio della domanda de Liebman reúne abertura e objeto", b), []


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


def build(p: dict) -> tuple[str, list[dict]]:
    """Emit one named, static glossa; reject misspellings instead of guessing."""
    modes = {"reforma": _reforma, "origens": _origens, "limites": _limites,
             "tria": _tria, "simetria": _simetria}
    mode = p.get("mode")
    if mode not in modes:
        raise ValueError("glosas_inicial mode must be reforma, origens, limites, tria or simetria")
    return modes[mode](p)
