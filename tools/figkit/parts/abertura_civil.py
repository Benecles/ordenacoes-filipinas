"""abertura_civil: a cause unfolded in the case file, requests traced on carbon
copies, and an initial petition being revised. Original objects for Aula 01.

Params (facts, never coordinates):
  mode       percurso | pedidos | revisao (required)
  title      optional accessible title
  claimant   optional name, default Cecília
  defendant  optional name, default Oficina Horizonte

The drawings contain no dates, monetary amounts or invented folha numbers.
The procedural map is an accordion folio; creases carry the stages and two
pleadings converge on the disputed facts before the evidence reaches judgment.
The clipboard has three alternative tracings: ambos, subsidiario, qualquer.
The revision sheet has three numbered proofreader's tabs: valor, cpf, novo.
Map selection traces the relevant dependencies on the folio itself.
Only ambos draws rental receipts; the other modes replace them with a folded
valuation sheet for the machine's monetary equivalent, without inventing a sum.

Contract:
  build(p) -> (svg, objects), as with the other figkit parts.
  Map/revision targets: <g data-object="ID" role="button" tabindex="0">.
  Selection tracings and paper tabs: <g data-object-state="ID" data-state="active"
    visibility="hidden">. The page toggles visibility and writes its long
    legal answer in a fixed HTML slot outside the drawing.
  Clipboard layers: <g data-variant="ambos|subsidiario|qualquer"
    visibility="visible|hidden">; ambos is initially visible. The page
    changes only this visibility when a mode is selected.
All paths and tangible objects are emitted by the part, never hand-written SVG
in the shell source. No scroll-driven or automatic animation.
"""
from __future__ import annotations

from . import svg as S

PAPER2 = "var(--paper-2, var(--paper2, var(--paper)))"


def _hit(x, y, w, h) -> str:
    return S.rect(x, y, w, h, fill=S.INK, opacity="0")


def _group(body: list[str], **attrs) -> str:
    return f'<g {S.attrs(**attrs)}>{"".join(body)}</g>'


def _arrow(points: str, x: int, y: int, color=S.INK, dashed=False) -> list[str]:
    return [S.path(points, fill="none", stroke=color, stroke_width=2,
                   stroke_dasharray="5 5" if dashed else None,
                   stroke_linecap="round", stroke_linejoin="round"),
            S.path(f"M{x - 7} {y - 4} L{x} {y} L{x - 7} {y + 4}",
                   fill="none", stroke=color, stroke_width=2,
                   stroke_linecap="round", stroke_linejoin="round")]


def _writing(x: int, y: int, widths: list[int], gap=12, color=S.GRID) -> list[str]:
    return [S.line(x, y + i * gap, x + w, y + i * gap,
                   stroke=color, stroke_width=1) for i, w in enumerate(widths)]


def _machine(x: int, y: int, scale=1) -> str:
    """A recognisable domestic sewing machine: arm, handwheel, needle, bed."""
    b = [S.path("M0 112 H174 V124 H0 Z", fill=PAPER2,
                stroke=S.INK, stroke_width=1.6),
         S.path("M18 112 V94 H62 V39 Q63 23 80 23 H137 Q157 23 157 44 V112 H127 V56 H88 V94 H101 V112 Z",
                fill=S.PAPER, stroke=S.INK, stroke_width=1.8,
                stroke_linejoin="round"),
         S.circle(156, 54, 19, fill=S.PAPER, stroke=S.INK, stroke_width=1.6),
         S.circle(156, 54, 10, fill="none", stroke=S.INK2, stroke_width=1),
         S.line(80, 59, 80, 105, stroke=S.INK, stroke_width=1.5),
         S.line(74, 105, 89, 105, stroke=S.INK, stroke_width=1.5),
         S.line(115, 23, 115, 10, stroke=S.INK, stroke_width=1.5),
         S.rect(108, 8, 14, 9, fill=S.PAPER, stroke=S.INK, stroke_width=1.3),
         S.circle(137, 80, 4, fill="none", stroke=S.INK2, stroke_width=1),
         S.path("M48 111 Q58 102 72 110 Q82 116 95 110", fill="none",
                stroke=S.DIF, stroke_width=1.5)]
    return _group(b, transform=f"translate({x} {y}) scale({scale})")


