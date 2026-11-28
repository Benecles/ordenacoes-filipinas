"""Aula 05, blueprint round 2: campo, autos, calendario, tally, garantia.

Params: mode (default campo). No dimensions or invented quantities supplied by
the caller. Campo is a qualitative classification, not a scale of risk. Its
trace hooks connect each contract to the regimes it activates. Sources:
Pereira §§192/194; exam lists q3–5. Autos has chain-of-title tabs, not measured
volume (REsp 1.332.112 pp.7/13). Calendario counts 30/90 consecutive days,
without assigning dates or turning a civil year into 365 days. Tally uses
three schematic performances, not facts of Vandir's transaction (CM §195).
Garantia is the companion's three relations (CM §§207–211).
"""
from . import svg as S


from . import svg as S
from .tgc01_hand import cord, rule, mark, name, gloss, art, bracket


def tr(d, col=S.INK, w=1.0, **kw):
    """Hairline of a trace group: turns blue when the thread is lit (page CSS .tr)."""
    return S.path(d, fill='none', stroke=col, stroke_width=w, stroke_linecap='round', stroke_linejoin='round', class_='tr', **kw)


def arrow(x1, x2, y, col=S.INK, w=1.3):
    d = 1 if x2 > x1 else -1
    return S.path(f'M{x1},{y} H{x2} M{x2 - 7 * d},{y - 4} L{x2},{y} L{x2 - 7 * d},{y + 4}', fill='none', stroke=col,
                  stroke_width=w, stroke_linecap='round', stroke_linejoin='round')


def cut(x, y, h=9, col=S.CONC, w=2.0):
    """An orange cut mark across a line (limits and breaks only)."""
    return S.path(f'M{x - 5},{y + h} L{x + 5},{y - h}', fill='none', stroke=col, stroke_width=w, stroke_linecap='round')


def campo():
    # Field: columns = vantagem (gratuito | oneroso), rows = incerteza (sem álea | com álea). A contract is a named
    # mark; the cord runs from it along the rail of each regime it switches on. Gratuito = one strand (the advantage
    # has no return); oneroso = two strands twisted. All twisted cords end on the flags at x = X1, so strands coincide.
    X1 = 852
    rails = {'vicios': 262, 'eviccao': 304, 'alea': 346, 'estrita': 388}
    o = [rule('M300,30 V232', S.INK2, 1.0, '2 5'), rule('M24,150 H840', S.GRID, 1.0),
         name(150, 44, 'gratuito', col=S.INK2, anchor='middle', size=11.5), name(560, 44, 'oneroso', col=S.INK2, anchor='middle', size=11.5),
         gloss(24, 92, 'sem álea', size=14), gloss(24, 192, 'com álea', size=14)]
    for ident, x, y, label, note, to in [
        ('doacao', 150, 96, 'Doação pura', 'vantagem sem encargo', ['estrita']),
        ('lotes', 420, 96, 'Lotes de Vandir', 'preço e lotes definidos', ['vicios', 'eviccao']),
        ('capital', 660, 96, 'Integralização', 'imóvel por quotas', ['vicios', 'eviccao']),
        ('swap', 468, 190, 'Swap', 'oscilação assumida', ['alea']),
        ('loteria', 708, 190, 'Projeto de loteria', 'remuneração incerta', ['alea'])]:
        o.append(f'<g data-thread="{ident}" data-fio="{ident}" tabindex="0" role="button" aria-label="Traçar {label}" aria-pressed="false">')
        o += [S.rect(x - 15, y - 24, 205, 62, fill='none', pointer_events='all'),
              tr(f'M{x},{y + 7} V{max(rails[r] for r in to)}', data_lk=ident)]
        for r in to:
            ry = rails[r]
            o.append(f'<g data-lk="{ident}">' + (cord(x, X1, ry, amp=6.5, half=24, taper=30) if ident != 'doacao' else
                     S.path(f'M{x},{ry} H{X1}', fill='none', stroke=S.DIF, stroke_width=2, stroke_linecap='round')) + '</g>')
            o.append(S.circle(x, ry, 3.5, fill=S.INK, stroke=S.INK, data_lk=ident))
        o += [mark(x, y, S.INK, 6.5), name(x + 15, y + 4, label, size=12.5), gloss(x + 15, y + 24, note, size=14), '</g>']
    for r, a, b in [('vicios', 'vícios redibitórios', 'utilidade da coisa'),
                    ('eviccao', 'evicção', 'direito transmitido'),
                    ('alea', 'álea assumida', 'resultado suportado'),
                    ('estrita', 'interpretação estrita', 'benefício não se amplia')]:
        y = rails[r]
        o += [mark(X1, y, S.CONC if r == 'estrita' else S.INK, 5), name(X1 + 14, y - 1, a, size=12.5),
              gloss(X1 + 14, y + 15, b, size=14)]
    return S.svg(1080, 416, 'Campo de vantagem e álea; traçar cada contrato até os regimes que ele aciona', o), []


