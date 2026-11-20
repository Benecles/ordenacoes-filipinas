"""Aula 07: folio planta, dot tally and six-decision hemicycle.

params: mode = folio | atos | hemiciclo. All facts are fixed to this lesson's
assigned decisions; no invented votes, quantities or chronology. The folio's
clause is a spliced HTML source block over the empty document centre.
Desktop and phone versions use the same facts at legible native coordinates.
Folio extends the lesson planta's thread contract, replacing the railway form.
"""
from __future__ import annotations
from math import cos, sin, radians
from . import svg as S


def paired(large, small):
    return '<div class="tgc07-large">' + large + '</div><div class="tgc07-small">' + small + '</div>'


def folio(phone=False):
    w,h = (340,510) if phone else (1040,360)
    x,y,pw,ph = (10,8,320,312) if phone else (264,20,510,305)
    o=[S.rect(x,y,pw,ph,fill=S.PAPER2,stroke=S.INK,stroke_width=1.1),
       S.line(x+16,y+35,x+pw-16,y+35,stroke=S.GRID,stroke_width=1),
       S.text(x+20,y+23,'CLÁUSULA TERCEIRA · TJSP',size=12)]
    # The square marks and marginal circuits identify the exact portion governed.
    specs=[('intencao','art. 112','intenção declarada'),('conjunto','art. 113','conjunto e execução'),('limite','art. 114','limite às liberalidades')]
    for i,(key,law,note) in enumerate(specs):
        if phone:
            gy=365+i*53; gx=28
            d=f'M{gx}, {gy-20} V{gy-31} H{310-i*14} V{324-i*12}'
        else:
            gx=18 if i<2 else 810; gy=105+i*112 if i<2 else 192
            edge=x if i<2 else x+pw
            d=f'M{gx+190 if i<2 else gx-10},{gy+7} H{edge-24 if i<2 else edge+24} V{y+75+i*80} H{edge}'
        tone=S.CONC if i==2 else S.INK
        o.append(f'<g data-thread="{key}" tabindex="0" role="link" aria-label="{S.esc(law+": "+note)}" data-fio="{key}">')
        o += [S.path(d,fill='none',stroke=tone,stroke_width=1.2),
              S.circle(gx,gy,4,fill=S.PAPER,stroke=tone,stroke_width=1.2),
              S.text(gx+12,gy+4,law,size=12.5),
              S.text(gx+12,gy+24,note,size=12.5,family=S.SERIF,fill=tone),
              S.rect(x-3 if i<2 else x+pw-3,y+72+i*80,6,6,fill=S.PAPER,stroke=tone,stroke_width=1.2)]
        o.append('</g>')
    return S.svg(w,h,'Planta da leitura: uma cláusula glosada pelos arts. 112 a 114',o)


def atos(phone=False):
    w,h=(340,290) if phone else (650,240)
    o=[S.text(12,25,'ATOS DE EXECUÇÃO',size=13),S.text(w-12,25,'4 registros',size=12,anchor='end')]
    names=['Administração assumida','Passivo assumido','Primeira parcela paga','Receitas recebidas']
    for i,name in enumerate(names):
        y=68+i*(56 if phone else 44)
        # Every dot denotes one kind of act, not frequency or strength of proof.
        o += [S.circle(25,y-5,5,fill=S.INK),S.text(45,y,name,size=15,family=S.SERIF),
              S.line(12,y+17,w-12,y+17,stroke=S.GRID,stroke_width=1)]
    return S.svg(w,h,'Quatro atos registrados no contrato de cessão de quotas',o)


def hemiciclo(phone=False):
    w,h=(340,420) if phone else (980,410)
    cx,cy=(170,200) if phone else (490,280)
    rx,ry=(135,160) if phone else (320,200)
    o=[]
    for factor in [1,.79]:
        o.append(S.path(f'M{cx-rx*factor},{cy} A{rx*factor},{ry*factor} 0 0 1 {cx+rx*factor},{cy}',fill='none',stroke=S.GRID,stroke_width=1))
    data=[('AR 7.296','letra mantida','intencao'),('REsp 1.013.976','nome insuficiente','intencao'),('REsp 1.938.997','liberalidade limitada','criterios'),('REsp 15.339','todo qualificado','qualificacao'),('AC 1000680','execução confirma','criterios'),('AREsp 1.679.541','prova preservada','criterios')]
    for i,(case,meaning,target) in enumerate(data):
        angle=180-i*36
        x=cx+rx*cos(radians(angle)); y=cy-ry*sin(radians(angle))
        o.append(f'<a tabindex="0" data-thread="caso-{i}" href="#{target}" aria-label="{S.esc(case+": "+meaning)}">')
        o += [S.circle(x,y,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.5)]
        if not phone:
            if i in (1,4):
                # outside the whole arc's box, led by a rule from its dot, so no label straddles the figure's edge
                side=-1 if i==1 else 1
                tx=cx+side*(rx+14); ty=y-2
                o += [S.line(x+side*9,y,tx-side*4,y,stroke=S.MUTED,stroke_width=.8),S.text(tx,ty-24,case,size=13,anchor='end' if i==1 else 'start'),S.text(tx,ty-2,meaning,size=15,anchor='end' if i==1 else 'start',family=S.SERIF)]
            else:
                ty=335 if i in (0,5) else 36
                o += [S.line(x,y-9 if i in (2,3) else y+9,x,ty+32 if i in (2,3) else ty-21,stroke=S.MUTED,stroke_width=.8),S.text(x,ty,case,size=13,anchor='middle'),S.text(x,ty+22,meaning,size=15,anchor='middle',family=S.SERIF)]
        else:
            # Six numbered positions point to a readable key under the hemicycle.
            o.append(S.text(x,y-12,str(i+1),size=12,anchor='middle'))
        o.append('</a>')
    o += [S.text(cx,cy-45,'DECLARAÇÃO',size=13,anchor='middle'),S.text(cx,cy-23,'lida nas circunstâncias',size=14,anchor='middle',family=S.SERIF)]
    if phone:
        for i,(case,meaning,target) in enumerate(data):
            o.append(f'<a href="#{target}">')
            o.append(S.text(8,250+i*27,f'{i+1}  {case} · {meaning}',size=12,family=S.SERIF));o.append('</a>')
    return S.svg(w,h,'Seis julgados em torno da declaração: fundamentos distintos de leitura, sem contagem de votos',o)


def build(p: dict) -> tuple[str,list[dict]]:
    fn={'folio':folio,'atos':atos,'hemiciclo':hemiciclo}[p['mode']]
    return paired(fn(),fn(True)),[]