def _percurso(p: dict) -> tuple[str, list[dict]]:
    b = [S.text(53, 27, "O percurso da causa", size=17, family=S.SANS,
                weight="600"),
         S.path("M55 59 V49 H979 V59", fill="none", stroke=S.DIF,
                stroke_width=1.5),
         S.text(518, 43, "fase de conhecimento", size=13, fill=S.DIF,
                anchor="middle"),
         # One continuous folded folio, with the cover and sheet edges beneath.
         S.path("M48 96 L305 85 L552 92 L791 83 L985 95 L990 313 L791 307 L553 319 L306 310 L49 321 Z",
                fill=PAPER2, stroke=S.INK, stroke_width=1.4),
         S.path("M49 89 L305 78 L552 85 L791 76 L985 88 L987 306 L791 300 L553 312 L306 303 L49 314 Z",
                fill=S.PAPER, stroke=S.INK, stroke_width=1.2),
         S.path("M48 82 L305 71 L552 78 L791 69 L985 81 L985 299 L791 293 L553 305 L306 296 L48 307 Z",
                fill=S.PAPER, stroke=S.INK, stroke_width=1.8),
         S.line(306, 75, 306, 294, stroke=S.GRID, stroke_width=1),
         S.line(552, 82, 553, 302, stroke=S.GRID, stroke_width=1),
         S.line(791, 73, 791, 290, stroke=S.GRID, stroke_width=1)]
    # Stitching along the lower edge makes the stages one physical case file.
    b.append(S.path("M62 300 Q302 281 553 297 Q794 282 974 292",
                    fill="none", stroke=S.INK2, stroke_width=1))
    for x, y in [(98, 298), (196, 293), (405, 291), (647, 292), (887, 289)]:
        b.append(S.path(f"M{x - 4} {y - 3} q-2 15 7 12 q7 -6 -3 -9",
                        fill="none", stroke=S.INK2, stroke_width=1.2))
    # Pleadings: distinct pieces of paper converge on a contested statement.
    initial = [S.path("M0 0 H121 L137 16 V137 H0 Z", fill=S.PAPER,
                      stroke=S.DIF, stroke_width=1.8),
               S.path("M121 0 V16 H137", fill="none", stroke=S.DIF,
                      stroke_width=1.2),
               S.text(12, 28, "Petição inicial", size=15, family=S.SERIF,
                      fill=S.DIF, weight="600"),
               S.text(12, 51, "fatos + pedidos", size=11.5, fill=S.INK2)]
    initial += _writing(12, 68, [99, 108, 88, 102, 64], gap=11)
    initial.append(S.path("M14 125 q22 -7 41 0", fill="none", stroke=S.INK2,
                          stroke_width=1))
    b.append(_group(initial, transform="translate(71 113) rotate(-5 68 68)"))
    defense = [S.path("M0 0 H103 L116 13 V111 H0 Z", fill=S.PAPER,
                      stroke=S.INK, stroke_width=1.3),
               S.path("M103 0 V13 H116", fill="none", stroke=S.INK,
                      stroke_width=1),
               S.text(10, 26, "Contestação", size=14, family=S.SERIF),
               S.text(10, 46, "resposta do réu", size=11.5, fill=S.INK2)]
    defense += _writing(10, 61, [91, 84, 92, 60], gap=10)
    b.append(_group(defense, transform="translate(168 160) rotate(6 58 55)"))
    b += _arrow("M207 151 C252 119 300 127 347 169", 347, 169)
    b += _arrow("M283 221 C316 216 320 194 347 186", 347, 186)
    # The organisation leaf is a working minute with an actual selected line.
    b += [S.text(369, 130, "O que precisa ser decidido", size=14,
                 family=S.SERIF),
          S.line(367, 142, 523, 142, stroke=S.GRID, stroke_width=1),
          S.text(374, 175, "fatos controvertidos", size=15, family=S.SERIF),
          S.path("M368 185 Q446 180 526 184", fill="none", stroke=S.INK,
                 stroke_width=1.4),
          S.text(374, 207, "provas necessárias", size=14, family=S.SERIF),
          S.text(373, 243, "Saneamento", size=11.5, fill=S.INK2)]
    # Evidence is on receipts pinned into the same folio, not a text box.
    b += _arrow("M526 181 C552 181 568 190 591 190", 591, 190)
    receipt = [S.path("M0 0 H110 V105 L102 101 L94 105 L86 101 L78 105 L70 101 L62 105 L54 101 L46 105 L38 101 L30 105 L22 101 L14 105 L6 101 L0 105 Z",
                      fill=S.PAPER, stroke=S.INK, stroke_width=1.2),
               S.text(11, 22, "Recibos", size=13, family=S.SERIF),
               S.line(10, 29, 97, 29, stroke=S.INK2, stroke_width=.8)]
    receipt += _writing(11, 46, [85, 73, 86, 59], gap=12)
    b.append(_group(receipt, transform="translate(619 128) rotate(7 55 52)"))
    b.append(S.path("M628 125 q-9 -11 -2 -15 q7 -3 8 5 l2 17 q0 7 -6 5 l-3 -15",
                    fill="none", stroke=S.INK2, stroke_width=1.2))
    b += [S.text(617, 257, "Contrato · documentos · prova", size=11.5,
                 fill=S.INK2, anchor="middle")]
    b += _arrow("M736 187 C763 180 788 177 818 177", 818, 177)
    # The judgment shares the petition's blue thread: it answers that demand.
    judgment = [S.path("M0 0 H124 L140 16 V145 H0 Z", fill=S.PAPER,
                       stroke=S.INK, stroke_width=1.4),
                S.path("M124 0 V16 H140", fill="none", stroke=S.INK,
                       stroke_width=1),
                S.text(12, 31, "Sentença", size=16, family=S.SERIF,
                       weight="600"),
                S.text(12, 54, "resposta à demanda", size=11.5, fill=S.INK2)]
    judgment += _writing(12, 71, [114, 98, 112], gap=11)
    judgment += [S.line(12, 113, 121, 113, stroke=S.DIF, stroke_width=2),
                 S.path("M70 130 q16 -9 23 -2 t24 -2", fill="none",
                        stroke=S.INK2, stroke_width=1)]
    b.append(_group(judgment, transform="translate(821 111) rotate(-3 70 72)"))
    # The shortcut lies above the evidentiary material; it has a condition.
    b += _arrow("M487 119 C574 66 728 66 846 111", 846, 111,
                color=S.CONC, dashed=True)
    b.append(S.text(665, 95, "julgamento antecipado, quando cabível", size=11.5,
                    fill=S.CONC, anchor="middle"))
    # Demand's perimeter is a fine continuous thread, from first request to decree.
    b.append(S.path("M85 263 Q413 286 827 264", fill="none", stroke=S.DIF,
                    stroke_width=1, stroke_dasharray="2 5"))
    b.append(S.text(483, 283, "os pedidos delimitam a resposta", size=11.5,
                    fill=S.DIF, anchor="middle"))
    b += _arrow("M960 227 C985 227 1010 227 1053 227", 1053, 227)
    b += [S.text(1008, 247, "cumprimento", size=11.5, fill=S.INK2,
                 anchor="middle"),
          S.text(1008, 261, "do decidido", size=11.5, fill=S.INK2,
                 anchor="middle")]
    phases = [
        ("postular", 176, "Postular", "Petição e resposta põem a causa em discussão.", 53, 92, 244, 211),
        ("organizar", 430, "Organizar", "O saneamento delimita questões e provas.", 311, 112, 237, 181),
        ("instruir", 670, "Instruir", "A prova esclarece os fatos que seguem controvertidos.", 559, 119, 228, 173),
        ("decidir", 891, "Decidir", "A decisão responde à demanda nos limites do pedido.", 797, 112, 185, 178),
    ]
    # A selection traces dependencies in the object, retaining the complete base map.
    traces = {
        "postular": [S.path("M65 111 L200 98 L216 250 L78 263 Z M170 155 L290 168 L278 283 L160 271 Z",
                            fill="none", stroke=S.DIF, stroke_width=2.5)]
                    + _arrow("M207 151 C252 119 300 127 347 169", 347, 169, color=S.DIF)
                    + _arrow("M283 221 C316 216 320 194 347 186", 347, 186, color=S.DIF),
        "organizar": _arrow("M207 151 C252 119 300 127 347 169", 347, 169, color=S.DIF)
                     + _arrow("M283 221 C316 216 320 194 347 186", 347, 186, color=S.DIF)
                     + [S.path("M365 155 H529 V217 H365", fill="none", stroke=S.DIF, stroke_width=2.5)]
                     + _arrow("M526 181 C552 181 568 190 591 190", 591, 190, color=S.DIF)
                     + _arrow("M487 119 C574 66 728 66 846 111", 846, 111, color=S.CONC, dashed=True),
        "instruir": _arrow("M526 181 C552 181 568 190 591 190", 591, 190, color=S.DIF)
                    + [S.path("M617 122 L739 135 L726 242 L605 228 Z", fill="none", stroke=S.DIF, stroke_width=2.5)]
                    + _arrow("M736 187 C763 180 788 177 818 177", 818, 177, color=S.DIF),
        "decidir": [S.path("M85 263 Q413 286 827 264", fill="none", stroke=S.DIF, stroke_width=3),
                    S.path("M829 222 L946 216 M829 232 L929 227 M829 242 L940 236", fill="none", stroke=S.DIF, stroke_width=2),
                    S.path("M818 109 L959 102 L967 255 L824 263 Z", fill="none", stroke=S.DIF, stroke_width=2.5)]
                   + _arrow("M960 227 C985 227 1010 227 1053 227", 1053, 227, color=S.DIF),
    }
    objects = []
    for oid, x, label, description, hx, hy, hw, hh in phases:
        b.append(_group(traces[oid], data_object_state=oid, data_state="active", visibility="hidden"))
        tab = [S.path(f"M{x-77} 320 H{x+77} V352 H{x-77} Z", fill=S.PAPER,
                      stroke=S.INK2, stroke_width=1, class_="paper-tab"),
               S.text(x, 342, label, size=16, family=S.SANS, weight="600", anchor="middle"),
               _hit(hx, hy, hw, hh)]
        b.append(_group(tab, data_object=oid, role="button", tabindex="0",
                        aria_label=label + ": " + description))
        objects.append({"id": oid, "label": label, "description": description})
    b += [S.text(103, 374, "partes e terceiros", size=11.5, fill=S.INK2),
          S.text(429, 374, "saneamento", size=11.5, fill=S.INK2, anchor="middle"),
          S.text(670, 374, "prova", size=11.5, fill=S.INK2, anchor="middle"),
          S.line(175, 397, 902, 397, stroke=S.GRID, stroke_width=1),
          S.line(175, 392, 175, 402, stroke=S.GRID, stroke_width=1),
          S.line(902, 392, 902, 402, stroke=S.GRID, stroke_width=1),
          S.rect(411, 386, 259, 22, fill=S.PAPER),
          S.text(540, 401, "comunicação dos atos · prazos", size=11.5,
                 fill=S.INK2, anchor="middle"),
          S.text(92, 101, "esta aula", size=11.5, fill=S.DIF)]
    return S.svg(1080, 416, p.get("title") or "O percurso da causa: a petição e a resposta convergem no saneamento; a prova conduz à decisão; o julgamento antecipado pode abreviar o percurso", b), objects


