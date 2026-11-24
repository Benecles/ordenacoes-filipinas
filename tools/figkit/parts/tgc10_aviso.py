"""The notice in REsp 1.112.796: 3 Jun 1998 to 25 Jan 1999, against the 60 days of clause 13.

Measured picture; one calendar scale, day by day (1 Jun 1998 to 31 Jan 1999), computed by script.
Sources: REsp 1.112.796/PR, relatório (notification 03.06.98, cessation 25.01.99) and cláusula 13ª (60 days).
Params: narrow (bool).
"""
from datetime import date, timedelta

from . import svg as S

MONTHS = ['jun.', 'jul.', 'ago.', 'set.', 'out.', 'nov.', 'dez.', 'jan.']


def build(p):
    narrow = p.get('narrow', False)
    W = 360 if narrow else 700
    x0, wb = 18, W - 36
    d0, d1 = date(1998, 6, 1), date(1999, 1, 31)
    span = (d1 - d0).days + 1
    X = lambda d: x0 + wb * (d - d0).days / span
    notif, cess = date(1998, 6, 3), date(1999, 1, 25)
    mini = cess - timedelta(days=60)
    aviso = (cess - notif).days
    ay, ah = 108, 34
    out = []
    starts = [date(1998, 6, 1), date(1998, 7, 1), date(1998, 8, 1), date(1998, 9, 1), date(1998, 10, 1),
              date(1998, 11, 1), date(1998, 12, 1), date(1999, 1, 1), date(1999, 2, 1)]
    for i in range(8):
        a, b = X(starts[i]), (X(starts[i + 1]) if i < 7 else x0 + wb)
        out.append(S.rect(a, ay, b - a, ah, fill=S.PAPER2 if i % 2 == 0 else 'none', stroke=S.INK, stroke_width=1.2))
        out.append(S.text((a + b) / 2, ay + ah + 20, MONTHS[i], size=14, family=S.SERIF, anchor='middle'))
    out.append(S.text(x0, ay + ah + 40, '1998', size=14, family=S.SERIF, fill=S.MUTED))
    out.append(S.text(X(starts[7]), ay + ah + 40, '1999', size=14, family=S.SERIF, fill=S.MUTED))
    # the two events
    xn, xc = X(notif), X(cess)
    out.append(S.line(xn, 58, xn, ay + ah, stroke=S.INK, stroke_width=2.5))
    out.append(S.line(xc, 58, xc, ay + ah, stroke=S.INK, stroke_width=2.5))
    out.append(S.text(xn - 2, 18, 'notificação', size=14, family=S.SANS, weight='600'))
    out.append(S.text(xn - 2, 36, '3 de junho' if narrow else '3 de junho de 1998', size=14, family=S.SERIF))
    out.append(S.text(xc + 2, 18, 'cessa a vigência', size=14, family=S.SANS, weight='600', anchor='end'))
    out.append(S.text(xc + 2, 36, '25 de janeiro' if narrow else '25 de janeiro de 1999', size=14, family=S.SERIF, anchor='end'))
    # the notice given
    by = 80
    out.append(S.line(xn, by, xc, by, stroke=S.INK, stroke_width=2))
    out.append(S.line(xn, by - 7, xn, by + 7, stroke=S.INK, stroke_width=2))
    out.append(S.line(xc, by - 7, xc, by + 7, stroke=S.INK, stroke_width=2))
    out.append(S.text((xn + xc) / 2, by - 10, f'{aviso} dias de aviso', size=16, family=S.SANS, weight='600', anchor='middle'))
    # the minimum of the contract
    my = ay + ah + 74
    xm = X(mini)
    out.append(S.line(xm, my, xc, my, stroke=S.CONC, stroke_width=3))
    out.append(S.line(xm, my - 7, xm, my + 7, stroke=S.CONC, stroke_width=3))
    out.append(S.line(xc, my - 7, xc, my + 7, stroke=S.CONC, stroke_width=3))
    if narrow:
        out.append(S.text(xc, my + 26, '60 dias, mínimo', size=14, family=S.SERIF, fill=S.CONC, anchor='end'))
        out.append(S.text(xc, my + 44, 'da cláusula 13ª', size=14, family=S.SERIF, fill=S.CONC, anchor='end'))
        H = my + 58
    else:
        out.append(S.text(xm - 10, my + 5, '60 dias, mínimo da cláusula 13ª', size=15, family=S.SERIF, fill=S.CONC, anchor='end'))
        H = my + 26
    return S.svg(W, H, 'O aviso de 236 dias dado pela Antarctica, contra os 60 dias mínimos da cláusula 13ª', out), []
