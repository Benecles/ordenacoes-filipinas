"""percurso_instancias: one case file, read across and up the court structure.

Params (facts, never coordinates):
  title  optional accessible description; no other params are required.

Canvas: 1084 x 535, intended for a full-width static spread in the text flow.
The lower fore-edge carries the four predominant activities of knowledge,
then eventual liquidation and fulfillment. The same file's appeal route rises
to TJ/TRF; a distinct, conditional route reaches STF/STJ for interpretation
and precedents. It does not depict a third ordinary degree of review.

Provenance: Marinoni, Arenhart and Mitidiero, Novo curso, v. 2, pp. 139-146,
especially horizontal/vertical perspectives, pp. 142-146. This is an orientation
map, not a procedural history attributed to the fictional running case. There
are no invented dates, numbered folhas, outcomes or folded paper corners.

Contract: build(p) -> (svg, objects); objects=[] (no buttons or hidden states).
All paths are emitted by this part, with house tokens for light/dark mode.
"""
from __future__ import annotations

from . import svg as S


def _p(d: str, color=S.INK, width=1.5, **kw) -> str:
    return S.path(d, fill="none", stroke=color, stroke_width=width,
                  stroke_linecap="round", stroke_linejoin="round", **kw)


def _t(x, y, words: str, size=15, color=S.INK, **kw) -> str:
    return S.text(x, y, words, size=size, family=S.SANS, fill=color, **kw)


def _writing(x, y, widths, gap=10) -> list[str]:
    return [S.line(x, y + n * gap, x + width, y + n * gap,
                   stroke=S.GRID, stroke_width=1) for n, width in enumerate(widths)]


def _group(body: list[str], transform: str) -> str:
    return f'<g {S.attrs(transform=transform)}>{"".join(body)}</g>'