def _equivalent_sheet() -> list[str]:
    """A folded valuation, distinctly different from a rental receipt; no fictional sum."""
    return [S.path("M425 148 H568 L590 170 V284 H425 Z", fill=S.PAPER,
                   stroke=S.INK, stroke_width=1.2),
            S.path("M568 148 V170 H590", fill="none", stroke=S.INK, stroke_width=1),
            S.text(441, 195, "Estimativa da máquina", size=11, fill=S.INK2),
            S.rect(450, 211, 118, 45, fill=PAPER2, stroke=S.INK2, stroke_width=1),
            S.circle(510, 233, 17, fill="none", stroke=S.INK2, stroke_width=1),
            S.text(510, 238, "R$", size=14, family=S.SERIF, anchor="middle"),
            S.line(442, 272, 572, 272, stroke=S.GRID, stroke_width=1)]


def _pedidos(p: dict) -> tuple[str, list[dict]]:
    claimant, defendant = p.get("claimant", "Cecília"), p.get("defendant", "Oficina Horizonte")
    b = [# Prancheta and offset carbon-copy sheet edges.
         S.path("M71 43 Q71 28 86 28 H648 Q662 28 662 43 V365 Q662 380 647 380 H86 Q71 380 71 365 Z",
                fill=PAPER2, stroke=S.INK, stroke_width=1.7),
         S.path("M104 68 H633 V356 H104 Z", fill=PAPER2, stroke=S.INK2,
                stroke_width=.7),
         S.path("M98 62 H627 V350 H98 Z", fill=S.PAPER, stroke=S.INK2,
                stroke_width=.8),
         S.path("M92 56 H621 V344 H92 Z", fill=S.PAPER, stroke=S.INK,
                stroke_width=1.2),
         S.rect(295, 18, 117, 43, rx=5, fill=PAPER2, stroke=S.INK,
                stroke_width=1.5),
         S.rect(321, 12, 65, 17, rx=7, fill=S.PAPER, stroke=S.INK,
                stroke_width=1.4),
         S.line(305, 50, 402, 50, stroke=S.INK2, stroke_width=1),
         S.text(356, 89, f"{claimant} × {defendant}", size=16,
                family=S.SERIF, anchor="middle"),
         S.line(123, 103, 590, 103, stroke=S.GRID, stroke_width=1),
         S.text(137, 130, "Entrega da máquina de costura", size=15,
                family=S.SERIF),
         _machine(142, 148, 1.03),
         S.text(231, 305, "primeira prestação", size=10, fill=S.INK2,
                anchor="middle"),
         ]
    # A separate judicial folio receives the tracings from the requested objects.
    b += [S.path("M792 67 H996 L1015 86 V338 H792 Z", fill=PAPER2,
                 stroke=S.INK2, stroke_width=.8),
          S.path("M785 60 H989 L1008 79 V331 H785 Z", fill=S.PAPER,
                 stroke=S.INK, stroke_width=1.4),
          S.path("M989 60 V79 H1008", fill="none", stroke=S.INK,
                 stroke_width=1),
          S.text(896, 101, "Decisão", size=19, family=S.SERIF,
                 anchor="middle"),
          S.line(811, 117, 981, 117, stroke=S.GRID, stroke_width=1)]
    for mode in ("ambos", "subsidiario", "qualquer"):
        layer = []
        if mode == "ambos":
            layer += [S.path("M423 151 L584 143 L593 279 L585 275 L577 280 L569 276 L561 281 L553 277 L545 282 L537 278 L529 283 L521 279 L513 284 L505 280 L497 285 L489 281 L481 286 L473 282 L465 287 L457 283 L449 288 L441 284 L432 289 Z",
                             fill=PAPER2, stroke=S.INK, stroke_width=1.2),
                      S.line(437, 185, 574, 178, stroke=S.GRID, stroke_width=1)]
            layer += _writing(442, 220, [129, 103, 123], gap=13)
            layer += [S.text(442, 172, "Recibos de aluguel", size=13,
                             family=S.SERIF),
                      S.text(514, 305, "reembolso do aluguel", size=10,
                             fill=S.INK2, anchor="middle"),
                      S.text(813, 169, "Entrega da máquina", size=15,
                             family=S.SERIF, fill=S.DIF),
                      S.text(813, 224, "+ reembolso", size=15,
                             family=S.SERIF, fill=S.DIF)]
            layer += _arrow("M325 190 C355 108 700 100 803 169", 803, 169,
                            color=S.DIF)
            layer += _arrow("M591 237 C675 250 735 224 803 224", 803, 224,
                            color=S.DIF)
            layer += [S.path("M812 180 H978 M812 235 H958", fill="none",
                              stroke=S.DIF, stroke_width=1.2),
                      S.text(895, 364, "duas prestações", size=12,
                             fill=S.DIF, anchor="middle")]
        elif mode == "subsidiario":
            layer += _equivalent_sheet()
            layer += [S.text(441, 173, "Equivalente em dinheiro", size=12,
                             family=S.SERIF),
                      S.text(513, 306, "pedido de reserva", size=10,
                             fill=S.CONC, anchor="middle"),
                      S.text(813, 168, "1. Entrega", size=16,
                             family=S.SERIF, fill=S.DIF),
                      S.text(813, 214, "2. Equivalente", size=15,
                             family=S.SERIF, fill=S.CONC),
                      S.text(813, 237, "se o primeiro não for acolhido", size=9,
                             fill=S.CONC)]
            layer += _arrow("M325 190 C355 108 690 96 803 164", 803, 164,
                            color=S.DIF)
            layer += _arrow("M590 240 C669 257 743 212 803 212", 803, 212,
                            color=S.CONC, dashed=True)
            layer += [S.path("M812 181 H948", fill="none", stroke=S.DIF,
                              stroke_width=1.2),
                      S.text(895, 364, "uma ordem de preferência", size=12,
                             fill=S.DIF, anchor="middle")]
        else:
            layer += _equivalent_sheet()
            layer += [S.text(441, 173, "Equivalente em dinheiro", size=12,
                             family=S.SERIF),
                      S.text(513, 306, "sem preferência", size=10,
                             fill=S.INK2, anchor="middle"),
                      S.text(813, 165, "Entrega", size=16, family=S.SERIF,
                             fill=S.DIF),
                      S.text(861, 192, "ou", size=14, family=S.SERIF,
                             fill=S.INK2),
                      S.text(813, 219, "Equivalente", size=16,
                             family=S.SERIF, fill=S.DIF)]
            layer += [S.path("M325 190 C355 108 600 130 704 195 M590 241 C649 245 674 218 704 195",
                              fill="none", stroke=S.DIF, stroke_width=2,
                              stroke_linecap="round")]
            layer += _arrow("M704 195 C737 187 765 188 803 188", 803, 188,
                            color=S.DIF)
            layer += [S.path("M986 151 h8 v79 h-8", fill="none", stroke=S.DIF,
                              stroke_width=1.5),
                      S.text(895, 364, "uma das prestações", size=12,
                             fill=S.DIF, anchor="middle")]
        b.append(_group(layer, data_variant=mode,
                        visibility="visible" if mode == "ambos" else "hidden"))
    return S.svg(1080, 416, p.get("title") or "Pedidos em sobreposição: os traços saem da máquina e do segundo pedido e chegam às prestações que o juízo pode conceder", b), []


