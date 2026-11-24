"""Aula 06, chapter 5: how a contract relates to the legal model and to other contracts.

Five small constructions side by side (stacked on phones). A contract is an outline;
a filled square is a piece that comes from the legal type, a hollow square is a
piece the parties made up. Típico: every piece is the law's; atípico: every piece is the
parties' (art. 425), with the nearest type lending principles by analogy (dashed);
misto: one grafted piece inside a typical frame; coligados: two outlines that stay
separate, tied by a thread of dependence; derivado: a shorter outline hanging inside the
extent of the base. Facts: Pereira pp.56-57 (típico, atípico, misto; contratos sob
medida; contrato típico mais próximo), p.70 (coligados: conexão funcional, um só tem
executividade se o outro tiver; não se confundem com mistos); Venosa pp.46-47 (derivado:
limite no contrato-base, nemo plus iuris). Params: none. Geometry is schematic.
"""
from . import svg as S

PW, PH = 200, 250


def _piece(o, x, y, s=20, own=False):
    if own:
        o.append(S.rect(x, y, s, s, fill=S.PAPER, stroke=S.INK, stroke_width=2))
    else:
        o.append(S.rect(x, y, s, s, fill=S.INK, stroke=S.INK, stroke_width=1))


def _frame(o, x, y, w, h, dash=None):
    kw = dict(fill='none', stroke=S.INK, stroke_width=2.2)
    if dash:
        kw = dict(fill='none', stroke=S.MUTED, stroke_width=1.4, stroke_dasharray=dash)
    o.append(S.rect(x, y, w, h, **kw))


def _panel(ox, oy, kind):
    o = []
    T = S.text
    titles = {'tipico': 'Típico', 'atipico': 'Atípico', 'misto': 'Misto', 'coligados': 'Coligados', 'derivado': 'Derivado'}
    caps = {'tipico': 'todas as peças vêm da lei', 'atipico': 'peças feitas pelas partes',
            'misto': 'peças da lei e das partes', 'coligados': 'dois contratos, um fim',
            'derivado': 'preso ao limite da base'}
    o.append(T(ox + 14, oy + 26, titles[kind], size=16, family=S.SANS, weight='600'))
    if kind == 'tipico':
        _frame(o, ox + 20, oy + 84, 160, 64)
        for i in range(4):
            _piece(o, ox + 34 + i * 34, oy + 106)
    elif kind == 'atipico':
        _frame(o, ox + 20, oy + 70, 160, 56)
        for i in range(4):
            _piece(o, ox + 34 + i * 34, oy + 87, own=True)
        o.append(S.path(f'M{ox+100},{oy+128} V{oy+150}', fill='none', stroke=S.MUTED, stroke_width=1.3, stroke_dasharray='4 4'))
        _frame(o, ox + 52, oy + 150, 96, 40, dash='5 4')
        _piece(o, ox + 66, oy + 160, 16)
        _piece(o, ox + 118, oy + 160, 16)
    elif kind == 'misto':
        _frame(o, ox + 20, oy + 84, 160, 64)
        for i in range(3):
            _piece(o, ox + 34 + i * 34, oy + 106)
        _piece(o, ox + 136, oy + 106, own=True)
    elif kind == 'coligados':
        _frame(o, ox + 12, oy + 84, 74, 64)
        _frame(o, ox + 114, oy + 84, 74, 64)
        for x in (ox + 26, ox + 56, ox + 128, ox + 158):
            _piece(o, x, oy + 106, 18)
        o.append(S.line(ox + 86, oy + 116, ox + 114, oy + 116, stroke=S.INK, stroke_width=2.4))
        o.append(S.circle(ox + 86, oy + 116, 4, fill=S.INK, stroke=S.INK))
        o.append(S.circle(ox + 114, oy + 116, 4, fill=S.INK, stroke=S.INK))
    else:
        _frame(o, ox + 20, oy + 70, 160, 44)
        for x in (34, 68, 102, 136):
            _piece(o, ox + x, oy + 82, 20)
        _frame(o, ox + 90, oy + 150, 90, 44)
        _piece(o, ox + 104, oy + 162, 20)
        _piece(o, ox + 140, oy + 162, 20)
        for x in (ox + 110, ox + 150):
            o.append(S.line(x, oy + 114, x, oy + 150, stroke=S.INK, stroke_width=1.2))
        o.append(S.line(ox + 180, oy + 60, ox + 180, oy + 202, stroke=S.CONC, stroke_width=1.6, stroke_dasharray='4 4'))
    o.append(T(ox + 100, oy + 226, caps[kind], size=14, family=S.SERIF, anchor='middle'))
    return ''.join(o)


def _key(x, y, gap=190):
    return ''.join([
        S.rect(x, y - 11, 12, 12, fill=S.INK, stroke=S.INK, stroke_width=1),
        S.text(x + 20, y, 'peça do modelo legal', size=13, family=S.SERIF),
        S.rect(x + gap, y - 11, 12, 12, fill=S.PAPER, stroke=S.INK, stroke_width=1.8),
        S.text(x + gap + 20, y, 'peça criada pelas partes', size=13, family=S.SERIF)])


KINDS = ('tipico', 'atipico', 'misto', 'coligados', 'derivado')
TITLE = 'Típico, atípico, misto, coligados e derivado'


def build(p):
    if p.get('mobile', False):
        parts = []
        for i, k in enumerate(KINDS):
            parts.append(_panel(70, i * PH, k))
            if i:
                parts.append(S.line(30, i * PH, 310, i * PH, stroke=S.MUTED, stroke_width=.8))
        parts.append(S.rect(40, PH * 5 + 6, 12, 12, fill=S.INK, stroke=S.INK, stroke_width=1))
        parts.append(S.text(60, PH * 5 + 17, 'peça do modelo legal', size=13, family=S.SERIF))
        parts.append(S.rect(40, PH * 5 + 30, 12, 12, fill=S.PAPER, stroke=S.INK, stroke_width=1.8))
        parts.append(S.text(60, PH * 5 + 41, 'peça criada pelas partes', size=13, family=S.SERIF))
        return S.svg(340, PH * 5 + 54, TITLE, parts), []
    parts = [_panel(i * PW + 5, 0, k) for i, k in enumerate(KINDS)]
    for i in range(1, 5):
        parts.append(S.line(i * PW, 20, i * PW, PH - 20, stroke=S.MUTED, stroke_width=.8))
    parts.append(_key(300, PH + 22))
    return S.svg(PW * 5 + 10, PH + 40, TITLE, parts), []
