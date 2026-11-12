"""abertura_civil: physical tracings and petition sheets for Aula 01.

Params (facts, never coordinates):
  mode       percurso | pedidos | peticao | revisao | janelas | fecho (required)
  title      optional accessible title
  claimant   optional name, default Cecília
  defendant  optional name, default Oficina Horizonte

The lower drawings are static and fully readable. `pedidos` relates the same
objects by independent landings, a dependency and a fork, without frames;
`peticao` annotates the seven requisites; `revisao`
separates repair of the same initial from a new claim; `janelas` progressively
secures the demand's thread; `fecho` returns the running facts to the limits of
the judgment. None invents an amount, date, folha number or outcome. Art. 326's
equivalent-money formulations are hypothetical, not a substantive entitlement.
All flat folios have unturned corners: the site's fold belongs to backstage.
The legacy `percurso` mode preserves its object contract for existing callers.

Contract:
  build(p) -> (svg, objects). Lower modes return objects=[]; no buttons, hidden
  states, title elements or tooltip targets. House colour tokens support dark
  mode. All paths are emitted here, never hand-written in the shell source.
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


def _paper(x, y, w, h, color=S.INK, under=True) -> list[str]:
    """A flat folio with unturned corners. Offset edges show thickness."""
    b = []
    if under:
        b.append(S.rect(x + 5, y + 5, w, h, fill=PAPER2,
                        stroke=S.INK2, stroke_width=.7))
    b.append(S.rect(x, y, w, h, fill=S.PAPER, stroke=color,
                    stroke_width=1.3))
    return b


def _receipt(x, y, w=100, h=110) -> list[str]:
    """A rental receipt, with its cut edge and handwritten signature."""
    bottom = f"M{x} {y} H{x+w} V{y+h}"
    for i in range(10, w + 1, 10):
        bottom += f" L{x+w-i} {y+h-(4 if i % 20 else 0)}"
    bottom += " Z"
    b = [S.path(bottom, fill=S.PAPER, stroke=S.INK, stroke_width=1.2),
         S.text(x + 11, y + 25, "Aluguel", size=14, family=S.SERIF),
         S.line(x + 11, y + 34, x + w - 11, y + 34, stroke=S.INK2,
                stroke_width=.7)]
    b += _writing(x + 11, y + 49, [w - 22, w - 35, w - 24], gap=11)
    b.append(S.path(f"M{x+14} {y+h-15} q18 -8 24 -1 t23 -2", fill="none",
                    stroke=S.INK2, stroke_width=.9))
    return b


def _money(x, y, w=110, h=68) -> list[str]:
    """A monetary equivalent, without a fabricated amount."""
    return [S.rect(x + 4, y + 5, w, h, fill=PAPER2, stroke=S.INK2,
                   stroke_width=.7),
            S.rect(x, y, w, h, fill=S.PAPER, stroke=S.INK, stroke_width=1.2),
            S.path(f"M{x+14} {y+7} H{x+w-14} q0 8 7 8 V{y+h-15} q-7 0 -7 8 H{x+14} q0 -8 -7 -8 V{y+15} q7 0 7 -8 Z",
                   fill="none", stroke=S.INK2, stroke_width=.7),
            S.circle(x + w / 2, y + h / 2, 19, fill="none",
                     stroke=S.INK2, stroke_width=.9),
            S.text(x + w / 2, y + h / 2 + 6, "R$", size=19,
                   family=S.SERIF, anchor="middle")]


def _small_arrow(points, x, y, color=S.DIF, dashed=False) -> list[str]:
    return [S.path(points, fill="none", stroke=color, stroke_width=1.8,
                   stroke_dasharray="4 4" if dashed else None,
                   stroke_linecap="round", stroke_linejoin="round"),
            S.path(f"M{x-4} {y-7} L{x} {y} L{x+4} {y-7}",
                   fill="none", stroke=color, stroke_width=1.8,
                   stroke_linecap="round", stroke_linejoin="round")]


def _pedidos(p: dict) -> tuple[str, list[dict]]:
    """One desk drawing: two landings, a dependency, then an unranked fork.

    The second and third are hypothetical formulations under art. 326, not
    statements about a substantive right to replace this machine by money.
    The blue paths describe examination or the author's preference, never a
    promised award. Sources: Marinoni v.2 pp.161–163; CPC arts.326 and327.
    """
    b = [S.text(31, 29, "Cumulação simples", size=21, family=S.SERIF,
                weight="600"),
         S.text(386, 29, "Pedido subsidiário", size=21, family=S.SERIF,
                weight="600"),
         S.text(755, 29, "Sem preferência", size=21, family=S.SERIF,
                weight="600")]
    # Two claims arrive independently at the judge's examination. Their two
    # landing points remain distinct even though they share the same line.
    b += [_machine(35, 86, .72)]
    b += _receipt(224, 77, 91, 110)
    b += _small_arrow("M97 177 C97 220 84 218 84 256", 84, 256)
    b += _small_arrow("M270 190 C270 223 278 224 278 256", 278, 256)
    b += [S.line(50, 269, 312, 269, stroke=S.DIF, stroke_width=1.8),
          S.circle(84, 269, 3, fill=S.DIF),
          S.circle(278, 269, 3, fill=S.DIF),
          S.text(35, 217, "entrega", size=15, family=S.SERIF),
          S.text(188, 217, "reembolso", size=15, family=S.SERIF),
          S.text(181, 302, "ambos podem ser acolhidos", size=17,
                 family=S.SERIF, anchor="middle"),
          S.text(31, 339, "art. 327", size=13, fill=S.INK2)]
    # The reserve lies physically behind the first landing. Its route begins
    # at that landing and needs its failure before the second examination.
    b += [_machine(386, 84, .72)]
    b += _money(579, 152, 101, 65)
    b += _small_arrow("M448 176 V253", 448, 253)
    b += [S.text(429, 230, "1", size=16, fill=S.DIF),
          S.line(410, 269, 491, 269, stroke=S.DIF, stroke_width=1.8),
          S.circle(448, 269, 3, fill=S.DIF)]
    b += _small_arrow("M448 269 C492 269 508 233 550 233 H610 Q632 233 632 252",
                       632, 252, color=S.CONC, dashed=True)
    b += [S.line(590, 269, 675, 269, stroke=S.CONC, stroke_width=1.8),
          S.text(652, 248, "2", size=16, fill=S.CONC),
          S.text(540, 302, "se o principal não for acolhido", size=17,
                 family=S.SERIF, anchor="middle"),
          S.text(386, 339, "art. 326, caput", size=13, fill=S.INK2)]
    # A true fork has no ordinal or preferred branch. Only one of its two
    # ends needs to be fulfilled to satisfy this hypothetical formulation.
    b += [S.circle(902, 73, 3.5, fill=S.PAPER, stroke=S.DIF,
                   stroke_width=1.5),
          S.path("M902 77 V94 C902 111 819 102 819 130 M902 94 C902 111 987 102 987 146",
                 fill="none", stroke=S.DIF, stroke_width=1.8,
                 stroke_linecap="round"),
          S.path("M815 123 l4 7 l4 -7 M983 139 l4 7 l4 -7", fill="none",
                 stroke=S.DIF, stroke_width=1.8),
          S.text(902, 138, "ou", size=18, family=S.SERIF,
                 fill=S.DIF, anchor="middle"),
          _machine(758, 139, .72)]
    b += _money(936, 163, 103, 65)
    b += [S.text(820, 260, "máquina", size=15, family=S.SERIF,
                 anchor="middle"),
          S.text(987, 260, "equivalente", size=15, family=S.SERIF,
                 anchor="middle"),
          S.text(904, 302, "qualquer um satisfaz a autora", size=17,
                 family=S.SERIF, anchor="middle"),
          S.text(755, 339, "art. 326, parágrafo único", size=13,
                 fill=S.INK2),
          S.text(386, 388, "O equivalente é uma formulação hipotética: exige fundamento no direito material.",
                 size=14.5, family=S.SERIF, fill=S.INK2)]
    return S.svg(1080, 416, p.get("title") or
                 "Uma relação desenhada para cada formulação: entrega e reembolso chegam independentes ao julgamento; o equivalente subsidiário depende de não se acolher a entrega; a formulação sem preferência bifurca-se entre máquina e equivalente", b), []


# The specimen initial is shared by the requirements and revision drawings.
# Coordinates belong here in the drawing part, never to lesson parameters.
SHEET = (200, 28, 770, 414)
ROW = {"juizo": (44, 80), "partes": (90, 140), "causa": (150, 222),
       "pedido": (232, 266), "valor": (276, 322),
       "provas": (328, 358), "audiencia": (362, 394)}


def _sheet(blank_value: bool, claimant: str, defendant: str) -> list[str]:
    x0, y0, x1, y1 = SHEET
    b = _paper(x0, y0, x1 - x0, y1 - y0)
    b += [S.text((x0 + x1) / 2, 66, "Ao juízo competente", size=18,
                 family=S.SERIF, anchor="middle"),
          S.line(x0 + 27, 80, x1 - 27, 80, stroke=S.GRID, stroke_width=.8),
          S.text(x0 + 30, 112, f"{claimant}, em face de {defendant};", size=16,
                 family=S.SERIF),
          S.text(x0 + 30, 134, "endereço conhecido; CPF/CNPJ da ré desconhecido.",
                 size=16, family=S.SERIF),
          S.text(x0 + 30, 172, "Entregou a máquina de costura para conserto.",
                 size=16, family=S.SERIF),
          S.text(x0 + 30, 194, "O prazo combinado venceu sem devolução.",
                 size=16, family=S.SERIF),
          S.text(x0 + 30, 216, "Alugou outra máquina e guardou os recibos.",
                 size=16, family=S.SERIF),
          S.text(x0 + 30, 254, "Pede a entrega da máquina e o reembolso do aluguel.",
                 size=16, family=S.SERIF),
          S.text(x0 + 30, 306, "Valor da causa:", size=16, family=S.SERIF)]
    if blank_value:
        b.append(S.line(x0 + 155, 309, x1 - 32, 309, stroke=S.INK2,
                        stroke_width=1, stroke_dasharray="2 5"))
    else:
        # The packet provides no amount. This is an annotation of the criterion,
        # not a fabricated economic fact of the running case.
        b.append(S.text(x0 + 160, 306, "[soma dos pedidos]", size=16,
                        family=S.SERIF, fill=S.INK2))
    b += [S.text(x0 + 30, 346, "Provas: recibos e comprovante da entrega.",
                 size=16, family=S.SERIF),
          S.text(x0 + 30, 380, "Tem interesse na audiência de conciliação.",
                 size=16, family=S.SERIF),
          S.path(f"M{x1-150} {y1-17} q20 -10 30 -1 t30 -3", fill="none",
                 stroke=S.INK2, stroke_width=1)]
    return b


def _peticao(p: dict) -> tuple[str, list[dict]]:
    """The seven requisites written in the margin of a static specimen initial."""
    claimant = p.get("claimant", "Cecília")
    defendant = p.get("defendant", "Oficina Horizonte")
    b = _sheet(False, claimant, defendant)
    reqs = [("juizo", "I", "Juízo"), ("partes", "II", "Partes"),
            ("causa", "III", "Causa de pedir"),
            ("pedido", "IV", "Pedido"), ("valor", "V", "Valor da causa"),
            ("provas", "VI", "Provas"), ("audiencia", "VII", "Audiência")]
    for key, rom, label in reqs:
        y0, y1 = ROW[key]
        yc = (y0 + y1) / 2
        color = S.DIF if key in ("causa", "pedido") else S.INK2
        b += [S.text(166, yc + 5, rom, size=14, fill=color, anchor="end"),
              S.line(177, yc, 198, yc, stroke=color, stroke_width=1),
              S.path(f"M778 {yc-9} h10 v18 h-10 M788 {yc} h20", fill="none",
                     stroke=color, stroke_width=1),
              S.text(823, yc + 5, label, size=16, family=S.SERIF, fill=color)]
    b += [S.text(823, 423, "art. 319", size=13, fill=S.INK2)]
    return S.svg(1080, 445, p.get("title") or
                 "A inicial de Cecília com os sete requisitos do art. 319 escritos à margem; a causa de pedir e o pedido ligam os fatos à tutela pretendida", b), []


def _scrap_path(x, y, w=210, h=96) -> str:
    """A scrap with straight top and sides, and a torn bottom; no turned corner."""
    pts, xx, k = [f"M{x} {y} H{x+w} V{y+h}"], x + w, 0
    while xx > x:
        xx = max(xx - 10, x)
        pts.append(f"L{xx} {y+h-(5 if k % 2 == 0 else 0)}")
        k += 1
    return " ".join(pts) + " Z"


def _revisao(p: dict) -> tuple[str, list[dict]]:
    """Correction marks stay on the original; a new claim sits on a separate leaf.

    Art. 319's missing data is not equated with automatic refusal. The value
    omission is curable under art. 321. New relief is separately governed by
    art. 329; the picture makes no ruling on substantive entitlement.
    """
    claimant = p.get("claimant", "Cecília")
    defendant = p.get("defendant", "Oficina Horizonte")
    b = _sheet(True, claimant, defendant)
    # The identifying information has a marginal check, not an invented CPF.
    b += [S.path("M222 98 h-10 v42 h10 M771 130 H805", fill="none",
                 stroke=S.DIF, stroke_width=1.4),
          S.text(824, 119, "Examinar se os dados", size=16,
                 family=S.SERIF, fill=S.DIF),
          S.text(824, 142, "permitem a citação.", size=16,
                 family=S.SERIF, fill=S.DIF),
          S.text(824, 168, "art. 319, §§ 1º–3º", size=12.5, fill=S.INK2)]
    # A proofreader's insertion sign and a handwritten addition complete the
    # same petition. The replacement gives no fictitious monetary amount.
    b += [S.path("M369 314 l8 -11 l8 11", fill="none", stroke=S.DIF, stroke_width=1.6),
          S.path("M377 316 H560", fill="none", stroke=S.DIF, stroke_width=1.6),
          S.path("M560 316 Q600 316 600 350 V410", fill="none", stroke=S.DIF, stroke_width=1.6),
          S.path("M600 410 C600 440 520 452 417 446", fill="none", stroke=S.DIF, stroke_width=1.6),
          S.text(180, 464, "Completar o valor da causa", size=18,
                 family=S.SERIF, fill=S.DIF),
          S.text(180, 489, "emenda · art. 321", size=13, fill=S.INK2),
          S.path("M178 474 q106 -8 223 -1", fill="none", stroke=S.DIF,
                 stroke_width=1)]
    # The orange leaf is deliberately outside the original sheet. It cannot
    # become a mere formal repair by borrowing the insertion mark above.
    b += [S.path(_scrap_path(817, 292, 220, 123), fill=S.PAPER,
                 stroke=S.CONC, stroke_width=1.4),
          S.text(836, 327, "Reparação de", size=19, family=S.SERIF,
                 fill=S.CONC),
          S.text(836, 354, "dano novo", size=19, family=S.SERIF,
                 fill=S.CONC)]
    b += _writing(836, 374, [160, 138], gap=11)
    b += [S.path("M818 350 C783 350 797 254 777 254 M777 246 V262 M769 246 V262",
                 fill="none", stroke=S.CONC, stroke_width=1.5),
          S.text(817, 464, "Acrescentar outra pretensão", size=18,
                 family=S.SERIF, fill=S.CONC),
          S.text(817, 489, "alteração · art. 329", size=13, fill=S.INK2)]
    return S.svg(1080, 516, p.get("title") or
                 "Revisar a inicial: examinar os dados que permitem citar, completar o valor omitido e distinguir disso a nova pretensão em folha separada", b), []


def _petition_tag(x, y, text="pedido", color=S.INK, w=123, h=111) -> list[str]:
    b = _paper(x, y, w, h, color=color, under=False)
    b += [S.circle(x + 15, y + 16, 3, fill=S.PAPER, stroke=S.INK2,
                   stroke_width=.9),
          S.text(x + 16, y + 43, text, size=17, family=S.SERIF, fill=color)]
    b += _writing(x + 16, y + 61, [w - 34, w - 43, w - 34], gap=12)
    return b


def _knot(x, y) -> list[str]:
    """Interwoven demand and defence threads; paper-width gaps show over/under."""
    return [S.path(f"M{x-46} {y-8} C{x-14} {y-24} {x+39} {y+27} {x+18} {y+29} C{x-1} {y+31} {x-23} {y-28} {x-5} {y-28} C{x+12} {y-28} {x+13} {y+12} {x+46} {y+7}",
                   fill="none", stroke=S.DIF, stroke_width=2.3,
                   stroke_linecap="round"),
            S.path(f"M{x-46} {y+8} C{x-15} {y+25} {x+38} {y-27} {x+18} {y-29} C{x-1} {y-31} {x-23} {y+28} {x-5} {y+28} C{x+12} {y+28} {x+13} {y-12} {x+46} {y-7}",
                   fill="none", stroke=S.PAPER, stroke_width=6,
                   stroke_linecap="round"),
            S.path(f"M{x-46} {y+8} C{x-15} {y+25} {x+38} {y-27} {x+18} {y-29} C{x-1} {y-31} {x-23} {y+28} {x-5} {y+28} C{x+12} {y+28} {x+13} {y-12} {x+46} {y-7}",
                   fill="none", stroke=S.INK2, stroke_width=1.8,
                   stroke_linecap="round"),
            S.path(f"M{x-8} {y-26} C{x+3} {y-25} {x+9} {y-3} {x+14} {y+12}",
                   fill="none", stroke=S.PAPER, stroke_width=5.5),
            S.path(f"M{x-8} {y-26} C{x+3} {y-25} {x+9} {y-3} {x+14} {y+12}",
                   fill="none", stroke=S.DIF, stroke_width=2.3)]


def _janelas(p: dict) -> tuple[str, list[dict]]:
    """Art. 329 as a loose thread, mutual knot and sealed demand.

    Static, fully readable states; no axis, button, bracket heading or tooltip.
    The seal closes unilateral alteration only. The note retains the books'
    disagreement about a later agreement under art. 190.
    """
    b = []
    # A loose loop: the author's thread can be taken out and retied.
    b += _petition_tag(39, 60, "pedido")
    b += [S.path("M54 76 C-3 15 177 -4 203 74 C222 130 127 165 144 197 C159 225 215 171 258 192 C307 216 304 152 272 154 C247 155 247 202 294 233",
                 fill="none", stroke=S.DIF, stroke_width=2.2,
                 stroke_linecap="round"),
          S.path("M286 225 l8 8 l-1 -12", fill="none", stroke=S.DIF,
                 stroke_width=1.5)]
    b += [S.text(39, 284, "Até a citação", size=21, family=S.SERIF,
                 weight="600"),
          S.text(39, 314, "O autor altera sem precisar", size=17,
                 family=S.SERIF),
          S.text(39, 339, "do consentimento da ré.", size=17,
                 family=S.SERIF),
          S.text(39, 374, "art. 329, I", size=13, fill=S.INK2)]
    # The two participants' strands meet at a real over-and-under knot.
    b += _petition_tag(398, 39, "pedido", w=121, h=107)
    b += _petition_tag(618, 78, "resposta", w=112, h=105)
    b += [S.path("M413 55 C390 2 340 91 404 159 C424 183 469 172 491 165",
                 fill="none", stroke=S.DIF, stroke_width=2.2,
                 stroke_linecap="round"),
          S.path("M633 94 C697 14 769 147 690 173 C648 189 617 176 583 165",
                 fill="none", stroke=S.INK2, stroke_width=1.8,
                 stroke_linecap="round")]
    b += _knot(537, 173)
    b += [S.text(401, 284, "Da citação ao saneamento", size=21,
                 family=S.SERIF, weight="600"),
          S.text(401, 314, "Consentimento da ré;", size=17, family=S.SERIF),
          S.text(401, 339, "manifestação em no mínimo 15 dias;", size=16,
                 family=S.SERIF),
          S.text(401, 362, "possibilidade de prova suplementar.", size=16,
                 family=S.SERIF),
          S.text(401, 393, "art. 329, II", size=13, fill=S.INK2)]
    # A sealed strand: no unilateral retie. The books disagree about whether
    # a valid new agreement can overcome this boundary, and that remains visible.
    b += _petition_tag(823, 39, "pedido", w=153, h=134)
    b += [S.path("M838 55 C782 8 756 98 797 161 C826 205 940 234 973 185 C1001 143 966 142 939 157",
                 fill="none", stroke=S.DIF, stroke_width=2.2,
                 stroke_linecap="round"),
          S.path("M927 177 l-14 55 l19 -9 l8 20 l13 -62", fill=S.PAPER,
                 stroke=S.CONC, stroke_width=1.2),
          S.path("M916 158 l7 -11 l12 -2 l10 -8 l12 5 l12 -1 l7 11 l11 6 l-2 13 l4 11 l-9 10 l-4 12 l-13 1 l-11 5 l-11 -7 l-13 -2 l-3 -12 l-8 -10 l5 -11 Z",
                 fill=S.PAPER, stroke=S.CONC, stroke_width=1.7),
          S.circle(948, 171, 21, fill="none", stroke=S.CONC, stroke_width=.9),
          S.path("M939 171 l7 7 l12 -17", fill="none", stroke=S.CONC,
                 stroke_width=1.5, stroke_linecap="round"),
          S.text(790, 284, "Depois do saneamento", size=21,
                 family=S.SERIF, weight="600"),
          S.text(790, 314, "Fechada ao ato unilateral.", size=17,
                 family=S.SERIF),
          S.path("M965 334 V399 Q965 412 950 412 H700", fill="none",
                 stroke=S.CONC, stroke_width=.8),
          S.text(700, 439, "Acordo posterior: Marinoni admite pelo art. 190;", size=15.5,
                 family=S.SERIF, fill=S.CONC),
          S.text(700, 462, "Didier lê a vedação do art. 329 e a critica.", size=15.5,
                 family=S.SERIF, fill=S.CONC)]
    return S.svg(1080, 485, p.get("title") or
                 "O fio da demanda: solto antes da citação; preso ao consentimento da ré até o saneamento; selado contra o ato unilateral depois dele, com divergência doutrinária sobre o acordo posterior", b), []


def _fecho(p: dict) -> tuple[str, list[dict]]:
    """An open case file: the first and final folios hold the same threads.

    Canvas 1080×515. Both leaves belong to one bound object, not framed
    labels. The petition carries the running facts and the completed value;
    the judgment has room for reasons and a dispositivo, without an invented
    outcome. A separate new-claim slip cannot enter through the art.329 clasp.
    Provenance: CPC arts.319,321,329,141,492; Didier p.618; Marinoni pp.163–167.
    """
    # The curved fore-edge and the repeated leaves make a single open file.
    # The centre is its sewn binding; neither leaf has a separate card frame.
    b = [S.path("M38 43 Q278 24 532 49 Q782 24 1042 43 V380 Q782 360 532 391 Q278 360 38 380 Z",
                fill=S.PAPER, stroke=S.INK, stroke_width=1.5)]
    for offset in (5, 10, 15):
        b += [S.path(f"M38 {380 + offset} Q278 {360 + offset} 532 {391 + offset} Q782 {360 + offset} 1042 {380 + offset}",
                     fill="none", stroke=S.INK2, stroke_width=.7)]
    b += [S.path("M532 49 V391 M525 50 Q512 209 525 386 M539 50 Q551 209 539 386",
                 fill="none", stroke=S.INK2, stroke_width=.8)]
    for y in (76, 154, 321, 367):
        b.append(S.path(f"M526 {y} q6 8 12 0", fill="none",
                       stroke=S.INK, stroke_width=1))

    # Initial pleading: concrete allegations and two requested results, on
    # the same sheet as the value supplied by a formal amendment.
    b += [S.text(75, 78, "Petição inicial", size=25, family=S.SERIF, weight="600"),
          S.text(75, 103, "Cecília · Oficina Horizonte", size=14.5,
                 family=S.SERIF, fill=S.INK2),
          S.line(75, 116, 473, 116, stroke=S.GRID, stroke_width=.8),
          S.text(75, 145, "Entregou a máquina para conserto.", size=18, family=S.SERIF),
          S.text(75, 173, "Prazo vencido, sem devolução.", size=18, family=S.SERIF),
          S.text(75, 201, "Alugou outra e guardou recibos.", size=18, family=S.SERIF),
          S.text(75, 248, "entrega da máquina", size=20, family=S.SERIF, fill=S.DIF),
          S.text(75, 290, "reembolso do aluguel", size=20, family=S.SERIF, fill=S.DIF),
          S.text(75, 335, "Valor da causa:", size=16.5, family=S.SERIF),
          S.text(195, 335, "soma dos pedidos", size=17, family=S.SERIF, fill=S.DIF),
          S.path("M194 342 q99 -4 172 0", fill="none", stroke=S.DIF, stroke_width=.9),
          S.text(75, 363, "valor completado · art. 321", size=12.5, fill=S.INK2)]

    # Reasons remain open for the parties' allegations and proof. The
    # dispositif receives each request, not a fictional grant or dismissal.
    b += [S.text(588, 78, "Sentença", size=25, family=S.SERIF, weight="600"),
          S.text(588, 113, "alegações e provas examinadas", size=16,
                 family=S.SERIF, fill=S.INK2)]
    b += _writing(588, 135, [409, 389, 410, 324], gap=15)
    b += [S.text(769, 218, "Dispositivo", size=21, family=S.SERIF, weight="600"),
          S.text(769, 248, "pedido de entrega", size=19, family=S.SERIF),
          S.text(769, 290, "pedido de reembolso", size=19, family=S.SERIF),
          S.text(769, 337, "acolher ou rejeitar", size=16, family=S.SERIF,
                 fill=S.INK2)]

    # Continuous thread, with no arrows and no two-card comparison. The
    # slight rise over the gutter follows the paper's binding in space.
    for y in (257, 299):
        b += [S.path(f"M75 {y} H473 Q532 {y-10} 588 {y} H998", fill="none",
                     stroke=S.DIF, stroke_width=2.1),
              S.circle(473, y, 3, fill=S.DIF)]
    b += [S.path("M755 237 h-9 v72 h9 M740 237 v72", fill="none",
                 stroke=S.CONC, stroke_width=1.7),
          S.text(606, 335, "arts. 141 e 492", size=12.5, fill=S.CONC),
          S.path("M730 329 H741 V316", fill="none", stroke=S.CONC,
                 stroke_width=.8)]

    # The new relief is a loose, torn slip. A clasp in the binding holds its
    # thread off the settled requests: entry depends on the art.329 window.
    b += [S.path("M692 444 C614 444 559 427 551 398 V382", fill="none",
                 stroke=S.CONC, stroke_width=1.7),
          S.path("M541 365 v-9 q0 -11 10 -11 q10 0 10 11 v9", fill="none",
                 stroke=S.CONC, stroke_width=1.5),
          S.path("M537 365 H565 V389 H537 Z", fill=S.PAPER,
                 stroke=S.CONC, stroke_width=1.4),
          S.circle(551, 375, 2, fill=S.CONC),
          S.path("M551 377 v5", fill="none", stroke=S.CONC, stroke_width=1),
          S.text(580, 380, "art. 329", size=12.5, fill=S.CONC),
          S.path(_scrap_path(692, 416, 313, 78), fill=S.PAPER,
                 stroke=S.CONC, stroke_width=1.3),
          S.text(712, 447, "Reparação de dano novo", size=20,
                 family=S.SERIF, fill=S.CONC),
          S.text(712, 475, "outra pretensão · entrada condicionada", size=12.5,
                 fill=S.CONC),
          S.text(75, 460, "A peça se completa;", size=21, family=S.SERIF),
          S.text(75, 489, "os pedidos mantêm seus limites.", size=21,
                 family=S.SERIF, fill=S.DIF)]
    return S.svg(1080, 515, p.get("title") or
                 "Os mesmos autos, abertos entre a inicial e a sentença: os fatos de Cecília sustentam os pedidos de entrega e reembolso, cujos fios chegam ao dispositivo sob os limites dos arts.141 e492. O valor foi completado pelo art.321; a pretensão de dano novo fica na folha avulsa, sujeita ao art.329", b), []


def _peticao_repensada(p: dict) -> tuple[str, list[dict]]:
    """An anatomical plate of the carrier's pleading, with its real objects.

    The machine sits against its request; the rental receipts sit against the
    proof paragraph. Seven external leaders identify functions that the real
    document already performs. No cadastral datum or monetary amount is made
    up. The bracketed value is a specimen's criterion, not a claimed amount.
    """
    claimant = p.get("claimant", "Cecília")
    defendant = p.get("defendant", "Oficina Horizonte")
    b = _paper(260, 24, 530, 535)
    b += [S.text(290, 69, "AO JUÍZO COMPETENTE", size=16.5,
                 family=S.SANS, weight="600"),
          S.text(290, 111, f"{claimant} · {defendant}", size=18,
                 family=S.SERIF),
          S.text(290, 134, "Endereço conhecido; CNPJ da ré desconhecido.",
                 size=15.5, family=S.SERIF),
          S.line(290, 150, 760, 150, stroke=S.GRID, stroke_width=.8),
          S.text(290, 182, "Entregou a máquina de costura para conserto.",
                 size=17, family=S.SERIF),
          S.text(290, 206, "O prazo venceu sem devolução.", size=17,
                 family=S.SERIF),
          S.text(290, 230, "Alugou outra máquina e guardou os recibos.",
                 size=17, family=S.SERIF),
          S.text(290, 279, "Requer a entrega da máquina", size=19,
                 family=S.SERIF),
          S.text(290, 307, "e o reembolso do aluguel.", size=19,
                 family=S.SERIF),
          S.line(290, 320, 724, 320, stroke=S.DIF, stroke_width=1.5),
          S.text(290, 367, "Valor da causa: [soma dos pedidos]", size=17,
                 family=S.SERIF),
          S.text(290, 421, "Provas: recibos do aluguel", size=17,
                 family=S.SERIF),
          S.text(290, 445, "e comprovante da entrega.", size=17,
                 family=S.SERIF),
          S.text(290, 500, "Tem interesse na conciliação.", size=17,
                 family=S.SERIF),
          S.path("M610 535 q26 -12 38 -2 t49 -3", fill="none",
                 stroke=S.INK2, stroke_width=1.1)]
    # These are the things referred to, outside the folio, rather than labels
    # pretending to be its content. Their leaders end at the relevant text.
    b += [_machine(49, 266, .78),
          S.path("M188 343 H237 V286 H278", fill="none", stroke=S.DIF,
                 stroke_width=1.2),
          S.circle(278, 286, 2.5, fill=S.PAPER, stroke=S.DIF,
                   stroke_width=1.2)]
    receipt_back = _receipt(73, 420, 125, 132)
    receipt_front = _receipt(57, 409, 125, 132)
    b += [_group(receipt_back, transform="rotate(7 134 486)"),
          _group(receipt_front, transform="rotate(-4 119 475)"),
          S.path("M190 447 H237 V433 H278", fill="none", stroke=S.INK2,
                 stroke_width=1),
          S.circle(278, 433, 2.5, fill=S.PAPER, stroke=S.INK2,
                   stroke_width=1)]
    # Labels are in the margin. Their seven positions follow the document's
    # physical order and their leaders do not cross the writing.
    for roman, label, y in [("I", "Juízo", 65),
                            ("II", "Partes", 122),
                            ("III", "Causa de pedir", 205)]:
        b += [S.text(21, y + 5, roman, size=13.5, fill=S.INK2),
              S.text(59, y + 5, label, size=17, family=S.SERIF),
              S.line(220, y, 251, y, stroke=S.INK2, stroke_width=1),
              S.path(f"M252 {y-9} h7 v18 h-7", fill="none",
                     stroke=S.INK2, stroke_width=1)]
    for roman, label, y in [("IV", "Pedido", 291),
                            ("V", "Valor da causa", 362),
                            ("VI", "Provas", 433),
                            ("VII", "Audiência", 495)]:
        b += [S.path(f"M791 {y-9} h8 v18 h-8 M799 {y} H825",
                     fill="none", stroke=S.INK2, stroke_width=1),
              S.text(838, y + 5, roman, size=13.5, fill=S.INK2),
              S.text(880, y + 5, label, size=17, family=S.SERIF)]
    b.append(S.text(880, 551, "art. 319", size=13, fill=S.INK2))
    return S.svg(1080, 582, p.get("title") or
                 "A anatomia da inicial de Cecília: sete funções na margem, a máquina ligada ao pedido de entrega e os recibos ligados à prova do aluguel", b), []


def _pedidos_repensados(p: dict) -> tuple[str, list[dict]]:
    """Three geometries of possible awards, without an invented case outcome.

    Simples and subsidiária use the carrier's actual goods. The middle panel
    is explicitly the structure of a successive dispositif: the source does
    not supply a concrete successive claim, so the machine and rental are
    never drawn as if the latter legally depended on the former.
    """
    b = [S.text(28, 37, "Simples", size=24, family=S.SERIF, weight="600"),
         S.text(389, 37, "Sucessiva · estrutura", size=24,
                family=S.SERIF, weight="600"),
         S.text(749, 37, "Subsidiária", size=24, family=S.SERIF,
                weight="600"),
         S.line(360, 73, 360, 397, stroke=S.GRID, stroke_width=.8),
         S.line(720, 73, 720, 397, stroke=S.GRID, stroke_width=.8)]
    # Conjunction is spatial: two independently complete things stay present
    # together, with two marks of possible acolhimento under one open brace.
    b += [_machine(40, 124, .81)]
    b += _receipt(230, 124, 98, 129)
    b += [S.path("M194 180 H214 M204 170 V190", fill="none", stroke=S.INK,
                 stroke_width=1.7),
          S.path("M50 283 V296 H321 V283", fill="none", stroke=S.DIF,
                 stroke_width=1.5),
          S.path("M102 269 l7 7 l13 -18 M266 269 l7 7 l13 -18",
                 fill="none", stroke=S.DIF, stroke_width=2,
                 stroke_linecap="round", stroke_linejoin="round"),
          S.text(28, 343, "Os dois podem ser acolhidos.", size=18,
                 family=S.SERIF),
          S.text(28, 373, "Entrega e reembolso são independentes.", size=15,
                 family=S.SERIF, fill=S.INK2),
          S.text(28, 414, "art. 327", size=13, fill=S.INK2)]
    # A single real judicial object, not two cards joined by an arrow. Its
    # affirmative first section physically supports the recessed second one.
    # The second affirmative mark lies inside the first's open bracket.
    b += _paper(404, 86, 270, 224)
    b += [S.text(426, 116, "Dispositivo", size=19, family=S.SERIF,
                 weight="600"),
          S.line(426, 128, 652, 128, stroke=S.GRID, stroke_width=.8),
          S.text(426, 161, "1. Acolhimento", size=17, family=S.SERIF),
          S.text(447, 185, "do primeiro pedido.", size=16.5,
                 family=S.SERIF),
          S.path("M627 153 l7 7 l13 -18", fill="none", stroke=S.DIF,
                 stroke_width=2, stroke_linecap="round",
                 stroke_linejoin="round"),
          S.path("M439 198 H645 V279 H439", fill="none", stroke=S.DIF,
                 stroke_width=1.5),
          S.text(458, 230, "2. Acolhimento", size=17, family=S.SERIF),
          S.text(479, 254, "do segundo pedido.", size=16.5,
                 family=S.SERIF),
          S.path("M613 268 l7 7 l13 -18", fill="none", stroke=S.DIF,
                 stroke_width=2, stroke_linecap="round",
                 stroke_linejoin="round"),
          S.text(389, 343, "Querem-se os dois;", size=18,
                 family=S.SERIF),
          S.text(389, 369, "o segundo depende do primeiro acolhido.",
                 size=15.5, family=S.SERIF),
          S.text(389, 414, "Didier, pp. 639–645", size=13, fill=S.INK2)]
    # The preferred physical outcome occupies the upper position. The same
    # place can instead hold its monetary equivalent, lower and separated by
    # an exclusion stroke. It cannot hold both: there is no conjunction.
    b += [_machine(770, 83, .74)]
    b += _money(915, 221, 114, 69)
    b += [S.text(748, 109, "1", size=17, family=S.SANS, fill=S.INK2),
          S.text(891, 250, "2", size=17, family=S.SANS, fill=S.INK2),
          S.path("M777 290 L1032 84", fill="none", stroke=S.CONC,
                 stroke_width=1.5),
          S.text(971, 193, "ou", size=20, family=S.SERIF,
                 anchor="middle"),
          S.text(749, 343, "Máquina primeiro;", size=18,
                 family=S.SERIF),
          S.text(749, 369, "equivalente só se ela não for acolhida.",
                 size=15.5, family=S.SERIF),
          S.text(749, 414, "art. 326, caput", size=13, fill=S.INK2),
          S.text(749, 445, "Formulação hipotética da pretensão.", size=14,
                 family=S.SERIF, fill=S.INK2)]
    return S.svg(1080, 465, p.get("title") or
                 "Três relações: máquina e reembolso podem coexistir; na sucessiva o segundo acolhimento depende do primeiro; na subsidiária a preferência pela máquina exclui o exame do equivalente quando ela é acolhida", b), []


def _record_leaf(x, y, w, h, heading, lines, color=S.INK) -> list[str]:
    """A pleading/order carrying its own content, not a label container."""
    b = _paper(x, y, w, h, color=color, under=False)
    b += [S.text(x + 18, y + 30, heading, size=17, family=S.SERIF,
                 weight="600"),
          S.line(x + 18, y + 43, x + w - 18, y + 43, stroke=S.GRID,
                 stroke_width=.8)]
    for i, line in enumerate(lines):
        b.append(S.text(x + 18, y + 72 + 25 * i, line, size=15.5,
                        family=S.SERIF))
    return b


def _janelas_repensadas(p: dict) -> tuple[str, list[dict]]:
    """The litigation record gains layers, consent and an organised scope.

    The last leaf organises the existing matter. It neither closes a lock nor
    crosses out a later agreement: the books' divergence remains explicit.
    Every layer is an actual kind of document used in these proceedings.
    """
    b = [S.text(24, 36, "Antes da citação", size=22, family=S.SERIF,
                weight="600"),
         S.text(387, 36, "Da citação ao saneamento", size=22,
                family=S.SERIF, weight="600"),
         S.text(749, 36, "Depois do saneamento", size=22,
                family=S.SERIF, weight="600"),
         S.line(358, 78, 358, 383, stroke=S.GRID, stroke_width=.8),
         S.line(720, 78, 720, 383, stroke=S.GRID, stroke_width=.8)]
    # Before citation, an extra allegation/request is simply another leaf
    # that can be added to the author's record. The open top is intentional.
    b += _record_leaf(31, 139, 255, 215, "Petição inicial",
                      ["Cecília · Oficina Horizonte", "Entrega da máquina", "Reembolso do aluguel"])
    b += _writing(49, 292, [201, 184, 208], gap=12)
    extra = _record_leaf(162, 77, 159, 146, "Aditamento",
                         ["Reparação por", "outro dano."], color=S.DIF)
    extra += [S.path("M181 202 q24 -8 43 -1 t31 -3", fill="none",
                     stroke=S.INK2, stroke_width=1)]
    b.append(_group(extra, transform="rotate(5 241 150)"))
    b += [S.text(24, 399, "O autor pode acrescentar ou alterar.", size=17,
                 family=S.SERIF),
          S.text(24, 427, "Sem consentimento da ré · art. 329, I", size=14,
                 fill=S.INK2)]
    # After citation the extra sheet is no longer solely on top of the
    # author's pleading: it spans two procedural voices, with two signatures.
    left = _record_leaf(396, 139, 218, 215, "Petição inicial",
                        ["Cecília", "Entrega e aluguel"])
    left += _writing(414, 274, [160, 174, 147], gap=12)
    right = _record_leaf(454, 116, 218, 215, "Contestação",
                         ["Oficina Horizonte", "Resposta aos pedidos"])
    right += _writing(472, 251, [161, 171, 143], gap=12)
    b += [_group(left, transform="rotate(-4 505 247)"),
          _group(right, transform="rotate(4 563 223)" )]
    b += _record_leaf(414, 177, 256, 157, "Aditamento acordado",
                      ["Reparação por outro dano."])
    b += [S.path("M434 291 q19 -11 28 -1 t28 -3 M565 291 q16 -10 25 -1 t32 -3",
                 fill="none", stroke=S.INK, stroke_width=1.2),
          S.line(431, 302, 520, 302, stroke=S.GRID, stroke_width=.8),
          S.line(562, 302, 650, 302, stroke=S.GRID, stroke_width=.8),
          S.text(432, 321, "Cecília", size=12.5, fill=S.INK2),
          S.text(562, 321, "Oficina", size=12.5, fill=S.INK2),
          S.text(387, 399, "Depende do consentimento da ré.", size=17,
                 family=S.SERIF, fill=S.CONC),
          S.text(387, 427, "Debate e prova suplementar · art. 329, II", size=14,
                 fill=S.INK2)]
    # Once the scope is organised, the order keeps the claims beside their
    # corresponding evidence. Repeated exposed edges are the earlier record.
    for off in (12, 6):
        b += _paper(760 + off, 113 + off, 265, 241, under=False)
    b += _record_leaf(760, 113, 265, 241, "Saneamento",
                      ["Prazo e devolução", "Aluguel e recibos"])
    b += [S.line(778, 220, 1005, 220, stroke=S.GRID, stroke_width=.8),
          _machine(783, 239, .55)]
    b += _receipt(931, 236, 65, 100)
    b += [S.path("M1037 159 h9 v172 h-9 M1046 245 h11", fill="none",
                 stroke=S.INK2, stroke_width=1.1),
          S.text(749, 399, "Organizam-se as questões e as provas.", size=17,
                 family=S.SERIF),
          S.text(749, 427, "Acordo posterior: há divergência doutrinária.",
                 size=14, fill=S.CONC)]
    return S.svg(1080, 455, p.get("title") or
                 "A demanda deixa marcas nos autos: o aditamento entra livremente antes da citação; entre citação e saneamento, pede consentimento da ré e nova oportunidade de debate e prova; depois, as questões estão organizadas e o acordo posterior divide a doutrina", b), []


def build(p: dict) -> tuple[str, list[dict]]:
    builders = {"percurso": _percurso, "pedidos": _pedidos,
                "revisao": _revisao, "peticao": _peticao,
                "janelas": _janelas, "fecho": _fecho,
                "peticao_repensada": _peticao_repensada,
                "pedidos_repensados": _pedidos_repensados,
                "janelas_repensadas": _janelas_repensadas}
    mode = p.get("mode")
    if mode not in builders:
        raise ValueError("abertura_civil: unknown drawing mode")
    return builders[mode](p)
