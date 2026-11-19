"""Extinção dos contratos: literal measurements and one clause-reading instrument.

Params: mode = tempo | conta | aviso | efeitos | eixos.
Facts: REsp 1040606, PDF p.3; REsp1112796, PDF pp.4,30; CC234,395,474;
Martins-Costa pp.403–406. No invented quantitative scale. Dates and the
account difference are computed. Mobile variants are recomposed, not shrunk.
"""
from datetime import date
from decimal import Decimal
from . import svg as S


def build(p):
    mode=p['mode']; out=[]
    def t(x,y,s,**kw): out.append(S.text(x,y,s,**kw))
    def line(x,y,a,b,**kw): out.append(S.line(x,y,a,b,stroke=kw.pop('stroke',S.INK),**kw))
    def path(d,**kw): out.append(S.path(d,fill='none',stroke=kw.pop('stroke',S.INK),**kw))
    if mode=='conta':
        W,H=620,280
        paid=Decimal('41521.30'); returned=Decimal('28938.36'); rest=paid-returned
        def br(n): return f'{n:,.2f}'.replace(',','@').replace('.',',').replace('@','.')
        t(18,27,'CONTA DO ACORDO',size=12,letter_spacing='.09em')
        for i,(label,n,col) in enumerate([('Já desembolsado',paid,S.INK),('Devolução pactuada',returned,S.DIF),('Diferença entre os valores',rest,S.INK2)]):
            y=72+i*68
            t(18,y,label,size=17,family=S.SERIF)
            t(596,y,'R$ '+br(n),size=17,anchor='end',fill=col)
            line(18,y+19,596,y+19,stroke=S.GRID)
        t(18,265,'A diferença não é uma multa fixada pelo STJ.',size=14,family=S.SERIF,fill=S.INK2)
    elif mode=='tempo':
        W,H=610,330
        t(20,25,'O TEMPO E A UTILIDADE',size=12,letter_spacing='.08em')
        for i in range(3):
            y=84+i*94
            line(25,y,585,y,stroke=S.GRID)
            for x in range(25,586,20): line(x,y-4,x,y+4,stroke=S.GRID)
            if i==0:
                line(25,y,215,y,stroke_width=3)
                line(215,y,350,y,stroke=S.MUTED,stroke_width=2,stroke_dasharray='3 5')
                line(350,y,585,y,stroke_width=3)
                t(25,y-21,'Suspensão',size=17,family=S.SERIF)
                t(280,y+29,'o fim ainda pode ser alcançado',size=14,anchor='middle',family=S.SERIF)
            else:
                end=295 if i==1 else 215
                line(25,y,end,y,stroke_width=3)
                line(end,y-13,end,y+13,stroke=S.CONC,stroke_width=3)
                t(25,y-21,'Termo essencial' if i==1 else 'Impossibilidade definitiva',size=17,family=S.SERIF)
                t(end+20,y+29,'o atraso destrói a utilidade' if i==1 else 'a prestação não poderá ocorrer',size=14,family=S.SERIF,fill=S.CONC)
    elif mode=='aviso':
        W,H=1000,235
        a,b=date(1998,6,3),date(1999,1,25); days=(b-a).days
        x0,x1=45,955;y=118
        line(x0,y,x1,y,stroke_width=2)
        # Month lengths, rather than equal-width fictional months.
        for m in [date(1998,k,1) for k in range(7,13)]+[date(1999,1,1)]:
            x=x0+(m-a).days/days*(x1-x0)
            line(x,y-6,x,y+6,stroke=S.MUTED)
        for x in [x0,x1]: out.append(S.circle(x,y,7,fill=S.PAPER,stroke=S.INK,stroke_width=2))
        t(x0,53,'03.06.1998',size=14);t(x0,79,'Notificação',size=18,family=S.SERIF)
        t(x1,53,'25.01.1999',size=14,anchor='end');t(x1,79,'Cessação anunciada',size=18,family=S.SERIF,anchor='end')
        t(500,165,f'{days} dias entre os dois marcos',size=18,anchor='middle',family=S.SERIF)
        t(500,205,'O prazo do caso não é um prazo geral do Código.',size=15,anchor='middle',family=S.SERIF,fill=S.INK2)
    elif mode=='efeitos':
        W,H=980,330
        t(20,28,'RESTITUIR',size=12,letter_spacing='.08em')
        line(65,83,915,83,stroke_width=2);path('M905,76 L915,83 L905,90',stroke_width=2)
        line(915,135,65,135,stroke_width=2);path('M75,128 L65,135 L75,142',stroke_width=2)
        t(65,64,'Coisa recebida',size=17,family=S.SERIF);t(915,164,'Preço recebido',size=17,anchor='end',family=S.SERIF)
        line(20,195,960,195,stroke=S.GRID)
        t(20,229,'CONSERVAR O PERÍODO JÁ FRUÍDO',size=12,letter_spacing='.07em')
        line(65,270,565,270,stroke_width=4)
        line(565,270,915,270,stroke=S.MUTED,stroke_width=3,stroke_dasharray='3 5')
        line(565,247,565,290,stroke=S.CONC,stroke_width=2)
        t(65,313,'Uso já realizado',size=16,family=S.SERIF)
        t(605,313,'Fim da relação duradoura',size=16,family=S.SERIF)
    elif mode=='eixos':
        W,H=650,365
        line(100,300,610,300);line(100,300,100,45)
        t(108,25,'IMPEDIMENTO INSUPERÁVEL',size=12)
        t(108,345,'Ligado ao devedor',size=14,family=S.SERIF)
        t(610,345,'Para todos',size=14,family=S.SERIF,anchor='end')
        for x,y,label,sub in [(165,95,'Hospitalização','prestação pessoal'),(525,95,'Proibição legal','atividade vedada'),(165,245,'Falta de meios','não libera por si')]:
            out.append(S.circle(x,y,6,fill=S.PAPER,stroke=S.INK,stroke_width=2))
            t(x,y+26,label,size=17,anchor='middle',family=S.SERIF)
            t(x,y+48,sub,size=13,anchor='middle',family=S.SERIF,fill=S.INK2)
        line(100,195,610,195,stroke=S.GRID,stroke_dasharray='3 5')
        t(16,95,'Absoluta',size=13,family=S.SERIF)
        t(16,250,'Relativa',size=13,family=S.SERIF)
    else: raise ValueError(mode)
    return S.svg(W,H,'Extinção dos contratos: '+mode,out),[]


