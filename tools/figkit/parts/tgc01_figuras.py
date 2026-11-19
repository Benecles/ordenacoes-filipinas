"""Conceito de contrato: semantic drawings from the assigned local sources.

params:
  mode: 'vontades' | 'historia' | 'partes' | 'cobertura' | 'tipo' | 'planos'
No numeric quantity is asserted except the count of wills/centres. Paths show
logical inclusion or convergence, never money or elapsed years. historia uses
ordering, not a timeline scale. cobertura uses the categories expressly reported
in REsp 1.176.019 (local STJ reading, p.4); the enclosing contour is schematic.
Languages: party lanes; genealogy of enforceability; party seating; tracing film;
typological field. All static renderings are objects or measures; interactive
responses are supplied by the host page and keyboard accessible controls.
"""
from . import svg as S

def build(p):
    mode=p['mode'];o=[];T=S.text
    def tx(x,y,t,**k):o.append(T(x,y,t,size=k.pop('size',17),family=k.pop('family',S.SERIF),**k))
    def ln(x,y,a,b,**k):o.append(S.line(x,y,a,b,stroke=k.pop('stroke',S.INK),stroke_width=k.pop('stroke_width',1.5),**k))
    if mode=='vontades':
        w,h=600,260
        tx(30,27,'Duas manifestações',family=S.SANS,weight='600')
        for y,label in [(77,'doador'),(155,'donatário')]:
            o.append(S.circle(45,y,7,fill=S.PAPER,stroke=S.INK,stroke_width=2))
            tx(65,y-14,label)
            o.append(S.path(f'M52,{y} H194 Q242,{y} 277,116 H540',fill='none',stroke=S.INK,stroke_width=2))
        o.append(S.circle(277,116,8,fill=S.PAPER,stroke=S.INK,stroke_width=2))
        tx(294,101,'acordo',family=S.SANS)
        ln(45,206,540,206,stroke=S.DIF,stroke_width=2.5)
        o.append(S.path('M528,198 L540,206 L528,214',fill='none',stroke=S.DIF,stroke_width=2))
        tx(45,238,'Uma prestação: do patrimônio de quem doa ao de quem recebe',size=16)
    elif mode=='historia':
        w,h=700,320
        # Many distinct action lines develop into a common stem. No boxes.
        for i,(name,sub) in enumerate([('verbis','palavras'),('litteris','inscrição'),('re','entrega'),('consensu','quatro tipos')]):
            y=48+i*59
            tx(20,y-8,name,size=18,family=S.SANS,weight='600')
            tx(20,y+13,sub,size=15)
            ln(145,y,280,y,stroke_width=2)
            o.append(S.circle(145,y,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
            o.append(S.path(f'M280,{y} C350,{y} 340,135 410,135 H650',fill='none',stroke=S.INK,stroke_width=1.6))
        ln(410,113,410,158,stroke_width=2.5)
        tx(430,103,'generalização do consenso',size=18)
        tx(432,173,'palavra vinculante',size=16)
        ln(145,286,650,286,stroke=S.CONC,stroke_dasharray='5 5')
        tx(20,291,'pacto',size=18)
        tx(303,274,'exceção defensiva sem ação própria',size=16,fill=S.CONC)
    elif mode=='partes':
        w,h=600,280
        for j,(cx,n,label) in enumerate([(155,3,'uma parte'),(448,1,'outra parte')]):
            o.append(S.circle(cx,116,81,fill='none',stroke=S.INK,stroke_width=1.6))
            for i in range(n):
                x=cx+(i-(n-1)/2)*40
                o.append(S.circle(x,108,10,fill=S.PAPER,stroke=S.INK,stroke_width=1.6))
                o.append(S.path(f'M{x-13},140 Q{x},118 {x+13},140',fill='none',stroke=S.INK,stroke_width=1.6))
            tx(cx,230,label,anchor='middle',family=S.SANS,weight='600')
        ln(236,116,367,116,stroke_width=2)
        tx(300,93,'acordo',anchor='middle')
        tx(300,269,'Quatro pessoas · dois centros de interesses',anchor='middle',size=16)
    elif mode=='cobertura':
        w,h=640,310
        # A cut tracing sheet: the intersection carries legal meaning without words.
        o.append(S.path('M22,32 H610 V273 H22 Z',fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
        for y in [63,242]:
            o.append(S.circle(38,y,4,fill='none',stroke=S.MUTED,stroke_width=1))
        tx(66,61,'Recorte da cobertura de lucros cessantes',family=S.SANS,weight='600')
        o.append(S.path('M82,92 H470 V223 H82 Z',fill='none',stroke=S.DIF,stroke_width=2.5))
        for i,lab in enumerate(['táxi','lotação','van escolar','motoboy']):
            x=127+i*94
            ln(x,118,x,182,stroke=S.INK,stroke_width=2)
            o.append(S.circle(x,158,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
            tx(x,205,lab,size=14,anchor='middle')
        o.append('<g data-cobertura-mark="">'+S.circle(552,158,18,fill='none',stroke=S.CONC,stroke_width=2.3)+S.path('M541,147 L563,169 M541,169 L563,147',fill='none',stroke=S.CONC,stroke_width=1.5,data_cobertura_cross='')+T(552,114,'terceiro',size=16,family=S.SERIF,anchor='middle')+'</g>')
        tx(66,294,'REsp 1.176.019 · contorno esquemático, sem escala',size=15,fill=S.INK2)
    elif mode=='tipo':
        w,h=600,280
        # Nested spheres: supplier is a fixed endpoint, professional role varies.
        o.append(S.circle(320,133,104,fill='none',stroke=S.INK,stroke_width=1.7))
        o.append(S.circle(320,133,57,fill='none',stroke=S.DIF,stroke_width=2))
        tx(320,138,'art. 2º',anchor='middle',family=S.SANS,size=19)
        tx(320,218,'destinação final',anchor='middle',size=16)
        ln(50,133,216,133,stroke_width=2)
        o.append(S.circle(50,133,7,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
        tx(12,103,'fornecedor',size=17)
        o.append(S.path('M424,133 H555 M474,125 L482,133 L474,141',fill='none',stroke=S.CONC,stroke_width=1.8,stroke_dasharray='4 4'))
        tx(477,94,'art. 29',size=17)
        tx(439,177,'exposição',size=16)
        tx(439,201,'e vulnerabilidade',size=16)
        tx(42,270,'Os círculos delimitam regimes; suas áreas não medem pessoas.',size=15,fill=S.INK2)
    elif mode=='planos':
        w,h=780,300
        # Three planes as three gates on one line; the line is a negócio travelling through them (Venosa p.51; CC arts. 104, 125).
        gx=[150,390,630]
        ln(40,120,740,120,stroke=S.INK,stroke_width=3)
        o.append(S.path('M392,120 H628',fill='none',stroke=S.PAPER,stroke_width=5))
        ln(396,120,626,120,stroke=S.CONC,stroke_width=3,stroke_dasharray='7 6')
        ln(634,120,740,120,stroke=S.DIF,stroke_width=3.5)
        o.append(S.circle(40,120,7,fill=S.INK,stroke=S.INK))
        for x,n,sub in zip(gx,['existir','valer','produzir efeitos'],['declaração das vontades','art. 104','']):
            ln(x,74,x,166,stroke=S.INK,stroke_width=2.5)
            tx(x,56,n,anchor='middle',family=S.SANS,weight='600',size=18)
            if sub: tx(x if x!=390 else 398,190,sub,anchor='middle' if x!=390 else 'start',size=15,fill=S.INK2)
        # art. 104: three requirements as three ticks on the validity gate
        for i,lab in enumerate(['agente capaz','objeto lícito','forma']):
            y=214+i*24
            ln(366,y-5,390,y-5,stroke=S.INK,stroke_width=1.4)
            tx(398,y,lab,size=15,fill=S.INK2)
        # defective at validity: leaves the line downward
        o.append(S.path('M390,126 C378,168 318,176 296,238',fill='none',stroke=S.CONC,stroke_width=2,stroke_dasharray='3 4'))
        tx(292,260,'inválido',size=16,anchor='end',fill=S.CONC)
        tx(510,100,'condição suspensiva',anchor='middle',size=16,fill=S.CONC)
        tx(690,100,'efeito',anchor='middle',size=16,fill=S.DIF)
    else: raise ValueError(mode)
    return S.svg(w,h,'Conceito de contrato: '+mode,o),[]
