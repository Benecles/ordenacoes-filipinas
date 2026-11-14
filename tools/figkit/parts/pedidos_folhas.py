"""pedidos_folhas: the drawings of the Aula 01.2 companion (Pedidos, causas e controle da inicial).

Params: mode (required) = hero | vias | perecimento | indivisivel | cumulo | recurso | leitura | dispositivo | tutela |
        controle | estabilidade | discovery; stepped = optional panel-id prefix (one whole drawing per state).

One vocabulary: Cecilia's sewing machine, a coin for the money equivalent, a receipt for the rent, sheets of the
autos. A thing keeps its drawing from the petition to the decision, so what changes is where it sits (inside or
outside a vinculo, under a cover, lifted off the autos), never what it looks like. Blue is what was decided, orange
the limit, dashed grey what stays in reserve. Every drawing is composed from the facts of the passage it sits
beside (Marinoni, Arenhart e Mitidiero v.2 pp.144-168; Didier v.1 pp.622-665; Mitidiero 2022 pp.153-176; CPC).
"""
from __future__ import annotations

from . import svg as S


def T(x, y, s, size=16, fill=S.INK, family=S.SERIF, **kw):
    return S.text(x, y, s, size=size, family=family, fill=fill, **kw)


def L(x, y, s, size=12.5, fill=S.INK2, **kw):
    return S.text(x, y, s, size=size, family=S.MONO, fill=fill, letter_spacing=".05em", **kw)


def P(d, color=S.INK, width=1.5, **kw):
    return S.path(d, fill="none", stroke=color, stroke_width=width, stroke_linecap="round", stroke_linejoin="round", **kw)


def dot(x, y, hollow=True, color=S.INK, r=5):
    return S.circle(x, y, r, fill=S.PAPER if hollow else color, stroke=color, stroke_width=1.6)


def tick(x, y, color=S.DIF, w=2.4):
    return P(f"M{x} {y} l5 6 l11 -14", color, w)


def cross(x, y, r=9, color=S.CONC, w=2.6):
    return P(f"M{x - r} {y - r} l{2 * r} {2 * r} M{x + r} {y - r} l{-2 * r} {2 * r}", color, w)


def sheet(x, y, w, h, color=S.INK):
    return [S.rect(x + 5, y + 6, w, h, fill=S.PAPER, stroke=S.GRID, stroke_width=1),
            S.rect(x, y, w, h, fill=S.PAPER, stroke=color, stroke_width=1.5)]


def g(x, y, k, parts):
    return [f'<g transform="translate({x:g} {y:g}) scale({k:g})">' + "".join(parts) + "</g>"]


def dash(on):
    return {"stroke_dasharray": "4 4"} if on else {}


# ───────────── the objects (each drawn in a 70 x 52 box, origin top-left) ─────────────

def machine(x, y, k=1.0, c=S.INK, ghost=False, fill=None):
    w = 1.7 / k
    fl = fill or S.PAPER
    body = S.path("M8 4 H62 V36 H68 V50 H2 V38 H50 V18 H22 V24 H8 Z", fill=fl, stroke=c, stroke_width=w,
                  stroke_linejoin="round", **dash(ghost))
    return g(x, y, k, [body, P("M15 24 V38", c, w, **dash(ghost)), S.circle(65, 12, 6, fill=fl, stroke=c, stroke_width=w),
                       P("M10 10 H50", c, w * .7, **dash(ghost))])


def coin(x, y, r=15, c=S.INK, ghost=False):
    d = dash(ghost)
    return [S.circle(x, y, r, fill=S.PAPER, stroke=c, stroke_width=1.7, **d),
            S.circle(x, y, r * .62, fill="none", stroke=c, stroke_width=1.2, **d), P(f"M{x} {y - r * .3} V{y + r * .3}", c, 1.4)]


def receipt(x, y, k=1.0, c=S.INK, ghost=False):
    """The rent receipt: a slip with a torn edge and two ruled lines. Origin top-left, 40 x 54."""
    w = 1.7 / k
    body = S.path("M0 0 H40 V50 L35 54 L30 49 L25 54 L20 49 L15 54 L10 49 L5 54 L0 50 Z", fill=S.PAPER, stroke=c,
                  stroke_width=w, stroke_linejoin="round", **dash(ghost))
    return g(x, y, k, [body, P("M7 12 H33", c, w * .7), P("M7 22 H33", c, w * .7), P("M7 32 H22", c, w * .7)])


def person(x, y, c=S.INK, k=1.0):
    return g(x, y, k, [S.circle(10, 7, 6, fill=S.PAPER, stroke=c, stroke_width=1.6),
                       S.path("M0 28 Q0 15 10 15 Q20 15 20 28 Z", fill=S.PAPER, stroke=c, stroke_width=1.6)])


def block(x, y, w=34, h=24, c=S.INK2):
    """A seizable asset: a hatched block."""
    return [S.rect(x, y, w, h, fill=S.PAPER, stroke=c, stroke_width=1.6), *S.hatch(x, y, w, h, 7, stroke=c, stroke_width=1)]


def house(x, y, w=120, h=64, c=S.INK2):
    return [P(f"M{x} {y + 22} L{x + w / 2} {y} L{x + w} {y + 22} V{y + h} H{x} Z", c, 1.7)]


def caption_tag(x, y, s, fill=S.INK2, anchor=None, size=13.5):
    return T(x, y, s, size, fill, anchor=anchor)


# ───────────────────────────── hero ─────────────────────────────

