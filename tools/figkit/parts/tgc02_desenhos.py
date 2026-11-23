"""Aula 02's two chapter plates.

mode 'regua': four rulers of legal reach, stops correspond to distinct limits,
not numerical measurements. Pereira pp.21–27, Venosa p.9, CDC39 II/IX.
mode 'normas': stacked norms plate (CC421,421-A caput/I-II,2035 sole paragraph).
Both modes return desktop and phone variants. No remote assets or scripts.
"""
from __future__ import annotations
from . import svg as S

def regua(narrow):
    w,h=(340,450) if narrow else (800,340)
    x0,end=(16,236) if narrow else (270,560)
    o=[]
    rows=[('Contratar ou recusar','estoque · CDC 39',0),('Escolher a contraparte','monopólio',1),('Definir a modalidade','limites legais',2),('Estipular o conteúdo','norma cogente',3)]
    for name,limit,i in rows:
        y=(52+i*104) if narrow else (48+i*82)
        o.append(S.text(16,y-20 if narrow else y-4,name,size=16 if narrow else 18,family=S.SERIF))
        yy=y+12 if narrow else y
        o.append(S.line(x0,yy,end,yy,stroke=S.INK,stroke_width=2))
        o.append(S.line(x0,yy+10,end,yy+10,stroke=S.INK2,stroke_width=1))
        for k in range(13):
            x=x0+(end-x0)*k/12
            o.append(S.line(x,yy,x,yy+(10 if k%3==0 else 5),stroke=S.INK2,stroke_width=1))
        o.append(S.circle(x0,yy,4,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
        o.append(S.line(end,yy-15,end,yy+15,stroke=S.CONC,stroke_width=2.5))
        o+=S.hatch(end,yy-15,23,30,step=7,stroke=S.CONC,stroke_width=1)
        o.append(S.text(x0 if narrow else end+36,yy+38 if narrow else yy+5,limit,size=14,family=S.SANS,fill=S.INK2))
    return S.svg(w,h,'Quatro escolhas, cada qual limitada em seu alcance jurídico, sem escala numérica',o)

def normas(narrow):
    w,h=(340,470) if narrow else (800,372)
    o=[]
    # Ascending offset exposes each normative layer without hiding lower norms.
    sheets=[(14,118,300,302) if narrow else (56,96,666,218),
            (30,78,284,260) if narrow else (88,58,634,192),
            (46,36,268,210) if narrow else (120,20,602,168)]
    for i,(x,y,ww,hh) in enumerate(sheets):
        o.append(S.rect(x,y,ww,hh,fill=S.PAPER,stroke=S.INK,stroke_width=1.3))
        o.append(S.line(x+14,y+hh-54,x+ww-14,y+hh-54,stroke=S.GRID,stroke_width=1))
    x,y,ww,hh=sheets[2]
    lines=['CC 421 · liberdade contratual','nos limites da função social','intervenção mínima', 'revisão excepcional']
    for i,t in enumerate(lines):o.append(S.text(x+16,y+30+i*(35 if narrow else 31),t,size=13 if narrow else 16,family=S.SERIF if i else S.SANS,weight='600' if i==0 else None))
    x,y,ww,hh=sheets[1];yy=y+hh-32
    o.append(S.text(x+14,yy,'421-A · paridade presumida',size=13 if narrow else 15,family=S.SANS))
    o.append(S.text(x+14,yy+20,'ressalva dos regimes especiais',size=13,family=S.SERIF))
    x,y,ww,hh=sheets[0];yy=y+hh-32
    o.append(S.text(x+14,yy,'2.035 p.u. · ordem pública',size=13 if narrow else 15,family=S.SANS))
    o.append(S.text(x+14,yy+20,'a convenção não pode afastá-la',size=13,family=S.SERIF))
    # Alignment marks indicate one common field, not repeal or priority by chronology.
    o.append(S.line(8,h-34,w-12,h-34,stroke=S.INK2,stroke_width=1))
    o.append(S.text(14,h-12,'Normas que incidem em conjunto',size=13,family=S.SERIF,fill=S.INK2))
    return S.svg(w,h,'Placa sobreposta de normas: liberdade, presunção relativa e ordem pública coexistem',o)

def build(p:dict)->tuple[str,list[dict]]:
    mode=p.get('mode','regua'); fn={'regua':regua,'normas':normas}[mode]
    return ('<div class="drawing-desktop">'+fn(False)+'</div><div class="drawing-mobile">'+fn(True)+'</div>',[])
