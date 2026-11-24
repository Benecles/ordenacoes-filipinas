"""Contract classifications, Aula 06: four drawings in four paper languages.

modes: sinalagma (party lanes with the prestations that cross them), loja (a balance, promised against delivered),
rede (one fused sheet against four threaded sheets), fecho (a ladder of the lesson's three tests with their exits).
Every mode returns a wide drawing and a narrow one (same marks, laid out for a phone). Facts: Aula 06 sources only
(Pereira pp. 61-62, Venosa pp. 24-25, STJ REsp 764.901/RJ pp. 7-8, Pereira p. 70, Gomes pp. 121-122; CC arts. 423-425, 476-477, 643).
"""
from . import svg as S

T = S.text


def _arrow(o, x1, x2, y, col=S.INK, w=1.8, dash=None, gap=None):
    """Arrow from x1 to x2 at height y; gap=(a, b) leaves a break in the shaft for a label."""
    s = 1 if x2 > x1 else -1
    tip = x2
    segs = [(x1, x2 - s * 1)] if not gap else [(x1, gap[0]), (gap[1], x2 - s * 1)]
    for a, b in segs:
        o.append(S.line(a, y, b, y, stroke=col, stroke_width=w, stroke_dasharray=dash))
    o.append(S.path(f'M{tip - s * 9},{y - 5} L{tip},{y} L{tip - s * 9},{y + 5}', fill='none', stroke=col, stroke_width=w))


