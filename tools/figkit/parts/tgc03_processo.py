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
    X0, X1, SP = 120, 860, 96
    xs = [X0 + i * (X1 - X0) / (n - 1) for i in range(n)]
    pos = lambda f: X0 + f * (X1 - X0)
    row, top = 36, 160
    base = top + row * len(bands) + 26
    H = base + 86
    cover = lambda a, b, f: a - 1e-6 <= f <= b + 1e-6
    o = []
    if topic == 'core':
        o += bracket(xs[0], xs[2] - 10, 30, 'antes do contrato')
        o += bracket(xs[2] + 10, xs[4] - 10, 30, 'contrato em curso')
        o += bracket(xs[4] + 10, 940, 30, 'depois')
        o += [line(xs[2], SP + 14, xs[2], base - 14, stroke=S.DIF, stroke_dasharray='3 5'),
              T(xs[2] + 12, SP + 34, 'o vínculo se forma', size=12, fill=S.DIF, family=S.SERIF)]
    o += [line(X0 - 30, SP, 945, SP), S.path(f'M939,{SP-4} l6,4 l-6,4', fill='none', stroke=S.INK)]
    for i, (x, label) in enumerate(zip(xs, phases)):
        cov = ' '.join(f'b{k}' for k, (_, a, b) in enumerate(bands) if cover(a, b, i / (n - 1)))
        o += [line(x, SP, x, SP + 12),
              S.circle(x, SP, 5, fill=S.PAPER, stroke=S.INK, stroke_width=1.6, data_cov=cov),
              T(x, SP - 16, label, size=12.5, anchor='middle', family=S.SANS)]
    for i, (name, f0, f1) in enumerate(bands):
        y, x0, x1 = top + i * row, pos(f0) if f0 else X0, 930
        if f1 < 1:
            x1 = pos(f1)
        body = [S.path(f'M{x0},{y-12} H{x1} l-9,12 l9,12 H{x0} Z', fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
                S.circle(x0, y, 4.5, fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
                T(x0 + 17, y + 4.5, name, size=12, family=S.SANS)]
        o.append(f'<g data-thread="b{i}" tabindex="0" role="link" aria-label="Traçar {S.esc(name)}">' + ''.join(body) + '</g>')
    ay = base + 6
    o.append(line(X0 - 30, ay, 945, ay, stroke=S.GRID, stroke_width=1.2))
    for f, a, b in cases:
        x = pos(f)
        cov = ' '.join(f'b{k}' for k, (_, c, d) in enumerate(bands) if cover(c, d, f))
        o += [line(x, top - 12, x, ay, stroke=S.GRID, stroke_dasharray='2 4'),
              S.rect(x - 5, ay - 5, 10, 10, fill=S.PAPER, stroke=S.INK, stroke_width=1.5, data_cov=cov),
              T(x, ay + 26, a, size=12, family=S.SANS, weight=600, anchor='middle'),
              T(x, ay + 46, b, size=12, family=S.SERIF, anchor='middle')]
    return S.svg(1000, H, 'Deveres que acompanham a relação antes, durante e depois do contrato', o)


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
        o += [T(cx, 26, head, size=13, anchor='middle', family=S.SANS, weight=600),
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
              T(cx, cy + 34, lab, size=13, anchor='middle', family=S.SANS, weight=600),
              T(cx, cy + 54, sub, size=12, anchor='middle', fill=subfill)]
    o += [T(A[0], A[1] + 74, 'o contrato se localiza aqui', size=12.5, anchor='middle', family=S.SERIF, fill=S.DIF)]
    o += [line(B[0] - 12, ay, A[0] + 14, ay, stroke_width=1.6), S.path(f'M{A[0]+25},{ay-6} L{A[0]+14},{ay} L{A[0]+25},{ay+6}', fill='none', stroke=S.INK, stroke_width=1.6),
          T(500, ay - 12, 'aceitação', size=12.5, anchor='middle', family=S.SERIF)]
    # the clock of arrivals at the proponent: acceptance fixed, retraction movable
    y, ax = 400, 600
    o += [T(110, y + 4, 'chegada ao proponente', size=12, family=S.SANS, anchor='start'),
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
