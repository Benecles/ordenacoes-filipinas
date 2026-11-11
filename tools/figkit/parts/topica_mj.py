"""topica_mj: one received volume read, argued over and read again.

Params (reading mode and optional accessible title, never coordinates):
  mode   lugares | percurso | leitura | conceitos | opinio (required)
  title  optional accessible description replacing the mode's default
  state  opinio only: 1 (individual opinion), 2 (shared direction),
         3 (Cino's objection to infallibility). The page puts each state
         inside a .panel and its paragraphs in .step[data-panel].

Canvases: lugares 1100x560; percurso 1100x440; leitura 1100x650;
conceitos 1100x470; opinio 320x378.
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
    b += [_p("M395 108 H555 C606 108 607 161 661 183", S.INK2, 1.3),
          _p("M395 160 H555 C606 160 617 177 661 192", S.INK2, 1.3),
          _p("M395 209 H555 C606 209 617 206 661 201", S.INK2, 1.3),
          _p("M395 261 H555 C606 261 607 227 661 210", S.INK2, 1.3),
          _t(722, 121, "Confrontar", 24, anchor="middle"),
          _t(722, 149, "razões", 24, anchor="middle")]
    # The crossing and opposite arrowheads depict arguments that can resist
    # one another. No formal judgment is fabricated by the drawing.
    b += _arrow("M649 184 L772 223", 772, 223)
    b += _arrow("M772 181 L649 222", 649, 222, direction="left")
    b += [_t(712, 262, "premissas discutíveis", 19, fill=S.INK2,
             anchor="middle")]
    b += _arrow("M780 202 H861", 861, 202)

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


def _annotation(x, y, heading, lines):
    return [_t(x, y, heading, 23),
            *[_t(x, y + 29 + i * 25, line, 19)
              for i, line in enumerate(lines)]]


def _leader(d, x, y):
    return [_p(d, S.INK2, 1.1),
            S.circle(x, y, 2.8, fill=S.INK, stroke="none")]


def _leitura(p):
    b = [_t(550, 34, "Uma folha, oito operações", 27, anchor="middle")]

    # The progression starts at upper left, descends the left margin,
    # crosses the foot and ascends the right margin. The physical order
    # preserves Gribaldo's sequence without eight equal explanatory cards.
    b += _annotation(24, 73, "1 · Praemitto", (
        "Introduzir o texto;", "ensaiar a leitura literal."))
    b += _annotation(24, 247, "2 · Scindo", (
        "Dividir as partes lógicas;", "definir e relacionar as figuras."))
    b += _annotation(24, 433, "3 · Summo", (
        "Reelaborar o texto", "numa ordenação sistemática."))
    b += _annotation(255, 560, "4 · Casumque figuro", (
        "Casos paralelos, exemplos", "e precedentes judiciais."))
    b += _annotation(620, 560, "5 · Perlego", (
        "Reler à luz do contexto", "lógico e institucional construído."))
    b += _annotation(805, 433, "6 · Do causas", (
        "Natureza e diferença;", "origem e finalidade."))
    b += _annotation(805, 247, "7 · Connoto", (
        "Acrescentar brocardos", "e opiniões de juristas."))
    b += _annotation(805, 73, "8 · Et obiicio", (
        "Objeções e réplicas", "reabrem a interpretação."))

    b += _volume(336, 179, 426, 308)
    b += [_t(354, 216, "texto recebido", 21),
          _t(569, 216, "texto relido", 21),
          *_writing(356, 236, [168, 155, 163, 158], 12),
          *_writing(367, 302, [157, 148, 155], 12),
          *_writing(367, 360, [153, 159, 147], 12),
          *_writing(356, 420, [166, 151, 159], 12),
          _p("M361 299 H355 V329 H361 M361 357 H355 V387 H361", S.INK2, 1),
          _t(570, 258, "contexto", 20),
          *_writing(570, 275, [164, 153], 12),
          _t(570, 329, "causas", 20),
          *_writing(570, 345, [159, 153], 12),
          _t(570, 400, "autoridades", 20),
          *_writing(570, 416, [163, 151], 12),
          _t(570, 464, "objeções", 20)]

    # Leaders touch text zones, division marks and the reader's evolving
    # margin. They are annotations of one folio, not a chain of new objects.
    b += _leader("M260 135 C290 135 301 236 352 236", 352, 236)
    b += _leader("M301 318 H320 C333 318 333 312 352 312", 352, 312)
    b += _leader("M284 468 C309 468 317 425 352 425", 352, 425)
    b += _leader("M458 536 C458 512 427 504 427 452", 427, 452)
    b += _leader("M710 536 C710 515 740 508 740 287", 740, 287)
    b += _leader("M789 465 C780 465 786 331 737 331", 737, 331)
    b += _leader("M789 287 C779 287 786 401 736 401", 736, 401)
    # The last operation returns to the developed reading at the page's
    # end: the long marginal leader makes the reopening visibly deliberate.
    b += _leader("M805 135 H788 V464 H737", 737, 464)

    # Small directional cues, outside the writing, make the numerals' tour
    # unambiguous without surrounding the page with a decorative loop.
    b += _arrow("M39 157 V201", 39, 201, direction="down", colour=S.INK2)
    b += _arrow("M39 331 V388", 39, 388, direction="down", colour=S.INK2)
    b += _arrow("M73 520 C92 543 149 550 224 550", 224, 550, colour=S.INK2)
    b += _arrow("M544 568 H592", 592, 568, colour=S.INK2)
    b += _arrow("M953 539 C1000 531 1068 529 1068 497", 1068, 497,
                direction="up", colour=S.INK2)
    b += _arrow("M1071 395 V334", 1071, 334, direction="up", colour=S.INK2)
    b += _arrow("M1071 207 V157", 1071, 157, direction="up", colour=S.INK2)
    return S.svg(1100, 650, p.get("title") or
                 "As oito operações de Gribaldo Mopha anotam uma única folha: leitura literal, divisão, ordenação, casos paralelos, releitura contextual, causas, autoridades, objeções e réplicas; o percurso desce a margem esquerda e sobe a direita", b), []


def _conceitos(p):
    b = [_t(550, 83, "relação jurídica", 29, anchor="middle"),
          _p("M550 97 V155", S.INK2, 1.4),
          _t(575, 127, "gênero", 18, fill=S.INK2),
          _t(550, 185, "contrato", 29, anchor="middle"),
          _t(550, 216, "direito e dever recíproco", 19, fill=S.INK2,
             anchor="middle"),
          _p("M550 230 V258 H178 M550 258 H940", S.INK2, 1.4)]
    for x, name in ((178, "doação"), (438, "compra e venda"),
                    (699, "locação"), (940, "mútuo")):
        b += [_p(f"M{x} 258 V287", S.INK2, 1.3),
              _t(x, 318, name, 25, anchor="middle")]
    b += [_t(178, 347, "transferência gratuita", 19, fill=S.INK2,
             anchor="middle"),
          _t(438, 347, "espécies do mesmo gênero", 18, fill=S.INK2,
             anchor="middle"),
          _t(28, 100, "Definir", 25),
          _t(28, 129, "integrar a espécie", 20),
          _t(28, 155, "num gênero maior", 20),
          _t(864, 100, "Dividir", 25),
          _t(864, 129, "distinguir espécies", 20),
          _t(864, 155, "dentro de um gênero", 20)]
    b += _arrow("M92 246 V184", 92, 184, direction="up", colour=S.INK2)
    b += _arrow("M1010 184 V246", 1010, 246, direction="down", colour=S.INK2)

    # These are OTHER divisions of the SAME genus, using independent
    # criteria. A separate open baseline prevents reading them as descendants
    # of the donation/sale/lease/loan labels or as one four-way partition.
    b += [_p("M111 378 H989", S.GRID, 1),
          _t(550, 406, "Outras divisões do gênero contrato, por critérios diferentes", 21,
             anchor="middle"),
          _t(306, 447, "formais / consensuais", 23, anchor="middle"),
          _t(801, 447, "unilaterais / bilaterais", 23, anchor="middle"),
          _p("M306 419 V427 M801 419 V427", S.INK2, 1.3)]
    return S.svg(1100, 470, p.get("title") or
                 "No exemplo lógico de Hespanha, a definição sobe da espécie ao gênero e a divisão desce do gênero às espécies; relação jurídica, contrato e contratos particulares formam uma hierarquia, enquanto duas outras divisões de contrato empregam critérios diferentes", b), []


def _opinio(p):
    """Loose opinions are brought together in a revisable working book."""
    s = p.get("state", 1)
    if not isinstance(s, int) or isinstance(s, bool) or not 1 <= s <= 3:
        raise ValueError("topica_mj: opinio state must be an integer from 1 to 3")
    b = []
    # These ordinary manuscript leaves belong to one field of debate. Their
    # differing lengths do not imply a vote or measurable units of authority.
    for x, y, w, lengths in ((14, 27, 79, [53, 48, 51]),
                              (117, 14, 83, [57, 50, 55]),
                              (228, 37, 76, [49, 43, 47])):
        if s == 1 and x != 117:
            continue
        leaf = [S.rect(x + 3, y + 4, w, 76, fill=S.PAPER, stroke=S.GRID,
                       stroke_width=1),
                S.rect(x, y, w, 76, fill=S.PAPER, stroke=S.INK,
                       stroke_width=1.4)]
        leaf += _writing(x + 11, y + 20, lengths, 12)
        b += _f(leaf, s == 2 and x != 117)
    # A broad margin in the shared book remains available for contradiction.
    b += _volume(31, 183, 258, 123)
    b += [_t(45, 215, "solução", 20),
          _t(45, 242, "provável", 20),
          *_writing(46, 260, [90, 80], 11),
          *_writing(180, 211, [89, 80, 87, 77, 90], 12)]
    if s == 1:
        b += _arrow("M158 99 V119 M158 154 V171", 158, 171,
                    direction="down", colour=S.INK2)
        b += [_t(160, 145, "parecer de um perito", 19, anchor="middle"),
              _t(160, 357, "o número ainda não decide", 19, anchor="middle")]
    else:
        b += _f([_p("M54 112 C54 128 119 124 144 132 M158 99 V132 M266 122 C266 129 196 128 176 132", S.INK2, 1.4),
                 _t(160, 158, "opinio communis", 22, anchor="middle")], s == 2)
        if s == 2:
            b += _f([_p("M45 286 H138 M45 289 H126", S.INK2, 1.3),
                     _t(160, 347, "uma direção compartilhada", 19, anchor="middle")])
        else:
            # The objection has its own route into the accumulated argument;
            # its reasoning, rather than a numerical weight, remains decisive.
            b += _f([S.path("M222 285 L303 270 V328 H222 Z", fill=S.PAPER,
                            stroke=S.CONC, stroke_width=1.5),
                     _p("M233 296 l55 -10 M233 307 l48 -8 M233 318 l55 -10", S.CONC, 1.1),
                     _p("M225 280 C202 278 209 256 187 252", S.CONC, 1.7),
                     _p("M193 248 L187 252 L194 257", S.CONC, 1.7),
                     _t(160, 358, "concordância admite erro", 20, fill=S.CONC, anchor="middle")])
    return S.svg(320, 378, p.get("title") or
                 ["Um parecer perito entra na discussão sem que muitos seguidores provem sua correção",
                  "Opiniões admitidas convergem e orientam a interpretação como opinio communis",
                  "Uma objeção continua a poder contrariar a opinião comum: a concordância não produz infalibilidade"][s - 1], b), []


MODES = {"lugares": _lugares, "percurso": _percurso, "leitura": _leitura,
         "conceitos": _conceitos, "opinio": _opinio}


def build(p: dict) -> tuple[str, list[dict]]:
    mode = p.get("mode")
    if mode not in MODES:
        raise ValueError(f"topica_mj: mode must be one of {', '.join(MODES)}")
    return MODES[mode](p)