def hero(p):
    W, H = 1120, 470
    PX, PW = 14, 270
    CX0, CW = 294, 152
    DX, DW = 910, 198
    top, bot, sh = 14, 456, 112
    ys = (258, 338, 418)
    b = []
    stages = [("interpretar", "art. 322, § 2º", ["Lê-se a petição inteira,", "segundo a boa-fé."]),
              ("corrigir", "arts. 321 e 330", ["Emenda em 15 dias", "úteis; sem ela,", "indeferimento."]),
              ("estabilizar", "art. 329", ["Livre até a citação;", "depois, só com o réu;", "após o saneamento,", "pela convenção do", "art. 190."]),
              ("julgar", "arts. 141 e 492", ["Congruência: nada", "além, fora nem aquém", "do pedido."])]
    for i, (name, art, lines) in enumerate(stages):
        x = CX0 + i * CW
        b.append(S.rect(x, top, CW, bot - top, fill=S.PAPER2 if i % 2 == 0 else S.PAPER, stroke=S.GRID, stroke_width=1))
        b += [dot(x + 20, 40, True, S.INK, 9), T(x + 20, 45.5, str(i + 1), 13, S.INK, family=S.MONO, anchor="middle"),
              T(x + 38, 46, name, 20), T(x + 12, 70, art, 13.5, S.INK, family=S.MONO)]
        for k, ln in enumerate(lines):
            b.append(T(x + 12, 94 + k * 17, ln, 13.5, S.INK2))
    x3 = CX0 + 2 * CW
    t1, t2 = x3 + 50, x3 + 100
    zy = 196
    b += [P(f"M{x3 + 12} {zy} H{t1}", S.DIF, 3), P(f"M{t1} {zy} H{t2}", S.INK2, 3), P(f"M{t2} {zy} H{x3 + CW - 12}", S.CONC, 3),
          P(f"M{t1} {zy - 7} V{zy + 7}", S.INK, 1.4), P(f"M{t2} {zy - 7} V{zy + 7}", S.INK, 1.4),
          T(t1, zy - 12, "citação", 12.5, S.INK, anchor="middle"), T(t2 + 4, zy + 22, "saneamento", 12.5, S.INK, anchor="middle")]
    b += [*sheet(PX, sh, PW, bot - sh), *sheet(DX, sh, DW, bot - sh)]
    b += [T(PX + 16, sh + 36, "Petição de Cecília", 22), T(PX + 16, sh + 58, "máquina retida · aluguel de outra", 13.5, S.INK2),
          P(f"M{PX + 16} {sh + 70} H{PX + PW - 16}", S.GRID, 1),
          T(DX + 16, sh + 36, "Dispositivo", 22), P(f"M{DX + 16} {sh + 70} H{DX + DW - 16}", S.GRID, 1)]
    ent, eq, reem = ys
    rows = [(ent, "entrega da máquina", ["pedido principal"]),
            (eq, "equivalente em dinheiro", ["subsidiário: só se o", "principal for rejeitado", "(art. 326)"]),
            (reem, "reembolso do aluguel", ["cumulado com a entrega:", "cumulação simples"])]
    for y, nm, rl in rows:
        b.append(T(PX + 88, y - 14 if len(rl) > 1 else y - 4, nm, 15.5 if len(nm) > 20 else 17))
        base = y + 2 if len(rl) > 1 else y + 16
        for k, ln in enumerate(rl):
            b.append(T(PX + 88, base + k * 15, ln, 13, S.INK2))
    x_in, x_out = PX + PW, DX
    b += [*machine(PX + 16, ent - 22, .8), *coin(PX + 40, eq, 15), *receipt(PX + 26, reem - 24, .85)]
    b += [P(f"M{x_in} {ent} H{x_out}", S.DIF, 2.6), P(f"M{x_in} {reem} H{x_out}", S.DIF, 2.6),
          P(f"M{x_in} {eq} H{x_out}", S.INK2, 1.8, stroke_dasharray="6 5")]
    for y in ys:
        for i in range(4):
            b.append(dot(CX0 + i * CW + CW / 2, y, True, S.INK if y != eq else S.INK2, 4.5))
        b += [dot(x_in, y, False, S.INK), dot(x_out, y, False, S.INK)]
    b.append(P(f"M{t2} 232 V{bot - 12}", S.CONC, 4))
    b += [*machine(DX + 18, ent - 22, .8), *coin(DX + 42, eq, 15, S.INK2, True), *receipt(DX + 28, reem - 24, .85)]
    b += [T(DX + 88, ent + 4, "examinada", 13, S.INK2), T(DX + 88, ent + 19, "primeiro", 13, S.INK2),
          T(DX + 74, eq - 10, "examinado se a", 13, S.INK2), T(DX + 74, eq + 5, "entrega for", 13, S.INK2), T(DX + 74, eq + 20, "rejeitada", 13, S.INK2),
          T(DX + 76, reem - 6, "julgado à parte,", 13, S.INK2), T(DX + 76, reem + 9, "seja qual for o", 13, S.INK2), T(DX + 76, reem + 24, "da entrega", 13, S.INK2)]
    return S.svg(W, H, "A petição de Cecília leva a máquina, o equivalente em dinheiro e o recibo do aluguel pelos quatro controles, interpretar, corrigir, estabilizar e julgar; a máquina e o recibo chegam ao dispositivo como foram pedidos e o equivalente fica em reserva", b)


# ───────────────────────────── vias ─────────────────────────────

def vias(p):
    W, H = 1084, 380
    SX, SW = 16, 236
    EX = 946
    A, B, C = 96, 176, 306
    b = [*sheet(SX, 22, SW, 336), *sheet(EX, 22, W - EX - 14, 336)]
    b += [T(SX + 18, 58, "Sentença", 23), P(f"M{SX + 18} 70 H{SX + 190}", S.GRID, 1),
          T(EX + 14, 58, "Satisfação", 19), P(f"M{EX + 14} 70 H{W - 34}", S.GRID, 1)]
    for y, name, sub in [(A, "mandamental", "ordem de entrega, com multa"), (B, "executiva", "busca e apreensão"), (C, "condenatória", "reembolso do aluguel")]:
        b += [T(SX + 18, y + 2, name, 19), T(SX + 18, y + 21, sub, 13.5, S.INK2)]
    x0 = SX + SW
    # intrinsic: both reach the workshop, only one of them goes in; the machine leaves through one door
    hx, hy, hw, hh = 500, 82, 130, 104
    b += house(hx, hy, hw, hh)
    b += machine(hx + 34, hy + 52, .8)
    b += [P(f"M{x0} {A} H392 Q440 {A} 456 128 H{hx - 2}", S.DIF, 2.6), dot(x0, A, False)]
    for i in range(3):
        cx = 460 + i * 13
        b.append(P(f"M{cx} 121 l7 7 l-7 7", S.DIF, 2))
    b += [P(f"M{x0} {B} H400 Q440 {B} 470 168 L{hx + 28} 158", S.DIF, 2.6), dot(x0, B, False), dot(hx + 28, 158, False, S.DIF, 4.5)]
    b += [P(f"M{hx + hw} 160 H{EX - 6}", S.DIF, 2.6), dot(EX - 6, 160)]
    b += machine(720, 142, .6) + machine(EX + 22, 134, 1.0)
    b += [T(EX + 14, 204, "a obrigação", 13.5, S.INK2), T(EX + 14, 220, "cumprida", 13.5, S.INK2)]
    b += [T(SX + SW + 20, 44, "executividade intrínseca", 16, S.DIF),
          T(x0 + 22, A - 22, "a multa pressiona a oficina", 13.5, S.INK2), T(x0 + 22, A - 7, "a devolver a máquina", 13.5, S.INK2),
          T(x0 + 22, B + 26, "a busca e apreensão vai buscá-la,", 13.5, S.INK2), T(x0 + 22, B + 42, "sem outro processo", 13.5, S.INK2)]
    # extrinsic: a gate, then the account becomes a seizure and the seizure becomes money
    xa, xb = 292, 346
    b += [P(f"M{x0} {C} H{xa - 5}", S.INK2, 1.8), dot(x0, C, False), P(f"M{xa} {C} L{xb - 8} {C - 21}", S.INK2, 1.8),
          dot(xa, C, True, S.INK2), dot(xb, C, True, S.INK2), P(f"M{xb + 5} {C} H{EX - 20}", S.INK2, 1.8),
          T((xa + xb) / 2, C + 30, "só se a oficina", 13.5, S.INK2, anchor="middle"), T((xa + xb) / 2, C + 46, "deixar de pagar", 13.5, S.INK2, anchor="middle"),
          T(xa - 20, C - 62, "executividade extrínseca", 16, S.INK2)]
    st = [(442, "liquidação", ["só se a sentença", "for genérica"]), (546, "requerimento", ["a oficina é", "intimada a pagar"]),
          (650, "impugnação", ["a oficina", "pode impugnar"]), (754, "penhora", ["localização e", "penhora de bens"]),
          (858, "expropriação", ["adjudicação,", "alienação", "ou frutos"])]
    for x, name, sub in st:
        b.append(T(x, C - 34, name, 15.5, S.MUTED if name == "liquidação" else S.INK, anchor="middle"))
        for k, ln in enumerate(sub):
            b.append(T(x, C + 36 + k * 15, ln, 13, S.INK2, anchor="middle"))
    b += receipt(442 - 13, C - 20, .55, S.INK2, True)
    b += [S.rect(546 - 11, C - 14, 22, 28, fill=S.PAPER, stroke=S.INK2, stroke_width=1.6), P(f"M{546 - 6} {C - 6} H{546 + 6} M{546 - 6} {C + 2} H{546 + 6}", S.INK2, 1.2)]
    b += [S.rect(650 - 5, C - 16, 10, 32, fill=S.PAPER, stroke=S.INK2, stroke_width=1.6)]
    b += block(754 - 17, C - 12) + [S.circle(754 + 17, C - 12, 7, fill=S.PAPER, stroke=S.CONC, stroke_width=1.8), P(f"M{754 + 13} {C - 12} H{754 + 21}", S.CONC, 1.6)]
    b += block(858 - 38, C - 12, 26, 22) + [P(f"M{858 - 8} {C} H{858 - 2}", S.INK2, 1.4)] + coin(858 + 8, C, 9) + coin(858 + 26, C, 9) + coin(858 + 44, C, 9)
    b += coin(EX + 70, C, 17)
    b += [T(EX + 14, C + 36, "declarada", 13.5, S.INK2), T(EX + 14, C + 52, "por sentença", 13.5, S.INK2)]
    return S.svg(W, H, "A ordem de entrega com multa e a busca e apreensão levam à mesma máquina; a condenação ao reembolso só chega ao dinheiro depois de liquidação eventual, requerimento, impugnação, penhora e expropriação", b)