# ── the petition sheet shared by the "peticao" (chapter 3) and "revisao" (chapter 5) instruments ─────────────────────
SHEET = (200, 28, 770, 414)          # x0, y0, x1, y1
ROW = {"juizo": (44, 80), "partes": (90, 140), "causa": (150, 222), "pedido": (232, 266), "valor": (276, 322),
       "provas": (328, 358), "audiencia": (362, 394)}


def _torn(x0, x1, y, depth=6, step=10, down=True) -> str:
    """A torn edge as a polyline from x0 to x1 along y."""
    pts, x, k = [f"M{x0} {y}"], x0, 0
    while x < x1:
        x = min(x + step, x1)
        pts.append(f"L{x} {y + (depth if k % 2 == 0 else 0) * (1 if down else -1)}")
        k += 1
    return " ".join(pts)


def _tab(x, y, label, key=None) -> list[str]:
    return [S.rect(x, y - 13, 30, 26, fill=S.PAPER, stroke=S.INK2, stroke_width=1, class_="paper-tab"),
            S.text(x + 15, y + 5, label, size=13, anchor="middle")]


def _sheet(blank_value: bool, claimant: str, defendant: str) -> list[str]:
    x0, y0, x1, y1 = SHEET
    b = [S.path(f"M{x0 + 8} {y0 + 7} H{x1 + 8} L{x1 + 31} {y0 + 30} V{y1 + 7} H{x0 + 8} Z", fill=PAPER2, stroke=S.INK2,
                stroke_width=.8),
         S.path(f"M{x0} {y0} H{x1 - 23} L{x1} {y0 + 23} V{y1} H{x0} Z", fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
         S.path(f"M{x1 - 23} {y0} V{y0 + 23} H{x1}", fill="none", stroke=S.INK, stroke_width=1),
         S.text((x0 + x1) / 2 - 10, 66, "Ao juízo competente", size=17, family=S.SERIF, anchor="middle"),
         S.line(x0 + 26, 80, x1 - 40, 80, stroke=S.GRID, stroke_width=1),
         S.text(x0 + 30, 112, f"{claimant}, em face de {defendant}, endereço conhecido;", size=15.5, family=S.SERIF),
         S.text(x0 + 30, 134, "CPF/CNPJ da ré desconhecido.", size=15.5, family=S.SERIF),
         S.text(x0 + 30, 172, "Entregou a máquina de costura para conserto.", size=15.5, family=S.SERIF),
         S.text(x0 + 30, 194, "O prazo combinado venceu sem devolução.", size=15.5, family=S.SERIF),
         S.text(x0 + 30, 216, "Alugou outra máquina e guardou os recibos.", size=15.5, family=S.SERIF),
         S.text(x0 + 30, 254, "Pede a entrega da máquina e o reembolso do aluguel.", size=15.5, family=S.SERIF),
         S.text(x0 + 30, 306, "Valor da causa:", size=15.5, family=S.SERIF)]
    if blank_value:   # the blank has a torn edge, not a form field
        b.append(S.path(_torn(x0 + 160, x1 - 34, 290, 5, 10) + f" V{318} H{x0 + 160} Z", fill=PAPER2, stroke=S.GRID, stroke_width=1))
    else:
        b.append(S.line(x0 + 160, 309, x1 - 34, 309, stroke=S.GRID, stroke_width=1))
    b += [S.text(x0 + 30, 346, "Provas: recibos de aluguel e comprovante da entrega.", size=15.5, family=S.SERIF),
          S.text(x0 + 30, 380, "Tem interesse na audiência de conciliação.", size=15.5, family=S.SERIF),
          S.path(f"M{x1 - 190} {y1 - 20} q20 -10 30 -1 t30 -3", fill="none", stroke=S.INK2, stroke_width=1.2)]
    return b


def _row_frame(key, stroke=S.DIF, sw=2, wash=False) -> str:
    y0, y1 = ROW[key]
    return S.rect(SHEET[0] + 10, y0 - 3, SHEET[2] - SHEET[0] - 38, y1 - y0 + 6, fill="none", stroke=stroke, stroke_width=sw)


def _peticao(p: dict) -> tuple[str, list[dict]]:
    claimant, defendant = p.get("claimant", "Cecília"), p.get("defendant", "Oficina Horizonte")
    b = _sheet(False, claimant, defendant)
    reqs = [("juizo", "I", "Juízo", "Indicar o juízo a que a petição se dirige."),
            ("partes", "II", "Partes", "Individualizar e localizar quem litiga."),
            ("causa", "III", "Causa de pedir", "Narrar os fatos e seus fundamentos jurídicos."),
            ("pedido", "IV", "Pedido", "Dizer a providência e o bem pretendidos."),
            ("valor", "V", "Valor da causa", "Dar medida econômica ao que se põe em juízo."),
            ("provas", "VI", "Provas", "Indicar com o que se demonstram os fatos."),
            ("audiencia", "VII", "Audiência", "Optar pela audiência de conciliação ou mediação.")]
    notes = {"juizo": "o destinatário", "partes": "quem litiga", "causa": "o que aconteceu e por quê",
             "pedido": "o que se quer do juiz", "valor": "a medida da causa", "provas": "como se demonstra",
             "audiencia": "espaço para acordo"}
    objects = []
    for key, rom, label, desc in reqs:
        y0, y1 = ROW[key]
        yc = (y0 + y1) / 2
        state = [_row_frame(key), S.path(f"M{SHEET[2] + 2} {yc} H{SHEET[2] + 44}", fill="none", stroke=S.DIF, stroke_width=2),
                 S.text(SHEET[2] + 54, yc + 5, notes[key], size=15, family=S.SERIF, fill=S.DIF)]
        b.append(_group(state, data_object_state=key, data_state="active", visibility="hidden"))
        tab = _tab(SHEET[0] - 42, yc, rom) + [_hit(SHEET[0] - 46, y0 - 3, SHEET[2] - SHEET[0] + 40, y1 - y0 + 6)]
        b.append(_group(tab, data_object=key, role="button", tabindex="0", aria_label=f"{rom} · {label}: {desc}"))
        objects.append({"id": key, "label": label, "description": desc})
    return S.svg(1080, 432, p.get("title") or "A petição inicial de Cecília, com seus sete requisitos", b), objects


def _clip(x, y) -> list[str]:
    return [S.path(f"M{x} {y} v-20 q0 -8 7 -8 t7 8 v24 q0 5 -5 5 t-5 -5 v-18", fill="none", stroke=S.INK2, stroke_width=1.4,
                   stroke_linecap="round")]


def _scrap_path(x, y, w=210, h=96) -> str:
    """A scrap of paper: straight top and sides, torn bottom."""
    pts, xx, k = [f"M{x} {y} H{x + w} V{y + h}"], x + w, 0
    while xx > x:
        xx = max(xx - 10, x)
        pts.append(f"L{xx} {y + h - (6 if k % 2 == 0 else 0)}")
        k += 1
    return " ".join(pts) + " Z"


def _scrap(color=S.INK) -> list[str]:
    x, y = 810, 332
    return [S.path(_scrap_path(x, y), fill=PAPER2, stroke=color, stroke_width=1.4),
            S.text(x + 18, y + 44, "Reparação de", size=16, family=S.SERIF, fill=color),
            S.text(x + 18, y + 68, "dano novo", size=16, family=S.SERIF, fill=color)] + _clip(x + 40, y + 10)


def _revisao(p: dict) -> tuple[str, list[dict]]:
    claimant, defendant = p.get("claimant", "Cecília"), p.get("defendant", "Oficina Horizonte")
    b = _sheet(True, claimant, defendant) + _scrap()
    states = {
        "valor": [S.path(_torn(SHEET[0] + 160, SHEET[2] - 34, 290, 5, 10) + " V318 H360 Z", fill=S.PAPER, stroke=S.DIF,
                         stroke_width=1.4),
                  S.text(SHEET[0] + 172, 311, "Valor atribuído à causa", size=15.5, family=S.SERIF, fill=S.DIF),
                  S.path(f"M{SHEET[2] + 2} 304 H{SHEET[2] + 44}", fill="none", stroke=S.DIF, stroke_width=2),
                  S.text(SHEET[2] + 54, 309, "completa a peça", size=15, family=S.SERIF, fill=S.DIF)],
        "cpf": [_row_frame("partes", S.DIF, 2),
                S.path(f"M{SHEET[2] + 2} 115 H{SHEET[2] + 44}", fill="none", stroke=S.DIF, stroke_width=2),
                S.text(SHEET[2] + 54, 112, "a falta admite exame", size=15, family=S.SERIF, fill=S.DIF),
                S.text(SHEET[2] + 54, 133, "das condições de citação", size=15, family=S.SERIF, fill=S.DIF)],
        "novo": [S.path(_scrap_path(810, 332), fill="none", stroke=S.CONC, stroke_width=2.4),
                 S.path(f"M806 372 C788 372 790 262 {SHEET[2] + 4} 254", fill="none", stroke=S.CONC, stroke_width=2),
                 S.text(836, 306, "amplia o que se pede", size=15, family=S.SERIF, fill=S.CONC)],
    }
    objects = []
    for number, (oid, tx, ty, hx, hy, hw, hh, label, description) in enumerate([
        ("valor", SHEET[0] - 42, 303, SHEET[0] - 46, 272, 580, 54, "Valor da causa omitido", "Suprir a indicação do valor da causa."),
        ("cpf", SHEET[0] - 42, 115, SHEET[0] - 46, 88, 580, 54, "Identificação desconhecida", "Examinar a falta do CPF ou CNPJ quando o endereço é conhecido."),
        ("novo", 770 + 8, 230, 796, 322, 240, 106, "Novo pedido", "Distinguir a ampliação do pedido da correção formal da inicial."),
    ], 1):
        b.append(_group(states[oid], data_object_state=oid, data_state="active", visibility="hidden"))
        tab = _tab(tx, ty, str(number)) if oid != "novo" else []
        b.append(_group(tab + [_hit(hx, hy, hw, hh)], data_object=oid, role="button", tabindex="0", aria_label=label + ": " + description))
        objects.append({"id": oid, "label": label, "description": description})
    # the third tab sits on the scrap's corner
    b.append(S.rect(982, 318, 30, 26, fill=S.PAPER, stroke=S.INK2, stroke_width=1))
    b.append(S.text(997, 336, "3", size=13, anchor="middle"))
    return S.svg(1080, 432, p.get("title") or "A inicial de Cecília em revisão: um valor em branco, o CPF da ré desconhecido e um pedido novo em papel avulso", b), objects


def _janelas(p: dict) -> tuple[str, list[dict]]:
    """The demand's three windows (art. 329) on the autos seen edge-on: before the citação, until the saneamento, after."""
    X0, X1, C, SAN = 60, 1020, 360, 700
    Y0, Y1 = 120, 190
    b = [S.rect(X0, Y0, X1 - X0, Y1 - Y0, fill=PAPER2, stroke=S.INK, stroke_width=1.5)]
    k = X0 + 4
    while k < X1 - 2:
        b.append(S.line(k, Y0 + 1, k, Y1 - 1, stroke=S.GRID, stroke_width=1))
        k += 4
    for x, lab in ((C, "CITAÇÃO"), (SAN, "SANEAMENTO")):
        b += [S.rect(x - 8, Y0 - 22, 16, Y1 - Y0 + 44, fill=S.PAPER, stroke=S.INK, stroke_width=1.8),
              S.text(x, Y1 + 42, lab, size=13, anchor="middle", weight="600")]
    b += [S.text(X0, Y1 + 42, "PETIÇÃO", size=13, weight="600"),
          S.text(X1, Y1 + 42, "SENTENÇA", size=13, weight="600", anchor="end")]
    wins = [("antes", X0, C - 8, "ANTES DA CITAÇÃO", "art. 329, I"),
            ("ate", C + 8, SAN - 8, "ATÉ O SANEAMENTO", "art. 329, II"),
            ("depois", SAN + 8, X1, "DEPOIS DO SANEAMENTO", "art. 329 · art. 190")]
    for oid, a, c, head, art in wins:
        b += [S.line(a + 2, 22, c - 2, 22, stroke=S.CONC, stroke_width=1.6), S.line(a + 2, 22, a + 2, 30, stroke=S.CONC, stroke_width=1.6),
              S.line(c - 2, 22, c - 2, 30, stroke=S.CONC, stroke_width=1.6),
              S.text(a + 10, 50, head, size=14, family=S.SANS, fill=S.CONC, weight="600"),
              S.text(a + 10, 69, art, size=12.5, fill=S.MUTED)]

    def slip(x, y, color=S.INK, fill=S.PAPER):
        return [S.path(f"M{x} {y} h88 l12 12 v62 h-100 Z", fill=fill, stroke=color, stroke_width=1.8),
                S.path(f"M{x + 88} {y} v12 h12", fill="none", stroke=color, stroke_width=1.2),
                S.text(x + 10, y + 34, "dano novo", size=15, family=S.SERIF, fill=color),
                S.line(x + 10, y + 46, x + 82, y + 46, stroke=S.GRID, stroke_width=1),
                S.line(x + 10, y + 58, x + 70, y + 58, stroke=S.GRID, stroke_width=1)]
    states = {
        "antes": slip(176, 98, S.DIF) + [S.path("M120 138 H168", fill="none", stroke=S.DIF, stroke_width=2.4),
                                         S.text(60, 264, "entra sem o consentimento da ré", size=16, family=S.SERIF, fill=S.DIF)],
        "ate": slip(500, 98, S.DIF) + [S.rect(626, 110, 56, 28, fill=S.PAPER, stroke=S.DIF, stroke_width=1.6),
                                         S.text(654, 129, "ré: ok", size=13, anchor="middle", fill=S.DIF),
                                         S.path("M606 138 H622", fill="none", stroke=S.DIF, stroke_width=2.4),
                                         S.text(368, 264, "entra com o consentimento da ré e quinze dias para ela responder", size=16,
                                                family=S.SERIF, fill=S.DIF)],
        "depois": slip(584, 98, S.CONC, PAPER2) + [S.path(f"M{SAN - 6} 100 V210", fill="none", stroke=S.CONC, stroke_width=5),
                                                      S.path("M706 104 C716 80 790 80 800 106", fill="none", stroke=S.CONC, stroke_width=2,
                                                             stroke_dasharray="6 5"),
                                                      S.path("M792 98 L800 108 L808 98", fill="none", stroke=S.CONC, stroke_width=2),
                                                      S.rect(760, 112, 150, 62, fill="none", stroke=S.CONC, stroke_width=1.8,
                                                             stroke_dasharray="6 4"),
                                                      S.text(835, 139, "só por acordo", size=15, family=S.SERIF, fill=S.CONC, anchor="middle"),
                                                      S.text(835, 159, "art. 190", size=12.5, fill=S.CONC, anchor="middle"),
                                                      S.text(520, 264, "fechada para o pedido unilateral", size=16, family=S.SERIF,
                                                             fill=S.CONC)],
    }
    objects = []
    for oid, a, c, head, art in wins:
        b.append(_group(states[oid], data_object_state=oid, data_state="active", visibility="hidden"))
        b.append(_group([_hit(a, 16, c - a, 190)], data_object=oid, role="button", tabindex="0", aria_label=head))
        objects.append({"id": oid, "label": head.title(), "description": head})
    return S.svg(1080, 284, p.get("title") or "As três janelas do pedido de Cecília: antes da citação, até o saneamento e depois dele", b), objects


def build(p: dict) -> tuple[str, list[dict]]:
    builders = {"percurso": _percurso, "pedidos": _pedidos, "revisao": _revisao, "peticao": _peticao, "janelas": _janelas}
    mode = p.get("mode")
    if mode not in builders:
        raise ValueError("abertura_civil: mode must be percurso, pedidos, revisao, peticao or janelas")
    return builders[mode](p)
