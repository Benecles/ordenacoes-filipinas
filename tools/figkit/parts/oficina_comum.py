"""oficina_comum: books, folios and instruments for the schools of ius commune.

Params (facts and reading mode, never drawing coordinates):
  mode   hero | fontes | folios | recepcao | universidade | dominio |
         estatutos | argumento | autoridade | crise | desfecho (required)
  title  optional accessible description in place of the mode's default
  state  optional 1-based reading state for recepcao (1–3), fontes (1–3),
         universidade (1–4), estatutos (1–3), dominio (1–3),
         argumento (1–3), autoridade (1–3), crise (1–3).
         Put each result in its own .panel inside the house .scrolly figure;
         .step[data-panel] paragraphs choose the corresponding panel. The
         omission of state retains the original complete static drawing.

Canvases (width x height): hero 1100x440; fontes 320x290;
folios 1100x440; recepcao 320x330; universidade 320x330;
dominio 320x320; estatutos 320x330; argumento 520x440;
autoridade 320x290; crise 320x330; desfecho 1100x400.
The new marginal drawings use type of at least 17 units.

Each result is one static state, build(p) -> (svg, []). The house course script
changes whole panels on scroll; no selectors or animation scripts are emitted.
Folios are didactic reconstructions,
not facsimiles or historical glosses attributed to a named jurist. Their lines
are symbolic writing, never quotations. Folios reconstruct the page-and-margin
relation of Hespanha's plates (fig.7, p.451; fig.9, p.458) on two schematic
Corpus iuris leaves; no actual Roman passage is followed through the schools.
Only argumento uses the presentation of a document by the person concerned or
a procurator (p.469). Other provenance: recepcao pp.441-453; universidade
pp.456-457,459; glossa pp.459-460; dominio p.465; estatutos pp.461,465;
arguments pp.468-477; crise pp.479-482; later schools pp.481-488.
The page's plan.md and notes.md carry the full claim log and reconstruction
notice.

The physical positions carry relations: sources enter an annotated book;
the local statute stays beside the received law; marginal glosses surround a
text while commentary joins sources; argument supports an extension; authority
can meet contrary reasons; historical meaning and practical reception branch
from the same inherited material. No folded corners, selectors, tooltips,
invented dates, quotation fragments or amounts. All colours are house tokens.
"""
from __future__ import annotations

from . import svg as S


def _t(x, y, words, size=18, fill=S.INK, family=S.SERIF, **kw):
    return S.text(x, y, words, size=size, fill=fill, family=family, **kw)


def _p(d, stroke=S.INK, width=1.5, **kw):
    return S.path(d, fill="none", stroke=stroke, stroke_width=width,
                  stroke_linecap="round", stroke_linejoin="round", **kw)


def _g(body, **attrs):
    return f'<g {S.attrs(**attrs)}>{"".join(body)}</g>'


def _f(items, on=True):
    """Elements new in this reading state fade in; the house script keeps the previous state beneath them."""
    return [_g(items, class_="fade")] if on else list(items)


def _writing(x, y, widths, gap=11, color=S.GRID):
    return [S.line(x, y + i * gap, x + width, y + i * gap,
                   stroke=color, stroke_width=1) for i, width in enumerate(widths)]


def _arrow(d, x, y, color=S.INK, width=1.8, direction="right"):
    ends = {
        "right": f"M{x - 7} {y - 4} L{x} {y} L{x - 7} {y + 4}",
        "left": f"M{x + 7} {y - 4} L{x} {y} L{x + 7} {y + 4}",
        "down": f"M{x - 4} {y - 7} L{x} {y} L{x + 4} {y - 7}",
        "up": f"M{x - 4} {y + 7} L{x} {y} L{x + 4} {y + 7}",
    }
    return [_p(d, color, width),
            _p(ends[direction], color, width)]


def _folio(x, y, w, h, color=S.INK):
    # The two underleaves and their fibres give a flat sheet a physical edge.
    return [S.rect(x + 4, y + 5, w, h, fill=S.PAPER, stroke=S.GRID,
                   stroke_width=1),
            S.rect(x + 2, y + 2, w, h, fill=S.PAPER, stroke=S.INK2,
                   stroke_width=.8),
            S.rect(x, y, w, h, fill=S.PAPER, stroke=color,
                   stroke_width=1.5)]


def _closed_book(x, y, w, h, title, size=18, color=S.INK):
    body = [S.path(f"M{x} {y + 4} Q{x + 8} {y - 2} {x + 16} {y + 4} H{x + w} V{y + h} H{x + 16} Q{x + 7} {y + h - 5} {x} {y + h + 1} Z",
                   fill=S.PAPER, stroke=color, stroke_width=1.6),
            _p(f"M{x + 16} {y + 5} V{y + h - 1}", S.INK2, 1),
            _p(f"M{x + 23} {y + 10} H{x + w - 6} V{y + h - 7} H{x + 22}", S.GRID, 1),
            _p(f"M{x + w} {y + 8} l5 -4 V{y + h - 4} l-5 5", S.INK2, 1),
            _p(f"M{x + 5} {y + 19} h6 m-6 {h - 36} h6", S.INK2, 1),
            _t(x + 29, y + h / 2 + 6, title, size)]
    return body