# ───────────────────────────── 01: perecimento and indivisível ─────────────────────────────

def _vinculo(x, y, w, h, c=S.INK, broken=False):
    if broken:
        return [P(f"M{x} {y + 30} V{y} H{x + w} V{y + 30}", c, 2, stroke_dasharray="6 5"),
                P(f"M{x} {y + 50} V{y + h} H{x + w} V{y + h - 36}", c, 2, stroke_dasharray="6 5")]
    return [S.rect(x, y, w, h, fill="none", stroke=c, stroke_width=2, rx=8)]


def perecimento(p, st):
    on_a, on_b, per = st != 2, st != 1, st == 3
    ca = S.INK if on_a else S.GRID
    cb = S.INK if on_b else S.GRID
    la = S.INK if on_a else S.MUTED
    lb = S.INK if on_b else S.MUTED
    b = [T(18, 26, "alternativa", 20, la)]
    b += _vinculo(16, 40, 348, 110, ca)
    b += machine(44, 62, 1, ca, per) + machine(208, 62, 1, ca, False)
    b += [T(44, 134, "devolver a máquina", 14.5, la), T(208, 134, "entregar outra equivalente", 14.5, la)]
    if per:
        b += [cross(79, 88), tick(300, 96)]
    b += [T(18, 196, "faculdade de substituição", 20, lb)]
    b += _vinculo(16, 210, 190, 110, cb if not per else S.CONC, broken=per)
    b += machine(44, 232, 1, cb, False)
    b += coin(290, 266, 22, cb if on_b else S.GRID, True)
    b += [T(44, 304, "devolver a máquina", 14.5, lb), T(290, 312, "ou pagar seu valor", 14.5, lb, anchor="middle"),
          P("M212 266 H264", cb, 1.4, stroke_dasharray="3 4")]
    if per:
        b += [cross(79, 258)]
    return S.svg(380, 336, "Na alternativa, duas máquinas presas ao vínculo: perdida uma, resta a outra. Na faculdade de substituição, uma só máquina presa e o dinheiro fora do vínculo: perdida a máquina, o vínculo fica sem objeto", b)


def indivisivel(p):
    b = []
    xs = (64, 190, 316)
    for i, x in enumerate(xs):
        c = S.DIF if i == 0 else S.INK2
        b += person(x - 10, 14, c, 1.1)
        b.append(P(f"M{x} 48 C{x} 84 {170 + i * 20} 74 {170 + i * 20} 108", c, 1.5))
    b += machine(146, 106, 1.3)
    b += [T(190, 196, "um só objeto: cada credor pode reclamar o todo", 14.5, S.INK2, anchor="middle"), P("M16 214 H364", S.GRID, 1),
          T(190, 238, "o produto, repartido", 14.5, S.INK2, anchor="middle")]
    for i, x in enumerate(xs):
        c = S.DIF if i == 0 else S.INK2
        y = 286
        b += coin(x - 14, y + 10, 12, c) + coin(x + 14, y + 10, 12, c) + coin(x, y - 14, 12, c)
        b += coin(x + 50, y + 10, 8, S.INK2, True)
    b += [T(64, 334, "quota própria", 14.5, S.DIF, anchor="middle"), T(253, 334, "demais quotas", 14.5, S.INK2, anchor="middle"),
          T(372, 334, "despesas", 13.5, S.INK2, anchor="end")]
    return S.svg(380, 348, "A máquina indivisível permanece inteira e cada credor pode reclamá-la; o produto, se houver, reparte-se em quotas, com as despesas descontadas", b)


# ───────────────────────────── 02: cumulo and recurso ─────────────────────────────

def _verdict(x, y, mark=None, ghost=False):
    out = []
    for dx, nm in ((0, "acolhe"), (62, "rejeita")):
        out.append(S.rect(x + dx, y - 8, 15, 15, fill=S.PAPER, stroke=S.GRID if ghost else S.INK, stroke_width=1.3, **dash(ghost)))
        out.append(T(x + dx + 20, y + 4, nm, 12.5, S.MUTED if ghost else S.INK2))
    if mark == "ok":
        out.append(tick(x + 1, y + 1))
    elif mark == "no":
        out.append(cross(x + 62 + 7.5, y - .5, 5, S.CONC, 2))
    return out


