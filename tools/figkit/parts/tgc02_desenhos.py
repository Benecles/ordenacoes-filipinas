"""Aula 02's two chapter plates.

mode 'regua': survey plan of one plot, four sides each closed its own way (gate, wall, stones,
band), no numerical scale. Pereira pp.21–27, Venosa p.9, CDC39 II/IX.
mode 'normas': stacked norms plate (CC421,421-A caput/I-II,2035 sole paragraph).
Both modes return desktop and phone variants. No remote assets or scripts.
"""
from __future__ import annotations
from . import svg as S
from .tgc01_hand import cord, rule, mark, name, gloss, art, bracket

def regua(narrow):
    """Survey plan of one plot: the party's field, each of its four sides closed in its own way."""
    if narrow:
        w,h=340,372; px,py,pw,ph=96,72,140,214; wall=16; strip=36; fs=11; ls=12
    else:
        w,h=800,344; px,py,pw,ph=270,64,260,218; wall=22; strip=56; fs=12.5; ls=13
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
    o.append(gloss(cx+strip/2,cy+(34 if narrow else 40),'autonomia' if narrow else 'campo da autonomia',anchor='middle',size=ls))
    if narrow:
        o.append(gloss(cx+strip/2,cy+50,'privada',anchor='middle',size=ls))
    # labels, one per side, name over limit
    def lab(x,y,nm,limit,anchor):
        if narrow and len(nm)>14:
            a,b=(' '.join(nm.split()[:-1]),nm.split()[-1])
            o.append(name(x,y-8,a,anchor=anchor,size=fs)); o.append(name(x,y+8,b,anchor=anchor,size=fs)); y+=8
        else:
            o.append(name(x,y,nm,anchor=anchor,size=fs))
        o.append(gloss(x,y+18,limit,anchor=anchor,size=ls))
    lab(cx,py-40 if narrow else py-40,'Contratar ou recusar','estoque · CDC 39','middle')
    lab(px-14,cy,'Estipular o conteúdo','norma cogente','end')
    lab(px+pw+wall+14,cy,'Escolher a contraparte','monopólio','start')
    lab(cx,py+ph+(34 if narrow else 34),'Definir a modalidade','limites legais','middle')
    return S.svg(w,h,'Planta de um terreno: o campo da autonomia, com cada lado fechado de um modo próprio, sem escala numérica',o)

def normas(narrow):
    """Three norms as three hairline strata over one common field (no sheets, no boxes)."""
    w,h=(340,420) if narrow else (800,300)
    x0,x1=(24,316) if narrow else (70,730)
    o=[rule(f'M{x0},34 V{h-58}',S.GRID,1.0),rule(f'M{x1},34 V{h-58}',S.GRID,1.0)]
    ys=(64,196,300) if narrow else (62,150,226)
    # 421: the operative norm, with three marked limits along it
    y=ys[0]
    o+=[name(x0,y-16,'CC 421 · liberdade contratual',col=S.DIF,size=12 if narrow else 12.5),rule(f'M{x0},{y} H{x1}',S.DIF,2)]
    pts=[(x0+110,'nos limites da função social'),(x0+(x1-x0)//2+20,'intervenção mínima'),(x1-80,'revisão excepcional')]
    for k,(x,t) in enumerate(pts):
        o.append(mark(x,y,S.DIF,5))
        if narrow: o.append(gloss(x0,y+24+k*18,t,size=12.5))
        else: o.append(gloss(x,y+26,t,anchor='middle',size=13))
    y=ys[1]
    o+=[name(x0,y-16,'421-A · paridade presumida',size=12 if narrow else 12.5),rule(f'M{x0},{y} H{x1}',S.INK,1.0),mark(x1,y,S.INK,5),
        gloss(x0,y+24,'ressalva dos regimes especiais',size=13)]
    y=ys[2]
    o+=[name(x0,y-16,'2.035 p.u. · ordem pública',col=S.CONC,size=12 if narrow else 12.5),rule(f'M{x0},{y} H{x1}',S.CONC,2),mark(x1,y,S.CONC,5),
        gloss(x0,y+24,'a convenção não pode afastá-la',size=13)]
    o+=[bracket(x0,x1,h-30,up=False),gloss((x0+x1)/2,h-6,'normas que incidem em conjunto',anchor='middle',size=13)]
    return S.svg(w,h,'Estratos de normas sobre um mesmo campo: liberdade, presunção relativa e ordem pública coexistem',o)

def build(p:dict)->tuple[str,list[dict]]:
    mode=p.get('mode','regua'); fn={'regua':regua,'normas':normas}[mode]
    return ('<div class="drawing-desktop">'+fn(False)+'</div><div class="drawing-mobile">'+fn(True)+'</div>',[])
