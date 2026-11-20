"""Boa-fé e formação: segundo passe dos desenhos (ruptura, correio, dossiê).

Params: mode=ruptura|correio|dossie.
`ruptura` is a measured picture: five acts piled up (count), a missing capstone, and two columns drawn to scale
(R$ 200.000 alleged expenses; R$ 1.075.000 budget of the event). Facts: STJ REsp 1.367.955/SP pp.9-11.
`correio` is a letter's journey (declarar, expedir, receber, conhecer) over a pile of arrivals at the door: the pile
order is the order of arrival; three groups (data-order 0|1|2) are switched by the range control. No time scale.
`dossie` is the contract file seen from the front: earlier phases sit under the clause as offset sheets with tabs.
"""
from . import svg as S

T = S.text


def _ln(*a, **k):
    k.setdefault('stroke', S.INK)
    k.setdefault('stroke_width', 1.4)
    return S.line(*a, **k)


def _env(x, y, w, h, stroke=S.INK, fill=S.PAPER, sw=1.5, dash=None):
    """A flat envelope: body and the flap's V."""
    kw = dict(stroke_dasharray=dash) if dash else {}
    return [S.rect(x, y, w, h, fill=fill, stroke=stroke, stroke_width=sw, **kw),
            S.path(f'M{x},{y} L{x + w / 2},{y + h * .62} L{x + w},{y}', fill='none', stroke=stroke, stroke_width=sw, **kw)]


