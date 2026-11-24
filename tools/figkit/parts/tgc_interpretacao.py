"""Interpretação contratual: three drawings tied to the assigned sources.

params: mode = execucao | rebanho | fecho.
execucao: party lanes (LANGUAGES 3), checkbox film supplied by the lesson.
Facts: TJSP AC 1000680 pp.14–16; no quantitative time scale.
rebanho: schematic object (language 16), Venosa p.64; animal count is not data.
fecho: branching decision ladder (language 4), CC113/423 and CDC46/47.
Paths have trace hooks; focuses and pointer traces are handled in the source.
All coordinates and animal placements derive from the object geometry.
"""
from . import svg as S


def sheep(x, y, scale=1, pregnant=False):
    shape = [S.path('M-30,0 C-45,-17 -31,-31 -16,-27 C-12,-43 10,-44 18,-29 C36,-34 46,-16 35,-5 C45,13 28,23 12,18 C-5,30 -31,20 -30,0 Z',
                    fill=S.PAPER, stroke=S.INK, stroke_width=1.7),
             S.path('M27,-14 Q51,-26 55,-10 L52,9 Q40,18 31,7 Z', fill=S.PAPER, stroke=S.INK, stroke_width=1.7),
             S.path('M-20,17 L-22,36 L-14,36 M15,18 L16,36 L24,36', fill='none', stroke=S.INK, stroke_width=2),
             S.circle(46,-5,1.8,fill=S.INK)]
    if pregnant:
        shape += [S.path('M-13,0 Q-12,-16 2,-13 Q13,-16 16,-4 Q13,10 1,9 Q-10,12 -13,0 Z',
                         fill='none', stroke=S.DIF, stroke_width=2, stroke_dasharray='3 2'),
                  S.path('M5,3 L8,13 M-6,3 L-5,13', fill='none', stroke=S.DIF, stroke_width=1.5)]
    return '<g transform="translate(%s %s) scale(%s)">%s</g>' % (x,y,scale,''.join(shape))


