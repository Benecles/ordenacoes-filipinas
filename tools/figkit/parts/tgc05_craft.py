"""Aula 05: exchange record, fishing net, delivery and the horse's intended use.
Sources: Pereira III pp.59-60; Venosa pp.34,116,119. Marks are schematic,
not amounts, measured trajectories, or additional facts about Vandir.
"""
from . import svg as S

def t(x,y,s,size=18,**kw):
    return S.text(x,y,s,size=size,family=S.SERIF,**kw)

def line(x,y,a,b,**kw):
    return S.line(x,y,a,b,stroke=S.INK,stroke_width=1.5,**kw)

from .tgc01_hand import cord, rule, mark, name, gloss, bracket


def _arrow(x1, x2, y, col=S.INK, w=1.3):
    d = 1 if x2 > x1 else -1
    return S.path(f'M{x1},{y} H{x2} M{x2 - 7 * d},{y - 4} L{x2},{y} L{x2 - 7 * d},{y + 4}', fill='none', stroke=col,
                  stroke_width=w, stroke_linecap='round', stroke_linejoin='round')


def _cut(x, y, h=9):
    return S.path(f'M{x - 5},{y + h} L{x + 5},{y - h}', fill='none', stroke=S.CONC, stroke_width=2, stroke_linecap='round')


def exchange():
    # Two bonds on one scale. Sale: two strands twisted, the advantage goes one way and the encargo comes back.
    # Pure gift: one strand, the return path is cut. No fictitious price or money count.
    xa, xb = 250, 560
    o = [name(xa, 34, 'Vantagem recebida', anchor='middle', size=12), name(xb, 34, 'Encargo em troca', anchor='middle', size=12)]
    ya, yb = 122, 236
    o += [gloss(24, ya + 5, 'Compra e venda', size=15, col=S.INK), gloss(24, yb + 5, 'Doação pura', size=15, col=S.INK)]
    o += [cord(xa + 9, xb - 9, ya, amp=7, half=24, taper=30), mark(xa, ya), mark(xb, ya),
          _arrow(xa + 24, xb - 24, ya - 22), _arrow(xb - 24, xa + 24, ya + 22, S.DIF)]
    o += [S.path(f'M{xa + 9},{yb} H{xb - 9}', fill='none', stroke=S.DIF, stroke_width=2, stroke_linecap='round'),
          mark(xa, yb), mark(xb, yb), _arrow(xa + 24, xb - 24, yb - 22),
          rule(f'M{xb - 24},{yb + 22} H{xa + 24}', S.MUTED, 1.0, '3 6'), _cut((xa + xb) / 2, yb + 22)]
    return S.svg(640, 290, 'Compra e venda: vantagem de ida e encargo de volta; doação pura: só a ida, o retorno cortado', o), []


def net(state):
    o = [name(24, 36, {'hope': 'Esperança · sem captura', 'empty': 'Coisa esperada · sem captura', 'catch': 'Coisa esperada · captura escassa'}[state], size=12.5)]
    # A net: mouth and pouch carry the captured quantity, not a label card.
    o += [S.path('M65,95 Q225,65 385,95 L340,270 Q225,330 110,270 Z', fill='none', stroke=S.INK, stroke_width=1.6)]
    for k in range(1, 8):
        x = 65 + k * 40
        o += [S.path(f'M{x},92 Q225,180 {130 + k * 23},282', fill='none', stroke=S.GRID, stroke_width=1)]
    for y, w in [(132, 145), (172, 135), (212, 124), (252, 112)]:
        o += [S.path(f'M{225 - w},{y} Q225,{y + 25} {225 + w},{y}', fill='none', stroke=S.GRID, stroke_width=1)]
    if state == 'catch':
        o += [S.path('M190,247 Q220,225 247,247 Q220,269 190,247 L176,235 V259 Z', fill='none', stroke=S.DIF, stroke_width=2), S.circle(237, 245, 2, fill=S.INK)]
    color = S.CONC if state == 'empty' else S.DIF
    if state == 'empty':
        o += ['<g opacity="0.45">' + cord(55, 395, 348, amp=7, half=24, taper=30) + '</g>', _cut(225, 348, 14)]
    else:
        o += [cord(55, 395, 348, amp=7, half=24, taper=30)]
    o += [mark(55, 348, S.INK), mark(395, 348, S.INK),
          name(55, 384, 'Preço integral' if state != 'empty' else 'Preço restituído', col=color, size=13),
          gloss(24, 424, 'Sem culpa do alienante.', size=16, col=S.INK)]
    return S.svg(450, 450, 'Rede de pesca e efeito da captura sobre o preço contratado', o), []


def delivery():
    # The same unparticularised thing passes from promised (dashed) to delivered (solid); the bond below is a single
    # dotted strand until the delivery, a twisted cord after it.
    o = [name(24, 36, 'Comodato · entrega constitutiva', size=12.5), rule('M300,75 V250', S.MUTED, 1.0, '3 6')]
    for x, dashed in [(95, True), (385, False)]:
        o += [S.path(f'M{x},135 l70,-25 l75,30 v90 l-70,25 l-75,-30 Z M{x},135 l75,30 l70,-25 M{x + 75},165 v90', fill='none', stroke=S.INK,
                     stroke_width=1.6, **({'stroke_dasharray': '5 6'} if dashed else {}))]
    o += [rule('M40,292 H292', S.CONC, 1.5, '2 7'), cord(308, 600, 292, amp=7, half=24, taper=30), mark(300, 292, S.INK, 5),
          gloss(40, 332, 'Promessa de emprestar', size=17, col=S.INK), gloss(360, 332, 'Coisa entregue', size=17, col=S.DIF),
          name(40, 364, 'Ainda sem comodato', col=S.CONC, size=12), name(360, 364, 'Contrato formado', col=S.DIF, size=12)]
    return S.svg(640, 384, 'A promessa precede a entrega; a entrega constitui o comodato', o), []


def horse():
    # Literal object of the example in Venosa p.119. No diagnostic anatomy.
    o = [name(24, 36, 'Cavalo destinado à corrida', size=12.5),
         S.path('M120,175 Q155,125 265,150 L303,90 L335,75 L355,108 L335,152 L310,155 L300,205 L275,238 L270,302 L253,302 L246,226 L195,226 L166,300 L149,300 L156,218 L131,204 L102,260 L87,253 L108,208 Z', fill='none', stroke=S.INK, stroke_width=1.6, stroke_linejoin='round'),
         S.path('M120,175 Q65,142 67,221', fill='none', stroke=S.INK, stroke_width=2, stroke_linecap='round'),
         S.path('M340,166 Q375,154 394,168 M348,184 Q376,172 394,186', fill='none', stroke=S.CONC, stroke_width=2, stroke_dasharray='6 7'),
         name(24, 344, 'Moléstia respiratória', col=S.CONC, size=12.5), gloss(24, 378, 'A finalidade da aquisição fica comprometida.', size=16, col=S.INK)]
    return S.svg(450, 405, 'O cavalo e o problema respiratório que compromete a finalidade da aquisição', o), []


def build(p):
    mode=p.get('mode','exchange')
    if mode=='net':return net(p['state'])
    return {'exchange':exchange,'delivery':delivery,'horse':horse}[mode]()
