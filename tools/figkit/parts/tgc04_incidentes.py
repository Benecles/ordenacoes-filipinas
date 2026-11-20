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
  W,H=540,350
  # Formation across the top; performance descends to the third point.
  a,b,c=(65,85),(440,85),(440,265)
  l(*a,*b); l(*b,*c,S.DIF); path('M65,85 Q65,265 440,265',S.INK,'3 5')
  for q in (a,b,c): dot(*q)
  t(65,48,'Estipulante');t(440,48,'Promitente',anchor='end')
  t(440,302,'Beneficiário',anchor='end')
  t(252,73,'acordo',anchor='middle',size=13)
  t(425,178,'prestação',anchor='end',fill=S.DIF)
  t(65,226,'substituição',size=13);t(65,245,'se reservada',size=13)
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
  W,H=600,295
  l(55,80,540,80);l(55,205,540,205,S.DIF);l(55,53,55,230,S.GRID);l(495,53,495,230,S.GRID)
  t(55,35,'celebração',size=13);t(495,35,'nomeação',size=13,anchor='middle')
  dot(55,80);dot(495,80);dot(495,205,S.DIF);dot(55,205,S.DIF)
  path('M495,195 C390,125 170,125 55,195',S.DIF)
  path('M65,180 L55,195 L76,194',S.DIF)
  t(74,109,'contratante originário',size=15);t(74,235,'pessoa nomeada',size=15,fill=S.DIF)
  t(280,157,'efeito retroativo',size=14,anchor='middle',fill=S.DIF)
  t(55,280,'Uma posição inteira; direitos e obrigações desde o início.',size=14)
 elif m=='arras':
  W,H=640,260
  # The principal is a physical counter; second counter is the equivalent.
  for i in range(2):
   x=180+i*220
   o.append(S.circle(x,110,54,fill=S.PAPER,stroke=S.INK,stroke_width=1.6))
   o.append(S.circle(x,110,46,fill='none',stroke=S.GRID,stroke_width=1))
   t(x,119,'A',size=30,anchor='middle')
   t(x,190,'sinal recebido' if i==0 else 'equivalente',size=15,anchor='middle')
  t(290,119,'+',size=30,anchor='middle');l(100,217,480,217)
  t(290,245,'devolução + indenização',size=15,anchor='middle')
 elif m=='history':
  W,H=1000,240
  dates=[(1937,'Loteamentos'),(1939,'Declaração suprida'),(1941,'Duas formas'),(2002,'Forma livre')]
  X=lambda yr:80+(yr-1937)/(2002-1937)*830
  l(80,122,910,122)
  for i,(yr,label) in enumerate(dates):
   x=X(yr);dot(x,122,S.DIF if yr==2002 else S.INK)
   tx,y=[(80,35),(250,183),(470,35),(910,183)][i]
   l(x,122,tx,y+30 if i%2==0 else y-18,S.GRID)
   anchor='start' if i<3 else 'end'
   t(tx,y,str(yr),size=15,anchor=anchor)
   t(tx,y+22,label,size=14,anchor=anchor)
  t(80,231,'Distâncias proporcionais ao tempo · Pereira, pp.79–80',size=13)
 elif m=='coins':
  W,H=540,235
  for x,r,label in [(130,50,'anel'),(390,30,'vintém')]:
   o.append(S.circle(x,95,r,fill='none',stroke=S.INK,stroke_width=2))
   o.append(S.circle(x,95,r-8,fill='none',stroke=S.INK,stroke_width=1))
   t(x,180,label,size=15,anchor='middle')
  t(270,221,'O pequeno valor confirma o acordo, sem comprar a saída.',size=14,anchor='middle')
 else: raise ValueError(m)
 return S.svg(W,H,'Relações e efeitos · '+m,o),[]
