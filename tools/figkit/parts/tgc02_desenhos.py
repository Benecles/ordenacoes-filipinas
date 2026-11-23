"""Aula 02's two chapter plates.

mode 'regua': survey plan of one plot, four sides each closed its own way (gate, wall, stones,
band), no numerical scale. Pereira pp.21–27, Venosa p.9, CDC39 II/IX.
mode 'normas': stacked norms plate (CC421,421-A caput/I-II,2035 sole paragraph).
Both modes return desktop and phone variants. No remote assets or scripts.
"""
from __future__ import annotations
from . import svg as S

def regua(narrow):
    """Survey plan of one plot: the party's field, each of its four sides closed in its own way."""
    if narrow:
        w,h=340,372; px,py,pw,ph=96,72,140,214; wall=16; strip=36; fs=15; ls=13
    else:
        w,h=800,344; px,py,pw,ph=270,64,260,218; wall=22; strip=56; fs=18; ls=14
    o=[]
    cx=px+pw/2; cy=py+ph/2
    # left side: a mandatory band already occupies the edge of the plot (norma cogente)
    o+=S.hatch(px,py,strip,ph,step=7,stroke=S.CONC,stroke_width=1)
    o.append(S.line(px+strip,py,px+strip,py+ph,stroke=S.CONC,stroke_width=2.5))
    o.append(S.line(px,py,px,py+ph,stroke=S.INK,stroke_width=2))
    # top side: the boundary opens where the supplier must serve (estoque, CDC 39)
    gw=pw*0.34; g0=cx-gw/2; g1=cx+gw/2
    o.append(S.line(px,py,g0,py,stroke=S.INK,stroke_width=2))
    o.append(S.line(g1,py,px+pw,py,stroke=S.INK,stroke_width=2))
    o.append(S.line(g0,py-9,g0,py+9,stroke=S.CONC,stroke_width=2.5))
    o.append(S.line(g1,py-9,g1,py+9,stroke=S.CONC,stroke_width=2.5))
    o.append(S.line(g0,py,g0,py+gw,stroke=S.INK2,stroke_width=1.5))
    o.append(S.path(f"M{g1:.1f} {py} A{gw:.1f} {gw:.1f} 0 0 0 {g0:.1f} {py+gw:.1f}",fill="none",stroke=S.INK2,stroke_width=1,stroke_dasharray="3 3"))
    # right side: a wall of mass supply with one narrow gate (monopolio)
    gy0=cy-ph*0.1; gy1=cy+ph*0.1
    o+=S.hatch(px+pw,py,wall,gy0-py,step=7,stroke=S.CONC,stroke_width=1)
    o+=S.hatch(px+pw,gy1,wall,py+ph-gy1,step=7,stroke=S.CONC,stroke_width=1)
    o.append(S.line(px+pw,py,px+pw,gy0,stroke=S.INK,stroke_width=2))
    o.append(S.line(px+pw,gy1,px+pw,py+ph,stroke=S.INK,stroke_width=2))
    o.append(S.line(px+pw+wall,py,px+pw+wall,gy0,stroke=S.CONC,stroke_width=2.5))
    o.append(S.line(px+pw+wall,gy1,px+pw+wall,py+ph,stroke=S.CONC,stroke_width=2.5))
    # bottom side: a line of boundary stones, the legal limits on the modality
    o.append(S.line(px,py+ph,px+pw,py+ph,stroke=S.INK,stroke_width=2,stroke_dasharray="9 5"))
    n=4 if narrow else 6
    for k in range(n+1):
        x=px+pw*k/n
        o.append(S.rect(x-4,py+ph-4,8,8,fill=S.PAPER,stroke=S.CONC,stroke_width=1.8))
    # the free field
    o.append(S.circle(cx+strip/2,cy+(8 if narrow else 14),4,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
    o.append(S.text(cx+strip/2,cy+(34 if narrow else 40),'autonomia' if narrow else 'campo da autonomia',size=ls,family=S.SERIF,fill=S.INK2,anchor='middle'))
    if narrow:
        o.append(S.text(cx+strip/2,cy+50,'privada',size=ls,family=S.SERIF,fill=S.INK2,anchor='middle'))
    # labels, one per side, name over limit
    def lab(x,y,name,limit,anchor):
        if narrow and len(name)>14:
            a,b=name.rsplit(' ',1) if name.count(' ')==1 else (' '.join(name.split()[:-1]),name.split()[-1])
            o.append(S.text(x,y-8,a,size=fs,family=S.SERIF,anchor=anchor)); o.append(S.text(x,y+10,b,size=fs,family=S.SERIF,anchor=anchor)); y+=10
        else:
            o.append(S.text(x,y,name,size=fs,family=S.SERIF,anchor=anchor))
        o.append(S.text(x,y+20,limit,size=ls,family=S.SANS,fill=S.INK2,anchor=anchor))
    lab(cx,py-40 if narrow else py-40,'Contratar ou recusar','estoque · CDC 39','middle')
    lab(px-14,cy,'Estipular o conteúdo','norma cogente','end')
    lab(px+pw+wall+14,cy,'Escolher a contraparte','monopólio','start')
    lab(cx,py+ph+(34 if narrow else 34),'Definir a modalidade','limites legais','middle')
    return S.svg(w,h,'Planta de um terreno: o campo da autonomia, com cada lado fechado de um modo próprio, sem escala numérica',o)

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
