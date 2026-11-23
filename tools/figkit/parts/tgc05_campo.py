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


def txt(x, y, s, size=13, **kw):
    return S.text(x, y, s, size=size, **kw)


def wire(d, color=S.INK, **kw):
    return S.path(d, fill='none', stroke=color, stroke_width=1.5, **kw)


def campo():
    # Field: columns = vantagem (gratuito | oneroso), rows = prestacao (certa | alea contratada).
    # Each contract drops onto the rails (regimes) it switches on; junction dots mark the connections.
    rails = {'estrita': 460, 'vicios': 340, 'eviccao': 380, 'alea': 420}
    o = [txt(20, 24, 'PRESTAÇÃO', 11.4, fill=S.MUTED), txt(170, 24, 'VANTAGEM', 11.4, fill=S.MUTED),
         txt(170, 58, 'gratuito', 17, family=S.SERIF), txt(360, 58, 'oneroso', 17, family=S.SERIF),
         S.line(345, 40, 345, 290, stroke=S.MUTED, stroke_dasharray='3 5'),
         S.line(20, 165, 830, 165, stroke=S.GRID),
         txt(20, 108, 'comutativo', 12), txt(20, 128, 'prestação certa', 11.4, fill=S.INK2),
         txt(20, 228, 'aleatório', 12), txt(20, 248, 'incerteza contratada', 11.4, fill=S.INK2)]
    for ident, x, y, label, note, to in [
        ('doacao', 185, 108, 'Doação pura', 'sem contraprestação', ['estrita']),
        ('lotes', 380, 108, 'Lotes de Vandir', 'preço e lotes definidos', ['vicios', 'eviccao']),
        ('capital', 610, 108, 'Integralização', 'imóvel por quotas', ['vicios', 'eviccao']),
        ('swap', 440, 228, 'Swap', 'oscilação assumida', ['eviccao', 'alea']),
        ('loteria', 660, 228, 'Projeto de loteria', 'remuneração incerta', ['eviccao', 'alea'])]:
        o.append(f'<g data-thread="{ident}" data-fio="{ident}" tabindex="0" role="button" aria-label="Traçar {label}" aria-pressed="false">')
        o += [S.rect(x-15, y-24, 215, 64, fill='none', pointer_events='all'),
              wire(f'M{x},{y+7} V{max(rails[r] for r in to)}', data_lk=ident)]
        for r in to:
            o += [wire(f'M{x},{rails[r]} H852', data_lk=ident),
                  S.circle(x, rails[r], 3.5, fill=S.INK, stroke=S.INK, data_lk=ident)]
        o += [S.circle(x, y, 6, fill=S.PAPER, stroke=S.INK, stroke_width=1.7),
              txt(x+15, y+5, label, 12.5, family=S.SANS),
              txt(x+15, y+27, note, 11.4, fill=S.INK2), '</g>']
    for r, a, b in [('vicios', 'vícios redibitórios', 'utilidade da coisa'),
                    ('eviccao', 'evicção', 'direito transmitido'),
                    ('alea', 'álea assumida', 'resultado suportado'),
                    ('estrita', 'interpretação estrita', 'benefício não se amplia')]:
        y = rails[r]
        o += [S.rect(852, y-4, 8, 8, fill=S.PAPER, stroke=S.INK),
              txt(876, y+1, a, 12), txt(876, y+17, b, 11.4, fill=S.INK2)]
    return S.svg(1060, 492, 'Campo de vantagem e prestação; traçar cada contrato até os regimes que ele aciona', o), []


def autos():
    o = []
    # Layering means successive documentary titles; thickness is not a count.
    for x,y,w in [(40,75,570),(32,87,570),(24,99,570)]:
        o += [S.rect(x,y,w,175,fill=S.PAPER,stroke=S.INK2,stroke_width=1),
              S.line(x+12,y+165,x+w-12,y+165,stroke=S.GRID)]
    for y, name, detail in [(106,'Onogás','proprietária anterior'),(154,'Philips','alienante'),(202,'Vandir','adquirente em 2002')]:
        o += [S.path(f'M640,{y} H832 L820,{y+30} H640 Z',fill=S.PAPER,stroke=S.INK,stroke_width=1.3),
              txt(660,y+21,name,15,family=S.SANS),txt(70,y+22,detail,14,family=S.SERIF)]
    o += [wire('M48,75 V44 H540 V75',S.CONC),
          txt(55,30,'EXECUÇÃO FISCAL · vício anterior à compra',13),
          wire('M70,264 H567 V294',S.CONC),
          txt(70,256,'Certidões das matrículas · 2006',15,family=S.SERIF),
          txt(566,318,'ineficácia das alienações + arresto',14,anchor='middle',fill=S.CONC),
          txt(36,350,'Perda iminente já afeta o direito de Vandir.',15,family=S.SERIF)]
    return S.svg(850,370,'Autos da cadeia de aquisições e constrição: REsp 1.332.112',o),[]


