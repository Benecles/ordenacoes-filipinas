"""Princípios contratuais, Aula 02: three drawings in three paper languages.

modes
  escolhas  four lines of will, each running into the stop where the law steps in (hand line / ruled stop; Pereira pp. 22-28,
            Venosa, CDC art. 39 II e IX, CC art. 425): contratar ou recusar, a contraparte, a modalidade, o conteúdo.
  fim       three plans (a street, a church footprint, a sheaf of material): the thing still possible is solid, the end
            it was meant for is dashed and crossed (coroação, Larenz, Zeca; Orlando Gomes via the lesson, REsp 1.316.149/SP).
  fecho     the closing instrument: the Zeca contract as concentric rings; press a ring for the principle it shows.
Every mode returns a wide drawing and a narrow one (same marks, laid out for a phone). Facts come from the lesson's sources only.
"""
from __future__ import annotations

import math

from . import svg as S

T = S.text


def _wave(x0, x1, y, amp=4.2, period=24):
    n = max(1, round((x1 - x0) / period))
    p = (x1 - x0) / n
    seg = f' q{p / 4:.2f},{-amp} {p / 2:.2f},0 q{p / 4:.2f},{amp} {p / 2:.2f},0'
    return f'M{x0:.1f},{y}' + seg * n


def _ellipse_pts(cx, cy, rx, ry, amp=0.0, waves=0, n=240):
    pts = []
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        k = 1 + (amp * math.sin(waves * a) if waves else 0)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return pts


