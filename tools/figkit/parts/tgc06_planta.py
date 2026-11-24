"""Aula 06 planta: a shared lock engaged by two reciprocal keys.

Paper language 15 (tactile mechanism), cast as a relational mapa, never a
chronology. Params: title (accessible label, optional), mobile (bool, default
False). Each key is a trace hook, not a choice of alternative pictures. Facts:
Pereira pp.61–62,143–144; CC476–477. Geometry is schematic, not measured.
"""
from . import svg as S


def build(p):
    mobile = p.get('mobile', False)
    o=[]
    def text(x,y,s,**kw):o.append(S.text(x,y,s,**kw))
    def path(d,**kw):o.append(S.path(d,fill='none',stroke=S.INK,stroke_width=1.6,**kw))
    def key(x,y,flip=False):
        # A cut key: bow, neck, shaft, two wards. Mirrored keys engage one lock.
        tr=f'translate({x} {y})'+(' scale(-1 1)' if flip else '')
        return f'<g transform="{tr}">'+S.circle(0,0,29,fill='none',stroke=S.INK,stroke_width=2)+S.circle(0,0,17,fill='none',stroke=S.INK,stroke_width=1)+S.path('M29,-7 H204 V7 H187 V25 H173 V7 H151 V18 H137 V7 H29',fill='none',stroke=S.INK,stroke_width=2)+'</g>'
    w,h=(360,420) if mobile else (1080,322)
    if mobile:
        # Same two keys, with shorter shafts, and a vertical coupling.
        for ident,y,label in [('preco',107,'Preço · comprador'),('loja',248,'Loja · empreendedora')]:
            o.append(f'<g data-thread="{ident}" data-fio="{ident}" tabindex="0" role="button" aria-label="Traçar {label}">')
            o.append('<g transform="translate(29 '+str(y)+') scale(.83 1)">'+key(0,0)+'</g>')
            o.append(S.circle(204,y,21,fill=S.PAPER,stroke=S.INK,stroke_width=1.7))
            o.append(S.rect(199,y-5,10,10,fill=S.PAPER,stroke=S.INK,stroke_width=1.4))
            text(12,y-47,label,size=16,family=S.SERIF)
            o.append('</g>')
        path('M225,107 H264 V248 H225')
        path('M254,167 H275 M264,157 V177')
        text(281,180,'476',size=13,family=S.SERIF)
        text(12,28,'Sinalagma · reciprocidade das prestações',size=14,family=S.SERIF)
        text(12,331,'A falta relevante impede exigir a outra.',size=14,family=S.SERIF)
        text(12,362,'477 · risco superveniente comprovado',size=13,family=S.SERIF)
        text(12,388,'Cumprimento ou garantia libera a prestação.',size=13,family=S.SERIF)
    else:
        text(24,30,'Execução · as prestações permanecem vinculadas',size=13,family=S.MONO)
        # Two mirrored keys turn one shared lock: neither prestação turns alone.
        for ident,x,flip,label,tail in [('preco',120,False,'Comprador · preço','deve pagar pela loja prometida'),('loja',960,True,'Empreendedora · loja','deve entregar nas condições prometidas')]:
            y=150
            o.append(f'<g data-thread="{ident}" data-fio="{ident}" tabindex="0" role="button" aria-label="Traçar {label}">')
            o.append(key(x,y,flip))
            sx=x+204 if not flip else x-204
            ex=490 if not flip else 590
            path(f'M{sx},{y} H{ex}')
            text(24 if not flip else 1056,y-52,label,size=16,family=S.SERIF,anchor='start' if not flip else 'end')
            text(24 if not flip else 1056,y+56,tail,size=13,family=S.SERIF,anchor='start' if not flip else 'end')
            o.append('</g>')
        o.append(S.circle(540,150,50,fill=S.PAPER,stroke=S.INK,stroke_width=2))
        o.append(S.rect(530,140,20,20,fill=S.PAPER,stroke=S.INK,stroke_width=1.6))
        o.append(S.path('M540,100 V70 M526,70 H554',fill='none',stroke=S.CONC,stroke_width=2.3))
        text(566,66,'476 · falta relevante',size=13,family=S.SERIF)
        text(566,86,'obsta a exigência',size=13,family=S.SERIF)
        path('M540,200 V262')
        o.append(S.rect(534,262,12,12,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
        text(540,300,'477 · o risco superveniente permite suspender até cumprimento ou garantia',size=13,anchor='middle',family=S.SERIF)
    return S.svg(w,h,p.get('title','Sinalagma: duas chaves ligadas pelo cumprimento recíproco'),o),[]
