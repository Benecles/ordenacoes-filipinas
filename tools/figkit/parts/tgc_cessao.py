"""Cessão: temporal geometry of substitution, election, and residual responsibility.

params: mode = tempo | vias | reserva | alcance. No dates, amounts or fictional
case facts are added. Positions represent relative order only. `reserva` is an
abstract stipulation, signed using the HTML checkbox beside the generated sheet.
Sources: Luis Renato Ferreira da Silva, pp.398–408; Venosa §5.9 pp.46–47.
All other content and geometry derive from the selected mode, not caller offsets.
"""
from . import svg as S


def build(p):
    mode=p.get('mode','tempo')
    o=[]
    def t(x,y,s,**kw): o.append(S.text(x,y,s,**kw))
    def line(x,y,x2,y2,**kw): o.append(S.line(x,y,x2,y2,stroke=kw.pop('stroke',S.INK),**kw))
    def dot(x,y,col=S.INK): o.append(S.circle(x,y,4,fill=S.PAPER,stroke=col,stroke_width=1.5))
    if mode=='tempo':
        w,h=850,270
        start,change,end=210,540,805
        for i,label in enumerate(['Cessão da posição','Pessoa a declarar']):
            y=77+i*125
            t(20,y-22,label,family=S.SANS,size=16,weight='600')
            line(start,y,end,y,stroke_width=1.5)
            for x in (start,change,end): dot(x,y)
            if i==0:
                line(start,y-8,change,y-8,stroke_width=4)
                line(change,y-8,end,y-8,stroke=S.DIF,stroke_width=4)
                t(start,y+25,'cedente',size=13)
                t(change+15,y+25,'cessionário · ex nunc',size=13,fill=S.DIF)
            else:
                line(start,y-8,end,y-8,stroke=S.DIF,stroke_width=4)
                o.append(S.path(f'M{change},{y-19} Q{(start+change)/2},{y-60} {start},{y-19}',fill='none',stroke=S.DIF,stroke_width=1.5))
                t(start,y+25,'nomeado · desde a celebração',size=13,fill=S.DIF)
                t(change+15,y+25,'nomeação · ex tunc',size=13)
        t(start,25,'celebração',size=12,fill=S.MUTED)
        t(change,25,'substituição',size=12,fill=S.MUTED)
    elif mode=='vias':
        w,h=850,340
        for i,label in enumerate(['Cessão','Subcontrato']):
            y=62+i*168
            t(20,y,label,family=S.SANS,size=17,weight='600')
            x0,cut,x1=220,510,800
            line(x0,y-10,x1,y-10,stroke_width=2)
            t(x0,y-24,'cedido',size=13)
            if i==0:
                line(x0,y+60,cut,y+60,stroke_width=2)
                o.append(S.path(f'M{cut},{y+60} C{cut+50},{y+60} {cut+15},{y+100} {cut+70},{y+100}',stroke=S.MUTED,fill='none',stroke_width=1.5))
                line(cut,y+60,x1,y+60,stroke=S.DIF,stroke_width=2)
                for x in (x0+55,x1-40): line(x,y-10,x,y+60,stroke=S.MUTED,stroke_dasharray='3 4')
                t(x0,y+82,'cedente',size=13)
                t(cut+88,y+82,'cessionário',size=13,fill=S.DIF)
                dot(cut,y+60)
            else:
                line(x0,y+48,x1,y+48,stroke_width=2)
                line(cut,y+100,x1,y+100,stroke_width=2)
                for x in (x0+55,x1-40): line(x,y-10,x,y+48,stroke=S.MUTED,stroke_dasharray='3 4')
                for x in (cut+35,x1-40): line(x,y+48,x,y+100,stroke=S.MUTED,stroke_dasharray='3 4')
                t(x0,y+70,'contratante comum',size=13)
                t(cut+85,y+123,'subcontratado',size=13)
                dot(cut,y+100)
    elif mode=='reserva':
        w,h=760,255
        # The signed reservation supplies an additional contingent path; the primary lane is invariant.
        t(28,30,'ESTIPULAÇÃO DE RESPONSABILIDADE',size=13,weight='600')
        line(28,45,732,45,stroke=S.GRID)
        t(28,75,'A posição passa ao cessionário.',family=S.SERIF,size=20)
        t(28,105,'A responsabilidade do cedente fica reservada em caráter subsidiário.',family=S.SERIF,size=18)
        line(45,165,710,165,stroke_width=2)
        t(45,147,'cessionário',size=13)
        t(710,147,'cedido',size=13,anchor='end')
        o.append('<g data-reserva hidden>')
        o.append(S.path('M190,165 L190,220 L650,220 L650,165',stroke=S.CONC,fill='none',stroke_width=1.6,stroke_dasharray='4 5'))
        t(370,244,'cedente · via subsidiária',size=13,fill=S.CONC,anchor='middle')
        o.append('</g>')
        dot(190,165);dot(650,165)
    elif mode=='alcance':
        w,h=850,265
        a,b,c,d=65,390,535,800
        for x,label in [(a,'pagamentos anteriores'),(c,'cessão'),(d,'discussão judicial')]:
            t(x,27,label,size=12,anchor='end' if x==d else 'start',fill=S.MUTED)
            line(x,43,x,235,stroke=S.GRID)
        line(a,95,b,95,stroke_width=7)
        line(b,81,b,109,stroke_width=2)
        t(a,145,'prestações quitadas',size=14)
        o.append(S.path(f'M{a},195 L{c},195 L{d},195',stroke=S.DIF,fill='none',stroke_width=3))
        dot(c,195,S.DIF);dot(d,195,S.DIF)
        t(a,222,'créditos incluídos na cessão',size=14)
        t(c+18,177,'novo titular',size=14,fill=S.DIF)
    else:
        raise ValueError('mode must be tempo, vias, reserva or alcance')
    return S.svg(w,h,{'tempo':'Início dos efeitos na cessão e na nomeação','vias':'Uma relação continuada ou duas relações dependentes','reserva':'Reserva expressa de responsabilidade subsidiária','alcance':'Pagamento extinto e crédito transmitido no REsp 356.383/SP'}[mode],o),[]
