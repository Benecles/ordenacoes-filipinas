"""Aula 08: three measured or traceable pictures for chapters 3-5 of the cessão lesson.

Params: mode = consentimento | janela | saida. No case quantities are encoded.
consentimento: a time ruler. The cedido's consent (a square) sits before, on or after
  the cedente-cessionário agreement (a dot); the orange hatch is the stretch in which the
  negócio still depends on whoever stays. Sources: Luis Renato pp. 6-7; Orlando Gomes (p. 7).
janela: the life of a contract as cells (satisfied filled, pending hollow) and where the
  position changes hands. Same contract, one fact changed: only a crédito left (cessão de
  crédito) or a remaining dever that obliges to act (cessão da posição). Source: Luis Renato p. 7.
saida: the cedido's way to the person who answers, drawn as a circuit. Liberatória: the
  cedente's link is open; subsidiária: cessionário and cedente in series with a gate
  (excussão); solidária: two branches in parallel. Each row is a focusable thread.
  Source: Luis Renato pp. 9-10.
"""
from . import svg as S


def build(p):
    mode = p.get('mode', 'consentimento')
    label = S.esc(p.get('label', 'Cessão da posição contratual'))
    fn = {'consentimento': _consentimento, 'janela': _janela, 'saida': _saida}.get(mode)
    if fn is None:
        raise ValueError(f'unknown Aula 08 vínculo mode: {mode}')
    desk_w, desk_h, desk = fn(False)
    comp_w, comp_h, comp = fn(True)
    return (f'<svg data-assembly="full" viewBox="0 0 {desk_w} {desk_h}" role="img" aria-label="{label}">' + ''.join(desk) + '</svg>'
            + f'<svg data-assembly="compact" viewBox="0 0 {comp_w} {comp_h}" role="img" aria-label="{label}">' + ''.join(comp) + '</svg>'), []


class _Pen:
    def __init__(self, out, small):
        self.out, self.small = out, small

    def line(self, x, y, xx, yy, color=S.INK, width=1.5, **kw):
        self.out.append(S.line(x, y, xx, yy, stroke=color, stroke_width=width, **kw))

    def path(self, d, color=S.INK, width=1.5, **kw):
        self.out.append(S.path(d, fill='none', stroke=color, stroke_width=width, **kw))

    def dot(self, x, y, r=5, color=S.INK):
        self.out.append(S.circle(x, y, r, fill=S.PAPER, stroke=color, stroke_width=1.6))

    def sq(self, x, y, r=9, color=S.INK, width=1.8):
        self.out.append(S.rect(x - r, y - r, 2 * r, 2 * r, fill=S.PAPER, stroke=color, stroke_width=width))

    def text(self, x, y, s, size=None, **kw):
        size = size or (12 if self.small else 14)
        self.out.append(S.text(x, y, s, size=size, **kw))


