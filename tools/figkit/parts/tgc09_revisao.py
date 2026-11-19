"""Revisão dos contratos: drawings grounded in the assigned record.

params:
 mode: contagem | historia | risco | efeitos | poderes | prestacoes
 contagem: total (default35), performed (default3), both from TJDFT810778 pp7–10.
 historia: dated positions calculated on a linear 1850–2002 scale; doctrine in Dias331–333.
 risco: qualitative nested regions; marker moved by the page's labelled range control.
 efeitos: categorical temporal lanes, no claim to measured duration, CC157/478.
All modes return SVG and an empty renderer object list. No source fact is randomised.
"""
from . import svg as S

def build(p):
    mode=p.get('mode','contagem'); o=[]; T=S.text
    if mode=='contagem':
        total=int(p.get('total',35)); done=int(p.get('performed',3)); w,h=780,262
        o += [T(20,30,'35 apresentações prometidas',size=23,family=S.SERIF),T(20,60,'3 realizadas',size=15,family=S.SANS,fill=S.INK2)]
        for i in range(total):
            x=44+(i%7)*105; y=105+(i//7)*25
            o.append(S.circle(x,y,6,fill=S.INK if i<done else S.PAPER,stroke=S.INK,stroke_width=1.3))
        o += [S.line(20,222,760,222,stroke=S.GRID),T(20,244,'Cumprimento parcial',size=13,fill=S.INK2),T(760,244,'Validade examinada na assinatura',size=13,anchor='end',fill=S.CONC)]
        title='Trinta e cinco marcas de apresentações, três preenchidas; quantidade não mede equivalência econômica'
    elif mode=='historia':
        w,h=900,360; x=lambda yr:60+(yr-1850)/(2002-1850)*770
        o += [S.line(60,162,830,162,stroke=S.INK,stroke_width=1.5)]
        for year in range(1850,2001,25):
            xx=x(year);o += [S.line(xx,156,xx,171,stroke=S.MUTED),T(xx,190,str(year),size=12,anchor='middle',fill=S.MUTED)]
        a,b=x(1914),x(1918)
        o += [S.rect(a,145,b-a,34,fill=S.INK,opacity='.18'),T((a+b)/2,130,'1914–1918',size=12,anchor='middle',fill=S.INK2)]
        data=[(1850,'Windscheid','pressuposição',45,'start'),(1921,'Oertmann','base subjetiva',244,'middle'),(1942,'Itália','onerosidade excessiva',85,'middle'),(1990,'CDC','fato superveniente',317,'middle'),(2002,'Código Civil','extraordinário e imprevisível',32,'end')]
        for year,name,sub,y,anchor in data:
            xx=x(year); end=y+22 if y<162 else y-38
            o += [S.line(xx,162,xx,end,stroke=S.INK2,stroke_width=1),S.circle(xx,162,4,fill=S.PAPER,stroke=S.INK,stroke_width=1.5),T(xx,y,str(year)+' · '+name,size=15,anchor=anchor,family=S.SANS,weight='600'),T(xx,y+22,sub,size=15,anchor=anchor,family=S.SERIF,fill=S.INK2)]
        title='Datas entre 1850 e 2002: pressuposição, base do negócio e codificações'
    elif mode=='risco':
        w,h=740,320
        # Nested, qualitative regions: the ordinary risk belongs to every future contract;
        # typical risk adds a specific layer in an aleatory bargain. Outside both is a separate inquiry.
        o += [S.circle(240,160,125,fill='none',stroke=S.INK2,stroke_width=1.5),S.circle(240,160,64,fill='none',stroke=S.INK,stroke_width=1.5)]
        o += [T(240,153,'normal',size=17,anchor='middle',family=S.SERIF),T(240,177,'todo contrato',size=12,anchor='middle',fill=S.INK2),T(240,65,'típica do aleatório',size=16,anchor='middle',family=S.SERIF),T(465,85,'Fora das duas áleas',size=19,family=S.SERIF),T(465,110,'demais requisitos por provar',size=13,fill=S.INK2)]
        o += [S.line(240,225,640,225,stroke=S.GRID,stroke_width=1.2)]
        o += ['<g data-risk-marker="true" transform="translate(0,0)" class="risk-pointer">'+S.path('M230,245 L240,229 L250,245 Z',fill=S.CONC)+S.line(240,245,240,272,stroke=S.CONC,stroke_width=2)+'</g>']
        o += [T(465,185,'O risco assumido limita a reação.',size=17,family=S.SERIF,fill=S.CONC),T(465,285,'Áreas sem escala quantitativa',size=12,fill=S.MUTED)]
        title='Campos de risco normal, típico e externo, com marcador controlado por faixa'
    elif mode=='efeitos':
        w,h=820,335
        # Categorical positions; no invented dates or measured duration.
        a,event,cite,end=220,420,580,780
        o += [S.line(a,35,a,305,stroke=S.INK,stroke_width=1),S.line(event,88,event,305,stroke=S.MUTED,stroke_width=1,stroke_dasharray='2 5'),S.line(cite,35,cite,305,stroke=S.INK,stroke_width=1)]
        for xx,label in [(a,'celebração'),(event,'mudança'),(cite,'citação')]:o.append(T(xx,24 if xx!=event else 77,label,size=14,anchor='middle',family=S.SANS))
        for y,label in [(130,'lesão'),(215,'onerosidade')]:
            o += [T(15,y+5,label,size=17,family=S.SERIF),S.line(a,y,end,y,stroke=S.INK,stroke_width=3)]
        for xx in range(a,end,22):o.append(S.line(xx,119,xx+13,141,stroke=S.CONC,stroke_width=1.2))
        o += [T(250,168,'o defeito já existia',size=15,family=S.SERIF,fill=S.INK2)]
        o += [S.line(cite,203,end,203,stroke=S.DIF,stroke_width=3),S.line(cite,227,end,227,stroke=S.DIF,stroke_width=3),T(390,263,'fato posterior',size=14,family=S.SERIF),T(780,295,'efeitos da resolução desde a citação',size=14,family=S.SERIF,anchor='end',fill=S.DIF)]
        title='Lesão alcança o negócio originário; resolução por onerosidade tem efeitos a partir da citação'
    elif mode=='poderes':
        w,h=820,300
        # Who the Civil Code lets act, by remedy: CC 478-480 and 317; the dashed ring is the disputed power (Enunciado 176; Marino).
        cols=[(300,'resolver','art. 478'),(450,'modificar','art. 479'),(600,'reduzir','art. 480'),(750,'corrigir valor','art. 317')]
        rows=[(125,'devedor'),(215,'credor, réu')]
        for x,a,b in cols:
            o += [T(x,38,a,size=15,anchor='middle',family=S.SANS,weight='600'),T(x,60,b,size=14,anchor='middle',fill=S.MUTED)]
            o.append(S.line(x,76,x,262,stroke=S.GRID,stroke_width=1))
        for y,l in rows:
            o += [T(20,y+5,l,size=17,family=S.SERIF),S.line(150,y,800,y,stroke=S.GRID,stroke_width=1)]
        solid=[(300,125),(600,125),(750,125),(450,215),(750,215)]
        for x,y in solid:
            o.append(S.circle(x,y,13,fill=S.INK,stroke=S.INK,stroke_width=1.5))
        o.append(S.circle(450,125,13,fill='none',stroke=S.CONC,stroke_width=2.2,stroke_dasharray='4 3'))
        o += [T(475,168,'pedir a modificação:',size=14,fill=S.CONC,family=S.SERIF),T(475,187,'Enunciado 176 contra Marino',size=14,fill=S.CONC,family=S.SERIF)]
        o += [T(20,285,'O juiz atua em cada coluna a pedido da parte.',size=14,family=S.SERIF,fill=S.INK2)]
        title='Quatro remédios do Código Civil e quem pode pedir cada um; o pedido do devedor para modificar é disputado'
    elif mode=='prestacoes':
        w,h=820,300
        # Schematic ledger of instalments around the citation (Caio Mario p.150; Venosa p.71); the count of squares is illustrative.
        cut,sen=330,590
        o += [S.line(20,150,800,150,stroke=S.GRID,stroke_width=1)]
        for i in range(5):o.append(S.rect(45+i*54,134,32,32,fill=S.INK,stroke=S.INK))
        for i in range(3):
            x=cut+22+i*54;o += [S.rect(x,134,32,32,fill='none',stroke=S.DIF,stroke_width=2),S.line(x+2,164,x+30,136,stroke=S.DIF,stroke_width=1.2),S.line(x+16,164,x+30,150,stroke=S.DIF,stroke_width=1.2),S.line(x+2,150,x+16,136,stroke=S.DIF,stroke_width=1.2)]
        for i in range(4):o.append(S.rect(sen+22+i*50,134,32,32,fill='none',stroke=S.INK,stroke_width=1.5,stroke_dasharray='4 3'))
        for x,l in [(cut,'ingresso em juízo'),(sen,'sentença')]:
            o += [S.line(x,92,x,208,stroke=S.INK,stroke_width=2),T(x,80,l,size=15,anchor='middle',family=S.SANS,weight='600')]
        o += [T(150,198,'pagas antes do pedido',size=15,anchor='middle',family=S.SERIF),T(150,220,'extintas, sem revisão',size=14,anchor='middle',fill=S.INK2,family=S.SERIF)]
        o += [T(460,198,'pagas durante a lide',size=15,anchor='middle',family=S.SERIF,fill=S.DIF),T(460,220,'ajustadas na execução da sentença',size=14,anchor='middle',fill=S.DIF,family=S.SERIF)]
        o += [T(700,198,'ainda devidas',size=15,anchor='middle',family=S.SERIF),T(700,220,'objeto do pedido',size=14,anchor='middle',fill=S.INK2,family=S.SERIF)]
        o += [T(460,260,'cessar o pagamento por conta própria: só com autorização judicial',size=14,anchor='middle',fill=S.CONC,family=S.SERIF)]
        title='Parcelas pagas antes do ingresso em juízo, durante a lide e ainda devidas depois da sentença'
    else:raise ValueError('Unknown tgc09 mode: '+mode)
    return S.svg(w,h,title,o),[]