def _poly(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ' Z'


def _cross(o, x, y, r=10, w=2.6):
    o.append(S.path(f'M{x - r},{y - r} L{x + r},{y + r} M{x + r},{y - r} L{x - r},{y + r}', fill='none', stroke=S.CONC, stroke_width=w))


# ---------------------------------------------------------------- escolhas

def escolhas(narrow):
    o = []
    rows = [('Contratar ou recusar', 'imposto', 'stop'), ('Escolher a contraparte', 'coativo', 'stop'),
            ('Definir a modalidade', None, 'free'), ('Estipular o conteúdo', 'cogente', 'mixed')]
    if narrow:
        W, H, x0, xs, step = 340, 372, 16, 226, 88
    else:
        W, H, x0, xs, step = 800, 304, 262, 572, 70
    for i, (name, stop, kind) in enumerate(rows):
        if narrow:
            yl = 38 + i * step
            y = yl + 24
            o.append(T(x0 - 4, yl, name, size=17, family=S.SERIF))
        else:
            y = 50 + i * step
            o.append(T(20, y + 6, name, size=19, family=S.SERIF))
        o.append(S.circle(x0, y, 6, fill=S.PAPER, stroke=S.INK, stroke_width=2))
        end = xs if kind in ('stop', 'mixed') else xs + 40
        if kind == 'mixed':
            a, b = (x0 + 70, x0 + 130) if narrow else (x0 + 80, x0 + 176)
            o.append(S.path(_wave(x0 + 6, a, y), fill='none', stroke=S.INK, stroke_width=2))
            o.append(S.line(a, y, b, y, stroke=S.INK2, stroke_width=2.2, stroke_dasharray='2 6'))
            o.append(S.path(_wave(b, end, y), fill='none', stroke=S.INK, stroke_width=2))
            o.append(T((a + b) / 2, y + (28 if narrow else 30), 'supletiva', size=15, family=S.SANS, fill=S.INK2, anchor='middle'))
        else:
            o.append(S.path(_wave(x0 + 6, end, y), fill='none', stroke=S.INK, stroke_width=2))
        if kind in ('stop', 'mixed'):
            o += S.hatch(xs, y - 13, 40, 26, step=7, stroke=S.CONC, stroke_width=1.3)
            o.append(S.line(xs, y - 17, xs, y + 17, stroke=S.CONC, stroke_width=3.2))
            o.append(T(xs + 52 if not narrow else xs + 46, y + 5, stop, size=16, family=S.SANS, fill=S.CONC))
        else:
            o.append(S.circle(end, y, 6, fill=S.PAPER, stroke=S.INK, stroke_width=2))
            if narrow:
                o.append(T(x0 - 4, y + 32, 'tipo livre · art. 425', size=14, family=S.SANS, fill=S.INK2))
            else:
                o.append(T(xs + 62, y + 5, 'tipo livre · art. 425', size=15, family=S.SANS, fill=S.INK2))
    return S.svg(W, H, 'Quatro escolhas da autonomia privada e o ponto em que a lei impõe, dirige ou deixa livre', o)


# ---------------------------------------------------------------- fim

def _scene_street(o):
    o.append(T(120, 16, 'Coroação de Eduardo VII', size=17, family=S.SANS, weight='600', anchor='middle'))
    for yb, s in ((52, 1), (118, -1)):
        o.append(S.line(8, yb, 232, yb, stroke=S.INK, stroke_width=1.8))
        for x in (26, 70, 114, 158, 198):
            o.append(S.path(f'M{x},{yb} v{14 * s} h20 v{-14 * s}', fill='none', stroke=S.INK, stroke_width=1.8))
    o.append(S.line(14, 85, 226, 85, stroke=S.MUTED, stroke_width=1.6, stroke_dasharray='7 6'))
    o.append(S.path('M216,79 L228,85 L216,91', fill='none', stroke=S.MUTED, stroke_width=1.6))
    _cross(o, 120, 85)
    o.append(T(120, 176, 'janelas e sacadas à disposição', size=15, family=S.SERIF, anchor='middle'))
    o.append(T(120, 198, 'cortejo cancelado', size=15, family=S.SANS, fill=S.CONC, anchor='middle'))


def _scene_church(o):
    o.append(T(120, 16, 'Porta da igreja demolida', size=17, family=S.SANS, weight='600', anchor='middle'))
    o.append(S.path('M64,134 V70 A56,30 0 0 1 176,70 V134 Z', fill='none', stroke=S.MUTED, stroke_width=1.6, stroke_dasharray='7 6'))
    o.append(S.line(110, 134, 110, 106, stroke=S.INK, stroke_width=3.2))
    o.append(S.path('M110,106 A28,28 0 0 1 138,134', fill='none', stroke=S.INK, stroke_width=1.6))
    o.append(S.circle(110, 134, 3.5, fill=S.INK, stroke=S.INK, stroke_width=1))
    _cross(o, 120, 78)
    o.append(T(120, 176, 'a porta feita para o portal', size=15, family=S.SERIF, anchor='middle'))
    o.append(T(120, 198, 'igreja bombardeada', size=15, family=S.SANS, fill=S.CONC, anchor='middle'))


def _scene_material(o):
    o.append(T(120, 16, 'Campanha de Zeca', size=17, family=S.SANS, weight='600', anchor='middle'))
    o.append(S.path('M58,40 H182 V96 H58 Z', fill='none', stroke=S.MUTED, stroke_width=1.6, stroke_dasharray='7 6'))
    o.append(S.line(88, 96, 88, 132, stroke=S.MUTED, stroke_width=1.6, stroke_dasharray='7 6'))
    o.append(S.line(152, 96, 152, 132, stroke=S.MUTED, stroke_width=1.6, stroke_dasharray='7 6'))
    _cross(o, 120, 68)
    for k in range(3):
        x, y = 72 + k * 7, 118 - k * 7
        o.append(S.rect(x, y, 84, 34, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
    o.append(S.line(86, 106, 134, 106, stroke=S.MUTED, stroke_width=1.2))
    o.append(S.line(86, 114, 120, 114, stroke=S.MUTED, stroke_width=1.2))
    o.append(T(120, 176, 'material produzido', size=15, family=S.SERIF, anchor='middle'))
    o.append(T(120, 198, 'material imprestável', size=15, family=S.SANS, fill=S.CONC, anchor='middle'))


def fim(narrow):
    scenes = (_scene_street, _scene_church, _scene_material)
    o = []
    if narrow:
        W, H = 340, 3 * 214
        for i, sc in enumerate(scenes):
            o.append(f'<g transform="translate(50,{i * 214 + 8})">')
            sub = []
            sc(sub)
            o += sub
            o.append('</g>')
            if i:
                o.append(S.line(24, i * 214 - 4, 316, i * 214 - 4, stroke=S.GRID, stroke_width=1))
    else:
        W, H = 800, 212
        for i, sc in enumerate(scenes):
            o.append(f'<g transform="translate({8 + i * 268},8)">')
            sub = []
            sc(sub)
            o += sub
            o.append('</g>')
            if i:
                o.append(S.line(i * 268 - 4, 6, i * 268 - 4, 206, stroke=S.GRID, stroke_width=1))
    return S.svg(W, H, 'Três casos em que a prestação continua possível e o fim conhecido das partes já não se atinge', o)


# ---------------------------------------------------------------- fecho

ANSWERS = {
    'lib': ('Liberdade', 'O contrato anterior sustentava uma campanha criada por Fischer e All-E, com o cantor vinculado à exclusividade.'),
    'forca': ('Força obrigatória', 'A exclusividade em execução podia ser exigida, e seu descumprimento gerava reparação.'),
    'rel': ('Relatividade', 'A agência África não prometera protagonizar a campanha da Nova Schin; terceira, não devia a prestação do cantor.'),
    'fs': ('Função social', 'O dever externo de respeitar o contrato, expresso na boa-fé e na tutela contra a concorrência desleal, sustentou a responsabilidade da agência.'),
}


def _g(key, label, body):
    return f'<g data-pr="{key}" role="button" tabindex="0" aria-pressed="false" aria-label="{S.esc(label)}">' + ''.join(body) + '</g>'


def _halo(x, y, s, **kw):
    return T(x, y, s, stroke=S.PAPER, stroke_width=5, paint_order='stroke', **kw)


def fecho_svg(narrow):
    if narrow:
        W, H = 340, 400
        cx, cy = 170, 204
        rin = (74, 74)
        bo, bi = (166, 166), (146, 146)
        dx = 34
        na = (279, cy)
        sz = 12.5
    else:
        W, H = 800, 336
        cx, cy = 400, 168
        rin = (150, 64)
        bo, bi = (370, 154), (338, 130)
        dx = 60
        na = (640, cy)
        sz = 15
    o = []
    # outer band: social function, the limit (radial ticks between two ellipses)
    band = []
    n = 96
    for i in range(n):
        a = 2 * math.pi * i / n
        band.append(S.line(cx + bi[0] * math.cos(a), cy + bi[1] * math.sin(a), cx + bo[0] * math.cos(a), cy + bo[1] * math.sin(a), stroke=S.CONC, stroke_width=1.2))
    band.append(f'<ellipse {S.attrs(cx=cx, cy=cy, rx=bo[0], ry=bo[1], fill="none", stroke=S.CONC, stroke_width=2.2)}/>')
    band.append(f'<ellipse {S.attrs(cx=cx, cy=cy, rx=bi[0], ry=bi[1], fill="none", stroke=S.CONC, stroke_width=1.2)}/>')
    band.append(f'<ellipse {S.attrs(cx=cx, cy=cy, rx=(bo[0] + bi[0]) / 2, ry=(bo[1] + bi[1]) / 2, fill="none", stroke=S.INK, stroke_opacity="0", stroke_width=(bo[0] - bi[0]) + 12, pointer_events="stroke")}/>')
    ty = cy - (bo[1] + bi[1]) / 2 + 5
    band.append(_halo(cx, ty, 'função social', size=sz, family=S.SANS, fill=S.CONC, anchor='middle', weight='600'))
    o.append(_g('fs', 'Função social', band))
    # liberty: the ring the parties drew by hand
    lib = [S.path(_poly(_ellipse_pts(cx, cy, rin[0], rin[1], 0.035, 30 if not narrow else 20)), fill=S.PAPER2, stroke=S.INK, stroke_width=2.4),
           f'<ellipse {S.attrs(cx=cx, cy=cy, rx=rin[0], ry=rin[1], fill="none", stroke=S.INK, stroke_opacity="0", stroke_width=26, pointer_events="stroke")}/>',
           T(cx, cy + rin[1] + (sz + 12), 'liberdade', size=sz + 1, family=S.SERIF, anchor='middle', font_style='italic')]
    o.append(_g('lib', 'Liberdade', lib))
    # binding force: the bond between the parties
    bx0, bx1 = cx - dx, cx + dx
    forca = [S.line(bx0, cy, bx1, cy, stroke=S.INK, stroke_width=4),
             S.circle(bx0, cy, 7, fill=S.PAPER, stroke=S.INK, stroke_width=2.4), S.circle(bx1, cy, 7, fill=S.PAPER, stroke=S.INK, stroke_width=2.4),
             T(cx, cy - 16, 'força obrigatória', size=sz, family=S.SERIF, anchor='middle', font_style='italic'),
             S.rect(bx0 - 70, cy - 34, bx1 - bx0 + 140, 82, fill='none', pointer_events='all')]
    if narrow:
        forca += [T(bx0, cy + 25, 'Fischer', size=sz, family=S.SANS, anchor='middle'), T(bx0, cy + 41, 'All-E', size=sz, family=S.SANS, anchor='middle'),
                  T(bx1, cy + 25, 'Zeca', size=sz, family=S.SANS, anchor='middle')]
    else:
        forca += [T(bx0, cy + 30, 'Fischer / All-E', size=sz + 1, family=S.SANS, anchor='middle'), T(bx1, cy + 30, 'Zeca', size=sz + 1, family=S.SANS, anchor='middle')]
    o.append(_g('forca', 'Força obrigatória', forca))
    # relativity: the third party stands outside the ring; its interference reaches the bond
    ax, ay = na
    if narrow:
        arc = f'M{ax - 6},{ay - 12} Q{ax - 40},{ay - 78} {bx1 + 4},{ay - 11}'
        lab = (ax - 44, ay - 84)
    else:
        arc = f'M{ax - 10},{ay - 9} Q{ax - 90},{ay - 112} {bx1 + 8},{ay - 10}'
        lab = (ax - 92, ay - 84)
    rel = [S.circle(ax, ay, 7, fill=S.PAPER, stroke=S.INK, stroke_width=2.4),
           T(ax, ay + 28, 'África', size=sz + 1, family=S.SANS, anchor='middle'),
           T(ax, ay + 46, 'relatividade', size=sz, family=S.SERIF, anchor='middle', font_style='italic'),
           S.path(arc, fill='none', stroke=S.CONC, stroke_width=2.6),
           S.path(f'M{bx1 + 16},{ay - 22} L{bx1 + 5},{ay - 11} L{bx1 + 19},{ay - 5}', fill='none', stroke=S.CONC, stroke_width=2.2),
           T(lab[0], lab[1], 'induz à ruptura', size=sz, family=S.SANS, fill=S.CONC, anchor='middle'),
           S.rect(ax - 52, ay - 20, 104, 80, fill='none', pointer_events='all')]
    o.append(_g('rel', 'Relatividade', rel))
    return S.svg(W, H, 'O contrato de Zeca em anéis: o que as partes traçaram, o vínculo, o terceiro fora dele e o limite social', o)


def fecho_answers():
    return '<div class="closing-answer" aria-live="polite">' + ''.join(
        f'<p data-for="{k}"><span class="pr-name">{n}</span>{t}</p>' for k, (n, t) in ANSWERS.items()) + '</div>'


def build(p):
    mode = p['mode']
    if mode == 'fecho':
        return ('<div class="drawing-desktop">' + fecho_svg(False) + '</div><div class="drawing-mobile">' + fecho_svg(True) + '</div>' + fecho_answers()), []
    fn = {'escolhas': escolhas, 'fim': fim}[mode]
    return '<div class="drawing-desktop">' + fn(False) + '</div><div class="drawing-mobile">' + fn(True) + '</div>', []
