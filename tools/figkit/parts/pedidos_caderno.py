"""pedidos_caderno: working papers for the Aula 01 companion.

Params:
  mode: hero | cumulo | dispositivo | controle | fecho (required).
  stepped: optional panel-id prefix, for the three cumulative scroll states
    of cumulo, dispositivo and controle. No selectors or folded corners.

The objects are an open sewn case notebook, a sewing machine, the books
requested in Mitidiero's example, and the petition annotated by its judge.
All canvases use house tokens; hero/fecho are 1120×430, marginal studies
are 470×410. Legal facts: MAM v.2 pp.155–168; Didier v.1 pp.640–665;
Mitidiero (2022) pp.173–174; CPC 321,326,327,331,492,499.
"""
from __future__ import annotations

from . import svg as S


def t(x, y, text, size=15, fill=S.INK, **kw):
    return S.text(x, y, text, size=size, family=S.SERIF, fill=fill, **kw)


def path(d, color=S.INK, width=1.5, **kw):
    return S.path(d, fill="none", stroke=color, stroke_width=width,
                  stroke_linecap="round", stroke_linejoin="round", **kw)


def paper(x, y, w, h, color=S.INK):
    return [S.rect(x+4, y+5, w, h, fill=S.PAPER, stroke=S.GRID),
            S.rect(x, y, w, h, fill=S.PAPER, stroke=color, stroke_width=1.4)]


def machine(x, y, scale=1):
    # Sewing-machine head, wheel, needle, bed and stitch: Cecília's own good.
    body = [path("M5 120 H158 V136 H5 Z"),
            path("M28 118 V82 H67 V106 H126 V59 H64 V73 H27 V48 Q27 26 52 26 H128 Q149 26 149 48 V119"),
            S.circle(146, 55, 21, fill=S.PAPER, stroke=S.INK, stroke_width=1.8),
            S.circle(146, 55, 12, fill="none", stroke=S.INK2),
            path("M40 82 V106 M33 109 H49 M66 25 V14 H94 V25 M78 14 V8"),
            path("M17 127 H146", S.GRID, 1),
            path("M44 110 Q57 116 76 110 Q94 105 113 110", S.DIF, 1.6)]
    return '<g transform="translate(%s %s) scale(%s)">%s</g>' % (x, y, scale, "".join(body))


def book(x, y, label, color=S.INK, w=105):
    return [S.path(f"M{x} {y} Q{x+4} {y-4} {x+10} {y} H{x+w} V{y+29} H{x+10} Q{x+4} {y+25} {x} {y+29} Z",
                   fill=S.PAPER, stroke=color, stroke_width=1.4),
            path(f"M{x+12} {y} V{y+29} M{x+17} {y+24} H{x+w-3}", S.GRID, 1),
            t(x+19, y+18, label, 12, fill=color)]


def hero(p):
    b = [t(28, 31, "A causa abre-se em pedidos; a sentença devolve cada fio ao seu lugar.", 21)]
    b += paper(35, 69, 284, 292)
    b += [t(56, 98, "Petição de Cecília", 22), t(56, 126, "máquina retida · aluguel de outra", 15, fill=S.INK2),
          path("M56 144 H293", S.GRID, 1), t(56, 179, "entrega da máquina", 20, fill=S.DIF),
          t(56, 210, "se a entrega não puder ser obtida:", 14), t(56, 235, "equivalente em dinheiro", 18),
          t(56, 285, "+ reembolso do aluguel", 20, fill=S.DIF),
          t(56, 334, "dois resultados · uma preferência", 14, fill=S.INK2)]
    # The thread for the preferred good forks, while damages keep an
    # independent course. A stitched notebook carries both into judgment.
    b += [path("M319 171 C411 172 410 100 535 112 S743 93 800 123", S.DIF, 2.4),
          path("M370 168 C435 174 439 218 535 221 S722 244 807 225", S.INK2, 1.5, stroke_dasharray="5 5"),
          path("M319 281 C449 287 517 329 638 324 S751 292 807 301", S.DIF, 2.4),
          t(390, 86, "a tutela conserva o bem pedido", 15),
          t(457, 200, "a reserva aguarda a principal", 15, fill=S.INK2),
          t(470, 357, "o reembolso tem julgamento próprio", 15),
          machine(560, 55, .68)]
    b += paper(811, 69, 277, 292)
    b += [t(833, 99, "Dispositivo", 22), path("M832 143 H1067", S.GRID, 1),
          t(833, 177, "entrega", 21, fill=S.DIF), t(833, 229, "ou equivalente", 19),
          t(833, 282, "reembolso", 21, fill=S.DIF),
          path("M1080 151 H1098 V302 H1080", S.CONC, 2),
          t(833, 334, "arts. 141, 492 e 499", 14, fill=S.INK2),
          path("M36 382 Q421 397 811 382 H1091", S.INK2, 1),
          t(42, 410, "pedir", 16), t(351, 410, "interpretar · corrigir", 16),
          t(805, 410, "julgar · efetivar", 16)]
    return S.svg(1120, 430, "Os pedidos de Cecília seguem fios distintos até o dispositivo, com uma reserva subordinada à entrega", b)


