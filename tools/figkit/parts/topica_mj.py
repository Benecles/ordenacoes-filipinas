"""topica_mj: one received volume read, argued over and read again.

Params (reading mode and optional accessible title, never coordinates):
  mode   lugares | percurso | leitura | conceitos | opinio | baldo (required)
  title  optional accessible description replacing the mode's default
  state  opinio only: 1 (individual opinion), 2 (shared direction),
         3 (Cino's objection to infallibility). The page puts each state
         inside a .panel and its paragraphs in .step[data-panel].

Canvases: lugares 1100x560; percurso 1100x440; leitura 1100x630;
conceitos 1100x530; opinio 370x1440 (three zones of 480, one per step); baldo 370x350.
Each build result is static: build(params) -> (svg, []). For opinio the house
script swaps the three results as the text reaches the reading line. Type is at least
18 units; the reconstruction notice for lugares lives in the page caption. Colours are
house tokens through .svg; no selectors, folded corners or authored quotes.

Provenance: Hespanha, Historia das instituicoes (1982), 14.3.4, pp.467-479,
and 14.3.5, pp.479-488, read whole including notes. lugares combines the
procurator outcome transmitted from Bartolus (p.469) with the loci of
definition/division (pp.472-474), causes (p.474), comparison (pp.474-475)
and authority (pp.475-477). The FIRST THREE ARGUMENTS ARE HYPOTHETICAL
TEACHING RECONSTRUCTIONS, not arguments attributed to Bartolus's Consilium;
the notice sits in the figcaption. The fourth route cites the reported outcome
and explains the source's account of expertise. Authority remains defeasible.

percurso maps the relation of text, finding perspectives, confrontation,
probable solution and renewed objection in pp.468-477; pp.478-479 supply
Viehweg's situated decision. 'Provavel' qualifies a solution, not a formal
procedural category of provisional judicial decision. The single open
volume contains schematic writing, never an invented Roman passage.

leitura gives the eight operations of Gribaldo Mopha in the note spanning
pp.477-478: praemitto, scindo, summo, casumque figuro, perlego, do causas,
connoto, et obiicio. Obvious OCR letters in 'casumque figuro' and
'et obiicio' have been normalised. Numbers follow the note, down the left margin,
across the foot and up the right margin. Leaders attach the operations to
one folio's received text, logical divisions, reconstructed context and
objections; the double-sided annotations belong to that one working book.

conceitos maps the examples of definition and division in pp.473-474 and
their notes. It reproduces the book's logical examples, not current contract
doctrine. Legal relation > contract > donation, sale, lease and loan is a
genus/species ladder. The two further divisions (formal/consensual and
unilateral/bilateral) are drawn BELOW and apart from that tree: they use
different criteria and are never falsely attached as disjoint species of
the four named contracts. No unsourced allocation of a contract to either
classification is made.

opinio reconstructs the argument's changing credit and practical orientation
from pp.475–477, especially the note on probability before and after about
1250 (p.476). Converging manuscript strokes are opinions, never a head count
or a numerical proof. State 3 leaves a counterargument entering the working
book; it represents Cino's insistence that even unanimous doctors can err.
No manuscript stroke is a quotation, and no opinion is attributed to an
individual except the counterargument identified as Cino's in the prose.
"""
from __future__ import annotations

from . import svg as S


def _t(x, y, words, size=20, fill=S.INK, family=S.SERIF, **kw):
    return S.text(x, y, words, size=size, fill=fill, family=family, **kw)


def _p(d, stroke=S.INK, width=1.5, **kw):
    return S.path(d, fill="none", stroke=stroke, stroke_width=width,
                  stroke_linecap="round", stroke_linejoin="round", **kw)