def _sheet(x, y, title, first, cell=22, mark=None, ghost=False):
    """One tear-off page of a day pad: rings, header, perforation, ten columns of days.
    first = number of the page's first day; mark = day number that carries the limit (orange)."""
    w, hh, rows = cell * 10 + 28, 36, 3
    h = hh + 10 + rows * cell + 14
    o = [S.rect(x + 9, y + 9, w, h, fill=S.PAPER, stroke=S.GRID, stroke_width=1),
         S.rect(x + 4.5, y + 4.5, w, h, fill=S.PAPER, stroke=S.GRID, stroke_width=1),
         S.rect(x, y, w, h, fill=S.PAPER2, stroke=S.INK, stroke_width=1.4)]
    for k in range(5):
        o.append(S.circle(x + w * (k + 1) / 6, y + 9, 3.2, fill=S.PAPER, stroke=S.INK, stroke_width=1.3))
    o += [txt(x + 14, y + 29, title, 17, family=S.SERIF),
          S.line(x + 6, y + hh, x + w - 6, y + hh, stroke=S.INK2, stroke_width=1, stroke_dasharray='2 4')]
    gx, gy = x + 14, y + hh + 10
    for d in range(30):
        cx, cy = gx + d % 10 * cell, gy + d // 10 * cell
        n = first + d
        o.append(S.rect(cx, cy, cell, cell, fill='none', stroke=S.GRID, stroke_width=1))
        if mark == n:
            o += [S.rect(cx + 1.5, cy + 1.5, cell - 3, cell - 3, fill=S.CONC, stroke=S.CONC),
                  txt(cx + cell / 2, cy + cell - 6.5, str(n), 12, anchor='middle', fill=S.PAPER)]
        else:
            o.append(txt(cx + cell / 2, cy + cell - 6.5, str(n), 12, anchor='middle', fill=S.INK2 if ghost else S.INK))
    return o, (gx, gy, w, h)


def calendario():
    # Two pad pages of thirty days (CC 445 / CDC 26 non-durable) against three pages in a row (CDC 26 durable).
    # Counting only: no dates, no weekdays, no 365-day year.
    o, (gx, gy, w, h) = _sheet(36, 28, '30 dias', 1, mark=30)
    cell = 22
    ex, ey = gx + 9 * cell + cell, gy + 2 * cell + cell / 2          # right edge of day 30
    lead = 318
    for yy, a, b in [(ey - 42, 'CC 445 · móvel', 'regra: entrega efetiva'),
                     (ey + 16, 'CDC 26 · não durável', 'aparente: entrega / fim do serviço')]:
        o += [S.line(ex + 6, ey, lead - 10, yy - 5, stroke=S.INK2, stroke_width=1),
              S.circle(lead - 10, yy - 5, 3, fill=S.PAPER, stroke=S.INK, stroke_width=1.3),
              txt(lead + 4, yy, a, 14), txt(lead + 4, yy + 21, b, 13, family=S.SERIF)]
    top = 218
    o += [txt(36, top - 2, '90 dias', 20, family=S.SERIF), txt(150, top - 2, 'CDC 26 · durável', 14, fill=S.INK2),
          S.line(36, top + 8, 784, top + 8, stroke=S.INK, stroke_width=1)]
    for k in range(3):
        s_, _ = _sheet(36 + k * 252, top + 24, f'dias {k * 30 + 1} a {k * 30 + 30}', k * 30 + 1,
                       mark=90 if k == 2 else None, ghost=k < 2)
        o += s_
    o.append(txt(36, 436, 'No CDC, vício oculto: contar da evidência do defeito.', 15, family=S.SERIF))
    return S.svg(820, 452, 'Calendário sem datas: trinta dias em uma folha, noventa em três folhas contadas dia a dia', o), []


