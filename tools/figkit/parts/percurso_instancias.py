"""percurso_instancias: the procedimento comum read across and up, drawn as a plan.

Params: title (optional accessible description); no other params.

Canvas 1084 x 560, a static drawing in the text's flow. The horizontal rail is
the first-degree case: the four stages of knowledge (postular, organizar,
instruir, decidir), then the cumprimento. Above it, the course of the appeal:
a TJ/TRF rail fed by the apelação (solid) and by interlocutory decisions
(dashed), then, higher and fenced by an orange limit, the STF/STJ rail reached
only by RE/REsp. The orange note says what the top rail is not: a third
degree. Brackets on the left name the ordinary and the extraordinary phase.

Provenance: Marinoni, Arenhart e Mitidiero, Novo curso, v.2, pp.139-146,
horizontal and vertical perspectives. An orientation map, not the history of
the running case: no dates, no folhas, no outcomes.
"""
from __future__ import annotations

from . import svg as S


def P(d, color=S.INK, width=1.5, **kw):
    return S.path(d, fill="none", stroke=color, stroke_width=width,
                  stroke_linecap="round", stroke_linejoin="round", **kw)


def T(x, y, s, size=15, fill=S.INK, family=S.SERIF, **kw):
    return S.text(x, y, s, size=size, family=family, fill=fill, **kw)


def L(x, y, s, size=12.5, fill=S.INK2, **kw):
    return S.text(x, y, s, size=size, family=S.MONO, fill=fill, letter_spacing=".05em", **kw)


def dot(x, y, hollow=True, color=S.INK, r=5):
    return S.circle(x, y, r, fill=S.PAPER if hollow else color, stroke=color, stroke_width=1.6)


def arrow(x, y, direction="up", color=S.INK):
    d = {"up": f"M{x - 5} {y + 9} L{x} {y} L{x + 5} {y + 9}",
         "down": f"M{x - 5} {y - 9} L{x} {y} L{x + 5} {y - 9}",
         "right": f"M{x - 9} {y - 5} L{x} {y} L{x - 9} {y + 5}"}[direction]
    return P(d, color, 1.6)


