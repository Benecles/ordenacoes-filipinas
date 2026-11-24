"""Exclusivity and withheld price, REsp 764.901/RJ pp. 7–9; CC 476.
Three states of the existing loja schematic, not a building plan. The unnumbered
payment slip denotes the price obligation, never an amount or number of instalments.
The storefront and corridor marks derive from tgc06_figuras.loja.
"""
from . import svg as S


def build(p):
    state = p['state']
    assert state in ('promessa', 'falta', 'recusa')
    breach = state != 'promessa'
    withheld = state == 'recusa'
    o = []
    def line(a,b,c,d,col=S.INK,w=1.5):
        o.append(S.line(a,b,c,d,stroke=col,stroke_width=w))
    def text(x,y,label,**kw):
        o.append(S.text(x,y,label,size=18,family=S.SERIF,**kw))
    # Two unequal storefronts and their openings face the same corridor.
    for x,width,y in ((36,112,146),(228,154,170)):
        o.append(S.path(f'M{x},{y} V54 H{x+width} V{y} H{x+width-32} M{x+32},{y} H{x}',fill='none',stroke=S.INK,stroke_width=2))
    text(92,40,'loja',anchor='middle')
    text(305,40,'âncora',anchor='middle')
    # The same product mark appears in the anchor only once exclusivity is broken.
    def phone(x,y):
        o.append(S.rect(x,y,20,33,fill=S.PAPER,stroke=S.INK,stroke_width=1.7))
        line(x+5,y+5,x+15,y+5)
        line(x+8,y+27,x+12,y+27)
    phone(82,83)
    if breach:
        phone(295,83)
        o.append(S.path('M69,132 C130,64 249,64 329,132',fill='none',stroke=S.CONC,stroke_width=2))
        text(210,204,'exclusividade violada',anchor='middle',fill=S.CONC)
    else:
        o.append(S.circle(92,100,39,fill='none',stroke=S.INK,stroke_width=1.5))
        text(210,204,'venda reservada à loja',anchor='middle')
    # One price slip remains intact in every state. At state 3 it stops short
    # of the collection boundary, so suspension does not erase the obligation.
    x = 40 if withheld else 104
    o.append(S.rect(x,230,202,65,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
    for yy,length in ((245,145),(254,121),(263,135)):
        line(x+14,yy,x+length,yy,S.MUTED,1)
    text(x+101,286,'preço',anchor='middle')
    if withheld:
        line(280,227,280,300,S.DIF,2.5)
        line(288,227,288,300,S.DIF,1.2)
        text(210,331,'cobrança paralisada',anchor='middle',fill=S.DIF)
    else:
        text(210,331,'obrigação de pagar',anchor='middle')
    return S.svg(420,350,'Exclusividade e exigibilidade do preço: '+state,o), []
