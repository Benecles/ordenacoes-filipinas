"""Aula05: desenhos próprios das consequências da classificação.
params: mode = rede | prazo | aguada | tempo | contas.
rede: rede sem captura; a escolha do risco é feita em controles HTML adjacentes.
prazo: duas réguas computadas, 30 e90 dias do CDC26, escala comum.
aguada: esquema qualitativo, sem escala, da fazenda de criar de Pereira p130.
tempo: marcas pontuais versus prestação contínua, sem datas inventadas.
contas: escrituração das rubricas de restituição do CC450–454, sem valores fictícios.
"""
from . import svg as S

def build(p):
 mode=p['mode']; o=[]; T=S.text
 if mode=='rede':
  w,h=620,280
  # A net is empty whichever legal risk was bought: the visible absence is the argument.
  o += [S.path('M125,55 Q310,335 495,55',fill='none',stroke=S.INK,stroke_width=2),S.line(125,55,495,55,stroke=S.INK,stroke_width=2)]
  for i in range(1,12):
   t=i/12; x=125+370*t; bottom=55+140*4*t*(1-t)
   o.append(S.line(x,55,x,bottom,stroke=S.MUTED,stroke_width=1))
  for y in [85,115,145,175]:
   # horizontal strings terminate within the bowl of the net
   t=(1-(max(0,1-(y-55)/140))**.5)/2; a=125+370*t
   o.append(S.line(a,y,620-a,y,stroke=S.MUTED,stroke_width=1))
  o += [T(310,28,'O lanço não trouxe peixe',size=22,family=S.SERIF,anchor='middle'),T(310,251,'A rede vazia é o mesmo fato; o risco contratado muda o preço.',size=16,family=S.SERIF,anchor='middle')]
 elif mode=='prazo':
  w,h=620,235; left=115; scale=4.7
  for i,(n,label) in enumerate([(30,'Não durável'),(90,'Durável')]):
   y=65+i*80
   o += [T(16,y+5,label,size=14,family=S.SANS),S.line(left,y,left+90*scale,y,stroke=S.GRID,stroke_width=1)]
   for d in range(0,91,10):o.append(S.line(left+d*scale,y-5,left+d*scale,y+5,stroke=S.MUTED,stroke_width=1))
   o += [S.line(left,y,left+n*scale,y,stroke=S.INK,stroke_width=4),S.line(left+n*scale,y-14,left+n*scale,y+14,stroke=S.CONC,stroke_width=2),T(left+n*scale,y-23,f'{n} dias',size=15,anchor='middle')]
  o += [T(115,210,'Vício oculto: o prazo parte da evidência do defeito.',size=17,family=S.SERIF)]
 elif mode=='aguada':
  w,h=620,390
  boundary='M60,75 L490,45 L555,160 L520,315 L90,335 L45,195 Z'
  o.append(S.path(boundary,fill='none',stroke=S.INK,stroke_width=2))
  # small strip contains the source's sole economically essential feature; no area figure.
  o.append(S.path('M490,45 L555,160 L538,231 L469,233 L447,140 Z',fill='none',stroke=S.CONC,stroke_width=2))
  for x in range(464,526,12):o.append(S.line(x,126,x+4,204,stroke=S.CONC,stroke_width=.7,opacity=.4))
  o.append(S.path('M472,163 C480,147 503,144 518,162 C529,180 510,193 490,187 C478,184 467,177 472,163 Z',fill='none',stroke=S.DIF,stroke_width=2))
  for y in [166,173,180]:o.append(S.path(f'M480,{y} q9,-4 18,0 t16,0',fill='none',stroke=S.DIF,stroke_width=1))
  o += [T(235,185,'Fazenda de criar',size=24,family=S.SERIF,anchor='middle'),T(397,113,'aguada',size=17,family=S.SERIF),S.line(448,117,481,151,stroke=S.INK,stroke_width=1),T(310,371,'Perda pequena em área; decisiva para a criação. Esquema sem escala.',size=15,family=S.SERIF,anchor='middle')]
 elif mode=='tempo':
  w,h=940,310
  for y,label in [(65,'Imediata'),(145,'Diferida'),(225,'Continuada')]:
   o += [T(20,y+5,label,size=17,family=S.SANS),S.line(190,y,900,y,stroke=S.GRID,stroke_width=1),S.line(210,y-14,210,y+14,stroke=S.INK,stroke_width=1)]
  for x,y in [(210,65),(590,145)]:
   o.append(S.circle(x,y,9,fill=S.INK))
  o += [S.line(210,225,870,225,stroke=S.INK,stroke_width=5)]
  for x in range(320,871,110):o.append(S.line(x,213,x,237,stroke=S.INK,stroke_width=2))
  o += [T(210,29,'celebração',size=14,anchor='middle'),T(610,106,'cumprimento único',size=15),T(510,190,'uso mantido e prestações periódicas',size=16),T(190,285,'O tempo apenas adia a compra; integra a prestação da locação.',size=18,family=S.SERIF)]
 elif mode=='contas':
  w,h=620,310
  o += [S.line(38,52,582,52,stroke=S.INK,stroke_width=2),S.line(150,52,150,280,stroke=S.INK,stroke_width=1)]
  for i,(a,b) in enumerate([('+','valor da coisa na evicção'),('+','frutos restituídos e prejuízos diretos'),('+','despesas, custas e honorários'),('+','benfeitorias úteis ou necessárias não abonadas'),('−','vantagens já recebidas, quando dedutíveis')]):
   y=86+i*44;o.extend([S.line(38,y+17,582,y+17,stroke=S.GRID,stroke_width=1),T(95,y,a,size=25,anchor='middle'),T(170,y,b,size=16,family=S.SERIF)])
  o.append(T(38,28,'Recompor o patrimônio sem duplicar o reembolso',size=20,family=S.SERIF))
 else:raise ValueError(mode)
 return S.svg(w,h,'Aula05 · '+mode,o),[]