def build(p: dict) -> tuple[str, list[dict]]:
    Y0, Y1, Y2 = 440, 235, 72          # rails: first degree, TJ/TRF, STF/STJ
    X0 = 150
    st = [("postular", 150, 330), ("organizar", 330, 520), ("instruir", 520, 700), ("decidir", 700, 850)]
    b = []

    # ── first-degree rail: stations and stage brackets
    b.append(P(f"M{X0} {Y0} H{1010}", S.INK, 2.6))
    for name, x0, x1 in st:
        b += [P(f"M{x0 + 3} {Y0 - 70} V{Y0 - 78} H{x1 - 3} V{Y0 - 70}", S.INK2, 1.2),
              L((x0 + x1) / 2, Y0 - 88, name, 13, anchor="middle"),
              dot(x0, Y0, False)]
    b += [dot(850, Y0, False), dot(1010, Y0, False)]
    # liquidation: an optional detour, only if the condemnation is generic
    b += [P(f"M850 {Y0} C868 {Y0 + 34} 902 {Y0 + 34} 920 {Y0}", S.INK2, 1.4, stroke_dasharray="4 4"),
          T(885, Y0 + 84, "liquidação, se a condenação", 13, S.INK2, anchor="middle"),
          T(885, Y0 + 102, "for genérica", 13, S.INK2, anchor="middle"),
          T(965, Y0 - 14, "cumprir", 17, S.INK, anchor="middle", weight="600"),
          arrow(1010, Y0, "right")]
    # the sheets that mark the rail
    b += [S.rect(66, Y0 - 52, 70, 80, fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
          T(76, Y0 - 28, "inicial", 14), P(f"M76 {Y0 - 16} H126 M76 {Y0 - 6} H122 M76 {Y0 + 4} H126", S.GRID, 1)]
    # fore-edge brackets under the rail
    b += [P(f"M{X0} {Y0 + 22} V{Y0 + 30} H850 V{Y0 + 22}", S.INK2, 1.2),
          T(500, Y0 + 52, "fase de conhecimento", 16, S.INK, anchor="middle"),
          P(f"M930 {Y0 + 22} V{Y0 + 30} H1010 V{Y0 + 22}", S.INK2, 1.2),
          T(970, Y0 + 52, "quando necessário", 13, S.INK2, anchor="middle")]
    # first degree label
    b += [T(40, Y0 + 84, "Primeiro grau", 22, S.INK, family=S.SANS, weight="600"),
          T(40, Y0 + 104, "decidir e efetivar o direito no caso", 14, S.INK2, family=S.SANS)]

    # ── second degree: apelação rises from the sentence, interlocutórias from organizar
    b += [P(f"M560 {Y1} H1010", S.INK, 2.6), dot(560, Y1, False), dot(1010, Y1, False),
          T(560, Y1 - 38, "TJ / TRF", 22, S.INK, family=S.SANS, weight="600"),
          T(560, Y1 - 16, "segundo grau · revê as decisões", 14, S.INK2, family=S.SANS),
          P(f"M850 {Y0 - 14} C850 {Y0 - 70} 780 {Y1 + 40} 780 {Y1 + 6}", S.INK, 1.8), arrow(780, Y1 + 4, "up"),
          T(866, Y0 - 56, "apelação da sentença", 14, S.INK, anchor="start"),
          P(f"M430 {Y0 - 14} C430 {Y0 - 70} 650 {Y1 + 60} 650 {Y1 + 6}", S.INK2, 1.3, stroke_dasharray="4 5"),
          arrow(650, Y1 + 4, "up", S.INK2),
          T(170, Y1 + 80, "interlocutória: agravo de instrumento, quando cabível,", 13, S.INK2),
          T(170, Y1 + 98, "ou discussão na apelação (arts. 1.009 e 1.015)", 13, S.INK2)]

    # ── third level: reached by RE / REsp, a different function
    b += [P(f"M780 {Y2} H1010", S.INK, 2.6), dot(780, Y2, False), dot(1010, Y2, False),
          T(780, Y2 - 22, "STF / STJ", 22, S.INK, family=S.SANS, weight="600"),
          T(780, Y2 + 28, "interpretam o direito constitucional e federal", 14, S.INK2, family=S.SANS),
          T(780, Y2 + 48, "e formam precedentes", 14, S.INK2, family=S.SANS),
          P(f"M900 {Y1} C900 {Y1 - 50} 900 {Y2 + 90} 900 {Y2 + 62}", S.CONC, 1.6, stroke_dasharray="4 5"),
          arrow(900, Y2 + 60, "up", S.CONC),
          T(914, Y1 - 28, "RE / REsp, quando cabíveis", 13, S.INK, anchor="start"),
          P(f"M760 {Y2 - 40} V{Y2 + 70}", S.CONC, 3),
          T(752, Y2 + 10, "não é terceiro grau", 14, S.CONC, anchor="end"),
          T(752, Y2 + 30, "de jurisdição", 14, S.CONC, anchor="end")]

    # ── vertical brackets for the phases
    b += [P(f"M30 {Y1 - 20} H22 V{Y0 + 36} H30", S.INK2, 1.2),
          P(f"M30 {Y2 - 30} H22 V{Y2 + 60} H30", S.INK2, 1.2)]
    b += [S.text(16, (Y1 + Y0) / 2 + 30, "fase ordinária", size=13, family=S.MONO, fill=S.INK2, anchor="middle",
                 transform=f"rotate(-90 16 {(Y1 + Y0) / 2 + 30})", letter_spacing=".05em"),
          S.text(16, Y2 + 16, "extraordinária", size=13, family=S.MONO, fill=S.INK2, anchor="middle",
                 transform=f"rotate(-90 16 {Y2 + 16})", letter_spacing=".05em")]
    return S.svg(1084, 560, p.get("title") or
                 "O procedimento comum em duas direções: ao longo dos autos, postular, organizar, instruir, decidir e cumprir; para cima, apelação ao TJ ou TRF e, só por RE ou REsp, STF e STJ, que interpretam o direito e não formam terceiro grau.", b), []
