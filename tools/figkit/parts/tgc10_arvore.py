"""Planta da extinção, em árvore Sankey.

Params: narrow (bool, default False); mode ('fundamentos' for the companion).
The two wider twigs carry the two
assigned decisions (Tânia's distrato and Santiago's denúncia). Width is an
editorial allocation to the cases, never incidence or probability.
Sources: roteiro pp.3–24; REsp1040606 p.3; REsp1112796 pp.4,30.
The shared planta vocabulary is retained: hollow junctions, square terminals,
focusable threads. No time axis or party lanes.
"""
from . import svg as S


def build(p):
    narrow = p.get('narrow', False)
    out = []
    if p.get('mode') == 'fundamentos':
        if narrow:
            out.append(S.text(18,28,'Interdependência das prestações',size=15,family=S.SANS,weight='600'))
            out.append(S.line(35,60,35,280,stroke=S.INK,stroke_width=4))
            out.append(S.circle(35,60,7,fill=S.PAPER,stroke=S.INK,stroke_width=2))
            for key,y,name,act in [('legal',135,'Resolução legal','constituição judicial'),('negocial',280,'Cláusula expressa','declaração do credor')]:
                body=S.path(f'M35,{y-45} Q35,{y} 95,{y} H330',fill='none',stroke=S.INK,stroke_width=3)
                body+=S.circle(95,y,6,fill=S.PAPER,stroke=S.INK,stroke_width=2)
                body+=S.text(108,y-22,name,size=15,family=S.SANS,weight='600')
                body+=S.text(108,y+30,act,size=15,family=S.SERIF)
                out.append(f'<g data-thread="{key}" tabindex="0" role="button" aria-label="{name}">{body}</g>')
            return S.svg(360,345,'Fontes legal e negocial da resolução',out),[]
        W,H=1000,300
        out.append(S.text(24,137,'Interdependência',size=12.2,family=S.SANS,weight='600'))
        out.append(S.text(24,158,'a troca frustrada',size=11.8,family=S.SERIF,fill=S.INK2))
        out.append(S.line(190,145,280,145,stroke=S.INK,stroke_width=12))
        out.append(S.circle(280,145,7,fill=S.PAPER,stroke=S.INK,stroke_width=2))
        for key,y,name,act,sub in [('legal',65,'Resolução legal','Constituição judicial','a falta atinge o interesse útil'),('negocial',235,'Cláusula expressa','Declaração do credor','o pacto individualiza o risco')]:
            body=S.path(f'M287,145 C380,145 380,{y} 490,{y} H715',fill='none',stroke=S.INK,stroke_width=5)
            body+=S.circle(490,y,6,fill=S.PAPER,stroke=S.INK,stroke_width=2)
            body+=S.text(490,y-24,name,size=12.2,family=S.SANS,weight='600',anchor='middle')
            body+=S.text(490,y+30,sub,size=11.8,family=S.SERIF,anchor='middle',fill=S.INK2)
            body+=S.rect(711,y-4,8,8,fill=S.PAPER,stroke=S.INK,stroke_width=1.5)
            body+=S.text(743,y+4,act,size=12.2,family=S.SANS)
            out.append(f'<g data-thread="{key}" tabindex="0" role="button" aria-label="{name}">{body}</g>')
        return S.svg(W,H,'Resolução legal e direito negocial de resolver',out),[]
    leaves = [
        ('impossibilidade', 'Impossibilidade', 'resultado inviável', '#c2', 5),
        ('distrato', 'Distrato', 'Tânia · acordo extintivo', '#c3', 10),
        ('revogacao', 'Revogação', 'retirada permitida pelo tipo', '#c3', 5),
        ('denuncia', 'Denúncia', 'Santiago · fim da continuidade', '#c4', 10),
        ('resolucao', 'Resolução', 'falta e interesse útil', '#c5', 8),
        ('morte', 'Morte', 'pessoa insubstituível', '#c6', 6),
    ]
    def label(x, y, text, sub, size=12.5):
        return S.text(x,y,text,size=size,family=S.SANS,weight='600') + S.text(x,y+20,sub,size=size,family=S.SERIF,fill=S.INK2)
    def thread(key, title, body):
        return f'<g data-thread="{key}" tabindex="0" role="button" aria-label="{S.esc(title)}">{body}</g>'
    if narrow:
        W,H = 360,650
        out.append(label(18,25,'Extinção','fim do vínculo',15))
        out.append(S.circle(35,80,7,fill=S.PAPER,stroke=S.INK,stroke_width=2))
        body = S.path('M35,80 C35,130 160,110 175,110 H330',fill='none',stroke=S.INK,stroke_width=3)
        body += label(175,77,'Satisfativa','cumprimento',14)
        out.append(thread('cumprimento','Cumprimento',body))
        out.append(S.line(35,87,35,580,stroke=S.INK,stroke_width=4))
        out.append(label(65,164,'Não satisfativa','o fim não se realiza',14))
        for i,(key,name,sub,href,width) in enumerate(leaves):
            y=230+i*74
            body=S.path(f'M35,{y-30} C35,{y} 65,{y} 90,{y}',fill='none',stroke=S.INK,stroke_width=width/2)
            body+=S.rect(86,y-4,8,8,fill=S.PAPER,stroke=S.INK,stroke_width=1.5)
            body+=f'<a href="{href}">'+label(108,y-6,name,sub,14)+'</a>'
            out.append(thread(key,name,body))
    else:
        # Sankey: every ribbon's thickness is the editorial allocation (the two assigned decisions
        # are the widest twigs), stacked without gaps inside each node; never incidence.
        W,H = 1080,440
        K=1.7
        sat=9
        tot=sum(l[4] for l in leaves)*K
        pad=0
        def ribbon(x0,a0,b0,x1,a1,b1):
            xm=(x0+x1)/2
            return S.path(f'M{x0},{a0} C{xm},{a0} {xm},{a1} {x1},{a1} L{x1},{b1} C{xm},{b1} {xm},{b0} {x0},{b0} Z',fill=S.INK,stroke='none')
        rx,ry=40,170                      # root node: left edge, top
        rw=16
        out.append(S.text(rx,ry-42,'Extinção',size=13,family=S.SANS,weight='600'))
        out.append(S.text(rx,ry-24,'fim do vínculo',size=12,family=S.SERIF,fill=S.INK2))
        out.append(S.rect(rx,ry,rw,sat+tot,fill=S.INK,stroke='none'))
        # satisfativa ribbon, top slice of the root
        ty=34
        body=ribbon(rx+rw-1,ry,ry+sat,780,ty-sat/2,ty+sat/2)
        body+=S.rect(776,ty-4,8,8,fill=S.PAPER,stroke=S.INK,stroke_width=1.5)
        body+='<a href="#c1">'+label(806,ty-4,'Satisfativa','cumprimento do programa',11.8)+'</a>'
        out.append(thread('cumprimento','Cumprimento',body))
        # intermediate node, centred on the fan of leaves
        nx=372; nw=16
        ny=ry+sat+22
        out.append(ribbon(rx+rw-1,ry+sat,ry+sat+tot,nx,ny,ny+tot))
        out.append(S.rect(nx,ny,nw,tot,fill=S.INK,stroke='none'))
        out.append(S.circle(nx+nw,ny+tot/2,6,fill=S.PAPER,stroke=S.INK,stroke_width=2))
        out.append(S.text(nx-10,ny+tot+34,'Não satisfativa',size=13,family=S.SANS,weight='600',anchor='end'))
        out.append(S.text(nx-10,ny+tot+53,'o fim não se realiza',size=12,family=S.SERIF,fill=S.INK2,anchor='end'))
        cum=0
        for i,(key,name,sub,href,width) in enumerate(leaves):
            y=104+i*62
            width*=K
            a0=ny+cum; b0=a0+width; cum+=width
            body=ribbon(nx+nw-1,a0,b0,780,y-width/2,y+width/2)
            body+=S.rect(776,y-4,8,8,fill=S.PAPER,stroke=S.INK,stroke_width=1.5)
            body+=f'<a href="{href}">'+label(806,y-4,name,sub,11.8)+'</a>'
            out.append(thread(key,name,body))
    return S.svg(W,H,'Extinção: modos satisfativo e não satisfativo e suas causas',out),[]
