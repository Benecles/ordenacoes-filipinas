"""Paired strips: retroactive liquidation / future cut in a continuing relation.

No numerical scale or invented periods. Params: narrow (bool). A folded-back
strip represents unwinding the exchange; an intact spent strip and detached
future represent preservation of consumed use. Sources: Venosa p.95;
Caio Mário p.142; Ruy Rosado pp.508–509; Pontes pp.401–405.
"""
from . import svg as S


def build(p):
    narrow=p.get('narrow',False)
    W=360 if narrow else 700
    H=380 if narrow else 356
    x=18;end=W-18;cut=W*.56
    out=[]
    def t(a,b,s,**kw):out.append(S.text(a,b,s,**kw))
    t(x,28,'Ex tunc',size=18,family=S.SANS,weight='600')
    t(x,54,'desfazer a troca recebida',size=15,family=S.SERIF)
    out.append(S.rect(x,82,end-x,34,fill=S.PAPER2,stroke=S.INK,stroke_width=1.5))
    # A physical strip doubles back to its starting edge.
    out.append(S.path(f'M{end-28},99 C{end+8},99 {end+8},151 {end-32},151 H{x+28} Q{x},151 {x},124',fill='none',stroke=S.INK,stroke_width=2.5))
    out.append(S.path(f'M{x-5},132 L{x},123 L{x+6},132',fill='none',stroke=S.INK,stroke_width=1.5))
    t(W/2,106,'coisa e preço',size=16,family=S.SERIF,anchor='middle')
    t(x,205,'Ex nunc',size=18,family=S.SANS,weight='600')
    t(x,231,'preservar a fruição consumida',size=15,family=S.SERIF)
    out.append(S.rect(x,256,cut-x-7,34,fill=S.PAPER2,stroke=S.INK,stroke_width=1.5))
    out+=S.hatch(x+1,257,cut-x-9,32,step=13,stroke=S.GRID,stroke_width=1)
    out.append(S.rect(cut+9,264,end-cut-9,34,fill='none',stroke=S.MUTED,stroke_width=1.5,stroke_dasharray='3 4'))
    out.append(S.line(cut,245,cut,309,stroke=S.CONC,stroke_width=2))
    t(x,325,'passado preservado',size=15,family=S.SERIF)
    t(end,348 if narrow else 325,'futuro encerrado',size=15,family=S.SERIF,anchor='end')
    return S.svg(W,H,'Efeitos da resolução: retroação e preservação da fruição passada',out),[]
