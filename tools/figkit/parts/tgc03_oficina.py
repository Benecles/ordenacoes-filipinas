"""Boa-fé e formação: desenhos de relações, contagem e correspondência.

Params: mode=tally|ruptura|encaixe|correio|informacao.
`tally` accepts count (default36), computed rows of six payment marks.
`correio` draws logical stages, NOT a measured elapsed time; the adjacent
range control changes the arrival of withdrawal relative to acceptance.
`informacao` draws the accessible informational field with a variable boundary.
All facts: TJRS71001586668 pp1–6; STJ1367955 pp9–11; CC427–435;
Versiani pp13–14. No invented dates, amounts or geographical distances.
"""
from . import svg as S

def build(p):
 mode=p.get('mode','tally'); o=[]; T=S.text
 def line(a,b,c,d,**kw):return S.line(a,b,c,d,stroke=S.INK,stroke_width=1.4,**kw)
 if mode=='tally':
  n=int(p.get('count',36)); w,h=460,270
  for i in range(n):
   x=48+(i%6)*55;y=58+(i//6)*30
   o += [S.circle(x,y,7,fill='none',stroke=S.INK,stroke_width=1.3),S.path(f'M{x-3},{y} l2,3 l5,-7',fill='none',stroke=S.INK,stroke_width=1.4)]
  o += [T(47,27,'36 pagamentos',size=18,family=S.SERIF),line(25,39,25,222),line(25,222,365,222),T(47,247,'a cobrança repetida sustenta a confiança',size=14,family=S.SERIF),S.path('M385,58 L385,208 M379,58 L391,58 M379,208 L391,208',fill='none',stroke=S.CONC,stroke_width=2),T(403,145,'saldo',size=13,fill=S.CONC),T(403,165,'tardio',size=13,fill=S.CONC)]
 elif mode=='ruptura':
  w,h=840,245
  o += [T(25,30,'Asti',size=17,family=S.SERIF),T(25,212,'CBD',size=17,family=S.SERIF)]
  o += [S.path('M80,62 C160,62 180,90 270,90 L465,90',fill='none',stroke=S.INK,stroke_width=2),S.path('M80,178 C160,178 180,150 270,150 L465,150',fill='none',stroke=S.INK,stroke_width=2)]
  for x in [230,330,430]:
   o += [line(x,90,x,150,stroke_dasharray='3 4'),S.circle(x,90,4,fill=S.PAPER,stroke=S.INK),S.circle(x,150,4,fill=S.PAPER,stroke=S.INK)]
  o += [T(220,68,'reuniões',size=13),T(315,190,'preparação',size=13),S.path('M480,72 l20,18 l-20,18 M480,132 l20,18 l-20,18',fill='none',stroke=S.CONC,stroke_width=2),T(506,124,'ruptura',size=15,fill=S.CONC),S.path('M430,150 C445,210 560,210 617,182',fill='none',stroke=S.DIF,stroke_width=2),T(570,228,'reparar despesas comprovadas',size=14,fill=S.DIF),line(666,55,666,165,stroke_dasharray='3 6'),T(690,97,'contrato',size=16,family=S.SERIF,fill=S.MUTED),T(690,121,'não celebrado',size=14,family=S.SERIF,fill=S.MUTED)]
 elif mode=='encaixe':
  w,h=580,220
  o += [S.path('M30,70 H175 V55 H200 V70 H310 V100 H295 V120 H310 V150 H200 V165 H175 V150 H30 Z',fill='none',stroke=S.INK,stroke_width=1.7),S.path('M335,70 H425 V55 H450 V70 H550 V150 H450 V165 H425 V150 H335 V120 H320 V100 H335 Z',fill='none',stroke=S.INK,stroke_width=1.7),T(55,108,'proposta completa',size=18,family=S.SERIF),T(55,132,'termos essenciais definidos',size=13),T(356,108,'aceitação',size=18,family=S.SERIF),T(356,132,'nos mesmos termos',size=13),T(30,193,'o assentimento basta para fechar o acordo',size=16,family=S.SERIF)]
 elif mode=='correio':
  w,h=900,300
  xs=[90,310,570,810]
  labels=['declarar','expedir','receber','conhecer']
  o += [line(xs[0],105,xs[-1],105),line(xs[0],211,xs[-1],211)]
  for x,l in zip(xs,labels):
   o += [line(x,92,x,118),line(x,199,x,220),T(x,70,l,size=15,anchor='middle'),S.circle(x,105,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.5)]
  o += [S.path('M310,105 C385,105 465,211 570,211',fill='none',stroke=S.INK,stroke_width=2),T(592,160,'aceitação',size=16,family=S.SERIF),T(40,32,'aceitante',size=15,family=S.SERIF),T(40,258,'proponente',size=15,family=S.SERIF),S.path('M340,105 C430,105 445,185 535,211',fill='none',stroke=S.CONC,stroke_width=2,data_withdraw='path'),S.circle(535,211,7,fill=S.PAPER,stroke=S.CONC,stroke_width=2,data_withdraw='dot'),T(490,281,'retratação chega antes: aceitação inexistente',size=14,fill=S.CONC,data_withdraw='label')]
 elif mode=='informacao':
  w,h=660,210
  for x in range(40,621,20): o.append(line(x,75,x,85 if x%100 else 93))
  o += [line(40,75,620,75),T(40,38,'informação acessível',size=18,family=S.SERIF),T(40,134,'cada parte diligencia seus interesses',size=16,family=S.SERIF),S.path('M350,59 V110 M345,59 H355',fill='none',stroke=S.INK,stroke_width=2,data_info='boundary'),T(40,182,'confiança particular pode ampliar o dever de informar',size=16,family=S.SERIF)]
 else: raise ValueError(mode)
 return S.svg(w,h,{'tally':'Trinta e seis boletos pagos','ruptura':'Tratativas interrompidas antes do contrato','encaixe':'Encaixe de proposta e aceitação','correio':'Quatro marcos lógicos da comunicação','informacao':'Âmbito contextual do dever de informar'}[mode],o),[]
