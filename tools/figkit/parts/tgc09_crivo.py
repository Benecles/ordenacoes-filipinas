"""Aula09 ch.4 instrument: four decided cases walked through the requisitos of CC 478.
Each case is a focusable thread that runs until the requisito the court found missing.
Facts only from the page's own cases: STJ REsp 860.277/2010 (soja futura), TJSP Ap 0022991 (bingo),
TJSP Ap 0067544 (maquinario), Venosa p.74-76 (swap). No quantities; the stop position is categorical.
"""
from . import svg as S

def build(p):
    t=S.text; o=[]
    gx=[500,690,880]
    heads=[('execução continuada','ou diferida'),('acontecimento','extraordinário e imprevisível'),('fora da álea','do contrato')]
    for x,(a,b) in zip(gx,heads):
        o += [t(x,34,a,size=14,family=S.SANS,weight='600',anchor='middle'),t(x,53,b,size=13,family=S.SERIF,fill=S.INK2,anchor='middle'),S.line(x,70,x,300,stroke=S.GRID,stroke_width=1,stroke_dasharray='2 5')]
    cases=[('Soja de safra futura','STJ, REsp 860.277','cotação em bolsa: a oscilação diária é inerente',1),
           ('Bingo mantido por liminar','TJSP, 2014','a cassação das liminares era conhecida das duas partes',2),
           ('Compra de maquinário','TJSP, 2013','preço e pagamento prefixados, sem menção ao câmbio',1),
           ('Swap','parâmetros financeiros','a oscilação prevista é o risco do negócio',2)]
    for i,(name,src,why,stop) in enumerate(cases):
        y=108+i*62
        o.append(f'<g data-case="{i}" tabindex="0" role="link" aria-label="{S.esc(name)}">')
        o.append(S.rect(0,y-28,1000,56,fill='none',stroke='none',pointer_events='all'))
        o += [t(20,y-4,name,size=16,family=S.SANS,weight='600'),t(20,y+17,why,size=12.5,family=S.SERIF,fill=S.INK2)]
        o += [S.circle(330,y,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.7),S.line(335,y,gx[stop]-8,y,stroke=S.INK,stroke_width=2)]
        for k in range(stop):o.append(S.circle(gx[k],y,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.7))
        sx=gx[stop]
        o += [S.rect(sx-7,y-7,14,14,fill=S.PAPER,stroke=S.CONC,stroke_width=2),S.line(sx-5,y-5,sx+5,y+5,stroke=S.CONC,stroke_width=1.8),S.line(sx-5,y+5,sx+5,y-5,stroke=S.CONC,stroke_width=1.8)]
        o.append('</g>')
    return S.svg(1000,334,'Quatro decisões percorrem os requisitos do art. 478; cada uma cai no que o tribunal não viu preenchido',o),[]
