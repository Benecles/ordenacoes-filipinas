"""Aula 05: exchange record, fishing net, delivery and the horse's intended use.
Sources: Pereira III pp.59-60; Venosa pp.34,116,119. Marks are schematic,
not amounts, measured trajectories, or additional facts about Vandir.
"""
from . import svg as S

def t(x,y,s,size=18,**kw):
    return S.text(x,y,s,size=size,family=S.SERIF,**kw)

def line(x,y,a,b,**kw):
    return S.line(x,y,a,b,stroke=S.INK,stroke_width=1.5,**kw)

def exchange():
    # Account-book language: cancellation of the return entry carries the
    # difference even without words. No fictitious price or money count.
    o=[S.rect(24,24,592,312,fill=S.PAPER2,stroke=S.INK),line(320,24,320,336),
       t(48,59,'Vantagem recebida'),t(345,59,'Encargo em troca')]
    for y,label,returning in [(128,'Compra e venda',True),(250,'Doação pura',False)]:
        o += [line(24,y+54,616,y+54), t(48,y-34,label,17),
              S.path(f'M65,{y} h170 m-15,-6 l15,6 l-15,6',fill='none',stroke=S.INK,stroke_width=2)]
        if returning:
            o += [S.path(f'M555,{y} H385 m15,-6 l-15,6 l15,6',fill='none',stroke=S.DIF,stroke_width=2)]
        else:
            o += [line(385,y,555,y,stroke_dasharray='3 6'),S.path(f'M456,{y-16} l28,32 m-28,0 l28,-32',fill='none',stroke=S.CONC,stroke_width=2)]
    return S.svg(640,360,'Registro de vantagem e encargo: retorno na venda, sem contraprestação na doação pura',o),[]

def net(state):
    o=[t(24,35,{'hope':'Esperança · sem captura','empty':'Coisa esperada · sem captura','catch':'Coisa esperada · captura escassa'}[state])]
    # A net: mouth and pouch carry the captured quantity, not a label card.
    o += [S.path('M65,95 Q225,65 385,95 L340,270 Q225,330 110,270 Z',fill='none',stroke=S.INK,stroke_width=2)]
    for k in range(1,8):
        x=65+k*40
        o += [S.path(f'M{x},92 Q225,180 {130+k*23},282',fill='none',stroke=S.GRID,stroke_width=1)]
    for y,w in [(132,145),(172,135),(212,124),(252,112)]:
        o += [S.path(f'M{225-w},{y} Q225,{y+25} {225+w},{y}',fill='none',stroke=S.GRID,stroke_width=1)]
    if state=='catch':
        o += [S.path('M190,247 Q220,225 247,247 Q220,269 190,247 L176,235 V259 Z',fill=S.PAPER,stroke=S.DIF,stroke_width=2),S.circle(237,245,2,fill=S.INK)]
    color=S.CONC if state=='empty' else S.DIF
    o += [line(55,348,395,348), t(55,382,'Preço integral' if state!='empty' else 'Preço restituído',19,fill=color)]
    if state=='empty':
        o += [S.path('M55,332 L395,364 M55,364 L395,332',fill='none',stroke=color,stroke_width=2)]
    else:
        o += [S.path('M55,340 L66,352 L90,326',fill='none',stroke=color,stroke_width=3)]
    o += [t(24,424,'Sem culpa do alienante.',16)]
    return S.svg(450,450,'Rede de pesca e efeito da captura sobre o preço contratado',o),[]

def delivery():
    # The same unparticularised thing passes from promised (dotted) to
    # delivered (solid); the separating edge is the point of constitution.
    o=[t(24,35,'Comodato · entrega constitutiva'),line(300,75,300,285,stroke_dasharray='3 6')]
    for x,dashed in [(95,True),(385,False)]:
        o += [S.path(f'M{x},135 l70,-25 l75,30 v90 l-70,25 l-75,-30 Z M{x},135 l75,30 l70,-25 M{x+75},165 v90',fill='none',stroke=S.INK,stroke_width=2,**({'stroke_dasharray':'5 6'} if dashed else {}))]
    o += [t(40,315,'Promessa de emprestar',18),t(360,315,'Coisa entregue',18,fill=S.DIF),
          t(40,350,'Ainda sem comodato',17,fill=S.CONC),t(360,350,'Contrato formado',17,fill=S.DIF)]
    return S.svg(640,380,'A promessa precede a entrega; a entrega constitui o comodato',o),[]

def horse():
    # Literal object of the example in Venosa p.119. No diagnostic anatomy.
    o=[t(24,36,'Cavalo destinado à corrida'),
       S.path('M120,175 Q155,125 265,150 L303,90 L335,75 L355,108 L335,152 L310,155 L300,205 L275,238 L270,302 L253,302 L246,226 L195,226 L166,300 L149,300 L156,218 L131,204 L102,260 L87,253 L108,208 Z',fill=S.PAPER2,stroke=S.INK,stroke_width=2),
       S.path('M120,175 Q65,142 67,221',fill='none',stroke=S.INK,stroke_width=3),
       S.path('M340,166 Q375,154 394,168 M348,184 Q376,172 394,186',fill='none',stroke=S.CONC,stroke_width=2,stroke_dasharray='6 7'),
       t(24,344,'Moléstia respiratória',18,fill=S.CONC),t(24,378,'A finalidade da aquisição fica comprometida.',16)]
    return S.svg(450,405,'O cavalo e o problema respiratório que compromete a finalidade da aquisição',o),[]

def build(p):
    mode=p.get('mode','exchange')
    if mode=='net':return net(p['state'])
    return {'exchange':exchange,'delivery':delivery,'horse':horse}[mode]()
