"""Aula 03: the process of formation, three dials for CC 428 and a two-city atlas for CC 433-435.

params:
  mode: planta | relogio | atlas.
  topic: core (default) | continuidade | informacao | silencio, for planta.

The planta is a schematic temporal spine, not a dated chronology of the cases. Each duty band is a notched flag that
starts where the duty starts and runs past the consent line; endpoints express legal scope, not measured duration.
Tracing a band (hover, focus or press) fills the stations and cases it covers (data-cov, lit by the page's CSS).
The dials express CC 428's three criteria without inventing hours: a point, an open arc, a closed arc.
Atlas contours stand for two unspecified cities, not real maps; the three arrival states illustrate CC 433 only.
All shapes and label positions are calculated here; output is never hand-edited.
"""
from __future__ import annotations
import math
from . import svg as S
from . import tgc01_hand as H

T = S.text


def line(x1, y1, x2, y2, **kw):
    return S.line(x1, y1, x2, y2, stroke=kw.pop('stroke', S.INK), stroke_width=kw.pop('stroke_width', 1.3), **kw)


def bracket(x0, x1, y, label):
    return [S.path(f'M{x0},{y+7} V{y} H{x1} V{y+7}', fill='none', stroke=S.INK2, stroke_width=1),
            T((x0 + x1) / 2, y - 8, label, size=12, anchor='middle', family=S.SERIF, fill=S.INK2)]


# (stations, bands as (name, from, to) in fractions of the spine, cases as (position, name, note), brackets)
CORE = (['Tratativas', 'Proposta', 'Aceitação', 'Execução', 'Após cumprir'],
        [('lealdade e correção', 0, 1), ('informação', 0, 1), ('cuidado e segurança', 0, 1), ('sigilo', 0, 1),
         ('cooperação', .5, 1)],
        [(.02, 'Asti / CBD', 'confiança sem contrato'), (.25, 'Eike', 'faltam termos essenciais'),
         (.75, 'Consórcio', 'confiança no cumprimento')])
TOPICS = {
    'continuidade': (['Pacto', 'Execução', 'Exercício do direito'],
                     [('interpretar', 0, 1), ('cooperar', .2, 1), ('controlar', .45, 1)],
                     [(.1, 'seguro', 'risco compreensível'), (.5, 'liras italianas', 'documentação necessária'),
                      (.9, 'tarifas', 'confiança na quitação')]),
    'informacao': (['Negociação', 'Informação', 'Decisão de contratar'],
                   [('acesso possível', 0, 1), ('confiança particular', .2, 1), ('informação devida', .45, 1)],
                   [(.1, 'investigar', 'diligência própria'), (.5, 'comunicar', 'dado essencial'),
                    (.9, 'consentir', 'riscos conhecidos')]),
    'silencio': (['Proposta', 'Contexto', 'Assentimento'],
                 [('declaração', 0, 1), ('atos de execução', .2, 1), ('silêncio qualificado', .45, 1)],
                 [(.1, 'vontade expressa', 'palavras ou gestos'), (.5, 'vontade tácita', 'conduta inequívoca'),
                  (.9, 'silêncio', 'usos e circunstâncias')]),
}


