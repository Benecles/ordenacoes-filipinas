"""Contract classifications, Aula 06. Five paper languages derived from the assigned passages.

params: mode ('loja'|'risco'|'adesao'|'rede'), title (optional accessible description).
No dates, prices, dimensions or building plans are asserted. loja is an expressly
schematic spatial comparison of exclusivity and competing product, not a facsimile.
risco encodes order, never a time scale. All positions follow the chosen mode's grid.
"""
from . import svg as S


def build(p):
    mode=p['mode']; o=[]; T=S.text
    def line(a,b,c,d,col=S.INK,w=1.3,**kw):o.append(S.line(a,b,c,d,stroke=col,stroke_width=w,**kw))
    def txt(x,y,t,**kw):o.append(T(x,y,t,**kw))
    if mode=='planta_mobile':
        w,h=324,380
        labels=[('prestacoes','Prestações recíprocas','cumprir · suspender · garantir'),('negociacao','Conteúdo predisposto','interpretar · excluir renúncia'),('unidade','Operação composta','unidade mista · rede coligada')]
        for i,(ident,label,tail) in enumerate(labels):
            y=58+i*111
            marks=[S.path(f'M23,{y-15} V{y+37} H294',fill='none',stroke=S.INK,stroke_width=1.7),S.circle(23,y-15,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.5),T(43,y-8,label,size=15,family=S.SANS,weight='600'),T(43,y+18,tail,size=12,family=S.SERIF),S.circle(294,y+37,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.5)]
            o.append(f'<g data-thread="{ident}" role="button" tabindex="0" aria-label="{label}">'+''.join(marks)+'</g>')
        return S.svg(w,h,'Três critérios e seus efeitos',o),[]
    if mode=='loja':
        w,h=720,335
        # Shared product territory, represented as overlapping outlines, rather than label cards.
        for n,x in enumerate((36,397)):
            txt(x,28,('Exclusividade prometida','Concorrência admitida')[n],size=17,family=S.SANS,weight='600')
            line(x,54,x+278,54); line(x,54,x,265); line(x+278,54,x+278,265);line(x,265,x+278,265)
            # Sales frontage: short shop, long anchor, separated by a corridor.
            o.append(S.path(f'M{x+15},142 v-56 h78 v56 M{x+15},142 h24 m28,0 h26',fill='none',stroke=S.INK,stroke_width=2.3))
            o.append(S.path(f'M{x+128},213 v-127 h133 v127 M{x+128},213 h42 m33,0 h58',fill='none',stroke=S.INK,stroke_width=2.3))
            txt(x+54,113,'loja',size=14,anchor='middle',family=S.SERIF)
            txt(x+194,113,'âncora',size=14,anchor='middle',family=S.SERIF)
            # Product contours overlap only in the actual breach panel.
            o.append(S.circle(x+53,182,29,fill='none',stroke=S.INK,stroke_width=1.7))
            if n:
                o.append(S.path(f'M{x+42},184 C{x+104},134 {x+168},134 {x+233},176 C{x+172},225 {x+103},225 {x+42},184',fill='none',stroke=S.CONC,stroke_width=2))
                txt(x+147,246,'mesmo produto',size=14,anchor='middle',fill=S.CONC,family=S.SERIF)
            else:
                txt(x+133,246,'venda reservada à loja',size=14,anchor='middle',family=S.SERIF)
        txt(36,312,'Esquema da relação comercial · REsp 764.901/RJ, pp. 7–8',size=12,fill=S.MUTED)
    elif mode=='risco':
        w,h=760,300
        xs=(45,282,482,703)
        txt(45,26,'Ordem de cumprimento · sem escala de tempo',size=14,family=S.SANS,weight='600')
        for y,label in ((104,'parte que presta antes'),(205,'contraprestação futura')):
            line(xs[0],y,xs[-1],y,w=1.8)
            txt(xs[0],y-22,label,size=15,family=S.SERIF)
        o.append(S.circle(xs[0],104,6,fill=S.PAPER,stroke=S.INK,stroke_width=1.8))
        o.append(S.circle(xs[0],205,6,fill=S.PAPER,stroke=S.INK,stroke_width=1.8))
        line(xs[1],65,xs[1],230,S.CONC,2.4)
        line(xs[1]-10,76,xs[1]+10,76,S.CONC,2.4)
        txt(xs[1]+15,72,'risco superveniente',size=14,fill=S.CONC,family=S.SERIF)
        o.append(S.rect(xs[2]-7,97,14,14,fill=S.PAPER,stroke=S.INK,stroke_width=2))
        o.append(S.rect(xs[3]-7,198,14,14,fill=S.PAPER,stroke=S.INK,stroke_width=2))
        txt(xs[2],142,'primeira prestação',size=13,anchor='middle')
        txt(xs[3]-8,243,'segunda',size=13,anchor='end')
        o.append(S.path(f'M{xs[1]},266 C{xs[1]+60},295 {xs[2]+100},295 {xs[3]},266',fill='none',stroke=S.DIF,stroke_width=1.5))
        txt(493,283,'cumprimento ou garantia bastante',size=13,anchor='middle',fill=S.DIF,family=S.SERIF)
    elif mode=='adesao':
        w,h=860,400
        # The form as an object: one printed standard sheet (grey ruled clauses), a stack of identical copies behind it,
        # and the few blanks the parties fill in, in blue.
        for k in (3,2,1):
            line(60+11*k,45-9*k,580+11*k,45-9*k,S.MUTED,1); line(580+11*k,45-9*k,580+11*k,363-9*k,S.MUTED,1)
        o.append(S.rect(60,45,520,318,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
        lens=[1,.96,.99,.9,1,.97,.62,1,.94,.98,.88,.55]
        for i,l in enumerate(lens):
            y=72+i*14
            line(86,y,86+l*468,y,S.MUTED,1.1)
        for i,(x0,x1) in enumerate(((86,260),(300,430),(470,554))):
            y=300
            line(x0,y,x1,y,S.INK,1.2)
            o.append(S.path(f'M{x0+6},{y-6} q9,-13 17,-1 t17,-1 t17,0 t17,-2 t16,1',fill='none',stroke=S.INK,stroke_width=1.8))
        txt(86,330,'dados',size=12,fill=S.INK); txt(300,330,'objeto',size=12,fill=S.INK); txt(470,330,'preço',size=12,fill=S.INK)
        # brackets: printed block vs blanks
        o.append(S.path('M660,72 h10 v160 h-10',fill='none',stroke=S.INK,stroke_width=1.4))
        txt(684,148,'condições gerais',size=15,family=S.SERIF)
        txt(684,167,'iguais em cada cópia',size=12,fill=S.MUTED)
        o.append(S.path('M660,284 h10 v38 h-10',fill='none',stroke=S.INK,stroke_width=1.4))
        txt(684,309,'ajuste particular',size=15,family=S.SERIF,fill=S.INK)
    elif mode=='rede':
        w,h=760,310
        txt(32,28,'Unidade mista',size=17,family=S.SANS,weight='600')
        txt(416,28,'Pluralidade coligada',size=17,family=S.SANS,weight='600')
        # A continuous woven field: one enclosing outline; threads penetrate each other.
        o.append(S.path('M48,69 H300 V244 H48 Z',fill='none',stroke=S.INK,stroke_width=2))
        for i in range(6):
            y=91+i*25
            o.append(S.path(f'M49,{y} C112,{y-22} 235,{y+22} 299,{y}',fill='none',stroke=S.INK,stroke_width=1.1))
        for i in range(7):
            x=69+i*35
            o.append(S.path(f'M{x},70 C{x-20},115 {x+20},202 {x},243',fill='none',stroke=S.INK,stroke_width=1.1))
        # Two independent circuits with coupling: even without words the identity is preserved.
        for x in (433,610):
            o.append(S.path(f'M{x},93 h100 v120 h-100 Z',fill='none',stroke=S.INK,stroke_width=2))
            o.append(S.circle(x+50,93,6,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
        for y in (132,174):line(533,y,610,y,w=1.4)
        txt(175,278,'elementos fundidos',size=14,family=S.SERIF,anchor='middle')
        txt(573,278,'contratos preservados',size=14,family=S.SERIF,anchor='middle')
    else:raise ValueError(mode)
    desktop=S.svg(w,h,p.get('title',mode),o)
    if mode in ('loja','rede'):
        # Cropped coordinates keep the very same marks and 12+ px letters on phones.
        cropw=350
        mobile=''.join(desktop.replace(f'viewBox="0 0 {w} {h}"',f'viewBox="{x} 0 {cropw} {h-25 if mode=="loja" else h}"') for x in ((0,365) if mode=='loja' else (0,400)))
    elif mode=='risco':
        b=[T(12,23,'Ordem, sem escala de tempo',size=13,family=S.SANS)]
        for x in (48,265):b.append(S.line(x,58,x,340,stroke=S.INK,stroke_width=1.6))
        for x,y in ((48,207),(265,320)):b.append(S.rect(x-6,y-6,12,12,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
        b.extend([S.line(27,118,289,118,stroke=S.CONC,stroke_width=2),T(78,108,'risco posterior',size=13,fill=S.CONC),T(70,209,'prestar antes',size=13,family=S.SERIF),T(84,321,'contraprestação',size=13,family=S.SERIF),T(18,373,'A suspensão termina com cumprimento',size=12,family=S.SERIF),T(18,392,'ou garantia bastante.',size=12,family=S.SERIF)])
        mobile=S.svg(324,410,'Risco posterior e ordem de cumprimento',b)
    else:
        # A single real form: printed terms above, blanks for particulars below.
        b=[S.rect(12,26,300,342,fill=S.PAPER,stroke=S.INK,stroke_width=1.5)]
        for i,k in enumerate((1,.96,.99,.86,1,.94,.7,1,.91,.98,.76)):
            b.append(S.line(30,52+i*17,30+264*k,52+i*17,stroke=S.MUTED,stroke_width=1))
        for x,word in ((30,'dados'),(127,'objeto'),(224,'preço')):
            b.extend([S.line(x,314,x+70,314,stroke=S.INK,stroke_width=1.2),T(x,341,word,size=13)])
        b.extend([T(12,17,'Conteúdo predisposto',size=14,family=S.SERIF),T(12,397,'Campos particulares conservam a adesão.',size=13,family=S.SERIF)])
        mobile=S.svg(324,418,'Formulário: conteúdo predisposto e campos particulares',b)
    return '<div class="drawing-desktop">'+desktop+'</div><div class="drawing-mobile">'+mobile+'</div>',[]
