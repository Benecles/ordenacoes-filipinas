"""pedidos_caderno: the petition's pedidos as wires, for the Aula 01 companion.

Params:
  mode: hero | fecho | cumulo | dispositivo | controle (required).
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


def hero(p):
    return S.svg(1120, 430, "Cecília pede a entrega, o equivalente em dinheiro e o reembolso: o equivalente só conduz se a entrega não for acolhida, e o reembolso segue fio próprio até o dispositivo", board(False))


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
    c, r = CX, ROW
    xl, xr = c["lx"] + c["lw"], c["rx"]
    b = _cumulo_frame(stage)
    mid = (xl + xr) / 2
    # two independent wires: each pedido has its own verdict
    b += [P(f"M{xl} {r['ent']} H{xr}", S.DIF, 2.6), P(f"M{xl} {r['re']} H{xr}", S.DIF, 2.6),
          dot(xl, r["ent"], False), dot(xl, r["re"], False), dot(xr, r["ent"]), dot(xr, r["re"])]
    ent_state = None if stage == 1 else ("granted" if stage == 2 else "partial")
    bx = c["rx"] + 132
    b += _boxes(bx, r["ent"], ent_state) + _boxes(bx, r["re"], None)
    if stage >= 2:
        b += [T(c["lx"] + 16, r["eq"] + 6, "equivalente", 19),
              T(c["rx"] + 16, r["eq"] + 6, "equivalente", 19, S.INK2),
              P(f"M{xl} {r['eq']} H{mid - 20}", S.INK2, 1.6, stroke_dasharray="5 5"),
              *lever_switch(mid - 20, mid + 20, r["eq"], False, S.CONC if stage == 3 else S.INK2),
              P(f"M{mid + 25} {r['eq']} H{xr}", S.INK2, 1.6, stroke_dasharray="5 5"),
              dot(xl, r["eq"], False), dot(xr, r["eq"]),
              dot(mid, r["ent"], False, S.CONC if stage == 3 else S.INK2),
              P(f"M{mid} {r['ent'] + 5} V{r['eq'] - 24}", S.CONC if stage == 3 else S.INK2, 1.2, stroke_dasharray="2 4"),
              T(mid, r["eq"] + 34, "aguarda", 14.5, S.INK2, anchor="middle")]
        b += _boxes(bx, r["eq"], "ghost")
        if stage == 2:
            b += [T(c["rx"] + 16, r["eq"] + 30, "sem julgamento", 13.5, S.INK2)]
    if stage == 3:
        # the principal is only partly granted: the wire breaks into its granted share and the rest
        b += [P(f"M{xl + 52} {r['ent'] - 14} V{r['ent'] + 14}", S.CONC, 2.6),
              T(c["lx"] + 16, r["re"] + 50, "a preferência", 16, S.CONC),
              T(c["lx"] + 16, r["re"] + 70, "precisa ser lida", 16, S.CONC)]
    return S.svg(480, 390, "Pedidos ligados à sentença: dois fios independentes, um equivalente que só conduz se a entrega falhar e a entrega acolhida em parte", b)


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


def build(p: dict) -> tuple[str, list[dict]]:
    mode = p.get("mode")
    if mode in ("hero", "fecho"):
        return (hero(p) if mode == "hero" else fecho(p)), []
    fn = {"cumulo": cumulo, "dispositivo": dispositivo, "controle": controle}.get(mode)
    if fn is None:
        raise ValueError("pedidos_caderno mode must be hero, fecho, cumulo, dispositivo or controle")
    if p.get("stage"):
        return fn(p, int(p["stage"])), []
    prefix = p.get("stepped")
    if not prefix:
        return fn(p, 3), []
    panels = []
    for stage in range(1, 4):
        panels.append(f'<div class="panel{" on" if stage == 1 else ""}" id="{S.esc(prefix)}-{stage}">{fn(p, stage)}</div>')
    return "".join(panels), []