def build(p):
    mode=p.get('mode','rebanho')
    T=S.text
    if mode == 'execucao':
        out=[]
        for y, name in [(70,'Shirley'),(220,'André')]:
            out += [T(12,y+5,name,size=17,family=S.SERIF),
                    S.line(105,y,620,y,stroke=S.INK,stroke_width=1.4)]
        out += [S.line(210,35,210,250,stroke=S.MUTED,stroke_width=1,stroke_dasharray='3 5'),
                T(210,22,'celebração',size=13,anchor='middle'),
                T(224,56,'preço ligado à renovação',size=13,fill=S.INK2),
                S.circle(210,70,6,fill=S.PAPER,stroke=S.INK,stroke_width=2),
                S.circle(210,220,6,fill=S.PAPER,stroke=S.INK,stroke_width=2),
                T(385,290,'O negócio foi executado desde a celebração.',size=16,family=S.SERIF,anchor='middle')]
        out += ['<g class="execution-film">',
                S.path('M210,78 C210,155 285,140 285,212',fill='none',stroke=S.DIF,stroke_width=2.4),
                S.path('M278,204 L285,214 L292,204',fill='none',stroke=S.DIF,stroke_width=2),
                T(196,146,'administração e passivo',size=14,fill=S.DIF,anchor='end'),
                S.path('M450,212 C450,150 520,145 520,78',fill='none',stroke=S.DIF,stroke_width=2.4),
                S.path('M513,87 L520,77 L527,87',fill='none',stroke=S.DIF,stroke_width=2),
                T(532,150,'parcela do preço',size=14,family=S.SERIF,fill=S.DIF),
                S.line(285,220,620,220,stroke=S.DIF,stroke_width=3),
                T(605,249,'receitas recebidas',size=14,fill=S.DIF,anchor='end'),'</g>']
        return S.svg(650,315,'Atos de execução na cessão de quotas',out),[]
    if mode == 'rebanho':
        out=[S.path('M70,110 C70,20 510,15 562,106 C610,200 514,265 329,260 C127,275 32,206 70,110 Z',
                    fill='none',stroke=S.INK,stroke_width=1.5)]
        for x,y,k,pr in [(160,125,1.1,False),(335,107,1.2,True),(454,189,.9,False),(235,201,.9,False)]:
            out.append(sheep(x,y,k,pr))
        out += [T(320,25,'universalidade vendida',size=15,family=S.SANS,anchor='middle'),
                S.line(335,124,335,160,stroke=S.DIF,stroke_width=1.2),
                T(335,180,'crias concebidas',size=15,family=S.SERIF,anchor='middle',fill=S.DIF),
                T(320,304,'O particular desconhecido permanece dentro do objeto contratado.',size=17,family=S.SERIF,anchor='middle')]
        return S.svg(650,330,'Rebanho vendido e crias concebidas',out),[]
    if mode == 'integracao':
        # Two ruled sheets with the same hole: the gap is closed from inside the text, or from sources outside it.
        out=[]
        full=[1,.9,1,1,.86,.72,1,.58]
        def sheet(y0,fill_gap):
            o=[S.rect(20,y0,330,184,fill=S.PAPER,stroke=S.INK,stroke_width=1.2)]
            for i,k in enumerate(full):
                y=y0+20+i*20
                x2=36+286*k
                if 3<=i<=5:
                    o += fill_gap(i,y,x2)
                else:
                    o.append(S.line(36,y,x2,y,stroke=S.INK2,stroke_width=2.2))
            return o
        def inner(i,y,x2):
            return [S.line(36,y,x2,y,stroke=S.DIF,stroke_width=2.4,stroke_dasharray='6 4')]
        def outer(i,y,x2):
            return [S.line(36,y,x2,y,stroke=S.INK,stroke_width=3.2),
                    S.line(350,y,372,y,stroke=S.INK,stroke_width=1.6),
                    S.rect(372,y-4,8,8,fill=S.INK)]
        out += [T(20,22,'interpretação integrativa',size=15,family=S.SANS,weight='600')]
        out += sheet(32,inner)
        out += [S.path('M360,108 L366,108 L366,156 L360,156',fill='none',stroke=S.DIF,stroke_width=1.4),
                T(376,128,'ideia geral do contrato,',size=14,family=S.SERIF,fill=S.DIF),
                T(376,148,'boa-fé e o já cumprido',size=14,family=S.SERIF,fill=S.DIF)]
        out += [T(20,248,'integração',size=15,family=S.SANS,weight='600')]
        out += sheet(258,outer)
        for i,lab in zip((3,4,5),('normas supletivas','usos','equidade contratual')):
            out.append(T(390,258+20+i*20+5,lab,size=14,family=S.SERIF))
        return S.svg(650,452,'Lacuna fechada por dentro do texto e por fontes externas',out),[]
    if mode == 'fecho':
        # Each branch names its own legal condition; conditions can coexist.
        out=[S.circle(74,155,7,fill=S.PAPER,stroke=S.INK,stroke_width=2),
             T(62,177,'dúvida',size=15,family=S.SERIF,anchor='end')]
        for i,(test,result,article) in enumerate([
            ('não redator identificável','sentido mais benéfico','CC 113, § 1º, IV'),
            ('adesão + ambiguidade','favor ao aderente','CC 423'),
            ('relação de consumo','favor ao consumidor','CDC 47')]):
            y=48+i*108
            out += [f'<g data-thread="fundamento-{i}" tabindex="0" role="button" aria-label="{test}: {result}">',
                    S.path(f'M82,155 C118,155 100,{y} 143,{y} L600,{y}',fill='none',stroke=S.INK,stroke_width=1.7),
                    S.circle(145,y,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.5),
                    T(168,y-13,test,size=15,family=S.SANS),
                    S.rect(597,y-4,8,8,fill=S.DIF),
                    T(595,y+25,result,size=16,family=S.SERIF,fill=S.DIF,anchor='end'),
                    T(168,y+24,article,size=12,fill=S.INK2),'</g>']
        out += [S.line(45,315,605,315,stroke=S.CONC,stroke_width=1.5),
                T(45,344,'Conteúdo inacessível ou incompreensível: não obriga.',size=16,family=S.SERIF,fill=S.CONC),
                T(45,369,'CDC 46',size=12)]
        return S.svg(650,390,'Fundamentos distintos de proteção na interpretação',out),[]
    raise ValueError('mode must be execucao, rebanho, integracao or fecho')