def cumulo(p, stage):
    b = paper(28, 34, 408, 326)
    b += [path("M231 35 V359", S.GRID, 1), t(47, 65, "Petição", 23), t(250, 65, "Sentença", 23),
          t(47, 115, "entrega", 20), t(47, 156, "reembolso", 20),
          path("M165 108 C199 106 211 114 246 108", S.DIF, 2),
          path("M165 150 C199 147 216 154 246 150", S.DIF, 2),
          t(250, 115, "examina", 18, fill=S.DIF), t(250, 157, "examina", 18, fill=S.DIF)]
    if stage >= 2:
        b += [t(47, 219, "principal", 20), t(47, 277, "subsidiário", 20),
              path("M165 212 H231 H250", S.DIF, 2),
              path("M178 214 C202 224 205 263 245 271", S.INK2, 1.6),
              t(250, 219, "acolhido" if stage == 2 else "parcial?", 18,
                fill=S.DIF if stage == 2 else S.CONC)]
        if stage == 2:
            b += [path("M239 249 L252 285 M253 249 L239 285", S.CONC, 1.6),
                  t(275, 277, "aguarda", 17, fill=S.INK2)]
    if stage >= 3:
        b += [path("M173 213 H243", S.CONC, 1.6),
              t(251, 277, "preferência", 17), t(251, 300, "a esclarecer", 17)]
    b += [t(30, 397, ["Autonomia: dois pedidos, dois exames.", "Preferência: a reserva tem uma condição.", "A vitória parcial exige interpretar a ordem."][stage-1], 17)]
    return S.svg(470, 410, "Pedidos costurados à sentença: autonomia, subsidiariedade e procedência parcial", b)


def dispositivo(p, stage):
    b = [t(25, 30, "O pedido", 20), t(263, 30, "A decisão", 20)]
    for i in range(3):
        b += book(25, 60+i*33, "Calamandrei", w=145)
    b += [t(26, 193, "+ danos materiais", 17), path("M194 93 H238", S.DIF, 1.8)]
    count = 5 if stage == 1 else 3
    name = "Chiovenda" if stage == 2 else "Calamandrei"
    for i in range(count):
        b += book(263, 60+i*33, name, S.CONC if stage < 3 else S.DIF, 145)
    if stage == 1:
        b += [path("M420 159 H437 V221 H420", S.CONC, 2), t(264, 273, "ultra: duas coleções a mais", 16, fill=S.CONC)]
    elif stage == 2:
        b += [t(263, 221, "extra: outro objeto", 17, fill=S.CONC)]
    else:
        b += [path("M264 185 H413", S.CONC, 1.5, stroke_dasharray="4 5"),
              t(263, 221, "infra: indenização omitida", 16, fill=S.CONC)]
    b += [path("M24 317 H439", S.GRID, 1), t(25, 347, "Mudar o meio de entrega preserva o objeto.", 16),
          t(25, 374, "Mudar o livro muda a tutela pedida.", 16)]
    return S.svg(470, 410, "As coleções pedidas e entregues distinguem ultra, extra e infra petita", b)


def controle(p, stage):
    b = paper(40, 26, 347, 302)
    b += [t(60, 58, "Inicial devolvida para emenda", 20),
          path("M59 80 H365", S.GRID, 1), t(60, 112, "causa · pedido · valor", 18),
          path("M61 137 H352 M61 155 H329 M61 173 H347", S.GRID, 1),
          t(60, 209, "O que precisa ser corrigido?", 18)]
    if stage >= 2:
        b += [path("M349 107 H408 V248 H349", S.DIF, 1.8),
              t(60, 241, "ordem precisa · prazo · correção", 17, fill=S.DIF),
              path("M64 265 l8 9 l17 -23", S.DIF, 2), t(99, 272, "o autor escolhe a sua causa", 17)]
    if stage == 3:
        b += [path("M184 330 C184 349 93 348 78 369", S.DIF, 1.8),
              path("M252 330 C252 350 347 348 367 369", S.CONC, 1.8),
              t(26, 398, "parte apta prossegue", 17, fill=S.DIF),
              t(269, 398, "vício persiste", 17, fill=S.CONC)]
    else:
        b += [t(41, 385, "Esclarecer permite decidir a demanda formulada.", 16)]
    return S.svg(470, 410, "A ordem judicial marca o defeito; a emenda pertence ao autor; só a parte viciada precisa ser excluída", b)


def fecho(p):
    b = [path("M35 62 Q272 33 553 72 Q820 34 1083 62 V352 Q812 326 553 365 Q275 326 35 352 Z"),
          path("M553 72 V365", S.INK2, 1.5),
          t(68, 97, "A demanda que pode ser julgada", 24),
          t(596, 97, "O que a decisão pode entregar", 24)]
    rows=[("fatos jurídicos que sustentam a pretensão", "a tutela fundada na causa discutida"),
          ("pedidos com autonomia ou preferência", "cada pedido no seu lugar de exame"),
          ("defeito identificado e corrigido", "aproveitamento da parte admissível"),
          ("alteração submetida ao contraditório", "o objeto que ambas as partes discutiram")]
    for i,(a,z) in enumerate(rows):
        y=153+i*54
        b += [t(68,y,a,17),t(596,y,z,17,fill=S.DIF),path(f"M505 {y-5} Q553 {y+14} 581 {y-5}",S.DIF,1.4)]
    b += [path("M53 387 H1080",S.GRID,1),t(69,416,"O objeto permanece reconhecível; o meio pode ajustar-se à tutela.",20)]
    return S.svg(1120,430,"Um caderno aberto reconduz cada parte da decisão ao pedido que a autoriza",b)


def build(p: dict) -> tuple[str, list[dict]]:
    mode=p.get("mode")
    if mode in ("hero","fecho"):
        return (hero(p) if mode=="hero" else fecho(p)), []
    fn={"cumulo":cumulo,"dispositivo":dispositivo,"controle":controle}.get(mode)
    if fn is None:
        raise ValueError("pedidos_caderno mode must be hero, cumulo, dispositivo, controle or fecho")
    prefix=p.get("stepped")
    if not prefix:
        return fn(p,3),[]
    panels=[]
    for stage in range(1,4):
        panels.append(f'<div class="panel{" on" if stage==1 else ""}" id="{S.esc(prefix)}-{stage}">{fn(p,stage)}</div>')
    return "".join(panels),[]
