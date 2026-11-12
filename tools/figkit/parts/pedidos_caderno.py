"""pedidos_caderno: the petition's pedidos as wires, for the Aula 01 companion.

Params:
  mode: hero | fecho | cumulo | dispositivo | controle | vias | perecimento | leitura | funil (required).
  vias and funil are 1084-wide plates; perecimento (stepped) and leitura are 380-wide margin glosses.
  stepped: optional panel-id prefix, for the three cumulative scroll states
    of cumulo, dispositivo and controle (one panel per state, each a whole
    drawing, so the static parts coincide and only the new layer fades in).

Drawn in the language of the course's planta: sheets with ruled rows, a wire
per pedido, hollow dots for terminals, a wavy wire where the demand can still
change and a straight one once the law fixes it, an orange bar where it locks.
The subsidiary pedido is a normally open switch: it conducts only when the
principal is not granted. No selectors, no folded corners.

hero / fecho are 1120 x 430 (fecho is the hero resolved: every gate passed);
the three stepped studies are 480 x 410 and read at about 1:1 beside the text.
Legal facts: Marinoni, Arenhart e Mitidiero v.2 pp.155-168; Didier v.1
pp.640-665; Mitidiero (2022) pp.173-174; CPC 321, 326, 327, 329, 331, 354,
492, 499.
"""
from __future__ import annotations

from . import svg as S


def T(x, y, s, size=16, fill=S.INK, family=S.SERIF, **kw):
    return S.text(x, y, s, size=size, family=family, fill=fill, **kw)


def L(x, y, s, size=12.5, fill=S.INK2, **kw):
    """A small mono label, the planta's bracket voice."""
    return S.text(x, y, s, size=size, family=S.MONO, fill=fill, letter_spacing=".05em", **kw)


def P(d, color=S.INK, width=1.5, **kw):
    return S.path(d, fill="none", stroke=color, stroke_width=width,
                  stroke_linecap="round", stroke_linejoin="round", **kw)


def dot(x, y, hollow=True, color=S.INK, r=5):
    return S.circle(x, y, r, fill=S.PAPER if hollow else color, stroke=color, stroke_width=1.6)


def tick(x, y, color=S.DIF, w=2):
    return P(f"M{x} {y} l4.5 5.5 l9.5 -12.5", color, w)


def wave(x0, x1, y, amp=3, period=30):
    d, x, up = f"M{x0} {y}", x0, True
    while x < x1:
        nx = min(x + period / 2, x1)
        d += f" Q{(x + nx) / 2:.1f} {y - amp if up else y + amp} {nx:.1f} {y}"
        x, up = nx, not up
    return d


def sheet(x, y, w, h, color=S.INK):
    return [S.rect(x + 5, y + 6, w, h, fill=S.PAPER, stroke=S.GRID, stroke_width=1),
            S.rect(x, y, w, h, fill=S.PAPER, stroke=color, stroke_width=1.5)]


def bracket(x0, x1, y, label, color=S.INK2, up=True):
    d = f"M{x0} {y + 8} V{y} H{x1} V{y + 8}"
    return [P(d, color, 1.2), L((x0 + x1) / 2, y - 8, label, fill=color, anchor="middle")]


def lever_switch(xa, xb, y, closed=False, color=S.INK2):
    """A knife switch between two hollow contacts; open by default."""
    lever = f"M{xa} {y} L{xb} {y}" if closed else f"M{xa} {y} L{xb - 8} {y - 21}"
    return [dot(xa, y, True, color), dot(xb, y, True, color), P(lever, color, 1.8)]


# ───────────────────────────── hero and closure ─────────────────────────────