def build(p: dict) -> tuple[str, list[dict]]:
    b = [
        _t(34, 30, "O mesmo procedimento, em duas direções", 23, weight="600"),
        _t(34, 57, "Ao longo dos autos: conhecer e, quando necessário, cumprir.", 15, S.INK2),
        _t(34, 80, "Nos recursos: rever o caso; no vértice, interpretar o direito.", 15, S.INK2),
    ]

    # A signed judgment grows out of the case file. Its appellate thread
    # follows the file up to a different bundle, rather than a ladder of boxes.
    b += [
        _p("M686 327 C714 288 750 274 726 250", width=1.8),
        _p("M734 252 l-8 -2 l2 8", width=1.8),
        _t(749, 248, "apelação", 14),
        _t(749, 269, "da sentença", 13, S.INK2),
        _p("M624 278 C610 253 587 240 570 218", S.INK2, 1.2,
           stroke_dasharray="4 5"),
        _t(294, 206, "interlocutórias:", 13, S.INK2),
        _t(294, 225, "agravo, quando cabível;", 13, S.INK2),
        _t(294, 244, "ou discussão na apelação", 13, S.INK2),
    ]

    # A second-grau file lies higher on the desk. The square sheets are court
    # papers: visible fore-edges, stitched holes and an acórdão entry.
    appeal = [
        S.rect(0, 0, 190, 99, fill=S.PAPER, stroke=S.INK2, stroke_width=1),
        S.path("M-5 -5 H181 V94 H-5 Z", fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
        _p("M7 3 V86", S.INK2, .8),
        S.circle(1, 18, 1.7, fill=S.INK2),
        S.circle(1, 73, 1.7, fill=S.INK2),
        _t(20, 18, "Acórdão", 15, weight="600"),
        *_writing(20, 33, [145, 129, 148, 115], 10),
        _p("M109 83 q13 -9 22 -2 t26 -2", S.INK2, 1),
    ]
    b.append(_group(appeal, "translate(537 145) rotate(-4 90 48)"))
    b += [
        _t(529, 102, "TJ / TRF", 23, weight="600"),
        _t(529, 125, "segundo grau · controle das decisões", 14),
        _t(34, 200, "Primeiro grau", 22, weight="600"),
        _t(34, 224, "decidir e efetivar o direito no caso", 14),
        _p("M35 236 C121 236 147 250 173 276", S.INK2, 1),
        _t(294, 151, "fase ordinária", 16, weight="600"),
        _p("M296 160 H492", S.INK2, 1),
        _t(294, 182, "primeiro e segundo graus", 13, S.INK2),
    ]

    # RE / REsp leave the ordinary file on a conditional, narrower route.
    # The upper object is a bound collection of reasons, not another case
    # review tray: it marks the changed function at the judicial vertex.
    b += [
        _p("M712 158 C783 158 776 92 838 92", S.CONC, 1.6,
           stroke_dasharray="4 5"),
        _p("M830 88 l8 4 l-8 4", S.CONC, 1.5),
        _t(737, 180, "RE / REsp", 13),
        _t(737, 199, "quando cabíveis", 12.5, S.INK2),
        _t(851, 30, "STF / STJ", 23, weight="600"),
        _t(851, 53, "fase extraordinária", 14),
    ]
    precedent = [
        S.path("M0 0 Q13 -9 27 -2 H157 V99 H27 Q13 91 0 99 Z",
               fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
        _p("M27 -2 V99 M35 4 H149 V91 H35", S.INK2, .9),
        _p("M9 18 h8 m-8 60 h8", S.INK2, 1),
        _t(41, 25, "Razões", 13, weight="600"),
        _t(41, 42, "de decidir", 13, weight="600"),
        *_writing(41, 53, [98, 91], 10),
        S.line(41, 78, 139, 78, stroke=S.DIF, stroke_width=1.7),
    ]
    b.append(_group(precedent, "translate(852 72) rotate(3 78 50)"))
    b += [
        _t(849, 204, "interpretação e precedentes", 14),
        _t(849, 225, "constitucional / federal", 13, S.INK2),
        _t(849, 247, "não constituem terceiro grau", 13, S.CONC),
    ]

    # A single thick file crosses the canvas. Its irregular page fore-edge
    # makes activities into a continuous material sequence, not compartments.
    b += [
        S.path("M41 348 L243 342 L441 347 L647 340 L832 346 L1040 337 V421 L833 430 L645 423 L442 430 L245 425 L41 431 Z",
               fill=S.PAPER, stroke=S.INK, stroke_width=1.6),
        _p("M42 418 L245 412 L442 417 L647 411 L833 417 L1040 408", S.INK2, 1),
        _p("M44 423 L245 417 L441 422 L647 416 L833 422 L1039 413", S.GRID, .9),
        _p("M44 428 L245 422 L441 427 L647 421 L833 427 L1039 418", S.GRID, .9),
        _p("M54 357 C243 349 432 359 641 352 C805 348 925 350 1028 345", S.INK2, 1),
    ]
    for x, y in [(74, 351), (233, 350), (407, 352), (583, 349), (769, 350), (1001, 344)]:
        b.append(_p(f"M{x} {y} q-5 17 3 19 q8 1 2 -12", S.INK2, 1))

    # The four kinds of document are views into the same file.
    initial = [
        S.rect(0, 0, 126, 85, fill=S.PAPER, stroke=S.INK, stroke_width=1.2),
        _t(12, 23, "Petição inicial", 14, weight="600"),
        *_writing(12, 37, [102, 92, 104, 76], 10),
    ]
    b.append(_group(initial, "translate(69 280) rotate(-4 63 43)"))
    b += [
        _t(255, 291, "questões e provas", 13),
        _p("M255 302 H383 M255 317 H368 M255 332 H386", S.GRID, 1),
        _p("M270 299 l5 6 l10 -14 M270 314 l5 6 l10 -14", S.INK2, 1.2),
    ]
    receipt = [
        S.path("M0 0 H115 V88 L107 85 L99 89 L91 85 L83 89 L75 85 L67 89 L59 85 L51 89 L43 85 L35 89 L27 85 L19 89 L11 85 L3 89 L0 87 Z",
               fill=S.PAPER, stroke=S.INK, stroke_width=1.1),
        _t(10, 23, "Documentos", 13),
        *_writing(10, 37, [94, 82, 95], 10),
        _p("M71 72 q9 -6 17 0", S.INK2, .8),
    ]
    b.append(_group(receipt, "translate(444 276) rotate(5 57 44)"))
    judgment = [
        S.rect(0, 0, 119, 91, fill=S.PAPER, stroke=S.INK, stroke_width=1.3),
        _t(11, 23, "Sentença", 15, weight="600"),
        *_writing(11, 38, [96, 90], 10),
        S.line(11, 65, 105, 65, stroke=S.DIF, stroke_width=1.8),
        _p("M48 79 q12 -7 20 -1 t27 -3", S.INK2, .9),
    ]
    b.append(_group(judgment, "translate(622 270) rotate(-2 60 45)"))

    # One fine thread supplies reading direction on the fore-edge. The eventual
    # fifth knowledge stage is a separate loose annotation before fulfillment.
    b += [
        _p("M74 390 C276 382 488 394 704 384 S931 386 1007 375", width=1.7),
        _p("M997 371 l10 4 l-8 7", width=1.6),
        _t(83, 380, "postular", 16),
        _t(270, 378, "organizar", 16),
        _t(455, 380, "instruir", 16),
        _t(640, 376, "decidir", 16),
        _t(887, 368, "cumprir", 18, weight="600"),
        _t(841, 397, "atos que satisfazem a obrigação", 12.5, S.INK2),
        _p("M63 453 V445 H735 V453", S.INK2, 1),
        _t(399, 475, "fase de conhecimento", 16, anchor="middle"),
        _t(399, 497, "a atividade predominante dá nome ao estágio", 13, S.INK2, anchor="middle"),
        _p("M749 355 C775 326 792 318 813 320", S.INK2, 1,
           stroke_dasharray="4 4"),
        _t(785, 290, "liquidação eventual", 14),
        _t(785, 311, "se a condenação for genérica", 12.5, S.INK2),
        _p("M828 446 V438 H1033 V446", S.INK2, 1),
        _t(930, 475, "fase de cumprimento", 16, anchor="middle"),
        _t(930, 497, "quando necessária", 13, S.INK2, anchor="middle"),
    ]
    return S.svg(1084, 535, p.get("title") or
                 "O procedimento comum em duas perspectivas: os autos atravessam postulação, organização, instrução e decisão, com liquidação eventual e cumprimento quando necessário. Acima, primeiro grau e TJ ou TRF compõem a fase ordinária; STF e STJ interpretam o direito e formam precedentes na fase extraordinária, com função diferente de um terceiro grau.", b), []
