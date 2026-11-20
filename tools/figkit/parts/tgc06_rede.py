"""Network of contracts cited in REsp764901/RJ pp.6–9.

Language 16: student's relational sketch, distinct contract marks around one
shopping. Not a floor plan or a statement that the two cases are the same.
Params: mobile (bool, default False). Text sits beside hollow contract marks;
spatial convergence and the retained boundaries carry the argument words off.
"""
from . import svg as S


def build(p):
    mobile=p.get('mobile',False)
    w,h=(340,330) if mobile else (880,330)
    bx=215 if mobile else 420          # the shopping's bus bar
    ax=312 if mobile else 720          # the anchor store
    ys=(80,160,240)
    o=[]
    o.append(S.path(f'M{bx},{ys[0]+12} V{ys[2]}',fill='none',stroke=S.INK,stroke_width=1.7))
    for i,(y,t) in enumerate(zip(ys,['Compra · Graciela','Reserva · precedente','Locação · precedente'])):
        o.append(S.path(f'M48,{y} H{bx}',fill='none',stroke=S.INK,stroke_width=1.7,stroke_dasharray='5 4' if i else 'none'))
        o.append(S.rect(34,y-7,14,14,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
        o.append(S.text(34,y+24,t,size=14,family=S.SERIF))
    o.append(S.circle(bx,ys[1],22,fill=S.PAPER,stroke=S.INK,stroke_width=1.8))
    o.append(S.text(bx,ys[1]+46 if mobile else ys[1]+46,'empreendedor',size=14,family=S.SERIF,anchor='middle'))
    o.append(S.path(f'M{bx+22},{ys[1]} H{ax-12}',fill='none',stroke=S.INK,stroke_width=1.5))
    o.append(S.circle(ax,ys[1],12,fill=S.PAPER,stroke=S.INK,stroke_width=1.7))
    o.append(S.text(ax,ys[1]+34,'âncora',size=14,family=S.SERIF,anchor='middle'))
    # The promised exclusivity runs from the purchase straight to the anchor, over the bus.
    ty=34; mx=(ax+41)//2
    for d in (f'M41,{ys[0]-7} V{ty}',f'M41,{ty} H{mx-12}',f'M{mx+12},{ty} H{ax}',f'M{ax},{ty} V{ys[1]-12}'):
        o.append(S.path(d,fill='none',stroke=S.CONC,stroke_width=1.6))
    o.append(S.path(f'M{mx-8},{ty-8} l16,16 m-16,0 l16,-16',fill='none',stroke=S.CONC,stroke_width=1.8))
    o.append(S.text(mx,ty-14,'exclusividade violada',size=13,family=S.SERIF,anchor='middle',fill=S.CONC))
    o.append(S.text(w/2 if mobile else bx,h-14,'Contratos distintos · finalidade comercial articulada',size=14 if mobile else 15,family=S.SERIF,anchor='middle'))
    return S.svg(w,h,'Contratos em torno do shopping nos dois processos citados',o),[]