def board(closed: bool):
    ent, eq, reem = 190, 250, 326
    LX, LW, RX, RW = 34, 266, 860, 226
    top, bottom = 92, 362
    b = [*sheet(LX, top, LW, bottom - top), *sheet(RX, top, RW, bottom - top)]
    # petition sheet
    b += [T(LX + 22, 126, "Petição de Cecília", 22),
          T(LX + 22, 148, "máquina retida · aluguel de outra", 14.5, S.INK2),
          P(f"M{LX + 22} 162 H{LX + LW - 20}", S.GRID, 1),
          T(LX + 22, ent + 7, "entrega da máquina", 20),
          P(f"M{LX + 22} 215 H{LX + LW - 20}", S.GRID, 1),
          T(LX + 22, eq + 3, "equivalente em dinheiro", 19),
          T(LX + 22, eq + 24, "se a entrega não puder ser acolhida", 13.5, S.INK2),
          P(f"M{LX + 22} 288 H{LX + LW - 20}", S.GRID, 1),
          T(LX + 22, reem + 7, "reembolso do aluguel", 20)]
    # dispositivo sheet
    b += [T(RX + 22, 126, "Dispositivo", 22),
          P(f"M{RX + 22} 162 H{RX + RW - 20}", S.GRID, 1),
          T(RX + 26, ent + 7, "entrega", 20, S.DIF),
          P(f"M{RX + 22} 215 H{RX + RW - 20}", S.GRID, 1),
          T(RX + 26, eq + 7, "sem julgamento" if closed else "ou equivalente", 18, S.INK2),
          P(f"M{RX + 22} 288 H{RX + RW - 20}", S.GRID, 1),
          T(RX + 26, reem + 7, "reembolso", 20, S.DIF),
          T(RX + RW, 388, "arts. 141, 492 e 499", 13.5, S.INK2, anchor="end")]
    # wires: wavy while the demand can still change, straight after the lock
    lock = 700
    for y in (ent, reem):
        b.append(P(f"M{LX + LW} {y} H{RX}" if closed else wave(LX + LW, lock, y) + f" H{RX}", S.DIF, 2.6))
    # the subsidiary: a normally open switch, held open by the principal
    xa, xb = 742, 800
    b += [P(f"M{LX + LW} {eq} H{xa - 5}", S.INK2, 1.6, stroke_dasharray="5 5"),
          *lever_switch(xa, xb, eq),
          P(f"M{xb + 5} {eq} H{RX}", S.GRID if closed else S.INK2, 1.6, stroke_dasharray="5 5"),
          dot(xb - 2, ent, False, S.INK2), P(f"M{xb - 2} {ent + 5} V{eq - 23}", S.INK2, 1.1, stroke_dasharray="2 4"),
          T((xa + xb) / 2, eq + 26, "só se a entrega", 13.5, S.INK2, anchor="middle"),
          T((xa + xb) / 2, eq + 43, "não for acolhida", 13.5, S.INK2, anchor="middle"),
          T(560, reem - 12, "julgamento próprio", 14, S.INK2, anchor="middle")]
    b += [dot(LX + LW, ent, False, S.INK), dot(LX + LW, eq, False, S.INK), dot(LX + LW, reem, False, S.INK),
          dot(RX, ent), dot(RX, eq), dot(RX, reem)]
    # the lock: after saneamento the object is fixed
    b += [P(f"M{lock} 168 V346", S.CONC, 4), T(lock, 362, "art. 329", 13.5, S.INK2, anchor="middle")]
    # brackets along the top
    gates = [(352, 530, "interpretar"), (530, 692, "corrigir")]
    for x0, x1, name in gates:
        b += bracket(x0, x1, 74, ("✓ " if closed else "") + name, S.DIF if closed else S.INK2)
    b += bracket(708, 790, 74, "estabilizar", S.CONC)
    b += bracket(800, 852, 74, "julgar", S.DIF if closed else S.INK2)
    if closed:
        b += [tick(RX + RW - 44, ent - 6), tick(RX + RW - 44, reem - 6)]
    return b


