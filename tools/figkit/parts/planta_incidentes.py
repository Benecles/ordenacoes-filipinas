"""Lesson-specific planta: five contractual threads sharing formation and effects.
Params: none. Based on planta's hollow stations and traced legal threads.
Five rows are alternatives, not consecutive phases. Source: CC436–440,
462–471,417–420; Pereira III §§198–206-A. No invented factual events.
"""
from . import svg as S

def build(p):
 o=[]; W,H=1080,390
 def t(x,y,s,**kw): return S.text(x,y,s,size=13,family=S.SANS,**kw)
 o += [t(270,28,'ACORDO'),t(555,28,'QUEM ENTRA / O QUE SE ADIA'),t(910,28,'EFEITO')]
 rows=[('favor','Estipulação', 'benefício ao terceiro','direito próprio','436–438'),('fato','Promessa', 'compromisso do terceiro','devedor sucessivo','439–440'),('pessoa','Pessoa a declarar','posição contratual inteira','substituição retroativa','467–471'),('preliminar','Contrato preliminar','contrato definitivo','direito de exigir','462–466'),('arras','Arras','entrega do sinal','piso ou limite','417–420')]
 for i,(key,label,middle,end,art) in enumerate(rows):
  y=73+i*64
  body=[t(12,y+5,label),S.line(245,y,1005,y,stroke=S.INK,stroke_width=1.4),S.circle(270,y,6,fill=S.PAPER,stroke=S.INK,stroke_width=2),S.circle(565,y,6,fill=S.PAPER,stroke=S.INK,stroke_width=2),S.rect(985,y-6,12,12,fill=S.PAPER,stroke=S.INK,stroke_width=1.5),S.rect(579,y-15,290,29,fill=S.PAPER),t(585,y+5,middle),S.rect(882,y-13,185,27,fill=S.PAPER),t(898,y+5,end),t(270,y+23,'CC '+art,fill=S.MUTED)]
  body += [S.rect(0,y-24,1080,54,fill=S.PAPER,opacity=0)]
  o.append(f'<g class="thread" data-thread="{key}" role="button" tabindex="0" aria-label="Traçar {S.esc(label)}" aria-pressed="false">'+''.join(body)+'</g>')
 return S.svg(W,H,'Cinco vínculos: quem recebe, quem deve, quem substitui e o que se adia',o),[]