def ruptura():
    w, h = 860, 350
    o = []
    base = 300
    o.append(_ln(30, base, 830, base, stroke_width=1.6))
    # left: the pile of acts (a count, one slab each)
    acts = ['reuniões', 'e-mails', 'visita técnica', 'memoriais descritivos', 'terceiros contratados']
    x0, sw_, sh = 60, 250, 36
    for i, a in enumerate(acts):
        y = base - (i + 1) * sh
        o += [S.rect(x0, y, sw_, sh, fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
              T(x0 + 14, y + 23, a, size=14, family=S.SERIF)]
    ytop = base - 5 * sh
    o += [S.rect(x0, ytop - sh, sw_, sh, fill='none', stroke=S.CONC, stroke_width=1.6, stroke_dasharray='6 5'),
          T(x0 + 14, ytop - sh + 23, 'contrato', size=14, family=S.SERIF, fill=S.CONC)]
    o += [T(x0, 36, 'a confiança construída', size=16, family=S.SERIF),
          T(x0, 56, 'cinco atos, um sobre o outro', size=12, fill=S.MUTED)]
    # right: two columns to scale
    top = 78
    th = base - top  # 222 px = R$ 1.075.000
    sc = th / 1075000
    c1x, c2x, cw = 400, 610, 120
    h200 = 200000 * sc
    o += [S.rect(c1x, top, cw, th, fill='none', stroke=S.INK2, stroke_width=1.5, stroke_dasharray='6 5'),
          T(c1x + cw / 2, top + 24, 'evento', size=14, family=S.SERIF, anchor='middle'),
          T(c1x + cw / 2, top + 44, 'R$ 1.075.000', size=13, anchor='middle'),
          S.rect(c2x, base - h200, cw, h200, fill=S.PAPER, stroke=S.INK, stroke_width=1.8)]
    o += S.hatch(c2x, base - h200, cw, h200, step=8, stroke=S.INK, stroke_width=.8, opacity='.45')
    o += [T(c2x + cw / 2, base - h200 - 12, 'R$ 200.000', size=13, anchor='middle'),
          T(c2x + cw / 2, base + 22, 'despesas alegadas', size=13, family=S.SERIF, anchor='middle'),
          T(c1x + cw / 2, base + 22, 'orçamento', size=13, family=S.SERIF, anchor='middle')]
    # the remedy: a bracket on the small column, the exclusion on the tower
    o += [S.path(f'M{c2x + cw + 14},{base} H{c2x + cw + 24} V{base - h200} H{c2x + cw + 14}', fill='none', stroke=S.DIF, stroke_width=1.8),
          T(c2x + cw + 32, base - h200 / 2 + 5, 'reparado', size=14, family=S.SERIF, fill=S.DIF, weight=600)]
    o += [S.path(f'M{c1x + cw + 14},{top} H{c1x + cw + 24} V{base - h200 - 8} H{c1x + cw + 14}', fill='none', stroke=S.CONC, stroke_width=1.8),
          T(c1x + cw + 32, (top + base - h200) / 2 + 5, 'lucro estimado', size=14, family=S.SERIF, fill=S.CONC, weight=600),
          T(c1x + cw + 32, (top + base - h200) / 2 + 24, 'afastado', size=14, family=S.SERIF, fill=S.CONC, weight=600)]
    o += [T(x0 + sw_ + 40, 36, 'a escala', size=16, family=S.SERIF), T(x0 + sw_ + 40, 56, 'só as duas colunas à direita', size=12, fill=S.MUTED)]
    return S.svg(w, h, 'Tratativas interrompidas: cinco atos sem contrato; despesas e evento em escala', o)


def correio():
    w, h = 900, 335
    o = []
    # the road
    road = 118
    o += [_ln(70, road, 830, road, stroke_width=2.2),
          _ln(70, road + 8, 830, road + 8, stroke_width=.9, stroke_dasharray='2 7')]
    xs = [95, 310, 590, 810]
    # 1 declarar: a sheet with writing
    x = xs[0]
    o += [S.rect(x - 24, road - 70, 48, 58, fill=S.PAPER, stroke=S.INK, stroke_width=1.5)]
    o += [_ln(x - 15, road - 56 + k * 10, x + 15 - (6 if k == 3 else 0), road - 56 + k * 10, stroke_width=1) for k in range(4)]
    # 2 expedir: a postmark with cancel lines
    x = xs[1]
    o += [S.circle(x, road - 40, 28, fill=S.PAPER, stroke=S.INK, stroke_width=1.6),
          S.circle(x, road - 40, 20, fill='none', stroke=S.INK, stroke_width=1),
          _ln(x - 14, road - 40, x + 14, road - 40, stroke_width=1)]
    for k in range(4):
        yy = road - 54 + k * 9
        o.append(S.path(f'M{x + 34},{yy} q10,-5 20,0 t20,0 t20,0', fill='none', stroke=S.INK, stroke_width=1.1))
    # 3 receber: a door with a letter slot
    x = xs[2]
    o += [S.rect(x - 30, road - 76, 60, 76, fill=S.PAPER, stroke=S.INK, stroke_width=1.6),
          S.rect(x - 18, road - 36, 36, 6, fill=S.INK),
          S.circle(x + 20, road - 20, 2.5, fill=S.INK)]
    # 4 conhecer: an opened letter
    x = xs[3]
    o += [S.rect(x - 30, road - 56, 60, 40, fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
          S.path(f'M{x - 30},{road - 56} L{x},{road - 80} L{x + 30},{road - 56}', fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
          _ln(x - 18, road - 44, x + 18, road - 44, stroke_width=1), _ln(x - 18, road - 34, x + 8, road - 34, stroke_width=1)]
    for xx, lab in zip(xs, ['declarar', 'expedir', 'receber', 'conhecer']):
        o += [S.circle(xx, road, 5, fill=S.PAPER, stroke=S.INK, stroke_width=1.6), T(xx, road + 30, lab, size=15, family=S.SERIF, anchor='middle')]
    # the moment the contract forms: a flag over the postmark, blue (decided)
    o += [T(xs[1], road + 54, 'contrato perfeito', size=14, family=S.SERIF, fill=S.DIF, anchor='middle', weight=600),
          T(xs[1], road + 71, 'art. 434', size=12, fill=S.INK2, anchor='middle')]
    # the retraction's lane (orange, dashed) running to the door
    o += [S.path(f'M{xs[0] + 40},{road + 96} H{xs[2] - 16}', fill='none', stroke=S.CONC, stroke_width=1.6, stroke_dasharray='7 5'),
          S.path(f'M{xs[2] - 24},{road + 90} l9,6 l-9,6', fill='none', stroke=S.CONC, stroke_width=1.6)]
    o += _env(xs[0] + 8, road + 62 + 0, 0, 0) if False else []
    o += _env(xs[0] + 40, road + 108, 34, 22, stroke=S.CONC)
    o += [T(xs[0] + 84, road + 124, 'retratação', size=14, family=S.SERIF, fill=S.CONC)]
    # the pile at the door: order of arrival = order of layers
    floor = 300
    px = xs[2] - 90
    ew, eh = 170, 24
    o += [_ln(px - 20, floor, px + ew + 20, floor, stroke_width=1.6),
          T(px + ew / 2, floor + 18, 'camadas na ordem de chegada', size=12, fill=S.MUTED, anchor='middle')]
    # state 0: retraction first (bottom), acceptance on top (ghosted)
    g0 = _env(px, floor - eh, ew, eh, stroke=S.CONC) + _env(px + 10, floor - 2 * eh - 4, ew - 20, eh, stroke=S.INK, fill=S.PAPER, dash='5 4') + [
        T(px + ew + 30, floor - 10, 'retratação chegou primeiro', size=13, family=S.SERIF, fill=S.CONC),
        T(px + ew + 30, floor - eh - 28, 'aceitação inexistente', size=13, family=S.SERIF)]
    # state 1: side by side, same layer
    hw = ew / 2 - 5
    g1 = _env(px, floor - eh, hw, eh, stroke=S.CONC) + _env(px + hw + 10, floor - eh, hw, eh, stroke=S.INK, dash='5 4') + [
        T(px + ew + 30, floor - 10, 'chegaram juntas', size=13, family=S.SERIF, fill=S.CONC),
        T(px + ew + 30, floor - eh - 28, 'aceitação inexistente', size=13, family=S.SERIF)]
    # state 2: acceptance first (bottom), retraction on top
    g2 = _env(px, floor - eh, ew, eh, stroke=S.DIF, sw=2) + _env(px + 10, floor - 2 * eh - 4, ew - 20, eh, stroke=S.CONC) + [
        T(px + ew + 30, floor - 10, 'aceitação chegou primeiro', size=13, family=S.SERIF, fill=S.DIF),
        T(px + ew + 30, floor - eh - 28, 'retratação tardia', size=13, family=S.SERIF)]
    for i, g in enumerate((g0, g1, g2)):
        o.append(f'<g data-order="{i}"' + ('' if i == 0 else ' display="none"') + '>' + ''.join(g) + '</g>')
    return S.svg(w, h, 'A jornada da carta de aceitação e a ordem de chegada da retratação', o)


def dossie():
    w, h = 860, 400
    o = []
    x0, wd = 40, 640
    tabs = ['tratativas', 'proposta', 'aceitação', 'formação', 'depois']
    step, y, bot = 38, 18, 358

    def sheet(yy, stroke, sw):
        return S.path(f'M{x0},{yy} H{x0 + wd} V{bot} H{x0} Z', fill=S.PAPER, stroke=stroke, stroke_width=sw)

    def tab(yy, stroke, sw):
        return S.path(f'M{x0 + wd},{yy + 2} h120 v28 h-120', fill=S.PAPER, stroke=stroke, stroke_width=sw)
    for i, t in enumerate(tabs):
        yy = y + i * step
        o += [sheet(yy, S.INK, 1.5), tab(yy, S.INK, 1.5), T(x0 + wd + 14, yy + 21, t, size=14, family=S.SERIF)]
    fy = y + len(tabs) * step
    o += [sheet(fy, S.INK, 2), tab(fy, S.DIF, 2), T(x0 + wd + 14, fy + 21, 'cláusula', size=14, family=S.SERIF, fill=S.DIF, weight=600)]
    for k in range(5):
        o.append(_ln(x0 + 24, fy + 26 + k * 20, x0 + wd - 30 - (90 if k in (1, 4) else 0), fy + 26 + k * 20, stroke_width=1, stroke=S.INK2))
    o.append(_ln(x0 + 24, fy + 49, x0 + 230, fy + 49, stroke=S.DIF, stroke_width=2.4))
    return S.svg(w, h, 'O contrato como dossiê: a cláusula escrita sobre as folhas das fases anteriores', o)


def build(p):
    mode = p.get('mode', 'ruptura')
    if mode not in ('ruptura', 'correio', 'dossie'):
        raise ValueError(mode)
    return {'ruptura': ruptura, 'correio': correio, 'dossie': dossie}[mode](), []