def planta(p):
    topic = p.get('topic', 'core')
    phases, bands, cases = CORE if topic == 'core' else TOPICS[topic]
    n = len(phases)
    tie = 2 if topic != 'continuidade' else 0            # station where the two strands are twisted into one cord
    xs = [210 + i * (960 - 210) / (n - 1) for i in range(n)]
    pos = lambda f: xs[0] + f * (xs[-1] - xs[0])
    sy, ny, gy = 150, 40, 62
    o = []
    tkey = (lambda k, a: 'b0' if a == 0 else 'b1') if topic == 'core' else (lambda k, a: f'b{k}')
    cov = lambda f_idx: ' '.join(sorted({tkey(k, a) for k, (_, a, b) in enumerate(bands) if a - 1e-6 <= f_idx / (n - 1) <= b + 1e-6}))
    # the bond: loose strands (proposta, aceitação) twisted into a cord at the tie station
    xt = xs[tie]
    cord_end = xs[-1] - 8 if tie < n - 1 else xs[-1] + 84
    body = []
    if tie > 0:
        xa = xs[tie - 1]
        if tie > 1:
            body.append(H.rule(f'M{xs[0]},{sy} H{xa}', S.INK2, 1.0, '2 5'))
        body.append(H.rule(f'M{xa},{sy} C{xa + 90},{sy - 20} {xt - 70},{sy} {xt + 6},{sy}', S.DIF, 2.0))
        xb = xa + (xt - xa) * .62
        body.append(H.mark(xb, sy + 28, S.DIF, r=6))
        body.append(H.rule(f'M{xb + 6},{sy + 28} C{xb + 50},{sy + 28} {xt - 50},{sy} {xt + 6},{sy}', S.DIF, 2.0))
        body.append(H.name(xb - 12, sy + 33, 'Oblato', S.DIF, anchor='end', size=12))
        body.append(H.name(xa - 6, sy + 26, 'Proponente', S.DIF, anchor='middle', size=12))
    body.append(H.cord(xt + 6, cord_end, sy))
    o.append(H.wire('b4', 'Rastrear o vínculo formado', body))
    # stations
    for i, label in enumerate(phases):
        x = xs[i]
        o.append(H.mark(x, sy, S.DIF if i == tie else S.INK, solid=(i == tie)).replace('<circle', f'<circle data-cov="{cov(i)} b4"' if i >= tie else f'<circle data-cov="{cov(i)}"', 1))
        o.append(H.name(x, ny, label, anchor='middle', size=13))
        o.append(H.rule(f'M{x},{gy + 12} V{sy - 10}', S.INK2, 1.0))
    if topic == 'core':
        o.append(H.gloss(xs[tie], gy + 4, 'o vínculo se forma', S.DIF, anchor='middle', size=13))
    for f, a, b in cases:
        k = round(f * (n - 1))
        if topic == 'core':
            if k == tie:
                continue
            b = {'Asti / CBD': '', 'Eike': 'sem termos essenciais, não há proposta', 'Consórcio': ''}[a]
            a = a if not b else ''
            if not (a or b):
                continue
            if a == 'Eike' or b:
                a, b = '', b
        o.append(H.gloss(xs[k], gy + 4, ' · '.join(t for t in (a, b) if t) if topic == 'core' else f'{a} · {b}', S.INK2, anchor='middle', size=13))
    # the duties: fine strands that ride along the cord from the first station and run past the last; where a case
    # breaks a duty, its strand lifts off in orange
    xe = 1050
    y0, dy = (204, 20) if topic == 'core' else (232, 34)
    breaks = {0: 0, 3: 0} if topic == 'core' else {}   # core only: Asti and Consórcio break the lealdade/confiança strand; Eike is no breach
    def strand(y, x0, bxs=()):
        out = H.rule(f'M{x0},{y} H{xe}', S.INK, 1.0)
        for bx in bxs:
            out += (H.rule(f'M{bx - 30},{y} H{bx + 30}', S.PAPER, 4.0) + H.rule(f'M{bx - 30},{y} C{bx - 12},{y} {bx - 14},{y + 10} {bx},{y + 10} C{bx + 14},{y + 10} {bx + 12},{y} {bx + 30},{y}', S.CONC, 2.0))
        return out
    rows = bands if topic != 'core' else bands
    ylast = y0 + dy * (len(bands) - 1)
    for x in xs:
        o.append(H.rule(f'M{x},{sy + 12} V{ylast}', S.GRID, 1.0, '2 5'))
    brk = {k: max(xs[k], xs[0] + 36) for k in breaks}
    if topic == 'core':
        grp = []
        for i, (nm, a, b) in enumerate(bands[:4]):
            y = y0 + dy * i
            grp += [strand(y, xs[0], [brk[k] for k, bi in breaks.items() if bi == i]), H.gloss(xs[0] - 14, y + 4, nm, S.INK, anchor='end', size=13)]
        grp += [H.gloss(brk[0] + 36, y0 - 7, 'Asti / CBD · lealdade · ruptura das tratativas (REsp 1.367.955/SP)', S.CONC, size=13),
                H.gloss(brk[3] + 36, y0 - 7, 'confiança · suppressio · art. 187', S.CONC, size=13)]
        grp.append(H.hit(xs[0], y0 - 10, xe - xs[0], dy * 3 + 20))
        o.append(H.wire('b0', 'Rastrear os deveres desde as tratativas', grp))
        nm, a, b = bands[4]
        y, x0 = y0 + dy * 4, pos(a)
        o.append(H.wire('b1', 'Rastrear o dever de cooperação', [strand(y, x0), H.mark(x0, y, S.INK, r=4.5),
                 H.gloss(x0 - 12, y + 4, nm, S.INK, anchor='end', size=13), H.hit(x0, y - 10, xe - x0, 22)]))
        yb = y0 + dy * 4 + 52
        for x1, x2, lab in [(xs[0], xs[2] - 12, 'antes do contrato'), (xs[2] + 12, xs[4] - 12, 'contrato em curso'), (xs[4] + 12, xe, 'depois')]:
            o.append(H.bracket(x1, x2, yb, up=False, col=S.INK2))
            o.append(H.gloss((x1 + x2) / 2, yb + 22, lab, S.INK2, anchor='middle', size=13))
        Hh = yb + 40
    else:
        for j, (nm, a, b) in enumerate(bands):
            y, x0 = y0 + j * dy, pos(a)
            o.append(H.wire(f'b{j}', f'Rastrear {nm}', [strand(y, x0), H.mark(x0, y, S.INK, r=4.5),
                     H.gloss(x0 - 12, y + 4, nm, S.INK, anchor='end', size=13), H.hit(x0, y - 12, xe - x0, 24)]))
        Hh = y0 + dy * 2 + 40
    return S.svg(1080, Hh, 'Deveres que acompanham a relação antes, durante e depois do contrato: o vínculo em dois fios que se torcem na aceitação', o)


