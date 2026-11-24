"""Vínculos contratuais: régua de preços e relações de três sujeitos.

Params: mode = soja | terceiro | estipulacao. uid: optional unique HTML id.
soja: prices list of {label, value}, unit str, source str; linear scale starts
at zero, a tick for each five reais, values calculated from supplied data.
terceiro: no invented facts; a checkbox lays the known interference over an
existing exclusive relationship. Its answer occupies a fixed region.
estipulacao: triangle separating formation (top) and performance (base),
Pereira III, pp.95–101. All positions are derived from three subject points.
Returns the standard (markup, assets) tuple. No external assets or scripts.
"""
from . import svg as S

def build(p):
    mode=p.get('mode','terceiro')
    b=[]
    def t(x,y,s,**kw): return S.text(x,y,s,size=kw.pop('size',18),family=S.SANS,**kw)
    if mode=='soja':
        vals=p['prices']; maximum=max(v['value'] for v in vals); top=5*(int(maximum/5)+1)
        x0,x1,y0=165,705,65
        scale=lambda v:x0+(x1-x0)*v/top
        b += [t(25,26,p.get('unit','Reais por saca de 60 kg'),size=17),S.line(x0,y0,x1,y0,stroke=S.INK,stroke_width=1.5)]
        for v in range(0,top+1,5):
            x=scale(v); b += [S.line(x,y0-8,x,y0+7,stroke=S.INK,stroke_width=1),t(x,y0-17,str(v),size=15,anchor='middle',fill=S.INK2)]
        for i,v in enumerate(vals):
            y=110+65*i; x=scale(v['value']); col=S.CONC if i==len(vals)-1 else S.INK
            b += [t(145,y+5,v['label'],anchor='end',size=17),S.line(x0,y,x,y,stroke=col,stroke_width=9),S.line(x,y-13,x,y+13,stroke=col,stroke_width=2),t(x+12,y+6,f"{v['value']:.2f}".replace('.',','),size=18,fill=col)]
        b += [t(25,308,p.get('source',''),size=14,fill=S.MUTED)]
        return S.svg(780,330,'Preços contratuais e valor pedido, na mesma escala',b),[]
    if mode=='estipulacao':
        a,bp,c=(380,66),(110,270),(650,270)
        for u,v in [(a,bp),(bp,c),(a,c)]: b.append(S.line(*u,*v,stroke=S.INK,stroke_width=1.8,stroke_dasharray='4 5' if u==a and v==c else None))
        for point in (a,bp,c):b.append(S.circle(*point,7,fill=S.PAPER,stroke=S.INK,stroke_width=2))
        b += [t(380,32,'Estipulante',anchor='middle'),t(95,306,'Promitente',anchor='middle'),t(650,306,'Beneficiário',anchor='middle'),t(150,124,'Formação',size=18),t(380,252,'Execução da prestação',anchor='middle',fill=S.DIF),t(590,134,'Reserva de',size=16),t(590,155,'substituição',size=16),t(380,345,'O crédito chega ao terceiro; a autoria do ajuste permanece entre dois.',size=16,anchor='middle',fill=S.INK2)]
        return S.svg(760,370,'Formação e execução na estipulação em favor de terceiro',b),[]
    if mode!='terceiro': raise ValueError('unknown mode')
    uid=S.esc(p.get('uid','interferencia'))
    b += [S.line(120,100,620,100,stroke=S.INK,stroke_width=3),S.circle(120,100,9,fill=S.PAPER,stroke=S.INK,stroke_width=2),S.circle(620,100,9,fill=S.PAPER,stroke=S.INK,stroke_width=2),t(120,55,'Fischer / All-E',anchor='middle'),t(620,55,'Zeca Pagodinho',anchor='middle'),t(370,83,'Contrato em vigor',anchor='middle',size=17),t(370,129,'exclusividade',anchor='middle',size=16,fill=S.INK2),S.circle(620,260,9,fill=S.PAPER,stroke=S.INK,stroke_width=2),t(620,302,'África',anchor='middle'),S.line(120,174,704,174,stroke=S.GRID,stroke_width=1),t(120,197,'Fora da relação contratual',size=15,fill=S.INK2)]
    film=[S.path('M620 250 Q710 200 626 113',fill='none',stroke=S.CONC,stroke_width=3),S.path('M617 125 L626 112 L640 120',fill='none',stroke=S.CONC,stroke_width=2),t(370,235,'Indução à ruptura',size=18,fill=S.CONC),S.path('M350 243 L458 243',fill='none',stroke=S.CONC,stroke_width=1)]
    b.append('<g class="interference-film">'+''.join(film)+'</g>')
    graph=S.svg(760,330,'A agência concorrente fica fora do vínculo, mas sua interferência o atinge',b)
    return (f'<div class="contract-film"><label for="{uid}" class="film-control"><input id="{uid}" type="checkbox" checked> Sobrepor o aliciamento ao vínculo</label>'+graph+'<div class="film-answer" aria-live="polite"><p class="with-film">A agência responde pela interferência ilícita no contrato conhecido. Sua responsabilidade nasce do dever de respeito ao vínculo alheio.</p><p class="without-film">Ser estranha ao contrato impede que a agência seja cobrada pela prestação do cantor. Essa posição, sozinha, não configura ato ilícito.</p></div></div>'),[]
