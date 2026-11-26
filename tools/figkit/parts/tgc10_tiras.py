"""Two actual settlements: Tânia's distrato and a real-estate resolution.

Amounts and returns come from REsp 1.040.606 and Venosa p.99. The occupation
period is qualitative; the sources give no count to plot. Params: narrow bool.
"""
from . import svg as S


def build(p):
    narrow=p.get('narrow',False)
    W=360 if narrow else 700
    H=468 if narrow else 430
    x=18;end=W-18
    out=[]
    def t(a,b,s,**kw):out.append(S.text(a,b,s,**kw))
    t(x,25,'DISTRATO · TÂNIA',size=15,family=S.SANS,weight='600')
    t(x,49,'efeitos e devolução definidos no acordo',size=14,family=S.SERIF)
    paid=end-x
    returned=paid*(28938.36/41521.30)
    t(x,81,'pago',size=13,family=S.SANS)
    out.append(S.rect(x,91,paid,22,fill=S.PAPER2,stroke=S.INK,stroke_width=1.2))
    t(x+paid/2,107,'R$ 41.521,30',size=13,family=S.SERIF,anchor='middle')
    t(x,139,'acordado a devolver',size=13,family=S.SANS)
    out.append(S.rect(x,149,returned,22,fill=S.DIF,stroke=S.DIF,stroke_width=1.2))
    t(x+returned/2,165,'R$ 28.938,36',size=13,family=S.SERIF,anchor='middle',fill=S.PAPER)
    t(end,194,'6 parcelas mensais',size=14,family=S.SERIF,anchor='end')
    out.append(S.line(x,214,end,214,stroke=S.GRID,stroke_width=1))

    t(x,244,'RESOLUÇÃO · COMPRA E VENDA',size=15,family=S.SANS,weight='600')
    t(x,270,'retorno recíproco',size=14,family=S.SERIF)
    mid=W/2
    # Opposing paths make the two restitutions visible without implying values.
    t(x,300,'compradores',size=13,family=S.SANS)
    t(mid,300,'imóvel',size=13,family=S.SANS,anchor='middle')
    t(end,300,'alienantes',size=13,family=S.SANS,anchor='end')
    out.append(S.line(x+86,309,mid-35,309,stroke=S.DIF,stroke_width=2.2))
    out.append(S.line(mid+30,309,end-85,309,stroke=S.DIF,stroke_width=2.2))
    out.append(S.path(f'M{end-85},309 l-9,-5 M{end-85},309 l-9,5',fill='none',stroke=S.DIF,stroke_width=1.6))
    t(x,334,'compradores',size=13,family=S.SANS)
    t(mid,334,'quantias pagas',size=13,family=S.SANS,anchor='middle')
    t(end,334,'alienantes',size=13,family=S.SANS,anchor='end')
    out.append(S.line(end-85,343,mid+43,343,stroke=S.DIF,stroke_width=2.2))
    out.append(S.line(mid-43,343,x+86,343,stroke=S.DIF,stroke_width=2.2))
    out.append(S.path(f'M{x+86},343 l9,-5 M{x+86},343 l9,5',fill='none',stroke=S.DIF,stroke_width=1.6))
    t(x,386,'ocupação',size=13,family=S.SANS)
    out.append(S.line(x+76,381,end-75,381,stroke=S.INK,stroke_width=3))
    out.append(S.line(end-75,372,end-75,390,stroke=S.CONC,stroke_width=2))
    t(end,386,'desocupação',size=13,family=S.SANS,anchor='end')
    if narrow:
        t(x,413,'uso → aluguel mensal',size=14,family=S.SERIF)
        t(x,435,'créditos podem ser compensados',size=14,family=S.SERIF)
    else:
        t(x,413,'uso → aluguel mensal; créditos podem ser compensados',size=14,family=S.SERIF)
    return S.svg(W,H,'Distrato de Tânia e liquidação da resolução de compra e venda',out),[]