def _consentimento(small):
    out = []
    P = _Pen(out, small)
    if not small:
        w, h = 900, 330
        xb, xc, xp, x1 = 290, 560, 760, 860
        ys = (100, 192, 284)
        P.line(xb - 30, 46, x1, 46, S.MUTED, 1)
        P.text(xb, 26, 'contrato-base', anchor='middle')
        P.text(xc, 26, 'ajuste da cessão', anchor='middle')
        for x in (xb, xc):
            P.dot(x, 46, 5)
            P.line(x, 56, x, 310, S.GRID, 1, stroke_dasharray='2 5')
        for y, name in zip(ys, ('prévio', 'simultâneo', 'posterior')):
            P.text(22, y + 6, name, size=19, family=S.SANS)
            P.line(xb, y, x1, y, S.MUTED, 1)
        y = ys[0]
        P.path(f'M{xb} {y-7} H{xc} V{y+7} H{xb} Z', S.INK2, 1.3)
        P.sq(xb, y)
        P.dot(xc, y, 5)
        P.text(xb + 18, y - 22, 'anuência do cedido', anchor='start')
        P.text((xb + xc) / 2, y + 34, 'cláusula do contrato-base', anchor='middle', fill=S.INK2)
        y = ys[1]
        P.sq(xc, y, 12)
        P.dot(xc, y, 5)
        P.text(xc, y + 40, 'interveniente-anuente', anchor='middle', fill=S.INK2)
        y = ys[2]
        for hl in S.hatch(xc, y - 9, xp - xc, 18, step=8, stroke=S.CONC, stroke_width=1.2):
            out.append(hl)
        P.path(f'M{xc} {y-9} H{xp} V{y+9} H{xc} Z', S.CONC, 1.4)
        P.dot(xc, y, 5)
        P.sq(xp, y)
        P.text((xc + xp) / 2, y + 36, 'ainda depende de quem permanece', anchor='middle', fill=S.CONC)
        return w, h, out
    w, h = 340, 520
    xb, xc, xp = 52, 170, 290
    ys = (108, 252, 396)
    P.line(xb - 30, 46, 320, 46, S.MUTED, 1)
    P.text(xb, 26, 'contrato-base', anchor='middle')
    P.text(xc + 10, 26, 'ajuste da cessão', anchor='middle')
    for x in (xb, xc):
        P.dot(x, 46, 5)
        P.line(x, 56, x, 500, S.GRID, 1, stroke_dasharray='2 5')
    titles = (('prévio', 'cláusula do contrato-base'), ('simultâneo', 'interveniente-anuente'), ('posterior', 'ainda depende de quem permanece'))
    for y, (a, b) in zip(ys, titles):
        P.text(10, y - 30, a, size=16, family=S.SANS)
        P.line(xb, y, 322, y, S.MUTED, 1)
    y = ys[0]
    P.path(f'M{xb} {y-7} H{xc} V{y+7} H{xb} Z', S.INK2, 1.3)
    P.sq(xb, y)
    P.dot(xc, y, 5)
    P.text(xb + 16, y + 32, 'anuência do cedido', anchor='start')
    y = ys[1]
    P.sq(xc, y, 12)
    P.dot(xc, y, 5)
    P.text(xc + 22, y + 36, 'no instrumento', anchor='start')
    y = ys[2]
    for hl in S.hatch(xc, y - 9, xp - xc, 18, step=8, stroke=S.CONC, stroke_width=1.2):
        out.append(hl)
    P.path(f'M{xc} {y-9} H{xp} V{y+9} H{xc} Z', S.CONC, 1.4)
    P.dot(xc, y, 5)
    P.sq(xp, y)
    P.text(xc, y + 38, 'ainda depende de', anchor='start', fill=S.CONC)
    P.text(xc, y + 56, 'quem permanece', anchor='start', fill=S.CONC)
    return w, h, out


def _cells(P, x0, n, cw, gap, y, filled, tail=None):
    """n cells; the first `filled` are satisfied (solid ink), the rest hollow. tail = colour of the last hollow cell."""
    for i in range(n):
        x = x0 + i * (cw + gap)
        if i < filled:
            P.out.append(S.rect(x, y - 10, cw, 20, fill=S.INK2, stroke=S.INK2, stroke_width=1))
        else:
            col = tail if (tail and i == n - 1) else S.INK
            P.out.append(S.rect(x, y - 10, cw, 20, fill=S.PAPER, stroke=col, stroke_width=1.8))


def _marker(P, x, y, color, text, anchor='middle'):
    P.line(x, y - 26, x, y + 18, color, 2.2)
    P.dot(x, y - 26, 6, color)
    P.text(x, y - 40, text, anchor=anchor, fill=color if color != S.INK else S.INK)