def _arrow(d, x, y, direction="right", colour=S.INK, width=1.5):
    ends = {
        "right": f"M{x - 7} {y - 4} L{x} {y} L{x - 7} {y + 4}",
        "left": f"M{x + 7} {y - 4} L{x} {y} L{x + 7} {y + 4}",
        "up": f"M{x - 4} {y + 7} L{x} {y} L{x + 4} {y + 7}",
        "down": f"M{x - 4} {y - 7} L{x} {y} L{x + 4} {y - 7}",
    }
    return [_p(d, colour, width), _p(ends[direction], colour, width)]


def _f(items, on=True):
    """Elements new in this state fade in over the previous state, which the house script keeps beneath."""
    return [f'<g class="fade">{"".join(items)}</g>'] if on else list(items)


def _writing(x, y, widths, gap=12):
    return [S.line(x, y + i * gap, x + width, y + i * gap,
                   stroke=S.GRID, stroke_width=1)
            for i, width in enumerate(widths)]


def _volume(x, y, w, h):
    """An open working codex, with its gutter and visible lower leaves."""
    mid = x + w / 2
    out = [S.path(
        f"M{x - 5} {y + 6} Q{mid - 65} {y - 12} {mid} {y + 9} "
        f"Q{mid + 65} {y - 12} {x + w + 5} {y + 6} V{y + h + 7} "
        f"Q{mid + 65} {y + h - 10} {mid} {y + h + 12} "
        f"Q{mid - 65} {y + h - 10} {x - 5} {y + h + 7} Z",
        fill=S.PAPER, stroke=S.INK, stroke_width=1.7),
        S.path(
        f"M{x} {y} Q{mid - 65} {y - 16} {mid} {y + 7} "
        f"Q{mid + 65} {y - 16} {x + w} {y} V{y + h} "
        f"Q{mid + 65} {y + h - 16} {mid} {y + h + 6} "
        f"Q{mid - 65} {y + h - 16} {x} {y + h} Z",
        fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
        _p(f"M{mid} {y + 8} V{y + h + 5}", S.INK2, 1.1)]
    for offset in (4, 8):
        out.append(_p(
            f"M{x + 2} {y + h + offset} Q{mid - 65} {y + h - 13 + offset} "
            f"{mid} {y + h + 9 + offset} Q{mid + 65} "
            f"{y + h - 13 + offset} {x + w - 2} {y + h + offset}",
            S.INK2, .7))
    return out


def _leaf(x, y, w, h):
    return [S.rect(x + 4, y + 5, w, h, fill=S.PAPER, stroke=S.GRID,
                   stroke_width=1),
            S.rect(x + 2, y + 2, w, h, fill=S.PAPER, stroke=S.INK2,
                   stroke_width=.7),
            S.rect(x, y, w, h, fill=S.PAPER, stroke=S.INK,
                   stroke_width=1.4)]


def _lugares(p):
    b = []

    # Opposite positions are alternative perspectives on the SAME question.
    # No enclosing panels: the routes lead into the working folio itself.
    b += [_t(28, 66, "Definição · divisão", 25),
          _t(28, 94, "Se «apresentação» é o gênero,", 20),
          _t(28, 120, "próprio e procurador cabem nele.", 20),
          _t(778, 66, "Causas", 25),
          _t(778, 94, "Se o fim é apresentar a prova,", 20),
          _t(778, 120, "o portador preserva esse fim.", 20),
          _t(28, 443, "Comparação", 25),
          _t(28, 471, "A mesma razão para o ato", 20),
          _t(28, 497, "sustentaria a mesma consequência.", 20),
          _t(778, 443, "Autoridade", 25),
          _t(778, 471, "Bártolo inclui o procurador;", 20),
          _t(778, 497, "a perícia dá crédito à solução.", 20)]

    b += _arrow("M185 137 C185 188 280 214 370 226", 370, 226)
    b += _arrow("M917 137 C917 188 822 214 732 226", 732, 226,
                direction="left")
    b += _arrow("M185 410 C185 364 275 346 370 335", 370, 335)
    b += _arrow("M917 410 C917 364 827 346 732 335", 732, 335,
                direction="left")

    b += _leaf(374, 162, 354, 229)
    b += [_t(551, 198, "apresentação em processo", 23, anchor="middle"),
          _p("M398 213 H705", S.GRID, 1),
          _t(551, 249, "Pelo procurador também?", 25, anchor="middle"),
          _t(551, 294, "extensão admitida", 21, fill=S.DIF,
             anchor="middle"),
          _t(551, 330, "pelo próprio · pelo procurador", 21,
             anchor="middle"),
          _p("M410 343 H693", S.DIF, 1.3),
          _t(551, 370, "o alcance se sustenta em razões", 18,
             fill=S.INK2, anchor="middle")]

    # The limit interrupts only the authority route; expertise raises credit
    # without turning a probable opinion into an irrebuttable proposition.
    b += [_p("M919 507 V520 H650", S.CONC, 1.4),
          _p("M657 515 V525 M651 515 V525", S.CONC, 1.3),
          _t(550, 548, "Uma razão melhor pode infirmar a autoridade.", 21,
             fill=S.CONC, anchor="middle")]
    return S.svg(1100, 560, p.get("title") or
                 "O mesmo estatuto de apresentação é examinado pelos lugares da definição, das causas, da comparação e da autoridade; os argumentos didáticos convergem na questão do procurador e a autoridade admite refutação", b), []


def _percurso(p):
    b = [_t(30, 44, "Ler um texto", 25),
          _t(391, 44, "Encontrar perspectivas", 25),
          _t(883, 44, "Decidir no caso", 25)]

    # This is the inherited working volume, not a new hypothetical case.
    b += _volume(30, 115, 285, 213)
    b += [_t(48, 151, "texto", 23),
          *_writing(48, 173, [104, 100, 106, 92, 103, 96], 13),
          _t(192, 151, "problema", 23),
          _t(191, 192, "pelo próprio", 18),
          _t(191, 220, "pelo", 18),
          _t(191, 245, "procurador", 18),
          *_writing(191, 266, [101, 92, 100], 13)]

    # Finding a place is a branching movement; it supplies several grounds,
    # not one mechanically necessary next step in a deduction.
    b += _arrow("M318 206 C358 206 353 105 386 105", 386, 105)
    b += _arrow("M318 206 C360 206 354 157 386 157", 386, 157)
    b += _arrow("M318 206 H386", 386, 206)
    b += _arrow("M318 206 C358 206 353 258 386 258", 386, 258)
    for y, label in ((97, "definir · dividir"), (149, "causas"),
                     (198, "comparação"), (250, "autoridades")):
        b.append(_t(396, y, label, 21))
    b += [_p("M395 108 H540 C592 108 606 196 640 222", S.INK2, 1.3),
          _p("M395 160 H540 C592 160 608 204 640 226", S.INK2, 1.3),
          _p("M395 209 H540 C592 209 610 216 640 230", S.INK2, 1.3),
          _p("M395 261 H540 C592 261 608 244 640 234", S.INK2, 1.3),
          _t(722, 121, "Confrontar", 24, anchor="middle"),
          _t(722, 149, "razões", 24, anchor="middle")]
    # A balance that has not settled: two reasons weighed against each other, no formal judgment fabricated.
    b += [_p("M722 300 V200 M696 300 H748", S.INK, 1.8), S.circle(722, 200, 4.5, fill=S.PAPER, stroke=S.INK, stroke_width=1.6),
          _p("M650 216 L794 186", S.INK, 2),
          _p("M650 216 L634 252 M650 216 L666 252 M630 252 Q650 264 670 252", S.INK, 1.4),
          _p("M794 186 L778 222 M794 186 L810 222 M774 222 Q794 234 814 222", S.INK, 1.4),
          _t(722, 330, "premissas discutíveis", 19, fill=S.INK2, anchor="middle")]
    b += _arrow("M826 204 H861", 861, 204)

    # The solution sits as a still-open marginal conclusion, with no stamp
    # implying final certainty and no procedural label such as liminar.
    b += [_p("M877 158 H866 V259 H877", S.INK2, 1.2),
          _t(883, 187, "solução provável", 24),
          _t(883, 220, "adequada ao caso", 20),
          _p("M883 238 H1068", S.GRID, 1),
          _t(883, 281, "objeção", 23, fill=S.CONC)]
    b += _arrow("M1035 289 C1080 337 1025 378 922 378 H204 C144 378 124 359 124 320",
                124, 320, direction="up", colour=S.CONC)
    b += [_t(559, 419, "Uma razão melhor devolve o leitor ao texto e ao problema.",
             22, anchor="middle")]
    return S.svg(1100, 440, p.get("title") or
                 "O problema orienta a leitura do livro; os lugares encontram perspectivas, a dialética confronta razões, uma solução provável permite decidir e uma objeção pode devolver a investigação ao mesmo texto", b), []


def _station(x, y, n, colour=S.INK):
    return [S.circle(x, y, 16, fill=S.PAPER, stroke=colour, stroke_width=1.6),
            _t(x, y + 6, str(n), 17, fill=colour, family=S.SANS, weight="600", anchor="middle")]


def _op(side, y, n, name, lines, colour=S.INK):
    """One operation of the Gribaldo sequence: a numbered station beside the folio, its name and its gloss."""
    cx = 330 if side == "l" else 770
    tx = 298 if side == "l" else 802
    a = "end" if side == "l" else None
    kw = {"anchor": a} if a else {}
    out = _station(cx, y, n, colour)
    out.append(_t(tx, y - 2, name, 24, fill=colour, font_style="italic", **kw))
    for i, line in enumerate(lines):
        out.append(_t(tx, y + 25 + i * 24, line, 19, fill=S.INK2, **kw))
    return out


def _leitura(p):
    b = [_t(550, 38, "Uma folha, oito operações", 27, anchor="middle")]
    rows = (160, 280, 400, 520)

    # One station line: down the left of the folio (1-4), under it, up the right (8-5). Numerals sit on the line.
    # (the line stops at each station's edge, so no numeral sits on a stroke)
    b += [_p("M330 536 V560 Q330 592 362 592 H738 Q770 592 770 560 V536", S.INK2, 1.3)]
    for y0, y1 in zip(rows, rows[1:]):
        b += [_p(f"M330 {y0 + 16} V{y1 - 16}", S.INK2, 1.3), _p(f"M770 {y0 + 16} V{y1 - 16}", S.INK2, 1.3)]
        ym = (y0 + y1) // 2
        b += _arrow(f"M330 {ym - 8} V{ym + 6}", 330, ym + 6, "down", S.INK2)
        b += _arrow(f"M770 {ym + 8} V{ym - 6}", 770, ym - 6, "up", S.INK2)
    b += _arrow("M540 592 H556", 556, 592, "right", S.INK2)

    b += _volume(372, 98, 356, 440)
    b += [_t(392, 128, "texto recebido", 19, fill=S.INK2),
          _t(570, 128, "texto relido", 19, fill=S.INK2)]
    # faint ruling over the whole page, then the darker lines of each operation's place
    for x in (390, 562):
        b += [S.line(x, y, x + 148, y, stroke=S.GRID, stroke_width=1, opacity=".6") for y in range(150, 520, 12)]
    for y in rows:
        b += [S.line(392, y - 24 + k * 12, 392 + w, y - 24 + k * 12, stroke=S.INK2, stroke_width=1.1, opacity=".55")
              for k, w in enumerate([146, 130, 140, 118])]
    # 2 divides (brackets), 3 reorders (an outline), 4 adds parallel cases in the foot of the page.
    b += [_p(f"M386 {rows[1] - 24} H380 V{rows[1] + 12} H386", S.INK2, 1.1),
          _p(f"M386 {rows[1] + 2} H380", S.INK2, 1.1),
          ]
    # the right page is the re-reading: top row (8) objections in the limit colour, the rest in the decided colour.
    for i, y in enumerate(rows):
        col = S.CONC if i == 0 else S.DIF
        b += [S.line(560, y - 24 + k * 12, 560 + w, y - 24 + k * 12, stroke=col, stroke_width=1.1, opacity=".55")
              for k, w in enumerate([146, 132, 140, 120])]
    b += [_p(f"M706 {rows[0] - 24} H712 V{rows[0] + 12} H706", S.CONC, 1.2)]

    # leaders from each station to its place on the folio
    for y, n in zip(rows, (1, 2, 3, 4)):
        b += [_p(f"M346 {y} H388", S.INK2, 1.1), S.circle(390, y, 3, fill=S.INK, stroke="none")]
    for y, n in zip(rows, (8, 7, 6, 5)):
        c = S.CONC if n == 8 else S.INK2
        b += [_p(f"M754 {y} H716", c, 1.1), S.circle(714, y, 3, fill=S.CONC if n == 8 else S.INK, stroke="none")]

    for y, n, name, lines in zip(rows, (1, 2, 3, 4), ("Praemitto", "Scindo", "Summo", "Casumque figuro"),
                                 (("Introduzir o texto;", "ensaiar a leitura literal."),
                                  ("Dividir as partes lógicas;", "definir e relacionar as figuras."),
                                  ("Reelaborar o texto", "numa ordenação sistemática."),
                                  ("Casos paralelos, exemplos", "e precedentes judiciais."))):
        b += _op("l", y, n, name, lines)
    for y, n, name, lines in zip(rows, (8, 7, 6, 5), ("Et obiicio", "Connoto", "Do causas", "Perlego"),
                                 (("Objeções e réplicas", "reabrem a interpretação."),
                                  ("Acrescentar brocardos", "e opiniões de juristas."),
                                  ("Natureza e diferença;", "origem e finalidade."),
                                  ("Reler à luz do contexto", "lógico e institucional construído."))):
        b += _op("r", y, n, name, lines, S.CONC if n == 8 else S.INK)
    return S.svg(1100, 630, p.get("title") or
                 "As oito operações de Gribaldo Mopha anotam uma única folha: leitura literal, divisão, ordenação, casos paralelos, releitura contextual, causas, autoridades, objeções e réplicas; o percurso desce a margem esquerda e sobe a direita", b), []


def _dot(x, y, colour=S.INK):
    return S.circle(x, y, 5, fill=S.PAPER, stroke=colour, stroke_width=1.6)


def _conceitos(p):
    # Genre: a Porphyrian tree. The ladder up (defining) and down (dividing) runs along the margins.
    b = [_t(550, 56, "relação jurídica", 30, anchor="middle"),
         _p("M550 82 V148", S.INK2, 1.4), _dot(550, 76), _dot(550, 154),
         _t(572, 122, "gênero", 18, fill=S.INK2, font_style="italic"),
         _t(550, 192, "contrato", 30, anchor="middle"),
         _t(550, 220, "direito e dever recíproco", 19, fill=S.INK2, anchor="middle"),
         _p("M550 236 V262 H178 M550 262 H940", S.INK2, 1.4), _dot(550, 232)]
    for x, name, note in ((178, "doação", "transferência gratuita"), (438, "compra e venda", "espécies do mesmo gênero"),
                          (699, "locação", ""), (940, "mútuo", "")):
        b += [_p(f"M{x} 262 V292", S.INK2, 1.3), _dot(x, 298),
              _t(x, 338, name, 26, anchor="middle")]
        if note:
            b.append(_t(x, 364, note, 18, fill=S.INK2, anchor="middle"))
    # the two movements, carried along the margins
    b += [_p("M60 298 V92", S.DIF, 1.8), *_arrow("M60 108 V92", 60, 92, "up", S.DIF),
          _t(84, 170, "Definir", 27, fill=S.DIF),
          _t(84, 202, "integrar a espécie", 20), _t(84, 228, "num gênero maior", 20),
          _p("M1040 92 V298", S.DIF, 1.8), *_arrow("M1040 282 V298", 1040, 298, "down", S.DIF),
          _t(1016, 170, "Dividir", 27, fill=S.DIF, anchor="end"),
          _t(1016, 202, "distinguir espécies", 20, anchor="end"), _t(1016, 228, "dentro de um gênero", 20, anchor="end")]
    # Other divisions of the same genus, by other criteria: two small forks hung apart from the species row.
    b += [_p("M111 398 H989", S.GRID, 1),
          _t(550, 428, "Outras divisões do gênero contrato, por critérios diferentes", 21, fill=S.INK2, anchor="middle")]
    for cx, a, c in ((306, "formais", "consensuais"), (801, "unilaterais", "bilaterais")):
        b += [_dot(cx, 450), _p(f"M{cx} 456 C{cx} 470 {cx - 76} 466 {cx - 76} 480 M{cx} 456 C{cx} 470 {cx + 76} 466 {cx + 76} 480", S.INK2, 1.3),
              _t(cx - 76, 508, a, 23, anchor="middle"), _t(cx + 76, 508, c, 23, anchor="middle")]
    return S.svg(1100, 530, p.get("title") or
                 "No exemplo lógico de Hespanha, a definição sobe da espécie ao gênero e a divisão desce do gênero às espécies; relação jurídica, contrato e contratos particulares formam uma hierarquia, enquanto duas outras divisões de contrato empregam critérios diferentes", b), []


def _tally(x, y, n, colour=S.INK, per_row=7):
    """Tally marks: gates of five (four strokes and a slash), the remainder as loose strokes."""
    out, groups = [], [5] * (n // 5) + ([n % 5] if n % 5 else [])
    for i, g in enumerate(groups):
        gx, gy = x + (i % per_row) * 48, y + (i // per_row) * 40
        for k in range(min(g, 4)):
            out.append(S.line(gx + k * 8, gy, gx + k * 8, gy + 28, stroke=colour, stroke_width=2.4, stroke_linecap="round"))
        if g == 5:
            out.append(S.line(gx - 5, gy + 23, gx + 29, gy + 5, stroke=colour, stroke_width=2.4, stroke_linecap="round"))
    return out


def _baldo(p):
    # Genre: a tally sheet. Length carries the count, as the book counts the citations (Hespanha p. 472).
    b = [_t(0, 38, "Aristóteles", 26), _t(370, 40, "103", 34, anchor="end", weight="600"),
         _p("M0 52 H370", S.GRID, 1), *_tally(6, 74, 103),
         _t(0, 222, "Cícero", 26, fill=S.INK2), _t(370, 224, "17", 34, anchor="end", weight="600", fill=S.INK2),
         _p("M0 236 H370", S.GRID, 1), *_tally(6, 258, 17, S.INK2),
         _t(0, 336, "citações nos comentários de Baldo", 14, fill=S.INK2, family=S.SANS)]
    return S.svg(370, 350, p.get("title") or
                 "Nos comentários de Baldo, Aristóteles é citado 103 vezes e Cícero 17: cento e três marcas contra dezessete", b), []


def _opinio(p):
    """One cord of opinions down a tall margin: the working book at the top, then one zone per step of the text.

    Zones are 480 units high and the page gives each step the same height, so every state sits beside its paragraph.
    State 1 hangs one leaf on the cord, state 2 binds three into a thick strand, state 3 cuts it with a counter-leaf."""
    s = p.get("state", 1)
    if not isinstance(s, int) or isinstance(s, bool) or not 1 <= s <= 3:
        raise ValueError("topica_mj: opinio state must be an integer from 1 to 3")
    Z = 480

    def leaf(x, y, colour=S.INK, ink=S.GRID):
        return [S.rect(x + 3, y + 4, 80, 80, fill=S.PAPER, stroke=S.GRID, stroke_width=1),
                S.rect(x, y, 80, 80, fill=S.PAPER, stroke=colour, stroke_width=1.5),
                *[S.line(x + 12, y + 22 + i * 13, x + 12 + w, y + 22 + i * 13, stroke=ink, stroke_width=1)
                  for i, w in enumerate((54, 46, 52))]]

    # zone 1: the book under discussion and one expert's leaf
    z1 = _volume(55, 34, 260, 122)
    z1 += [_t(71, 74, "solução", 21), _t(71, 102, "provável", 21),
           *_writing(72, 120, [92, 80], 11), *_writing(204, 62, [92, 82, 90, 78, 88], 12),
           _p("M185 168 V236", S.INK2, 1.5), _dot(185, 232),
           *leaf(145, 242),
           _t(245, 276, "parecer de", 20), _t(245, 301, "um perito", 20),
           _p(f"M185 326 V{Z + 52}", S.INK2, 1.5),
           _t(206, 380, "o número ainda", 19, fill=S.INK2), _t(206, 405, "não decide", 19, fill=S.INK2)]
    out = list(z1)
    if s >= 2:
        # three leaves bound into one strand; the middle one is the expert of state 1
        z2 = [*leaf(30, Z + 52), *leaf(260, Z + 52), *leaf(145, Z + 52),
              _p(f"M70 {Z + 138} C70 {Z + 172} 185 {Z + 160} 185 {Z + 204}", S.INK2, 1.5),
              _p(f"M330 {Z + 138} C330 {Z + 172} 185 {Z + 160} 185 {Z + 204}", S.INK2, 1.5),
              _p(f"M185 {Z + 138} V{Z + 204}", S.INK2, 1.5),
              S.circle(185, Z + 204, 5, fill=S.INK, stroke="none"),
              _p(f"M185 {Z + 204} V{2 * Z + 150}", S.INK, 3.4),
              _t(210, Z + 262, "opinio", 23, font_style="italic"), _t(210, Z + 290, "communis", 23, font_style="italic"),
              _t(210, Z + 346, "uma direção", 19, fill=S.INK2), _t(210, Z + 371, "compartilhada", 19, fill=S.INK2)]
        out += _f(z2, s == 2)
    if s >= 3:
        y0 = 2 * Z
        z3 = [*leaf(262, y0 + 42, S.CONC, S.CONC),
              _p(f"M262 {y0 + 106} C220 {y0 + 118} 206 {y0 + 142} 190 {y0 + 160}", S.CONC, 1.8),
              _p(f"M200 {y0 + 160} L190 {y0 + 160} L192 {y0 + 148}", S.CONC, 1.8),
              _p(f"M171 {y0 + 150} L199 {y0 + 172} M171 {y0 + 164} L199 {y0 + 186}", S.CONC, 1.6),
              _p(f"M185 {y0 + 190} V{y0 + 380}", S.INK2, 1.6, stroke_dasharray="6 6"),
              _t(185, y0 + 424, "concordância admite erro", 20, fill=S.CONC, anchor="middle")]
        out += _f(z3, s == 3)
    return S.svg(370, 3 * Z, p.get("title") or
                 ["Um parecer perito entra na discussão sem que muitos seguidores provem sua correção",
                  "Opiniões admitidas convergem e orientam a interpretação como opinio communis",
                  "Uma objeção continua a poder contrariar a opinião comum: a concordância não produz infalibilidade"][s - 1], out), []


MODES = {"lugares": _lugares, "percurso": _percurso, "leitura": _leitura,
         "conceitos": _conceitos, "opinio": _opinio, "baldo": _baldo}


def build(p: dict) -> tuple[str, list[dict]]:
    mode = p.get("mode")
    if mode not in MODES:
        raise ValueError(f"topica_mj: mode must be one of {', '.join(MODES)}")
    return MODES[mode](p)
