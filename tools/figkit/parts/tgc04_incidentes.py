"""Incidentes: bespoke paper languages for the third party and the earnest.
Params: mode = triangle | successive | retro | arras | history | coins.
All geometry is computed here. Facts: Pereira III §§198–206-A; CC417–420,
439–440, 467–471. Arras is a symbolic unit, never a fabricated case amount.
The arras control is authored in HTML; this part casts its physical tally.
"""
from . import svg as S

def build(p):
 m=p.get('mode','triangle'); o=[]
 def t(x,y,s,size=14,**kw): o.append(S.text(x,y,s,size=size,family=S.SANS,**kw))
 def l(x,y,a,b,col=S.INK,dash=None): o.append(S.line(x,y,a,b,stroke=col,stroke_width=1.5,stroke_dasharray=dash))
 def dot(x,y,col=S.INK): o.append(S.circle(x,y,6,fill=S.PAPER,stroke=col,stroke_width=2))
 def path(d,col=S.INK,dash=None): o.append(S.path(d,fill='none',stroke=col,stroke_width=1.8,stroke_dasharray=dash))
 if m=='triangle':
  W,H=500,350
  # Formation across the top; performance descends to the third point.
  a,b,c=(65,85),(440,85),(440,265)
  l(*a,*b); l(*b,*c,S.DIF); path('M65,85 Q65,265 440,265',S.INK,'3 5')
  for q in (a,b,c): dot(*q)
  t(65,48,'Estipulante');t(440,48,'Promitente',anchor='end')
  t(440,302,'Beneficiário',anchor='end')
  t(252,73,'acordo',anchor='middle',size=14)
  t(425,178,'prestação',anchor='end',fill=S.DIF)
  t(65,226,'substituição',size=14);t(65,245,'se reservada',size=14)
  t(65,330,'Forma-se entre dois; cumpre-se em favor de outro.',size=14)
 elif m=='successive':
  W,H=600,310
  for y in (83,210): l(60,y,545,y,S.GRID)
  l(60,83,298,83);path('M298,83 C335,83 325,210 365,210',S.DIF);l(365,210,545,210,S.DIF)
  l(315,45,315,246,S.INK,'3 5');dot(60,83);dot(298,83);dot(365,210,S.DIF);dot(545,210,S.DIF)
  t(60,50,'Promitente');t(60,187,'Terceiro');t(330,32,'anuência',size=13)
  t(82,114,'obter o compromisso',size=14);t(382,240,'cumprir a prestação',size=14,fill=S.DIF)
  path('M298,83 Q290,147 210,147',S.CONC);t(65,156,'recusa: perdas e danos',size=13,fill=S.CONC)
  t(60,288,'Art. 440 · sem garantia adicional, a dívida muda de sujeito.',size=14)
 elif m=='retro':
  W,H=490,262
  # A ruled sheet of the lease, dated at its celebration; the nominee's film is laid over it and registers on its first line.
  # Drawn with open strokes (no closed boxes): sheet edges, ruled lines, a film marked by dashed edges and corner ticks.
  for x1,y1,x2,y2 in ((40,40,390,40),(40,40,40,245),(390,40,390,245),(40,245,390,245)): l(x1,y1,x2,y2,S.INK)
  t(58,68,'Locação',size=15,weight='600')
  for yy in (96,150,204): l(40,yy+14,390,yy+14,S.GRID)
  t(58,100,'locatário',size=14); t(150,100,'lojista',size=14,fill=S.MUTED); l(148,95,203,95,S.MUTED)
  t(58,154,'direitos',size=14); t(58,208,'obrigações',size=14)
  l(132,74,132,234,S.DIF,'6 4'); l(132,234,390,234,S.DIF,'6 4'); l(132,74,176,74,S.DIF); l(346,234,390,234,S.DIF)
  t(226,100,'pessoa nomeada',size=14,fill=S.DIF)
  for yy,name in ((60,'celebração'),(176,'nomeação')):
   l(390,yy+14,408,yy+14,S.INK); t(414,yy+19,name,size=14)
  path('M436,172 L436,96',S.DIF); path('M429,106 L436,94 L443,106',S.DIF)
 elif m=='arras':
  W,H=640,250
  # Four states (regime x who fails); the page script shows the one the reader has set. A is a symbolic unit, never a case amount.
  states=[('confirmatorias','recebeu',['A devolvido','A equivalente'],True,False),('confirmatorias','deu',['A retido'],True,False),
          ('penitenciais','recebeu',['A devolvido','A equivalente'],False,True),('penitenciais','deu',['A perdido'],False,True)]
  for reg,par,coins,ghost,limit in states:
   g=[]
   items=[(c,False) for c in coins]+([('suplemento, se provado',True)] if ghost else [])
   n=len(items); x0=320-(n-1)*105
   for i,(lab,gh) in enumerate(items):
    x=x0+i*210
    g.append(S.circle(x,98,46,fill=S.PAPER if not gh else 'none',stroke=S.INK if not gh else S.MUTED,stroke_width=1.8 if not gh else 1.4,stroke_dasharray='5 5' if gh else None))
    if not gh: g.append(S.circle(x,98,38,fill='none',stroke=S.GRID,stroke_width=1))
    g.append(S.text(x,108,'A' if not gh else '+',size=30,family=S.SANS,anchor='middle',fill=S.INK if not gh else S.MUTED))
    g.append(S.text(x,176,lab,size=16,family=S.SANS,anchor='middle',fill=S.INK if not gh else S.MUTED))
   if not ghost: pass
   if ghost:
    g.append(S.line(x0-50,206,x0+(n-2)*210+50,206,stroke=S.DIF,stroke_width=2.4))
    g.append(S.text(x0+(n-2)*105,232,'mínimo da indenização',size=15,family=S.SANS,anchor='middle',fill=S.DIF))
   if limit:
    xl=x0+(n-1)*210+86
    g.append(S.line(xl,40,xl,190,stroke=S.CONC,stroke_width=4))
    g.append(S.text(xl,214,'limite',size=15,family=S.SANS,anchor='middle',fill=S.CONC))
   o.append('<g data-arras="%s-%s" display="%s">'%(reg,par,'inline' if (reg,par)==('confirmatorias','recebeu') else 'none')+''.join(g)+'</g>')
 elif m=='history':
  W,H=960,274
  dates=[(1937,'Decreto-Lei 58: loteamentos'),(1939,'CPC: declaração de vontade suprida'),(1941,'Anteprojeto: duas formas'),(2002,'Código Civil: forma livre')]
  X=lambda yr:60+(yr-1937)/(2002-1937)*620
  for i,(yr,label) in enumerate(dates):
   y=38+i*48; last=(i==3); col=S.DIF if last else S.INK
   xe=900
   for p1,p2 in (((X(yr),y),(xe,y)),((X(yr),y+34),(xe,y+34)),((X(yr),y),(X(yr),y+34))): o.append(S.line(p1[0],p1[1],p2[0],p2[1],stroke=col,stroke_width=1.8))
   t(X(yr)+12,y+22,str(yr),size=15,weight='600'); t(X(yr)+62,y+22,label,size=14)
  l(60,236,900,236,S.GRID); t(60,260,'1937',size=13,fill=S.MUTED); t(900,260,'2002',size=13,fill=S.MUTED,anchor='end')
 elif m=='coins':
  W,H=540,235
  for x,r,label in [(130,50,'anel'),(390,30,'vintém')]:
   o.append(S.circle(x,95,r,fill='none',stroke=S.INK,stroke_width=2))
   o.append(S.circle(x,95,r-8,fill='none',stroke=S.INK,stroke_width=1))
   t(x,180,label,size=16,anchor='middle')
  t(270,221,'O pequeno valor confirma o acordo, sem comprar a saída.',size=15,anchor='middle')
 elif m=='historia':
  W,H=960,330
  # Three constructions, each a rail from its origin to the Civil Code of 2002 through one station between.
  XS=(250,560,860)
  t(XS[0],34,'ORIGEM',size=12,weight='600',anchor='middle');t(XS[1],34,'ENTRE',size=12,weight='600',anchor='middle');t(XS[2],34,'CÓDIGO CIVIL DE 2002',size=12,weight='600',anchor='middle')
  rows=[('terceiro','Terceiro','alteri stipulari nemo potest','dote e doação com encargo','ação direta do beneficiário'),
        ('preliminar','Preliminar','pactum de contrahendo','Decreto-Lei 58 de 1937','execução específica'),
        ('sinal','Sinal','arra como anel','confirmação e arrependimento','piso ou limite da indenização')]
  for i,(key,name,a1,a2,a3) in enumerate(rows):
   y=96+i*86; g=[]
   g.append(S.text(14,y+5,name,size=13,family=S.SANS,weight='600'))
   g.append(S.line(XS[0],y,XS[2],y,stroke=S.INK,stroke_width=3.5))
   g.append(S.rect(XS[0]-9,y-9,18,18,fill=S.INK,stroke=S.INK))
   g.append(S.circle(XS[1],y,8,fill=S.PAPER,stroke=S.INK,stroke_width=2.4))
   g.append(S.circle(XS[2],y,8,fill=S.PAPER,stroke=S.DIF,stroke_width=2.6))
   for x,lab,col in zip(XS,(a1,a2,a3),(S.INK,S.INK,S.DIF)):
    g.append(S.text(x,y-20,lab,size=12,family=S.SANS,fill=col,anchor='middle'))
   g.append(S.rect(0,y-34,W,66,fill=S.PAPER,opacity=0))
   o.append(f'<g class="thread" data-thread="{key}" role="button" tabindex="0" aria-label="Traçar {S.esc(name)}" aria-pressed="false">'+''.join(g)+'</g>')
 else: raise ValueError(m)
 return S.svg(W,H,'Relações e efeitos · '+m,o),[]