def _janela(small):
    out = []
    P = _Pen(out, small)
    rows = ('execução diferida', 'relação duradoura', 'só crédito restante', 'dever remanescente')
    if not small:
        w, h = 900, 490
        x0, cw, gap, n = 250, 52, 6, 8
        ys = (84, 200, 316, 432)
        end = x0 + n * (cw + gap) - gap
        for y, name in zip(ys, rows):
            P.text(22, y + 6, name, size=19, family=S.SANS)
        # A: formation and performance, with the interval between them.
        y = ys[0]
        P.path(f'M{x0} {y-10} H{end} V{y+10} H{x0} Z', S.INK, 1.8)
        P.dot(x0, y, 7)
        P.dot(end, y, 7)
        P.text(x0, y + 38, 'formação', anchor='middle')
        P.text(end, y + 38, 'cumprimento', anchor='middle')
        _marker(P, 500, y, S.INK, 'cessão da posição')
        # B: lasting relation, some parcels satisfied and others pending.
        y = ys[1]
        _cells(P, x0, n, cw, gap, y, 5)
        xm = x0 + 5 * (cw + gap) - gap / 2
        _marker(P, xm, y, S.INK, 'cessão da posição')
        P.text(x0 + (5 * (cw + gap) - gap) / 2, y + 38, 'satisfeitas', anchor='middle')
        P.text(xm + gap / 2 + (3 * (cw + gap) - gap) / 2, y + 38, 'pendentes', anchor='middle')
        # C and D: the same contract, principal performance done; one fact changes what remains.
        xl = x0 + 7 * (cw + gap) + cw / 2
        y = ys[2]
        _cells(P, x0, n, cw, gap, y, 7, S.CONC)
        _marker(P, xl, y, S.CONC, 'cessão de crédito')
        P.text(x0 + (7 * (cw + gap) - gap) / 2, y + 38, 'prestações cumpridas', anchor='middle')
        P.text(xl, y + 38, 'crédito', anchor='middle', fill=S.CONC)
        y = ys[3]
        _cells(P, x0, n, cw, gap, y, 7, S.DIF)
        _marker(P, xl, y, S.DIF, 'cessão da posição')
        P.text(x0 + (7 * (cw + gap) - gap) / 2, y + 38, 'prestações cumpridas', anchor='middle')
        P.text(xl, y + 38, 'dever de agir', anchor='middle', fill=S.DIF)
        return w, h, out
    w, h = 340, 640
    x0, cw, gap, n = 36, 30, 4, 8
    ys = (84, 236, 388, 540)
    end = x0 + n * (cw + gap) - gap
    xl = x0 + 7 * (cw + gap) + cw / 2
    for y, name in zip(ys, rows):
        P.text(10, y - 56, name, size=16, family=S.SANS)
    y = ys[0]
    P.path(f'M{x0} {y-10} H{end} V{y+10} H{x0} Z', S.INK, 1.8)
    P.dot(x0, y, 6)
    P.dot(end, y, 6)
    P.text(x0, y + 36, 'formação', anchor='start')
    P.text(end, y + 36, 'cumprimento', anchor='end')
    _marker(P, 170, y, S.INK, 'cessão da posição')
    y = ys[1]
    _cells(P, x0, n, cw, gap, y, 5)
    xm = x0 + 5 * (cw + gap) - gap / 2
    _marker(P, xm, y, S.INK, 'cessão da posição')
    P.text(x0, y + 36, 'satisfeitas', anchor='start')
    P.text(end, y + 36, 'pendentes', anchor='end')
    y = ys[2]
    _cells(P, x0, n, cw, gap, y, 7, S.CONC)
    _marker(P, xl, y, S.CONC, 'cessão de crédito', anchor='end')
    P.text(x0, y + 36, 'prestações cumpridas', anchor='start')
    P.text(end, y + 36, 'crédito', anchor='end', fill=S.CONC)
    y = ys[3]
    _cells(P, x0, n, cw, gap, y, 7, S.DIF)
    _marker(P, xl, y, S.DIF, 'cessão da posição', anchor='end')
    P.text(x0, y + 36, 'prestações cumpridas', anchor='start')
    P.text(end, y + 36, 'dever de agir', anchor='end', fill=S.DIF)
    return w, h, out


_SAIDA = (
    ('liberatória', 'cedente sem responsabilidade',
     'Na cessão liberatória, o cedente se afasta da relação e não mantém responsabilidade ou dever para com o cedido; a relação passa a ser atuada pelo cessionário.'),
    ('subsidiária', 'excussão do cessionário primeiro',
     'Sem liberar o cedente, Luis Renato fica com a responsabilidade subsidiária: o patrimônio do cessionário é buscado primeiro e só depois responde o cedente.'),
    ('solidária', 'afastada por Luis Renato',
     'Na solidariedade o cedido poderia se dirigir a qualquer um dos dois; Luis Renato afasta essa via para o cedente que permanece vinculado.'),
)