def _stub(x, y, spent=True, w=58, h=44, fade=1.0):
    if spent:
        o = [S.rect(x, y - h / 2, w, h, fill=S.PAPER2, stroke=S.INK, stroke_width=1.6),
             S.line(x + w - 13, y - h / 2, x + w - 13, y + h / 2, stroke=S.INK2, stroke_width=1.1, stroke_dasharray='2 3'),
             S.circle(x + 15, y, 5.5, fill=S.INK, stroke=S.INK),
             S.line(x + 28, y - 6, x + w - 20, y - 6, stroke=S.GRID, stroke_width=1.4),
             S.line(x + 28, y + 6, x + w - 20, y + 6, stroke=S.GRID, stroke_width=1.4)]
    else:
        o = [S.rect(x, y - h / 2, w, h, fill='none', stroke=S.MUTED, stroke_width=1.5, stroke_dasharray='5 4', opacity=str(fade)),
             S.line(x + w - 13, y - h / 2, x + w - 13, y + h / 2, stroke=S.MUTED, stroke_width=1, stroke_dasharray='2 3', opacity=str(fade)),
             S.circle(x + 15, y, 5.5, fill='none', stroke=S.MUTED, stroke_width=1.4, opacity=str(fade))]
    return o


def tally():
    # A stub book. Sale in instalments: one price, three stubs spend it, the strip ends.
    # Lease: each stub frees one period only; the book keeps going. Three schematic performances (CM par. 195).
    o = [txt(24, 27, 'PRESTAÇÕES CUMPRIDAS', 13, fill=S.MUTED)]
    x0, step = 300, 62
    y1, y2 = 98, 246
    o += [txt(24, y1 - 18, 'Venda com preço parcelado', 19, family=S.SERIF), S.line(24, y1 + 52, 846, y1 + 52, stroke=S.GRID),
          txt(24, y2 - 18, 'Locação', 19, family=S.SERIF), S.line(24, y2 + 52, 846, y2 + 52, stroke=S.GRID)]
    for k in range(3):
        o += _stub(x0 + k * step, y1)
    xe = x0 + 3 * step - 2
    o += [S.line(xe, y1 - 30, xe, y1 + 30, stroke=S.INK, stroke_width=3),
          S.path(f'M{x0},{y1 + 32} V{y1 + 38} H{xe - 6} V{y1 + 32}', fill='none', stroke=S.INK2, stroke_width=1.3),
          txt(xe + 30, y1 + 5, 'esgota o preço ajustado', 14, family=S.SERIF)]
    for k in range(3):
        o += _stub(x0 + k * step, y2)
        o.append(S.path(f'M{x0 + k * step + 2},{y2 + 32} V{y2 + 38} H{x0 + k * step + 54} V{y2 + 32}',
                        fill='none', stroke=S.INK2, stroke_width=1.3))
    for k in range(3, 9):
        o += _stub(x0 + k * step, y2, spent=False, fade=max(0.25, 1 - (k - 3) * 0.12))
    o.append(txt(x0 + 3 * step + 4, y2 - 32, 'o uso continua no período seguinte', 14, family=S.SERIF))
    o.append(txt(24, 335, 'Fracionar um preço e remunerar períodos de uso têm funções diferentes.', 15, family=S.SERIF))
    return S.svg(870, 352, 'Livro de recibos: o preço parcelado se exaure; os períodos de locação continuam', o), []


def garantia():
    o=[]
    for ident,x,y,label,sub,d in [
        ('utilidade',130,75,'Utilidade','coisa adequada','M130,85 V220 H440'),
        ('remedio',440,225,'Remédio','restituir ou abater','M450,225 H740 V85'),
        ('direito',740,75,'Direito','título protegido','M730,75 H140')]:
        o += [f'<g data-thread="{ident}" data-fio="{ident}" tabindex="0" role="button" aria-label="Traçar {label}" aria-pressed="false">',
              wire(d,data_lk=ident),S.circle(x,y,8,fill=S.PAPER,stroke=S.INK,stroke_width=1.5),
              txt(x,y-23,label,13.5,anchor='middle',family=S.SERIF),
              txt(x,y+33,sub,11,anchor='middle',fill=S.INK2),'</g>']
    o += [txt(440,122,'GARANTIA',11,anchor='middle'),txt(440,148,'o alienante responde pela prestação transmitida',11,anchor='middle',family=S.SERIF)]
    return S.svg(870,290,'Relações entre utilidade, remédio e direito garantido',o),[]


def build(p):
    return {'campo':campo,'autos':autos,'calendario':calendario,'tally':tally,'garantia':garantia}[p.get('mode','campo')]()
