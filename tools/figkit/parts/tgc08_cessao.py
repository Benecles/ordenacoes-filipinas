"""tgc08_cessao: Aula 08 drawings of Teoria Geral dos Contratos (cessão da posição contratual).

params: mode = tempo | vias | reserva | alcance | consentimento. No dates, amounts or case facts are added;
positions carry relative order only. `reserva` is an abstract stipulation: the checkbox beside the sheet toggles
[data-reserva] (the reserved path) and [data-sem-reserva] (the severed one).
Sources: Luis Renato Ferreira da Silva, pp. 398-408; Venosa pp. 46-47; Orlando Gomes pp. 177-180.
"""
from . import svg as S


def build(p):
    mode = p.get('mode', 'tempo')
    o = []

    def t(x, y, s, **kw):
        kw.setdefault('size', 14)
        o.append(S.text(x, y, s, **kw))

    def line(x, y, x2, y2, **kw):
        o.append(S.line(x, y, x2, y2, stroke=kw.pop('stroke', S.INK), **kw))

    def dot(x, y, col=S.INK, r=5):
        o.append(S.circle(x, y, r, fill=S.PAPER, stroke=col, stroke_width=2))

    def tie(x, y0, y1):
        line(x, y0, x, y1, stroke=S.MUTED, stroke_dasharray='3 4')

    if mode == 'tempo':
        w, h = 900, 290
        a, b, c = 230, 570, 850
        t(a, 26, 'celebração', fill=S.MUTED)
        t(b, 26, 'substituição', fill=S.MUTED, anchor='middle')
        for x in (a, b):
            line(x, 40, x, 262, stroke=S.GRID)
        # lane 1: cessão, the new holder counts from the substitution
        y = 105
        t(20, y + 5, 'Cessão', family=S.SANS, size=17, weight='600')
        line(a, y, b, y, stroke_width=5)
        line(b, y, c, y, stroke=S.DIF, stroke_width=5)
        dot(a, y); dot(b, y, S.DIF); dot(c, y, S.DIF)
        t(a, y + 30, 'cedente')
        t(b + 14, y + 30, 'cessionário · ex nunc', fill=S.DIF)
        # lane 2: pessoa a declarar, the nominee counts from the celebration
        y = 215
        t(20, y + 5, 'Pessoa a declarar', family=S.SANS, size=17, weight='600')
        line(a, y, c, y, stroke=S.DIF, stroke_width=5)
        dot(a, y, S.DIF); dot(b, y); dot(c, y, S.DIF)
        o.append(S.path(f'M{b},{y - 14} Q{(a + b) / 2},{y - 62} {a},{y - 14}', fill='none', stroke=S.DIF, stroke_width=1.8))
        o.append(S.path(f'M{a + 11},{y - 20} L{a},{y - 13} L{a + 13},{y - 9}', fill='none', stroke=S.DIF, stroke_width=1.8))
        t(a, y + 30, 'nomeado · desde a celebração', fill=S.DIF)
        t(b + 14, y + 30, 'nomeação · ex tunc')
    elif mode == 'vias':
        w, h = 900, 400
        x0, cut, x1 = 230, 540, 840
        # cessão: one relation whose holder changes
        t(20, 46, 'Cessão', family=S.SANS, size=17, weight='600')
        line(x0, 40, x1, 40, stroke_width=3)
        t(x0, 24, 'cedido')
        line(x0, 120, cut, 120, stroke_width=3)
        line(cut, 120, x1, 120, stroke=S.DIF, stroke_width=3)
        o.append(S.path(f'M{cut},120 C{cut + 30},120 {cut + 10},150 {cut + 40},150', fill='none', stroke=S.MUTED, stroke_width=1.5))
        dot(cut, 120, S.DIF)
        tie(x0 + 60, 44, 116); tie(x1 - 60, 44, 116)
        t(x0, 148, 'cedente')
        t(cut + 52, 154, 'cessionário', fill=S.DIF)
        line(20, 196, 880, 196, stroke=S.GRID)
        # subcontrato: two relations, the common party in both
        t(20, 256, 'Subcontrato', family=S.SANS, size=17, weight='600')
        line(x0, 230, x1, 230, stroke_width=3)
        t(x0, 214, 'cedido')
        line(x0, 300, x1, 300, stroke_width=3)
        t(x0, 330, 'contratante comum')
        line(cut, 360, x1, 360, stroke=S.DIF, stroke_width=3)
        dot(cut, 360, S.DIF)
        t(cut + 14, 388, 'subcontratado', fill=S.DIF)
        tie(x0 + 60, 234, 296); tie(x1 - 60, 234, 296)
        tie(cut + 70, 304, 356); tie(x1 - 60, 304, 356)
    elif mode == 'reserva':
        w, h = 780, 185
        xe, xc, xd = 100, 360, 680
        y = 120
        # the cessionário now answers to the cedido
        line(xc, y, xd, y, stroke=S.DIF, stroke_width=4)
        o.append(S.rect(xe - 9, y - 9, 18, 18, fill=S.INK, stroke=S.INK))
        dot(xc, y, S.DIF, 7); dot(xd, y, S.INK, 7)
        t(xe, y + 38, 'cedente', anchor='middle')
        t(xc, y + 38, 'cessionário', anchor='middle', fill=S.DIF)
        t(xd, y + 38, 'cedido', anchor='middle')
        line(xe + 11, y, xc - 9, y, stroke=S.MUTED, stroke_width=1.5, stroke_dasharray='2 5')
        # unsigned: the old tie is cut
        o.append('<g data-sem-reserva>')
        o.append(S.path(f'M{xe},{y - 14} C{xe + 40},{y - 90} {xc - 60},{y - 90} {xc - 20},{y - 90}', fill='none', stroke=S.MUTED, stroke_width=1.4, stroke_dasharray='3 4'))
        line(xc - 12, y - 102, xc - 12, y - 78, stroke=S.INK, stroke_width=3)
        t(xe + 50, y - 100, 'sem reserva: liberado', fill=S.MUTED)
        o.append('</g>')
        # signed: the tie survives, behind the cessionário
        o.append('<g data-reserva hidden>')
        o.append(S.path(f'M{xe},{y - 14} C{xe + 60},{y - 100} {xd - 60},{y - 100} {xd},{y - 14}', fill='none', stroke=S.CONC, stroke_width=2.4, stroke_dasharray='6 5'))
        t((xe + xd) / 2, y - 100, 'reserva: responde se o cessionário não cumprir', anchor='middle', fill=S.CONC)
        o.append('</g>')
    elif mode == 'alcance':
        w, h = 900, 270
        a, b, c, d = 40, 360, 560, 850
        for x, label, an in [(c, 'cessão', 'middle'), (d, 'discussão judicial', 'end')]:
            t(x, 26, label, fill=S.MUTED, anchor=an)
            line(x, 40, x, 240, stroke=S.GRID)
        t(a, 26, 'pagamentos anteriores', fill=S.MUTED)
        # lane 1: instalments already paid (extinct)
        y = 100
        for hh in S.hatch(a, y - 10, b - a, 20, step=8, stroke=S.MUTED, stroke_width=1):
            o.append(hh)
        line(a, y, b, y, stroke_width=5)
        line(b, y - 14, b, y + 14, stroke_width=3)
        t(a, y + 36, 'prestações quitadas: extintas')
        # lane 2: the credit that arises from them travels with the position
        y = 195
        line(a, y, d, y, stroke=S.DIF, stroke_width=5)
        dot(c, y, S.DIF, 6); dot(d, y, S.DIF, 6)
        t(a, y + 36, 'créditos incluídos na cessão', fill=S.DIF)
        t(c + 14, y - 16, 'novo titular', fill=S.DIF)
    elif mode == 'consentimento':
        w, h = 900, 270
        x0, act, x1 = 40, 450, 860
        y = 150
        line(x0, y, x1, y, stroke_width=3)
        o.append(S.rect(act - 11, y - 11, 22, 22, fill=S.INK, stroke=S.INK))
        t(act, y + 78, 'cedente e cessionário ajustam a substituição', anchor='middle', fill=S.INK2)
        t(x0, 28, 'consentimento do cedido', fill=S.DIF, weight='600')
        marks = [(185, 'antes', ['autorização', 'no contrato-base']),
                 (act, 'junto', ['interveniente-anuente']),
                 (730, 'depois', ['adesão por conduta', 'que revela concordância'])]
        for x, lab, notes in marks:
            line(x, y - 72, x, y - 11 if x == act else y, stroke=S.DIF, stroke_width=2)
            if x != act:
                dot(x, y, S.DIF, 6)
            o.append(S.path(f'M{x},{y - 72} L{x + 32},{y - 63} L{x},{y - 53} Z', fill=S.DIF, stroke=S.DIF))
            t(x, y - 84, lab, fill=S.DIF, weight='600', anchor='middle')
            for k, n in enumerate(notes):
                t(x, y + (34 if x != act else 40) + k * 20 if x != act else y + 40, n, size=14, fill=S.INK2, anchor='middle')
    else:
        raise ValueError('mode must be tempo, vias, reserva, alcance or consentimento')
    titles = {'tempo': 'Início dos efeitos na cessão e na nomeação', 'vias': 'Uma relação continuada ou duas relações dependentes',
              'reserva': 'Reserva expressa de responsabilidade subsidiária', 'alcance': 'Pagamento extinto e crédito transmitido no REsp 356.383/SP',
              'consentimento': 'Consentimento do cedido: antes, junto ou depois do ajuste entre cedente e cessionário'}
    return S.svg(w, h, titles[mode], o), []