def _mobile(mode):
    """Narrow plates recomposed at 360 units; labels remain readable on a phone."""
    out=[]
    def t(x,y,s,**kw):out.append(S.text(x,y,s,**kw))
    def ln(x,y,a,b,**kw):out.append(S.line(x,y,a,b,stroke=kw.pop('stroke',S.INK),**kw))
    H=350
    if mode=='tempo':
        H=345
        for i,(name,note) in enumerate([('Suspensão','o resultado continua possível'),('Termo essencial','o atraso destrói a utilidade'),('Impossibilidade definitiva','a prestação não poderá ocorrer')]):
            y=60+i*104;t(15,y-21,name,size=17,family=S.SERIF)
            ln(15,y,345,y,stroke=S.GRID)
            for x in range(15,346,15):ln(x,y-4,x,y+4,stroke=S.GRID)
            ln(15,y,130,y,stroke_width=3)
            if i==0:
                ln(130,y,220,y,stroke_dasharray='3 5',stroke=S.MUTED);ln(220,y,345,y,stroke_width=3)
            else:ln(130,y-11,130,y+11,stroke=S.CONC,stroke_width=3)
            t(15,y+30,note,size=14,family=S.SERIF,fill=S.INK2)
    elif mode=='conta':
        H=310;t(15,25,'CONTA DO ACORDO',size=12)
        paid,returned=Decimal('41521.30'),Decimal('28938.36')
        br=lambda n:f'{n:,.2f}'.replace(',','@').replace('.',',').replace('@','.')
        vals=[('Já desembolsado',br(paid)),('Devolução pactuada',br(returned)),('Diferença',br(paid-returned))]
        for i,(name,val) in enumerate(vals):
            y=65+i*76;t(15,y,name,size=17,family=S.SERIF);t(345,y+28,'R$ '+val,size=18,anchor='end',fill=S.DIF if i==1 else S.INK);ln(15,y+40,345,y+40,stroke=S.GRID)
        t(15,296,'Valores convencionados pelas partes.',size=14,family=S.SERIF)
    elif mode=='aviso':
        H=300;ln(35,45,35,225,stroke_width=2)
        a,b=date(1998,6,3),date(1999,1,25);days=(b-a).days
        for i in range(1,8):ln(30,45+i*180/8,40,45+i*180/8,stroke=S.GRID)
        for y in (45,225):out.append(S.circle(35,y,6,fill=S.PAPER,stroke=S.INK,stroke_width=2))
        t(60,42,'03.06.1998',size=15);t(60,68,'Notificação',size=18,family=S.SERIF)
        t(60,140,f'{days} dias',size=20,family=S.SERIF)
        t(60,222,'25.01.1999',size=15);t(60,248,'Cessação anunciada',size=18,family=S.SERIF)
        t(15,289,'Intervalo real deste contrato.',size=14,family=S.SERIF)
    elif mode=='efeitos':
        H=320;t(15,25,'RESTITUIR',size=12)
        ln(20,75,340,75,stroke_width=2);out.append(S.path('M330,68 l10,7 l-10,7',fill='none',stroke=S.INK))
        t(20,59,'Coisa recebida',size=17,family=S.SERIF)
        ln(340,120,20,120,stroke_width=2);out.append(S.path('M30,113 l-10,7 l10,7',fill='none',stroke=S.INK))
        t(340,150,'Preço recebido',size=17,family=S.SERIF,anchor='end')
        t(15,200,'PRESERVAR A FRUIÇÃO PASSADA',size=12)
        ln(20,240,195,240,stroke_width=4)
        ln(195,240,340,240,stroke_width=3,stroke=S.MUTED,stroke_dasharray='3 5')
        ln(195,220,195,260,stroke=S.CONC,stroke_width=2)
        t(20,286,'Uso realizado',size=16,family=S.SERIF);t(340,311,'Fim da duração',size=16,family=S.SERIF,anchor='end')
    elif mode=='eixos':
        H=360;ln(65,290,345,290);ln(65,290,65,35);ln(65,196,345,196,stroke=S.GRID,stroke_dasharray='3 5')
        t(65,21,'IMPEDIMENTO INSUPERÁVEL',size=12)
        for x,y,lines in [(125,70,['Hospitalização','pessoal']),(278,70,['Proibição','geral']),(125,220,['Falta','de meios'])]:
            out.append(S.circle(x,y,5,fill=S.PAPER,stroke=S.INK,stroke_width=2))
            for i,label in enumerate(lines):t(x,y+25+i*20,label,size=15,anchor='middle',family=S.SERIF)
        t(7,70,'Absoluta',size=12,family=S.SERIF);t(7,220,'Relativa',size=12,family=S.SERIF)
        t(65,320,'Devedor',size=15,family=S.SERIF);t(340,320,'Todos',size=15,anchor='end',family=S.SERIF)
    elif mode=='hero_mobile':
        H=420
        t(15,28,'O DESTINO DO PROGRAMA',size=12)
        ln(30,62,30,357,stroke_width=2)
        out.append(S.rect(22,54,16,16,fill=S.INK))
        t(55,69,'Contrato válido',size=19,family=S.SERIF)
        for key,y,label,sub in [('cumprimento',135,'Cumprimento','o fim se realiza'),('vontade',220,'Vontade','saída autorizada'),('frustracao',305,'Frustração','impossibilidade ou falta')]:
            body=S.line(30,y,330,y,stroke=S.INK,stroke_width=2)
            body+=S.circle(330,y,5,fill=S.PAPER,stroke=S.INK,stroke_width=2)
            body+=S.text(55,y-15,label,size=19,family=S.SERIF)
            body+=S.text(55,y+27,sub,size=16,family=S.SERIF,fill=S.INK2)
            out.append(f'<g data-thread="{key}" role="button" tabindex="0" aria-label="{label}">'+body+'</g>')
        ln(330,135,330,357,stroke_width=2)
        t(330,398,'Extinção e destino dos efeitos',size=18,anchor='end',family=S.SERIF)
    else: raise ValueError(mode)
    return S.svg(360,H,'Extinção dos contratos: '+mode,out)


_build_wide=build

def build(p):
    mode=p['mode']
    if mode=='hero_mobile':return _mobile(mode),[]
    wide,states=_build_wide(p)
    return '<div class="art-desktop">'+wide+'</div><div class="art-mobile">'+_mobile(mode)+'</div>',states
