"""Tânia's distrato on two scales: the 60-month term and the money (REsp 1.040.606).

Measured picture. Time: 60 equal cells from 5 Sep 2000, the agreement placed after 22 whole months (July 2002).
Money: R$ 61.560,00 the whole contract, R$ 41.521,30 paid, R$ 28.938,36 to be returned in six monthly
instalments (the second agreement). Bar lengths are proportional to the sums. Params: narrow (bool).
"""
from . import svg as S

TOTAL, PAID, BACK = 61560.00, 41521.30, 28938.36


def brl(v):
    s = f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return 'R$ ' + s


def build(p):
    narrow = p.get('narrow', False)
    W = 360 if narrow else 700
    x0, wb = 18, W - 36
    out = []
    # time strip
    ty, th = 58, 28
    out.append(S.text(x0, 30, 'Prazo de 60 meses, a contar de 5 de setembro de 2000', size=15, family=S.SERIF))
    cw = wb / 60
    out.append(S.rect(x0 + 22 * cw, ty, wb - 22 * cw, th, fill='none', stroke=S.MUTED, stroke_width=1.5, stroke_dasharray='3 4'))
    out.append(S.rect(x0, ty, 22 * cw, th, fill=S.PAPER2, stroke=S.INK, stroke_width=1.5))
    out += S.hatch(x0 + 1, ty + 1, 22 * cw - 2, th - 2, step=9, stroke=S.GRID, stroke_width=1)
    ticks = ' '.join(f'M{x0 + i * cw:.1f},{ty + th - 7:g} V{ty + th:g}' for i in range(1, 60))
    out.append(S.path(ticks, fill='none', stroke=S.INK, stroke_width=1))
    mx = x0 + 22 * cw
    out.append(S.line(mx, ty - 12, mx, ty + th + 12, stroke=S.DIF, stroke_width=3))
    out.append(S.text(mx + 8, ty + th + 26, 'julho de 2002', size=15, family=S.SANS, weight='600'))
    out.append(S.text(mx + 8, ty + th + 44, 'acordo de rescisão', size=14, family=S.SERIF))
    out.append(S.text(x0, ty + th + 26, '1º mês', size=14, family=S.SERIF, fill=S.MUTED))
    out.append(S.text(W - x0, ty + th + 26, '60º mês', size=14, family=S.SERIF, fill=S.MUTED, anchor='end'))
    # money bar
    by, bh = 196 if not narrow else 206, 32
    out.append(S.text(x0, by - 28, 'Valores em reais', size=15, family=S.SERIF))
    out.append(S.rect(x0, by, wb, bh, fill='none', stroke=S.MUTED, stroke_width=1.5, stroke_dasharray='3 4'))
    xp = x0 + wb * PAID / TOTAL
    xb = x0 + wb * BACK / TOTAL
    out.append(S.rect(x0, by, xp - x0, bh, fill=S.PAPER2, stroke=S.INK, stroke_width=1.5))
    out.append(S.rect(x0, by, xb - x0, bh, fill=S.DIF, stroke=S.INK, stroke_width=1.5))
    out.append(S.line(xb, by + bh, xb, by + bh + 14, stroke=S.INK, stroke_width=1.2))
    out.append(S.line(xp, by + bh, xp, by + bh + 40, stroke=S.INK, stroke_width=1.2))
    out.append(S.line(W - x0, by + bh, W - x0, by + bh + 66, stroke=S.INK, stroke_width=1.2))
    if narrow:
        out.append(S.text(x0, by + bh + 28, brl(BACK) + ' a devolver', size=14, family=S.SERIF))
        out.append(S.text(x0, by + bh + 46, 'em seis parcelas mensais', size=14, family=S.SERIF))
        out.append(S.text(xp - 6, by + bh + 74, 'pago ' + brl(PAID), size=14, family=S.SERIF, anchor='end'))
        out.append(S.text(W - x0, by + bh + 96, 'valor total ' + brl(TOTAL), size=14, family=S.SERIF, anchor='end'))
        H = by + bh + 110
    else:
        out.append(S.text(xb - 8, by + bh + 28, brl(BACK) + ' a devolver em seis parcelas mensais', size=14, family=S.SERIF, anchor='end'))
        out.append(S.text(xp - 6, by + bh + 50, 'pago ' + brl(PAID), size=14, family=S.SERIF, anchor='end'))
        out.append(S.text(W - x0 - 6, by + bh + 76, 'valor total ' + brl(TOTAL), size=14, family=S.SERIF, anchor='end'))
        H = by + bh + 92
    return S.svg(W, H, "O distrato de Tânia: o prazo de sessenta meses e os valores pago e a devolver", out), []