def sinalagma(narrow):
    W = 340 if narrow else 760
    xa, xb = (46, 294) if narrow else (230, 560)
    d = xb - xa
    o = []
    rows = [('compra e venda', 'coisa', 'preço'), ('locação', 'uso', 'aluguel'), ('troca', 'bem', 'bem'),
            ('doação pura', 'transferir', None), ('depósito', 'guardar', 'despesas · art. 643')]
    y = 34
    ys = []
    step = 92 if narrow else 86
    for i, r in enumerate(rows):
        extra = 44 if (narrow and i in (0, 3)) else 0
        y += extra
        ys.append(y)
        y += step if r[2] else step - (14 if narrow else 22)
    H = y + (4 if narrow else 14)
    top, bot = 20, H - 14
    for x in (xa, xb):
        o.append(S.line(x, top, x, bot, stroke=S.INK, stroke_width=1.7))
        o.append(S.circle(x, top, 5, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
        o.append(S.circle(x, bot, 5, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
    for i, (name, a, b) in enumerate(rows):
        y0 = ys[i]
        ny = y0 - 14 if narrow else y0 + 4
        if narrow:
            o.append(T(10, ny, name, size=15, family=S.SERIF))
            ya = y0 + 6
        else:
            o.append(T(24, ny, name, size=16, family=S.SERIF))
            ya = y0
        yb = ya + 26
        # the prestation that always exists: left lane to right lane
        la = xa + d * .30
        o.append(T(la, ya - 8, a, size=14, family=S.SERIF, anchor='middle'))
        _arrow(o, xa + 7, xb - 7, ya)
        if b:
            lb = xb - d * .30
            dashed = i == 4
            col = S.CONC if dashed else S.INK
            o.append(T(lb, yb + 20, b, size=14, family=S.SERIF, anchor='middle', fill=S.CONC if dashed else S.INK))
            _arrow(o, xb - 7, xa + 7, yb, col=col, dash='5 5' if dashed else None)
            if not dashed:
                # the tie that makes one prestation the reason for the other
                o.append(S.line((xa + xb) / 2, ya + 2, (xa + xb) / 2, yb - 2, stroke=S.DIF, stroke_width=2.6))
                o.append(S.circle((xa + xb) / 2, ya, 4, fill=S.PAPER, stroke=S.DIF, stroke_width=2))
                o.append(S.circle((xa + xb) / 2, yb, 4, fill=S.PAPER, stroke=S.DIF, stroke_width=2))
    # the hairline between the two families, and their names
    sep = (ys[2] + ys[3]) / 2 + (30 if narrow else 36) - (30 if narrow else 0) - (0 if narrow else 0)
    sep = ys[3] - (58 if narrow else 24)
    o.append(S.line(10, sep, W - 10, sep, stroke=S.MUTED, stroke_width=1, stroke_dasharray='2 5'))
    if narrow:
        o.append(T(10, ys[0] - 38, 'prestações recíprocas', size=13, family=S.SANS, weight='600'))
        o.append(T(10, sep + 20, 'prestação de um lado só', size=13, family=S.SANS, weight='600'))
    else:
        for y1, y2, t in ((ys[0] - 22, ys[2] + 40, 'prestações recíprocas'), (ys[3] - 22, ys[4] + 56, 'de um lado só')):
            o.append(S.path(f'M{xb + 26},{y1} h8 V{y2} h-8', fill='none', stroke=S.INK, stroke_width=1.3))
            o.append(T(xb + 44, (y1 + y2) / 2 + 5, t, size=15, family=S.SERIF))
    return S.svg(W, H, 'Prestações que cruzam duas partes: ligadas nos bilaterais, de um lado só nos unilaterais', o)


def _shop(o, x, y, w, h, dash=None, col=S.INK, sw=2.2):
    """A shopfront standing on y: walls, a zigzag awning, a door."""
    kw = dict(fill='none', stroke=col, stroke_width=sw, stroke_dasharray=dash)
    o.append(S.path(f'M{x},{y} V{y - h} H{x + w} V{y}', **kw))
    n = 4
    pts = ''.join(f' l{w / n / 2},8 l{w / n / 2},-8' for _ in range(n))
    o.append(S.path(f'M{x},{y - h}{pts}', **dict(kw, stroke_width=1.5)))
    dw = w * .26
    o.append(S.path(f'M{x + w * .5 - dw / 2},{y} v-{h * .45} h{dw} v{h * .45}', **dict(kw, stroke_width=1.5)))


def _balance(o, cx, cy, tilt, label, promised, delivered_anchor, narrow):
    """A balance: price in the left pan, the shop in the right. tilt>0 sinks the price side."""
    L = 105
    dy = tilt
    xl, yl = cx - L, cy + dy
    xr, yr = cx + L, cy - dy
    base = cy + 175
    o.append(S.line(cx, cy, cx, base, stroke=S.INK, stroke_width=2.2))
    o.append(S.line(cx - 34, base, cx + 34, base, stroke=S.INK, stroke_width=2.6))
    o.append(S.line(xl, yl, xr, yr, stroke=S.INK, stroke_width=2.8))
    o.append(S.circle(cx, cy, 6, fill=S.PAPER, stroke=S.INK, stroke_width=2))
    for x, y in ((xl, yl), (xr, yr)):
        o.append(S.circle(x, y, 3.5, fill=S.INK, stroke=S.INK, stroke_width=1))
        rim = y + 100
        o.append(S.path(f'M{x},{y} L{x - 88},{rim} M{x},{y} L{x + 88},{rim}', fill='none', stroke=S.INK, stroke_width=1.1))
        o.append(S.path(f'M{x - 92},{rim} Q{x},{rim + 22} {x + 92},{rim}', fill='none', stroke=S.INK, stroke_width=2.2))
    # price: a stack of coins, the same in both pans
    ry = yl + 100
    for k in range(5):
        o.append(f'<ellipse {S.attrs(cx=xl, cy=ry - 4 - k * 8, rx=26, ry=6.5, fill=S.PAPER, stroke=S.INK, stroke_width=1.6)}/>')
    o.append(T(xl, ry + 44, 'preço', size=15, family=S.SERIF, anchor='middle'))
    # the shop
    ry2 = yr + 100
    if delivered_anchor:
        _shop(o, xr - 66, ry2 - 3, 50, 36)
        _shop(o, xr + 2, ry2 - 3, 62, 50)
        o.append(S.path(f'M{xr - 40},{ry2 - 22} C{xr - 30},{ry2 - 52} {xr + 26},{ry2 - 54} {xr + 40},{ry2 - 24} C{xr + 22},{ry2 - 6} {xr - 28},{ry2 - 6} {xr - 40},{ry2 - 22}',
                         fill='none', stroke=S.CONC, stroke_width=2.2))
        o.append(T(xr - 41, ry2 + 44, 'loja', size=15, family=S.SERIF, anchor='middle'))
        o.append(T(xr + 33, ry2 + 44, 'âncora', size=15, family=S.SERIF, anchor='middle'))
    else:
        _shop(o, xr - 26, ry2 - 3, 52, 40)
        o.append(S.circle(xr, ry2 - 22, 17, fill='none', stroke=S.INK, stroke_width=2))
        o.append(T(xr, ry2 + 44, 'loja', size=15, family=S.SERIF, anchor='middle'))
    o.append(T(cx, base + 36, label, size=17, family=S.SANS, weight='600', anchor='middle'))


def loja(narrow):
    if narrow:
        W, H = 400, 640
        o = []
        _balance(o, 200, 50, 0, 'Exclusividade prometida', True, False, True)
        _balance(o, 200, 370, 22, 'Loja entregue', False, True, True)
    else:
        W, H = 800, 335
        o = []
        _balance(o, 200, 50, 0, 'Exclusividade prometida', True, False, False)
        _balance(o, 600, 50, 22, 'Loja entregue', False, True, False)
        o.append(S.line(400, 20, 400, 310, stroke=S.MUTED, stroke_width=1, stroke_dasharray='2 5'))
    return S.svg(W, H, 'Balança: com o mesmo preço, a loja prometida equilibra e a loja entregue não', o)


def _sheet(o, x, y, w, h, lines=5, sign=True, hole=False, col=S.INK, sw=1.6):
    o.append(S.rect(x, y, w, h, fill=S.PAPER, stroke=col, stroke_width=sw))
    for i in range(lines):
        yy = y + 24 + i * 12
        o.append(S.line(x + 10, yy, x + w - 10, yy, stroke=S.MUTED, stroke_width=1))
    if sign:
        o.append(S.line(x + 12, y + h - 16, x + w * .62, y + h - 16, stroke=S.INK, stroke_width=1.3))
        o.append(S.path(f'M{x + 16},{y + h - 20} q6,-9 12,-1 t12,-1 t12,0', fill='none', stroke=S.DIF, stroke_width=1.5))


def rede(narrow):
    o = []
    names = ['serviços médicos', 'hospitalização', 'medicamentos', 'seguro']
    if narrow:
        W, H = 340, 520
        # fused sheet, centred on top
        fx, fy, fw, fh = 110, 40, 120, 130
        gx = [(24, 270), (192, 270), (24, 398), (192, 398)]
        sw_, sh_ = 124, 96
        title1, title2 = (170, 22), (170, 218)
    else:
        W, H = 760, 306
        fx, fy, fw, fh = 70, 62, 170, 160
        gx = [(300 + i * 112, 62 + (i % 2) * 30) for i in range(4)]
        sw_, sh_ = 100, 160
        title1, title2 = (155, 30), (528, 30)
    # --- one sheet, three kinds of line braided inside it
    o.append(S.rect(fx, fy, fw, fh, fill=S.PAPER, stroke=S.INK, stroke_width=2))
    kinds = (None, '7 4', '2 4')
    n = 5
    for k, dash in enumerate(kinds):
        for j in range(4):
            yy = fy + 22 + j * ((fh - 60) / 3) + k * 6
            amp = 7
            x0, x1 = fx + 10, fx + fw - 10
            xm = (x0 + x1) / 2
            o.append(S.path(f'M{x0},{yy} C{x0 + (x1 - x0) * .25},{yy - amp * (1 if k % 2 else -1)} {xm + (x1 - x0) * .25},{yy + amp * (1 if k % 2 else -1)} {x1},{yy}',
                            fill='none', stroke=S.INK if k == 0 else S.MUTED, stroke_width=1.5 if k == 0 else 1.4, stroke_dasharray=dash))
    o.append(S.line(fx + 14, fy + fh - 15, fx + fw * .6, fy + fh - 15, stroke=S.INK, stroke_width=1.4))
    o.append(S.path(f'M{fx + 18},{fy + fh - 19} q6,-9 12,-1 t12,-1 t12,0', fill='none', stroke=S.DIF, stroke_width=1.5))
    o.append(T(title1[0], title1[1], 'Unidade mista', size=17, family=S.SANS, weight='600', anchor='middle'))
    # --- four separate sheets and the thread through their punch holes
    holes = []
    for i, (x, y) in enumerate(gx):
        _sheet(o, x, y, sw_, sh_, lines=5 if not narrow else 3)
        hx, hy = x + sw_ / 2, y + 12
        holes.append((hx, hy))
    if narrow:
        d = f'M{holes[0][0]},{holes[0][1]} L{holes[1][0]},{holes[1][1]} L{holes[3][0]},{holes[3][1]} L{holes[2][0]},{holes[2][1]}'
    else:
        d = 'M' + ' L'.join(f'{hx},{hy}' for hx, hy in holes)
    o.append(S.path(d, fill='none', stroke=S.DIF, stroke_width=2, stroke_dasharray='1 5', stroke_linecap='round'))
    for hx, hy in holes:
        o.append(S.circle(hx, hy, 5.5, fill=S.PAPER, stroke=S.DIF, stroke_width=2))
    for (x, y), nm in zip(gx, names):
        o.append(T(x + sw_ / 2, (284 if not narrow else y + sh_ + 22) + (0 if narrow else 0), nm, size=14, family=S.SERIF, anchor='middle'))
    o.append(T(title2[0], title2[1], 'Rede coligada', size=17, family=S.SANS, weight='600', anchor='middle'))
    return S.svg(W, H, 'Um contrato que funde elementos, e quatro contratos distintos ligados por uma finalidade comum', o)


def fecho(narrow):
    o = []
    W = 340 if narrow else 760
    tx = 36
    stations = [
        ('reciprocidade', '→ exceção do art. 476 e do art. 477', '→ sem exceção, como na doação pura'),
        ('redação', '→ aderente protegido, arts. 423 e 424', '→ paritário: cláusula livre'),
        ('unidade', '→ unidade mista: um contrato', '→ rede coligada: cada contrato conserva a identidade'),
    ]
    step = 168 if narrow else 118
    y0 = 64
    H = y0 + step * 2 + (112 if narrow else 74)
    o.append(S.line(tx, 14, tx, H - 20, stroke=S.INK, stroke_width=2.2))
    o.append(S.circle(tx, 14, 6, fill=S.PAPER, stroke=S.INK, stroke_width=1.8))
    o.append(S.rect(tx - 7, H - 27, 14, 14, fill=S.INK, stroke=S.INK, stroke_width=1))
    for i, (name, up, down) in enumerate(stations):
        y = y0 + i * step
        o.append(S.rect(tx - 7, y - 7, 14, 14, fill=S.PAPER, stroke=S.INK, stroke_width=2))
        o.append(T(tx + 24, y - 38, name, size=17, family=S.SANS, weight='600'))
        # the exit that applies a rule (blue) and the one that does not (muted)
        if narrow:
            ux, uy, dx_, dy_ = tx + 22, y + 22, tx + 22, y + 66
            o.append(S.path(f'M{tx + 8},{y} H{tx + 18} V{uy - 5} H{tx + 22}', fill='none', stroke=S.DIF, stroke_width=1.6))
            o.append(S.path(f'M{tx + 18},{uy - 5} V{dy_ - 5} H{tx + 22}', fill='none', stroke=S.MUTED, stroke_width=1.3))
            for (tx_, ty_, t, c) in ((ux + 10, uy, up, S.INK), (dx_ + 10, dy_, down, S.MUTED)):
                words = S.wrap(t, 34)
                for k, wl in enumerate(words):
                    o.append(T(tx_, ty_ + k * 17, wl, size=14, family=S.SERIF, fill=c))
        else:
            o.append(S.path(f'M{tx + 8},{y} H{tx + 60}', fill='none', stroke=S.INK, stroke_width=1.6))
            o.append(S.path(f'M{tx + 60},{y} V{y - 22} H{tx + 130}', fill='none', stroke=S.DIF, stroke_width=1.8))
            o.append(S.path(f'M{tx + 60},{y} V{y + 24} H{tx + 130}', fill='none', stroke=S.MUTED, stroke_width=1.3))
            o.append(T(tx + 142, y - 17, up, size=15, family=S.SERIF, fill=S.DIF if False else S.INK))
            o.append(T(tx + 142, y + 29, down, size=15, family=S.SERIF, fill=S.MUTED))
    return S.svg(W, H, 'Três testes em ordem e as regras que cada resposta aciona', o)


def build(p):
    mode = p['mode']
    fn = {'sinalagma': sinalagma, 'loja': loja, 'rede': rede, 'fecho': fecho}[mode]
    return '<div class="drawing-desktop">' + fn(False) + '</div><div class="drawing-mobile">' + fn(True) + '</div>', []