def chevron(x, y, deg, n=12, spread=30):
    t = math.radians(deg)
    dx, dy = math.cos(t), math.sin(t)
    pts = []
    for sg in (1, -1):
        c, sn = math.cos(math.radians(spread * sg)), math.sin(math.radians(spread * sg))
        bx, by = -(dx * c - dy * sn), -(dx * sn + dy * c)
        pts.append((x + n * bx, y + n * by))
    return f'M{pts[0][0]:.1f},{pts[0][1]:.1f} L{x:.1f},{y:.1f} L{pts[1][0]:.1f},{pts[1][1]:.1f}'


def relogio():
    o = []
    cy, r = 150, 82
    heads = [('Presente, sem prazo', 'art. 428, I', 'aceitação imediata'),
             ('Ausente, sem prazo', 'art. 428, II', 'tempo razoável para a resposta chegar'),
             ('Ausente, com prazo', 'art. 428, III', 'resposta expedida dentro do prazo')]
    for i, (head, art, rule) in enumerate(heads):
        cx = 170 + 330 * i
        o += [H.name(cx, 26, head, anchor='middle', size=13.5),
              T(cx, 46, art, size=13, anchor='middle', fill=S.INK2)]
        for j in range(60):
            a = math.radians(j * 6 - 90)
            r0 = r - (9 if j % 5 == 0 else 4)
            o.append(line(cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + r * math.cos(a), cy + r * math.sin(a),
                          stroke=S.INK if j % 5 == 0 else S.GRID, stroke_width=1.2))
        ar = r - 22
        pt = lambda deg: (cx + ar * math.sin(math.radians(deg)), cy - ar * math.cos(math.radians(deg)))
        if i == 0:
            # an instant: the hand does not leave twelve
            o += [line(cx, cy, cx, cy - ar, stroke_width=2.6), S.circle(cx, cy - ar - 6, 6, fill=S.PAPER, stroke=S.CONC, stroke_width=2.2)]
        elif i == 1:
            # an open interval: dashed, no mark where it stops
            x1, y1 = pt(250)
            o += [S.path(f'M{cx},{cy-ar} A{ar},{ar} 0 1 1 {x1:.1f},{y1:.1f}', fill='none', stroke=S.INK, stroke_width=2.2, stroke_dasharray='2 6'),
                  line(cx, cy, cx, cy - ar, stroke_width=2.6),
                  S.path(chevron(x1, y1, 250), fill='none', stroke=S.INK, stroke_width=2)]
        else:
            x1, y1 = pt(90)
            o += [S.path(f'M{cx},{cy-ar} A{ar},{ar} 0 0 1 {x1:.1f},{y1:.1f}', fill='none', stroke=S.INK, stroke_width=2.6),
                  line(cx, cy, cx, cy - ar, stroke_width=2.6), line(cx, cy, x1, y1, stroke_width=2.6),
                  line(x1 + 2, y1 - 13, x1 + 2, y1 + 13, stroke=S.CONC, stroke_width=2.6)]
        o += [S.circle(cx, cy, 3.5, fill=S.INK), T(cx, 262, rule, size=13, anchor='middle', family=S.SERIF)]
    return S.svg(1000, 280, 'Três critérios para a duração da proposta, sem escala horária', o)