def cumulo(p, st):
    lx, lw, rx, rw, top, bot = 12, 180, 286, 202, 34, 346
    r1, r2 = 130, 262
    xl, xr = lx + lw, rx
    b = [*sheet(lx, top, lw, bot - top), *sheet(rx, top, rw, bot - top),
         T(lx, 24, "Petição", 22), T(rx, 24, "Sentença", 22)]
    for y in (r1, r2):
        b += [dot(xl, y, False), dot(xr, y)]
    mid = (xl + xr) / 2
    if st == 1:
        b += machine(lx + 16, r1 - 30, 1.0) + receipt(lx + 38, r2 - 32, 1.1)
        b += [T(mid, r1 - 12, "entrega", 14.5, S.INK2, anchor="middle"), T(mid, r2 - 12, "reembolso", 14.5, S.INK2, anchor="middle")]
        b += machine(rx + 14, r1 - 22, .72, S.INK2) + receipt(rx + 28, r2 - 24, .85, S.INK2)
        b += [*_verdict(rx + 96, r1 - 12), *_verdict(rx + 96, r2 - 12)]
        b += [P(f"M{xl} {r1} H{xr}", S.DIF, 2.6), P(f"M{xl} {r2} H{xr}", S.DIF, 2.6),
              T(mid, (r1 + r2) / 2 - 6, "cada pedido,", 14, S.INK2, anchor="middle"), T(mid, (r1 + r2) / 2 + 12, "sua decisão", 14, S.INK2, anchor="middle")]
    elif st == 2:
        b += person(lx + 18, r1 - 28, S.INK, 1.2) + person(lx + 50, r1 - 12, S.INK, .85) + coin(lx + 42, r2, 20)
        b += [T(mid, r1 - 12, "filiação", 14.5, S.INK2, anchor="middle"), T(mid, r2 - 34, "alimentos", 14.5, S.INK2, anchor="middle")]
        b += person(rx + 14, r1 - 26, S.INK2, 1.0) + person(rx + 42, r1 - 12, S.INK2, .72) + coin(rx + 36, r2, 16, S.INK2)
        b += [*_verdict(rx + 96, r1 - 12, "ok"), *_verdict(rx + 96, r2 - 12)]
        b += [P(f"M{xl} {r1} H{xr}", S.DIF, 2.6), P(f"M{xl} {r2} H{mid - 22}", S.DIF, 2.6),
              P(f"M{mid - 22} {r2} L{mid + 22} {r2}", S.DIF, 1.8), dot(mid - 22, r2, True, S.DIF), dot(mid + 22, r2, True, S.DIF),
              P(f"M{mid + 27} {r2} H{xr}", S.DIF, 2.6), dot(mid, r1, False, S.DIF),
              P(f"M{mid} {r1 + 6} V{r2 - 6}", S.DIF, 1.4, stroke_dasharray="2 4"),
              T(mid, r2 + 36, "condiciona", 14, S.INK2, anchor="middle"),
              T(rx + 16, r2 + 46, "a examinar", 14, S.INK2)]
    else:
        b += machine(lx + 16, r1 - 30, 1.0) + coin(lx + 42, r2, 20, S.INK2, True)
        b += [T(mid, r1 - 12, "entrega", 14.5, S.INK2, anchor="middle"), T(mid, r2 - 34, "equivalente", 14.5, S.INK2, anchor="middle")]
        b += machine(rx + 14, r1 - 22, .72, S.INK2)
        b += _verdict(rx + 96, r1 - 12, "ok")
        fx, fy, fw, fh = rx + 12, r2 - 34, rw - 24, 68
        b += [S.rect(fx, fy, fw, fh, fill=S.PAPER, stroke=S.INK2, stroke_width=1.3), *S.hatch(fx, fy, fw, fh, 9, stroke=S.GRID, stroke_width=1.2),
              S.rect(fx + 38, fy + 22, 100, 24, fill=S.PAPER, stroke="none"), T(fx + 88, fy + 39, "sem julgamento", 13.5, S.INK2, anchor="middle")]
        b += [P(f"M{xl} {r1} H{xr}", S.DIF, 2.6), P(f"M{xl} {r2} H{mid - 22}", S.INK2, 1.6, stroke_dasharray="5 5"),
              P(f"M{mid - 22} {r2} L{mid + 14} {r2 - 21}", S.INK2, 1.8), dot(mid - 22, r2, True, S.INK2), dot(mid + 22, r2, True, S.INK2),
              P(f"M{mid + 27} {r2} H{xr}", S.INK2, 1.6, stroke_dasharray="5 5"),
              dot(mid, r1, False, S.INK2), P(f"M{mid} {r1 + 6} V{r2 - 26}", S.INK2, 1.2, stroke_dasharray="2 4"),
              T(mid, r2 + 36, "só se a entrega", 13.5, S.INK2, anchor="middle"), T(mid, r2 + 52, "for rejeitada", 13.5, S.INK2, anchor="middle")]
    return S.svg(500, 372, "Pedidos da petição e seus campos na sentença: dois independentes, um que condiciona o seguinte, um que só aparece se o principal for rejeitado", b)


def recurso(p, st):
    b = [*sheet(16, 36, 300, 290), T(16, 26, "Sentença", 22)]
    r1, r2 = 130, 252
    b += machine(36, r1 - 24, .85, S.INK2) + coin(70, r2, 17, S.INK2 if st != 2 else S.GRID, st == 2) + [P(f"M34 {r1 + 62} H298", S.GRID, 1)]
    b += [T(106, r1 - 2, "principal", 14, S.INK2), T(106, r1 + 16, "rejeitado", 14, S.INK2)]
    b += [T(106, r2 - 2, "equivalente", 14, S.INK2), T(106, r2 + 16, "acolhido" if st != 2 else "prejudicado", 14, S.INK2)]
    b += [cross(270, r2 - 6, 7, S.INK2, 1.8)] if st == 2 else [tick(258, r2 - 2)]
    if st == 1:
        b += [cross(270, r1 - 4)]
    else:
        ox, oy = 232, 76
        b += [*sheet(ox, oy, 252, 130, S.DIF), T(ox, oy - 10, "Recurso do autor", 19, S.INK)]
        if st == 2:
            b += machine(ox + 30, oy + 36, 1.0) + [tick(ox + 160, oy + 62), T(ox + 30, oy + 154, "provido", 14.5, S.DIF)]
        else:
            b += machine(ox + 30, oy + 36, 1.0, S.INK2) + [cross(ox + 170, oy + 62), T(ox + 30, oy + 154, "desprovido", 14.5, S.INK2)]
    return S.svg(500, 344, "A sentença concedeu o equivalente e rejeitou a máquina; o recurso do autor cobre só o capítulo da máquina: se provido, a máquina substitui o equivalente; se desprovido, a sentença permanece", b)


# ───────────────────────────── 03: leitura ─────────────────────────────

def leitura(p):
    b = [T(16, 30, "desistência", 22), P("M16 176 H364", S.GRID, 1)]
    # the autos are lifted off; the machine stays whole beneath
    b += [S.rect(24, 56, 108, 90, fill="none", stroke=S.GRID, stroke_width=1.2, stroke_dasharray="4 4")]
    b += machine(40, 76, 1.15)
    b += [P("M140 100 H214", S.INK2, 1.8), P("M204 92 l10 8 l-10 8", S.INK2, 1.8)]
    b += sheet(236, 60, 100, 84) + [P("M248 82 H324", S.GRID, 1.2), P("M248 96 H324", S.GRID, 1.2), P("M248 110 H300", S.GRID, 1.2)]
    b += [T(286, 170, "do processo", 14.5, S.INK2, anchor="middle")]
    b += [T(16, 214, "renúncia", 22)]
    b += machine(40, 240, 1.15, S.CONC, True) + [P("M34 232 L130 310", S.CONC, 3), T(80, 332, "do direito", 14.5, S.CONC, anchor="middle")]
    b += [T(210, 272, "pede vontade", 14.5, S.INK2), T(210, 290, "investigada", 14.5, S.INK2)]
    return S.svg(380, 358, "Desistir do processo retira as folhas e a máquina permanece inteira; renunciar ao direito risca a própria máquina", b)


# ───────────────────────────── 04: dispositivo and tutela ─────────────────────────────

def _case(x, y, kind, c=S.INK):
    out = [S.rect(x, y, 44, 64, fill=S.PAPER, stroke=c, stroke_width=1.6)]
    if kind == "a":
        out += [P(f"M{x + 12} {y} V{y + 64} M{x + 32} {y} V{y + 64}", c, 1.1), P(f"M{x} {y + 14} H{x + 44} M{x} {y + 50} H{x + 44}", c, 1.1)]
    else:
        out += S.hatch(x, y, 44, 64, 8, stroke=c, stroke_width=1.1)
    return out


def dispositivo(p, st):
    b = [T(20, 32, "O pedido", 21), P("M16 116 H470", S.GRID, 2)]
    for i in range(3):
        b += _case(40 + i * 62, 44, "a")
    b += [T(40, 138, "Calamandrei", 15, S.INK2), *coin(424, 80, 17), T(424, 118, "indenização", 14, S.INK2, anchor="middle")]
    b += [T(20, 196, "A decisão", 21), P("M16 282 H470", S.GRID, 2)]
    n = 5 if st == 1 else 3
    for i in range(n):
        extra = st == 1 and i >= 3
        b += _case(40 + i * 62, 210, "b" if st == 2 else "a", S.CONC if (extra or st == 2) else S.INK)
    if st == 1:
        b += [P("M164 202 V196 H292 V202", S.CONC, 1.6)]
    b += [T(40, 304, "Chiovenda" if st == 2 else "Calamandrei", 15, S.CONC if st == 2 else S.INK2)]
    if st == 3:
        b += [*coin(424, 246, 17, S.CONC, True), T(424, 284, "sem exame", 14, S.CONC, anchor="middle")]
    else:
        b += [*coin(424, 246, 17), T(424, 284, "indenização", 14, S.INK2, anchor="middle")]
    tag = {1: "ultra petita · duas a mais", 2: "extra petita · outro objeto", 3: "infra petita · pedido sem resposta"}[st]
    b += [P("M16 322 H470", S.GRID, 1), T(20, 350, "quantidade", 15, S.CONC if st == 1 else S.INK2), T(176, 350, "objeto", 15, S.CONC if st == 2 else S.INK2),
          T(300, 350, "resposta", 15, S.CONC if st == 3 else S.INK2), L(20, 376, tag, 14, S.CONC)]
    return S.svg(500, 392, "Três coleções e uma indenização pedidas, comparadas com o que a decisão entrega: coleções a mais, coleções de outra obra, ou a indenização sem resposta", b)