def _open_book(x, y, w, h):
    m, edge = x + w / 2, 16
    body = [S.path(f"M{x - 5} {y + 5} Q{m - 75} {y - 14} {m} {y + 9} Q{m + 72} {y - 14} {x + w + 5} {y + 5} V{y + h + 5} Q{m + 70} {y + h - 14} {m} {y + h + 10} Q{m - 70} {y + h - 14} {x - 5} {y + h + 5} Z",
                   fill=S.PAPER, stroke=S.INK, stroke_width=1.8),
            S.path(f"M{x} {y} Q{m - 74} {y - 18} {m} {y + 7} Q{m + 74} {y - 18} {x + w} {y} V{y + h} Q{m + 74} {y + h - 18} {m} {y + h + 7} Q{m - 74} {y + h - 18} {x} {y + h} Z",
                   fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
            _p(f"M{m} {y + 8} V{y + h + 6}", S.INK2, 1.2),
            _p(f"M{m - 6} {y + 12} Q{m - 10} {y + h / 2} {m - 6} {y + h - 1}", S.GRID, .9),
            _p(f"M{m + 6} {y + 12} Q{m + 10} {y + h / 2} {m + 6} {y + h - 1}", S.GRID, .9)]
    for offset in (4, 8):
        body.append(_p(f"M{x + offset} {y + h + offset} Q{m - 70} {y + h - 13 + offset} {m} {y + h + 9 + offset} Q{m + 70} {y + h - 13 + offset} {x + w - offset} {y + h + offset}", S.INK2, .7))
    return body


def _hero(p):
    b = [_t(230, 26, "Bolonha · XII–XIII", 18, family=S.SANS),
         _t(556, 26, "cidades italianas · XIV–XV", 18, family=S.SANS),
         _t(888, 26, "século XVI", 18, family=S.SANS)]
    # Three objects have different juridical destinations. Roman law enters
    # the text; canon law bounds the ensemble; the statute enters commentary.
    b += _closed_book(15, 91, 139, 60, "romano", 21)
    b += _closed_book(15, 227, 139, 60, "canônico", 21)
    b += _folio(17, 345, 151, 52)
    b += [_t(29, 369, "estatuto local", 18),
          *_writing(30, 380, [115, 103], 8),
          _t(18, 423, "direito próprio", 16, fill=S.INK2)]
    # The book is a real surface of work: a nucleus of inherited text with a
    # dense analytical margin, followed by a wider writing space for relations.
    b += _open_book(221, 95, 623, 277)
    b += [_t(239, 77, "Irnério → Acúrsio", 19),
          _t(555, 77, "Cino · Bártolo · Baldo", 19),
          _p("M298 121 V335 M456 121 V335", S.GRID, .8),
          _t(311, 146, "texto", 19),
          _t(311, 172, "justinianeu", 21),
          *_writing(309, 191, [132, 119, 136, 125, 132, 113, 138, 126], 11),
          _t(237, 130, "verba", 16, fill=S.INK2),
          _t(237, 150, "tenere", 16, fill=S.INK2),
          *_writing(237, 167, [47, 50], 8),
          _t(237, 219, "glosa", 18),
          *_writing(237, 234, [46, 49, 42], 8),
          _t(236, 299, "regras", 16, fill=S.INK2),
          *_writing(237, 314, [48, 43], 8),
          _t(468, 145, "sensum", 16, fill=S.INK2),
          _t(468, 165, "eligere", 16, fill=S.INK2),
          *_writing(469, 181, [46, 42], 8),
          _t(467, 242, "lugares", 16),
          _t(467, 262, "paralelos", 16),
          *_writing(469, 282, [44, 47, 39], 8),
          _p("M286 202 C300 201 290 169 307 164 M461 250 C447 250 461 226 443 226 M285 295 C297 295 291 270 307 270", S.INK2, 1),
          _t(325, 345, "Magna Glosa", 20),
          _p("M310 330 Q369 322 446 330", S.GRID, 1)]
    b += _arrow("M160 120 C191 120 183 159 309 159", 309, 159, S.INK)
    # A bounding line, rather than a second textual nucleus: the canonical
    # source limits how the whole body of material can be used.
    b += [_p("M160 255 H190 V54 H835 V344", S.CONC, 1.6),
          _p("M829 344 H841", S.CONC, 1.6),
          _t(394, 48, "limite canônico", 16, fill=S.CONC)]
    # A Roman passage carries forward into a practical, composite elaboration.
    b += [_t(562, 132, "comentário", 24),
          _t(562, 171, "texto recebido", 17),
          *_writing(562, 187, [232, 221], 10),
          _p("M443 207 C496 207 505 207 555 207", S.INK2, 1.3),
          _t(661, 232, "ius proprium", 18),
          _p("M650 218 V244 M646 218 H653 M646 244 H653", S.INK2, 1.1),
          *_writing(562, 251, [226, 211], 10),
          _t(562, 291, "concordar · distinguir", 18),
          _p("M563 302 Q654 313 792 302", S.GRID, 1),
          _t(652, 340, "consilia", 25, anchor="middle")]
    b += _arrow("M173 370 C206 370 195 401 520 401 C803 401 807 381 807 232 H790", 790, 232, S.INK, direction="left")
    # Subsequent uses share an inherited material; these branches are not a
    # single ladder in which one school simply erases its predecessor.
    b += [_p("M849 228 H865 M865 228 C879 228 872 141 886 141 M865 228 C879 228 872 294 886 294", S.INK, 1.7)]
    b += _arrow("M886 141 H1080", 1080, 141)
    b += _arrow("M886 294 H1080", 1080, 294)
    b += [_t(889, 103, "mos gallicus", 21),
          _t(889, 128, "sentido histórico", 17),
          _t(889, 256, "usus modernus", 21),
          _t(889, 281, "vigência prática", 17),
          _t(889, 322, "recepção das normas", 16, fill=S.INK2),
          _t(548, 433, "fontes · métodos · língua compartilhados", 17,
             fill=S.INK2, anchor="middle")]
    return S.svg(1100, 440, p.get("title") or
                 "De Bolonha às cidades italianas e ao século XVI: o texto romano glosado, a composição das fontes no comentário e duas investigações posteriores", b), []


def _fontes(p):
    b = [_t(15, 24, "Corpus iuris", 20)]
    # The four book spines are distinct; titles run along the binding.
    titles = ["Institutiones", "Digesto", "Código", "Novelas"]
    for i, title in enumerate(titles):
        x, y, w, h = 15 + i * 45, 43 + (3 if i % 2 else 0), 37, 137
        b += [S.path(f"M{x} {y} Q{x + 5} {y - 3} {x + 10} {y} H{x + w} V{y + h} H{x + 9} Q{x + 4} {y + h - 3} {x} {y + h} Z",
                     fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
              _p(f"M{x + 7} {y + 1} V{y + h - 1}", S.INK2, .8),
              _p(f"M{x + 4} {y + 15} H{x + w - 4} M{x + 4} {y + h - 15} H{x + w - 4}", S.GRID, 1),
              _t(0, 0, title, 16, anchor="middle",
                 transform=f"translate({x + 23} {y + h / 2}) rotate(-90)")]
    b += _folio(230, 57, 72, 148)
    b += [_t(240, 85, "direito", 16), _t(240, 107, "próprio", 16),
          *_writing(241, 124, [43, 36, 45, 41, 34], 11),
          _t(16, 211, "romano supre lacunas", 17)]
    b += [_p("M25 225 H262 V210", S.INK, 1.8),
          _p("M258 217 L262 210 L266 217", S.INK, 1.8)]
    # Canonical limits cross the route of supplementation without deleting it.
    b += [_p("M200 215 V239 M208 215 V239", S.CONC, 2),
          _p("M204 240 V253 H184", S.CONC, 1.2),
          _t(16, 269, "o cânone limita", 17, fill=S.CONC),
          _t(230, 253, "permanece", 16, fill=S.INK2)]
    return S.svg(320, 290, p.get("title") or
                 "Os quatro livros do Corpus e o direito próprio: o romano supre lacunas sob limites canônicos", b), []


def _folios(p):
    b = [_t(27, 28, "Irnério · leitura do texto", 22),
         _t(587, 28, "Acúrsio · reunião da glosa", 22)]
    b += _arrow("M327 21 H563", 563, 21, S.INK2, 1.3)
    b += _folio(24, 52, 494, 365)
    b += _folio(584, 52, 494, 365)
    # Both objects carry only received Roman text. Marginal and interlinear
    # marks point into that nucleus; they are not words of an invented gloss.
    for offset in (0, 560):
        b += [_p(f"M{152 + offset} 86 V351 M{354 + offset} 86 V351", S.GRID, .8),
              _t(171 + offset, 108, "Corpus iuris", 22),
              _t(171 + offset, 137, "Digesto", 24),
              *_writing(170 + offset, 161, [164, 150, 169, 160,
                                                   157, 171, 151, 167,
                                                   162, 149, 173, 158], 15),
              _p(f"M{185 + offset} 182 q8 -5 16 0 q7 4 13 -1 m17 1 q8 -5 17 0 m-56 45 q8 -5 15 0 q9 4 16 -1 m16 1 q8 -4 17 0", S.INK2, .9),
              _p(f"M{172 + offset} 202 q61 4 141 0 M{186 + offset} 277 q56 4 123 0", S.INK2, .8)]
    b += [_t(44, 105, "verba", 18, fill=S.INK2),
          _t(44, 128, "tenere", 18, fill=S.INK2),
          *_writing(45, 148, [86, 77, 88, 73, 80], 9),
          _t(375, 105, "sensum", 18, fill=S.INK2),
          _t(375, 128, "eligere", 18, fill=S.INK2),
          *_writing(376, 148, [92, 82, 88, 79], 9),
          _t(44, 249, "glosa", 19),
          _t(44, 272, "marginal", 18),
          *_writing(45, 290, [85, 77, 84, 69, 88], 9),
          _t(375, 249, "lugares", 18),
          _t(375, 272, "paralelos", 18),
          *_writing(376, 290, [88, 77, 91, 82, 69], 9),
          _p("M138 157 C154 157 143 163 166 163 M365 157 C347 157 359 193 339 193 M137 298 C156 298 145 269 166 269 M365 306 C349 306 355 307 339 307", S.INK2, 1),
          _t(170, 374, "glosa interlinear", 18),
          _p("M251 355 V335", S.INK2, 1),
          _t(44, 400, "o texto permanece no centro", 18, fill=S.INK2)]
    # An accumulated apparatus surrounds the same nucleus. The paired leaves
    # show a mode of transmission, never an attribution of these marks.
    for x in (605, 937):
        for y, lengths in ((92, [86, 78, 91, 83, 89, 74]),
                           (170, [89, 80, 85, 73, 91, 82]),
                           (248, [85, 77, 89, 81, 74, 88]),
                           (322, [91, 82, 87])):
            b += _writing(x, y, lengths, 9, S.INK2)
    b += [_p("M699 112 C716 112 698 160 726 160 M926 136 C910 136 919 207 899 207 M699 211 C714 211 709 251 728 251 M926 280 C912 280 917 296 899 296 M698 322 C713 322 709 326 728 326", S.INK2, .9),
          _p("M609 361 Q823 348 1053 361", S.GRID, 1),
          _t(832, 389, "Magna Glosa", 25, anchor="middle")]
    return S.svg(1100, 440, p.get("title") or
                 "Dois fólios esquemáticos do Corpus iuris: glosas entre linhas e nas margens e sua reunião na Magna Glosa de Acúrsio", b), []


def _recepcao(p):
    # The formal order is visible in the physical leaves. A second, curved
    # trace runs from the learned book back into the first leaf: training can
    # shape the reading of local law even before a lacuna calls for Roman law.
    b = _folio(29, 34, 252, 93)
    b += [_t(48, 63, "direito próprio", 22),
          _t(48, 88, "primeiro", 18, fill=S.INK2),
          *_writing(49, 105, [180, 167], 9)]
    b += _folio(45, 162, 252, 85)
    b += [_t(64, 191, "direito romano", 22),
          _t(64, 217, "subsidiário", 18),
          *_writing(65, 233, [181], 9),
          _t(138, 147, "lacuna", 17, fill=S.INK2)]
    b += _arrow("M252 108 C286 108 300 115 300 139 C300 160 282 177 278 177", 278, 177,
                S.INK, 1.6, direction="left")
    b += _open_book(28, 279, 99, 29)
    b += _writing(36, 287, [32, 29], 7)
    b += _writing(83, 287, [31, 29], 7)
    b += [_t(149, 285, "formação", 18),
          _t(149, 309, "romanística", 18),
          _p("M64 269 C8 255 8 207 12 146 C15 105 10 95 37 95", S.INK2, 1.4),
          _p("M30 91 L37 95 L30 99", S.INK2, 1.4)]
    return S.svg(320, 330, p.get("title") or
                 "A prioridade formal do direito próprio, o recurso subsidiário ao romano e a influência romanística da formação do jurista", b), []


def _universidade(p):
    # A book on a lectern keeps the two habits together, on facing leaves.
    b = [_p("M28 228 L159 251 L292 228 M159 252 V284 M120 295 H198", S.INK, 2),
         _p("M67 222 L111 276 M254 222 L209 276", S.INK2, 1.2)]
    b += _open_book(25, 48, 270, 172)
    b += [_t(42, 83, "texto", 22),
          _t(42, 111, "recebido", 20),
          *_writing(43, 132, [93, 82, 91], 10),
          _t(42, 183, "verba tenere", 17, fill=S.INK2),
          _t(179, 83, "razões", 22),
          *_writing(181, 105, [90, 81, 89, 84], 10),
          _t(179, 168, "sensum", 18, fill=S.INK2),
          _t(179, 192, "eligere", 18, fill=S.INK2),
          _t(25, 27, "universidade", 21),
          _t(160, 324, "aprender a interpretar", 20, anchor="middle")]
    return S.svg(320, 342, p.get("title") or
                 "O livro universitário reúne fidelidade ao texto recebido e investigação racional do seu sentido", b), []


def _dominio(p):
    b = [_t(160, 25, "dominium directum", 21, anchor="middle"),
         _t(160, 49, "actio directa", 17, fill=S.INK2, anchor="middle"),
         _p("M32 78 V66 H288 V78 M160 52 V66", S.INK2, 1.1),
         S.path("M46 94 L287 113 L270 216 L28 200 Z", fill=S.PAPER,
                stroke=S.INK, stroke_width=1.7),
         _p("M47 101 L280 119 M36 191 L266 207", S.GRID, 1),
         _p("M61 113 l-4 24 M94 116 l-4 23 M128 119 l-3 23 M162 122 l-3 22 M196 125 l-3 22 M230 127 l-3 22 M263 130 l-3 21", S.GRID, 1),
         _p("M50 175 l-3 17 M83 177 l-3 18 M117 179 l-3 19 M151 182 l-3 18 M185 185 l-3 18 M219 187 l-3 18 M253 190 l-3 17", S.GRID, 1),
         _t(159, 168, "a mesma terra", 23, anchor="middle"),
         _p("M29 229 V241 H288 V229 M160 241 V257", S.INK2, 1.1),
         _t(160, 278, "dominium utile", 21, anchor="middle"),
         _t(160, 304, "actio utilis", 17, fill=S.INK2, anchor="middle")]
    # Both brackets encompass the whole parcel. There are no halves and no
    # depiction of utile as a factual act of extracting utility from the land.
    return S.svg(320, 320, p.get("title") or
                 "Uma única terra comporta dominium directum e dominium utile, associados à actio directa e à actio utilis", b), []


def _estatutos(p):
    b = [_t(19, 24, "uma cidade", 18),
         _t(196, 24, "outra cidade", 18)]
    # The two town silhouettes have gates, not portraits or labelled cards.
    for x in (23, 200):
        b += [_p(f"M{x} 99 V65 H{x + 14} V45 H{x + 30} V65 H{x + 43} V55 H{x + 63} V67 H{x + 80} V99 M{x - 4} 99 H{x + 86}", S.INK, 1.5),
              _p(f"M{x + 3} 65 l5 -8 l6 8 M{x + 43} 55 l10 -11 l10 11", S.INK2, 1),
              _p(f"M{x + 17} 54 h7 M{x + 47} 72 h10 M{x + 70} 77 h7 M{x + 36} 99 V84 q7 -11 14 0 V99", S.INK2, 1)]
    b += _folio(18, 115, 111, 81)
    b += _folio(193, 115, 111, 81)
    for x in (32, 207):
        b += [_t(x, 142, "estatuto", 20),
              *_writing(x, 157, [77, 68, 74], 10)]
    # A winding route joins the gates behind the two statute leaves. No arrow
    # asserts a modern conflicts rule or a single law for every transaction.
    b += [_p("M67 100 C67 108 153 93 153 132 C153 163 135 198 159 215 C188 235 245 219 244 200", S.INK2, 1.4,
             stroke_dasharray="4 4"),
          _p("M244 114 V100", S.INK2, 1.4),
          _p("M27 229 l13 -11 l13 11 M31 227 V245 H49 V227 M38 245 V234 H43 V245", S.INK, 1.3),
          _p("M209 226 H232 V246 H209 Z M213 231 h15 m-15 5 h12 m-12 5 h15", S.INK, 1.1),
          _t(20, 274, "imóvel", 20),
          _t(20, 301, "localização", 18, fill=S.INK2),
          _t(174, 274, "contrato", 20),
          _t(174, 298, "lugar da", 18, fill=S.INK2),
          _t(174, 320, "conclusão", 18, fill=S.INK2)]
    return S.svg(320, 330, p.get("title") or
                 "Estatutos de cidades ligadas por relações: a escolha do direito pertinente distingue o imóvel e sua localização do contrato e seu lugar de conclusão", b), []


def _crise(p):
    b = [_t(26, 25, "direito aplicado", 20)]
    b += _closed_book(25, 45, 261, 123, "")
    b += [_t(66, 91, "compilação", 24),
          _t(66, 121, "nacional", 24),
          _p("M65 139 H251", S.GRID, 1),
          _p("M38 178 H286 M43 183 H280", S.INK2, .8)]
    b += _closed_book(53, 212, 226, 68, "Corpus iuris", 23)
    b += [_t(84, 313, "subsidiário", 20, fill=S.INK2),
          _p("M69 282 V305 H77", S.INK2, 1.1)]
    # A changed hierarchy of books, not a uniform march across all Europe.
    return S.svg(320, 330, p.get("title") or
                 "Nos ordenamentos em que se impõe a compilação nacional, ela se torna direito aplicado e o Corpus iuris ocupa posição subsidiária", b), []


def _argumento(p):
    b = _folio(27, 22, 460, 370)
    b += [_t(54, 63, "apresentação de documento", 24),
          _p("M53 78 H459", S.GRID, 1),
          _t(55, 119, "apresentação", 27),
          _p("M55 128 H227", S.INK2, 1.3),
          _p("M143 129 V150 C143 169 100 162 100 185 M143 150 C143 164 89 165 89 183 V245", S.INK, 1.6),
          _t(121, 202, "pelo próprio", 23),
          _t(121, 264, "por procurador", 23, fill=S.DIF),
          _p("M101 271 H292", S.DIF, 1.3),
          # The marginal arguments reach the extension; the term alone does not.
          _t(346, 129, "razões", 18, fill=S.INK2),
          _t(346, 173, "contexto", 18),
          _t(346, 218, "ratio", 18),
          _t(346, 263, "comparação", 18),
          _p("M329 148 V278 M329 150 h8 M329 276 h8 M327 239 C312 239 316 258 302 258", S.INK2, 1.2),
          _p("M55 313 H459", S.GRID, 1),
          _t(55, 344, "a palavra encontra seu alcance", 21),
          _t(55, 372, "no confronto das razões", 21),
          _t(31, 426, "texto · contexto · argumento", 17, fill=S.INK2)]
    return S.svg(520, 440, p.get("title") or
                 "A palavra apresentação alcança a apresentação por procurador com razões de contexto, ratio e comparação", b), []


def _autoridade(p):
    b = [_t(22, 28, "perícia", 19), _t(213, 28, "razões", 19)]
    # The beam remains capable of movement: no count decides the argument.
    b += [_p("M159 63 V231 M147 232 H172 M134 245 H185", S.INK, 2),
          S.circle(159, 73, 5, fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
          _p("M42 81 H274", S.INK, 2),
          _p("M63 81 L35 177 M63 81 L97 177 M248 81 L216 177 M248 81 L282 177", S.INK2, 1.2),
          _p("M25 177 Q64 206 106 177 Z", S.INK, 1.5),
          _p("M208 177 Q248 206 289 177 Z", S.INK, 1.5)]
    b += _closed_book(40, 133, 47, 42, "", 16)
    b += [_p("M51 140 h24 M51 148 h19 M51 156 h24", S.GRID, 1)]
    # Loose contrary arguments rest in the other scale pan.
    b += [S.path("M227 132 L272 126 V175 H227 Z", fill=S.PAPER,
                 stroke=S.CONC, stroke_width=1.4),
          S.path("M219 138 L263 132 V176 H219 Z", fill=S.PAPER,
                 stroke=S.INK, stroke_width=1.2),
          _p("M227 148 l27 -4 M227 158 l27 -4 M227 168 l23 -3", S.GRID, 1),
          _t(20, 263, "a autoridade pesa", 19),
          _t(20, 283, "e admite refutação", 17, fill=S.CONC)]
    return S.svg(320, 300, p.get("title") or
                 "O peso da perícia na balança do argumento continua sujeito a razões contrárias", b), []


def _desfecho(p):
    b = []
    # A small inherited codex is the common origin of two simultaneous routes.
    b += _open_book(493, 10, 114, 51)
    b += _writing(505, 25, [33, 29, 31], 8)
    b += _writing(561, 25, [32, 29, 33], 8)
    b += [_p("M549 77 V84 H243 V118 M549 84 H853 V118", S.INK2, 1.4),
          _t(30, 112, "Sentido histórico", 25),
          _t(655, 112, "Uso e vigência", 25)]
    # Left: the critical reader distinguishes layers rather than treating every
    # word transmitted in the book as part of the same historical moment.
    b += _open_book(32, 132, 451, 192)
    b += [_t(54, 161, "glosas", 18),
          *_writing(54, 177, [154, 143, 151], 10),
          _t(54, 231, "interpolações", 18),
          *_writing(54, 248, [152, 132, 144], 10),
          _p("M214 162 C239 162 223 216 266 220 M214 238 C237 238 247 232 266 230", S.INK2, 1.2),
          _t(350, 220, "contexto", 20, anchor="middle"),
          _t(350, 246, "original", 20, anchor="middle"),
          S.circle(349, 224, 76, fill="none", stroke=S.INK, stroke_width=2.5),
          S.circle(349, 224, 69, fill="none", stroke=S.GRID, stroke_width=1),
          _p("M401 281 L452 338", S.INK, 8),
          _p("M401 281 L452 338", S.PAPER, 3),
          _t(31, 377, "reconstituir o texto em seu tempo", 20)]
    # Right: a working notebook receives national norms and evidence of use.
    b += _folio(653, 129, 407, 204)
    b += [_p("M674 136 V324", S.INK2, 1.2)]
    for y in (153, 183, 213, 243, 273, 303):
        b.append(_p(f"M645 {y} Q659 {y - 9} 677 {y}", S.INK2, 1.3))
    b += [_t(701, 170, "normas nacionais", 22),
          *_writing(703, 187, [291, 271], 11),
          _t(701, 233, "prática de recepção", 22),
          *_writing(703, 250, [282, 260], 11),
          _t(701, 304, "norma por norma", 20, fill=S.INK2),
          _t(655, 377, "verificar o direito recebido em uso", 20)]
    return S.svg(1100, 400, p.get("title") or
                 "O material herdado abre duas investigações: o sentido histórico dos textos e a recepção prática das suas normas", b), []


def _state(p, maximum):
    state = p.get("state")
    if not isinstance(state, int) or isinstance(state, bool) or not 1 <= state <= maximum:
        raise ValueError(f"oficina_comum: state must be an integer from 1 to {maximum}")
    return state


def _recepcao_state(p):
    """School, subsidiary entry, then the formal order of consultation, pp.442–443."""
    s = _state(p, 3)
    b = _folio(29, 34, 252, 93)
    b += [_t(48, 63, "direito próprio", 22),
          _t(48, 88, "primeiro" if s > 1 else "na cidade e no reino", 18,
             fill=S.INK2), *_writing(49, 105, [180, 167], 9)]
    b += _folio(45, 162, 252, 85)
    b += [_t(64, 191, "direito romano", 22),
          _t(64, 217, "subsidiário" if s > 1 else "nas escolas", 18),
          *_writing(65, 233, [181], 9)]
    if s > 1:
        b += _f([_t(138, 147, "lacuna", 17, fill=S.INK2),
                 *_arrow("M252 108 C286 108 300 115 300 139 C300 160 282 177 278 177",
                         278, 177, S.INK, 1.6, direction="left")], s == 2)
    if s < 3:
        b += _open_book(28, 279, 99, 29)
        b += _writing(36, 287, [32, 29], 7)
        b += _writing(83, 287, [31, 29], 7)
        b += [_t(149, 285, "formação", 18),
              _t(149, 309, "romanística", 18),
              _p("M64 269 C8 255 8 207 12 146 C15 105 10 95 37 95", S.INK2, 1.4),
              _p("M30 91 L37 95 L30 99", S.INK2, 1.4)]
    else:
        # The route passes down the outside edges of the physical leaves;
        # it is an order of consultation, not a modern hierarchy of norms.
        b += _f([_p("M16 62 V213 M12 206 L16 213 L20 206", S.DIF, 1.7),
                 _t(30, 289, "a ordem está no", 19),
                 _t(30, 316, "direito particular", 21)])
    return S.svg(320, 342, p.get("title") or
                 ["O ensino romano circula entre ordenamentos locais",
                  "A lacuna permite recorrer ao romano; a formação também influencia a leitura do direito local",
                  "O direito particular enuncia a prioridade local e a passagem ao direito subsidiário"][s - 1], b), []


def _spine(x, width, title, size=16, color=S.INK):
    """A standing book, not a labelled diagram box."""
    y, h = 51, 170
    return [S.path(f"M{x} {y} Q{x + 4} {y - 3} {x + 9} {y} H{x + width} V{y + h} H{x + 9} Q{x + 4} {y + h - 3} {x} {y + h} Z",
                   fill=S.PAPER, stroke=color, stroke_width=1.4),
            _p(f"M{x + 6} {y + 2} V{y + h - 2} M{x + 9} {y + 15} H{x + width - 3} M{x + 9} {y + h - 15} H{x + width - 3}", S.GRID, 1),
            _t(0, 0, title, size, anchor="middle",
               transform=f"translate({x + width / 2 + 3} {y + h / 2}) rotate(-90)")]


def _fontes_state(p):
    """The four received divisions become five school volumes, pp.443,446."""
    s = _state(p, 3)
    b = [_t(13, 25, "Corpus iuris" if s == 1 else "o livro na escola", 22)]
    if s == 1:
        for i, title in enumerate(("Institutiones", "Digesto", "Código", "Novelas")):
            b += _spine(13 + i * 49, 40, title, 17)
        b += [_t(13, 258, "compilar · compatibilizar", 18),
              _t(13, 286, "o texto já tem camadas", 18, fill=S.INK2)]
    else:
        sp = []
        for i, title in enumerate(("Digesto Velho", "Infortiatum", "Digesto Novo", "Código", "Volumen parvum")):
            sp += _spine(10 + i * 42, 35, title, 17)
        b += _f(sp, s == 2)
        if s == 2:
            b += _f([_p("M179 224 V236 H213 V224 M196 236 V246", S.INK2, 1.2),
                     _t(13, 268, "tres libri · Institutiones", 18),
                     _t(13, 296, "Novelas · direito feudal", 18)])
        else:
            # A common binding claim spans the books. The separate local
            # leaf still has its own edge; unity never deletes it wholesale.
            b += _f([_p("M11 235 V249 H211 V235", S.INK, 1.4),
                     _t(112, 275, "unum ius", 22, anchor="middle"),
                     _t(160, 320, "império · razão", 20, anchor="middle")])
    b += _folio(238, 76, 70, 141)
    b += [_t(246, 104, "direito", 16),
          _t(246, 125, "próprio", 16), *_writing(247, 145, [48, 42, 47, 39], 11)]
    return S.svg(320, 340, p.get("title") or
                 ["Os quatro conjuntos justinianeus, ao lado do direito próprio",
                  "As escolas reagrupam o material em cinco volumes e incluem materiais feudais e imperiais",
                  "A unidade reivindicada pelo império e pela razão acompanha o ensino dos mesmos livros"][s - 1], b), []


def _universidade_state(p):
    """One lectern carries disputation, close reading and annotation, pp.456–459."""
    s = _state(p, 4)
    b = [_p("M28 228 L159 251 L292 228 M159 252 V284 M120 295 H198", S.INK, 2),
         _p("M67 222 L111 276 M254 222 L209 276", S.INK2, 1.2)]
    b += _open_book(25, 48, 270, 172)
    if s == 1:
        b += [_t(43, 89, "razão", 24), _t(178, 89, "objeção", 24),
              *_writing(44, 111, [92, 82, 91], 11),
              *_writing(180, 111, [88, 78, 89], 11),
              _p("M139 169 C157 153 166 154 182 170 M139 180 C156 195 169 195 182 179", S.INK2, 1.5),
              _t(25, 27, "discussão universitária", 19),
              _t(160, 324, "responder às razões", 21, anchor="middle")]
    else:
        b += _f([_t(42, 83, "texto", 22), _t(42, 111, "recebido", 20),
                 *_writing(43, 132, [93, 82, 91], 10),
                 _t(42, 183, "verba tenere", 17, fill=S.INK2),
                 _t(179, 83, "sentido", 22),
                 *_writing(181, 105, [90, 81, 89, 84], 10),
                 _t(179, 168, "sensum", 18, fill=S.INK2),
                 _t(179, 192, "eligere", 18, fill=S.INK2)], s == 2)
        if s == 2:
            b += _f([_t(25, 27, "Irnério · Bolonha", 21),
                     _t(160, 324, "palavras e sentido", 21, anchor="middle")])
        elif s == 3:
            b += _f([_t(25, 27, "Bolonha", 21), _t(211, 27, "França", 21),
                     *_arrow("M119 20 H200", 200, 20, S.INK2, 1.4),
                     _t(160, 324, "o ensino atravessa os Alpes", 18, anchor="middle")])
        else:
            b += _f([_t(25, 27, "glosa", 22),
                     _p("M45 139 q17 -7 35 0 m-33 14 q21 -6 38 0", S.DIF, 1),
                     _p("M46 158 q20 -7 42 -1 M129 119 V161 M126 119 h6 M126 161 h6", S.DIF, 1),
                     _p("M199 146 q13 -7 27 0 q13 7 25 0 M199 153 q13 -6 31 0", S.DIF, 1),
                     _t(160, 324, "entre as linhas e à margem", 19, anchor="middle")])
    return S.svg(320, 342, p.get("title") or
                 ["A discussão universitária exercita razões e objeções",
                  "A leitura dos glosadores esclarece palavras e investiga seu sentido",
                  "O ensino passa da Itália à França e encontra a escolástica francesa",
                  "A análise deixa glosas entre as linhas e na margem do livro"][s - 1], b), []


def _town(x, y):
    return [_p(f"M{x} {y + 54} V{y + 20} H{x + 14} V{y} H{x + 30} V{y + 20} H{x + 43} V{y + 10} H{x + 63} V{y + 22} H{x + 80} V{y + 54} M{x - 4} {y + 54} H{x + 86}", S.INK, 1.5),
            _p(f"M{x + 3} {y + 20} l5 -8 l6 8 M{x + 43} {y + 10} l10 -11 l10 11 M{x + 36} {y + 54} V{y + 39} q7 -11 14 0 V{y + 54}", S.INK2, 1)]


def _estatutos_state(p):
    """City statutes change, travel and enter a practical consilium, pp.461–462."""
    s = _state(p, 3)
    if s < 3:
        b = [_t(20, 25, "uma cidade", 18), _t(196, 25, "outra cidade", 18)]
        b += _town(23, 48) + _town(200, 48)
        b += _folio(18, 120, 111, 94) + _folio(193, 120, 111, 94)
        for x in (32, 207):
            b += [_t(x, 150, "estatuto", 20), *_writing(x, 167, [77, 68, 74], 11)]
        # The passage first says the statutes change; the link between places comes next.
        # Corrections on an ordinary flat leaf indicate that the statute
        # itself changes. No editorial quotation or invented wording.
        b += [_p("M31 176 H106 M33 179 q20 -6 37 0 m-37 9 q29 -5 68 0", S.DIF, 1.3),
              _t(160, 277, "muda a vida", 20, anchor="middle"),
              _t(160, 301, "muda o estatuto", 20, anchor="middle")]
        if s == 2:
            b += _f([_p("M67 103 C67 112 153 96 153 132 C153 164 136 225 159 242 C188 262 245 242 244 218", S.INK2, 1.4, stroke_dasharray="4 4"),
                     _p("M244 120 V103", S.INK2, 1.4),
                     _t(160, 326, "e relaciona lugares", 20, anchor="middle")])
    else:
        b = _open_book(10, 28, 180, 75)
        b += [_t(27, 56, "romano", 17), _t(109, 56, "canônico", 16)]
        b += _writing(27, 69, [57, 52], 8) + _writing(111, 69, [57, 49], 8)
        b += _folio(215, 32, 83, 84)
        b += [_t(224, 61, "estatuto", 16), *_writing(225, 76, [57, 50, 54], 9)]
        b += _folio(69, 174, 206, 140)
        b += [_t(88, 207, "consilium", 25), *_writing(89, 228, [155, 141, 157, 147, 152], 12)]
        b += _arrow("M97 115 C97 142 128 133 128 174", 128, 174, S.INK2, 1.5, "down")
        b += _arrow("M257 124 C257 146 228 143 228 174", 228, 174, S.INK2, 1.5, "down")
    return S.svg(320, 342, p.get("title") or
                 ["Cada cidade tem estatutos próprios e os modifica à medida que a vida muda",
                  "Relações interurbanas ligam cidades cujos estatutos mudam",
                  "O parecer prático relaciona o direito romano, o canônico e os estatutos"][s - 1], b), []


def _dominio_state(p):
    """Two forms of protection support two positions over the whole parcel, p.465."""
    s = _state(p, 3)
    b = [S.path("M46 94 L287 113 L270 216 L28 200 Z", fill=S.PAPER,
                stroke=S.INK, stroke_width=1.7),
         _p("M47 101 L280 119 M36 191 L266 207", S.GRID, 1),
         _p("M61 113 l-4 24 M94 116 l-4 23 M128 119 l-3 23 M162 122 l-3 22 M196 125 l-3 22 M230 127 l-3 22 M263 130 l-3 21", S.GRID, 1),
         _p("M50 175 l-3 17 M83 177 l-3 18 M117 179 l-3 19 M151 182 l-3 18 M185 185 l-3 18 M219 187 l-3 18 M253 190 l-3 17", S.GRID, 1),
         _t(159, 168, "a mesma terra", 23, anchor="middle")]
    if s == 1:
        b += [_t(160, 33, "direitos coexistentes", 22, anchor="middle"),
              _p("M32 78 V66 H288 V78 M29 229 V241 H288 V229", S.INK2, 1.1),
              _t(160, 291, "uma distinção a construir", 20, anchor="middle")]
    if s > 1:
        b += _f([_t(160, 25, "dominium directum", 21, anchor="middle"),
                 _t(160, 49, "actio directa", 17, fill=S.INK2, anchor="middle"),
                 _p("M32 78 V66 H288 V78 M160 52 V66", S.INK2, 1.1)], s == 2)
    if s == 2:
        b += _f([_t(160, 278, "a posição do proprietário", 20, anchor="middle")])
    if s == 3:
        b += _f([_p("M29 229 V241 H288 V229 M160 241 V257", S.DIF, 1.3),
                 _t(160, 278, "dominium utile", 21, fill=S.DIF, anchor="middle"),
                 _t(160, 304, "actio utilis", 17, fill=S.DIF, anchor="middle")])
    return S.svg(320, 330, p.get("title") or
                 ["Direitos de pessoas diferentes coexistem sobre a mesma terra",
                  "A actio directa fornece o apoio da posição de dominium directum",
                  "A actio utilis dá nome ao dominium utile; as duas posições abrangem a mesma terra"][s - 1], b), []


def _argumento_state(p):
    """The documented extension and its general hermeneutic supports, pp.469–470."""
    s = _state(p, 3)
    b = _folio(27, 22, 460, 370)
    b += [_t(54, 63, "apresentação de documento", 24),
          _p("M53 78 H459", S.GRID, 1),
          _t(55, 119, "apresentação", 27),
          _p("M55 128 H227", S.INK2, 1.3),
          # one stem, two plain ticks: no curve runs behind the labels
          _p("M84 130 V262", S.INK, 1.6),
          _p("M84 196 H104", S.INK, 1.6),
          _p("M84 262 H104", S.INK, 1.6),
          _t(116, 203, "pelo próprio", 23),
          _t(116, 269, "por procurador", 23, fill=S.DIF)]
    if s > 1:
        b += _f([_t(346, 129, "contexto", 18), *_writing(347, 145, [91, 80], 9),
                 _t(346, 202, "ratio", 21), *_writing(347, 218, [90, 81], 9),
                 _p("M329 120 V253 M329 120 h8 M329 253 h8", S.INK2, 1.2)], s == 2)
    if s == 3:
        b += _f([_p("M112 279 H329 V258 M324 264 L329 257 L334 264", S.DIF, 1.7),
                 _t(55, 344, "o alcance é reconstruído", 22),
                 _t(55, 373, "pelas razões do instituto", 21)])
    elif s == 1:
        b += [_t(55, 344, "mens · vontade racional", 21)]
    else:
        b += _f([_t(55, 344, "um preceito entre outros", 21)])
    return S.svg(520, 440, p.get("title") or
                 ["Bártolo inclui a apresentação pelo próprio e pelo procurador",
                  "O preceito é integrado no contexto e na ideia geral do instituto",
                  "A razão do instituto sustenta a extensão do alcance do preceito"][s - 1], b), []


def _autoridade_state(p):
    """Expertise bears weight but leaves the other pan open to reasons, pp.475–477."""
    s = _state(p, 3)
    b = [_t(22, 28, "perícia", 19), _t(213, 28, "razões", 19),
         _p("M159 63 V231 M147 232 H172 M134 245 H185", S.INK, 2),
         S.circle(159, 73, 5, fill=S.PAPER, stroke=S.INK, stroke_width=1.5)]
    # The source gives no amount or arithmetic of credibility. Moving the
    # beam shows that a better reason can counter expertise, not a vote count.
    left, right = (94, 68) if s == 1 else (81, 81)
    mv = [_p(f"M42 {left} L274 {right}", S.INK, 2),
          _p(f"M63 {left - 2} L35 {left + 96} M63 {left - 2} L97 {left + 96} M248 {right + 2} L216 {right + 96} M248 {right + 2} L282 {right + 96}", S.INK2, 1.2),
          _p(f"M25 {left + 96} Q64 {left + 125} 106 {left + 96} Z", S.INK, 1.5),
          _p(f"M208 {right + 96} Q248 {right + 125} 289 {right + 96} Z", S.INK, 1.5)]
    mv += _closed_book(40, left + 52, 47, 42, "", 16)
    mv += [_p(f"M51 {left + 59} h24 M51 {left + 67} h19 M51 {left + 75} h24", S.GRID, 1)]
    if s > 1:
        mv += [S.path(f"M227 {right + 51} L272 {right + 45} V{right + 94} H227 Z", fill=S.PAPER,
                      stroke=S.CONC, stroke_width=1.4),
               S.path(f"M219 {right + 57} L263 {right + 51} V{right + 95} H219 Z", fill=S.PAPER,
                      stroke=S.INK, stroke_width=1.2),
               _p(f"M227 {right + 67} l27 -4 M227 {right + 77} l27 -4 M227 {right + 87} l23 -3", S.GRID, 1)]
    # The beam changes position between the first and second state; the third keeps the second.
    b += _f(mv, s == 2)
    b += _f([_t(20, 274, ["o saber tem peso", "a objeção pode prevalecer", "uma direção, ainda discutível"][s - 1], 18)], s > 1)
    if s == 3:
        b += _f([_p("M35 294 H286", S.INK2, 1.1),
                 _p("M279 289 L286 294 L279 299", S.INK2, 1.1),
                 _t(20, 326, "soluções admitidas e provadas", 17, fill=S.INK2)])
    return S.svg(320, 342, p.get("title") or
                 ["A perícia reconhecida do jurista confere peso à sua opinião",
                  "Uma razão contrária pode infirmar a autoridade",
                  "As soluções aceitas orientam a interpretação conservando a possibilidade de refutação"][s - 1], b), []


def _rel_row(y, top, bottom, label, side=False, color=S.INK):
    """One position of the common law against the local laws, as two small books."""
    if side:
        out = [S.rect(24, y, 76, 40, fill=S.PAPER, stroke=color, stroke_width=1.5),
               S.rect(106, y, 76, 40, fill=S.PAPER, stroke=color, stroke_width=1.5),
               _t(62, y + 26, top, 17, anchor="middle"), _t(144, y + 26, bottom, 17, anchor="middle")]
    else:
        out = [S.rect(24, y, 158, 40, fill=S.PAPER, stroke=color, stroke_width=1.8),
               S.rect(44, y + 44, 118, 34, fill=S.PAPER, stroke=S.INK2, stroke_width=1.2),
               _t(103, y + 26, top, 18, anchor="middle"), _t(103, y + 67, bottom, 17, fill=S.INK2, anchor="middle")]
    return out + [_t(198, y + 36, label, 19, fill=color)]


def _crise_state(p):
    """A national book takes the working position; received law becomes subsidiary, pp.480–482."""
    s = _state(p, 3)
    if s == 1:
        # The outline keeps the former practical place of the Roman book while the national compilation occupies it.
        b = [_p("M41 28 H279 V75 M47 34 H272 V70", S.GRID, 1.1)]
        b += _closed_book(25, 48, 261, 114, "")
        b += [_t(66, 91, "compilação", 24), _t(66, 121, "nacional", 24),
              _t(26, 25, "direito aplicado", 20),
              _t(294, 25, "centralização", 18, fill=S.INK2, anchor="end")]
        b += _closed_book(53, 222, 226, 68, "Corpus iuris", 23)
        b += [_p("M299 89 V250 M294 243 L299 250 L304 243", S.INK2, 1.5),
              _t(26, 193, "muda o lugar das fontes", 20),
              _t(84, 323, "subsidiário", 20, fill=S.INK2)]
    elif s == 2:
        b = _open_book(30, 56, 256, 164)
        b += [_t(45, 93, "norma", 21), _t(45, 121, "nacional", 21),
              *_writing(46, 140, [94, 82, 89, 80], 11),
              _t(180, 93, "exigência", 19), _t(180, 119, "presente", 19),
              *_writing(181, 140, [84, 75, 82, 70], 11),
              _p("M133 187 Q156 202 180 186", S.INK2, 1.3),
              _t(160, 272, "o texto já nasce", 21, anchor="middle"),
              _t(160, 302, "das novas condições", 21, anchor="middle")]
    else:
        b = _rel_row(16, "comum", "próprios", "predomínio")
        b += _f(_rel_row(120, "comum", "próprios", "equilíbrio", side=True))
        b += _f(_rel_row(224, "próprios", "comum", "autonomia", color=S.DIF))
        b += [_p("M302 40 V292 M297 285 L302 292 L307 285", S.INK2, 1.3)]
    return S.svg(320, 342, p.get("title") or
                 ["A compilação nacional ocupa o lugar do direito usualmente aplicado e o Corpus fica em posição subsidiária",
                  "Disposições nascidas das exigências novas reduzem a antiga necessidade de adaptação dos textos romanos",
                  "A relação entre fontes passa do predomínio do comum ao equilíbrio e à autonomia dos direitos próprios"][s - 1], b), []


STATE_MODES = {"recepcao": _recepcao_state, "fontes": _fontes_state,
               "universidade": _universidade_state, "estatutos": _estatutos_state,
               "dominio": _dominio_state, "argumento": _argumento_state,
               "autoridade": _autoridade_state, "crise": _crise_state}


MODES = {"hero": _hero, "fontes": _fontes, "folios": _folios,
         "recepcao": _recepcao, "universidade": _universidade,
         "dominio": _dominio, "estatutos": _estatutos,
         "argumento": _argumento, "autoridade": _autoridade, "crise": _crise,
         "desfecho": _desfecho}


def build(p: dict) -> tuple[str, list[dict]]:
    mode = p.get("mode")
    if mode not in MODES:
        raise ValueError(f"oficina_comum: mode must be one of {', '.join(MODES)}")
    if "state" in p:
        if mode not in STATE_MODES:
            raise ValueError(f"oficina_comum: mode {mode} has no reading states")
        return STATE_MODES[mode](p)
    return MODES[mode](p)