def autos():
    # The chain of titles as one cord: three named marks (the title passes Onogás to Philips to Vandir). The orange
    # bracket is the prior cause (execução fiscal); the orange cut is the present restraint found in the 2006 certidões.
    xs = [120, 400, 680]
    o = [bracket(xs[0], xs[2], 70, up=False, col=S.CONC),
         name(xs[0], 52, 'Execução fiscal', col=S.CONC), gloss(xs[0] + 150, 52, 'causa anterior à compra', col=S.CONC)]
    for a, b in [(xs[0], xs[1]), (xs[1], xs[2])]:
        o.append(cord(a + 9, b - 9, 130, amp=7, half=24, taper=30))
    for x, nm, d in zip(xs, ['Onogás', 'Philips', 'Vandir'], ['proprietária anterior', 'alienante', 'adquirente em 2002']):
        o += [mark(x, 130, S.INK, 7), name(x, 170, nm, anchor='middle', size=13), gloss(x, 192, d, anchor='middle')]
    o += [cut(xs[2] + 50, 130, 12), rule(f'M{xs[0]},230 H{xs[2]}', S.INK2, 1.0),
          art(xs[0], 224, 'matrículas · certidões de 2006', S.INK2),
          gloss(880, 100, 'ineficácia + arresto: perda iminente', col=S.CONC, anchor='end', size=13),
          gloss(xs[0], 290, 'Não era preciso aguardar o leilão.', col=S.INK, size=15)]
    return S.svg(900, 310, 'Cadeia de títulos de Onogás a Vandir e a constrição: REsp 1.332.112', o), []


def calendario():
    # One scale for both counts (8 px a day): the CC 445 / CDC 26 non-durable count stops at day 30; the CDC 26
    # durable count runs three thirty-day stretches to day 90. Counting only: no dates, no weekdays, no 365-day year.
    sc, x0 = 8, 40

    def ruler(y, n, label, sub):
        o = [S.path(f'M{x0},{y} H{x0 + n * sc}', fill='none', stroke=S.INK, stroke_width=1)]
        for d in range(0, n + 1):
            big = d % 10 == 0
            o.append(S.line(x0 + d * sc, y - (8 if big else 4), x0 + d * sc, y, stroke=S.INK2, stroke_width=1))
            if big and d:
                o.append(art(x0 + d * sc, y + 18, str(d), anchor='middle', size=11.5))
        o.append(cord(x0, x0 + n * sc, y - 18, amp=6, half=24, taper=30))
        o.append(cut(x0 + n * sc, y - 18, 14))
        return o
    o = ruler(96, 30, '', '')
    ex = x0 + 30 * sc
    o += [name(ex + 40, 66, 'CC 445 · móvel', size=12), gloss(ex + 40, 84, 'regra: entrega efetiva'),
          name(ex + 40, 112, 'CDC 26 · não durável', size=12), gloss(ex + 40, 130, 'aparente: entrega / fim do serviço')]
    o += ruler(236, 90, '', '')
    for k in range(3):
        a, b = x0 + k * 30 * sc + 3, x0 + (k + 1) * 30 * sc - 3
        o += [bracket(a, b, 272, up=False), gloss((a + b) / 2, 296, f'dias {k * 30 + 1} a {k * 30 + 30}', anchor='middle', size=13)]
    o += [name(x0, 176, 'CDC 26 · durável', size=12), gloss(x0 + 640, 176, 'No CDC, vício oculto: contar da evidência do defeito.', anchor='end', size=13)]
    return S.svg(820, 316, 'Contagem sem datas: trinta dias na escala, noventa em três trinta dias seguidos', o), []