def tutela(p):
    W, H = 1084, 334
    L1, L2, L3 = 78, 130, 252
    X0, MX = 210, 900
    b = [T(16, L1 + 6, "multa", 20), T(16, L2 + 6, "busca e apreensão", 20), T(16, L3 + 6, "perdas e danos", 20, S.INK2)]
    b += [P(f"M{X0} {L1} H{MX - 8}", S.DIF, 2.6), P(f"M{X0} {L2} H{MX - 8}", S.DIF, 2.6), dot(X0, L1, False), dot(X0, L2, False),
          dot(MX - 8, L1, True, S.DIF), dot(MX - 8, L2, True, S.DIF)]
    for i in range(4):
        b.append(P(f"M{330 + i * 16} {L1 - 9} l9 9 l-9 9", S.DIF, 2.2))
    b += [S.rect(350, L2 - 9, 18, 18, fill=S.PAPER, stroke=S.DIF, stroke_width=1.8)]
    b += machine(MX, 62, 1.5)
    b += [T(560, 38, "a técnica se ajusta; o objeto continua sendo a máquina", 15, S.INK2, anchor="middle")]
    b += [P("M16 192 H1068", S.GRID, 1)]
    gx = 560
    b += [P(f"M{X0} {L3} H{gx - 40}", S.INK2, 1.8), dot(X0, L3, False, S.INK2), dot(gx - 40, L3, True, S.INK2), P(f"M{gx - 40} {L3} L{gx} {L3 - 22}", S.INK2, 1.8),
          dot(gx + 8, L3, True, S.INK2), P(f"M{gx + 14} {L3} H{MX - 6}", S.INK2, 1.8, stroke_dasharray="6 5"), *coin(MX + 52, L3, 28)]
    b += [T(gx - 20, L3 + 40, "a pedido do autor ou se impossíveis a tutela específica", 14, S.INK2, anchor="middle"),
          T(gx - 20, L3 + 58, "e o resultado prático equivalente (art. 499)", 14, S.INK2, anchor="middle")]
    b += [P(f"M{gx - 80} {L3 - 8} C{gx - 80} 200 {gx - 130} 190 {gx - 130} {L2 + 12}", S.CONC, 1.8, stroke_dasharray="5 4"),
          P(f"M{gx - 137} {L2 + 22} l7 -10 l7 10", S.CONC, 1.8),
          T(gx + 40, 208, "nas hipóteses de 2024, antes da conversão:", 14, S.CONC), T(gx + 40, 226, "a faculdade de cumprir a tutela específica", 14, S.CONC)]
    return S.svg(W, H, "A multa e a busca e apreensão levam à mesma máquina; só a conversão em perdas e danos a troca por dinheiro, e nas hipóteses de 2024 a faculdade de cumprir a tutela específica vem antes", b)


# ───────────────────────────── 05: controle ─────────────────────────────

def _inicial(rows, defect=True):
    b = [*sheet(20, 18, 232, 232), T(40, 52, "Inicial", 22), P("M38 66 H234", S.GRID, 1)]
    for name, y in rows:
        b += [T(40, y, name, 17.5), P(f"M38 {y + 12} H234", S.GRID, 1)]
    return b


