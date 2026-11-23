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


def calendario():
    o=[]
    for x,y,n,label in [(30,60,30,'30 dias'),(365,60,90,'90 dias')]:
        cols=10; cell=25; rows=(n+cols-1)//cols
        o += [txt(x,y-22,label,20,family=S.SERIF),
              S.line(x,y-8,x+250,y-8,stroke=S.INK)]
        for d in range(1,n+1):
            xx=x+(d-1)%cols*cell; yy=y+(d-1)//cols*cell
            o += [S.rect(xx,yy,cell,cell,fill='none',stroke=S.GRID),txt(xx+12.5,yy+17,str(d),11,anchor='middle')]
        o.append(S.rect(x+225,y+(rows-1)*cell,25,25,fill='none',stroke=S.CONC,stroke_width=2))
    o += [txt(30,170,'CC 445 · móvel',14),txt(30,198,'regra: entrega efetiva',14,family=S.SERIF),
          txt(30,241,'CDC 26 · não durável',14),txt(30,269,'aparente: entrega / fim do serviço',13,family=S.SERIF),
          txt(365,312,'CDC 26 · durável',14),
          txt(30,350,'No CDC, vício oculto: contar da evidência do defeito.',15,family=S.SERIF)]
    return S.svg(660,375,'Calendário sem datas: trinta e noventa dias contados individualmente',o),[]


def tally():
    o=[txt(24,27,'PRESTAÇÕES CUMPRIDAS',13,fill=S.MUTED)]
    for y,label,periodic in [(90,'Venda com preço parcelado',False),(210,'Locação',True)]:
        o += [txt(24,y-20,label,19,family=S.SERIF),S.line(24,y+14,828,y+14,stroke=S.GRID)]
        for k in range(3):
            x=350+k*65
            o += [S.circle(x,y,9,fill=S.INK,stroke=S.INK),S.line(x-13,y+26,x+13,y-26,stroke=S.INK,stroke_width=1.5)]
        if periodic:
            for k in range(3,7):o.append(S.circle(350+k*65,y,9,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
            o.append(txt(350,y+50,'o uso continua no período seguinte',14,family=S.SERIF))
        else:
            o += [S.line(510,y-27,510,y+27,stroke=S.INK,stroke_width=2),
                  txt(550,y+5,'esgota o preço ajustado',14,family=S.SERIF)]
    o.append(txt(24,313,'Fracionar um preço e remunerar períodos de uso têm funções diferentes.',15,family=S.SERIF))
    return S.svg(870,340,'Tally esquemático: preço que se exaure e uso que continua',o),[]


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