def _saida(small):
    out = []
    P = _Pen(out, small)
    if not small:
        w, h = 900, 340
        xd, xs, xe = 300, 560, 820
        ys = (110, 210, 310)
        for x, name in ((xd, 'cedido'), (xs, 'cessionário'), (xe, 'cedente')):
            P.text(x, 30, name, anchor='middle')
            P.line(x, 44, x, 330, S.GRID, 1, stroke_dasharray='2 5')
        for (name, sub, sentence), y in zip(_SAIDA, ys):
            out.append(f'<g data-thread="{name}" data-out="{S.esc(sentence)}" tabindex="0" role="button" aria-label="Traçar a via {name}">')
            out.append(S.rect(10, y - 40, 880, 80, fill='none', stroke='none', pointer_events='all'))
            P.text(22, y - 2, name, size=19, family=S.SANS)
            P.text(22, y + 22, sub, size=13, fill=S.INK2)
            if name == 'liberatória':
                P.line(xd + 8, y, xs - 7, y)
                P.dot(xd, y, 8)
                P.dot(xs, y, 6)
                P.out.append(S.circle(xe, y, 6, fill=S.PAPER, stroke=S.MUTED, stroke_width=1.4, stroke_dasharray='3 3'))
            elif name == 'subsidiária':
                P.line(xd + 8, y, xs - 7, y)
                P.line(xs + 6, y, xe - 6, y)
                P.dot(xd, y, 8)
                P.dot(xs, y, 6)
                P.dot(xe, y, 6)
                P.sq(690, y, 9)
                P.text(690, y - 22, 'excussão', anchor='middle', size=13)
            else:
                P.path(f'M{xd+8} {y} H360 V{y-14} H{xs-7}', S.MUTED, 1.4)
                P.path(f'M360 {y} V{y+14} H{xe-6}', S.MUTED, 1.4)
                P.dot(xd, y, 8, S.MUTED)
                P.dot(xs, y - 14, 6, S.MUTED)
                P.dot(xe, y + 14, 6, S.MUTED)
            out.append('</g>')
        return w, h, out
    w, h = 340, 420
    xd, xs, xe = 46, 176, 296
    ys = (118, 238, 358)
    for x, name in ((xd, 'cedido'), (xs, 'cessionário'), (xe, 'cedente')):
        P.text(x, 26, name, anchor='middle')
        P.line(x, 38, x, 408, S.GRID, 1, stroke_dasharray='2 5')
    for (name, sub, sentence), y in zip(_SAIDA, ys):
        out.append(f'<g data-thread="{name}" data-out="{S.esc(sentence)}" tabindex="0" role="button" aria-label="Traçar a via {name}">')
        out.append(S.rect(0, y - 54, 340, 112, fill='none', stroke='none', pointer_events='all'))
        P.text(10, y - 36, name, size=16, family=S.SANS)
        P.text(10, y - 18, sub, size=12, fill=S.INK2)
        if name == 'liberatória':
            P.line(xd + 8, y + 6, xs - 7, y + 6)
            P.dot(xd, y + 6, 8)
            P.dot(xs, y + 6, 6)
            P.out.append(S.circle(xe, y + 6, 6, fill=S.PAPER, stroke=S.MUTED, stroke_width=1.4, stroke_dasharray='3 3'))
        elif name == 'subsidiária':
            P.line(xd + 8, y + 6, xs - 7, y + 6)
            P.line(xs + 6, y + 6, xe - 6, y + 6)
            P.dot(xd, y + 6, 8)
            P.dot(xs, y + 6, 6)
            P.dot(xe, y + 6, 6)
            P.sq(236, y + 6, 8)
            P.text(236, y + 34, 'excussão', anchor='middle')
        else:
            P.path(f'M{xd+8} {y+6} H100 V{y-6} H{xs-7}', S.MUTED, 1.4)
            P.path(f'M100 {y+6} V{y+20} H{xe-6}', S.MUTED, 1.4)
            P.dot(xd, y + 6, 8, S.MUTED)
            P.dot(xs, y - 6, 6, S.MUTED)
            P.dot(xe, y + 20, 6, S.MUTED)
        out.append('</g>')
    return w, h, out