def tally():
    # Instalments spend one price and the strip ends; each lease period frees one period only and the cord goes on.
    # Three schematic performances (CM par. 195), not facts of Vandir's transaction.
    x0, step = 300, 62
    y1, y2 = 100, 230
    o = [name(24, y1 + 5, 'Venda com preço parcelado', size=12.5), name(24, y2 + 5, 'Locação', size=12.5)]
    xe = x0 + 3 * step - 22
    o += [cord(x0 - 18, xe, y1, amp=6, half=24, taper=28), S.line(xe, y1 - 16, xe, y1 + 16, stroke=S.INK, stroke_width=3),
          gloss(xe + 22, y1 + 5, 'esgota o preço ajustado')]
    o += ['<g opacity="0.38">' + cord(x0 + 3 * step - 22, 846, y2, amp=6, half=24, taper=28) + '</g>',
          cord(x0 - 18, x0 + 3 * step - 22, y2, amp=6, half=24, taper=28)]
    for k in range(3):
        for y in (y1, y2):
            o.append(S.circle(x0 + k * step, y, 6.5, fill=S.INK, stroke=S.INK))
        o.append(bracket(x0 + k * step - 22, x0 + k * step + 22, y2 + 34, up=False))
    o.append(bracket(x0 - 22, x0 + 2 * step + 22, y1 + 34, up=False))
    for k in range(3, 8):
        o.append(S.circle(x0 + k * step, y2, 6.5, fill=S.PAPER, stroke=S.MUTED, stroke_width=1.5, opacity=str(max(0.3, 1 - (k - 3) * 0.14))))
    o.append(gloss(x0 + 3 * step, y2 - 22, 'o uso continua no período seguinte'))
    o.append(gloss(24, 316, 'Fracionar um preço e remunerar períodos de uso têm funções diferentes.', size=15, col=S.INK))
    return S.svg(870, 336, 'Parcelas esgotam o preço; os períodos de locação continuam', o), []


def garantia():
    # Three relations of the guarantee (CM §§207-211) as a triangle of marks; the twisted cords run along the
    # horizontals, hairlines drop the verticals.
    o = []
    X0, X1 = 130, 740
    for ident, x, y, label, sub, lines, cords in [
        ('utilidade', 130, 75, 'Utilidade', 'coisa adequada', ['M130,85 V220'], [(130, 432, 220)]),
        ('remedio', 440, 220, 'Remédio', 'restituir ou abater', ['M740,220 V85'], [(448, 740, 220)]),
        ('direito', 740, 75, 'Direito', 'título protegido', [], [(148, 730, 75)])]:
        o.append(f'<g data-thread="{ident}" data-fio="{ident}" tabindex="0" role="button" aria-label="Traçar {label}" aria-pressed="false">')
        o.append(S.rect(x - 70, y - 44, 140, 90, fill='none', pointer_events='all'))
        o += [tr(d, data_lk=ident) for d in lines]
        o += ['<g data-lk="%s">' % ident + cord(a, b, yy, amp=6.5, half=24, taper=30) + '</g>' for a, b, yy in cords]
        o += [mark(x, y, S.INK, 7), name(x, y - 20, label, anchor='middle', size=10.5), gloss(x + (14 if ident == 'utilidade' else -14 if ident == 'direito' else 0), y + 31, sub, anchor={'utilidade': 'start', 'direito': 'end'}.get(ident, 'middle'), size=11), '</g>']
    o += [gloss(440, 150, 'o alienante responde pela prestação transmitida', anchor='middle', size=11.5)]
    return S.svg(870, 280, 'Relações entre utilidade, remédio e direito garantido', o), []


def build(p):
    return {'campo':campo,'autos':autos,'calendario':calendario,'tally':tally,'garantia':garantia}[p.get('mode','campo')]()
