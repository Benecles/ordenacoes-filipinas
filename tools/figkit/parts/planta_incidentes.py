"""Lesson-specific planta: one agreement, five incidents wired to it (Aula 04, Incidentes da formação do contrato).
Params: none. Read as an electrical plan: the vertical bus is the agreement; each row taps it between two parties (A, B)
and shows what the incident displaces: the one who receives (third dot), the one who owes (a gap before the dot),
the one who is party (a swap with a retroactive return), the moment of the main contract (a dashed run to a later
flag), the thing handed over (a coin and a fork). Alternatives, not phases. Source: CC436-440, 462-471, 417-420;
Pereira III §§198-206-A. No invented factual events. Every position is computed from the row index.
"""
from . import svg as S

def build(p):
 o=[]; W,H=1080,424
 def t(x,y,s,size=14,**kw): return S.text(x,y,s,size=size,family=S.SANS,**kw)
 BUS,XA,XB,XC,XE=215,262,372,560,712
 Y0,DY=92,72
 o += [S.line(BUS,62,BUS,H-26,stroke=S.INK,stroke_width=5)]
 o += [t(BUS+8,34,'ACORDO',size=13,weight='600',anchor='end',letter_spacing='.08em'),
       t(XA,34,'A',size=14,weight='600',anchor='middle'), t(XB,34,'B',size=14,weight='600',anchor='middle'),
       t(XE,34,'EFEITO',size=13,weight='600',letter_spacing='.08em')]
 def dot(x,y,dash=None,r=7): return S.circle(x,y,r,fill=S.PAPER,stroke=S.INK,stroke_width=2.2,stroke_dasharray=dash)
 rows=[('favor','Estipulação','436–438'),('fato','Promessa de fato de terceiro','439–440'),('pessoa','Pessoa a declarar','467–471'),('preliminar','Contrato preliminar','462–466'),('arras','Arras','417–420')]
 for i,(key,label,art) in enumerate(rows):
  y=Y0+i*DY
  b=[t(12,y-3,label,weight='600'),t(12,y+16,'CC '+art,size=13,fill=S.MUTED)]
  b+=[S.rect(BUS-6,y-6,12,12,fill=S.PAPER,stroke=S.INK,stroke_width=2),S.line(BUS+6,y,XA,y,stroke=S.INK,stroke_width=2)]
  if key=='favor':
   b+=[S.line(XA,y,XB,y,stroke=S.INK,stroke_width=2),dot(XA,y),dot(XB,y),
       S.line(XB,y,XC,y,stroke=S.DIF,stroke_width=2.6),dot(XC,y),
       t(XC,y-14,'beneficiário',size=13,anchor='middle'),
       t(XE,y+5,'direito próprio do beneficiário',fill=S.DIF)]
  elif key=='fato':
   b+=[S.line(XA,y,XB,y,stroke=S.INK,stroke_width=2),dot(XA,y),dot(XB,y),
       S.line(XB,y,452,y,stroke=S.INK,stroke_width=2,stroke_dasharray='3 5'),
       S.line(462,y-12,462,y+12,stroke=S.CONC,stroke_width=3),S.line(470,y-12,470,y+12,stroke=S.CONC,stroke_width=3),
       S.line(480,y,XC-8,y,stroke=S.INK,stroke_width=2,stroke_dasharray='3 5'),dot(XC,y,'3 2'),
       S.line(XC+8,y,640,y,stroke=S.DIF,stroke_width=2.6),
       t(466,y-18,'anuência do terceiro',size=13,anchor='middle'),
       S.path(f'M466,{y+12} C466,{y+28} 490,{y+26} 520,{y+26}',fill='none',stroke=S.CONC,stroke_width=1.6),
       S.rect(520,y+21,10,10,fill=S.PAPER,stroke=S.CONC,stroke_width=1.8),
       t(538,y+31,'recusa: perdas e danos',size=13,fill=S.CONC),
       t(XE,y+5,'devedor sucessivo, depois da anuência',fill=S.DIF)]
  elif key=='pessoa':
   b+=[S.line(XA,y,XB,y,stroke=S.INK,stroke_width=2),
       S.circle(XA,y,7,fill=S.PAPER,stroke=S.MUTED,stroke_width=2),
       S.line(XA-5,y-5,XA+5,y+5,stroke=S.MUTED,stroke_width=2),S.line(XA-5,y+5,XA+5,y-5,stroke=S.MUTED,stroke_width=2),
       dot(XB,y),dot(XA+34,y+26),S.line(XA+34,y+26,XB,y+4,stroke=S.DIF,stroke_width=2.6),
       S.path(f'M{XA+28},{y+22} C{XA+4},{y+22} {BUS+14},{y+18} {BUS+8},{y+9}',fill='none',stroke=S.DIF,stroke_width=1.6,stroke_dasharray='4 4'),
       t(XA+48,y+31,'pessoa nomeada',size=13),
       t(XE,y+5,'posição inteira, desde a celebração',fill=S.DIF)]
  elif key=='preliminar':
   b+=[S.line(XA,y,XB,y,stroke=S.INK,stroke_width=2),dot(XA,y),dot(XB,y),
       S.rect(XB+16,y-6,12,12,fill=S.PAPER,stroke=S.INK,stroke_width=2),
       S.line(XB+28,y,640,y,stroke=S.INK,stroke_width=2,stroke_dasharray='3 7'),
       S.line(640,y-14,640,y+14,stroke=S.INK,stroke_width=2),S.path(f'M640,{y-14} L664,{y-8} L640,{y-2}',fill=S.PAPER,stroke=S.INK,stroke_width=1.8),
       t(500,y-14,'contrato adiado',size=13,anchor='middle'),
       t(XE,y+5,'direito de exigir o definitivo',fill=S.DIF)]
  else:
   b+=[S.line(XA,y,XB,y,stroke=S.INK,stroke_width=2),dot(XA,y),dot(XB,y),
       S.circle(317,y,10,fill=S.PAPER,stroke=S.INK,stroke_width=2.2),S.circle(317,y,5,fill='none',stroke=S.INK,stroke_width=1.4),
       t(317,y-18,'sinal',size=13,anchor='middle'),
       S.path(f'M{XB},{y} C{XB+50},{y} {XB+60},{y-14} {XB+110},{y-14} L640,{y-14}',fill='none',stroke=S.DIF,stroke_width=2.6),
       S.path(f'M{XB},{y} C{XB+50},{y} {XB+60},{y+14} {XB+110},{y+14} L640,{y+14}',fill='none',stroke=S.CONC,stroke_width=2.6),
       t(XE,y-9,'confirmatória: piso da indenização',fill=S.DIF),
       t(XE,y+19,'penitencial: limite da saída',fill=S.CONC)]
  b+=[S.rect(0,y-34,W,68,fill=S.PAPER,opacity=0)]
  o.append(f'<g class="thread" data-thread="{key}" role="button" tabindex="0" aria-label="Traçar {S.esc(label)}" aria-pressed="false">'+''.join(b)+'</g>')
 return S.svg(W,H,'Um acordo e cinco incidentes: quem recebe, quem deve, quem é parte, quando se contrata e o que se entrega',o),[]