def controle(p, st):
    rows = [("partes", 96), ("causa de pedir", 130), ("pedido", 164), ("valor da causa", 198)]
    if st == 3:
        rows = [("partes", 96), ("causa de pedir", 130), ("pedido apto", 164), ("pedido viciado", 198)]
    b = _inicial(rows)
    if st == 3:
        b += [tick(222, 156, S.DIF), P("M236 184 V214", S.CONC, 3)]
    else:
        b += [P("M138 200 H232", S.INK2, 1.2, stroke_dasharray="2 4"), P("M236 184 V214", S.CONC, 3)]
    if st == 1:
        # the vague order sweeps the whole sheet; the precise one lands on a single line
        b += [P("M262 30 V240 M262 30 h-8 M262 240 h-8", S.INK2, 1.4, stroke_dasharray="5 4"),
              S.rect(282, 44, 190, 52, fill=S.PAPER, stroke=S.INK2, stroke_width=1.2), T(296, 76, "Regularize a inicial", 17, S.INK2),
              P("M292 70 H462", S.CONC, 2.4), P("M262 70 H282", S.INK2, 1.2),
              P("M262 186 V212 M262 186 h-8 M262 212 h-8", S.DIF, 2.2),
              S.rect(282, 134, 190, 92, fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
              T(296, 162, "Indique o valor", 17.5), T(296, 184, "da causa (art. 292)", 17.5), T(296, 210, "e complete a inicial", 17.5),
              P("M262 199 H282", S.DIF, 2)]
    elif st == 2:
        b += [S.rect(282, 134, 190, 92, fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
              T(296, 162, "Indique o valor", 17.5), T(296, 184, "da causa (art. 292)", 17.5), T(296, 210, "e complete a inicial", 17.5),
              P("M262 186 V212 M262 186 h-8 M262 212 h-8", S.DIF, 2.2), P("M262 199 H282", S.DIF, 2)]
        for r in range(3):
            for c in range(7):
                x, y = 28 + c * 34, 282 + r * 34
                if c < 5:
                    b.append(S.rect(x, y, 29, 29, fill=S.PAPER, stroke=S.INK, stroke_width=1.4))
                else:
                    b.append(S.rect(x, y, 29, 29, fill="none", stroke=S.GRID, stroke_width=1))
                    b += S.hatch(x, y, 29, 29, 7, stroke=S.GRID, stroke_width=.9)
        b += [P("M30 261 V273 M30 261 H264 M264 261 V273", S.INK2, 1.2), T(150, 252, "15 dias úteis", 18, S.INK, anchor="middle"),
              P("M274 314 H322", S.INK2, 1.6, stroke_dasharray="5 5"), P("M314 308 l8 6 l-8 6", S.INK2, 1.6),
              T(332, 312, "prorrogável", 15, S.INK2), T(332, 330, "antes do fim", 15, S.INK2)]
    else:
        b += [P("M252 164 H300", S.DIF, 2.6), dot(300, 164, True, S.DIF), T(312, 160, "a parte apta", 17, S.DIF), T(312, 180, "prossegue", 17, S.DIF),
              S.rect(268, 190, 188, 28, fill="none", stroke=S.CONC, stroke_width=1.6, stroke_dasharray="5 4"), T(280, 210, "a parte viciada fica de fora", 14.5, S.CONC),
              T(272, 44, "indeferimento parcial:", 17), T(272, 66, "agravo de instrumento", 17)]
        b += [P("M20 292 H470", S.GRID, 1), *sheet(40, 308, 76, 64, S.INK2), P("M40 308 L116 372 M116 308 L40 372", S.CONC, 2.4),
              T(138, 334, "indeferimento total:", 17, S.INK2), T(138, 358, "sentença e apelação", 17, S.INK2)]
    return S.svg(500, 392, "A inicial recebe uma ordem precisa, prazo para corrigir e, se um pedido persistir viciado, só essa parte fica de fora", b)


# ───────────────────────────── 06: estabilidade and discovery ─────────────────────────────

def _strip(x, y, w, c=S.INK, sw=1.5, ghost=False):
    out = [S.rect(x, y, w, 38, fill=S.PAPER, stroke=c, stroke_width=sw, **dash(ghost))]
    if not ghost:
        out += [P(f"M{x + 10} {y + 13} H{x + w - 10}", c, 1), P(f"M{x + 10} {y + 26} H{x + w - 26}", c, 1)]
    return out


def estabilidade(p, st):
    LX, RX, SW = 16, 264, 220
    ys = (64, 114, 164)
    b = [*sheet(LX, 40, SW, 270), *sheet(RX, 40, SW, 270), T(LX, 28, "Inicial", 22), T(RX, 28, "Defesa", 22)]
    for y in ys:
        b += _strip(LX + 14, y, SW - 28) + _strip(RX + 14, y, SW - 28)
        b += [P(f"M{LX + SW} {y + 19} H{RX}", S.DIF, 1.8), dot(LX + SW, y + 19, False, S.DIF, 3.5), dot(RX, y + 19, False, S.DIF, 3.5)]
    y4 = 224
    if st == 1:
        b += [T(250, 338, "a defesa responde ao que foi demandado", 15, S.INK2, anchor="middle")]
    elif st == 2:
        b += _strip(LX + 14, y4, SW - 28, S.CONC, 2) + _strip(RX + 14, y4, SW - 28, S.GRID, 1.4, True)
        b += [P(f"M{LX + SW} {y4 + 19} H{LX + SW + 14}", S.CONC, 1.8, stroke_dasharray="3 4"), dot(LX + SW, y4 + 19, False, S.CONC, 3.5),
              T(LX, 338, "parcela acrescida", 15, S.CONC), T(RX, 338, "sem resposta", 15, S.INK2)]
    else:
        b += _strip(LX + 14, y4, SW - 28) + _strip(RX + 14, y4, SW - 28, S.DIF, 2)
        b += [P(f"M{LX + SW} {y4 + 19} H{RX}", S.DIF, 2.2), dot(250, y4 + 19, True, S.DIF, 8), tick(244, y4 + 20, S.DIF, 2),
              T(LX, 338, "alteração", 15, S.INK2), T(RX, 338, "defesa ampliada", 15, S.DIF),
              P(f"M250 {y4 + 28} V322", S.INK2, 1.2, stroke_dasharray="2 4"), T(250, 358, "com o réu", 14.5, S.INK2, anchor="middle")]
    return S.svg(500, 368, "As faixas da inicial correspondem às da defesa; a parcela acrescida fica sem resposta até que o réu consinta e a defesa se amplie", b)


def discovery(p, st):
    cols, rows, x0, y0, px, py = 6, 5, 188, 84, 52, 56
    core = {(2, 2), (3, 2), (2, 3), (3, 3), (3, 1)}
    mid = {(c, r) for c in range(1, 5) for r in range(1, 4)}
    b = []
    cy = y0 + (rows * py) / 2 - 8
    # the opening sheet: a few lines in 1957, a worked narrative afterwards
    n = 1 if st == 1 else 5
    b += sheet(18, cy - 56, 78, 112)
    for k in range(n):
        b.append(P(f"M28 {cy - 36 + k * 18} H{86 - (k % 2) * 14}", S.INK, 1.6))
    if st == 2:
        b += [S.rect(10, cy - 66, 96, 132, fill="none", stroke=S.DIF, stroke_width=1.4, stroke_dasharray="4 4")]
    for c in range(cols):
        for r in range(rows):
            x, y = x0 + c * px, y0 + r * py
            if st == 1:
                col, w = S.INK2, 1.5
            elif (c, r) in core or (st == 3 and (c, r) in mid):
                col, w = (S.DIF if (c, r) in core else S.INK2), 1.8
            else:
                col, w = S.GRID, 1.2
            b += [S.rect(x, y, 30, 40, fill=S.PAPER, stroke=col, stroke_width=w), P(f"M{x + 6} {y + 12} H{x + 24} M{x + 6} {y + 22} H{x + 24}", col, 1)]
    if st == 1:
        b += [P(f"M98 {cy - 8} L{x0 + cols * px - 24} {y0 - 14} M98 {cy + 8} L{x0 + cols * px - 24} {y0 + rows * py + 4}", S.INK2, 1.4, stroke_dasharray="5 5")]
        tag = ["1957 · alegação curta e simples:", "a investigação alcança tudo"]
    elif st == 2:
        bx0, by0 = x0 + 2 * px - 6, y0 + 1 * py - 6
        b += [P(f"M98 {cy - 8} L{bx0} {by0} M98 {cy + 8} L{bx0} {y0 + 3 * py + 46}", S.DIF, 1.8)]
        tag = ["2007 e 2009 · fato específico e plausibilidade:", "só o que liga ao caso"]
    else:
        tag = None
        fr = lambda cs, rs, pad: (x0 + min(cs) * px - pad, y0 + min(rs) * py - pad, (max(cs) - min(cs)) * px + 30 + 2 * pad, (max(rs) - min(rs)) * py + 40 + 2 * pad)
        o = fr(range(cols), range(rows), 20)
        m = fr(range(1, 5), range(1, 4), 13)
        i = fr((2, 3), (1, 2, 3), 7)
        b += [S.rect(*o, fill="none", stroke=S.CONC, stroke_width=1.8, stroke_dasharray="7 5"),
              S.rect(*m, fill="none", stroke=S.INK2, stroke_width=1.8, stroke_dasharray="3 4"),
              S.rect(*i, fill="none", stroke=S.DIF, stroke_width=2.2)]
        for k, (c, t) in enumerate(((S.CONC, "1976 · sanções por abuso"), (S.INK2, "2000 · pertinência: da ação à pretensão ou defesa"),
                                    (S.DIF, "2015 · proporcionalidade ao resultado esperado"))):
            yy = 392 + k * 20
            b += [P(f"M20 {yy - 4} H48", c, 2.2, **({"stroke_dasharray": ["7 5", "3 4", ""][k]} if k < 2 else {})), T(58, yy, t, 14, S.INK)]
    if tag:
        b += [L(20, 396, tag[0], 12.5, S.INK2), L(20, 414, tag[1], 12.5, S.INK2)]
    return S.svg(500, 452, "Da alegação aberta, que abre a investigação a todos os documentos, à alegação específica, que seleciona só os ligados ao caso, e aos limites sucessivos da busca", b)



# ───────────────────────────── 02b: apelacao, especies · 06b: tempo ─────────────────────────────

def apelacao(p):
    """The reserve request across two dispositivos: first-degree sentence (principal granted, reserve unjudged) and the
    appellate judgment (principal rejected, reserve still waiting; Cruz e Tucci's wall, Didier's way round it)."""
    W, H = 1084, 336
    SW = 370
    X1, X2 = 16, W - 16 - SW
    top, bot, r1, r2 = 44, 306, 124, 238
    b = [T(X1, 28, "Sentença", 22), T(X2, 28, "Acórdão", 22), *sheet(X1, top, SW, bot - top), *sheet(X2, top, SW, bot - top)]
    for X, st in ((X1, 1), (X2, 2)):
        b += machine(X + 18, r1 - 24, .85, S.INK2 if st == 2 else S.INK)
        b += [T(X + 96, r1 + 5, "principal", 15, S.INK2), *_verdict(X + 176, r1 - 12, "ok" if st == 1 else "no")]
        if st == 2:
            b += [cross(X + 48, r1 - 2, 15, S.CONC, 2.8)]
        b += coin(X + 48, r2, 17, S.INK2, True) + [T(X + 96, r2 + 5, "reserva", 15, S.INK2)]
        if st == 1:
            fx, fy, fw, fh = X + 176, r2 - 24, 160, 48
            b += [S.rect(fx, fy, fw, fh, fill=S.PAPER, stroke=S.INK2, stroke_width=1.3), *S.hatch(fx, fy, fw, fh, 9, stroke=S.GRID, stroke_width=1.2),
                  S.rect(fx + 24, fy + 12, 112, 24, fill=S.PAPER, stroke="none"), T(fx + 80, fy + 29, "sem julgamento", 13.5, S.INK2, anchor="middle")]
        else:
            b += [*_verdict(X + 176, r2 - 12), T(X + 176, r2 + 28, "a examinar", 13.5, S.INK2)]
    xl, xr = X1 + SW, X2
    mid = (xl + xr) / 2
    b += [P(f"M{xl} {r1} H{xr}", S.DIF, 2.6), dot(xl, r1, False), dot(xr, r1),
          T(mid, r1 - 40, "apelação da oficina", 15, S.INK, anchor="middle"), T(mid, r1 - 20, "devolve o capítulo do principal", 13.5, S.INK2, anchor="middle")]
    wx = mid
    b += [P(f"M{xl} {r2} H{wx}", S.INK2, 1.6, stroke_dasharray="5 5"), P(f"M{wx} {r2} H{xr}", S.MUTED, 1.6, stroke_dasharray="5 5"),
          dot(xl, r2, False, S.INK2), dot(xr, r2, True, S.INK2),
          P(f"M{wx} {r2 - 22} V{r2 + 22}", S.CONC, 4.5),
          T(wx, r2 + 42, "Cruz e Tucci: só o", 14, S.CONC, anchor="middle"), T(wx, r2 + 60, "capítulo do principal", 14, S.CONC, anchor="middle")]
    b += [P(f"M{wx - 38} {r2 - 8} C{wx - 38} {r2 - 54} {wx + 38} {r2 - 54} {wx + 38} {r2 - 14}", S.INK2, 1.8, stroke_dasharray="5 4"),
          dot(wx - 38, r2 - 8, True, S.INK2, 4), P(f"M{wx + 32} {r2 - 24} l6 11 l6 -11", S.INK2, 1.8),
          T(wx, r2 - 78, "Didier: art. 1.013, § 3º, III,", 14, S.INK, anchor="middle"), T(wx, r2 - 60, "pedido omitido, causa pronta", 14, S.INK2, anchor="middle")]
    return S.svg(W, H, "Na sentença o principal foi acolhido e a reserva ficou sem julgamento; no acórdão o principal é rejeitado e a reserva espera: para Cruz e Tucci o tribunal só recebe o capítulo do principal, para Didier o art. 1.013, § 3º, III, pode levá-la a julgamento imediato", b)


def especies(p):
    """Próprias (all requests wanted: lines side by side reach the sentence) and impróprias (at most one: lines merge)."""
    W, H = 1084, 396
    rows = [78, 158, 274, 354]
    x0, xe, mx = 290, 770, 640
    names = [("simples", "entrega e reembolso"), ("sucessiva", "filiação e alimentos"),
             ("subsidiária", "entrega e equivalente"), ("alternativa", "devolver ou entregar outra")]
    b = []
    for i, (y, (nm, sub)) in enumerate(zip(rows, names)):
        y1, y2 = y - 17, y + 17
        b += [T(16, y - 2, nm, 20), T(16, y + 19, sub, 13.5, S.INK2)]
        if i == 0:
            b += machine(228, y1 - 14, .55) + receipt(238, y2 - 14, .5)
        elif i == 1:
            b += person(238, y1 - 11, S.INK, .8) + coin(247, y2, 11)
        elif i == 2:
            b += machine(228, y1 - 14, .55) + coin(247, y2, 11, S.INK2, True)
        else:
            b += machine(228, y1 - 14, .55) + machine(228, y2 - 14, .55)
        b += [dot(x0, y1, False), dot(x0, y2, False)]
        if i < 2:
            b += [P(f"M{x0} {y1} H{xe}", S.DIF, 2.6), P(f"M{x0} {y2} H{xe}", S.DIF, 2.6), dot(xe, y1), dot(xe, y2),
                  tick(xe + 14, y1 + 2), tick(xe + 14, y2 + 2)]
            if i == 1:
                b += [P(f"M{x0} {y2} H{500}", S.DIF, 2.6), dot(560, y1, True, S.DIF), dot(560, y2, True, S.DIF),
                      P(f"M560 {y1 + 6} V{y2 - 6}", S.DIF, 1.4, stroke_dasharray="2 4"), T(574, y + 4, "condiciona", 13.5, S.INK2)]
        else:
            m = y
            c1, c2 = (S.DIF, S.INK2) if i == 2 else (S.INK2, S.INK2)
            b += [P(f"M{x0} {y1} H560 C620 {y1} 620 {m} 680 {m} H{xe}", c1, 2.6)]
            if i == 2:
                b += [P(f"M{x0} {y2} H400", S.INK2, 1.6, stroke_dasharray="5 5"), P(f"M400 {y2} L440 {y2 - 20}", S.INK2, 1.8),
                      dot(400, y2, True, S.INK2), dot(448, y2, True, S.INK2),
                      P(f"M456 {y2} H560 C620 {y2} 620 {m} 680 {m}", S.INK2, 1.6, stroke_dasharray="5 5")]
            else:
                b += [P(f"M{x0} {y2} H560 C620 {y2} 620 {m} 680 {m}", S.INK2, 2.6)]
            b += [dot(xe, m), tick(xe + 14, m + 2)]
    b += [P("M16 118 H850", S.GRID, 1), P("M16 216 H1068", S.GRID, 2), P("M16 314 H850", S.GRID, 1)]
    for y0, y1_, nm, sub in ((46, 190, "próprias", "querem-se todos"), (242, 386, "impróprias", "no máximo um")):
        m = (y0 + y1_) / 2
        b += [P(f"M872 {y0} Q884 {y0} 884 {y0 + 14} V{m - 14} Q884 {m} 896 {m} Q884 {m} 884 {m + 14} V{y1_ - 14} Q884 {y1_} 872 {y1_}", S.INK2, 1.6),
              T(914, m - 2, nm, 21), T(914, m + 20, sub, 13.5, S.INK2)]
    return S.svg(W, H, "Simples e sucessiva levam os dois pedidos à sentença; subsidiária e alternativa juntam os dois caminhos em uma só saída", b)


def _mstrip(x, y, w, c=S.INK, sw=1.5, ghost=False):
    out = [S.rect(x, y, w, 30, fill=S.PAPER, stroke=c, stroke_width=sw, **dash(ghost))]
    if not ghost:
        out += [P(f"M{x + 10} {y + 11} H{x + w - 10}", c, 1), P(f"M{x + 10} {y + 21} H{x + w - 28}", c, 1)]
    return out


def tempo(p):
    """The case in time: before citação a change is free; after it, only with the defendant; after saneamento, only by
    the parties' agreement (art. 190). Each stretch shows the inicial and defesa lanes and the one new strip."""
    W, H = 1084, 322
    LM, cx, sx, end = 96, 404, 744, 1068
    ay, ry = 164, 254
    b = [dot(LM, 50, False), P(f"M{LM} 50 H{cx}", S.DIF, 4), P(f"M{cx} 50 H{sx}", S.INK2, 4), P(f"M{sx} 50 H{end}", S.CONC, 4),
         P(f"M{cx} 38 V62", S.INK, 1.6), P(f"M{sx} 38 V62", S.INK, 1.6),
         T(cx, 28, "citação", 14.5, S.INK, anchor="middle"), T(sx, 28, "saneamento", 14.5, S.INK, anchor="middle"),
         T(16, ay + 21, "Inicial", 15, S.INK2), T(16, ry + 21, "Defesa", 15, S.INK2)]
    heads = [(LM + 8, "livre", S.DIF, "modificar sem consentimento"), (cx + 12, "com o réu", S.INK, "consentimento, mesmo do revel"),
             (sx + 12, "por convenção", S.CONC, "art. 190: reabre debate e prova")]
    for x, h, c, sub in heads:
        b += [T(x, 100, h, 22, c), T(x, 122, sub, 13.5, S.INK2)]
    cols = [(LM + 8, 88, 16), (cx + 8, 92, 22), (sx + 8, 90, 22)]
    for ci, (a, w, gap) in enumerate(cols):
        for k in range(3):
            x = a + k * (w + gap)
            new = k == 2
            c = S.DIF if new and ci < 2 else (S.CONC if new else S.INK)
            b += _mstrip(x, ay, w, c if new else S.INK, 2.2 if new else 1.5, ghost=(ci == 2 and new))
            if ci == 0:
                b += _mstrip(x, ry, w, S.GRID, 1.3, ghost=True)
            else:
                ghost_r = ci == 2 and new
                b += _mstrip(x, ry, w, S.DIF if (new and ci == 1) else (S.GRID if ghost_r else S.INK), 2.2 if new and ci == 1 else (1.4 if ghost_r else 1.5), ghost=ghost_r)
                xc = x + w / 2
                if not new:
                    b += [P(f"M{xc} {ay + 30} V{ry}", S.DIF, 1.6), dot(xc, ay + 30, False, S.DIF, 3.5), dot(xc, ry, False, S.DIF, 3.5)]
                elif ci == 1:
                    b += [P(f"M{xc} {ay + 30} V{ry}", S.DIF, 2.4), dot(xc, (ay + 30 + ry) / 2, True, S.DIF, 11), P(f"M{xc - 5} {(ay + 30 + ry) / 2 + 1} l4 5 l7 -10", S.DIF, 2.4)]
                else:
                    ym = (ay + 30 + ry) / 2
                    b += [P(f"M{xc} {ay + 30} V{ry}", S.INK2, 1.6, stroke_dasharray="4 4"), dot(xc, ym, True, S.DIF, 5)]
                    b += person(xc - 46, ym - 16, S.DIF, 1.0) + person(xc + 26, ym - 16, S.DIF, 1.0)
            if new and ci == 0:
                b += [P(f"M{x + w / 2} 138 V{ay - 8}", S.DIF, 2), P(f"M{x + w / 2 - 6} {ay - 14} l6 7 l6 -7", S.DIF, 2)]
            if new and ci == 1:
                b += [P(f"M{x + w / 2} 138 V{ay - 8}", S.INK2, 2), P(f"M{x + w / 2 - 6} {ay - 14} l6 7 l6 -7", S.INK2, 2)]
    b += [P(f"M{sx} 134 V{H - 28}", S.CONC, 4.5)]
    return S.svg(W, H, "Antes da citação a inicial se modifica livremente; depois, só com o consentimento do réu, que amplia a defesa; após o saneamento, só pela convenção das partes", b)



def revisional(p):
    """Three instalment slips of the contract under revision, each cut along the dispute: the undisputed part is stamped
    paid on its due date (art. 330, § 3º); the disputed part, set apart, is in mora when unpaid (Didier) unless a
    provisional decision covers it."""
    W, H = 1084, 270
    sw, sh, cw, gap = 214, 96, 98, 12
    ay = 232
    b = [P(f"M16 {ay} H1060", S.INK2, 1.8), P(f"M1052 {ay - 7} l9 7 l-9 7", S.INK2, 1.8)]
    for i, x in enumerate((24, 388, 752)):
        y = 70
        xc = x + sw / 2
        slip = S.path(f"M{x} {y} H{x + sw} V{y + sh} L{x + sw - 8} {y + sh + 5} L{x + sw - 16} {y + sh} L{x + sw - 24} {y + sh + 5} L{x + sw - 32} {y + sh} H{x} Z",
                      fill=S.PAPER, stroke=S.INK, stroke_width=1.6, stroke_linejoin="round")
        b += [slip, P(f"M{x + 16} {y + 18} H{x + sw - 18}", S.GRID, 1), P(f"M{x + 16} {y + 30} H{x + sw - 60}", S.GRID, 1)]
        b += [S.circle(xc, y + sh - 28, 17, fill=S.PAPER, stroke=S.DIF, stroke_width=2),
              P(f"M{xc - 7} {y + sh - 27} l5 6 l10 -13", S.DIF, 2.4)]
        cx, cy = x + sw + gap, y + 14
        b += [S.rect(cx, cy, cw, sh, fill=S.PAPER, stroke=S.CONC if i < 2 else S.INK2, stroke_width=1.6, stroke_dasharray="6 4"),
              *S.hatch(cx, cy, cw, sh, 9, stroke=S.GRID, stroke_width=1.2)]
        if i < 2:
            mx, my = cx + cw / 2, cy + sh / 2
            b += [S.circle(mx, my, 15, fill=S.PAPER, stroke=S.CONC, stroke_width=2), P(f"M{mx - 8} {my} H{mx + 8}", S.CONC, 2.2)]
        else:
            b += sheet(cx + 12, cy + 14, cw - 24, sh - 28, S.DIF) + [P(f"M{cx + 24} {cy + 34} H{cx + cw - 24}", S.DIF, 1.2), P(f"M{cx + 24} {cy + 46} H{cx + cw - 36}", S.DIF, 1.2),
                  tick(cx + cw / 2 - 8, cy + sh - 26, S.DIF, 2.2)]
        b += [dot(xc, ay, False, S.INK, 4.5), P(f"M{xc} {y + sh + 8} V{ay - 8}", S.GRID, 1, stroke_dasharray="2 4")]
    b += [T(24, 44, "incontroverso", 19), T(24 + sw + gap, 44 + 14 + 0, "", 1) if False else T(24 + sw + gap, 44, "controvertido", 19, S.CONC)]
    b += [T(24, 258, "pago no tempo e modo contratados (art. 330, § 3º)", 14, S.INK2),
          T(752 + sw + gap + cw / 2, 258, "decisão provisória", 14, S.INK2, anchor="end")]
    return S.svg(W, H, "Três parcelas do contrato cortadas ao longo da disputa: a parte incontroversa segue paga a cada vencimento; a controvertida, posta à parte, está em mora se não paga, salvo quando uma decisão provisória a cobre", b)


MODES: dict = {}


def build(p: dict):
    mode = p.get("mode")
    if mode not in MODES:
        raise ValueError("pedidos_folhas mode must be one of " + ", ".join(sorted(MODES)))
    fn, n = MODES[mode]
    prefix = p.get("stepped")
    if not n:
        return fn(p), []
    if p.get("stage"):
        return fn(p, int(p["stage"])), []
    if not prefix:
        return fn(p, n), []
    return "".join(f'<div class="panel{" on" if s == 1 else ""}" id="{S.esc(prefix)}-{s}">{fn(p, s)}</div>' for s in range(1, n + 1)), []


MODES.update(hero=(hero, 0), vias=(vias, 0))

MODES.update(perecimento=(perecimento, 3), indivisivel=(indivisivel, 0), cumulo=(cumulo, 3), recurso=(recurso, 3), leitura=(leitura, 0),
             dispositivo=(dispositivo, 3), tutela=(tutela, 0), controle=(controle, 3), estabilidade=(estabilidade, 3), discovery=(discovery, 3))

MODES.update(apelacao=(apelacao, 0), especies=(especies, 0), tempo=(tempo, 0), revisional=(revisional, 0))
