"""Aula01, qualitative axis field: economic destination x proven vulnerability.

No params. Horizontal endpoints are uses, vertical positions are proof states,
not measured degrees of vulnerability. STJ local reading pp.1–4, slides p.24.
The insurance marker occupies the destination column without claiming a
judicial finding about a numerical degree of vulnerability.
"""
from . import svg as S


def build(p):
    o=[]; T=S.text
    o += [S.line(110,305,790,305,stroke=S.INK,stroke_width=1.4),
          S.line(110,305,110,40,stroke=S.INK,stroke_width=1.4),
          S.path('M785,300 L790,305 L785,310 M105,45 L110,40 L115,45',fill='none',stroke=S.INK),
          S.line(465,60,465,305,stroke=S.INK2,stroke_dasharray='3 6'),
          T(130,30,'Vulnerabilidade do adquirente profissional',size=14,family=S.SANS),
          T(95,100,'provada',size=13,anchor='end'),T(95,265,'sem prova',size=13,anchor='end'),
          T(280,334,'Uso na atividade produtiva',size=13,anchor='middle'),
          T(630,334,'Uso próprio · fora da atividade',size=13,anchor='middle'),
          T(280,356,'Maximalismo: basta a destinação fática',size=11.5,anchor='middle',fill=S.INK2),
          T(630,356,'Finalismo: destinação fática e econômica',size=11.5,anchor='middle',fill=S.INK2),
          S.circle(280,100,6,fill=S.PAPER,stroke=S.INK,stroke_width=1.8),
          T(280,127,'Uso profissional + vulnerabilidade provada',size=13,family=S.SANS,anchor='middle'),
          T(280,149,'pode atrair o CDC no caso concreto',size=13,anchor='middle',fill=S.INK2),
          S.circle(280,260,6,fill=S.PAPER,stroke=S.CONC,stroke_width=1.8),
          T(280,230,'Ingressos · capital de giro',size=14,family=S.SANS,anchor='middle'),
          T(280,284,'CDC afastado nos casos julgados',size=12,anchor='middle',fill=S.CONC),
          S.path('M520,75 L520,280 M520,177 L560,177',fill='none',stroke=S.DIF,stroke_width=1.8),
          S.circle(560,177,6,fill=S.PAPER,stroke=S.DIF,stroke_width=1.8),
          T(580,169,'Seguro da frota',size=15,family=S.SANS,fill=S.DIF),
          T(580,192,'transportadora consumidora',size=13,fill=S.DIF),
          T(580,218,'cobertura continua delimitada',size=12,fill=S.CONC),
          T(110,390,'Posições qualitativas; altura indica prova, sem escala numérica',size=12,fill=S.INK2)]
    return S.svg(870,405,'Correntes de destinação final e exame separado da vulnerabilidade concreta',o),[]