def territory(cx, cy, k, seed):
    """A closed contour of smooth curves; the radii differ so no two cities look alike."""
    rs = [(150, 100), (162, 108), (140, 118), (118, 96), (138, 104), (160, 94)][seed:] + [(150, 100), (162, 108), (140, 118), (118, 96), (138, 104), (160, 94)][:seed]
    pts = [(cx + rx * math.cos(math.radians(a)) * k, cy + ry * math.sin(math.radians(a)) * k)
           for a, (rx, ry) in zip(range(-80, 280, 60), rs)]
    m = [((pts[i][0] + pts[(i + 1) % 6][0]) / 2, (pts[i][1] + pts[(i + 1) % 6][1]) / 2) for i in range(6)]
    d = f'M{m[5][0]:.1f},{m[5][1]:.1f} '
    for i in range(6):
        d += f'Q{pts[i][0]:.1f},{pts[i][1]:.1f} {m[i][0]:.1f},{m[i][1]:.1f} '
    return d + 'Z'


def atlas():
    o = []
    ay = 130
    A, B = (215, ay), (785, ay)
    o += [S.path(territory(215, 150, 1.6, 0), fill='none', stroke=S.INK, stroke_width=1.6),
          S.path(territory(785, 150, 1.6, 2), fill='none', stroke=S.INK, stroke_width=1.6)]
    for (cx, cy), lab, sub, subfill in [(A, 'Lugar da proposta', 'art. 435', S.INK2), (B, 'Lugar da aceitação', 'expedição, art. 434', S.INK2)]:
        o += [line(cx - 22, cy, cx + 22, cy, stroke=S.GRID), line(cx, cy - 22, cx, cy + 22, stroke=S.GRID),
              S.circle(cx, cy, 6, fill=S.PAPER, stroke=S.INK, stroke_width=1.8),
              H.name(cx, cy + 34, lab, anchor='middle', size=13.5),
              T(cx, cy + 54, sub, size=12, anchor='middle', fill=subfill)]
    o += [T(A[0], A[1] + 74, 'o contrato se localiza aqui', size=12.5, anchor='middle', family=S.SERIF, fill=S.DIF)]
    o += [line(B[0] - 12, ay, A[0] + 14, ay, stroke_width=1.6), S.path(f'M{A[0]+25},{ay-6} L{A[0]+14},{ay} L{A[0]+25},{ay+6}', fill='none', stroke=S.INK, stroke_width=1.6),
          T(500, ay - 12, 'aceitação', size=12.5, anchor='middle', family=S.SERIF)]
    # the clock of arrivals at the proponent: acceptance fixed, retraction movable
    y, ax = 400, 600
    o += [H.name(110, y + 4, 'chegada ao proponente', size=13),
          line(330, y, 930, y), S.path(f'M924,{y-4} l6,4 l-6,4', fill='none', stroke=S.INK)]
    o += bracket(330, ax, y - 52, 'a retratação que chega aqui impede a aceitação')
    o += [S.circle(ax, y, 6, fill=S.INK, stroke=S.INK), T(ax, y + 28, 'aceitação', size=12.5, anchor='middle', family=S.SERIF),
          T(ax, y + 46, 'art. 433', size=13, anchor='middle', fill=S.INK2)]
    for i, x in enumerate([450, ax, 780]):
        dy = -2 if i != 1 else 0
        o.append(f'<g data-order="{i}"' + ('' if i == 0 else ' display="none"') + '>'
                 + line(x, y - 16, x, y + 16, stroke=S.CONC, stroke_width=3) + T(x, y - 22 - (0 if i != 1 else 0), 'retratação', size=12.5, anchor='middle', family=S.SERIF, fill=S.CONC) + '</g>')
    return S.svg(1000, 480, 'O lugar da proposta e a ordem da chegada da retratação da aceitação', o)


def build(p):
    mode = p.get('mode', 'planta')
    return {'planta': lambda: planta(p), 'relogio': relogio, 'atlas': atlas}[mode](), []
