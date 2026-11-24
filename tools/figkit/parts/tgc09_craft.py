"""Aula 09: cause families and successive powers under CC 478–480.
Causes: Venosa pp. 68–70, 73 and Luis Renato pp. 13, 29–30.
Powers: CC 478–480. Coordinates categorical; no numerical scale.
"""
from . import svg as S

def build(p):
    t=S.text; out=[]
    if p.get('mode') == 'causas':
        out += [S.path('M32,185 L180,185 C220,185 220,100 270,100 L420,100 M180,185 C220,185 220,280 270,280 L420,280',fill='none',stroke=S.INK,stroke_width=1.6)]
        for y,ends in [(100,[45,155]),(280,[245,350])]:
            for end in ends:
                out.append(S.path(f'M420,{y} C465,{y} 465,{end} 515,{end}',fill='none',stroke=S.INK,stroke_width=1.6))
        out += [t(38,168,'programa contratual',size=15,family=S.SERIF),t(260,78,'na formação',size=18,family=S.SERIF),t(260,258,'na execução',size=18,family=S.SERIF)]
        for y,label in [(45,'cláusula abusiva'),(155,'lesão'),(245,'imprevisão'),(350,'quebra da base')]:
            out += [S.circle(515,y,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.7),t(535,y+6,label,size=18,family=S.SERIF)]
        return S.svg(820,380,'Famílias de causas: vícios da formação e alterações na execução',out),[]
    state=int(p.get('state',1))
    cols=[(145,'resolver','478'),(255,'modificar','479'),(365,'reduzir','480')]
    for x,label,article in cols:
        out += [t(x,36,label,size=17,anchor='middle',family=S.SERIF),t(x,63,'art. '+article,size=14,anchor='middle'),S.line(x,85,x,264,stroke=S.GRID)]
    for y,label in [(140,'devedor'),(235,'réu')]:
        out += [t(12,y+6,label,size=17,family=S.SERIF),S.line(100,y,412,y,stroke=S.GRID)]
    marks=[(145,140),(255,235),(365,140)]
    for i,(x,y) in enumerate(marks,1):
        out.append(S.circle(x,y,12,fill=S.DIF if i==state else S.PAPER,stroke=S.DIF if i==state else S.MUTED,stroke_width=2))
    labels={1:['O devedor pede','a resolução.'],2:['O réu oferece a mudança','para conservar o contrato.'],3:['Só uma parte deve: redução','ou novo modo de execução.']}
    for i,line in enumerate(labels[state]):out.append(t(220,298+i*26,line,size=17,family=S.SERIF,anchor='middle',fill=S.DIF))
    return S.svg(440,340,'Titular do remédio: '+ ' '.join(labels[state]),out),[]