def planta(p):
    """The hero as a planta: three pedidos as rows, four stages of control as columns they cross."""
    W, H = 1120, 440
    PX, PW = 14, 212            # petition sheet
    CX0, CW = 236, 168          # first stage column, column width
    DX, DW = 916, 190           # dispositivo sheet
    top, bot = 14, 426
    ys = (252, 320, 388)        # entrega, equivalente, reembolso
    b = []
    # columns
    stages = [("interpretar", "art. 322, § 2º", ["Lê-se a petição inteira,", "segundo a boa-fé."]),
              ("corrigir", "arts. 321 e 330", ["Emenda em 15 dias úteis;", "sem ela, indeferimento."]),
              ("estabilizar", "art. 329", ["Livre até a citação;", "depois, só com o réu;", "após o saneamento,", "nunca."]),
              ("julgar", "arts. 141 e 492", ["Congruência: nada", "além, fora nem aquém", "do pedido."])]
    for i, (name, art, lines) in enumerate(stages):
        x = CX0 + i * CW
        b.append(S.rect(x, top, CW, bot - top, fill=S.PAPER2 if i % 2 == 0 else S.PAPER, stroke=S.GRID, stroke_width=1))
        b += [dot(x + 22, 40, True, S.INK, 9), T(x + 22, 45.5, str(i + 1), 13, S.INK, family=S.MONO, anchor="middle"),
              T(x + 40, 46, name, 20), T(x + 12, 70, art, 13.5, S.INK, family=S.MONO)]
        for k, ln in enumerate(lines):
            b.append(T(x + 12, 94 + k * 17, ln, 13.5, S.INK2))
        b.append(P(f"M{x + 12} 206 H{x + CW - 12}", S.GRID, 1))
    # estabilizar: the three zones of art. 329
    x3 = CX0 + 2 * CW
    t1, t2 = x3 + 52, x3 + 118
    b += [P(f"M{x3 + 12} 180 H{t1}", S.DIF, 3), P(f"M{t1} 180 H{t2}", S.INK2, 3), P(f"M{t2} 180 H{x3 + CW - 12}", S.CONC, 3),
          P(f"M{t1} 173 V187", S.INK, 1.4), P(f"M{t2} 173 V187", S.INK, 1.4),
          T(t1, 166, "citação", 13, S.INK, anchor="middle"), T(t2, 166, "saneamento", 13, S.INK, anchor="middle"),
          T((x3 + 12 + t1) / 2, 200, "livre", 13, S.INK2, anchor="middle"),
          T((t1 + t2) / 2, 200, "com o réu", 13, S.INK2, anchor="middle"),
          T((t2 + x3 + CW - 12) / 2, 200, "vedado", 13, S.INK2, anchor="middle")]
    # sheets
    b += [*sheet(PX, top, PW, bot - top), *sheet(DX, top, DW, bot - top)]
    b += [T(PX + 14, 46, "Petição de Cecília", 22), P(f"M{PX + 14} 62 H{PX + PW - 14}", S.GRID, 1),
          T(DX + 14, 46, "Dispositivo", 22), P(f"M{DX + 14} 62 H{DX + DW - 14}", S.GRID, 1)]
    roles = [("entrega da máquina", ["pedido principal"]),
             ("equivalente em dinheiro", ["subsidiário: só se o principal", "for rejeitado (art. 326)"]),
             ("reembolso do aluguel", ["cumulado com a entrega:", "cumulação simples"])]
    for y, (nm, rl) in zip(ys, roles):
        b.append(T(PX + 14, y - 14, nm, 17))
        for k, ln in enumerate(rl):
            b.append(T(PX + 14, y + 6 + k * 18, ln, 13.5, S.INK2))
    # wires through the four columns
    x_in, x_out = PX + PW, DX
    ent, eq, reem = ys
    for y in (ent, reem):
        b.append(P(f"M{x_in} {y} H{x_out}", S.DIF, 2.6))
    b.append(P(f"M{x_in} {eq} H{x_out}", S.INK2, 1.8, stroke_dasharray="6 5"))
    for y in ys:
        for i in range(4):
            b.append(dot(CX0 + i * CW + CW / 2, y, True, S.INK if y != eq else S.INK2, 4.5))
        b += [dot(x_in, y, False, S.INK), dot(x_out, y, False, S.INK)]
    # the limit of art. 329 crosses every row
    b.append(P(f"M{t2} 220 V404", S.CONC, 4))
    # dispositivo: outcome per pedido
    def verdict(y, ghost=False):
        x = DX + 16
        if ghost:
            return [S.rect(x, y - 24, 14, 14, fill="none", stroke=S.GRID, stroke_width=1.2, stroke_dasharray="3 3"),
                    S.rect(x + 74, y - 24, 14, 14, fill="none", stroke=S.GRID, stroke_width=1.2, stroke_dasharray="3 3"),
                    T(x + 20, y - 12, "acolhe", 13.5, S.INK2), T(x + 94, y - 12, "rejeita", 13.5, S.INK2)]
        return [S.rect(x, y - 24, 14, 14, fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
                S.rect(x + 74, y - 24, 14, 14, fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
                T(x + 20, y - 12, "acolhe", 13.5, S.INK), T(x + 94, y - 12, "rejeita", 13.5, S.INK)]
    b += verdict(ent) + [T(DX + 16, ent + 8, "examinada primeiro", 13.5, S.INK2)]
    b += verdict(eq, True) + [T(DX + 16, eq + 8, "examinado se a entrega", 13.5, S.INK2),
                              T(DX + 16, eq + 25, "for rejeitada", 13.5, S.INK2)]
    b += verdict(reem) + [T(DX + 16, reem + 8, "julgado à parte, seja qual", 13.5, S.INK2),
                          T(DX + 16, reem + 26, "for o da entrega", 13.5, S.INK2)]
    return b


def hero(p):
    return S.svg(1120, 440, "Os três pedidos de Cecília atravessam os quatro momentos de controle da inicial, interpretar, corrigir, estabilizar e julgar, até o dispositivo: o equivalente só é examinado se a entrega for rejeitada e o reembolso é julgado à parte", planta(p))


def fecho(p):
    return S.svg(1120, 430, "Os mesmos fios, agora lidos, corrigidos e estabilizados: a decisão entrega e reembolsa, e o equivalente fica sem julgamento", board(True))


# ───────────────────────── the three stepped studies ─────────────────────────
# Sheets are 150 wide, wires 128 long; rows sit at fixed heights in every state.

CX = dict(lx=12, lw=140, rx=268, rw=200, top=22, bot=368)
ROW = dict(ent=112, eq=192, re=272)


def _cumulo_frame(stage):
    c, r = CX, ROW
    b = [*sheet(c["lx"], c["top"], c["lw"], c["bot"] - c["top"]),
         *sheet(c["rx"], c["top"], c["rw"], c["bot"] - c["top"]),
         T(c["lx"] + 16, 56, "Petição", 22), T(c["rx"] + 16, 56, "Sentença", 22),
         P(f"M{c['lx'] + 14} 72 H{c['lx'] + c['lw'] - 14}", S.GRID, 1),
         P(f"M{c['rx'] + 14} 72 H{c['rx'] + c['rw'] - 14}", S.GRID, 1),
         L(c["rx"] + 147, 92, "veredito", 12, anchor="middle")]
    b += [T(c["lx"] + 16, r["ent"] + 6, "entrega", 19), T(c["lx"] + 16, r["re"] + 6, "reembolso", 19),
          T(c["rx"] + 16, r["ent"] + 6, "entrega", 19), T(c["rx"] + 16, r["re"] + 6, "reembolso", 19)]
    return b


def _boxes(x, y, state=None):
    """Two verdict boxes, 'acolhe' and 'rejeita'; state: None | granted | partial | ghost."""
    b = []
    if state == "ghost":
        return [S.rect(x, y - 8, 15, 15, fill="none", stroke=S.GRID, stroke_width=1, stroke_dasharray="3 3"),
                S.rect(x + 24, y - 8, 15, 15, fill="none", stroke=S.GRID, stroke_width=1, stroke_dasharray="3 3")]
    b += [S.rect(x, y - 8, 15, 15, fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
          S.rect(x + 24, y - 8, 15, 15, fill=S.PAPER, stroke=S.INK, stroke_width=1.4)]
    if state == "granted":
        b.append(tick(x + 1, y + 1))
    elif state == "partial":
        b.append(S.path(f"M{x} {y + 7} L{x + 15} {y + 7} L{x + 15} {y - 8} Z", fill=S.DIF, stroke="none"))
        b.append(T(x + 52, y + 6, "?", 18, S.CONC))
    return b


def cumulo(p, stage):
    """Four states: 1 independent wires, 2 sucessiva (the second waits on the first), 3 the subsidiary switch, 4 partial grant."""
    c, r = CX, ROW
    xl, xr = c["lx"] + c["lw"], c["rx"]
    b = _cumulo_frame(stage)
    mid = (xl + xr) / 2
    b += [P(f"M{xl} {r['ent']} H{xr}", S.DIF, 2.6),
          dot(xl, r["ent"], False), dot(xl, r["re"], False), dot(xr, r["ent"]), dot(xr, r["re"])]
    if stage == 2:
        # sucessiva: the reembolso wire runs through a switch held closed by the entrega's grant
        b += [P(f"M{xl} {r['re']} H{mid - 20}", S.DIF, 2.6), *lever_switch(mid - 20, mid + 20, r["re"], True, S.DIF),
              P(f"M{mid + 25} {r['re']} H{xr}", S.DIF, 2.6),
              dot(mid, r["ent"], False, S.DIF),
              P(f"M{mid} {r['ent'] + 5} V{r['re'] - 3}", S.DIF, 1.4, stroke_dasharray="2 4"),
              T(mid, r["re"] + 34, "condiciona", 15, S.INK2, anchor="middle")]
    else:
        b.append(P(f"M{xl} {r['re']} H{xr}", S.DIF, 2.6))
    st = {1: 1, 2: 0, 3: 2, 4: 3}[stage]       # the older three-state logic
    ent_state = None if st in (0, 1) else ("granted" if st == 2 else "partial")
    bx = c["rx"] + 132
    b += _boxes(bx, r["ent"], ent_state) + _boxes(bx, r["re"], None)
    if st >= 2:
        b += [T(c["lx"] + 16, r["eq"] + 6, "equivalente", 19),
              T(c["rx"] + 16, r["eq"] + 6, "equivalente", 19, S.INK2),
              P(f"M{xl} {r['eq']} H{mid - 20}", S.INK2, 1.6, stroke_dasharray="5 5"),
              *lever_switch(mid - 20, mid + 20, r["eq"], False, S.CONC if st == 3 else S.INK2),
              P(f"M{mid + 25} {r['eq']} H{xr}", S.INK2, 1.6, stroke_dasharray="5 5"),
              dot(xl, r["eq"], False), dot(xr, r["eq"]),
              dot(mid, r["ent"], False, S.CONC if st == 3 else S.INK2),
              P(f"M{mid} {r['ent'] + 5} V{r['eq'] - 24}", S.CONC if st == 3 else S.INK2, 1.2, stroke_dasharray="2 4"),
              T(mid, r["eq"] + 34, "aguarda", 14.5, S.INK2, anchor="middle")]
        b += _boxes(bx, r["eq"], "ghost")
        if st == 2:
            b += [T(c["rx"] + 16, r["eq"] + 30, "sem julgamento", 13.5, S.INK2)]
    if st == 3:
        # the principal is only partly granted: the wire breaks into its granted share and the rest
        b += [P(f"M{xl + 52} {r['ent'] - 14} V{r['ent'] + 14}", S.CONC, 2.6),
              T(c["lx"] + 16, r["re"] + 50, "a preferência", 16, S.CONC),
              T(c["lx"] + 16, r["re"] + 70, "precisa ser lida", 16, S.CONC)]
    return S.svg(480, 390, "Pedidos ligados à sentença: dois fios independentes, um fio que depende do primeiro, um equivalente que só conduz se a entrega falhar e a entrega acolhida em parte", b)


def _books(x, y, label, color, w=140, n=1, pitch=34):
    out = []
    for i in range(n):
        yy = y + i * pitch
        out += [S.path(f"M{x} {yy} Q{x + 4} {yy - 4} {x + 10} {yy} H{x + w} V{yy + 27} H{x + 10} Q{x + 4} {yy + 23} {x} {yy + 27} Z",
                       fill=S.PAPER, stroke=color, stroke_width=1.5),
                P(f"M{x + 13} {yy} V{yy + 27}", S.GRID, 1),
                T(x + 24, yy + 19, label, 15, color)]
    return out


def dispositivo(p, stage):
    lx, rx = 20, 312
    b = [T(lx, 30, "O pedido", 21), T(rx, 30, "A decisão", 21)]
    b += _books(lx, 52, "Calamandrei", S.INK, 148, 3)
    # the request also carries a slip for the indemnity
    slip = [S.path("M0 0 H148 V46 L140 43 L132 47 L124 43 L116 47 L108 43 L100 47 L92 43 L84 47 L76 43 L68 47 L60 43 L52 47 L44 43 L36 47 L28 43 L20 47 L12 43 L4 47 L0 44 Z",
                   fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
            T(14, 28, "indenização", 16)]
    b.append(f'<g transform="translate({lx} 170)">{"".join(slip)}</g>')
    ry = 255 if stage == 1 else 193
    b += [P("M176 82 H300", S.DIF, 2.2), dot(176, 82, False), dot(300, 82),
          P(f"M176 193 C238 193 238 {ry} 300 {ry}", S.DIF, 2.2), dot(176, 193, False), dot(300, ry)]
    name = "Chiovenda" if stage == 2 else "Calamandrei"
    count = 5 if stage == 1 else 3
    for i in range(count):
        extra = stage == 1 and i >= 3
        b += _books(rx, 52 + i * 34, name, S.CONC if (extra or stage == 2) else S.INK, 148)
    if stage == 1:
        b += [P("M470 52 q8 0 8 8 V138 q0 8 -8 8", S.CONC, 1.6)]
    if stage < 3:
        slip_y = 232 if stage == 1 else 170
        b.append(f'<g transform="translate({rx} {slip_y})">{"".join(slip)}</g>')
    else:
        b += [S.path(f"M{rx} 170 H{rx + 148} V216 H{rx} Z", fill="none", stroke=S.CONC, stroke_width=1.4, stroke_dasharray="5 5"),
              T(rx + 14, 198, "sem exame", 16, S.CONC)]
    tag = {1: "ultra petita · duas a mais", 2: "extra petita · outro objeto", 3: "infra petita · pedido sem resposta"}[stage]
    b += [P("M20 304 H464", S.GRID, 1), T(20, 338, "quantidade", 15, S.INK2 if stage != 1 else S.CONC),
          T(180, 338, "objeto", 15, S.INK2 if stage != 2 else S.CONC),
          T(320, 338, "resposta", 15, S.INK2 if stage != 3 else S.CONC),
          L(20, 366, tag, 14, S.CONC)]
    return S.svg(480, 390, "As coleções pedidas e decididas distinguem a decisão ultra, extra e infra petita", b)


def controle(p, stage):
    b = [*sheet(20, 18, 232, 232), T(40, 52, "Inicial", 22), P("M38 66 H234", S.GRID, 1)]
    rows = [("partes", 96), ("causa de pedir", 130), ("pedido", 164), ("valor da causa", 198)]
    for name, y in rows:
        b += [T(40, y, name, 17.5), P(f"M38 {y + 12} H234", S.GRID, 1)]
    # the defect: a blank value, marked by the judge
    b += [P("M138 200 H232", S.INK2, 1.2, stroke_dasharray="2 4"),
          P("M236 184 V214", S.CONC, 3), dot(236, 199, False, S.CONC)]
    if stage == 1:
        b += [S.rect(270, 40, 196, 52, fill=S.PAPER, stroke=S.INK2, stroke_width=1.2),
              T(284, 72, "Regularize a inicial", 17, S.INK2),
              P("M280 66 H456", S.CONC, 2.4),
              S.rect(270, 112, 196, 92, fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
              T(284, 140, "Indique o valor", 17.5), T(284, 162, "da causa (art. 292)", 17.5),
              T(284, 188, "e complete a inicial", 17.5),
              P("M270 158 C252 160 246 190 240 199", S.DIF, 1.8), dot(240, 199, False, S.DIF)]
    elif stage == 2:
        b += [S.rect(270, 112, 196, 92, fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
              T(284, 140, "Indique o valor", 17.5), T(284, 162, "da causa (art. 292)", 17.5),
              T(284, 188, "e complete a inicial", 17.5),
              P("M270 158 C252 160 246 190 240 199", S.DIF, 1.8), dot(240, 199, False, S.DIF)]
        for i in range(15):
            b.append(S.rect(28 + i * 22, 292, 18, 28, fill=S.PAPER, stroke=S.INK, stroke_width=1.3))
        for i in range(3):
            b.append(S.rect(28 + (15 + i) * 22, 292, 18, 28, fill="none", stroke=S.INK2, stroke_width=1.2, stroke_dasharray="3 3"))
        b += [P("M28 336 H434", S.GRID, 1), T(28, 362, "15 dias úteis", 18),
              T(434, 362, "prorrogáveis antes do fim", 15.5, S.INK2, anchor="end")]
    else:
        b += [P("M136 252 C136 282 80 280 70 318", S.DIF, 2.4), P("M168 252 C168 282 230 280 246 318", S.CONC, 2.4),
              P("M70 318 l-4 -10 M70 318 l9 -7", S.DIF, 2.4),
              T(20, 350, "a parte apta", 17, S.DIF), T(20, 372, "prossegue", 17, S.DIF),
              P("M232 322 H262", S.CONC, 3), T(214, 350, "a parte viciada", 17, S.CONC),
              T(214, 372, "fica de fora", 17, S.CONC),
              T(270, 80, "indeferimento parcial:", 17), T(270, 104, "agravo de instrumento", 17),
              T(270, 150, "indeferimento total:", 17, S.INK2), T(270, 174, "sentença e apelação", 17, S.INK2)]
    return S.svg(480, 390, "A inicial recebe ordem precisa, prazo para corrigir e, se um pedido persistir viciado, apenas essa parte fica de fora", b)


# ───────────────────────────── plates and margin glosses ─────────────────────────────

def vias(p):
    """Three sentences race to satisfaction: two carry their technique inside, one hands it to a second stage (1084 x 350)."""
    W, H = 1084, 360
    A, B, C = 100, 166, 288
    SX, SW = 16, 246
    EX = 950
    b = [*sheet(SX, 30, SW, 306), *sheet(EX - 6, 30, W - EX - 12, 306)]
    b += [T(SX + 20, 66, "Sentença", 23), P(f"M{SX + 20} 80 H{SX + 190}", S.GRID, 1),
          T(EX + 14, 66, "Satisfação", 20), P(f"M{EX + 14} 80 H{W - 32}", S.GRID, 1)]
    rows = [(A, "mandamental", "ordem de entrega, com multa"),
            (B, "executiva", "busca e apreensão"),
            (C, "condenatória", "reembolso do aluguel")]
    for y, name, sub in rows:
        b += [T(SX + 20, y - 2, name, 19), T(SX + 20, y + 18, sub, 13.5, S.INK2)]
    # intrinsic: the technique sits inside the sentence itself
    for y in (A, B):
        b += [P(f"M{SX + SW - 24} {y} H{EX - 6}", S.DIF, 2.6),
              S.rect(SX + SW - 36, y - 8, 16, 16, fill=S.PAPER, stroke=S.DIF, stroke_width=1.8),
              dot(EX - 6, y)]
    b += [T(330, A - 20, "executividade intrínseca", 16, S.DIF),
          T(330, A + 28, "a multa pressiona a oficina a devolver a máquina", 14.5, S.INK2),
          T(330, B + 28, "a busca e apreensão vai buscá-la, sem outro processo", 14.5, S.INK2)]
    # extrinsic: a gate, then a second stage with its own steps
    xa, xb = 296, 352
    b += [P(f"M{SX + SW} {C} H{xa - 5}", S.INK2, 1.8), dot(SX + SW, C, False),
          *lever_switch(xa, xb, C, False, S.INK2),
          P(f"M{xb + 5} {C} H{EX - 6}", S.INK2, 1.8), dot(EX - 6, C),
          T((xa + xb) / 2, C + 30, "só se a oficina", 13.5, S.INK2, anchor="middle"),
          T((xa + xb) / 2, C + 47, "deixar de pagar", 13.5, S.INK2, anchor="middle"),
          T(330, C - 58, "executividade extrínseca", 16, S.INK2)]
    stations = [(430, "liquidação", ["só se a sentença", "for genérica"], True),
                (542, "requerimento", ["a oficina é intimada", "a pagar"], False),
                (654, "impugnação", ["a oficina pode", "impugnar"], False),
                (766, "penhora", ["localização e", "penhora de bens"], False),
                (878, "expropriação", ["adjudicação,", "alienação", "ou frutos"], False)]
    for x, name, sub, ghost in stations:
        b.append(S.rect(x - 8, C - 8, 16, 16, fill=S.PAPER, stroke=S.GRID if ghost else S.INK2, stroke_width=1.6,
                        **({"stroke_dasharray": "3 3"} if ghost else {})))
        b.append(T(x, C - 20, name, 15.5, S.INK2 if ghost else S.INK, anchor="middle"))
        for k, ln in enumerate(sub):
            b.append(T(x, C + 28 + k * 16, ln, 13, S.INK2, anchor="middle"))
    b += [T(EX + 14, C - 4, "declarada", 14, S.INK2), T(EX + 14, C + 14, "por sentença", 14, S.INK2),
          T(EX + 14, A + 4, "a obrigação", 14, S.INK2), T(EX + 14, A + 22, "cumprida", 14, S.INK2)]
    return S.svg(W, H, "Três sentenças até a satisfação: a mandamental e a executiva carregam a técnica dentro de si; a condenatória, se a oficina não pagar, passa por liquidação eventual, requerimento, impugnação, penhora e expropriação", b)


def _structure(y0, title, dashed_second, lit, cut=None):
    """One obligation: a vínculo that feeds two wires into one satisfaction node. lit: draws it in ink, else ghost."""
    ink = S.INK if lit else S.GRID
    ink2 = S.INK2 if lit else S.GRID
    wire = S.DIF if lit else S.GRID
    y1, y2 = y0 + 52, y0 + 106
    xs, xe = 40, 336
    mid = (y1 + y2) / 2
    b = [T(20, y0 + 10, title, 20, S.INK if lit else S.MUTED)]
    b += [dot(xs, mid, False, ink),
          P(f"M{xs + 5} {mid} C{xs + 40} {mid} {xs + 30} {y1} {xs + 64} {y1}", ink2, 1.6),
          P(f"M{xs + 5} {mid} C{xs + 40} {mid} {xs + 30} {y2} {xs + 64} {y2}", ink2, 1.6, **({"stroke_dasharray": "5 5"} if dashed_second else {}))]
    c1 = wire if cut not in (1, 3) else S.GRID
    c2 = wire if cut not in (2, 3) else S.GRID
    b += [P(f"M{xs + 64} {y1} H{xe - 40} C{xe - 14} {y1} {xe - 18} {mid} {xe - 4} {mid}", c1, 2.6),
          P(f"M{xs + 64} {y2} H{xe - 40} C{xe - 14} {y2} {xe - 18} {mid} {xe - 4} {mid}", c2, 2.6,
            **({"stroke_dasharray": "6 5"} if dashed_second else {})),
          dot(xe, mid, True, ink)]
    return b, y1, y2, mid, xs, xe


def perecimento(p, stage):
    """Alternative vs facultative obligation, then what perishing does to each (380 x 400, whole drawing per state)."""
    top, bot = 22, 196
    b = []
    t, y1, y2, m, xs, xe = _structure(top, "alternativa", False, stage != 2, cut=1 if stage == 3 else None)
    b += t
    lab = S.INK if stage != 2 else S.MUTED
    b += [T(xs + 70, y1 - 16, "devolver a máquina", 15, lab),
          T(xs + 70, y2 - 16, "entregar outra equivalente", 15, lab)]
    t2, z1, z2, m2, _, _ = _structure(bot, "faculdade de substituição", True, stage != 1, cut=3 if stage == 3 else None)
    b += t2
    lab2 = S.INK if stage != 1 else S.MUTED
    b += [T(xs + 70, z1 - 16, "devolver a máquina", 15, lab2),
          T(xs + 70, z2 - 16, "ou pagar seu valor", 15, S.INK2 if stage != 1 else S.MUTED)]
    if stage == 3:
        # a prestação perishes: in the alternativa the other still satisfies; in the facultativa the whole falls
        def x(cx, cy):
            return P(f"M{cx - 8} {cy - 10} l16 20 M{cx + 8} {cy - 10} l-16 20", S.CONC, 2.6)
        b += [x(xs + 240, y1), tick(xe + 12, m - 6), x(xs + 240, z1), x(xs + 240, z2)]
    b.append(P("M20 178 H360", S.GRID, 1))
    return S.svg(380, 330, "Alternativa: duas prestações no vínculo, uma satisfaz. Faculdade de substituição: uma devida, a outra só liberta o devedor. Se a prestação perece, a alternativa guarda a outra; a facultativa cai", b)


def leitura(p):
    """Two readings of a pedido, one anchored in the text, one that needs the party's real will (380 x 380, static)."""
    b = []
    # case 1: aposentadoria
    b += [*sheet(14, 20, 230, 126), T(30, 50, "o segurado narra", 14.5, S.INK2),
          T(30, 76, "invalidez, sem sustento", 17), T(30, 118, "benefício desde a citação", 17),
          P("M28 126 H228", S.DIF, 2.4),
          P("M246 118 H276", S.DIF, 2.2), dot(246, 118, False, S.DIF), dot(280, 118, True, S.DIF),
          T(294, 123, "urgência", 14.5, S.DIF),
          T(14, 168, "o texto dá apoio mínimo", 14.5, S.INK2)]
    b.append(P("M14 186 H366", S.GRID, 1))
    # case 2: desistência
    b += [*sheet(14, 206, 210, 62), T(30, 244, "desistência", 22),
          P("M226 232 C242 232 246 222 272 222", S.INK2, 1.8), dot(226, 232, False, S.INK2), dot(276, 222, True, S.INK2),
          P("M226 244 C242 244 246 262 272 262", S.CONC, 1.8, stroke_dasharray="5 4"), dot(276, 262, True, S.CONC),
          P("M250 246 V268", S.CONC, 3),
          T(290, 227, "do processo", 14.5, S.INK2), T(290, 267, "do direito", 14.5, S.CONC),
          T(14, 306, "renúncia pede", 14.5, S.INK2), T(14, 326, "vontade investigada", 14.5, S.INK2)]
    return S.svg(380, 340, "Dois pedidos lidos pelo texto: o que a narrativa sustenta e a desistência, que só vira renúncia se a vontade efetiva o confirmar", b)


def funil(p):
    """The American gate narrowing across the century against the constant Brazilian entry (1084 x 410)."""
    W, H = 1084, 432
    X0, SC = 170, 850 / 80
    X = lambda yr: X0 + (yr - 1940) * SC
    up, lo = 125, 318
    def jaws(c, pts, color=S.INK, width=2.2):
        """pts: (year, gap); two polylines mirrored on c."""
        top = " ".join(f"{'M' if i == 0 else 'L'}{X(y):.1f} {c - g / 2:.1f}" for i, (y, g) in enumerate(pts))
        bot = " ".join(f"{'M' if i == 0 else 'L'}{X(y):.1f} {c + g / 2:.1f}" for i, (y, g) in enumerate(pts))
        return [P(top, color, width), P(bot, color, width)]
    b = [T(16, up - 12, "Alegação", 22), T(16, up + 10, "a entrada na", 13.5, S.INK2), T(16, up + 27, "inicial", 13.5, S.INK2),
         T(16, lo - 12, "Investigação", 22), T(16, lo + 10, "a discovery", 13.5, S.INK2),
         P(f"M{X0 - 10} 218 H{W - 20}", S.GRID, 1)]
    # Brazil: a constant, narrow entry from the start
    b += [P(f"M{X0} {up - 21} H{W - 24}", S.INK2, 1.6, stroke_dasharray="6 5"),
          P(f"M{X0} {up + 21} H{W - 24}", S.INK2, 1.6, stroke_dasharray="6 5"),
          T(X0 + 6, up - 4, "Brasil: alegação", 13.5, S.INK2), T(X0 + 6, up + 13, "específica", 13.5, S.INK2)]
    # the American entry
    us = [(1957, 112), (2006.5, 112), (2007, 62), (2008.5, 62), (2009, 34), (2020, 34)]
    b += jaws(up, us)
    b.append(P(f"M{X(1957):.1f} {up} H{W - 24}", S.DIF, 2.6))
    for yr, nm, sub, anchor, dx in [(1957, "Conley v. Gibson (1957)", "alegação curta e simples", "middle", 0),
                                    (2007, "Bell Atlantic v. Twombly (2007)", "fato específico", "end", -6),
                                    (2009, "Ashcroft v. Iqbal (2009)", "plausibilidade", "start", 6)]:
        g = dict(us)[yr] if yr in dict(us) else 112
        b += [P(f"M{X(yr):.1f} 50 V{up - 6}", S.GRID, 1, stroke_dasharray="2 4"), dot(X(yr), up, False, S.INK, 4.5),
              T(X(yr) + dx, 40, nm, 15, S.INK, anchor=anchor),
              T(X(yr) + dx, up + 56 + 22, sub, 13.5, S.INK2, anchor=anchor)]
    # discovery: a band that tightens
    dis = [(1947, 120), (1975.5, 120), (1976, 96), (1999.5, 96), (2000, 66), (2014.5, 66), (2015, 38), (2020, 38)]
    b += jaws(lo, dis)
    b.append(P(f"M{X(1947):.1f} {lo} H{W - 24}", S.DIF, 2.6))
    for yr, nm, sub in [(1947, "Hickman v. Taylor (1947)", ["integra o preparo", "do caso"]),
                        (1976, "National Hockey League", ["v. Metropolitan Hockey Club", "sanções por abuso"]),
                        (2000, "Pertinência", ["da ação à pretensão", "ou defesa"]),
                        (2015, "Proporcionalidade", ["custos ao resultado", "esperado"])]:
        g = dict(dis)[yr]
        b += [P(f"M{X(yr):.1f} {lo - 60 - 8} V{lo - 6}", S.GRID, 1, stroke_dasharray="2 4"), dot(X(yr), lo, False, S.INK, 4.5),
              T(X(yr), lo - 60 - 14, nm, 15, S.INK, anchor="middle")]
        for k, ln in enumerate(sub):
            b.append(T(X(yr), lo + 60 + 22 + k * 16, ln, 13.5, S.INK2, anchor="middle"))
    return S.svg(W, H, "A entrada nas Federal Rules estreita de alegação curta e simples a fato específico e plausibilidade, e a discovery recebe limites sucessivos, enquanto a inicial brasileira exige alegação específica desde o começo", b)


def build(p: dict) -> tuple[str, list[dict]]:
    mode = p.get("mode")
    if mode in ("hero", "fecho", "vias", "leitura", "funil"):
        return {"hero": hero, "fecho": fecho, "vias": vias, "leitura": leitura, "funil": funil}[mode](p), []
    fn = {"cumulo": cumulo, "dispositivo": dispositivo, "controle": controle, "perecimento": perecimento}.get(mode)
    if fn is None:
        raise ValueError("pedidos_caderno mode must be hero, fecho, cumulo, dispositivo, controle, vias, perecimento, leitura or funil")
    n = 4 if mode == "cumulo" else 3
    if p.get("stage"):
        return fn(p, int(p["stage"])), []
    prefix = p.get("stepped")
    if not prefix:
        return fn(p, n), []
    panels = []
    for stage in range(1, n + 1):
        panels.append(f'<div class="panel{" on" if stage == 1 else ""}" id="{S.esc(prefix)}-{stage}">{fn(p, stage)}</div>')
    return "".join(panels), []
