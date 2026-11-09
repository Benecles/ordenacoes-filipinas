"""oficina_comum: books, folios and instruments for the schools of ius commune.

Params (facts and reading mode, never drawing coordinates):
  mode   hero | fontes | folios | argumento | autoridade | desfecho (required)
  title  optional accessible description in place of the mode's default

Canvases (width x height): hero 1100x440; fontes 320x290;
folios 1100x475; argumento 520x440; autoridade 320x290;
desfecho 1100x400. Wide drawings use type of at least 16 units.

All modes are static, build(p) -> (svg, []). Folios are didactic reconstructions,
not facsimiles or historical glosses attributed to a named jurist. The running
example is the presentation of a document by the person concerned or a procurator, from
Hespanha 1982, p.469. Other provenance: sources pp.441-453; glossa pp.459-460;
commentary pp.461-465; arguments pp.468-477; later schools pp.481-488. The page's
plan.md and notes.md carry the full claim log and reconstruction notice.

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


def _writing(x, y, widths, gap=11, color=S.GRID):
    return [S.line(x, y + i * gap, x + width, y + i * gap,
                   stroke=color, stroke_width=1) for i, width in enumerate(widths)]


def _arrow(d, x, y, color=S.INK, width=1.8, direction="right"):
    dx = -1 if direction == "right" else 1
    return [_p(d, color, width),
            _p(f"M{x + dx * 7} {y - 4} L{x} {y} L{x + dx * 7} {y + 4}",
               color, width)]


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
    b = [_t(27, 29, "Glosa · o texto e sua margem", 22),
         _t(588, 29, "Comentário · uma elaboração de fontes", 22)]
    b += _folio(24, 53, 494, 371)
    b += _folio(584, 53, 494, 371)
    # The text is a compact nucleus. Multiple marginal notes have different
    # targets and lengths; a glossa is not depicted as one explanatory label.
    b += [_p("M151 86 V359 M354 86 V359", S.GRID, .8),
          _t(169, 108, "texto recebido", 18, fill=S.INK2),
          *_writing(169, 125, [166, 149, 171, 160], 11),
          _t(164, 193, "apresentação", 27),
          _p("M165 202 Q251 210 337 202", S.INK2, 1),
          *_writing(169, 224, [167, 153, 163, 147, 171, 158, 165, 143, 172, 152, 163], 11),
          _t(44, 112, "verba tenere", 16, fill=S.INK2),
          *_writing(45, 129, [87, 78, 89, 73, 83], 9),
          _t(375, 109, "sensum", 16, fill=S.INK2),
          _t(375, 130, "eligere", 16, fill=S.INK2),
          *_writing(376, 148, [91, 82, 88], 9),
          _t(44, 236, "sentido", 17),
          _t(44, 258, "da palavra", 17),
          *_writing(45, 276, [85, 77, 82, 69, 88, 75], 9),
          _t(375, 246, "lugares", 17),
          _t(375, 268, "paralelos", 17),
          *_writing(376, 286, [88, 77, 91, 82, 69], 9),
          _p("M137 145 C151 145 141 181 162 185 M365 161 C347 161 361 184 339 187 M134 247 C154 247 147 213 167 214 M365 260 C347 260 357 279 338 279 M137 305 C150 305 146 327 166 327 M365 316 C351 316 351 335 338 335", S.INK2, 1),
          _t(59, 387, "summae · regras · discussões", 18),
          _p("M59 369 Q263 357 477 369", S.GRID, 1)]
    # Continuous working prose, not two source boxes: the ius proprium is an
    # insertion inside the elaboration, carried forward into the consilium.
    b += [_t(615, 94, "apresentação de documento", 23),
          _p("M615 108 H1040", S.GRID, 1),
          _t(628, 144, "texto recebido", 19),
          *_writing(629, 164, [372, 355, 381], 11),
          _t(881, 218, "ius proprium", 18),
          _p("M875 201 V230 M870 201 H878 M870 230 H878 M875 226 C858 226 854 236 838 236", S.INK2, 1.1),
          _p("M831 240 l7 -8 l7 8", S.INK2, 1.1),
          *_writing(629, 211, [217, 199], 11),
          _t(628, 273, "apresentação por procurador", 24, fill=S.DIF),
          *_writing(630, 292, [369, 348], 11),
          _p("M628 316 Q799 326 1007 316", S.GRID, 1),
          _t(815, 352, "consilium", 25, anchor="middle"),
          _t(815, 382, "distinção · concordância · solução prática", 18,
             fill=S.INK2, anchor="middle")]
    return S.svg(1100, 440, p.get("title") or
                 "Dois fólios didáticos: um texto rodeado por glosas e uma elaboração contínua que incorpora o ius proprium à consulta", b), []


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
    return S.svg(320, 290, p.get("title") or
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


MODES = {"hero": _hero, "fontes": _fontes, "folios": _folios,
         "argumento": _argumento, "autoridade": _autoridade,
         "desfecho": _desfecho}


def build(p: dict) -> tuple[str, list[dict]]:
    mode = p.get("mode")
    if mode not in MODES:
        raise ValueError(f"oficina_comum: mode must be one of {', '.join(MODES)}")
    return MODES[mode](p)
