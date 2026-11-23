"""Aula 02 force rose, cast through the planta part.

mode: 'rosa' (default). Five traceable rays relate Zeca's existing exclusivity
contract to freedom, binding force, relativity, social function and objective
good faith. A range control extends only the selected drawn ray; it assigns no
numerical weight to a principle. No arbitrary facts or legal rankings.
The desktop rose has a compact phone variant with the same topology.
"""
from __future__ import annotations
import math
import re
from . import svg as S
from . import planta

FORCES = [
 ('liberdade','Liberdade contratual','escolher e autovincular-se',-150,
  'A liberdade permite assumir o compromisso de exclusividade; a oportunidade posterior de contratar não o desfaz.'),
 ('forca','Força obrigatória','exigir o compromisso',-30,
  'Fischer e All-E podiam contar com o compromisso vigente: o descumprimento permitia exigir reparação.'),
 ('relatividade','Relatividade','a prestação cabe às partes',42,
  'A África não devia a prestação artística prometida pelo cantor, porque não era parte daquele contrato.'),
 ('social','Função social','respeitar o vínculo alheio',138,
  'O contrato integra a vida social: a interferência ilícita de quem conhece o vínculo pode gerar responsabilidade.'),
 ('conduta','Boa-fé objetiva','agir com lealdade',90,
  'A lealdade de conduta fundamenta o dever de respeito: conhecer a exclusividade e induzir sua ruptura pode constituir ilícito.')]

def rose(narrow=False):
    w,h = (340,420) if narrow else (1083,500)
    cx,cy=(170,190) if narrow else (541,205)
    o=[]
    # hollow terminals and orthogonal contact marks: shared planta grammar
    for key,label,note,angle,answer in FORCES:
        a=math.radians(angle); radius=76 if narrow else 172
        x,y=cx+radius*math.cos(a),cy+radius*math.sin(a)
        length=32 if narrow else 66
        o.append(f'<g data-thread="{key}" data-fio="{key}" role="button" tabindex="0" aria-pressed="false" aria-label="{S.esc(label)}">')
        o.append(S.line(cx,cy,x,y,stroke=S.INK,stroke_width=1.7))
        o.append(f'<g transform="translate({x:.1f},{y:.1f}) rotate({angle})"><g class="ray-extension">')
        o.append(S.line(0,0,length,0,stroke=S.CONC if key=='social' else S.INK,stroke_width=2))
        o.append(S.circle(length,0,4,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
        o.append('</g></g>')
        # labels stay fixed while only the contact's extension changes
        if narrow:
            pos={'liberdade':(10,69),'forca':(184,69),'relatividade':(184,310),'social':(10,310),'conduta':(170,385)}
            tx,ty=pos[key];anchor='middle' if key=='conduta' else 'start'
            words=label.split(); lines=[' '.join(words[:-1]),words[-1]] if len(words)>1 else [label]
            for i,line in enumerate(lines):o.append(S.text(tx,ty+i*17,line,size=13,family=S.SANS,anchor=anchor,weight='600'))
        else:
            ex=x+(length+10)*math.cos(a);ey=y+(length+10)*math.sin(a)
            if key=='conduta': tx,ty,anchor=541,ey+22,'middle'
            elif math.cos(a)<0: tx,ty,anchor=ex-6,ey+4,'end'
            else: tx,ty,anchor=ex+6,ey+4,'start'
            o.append(S.text(tx,ty,label,size=14,family=S.SANS,weight='600',anchor=anchor))
            o.append(S.text(tx,ty+20,note,size=13,family=S.SERIF,anchor=anchor,fill=S.INK2))
        o.append(S.circle(x,y,3.5,fill=S.PAPER,stroke=S.INK,stroke_width=1.4))
        o.append('</g>')
    # the junction represents the existing contract; no invented monetary weights
    bw,bh=(118,68) if narrow else (176,66)
    o.append(S.rect(cx-bw/2,cy-bh/2,bw,bh,fill=S.PAPER,stroke=S.INK,stroke_width=1.5,data_lk='liberdade forca relatividade social conduta'))
    o.append(S.text(cx,cy-8,'Zeca · Nova Schin',size=13,family=S.SANS,anchor='middle',weight='600'))
    o.append(S.line(cx-bw/2+12,cy+2,cx+bw/2-12,cy+2,stroke=S.GRID,stroke_width=1))
    o.append(S.text(cx,cy+22,'exclusividade vigente',size=12 if narrow else 13,family=S.SERIF,anchor='middle'))
    return S.svg(w,h,'Cinco forças incidentes no mesmo contrato de exclusividade',o)

def build(p:dict)->tuple[str,list[dict]]:
    if p.get('mode')!='rosa':
        q=dict(p)
        x,y,w,h=q.pop('crop',[50,104,1083,340])
        drawing,objects=planta.build(q)
        drawing=re.sub(r'viewBox="[^"]*"',f'viewBox="{x} {y} {w} {h}"',drawing,count=1)
        drawing=re.sub(r'font-size="(1[12](?:\.5)?)"','font-size="13"',drawing)
        return drawing,objects
    desktop=rose();mobile=rose(True)
    answers=''.join(f'<p data-answer="{k}"'+('' if i==0 else ' hidden')+'>'+S.esc(a)+'</p>' for i,(k,l,n,g,a) in enumerate(FORCES))
    return ('<div class="force-rose"><div class="rose-desktop">'+desktop+'</div><div class="rose-mobile">'+mobile+'</div><div class="force-readout">'+answers+'</div><label class="trace-length">Extensão gráfica do raio <input type="range" min="0.7" max="1.3" step="0.05" value="1" aria-label="Extensão gráfica do raio selecionado"></label></div>',[])
