"""Aula09 chapter plates. mode=diptico|genealogia|base.
Diptico: categorical moments of imbalance, CC157§1/V70; no quantities.
Genealogia: families of explanations, Dias331–333/Luis Renato29–30;
branches are conceptual, not assertions of direct historical influence.
Base: explicit metaphor of a pier under a span, Luis Renato28–30/Dias332;
performance remains possible after the common purpose disappears.
All coordinates qualitative; no invented economic series or factual objects.
"""
from . import svg as S

def build(p):
    mode=p.get('mode','diptico');t=S.text;out=[]
    if mode=='diptico':
        for x,title,later in [(20,'Lesão · na celebração',False),(440,'Imprevisão · depois',True)]:
            out += [t(x,28,title,size=19,family=S.SERIF),S.line(x+32,62,x+32,244,stroke=S.MUTED,stroke_dasharray='2 4'),t(x+32,270,'assinatura',size=13,anchor='middle'),t(x+330,270,'cumprimento',size=13,anchor='end'),S.line(x+32,196,x+330,196,stroke=S.INK2,stroke_width=1.7)]
            path=f'M{x+32},132 L{x+330},132' if not later else f'M{x+32},196 L{x+145},196 C{x+195},196 {x+195},132 {x+245},132 L{x+330},132'
            out += [S.path(path,fill='none',stroke=S.INK,stroke_width=2.4),S.circle(x+32,196 if later else 132,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.5)]
            for xx in ([x+70,x+120,x+170,x+220,x+270] if not later else [x+265,x+290,x+315]):out.append(S.line(xx,144,xx,184,stroke=S.CONC))
            out += [t(x,310,'desproporção originária' if not later else 'alteração superveniente',size=15,family=S.SERIF),t(x,334,'CC 157 · valores ao contratar' if not later else 'CC 478 · evento e risco a apurar',size=13,fill=S.INK2)]
        out.append(S.line(410,15,410,345,stroke=S.GRID))
        return S.svg(820,355,'Díptico: distância entre prestações presente ao contratar ou produzida posteriormente',out),[]
    if mode=='genealogia':
        out += [S.path('M40,150 L180,150 C230,150 230,76 280,76 L430,76 C480,76 480,45 530,45 L770,45',fill='none',stroke=S.INK,stroke_width=1.6),S.path('M430,76 C480,76 480,158 530,158 L770,158',fill='none',stroke=S.INK,stroke_width=1.6),S.path('M180,150 C230,150 230,280 280,280 L770,280',fill='none',stroke=S.INK,stroke_width=1.6)]
        nodes=[(40,150,'rebus sic stantibus',25,198,'estado das coisas'),(280,76,'Windscheid',263,49,'pressuposição · 1850'),(560,45,'Oertmann',548,92,'base subjetiva · 1921'),(560,158,'Larenz',548,204,'base objetiva'),(280,280,'imprevisão',263,329,'evento e repercussão não previstos')]
        for x,y,name,tx,ty,sub in nodes:out += [S.circle(x,y,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.7),t(tx,ty-20,name,size=17,family=S.SERIF),t(tx,ty,sub,size=13,fill=S.INK2)]
        out += [t(790,284,'CC',size=14,anchor='end'),t(790,306,'317 / 478',size=13,anchor='end',fill=S.INK2)]
        return S.svg(820,350,'Genealogia conceitual: pressuposição, base e imprevisão',out),[]
    if mode=='base':
        for x,absent in [(25,False),(445,True)]:
            out += [t(x,28,'Circunstância comum' if not absent else 'Circunstância desaparecida',size=18,family=S.SERIF),S.line(x+15,111,x+345,111,stroke=S.INK,stroke_width=3),S.line(x+15,124,x+345,124,stroke=S.INK,stroke_width=1.4)]
            for xx in [x+22,x+320]:out.append(S.path(f'M{xx},124 L{xx},207 L{xx+12},207 L{xx+12},124',fill='none',stroke=S.INK,stroke_width=1.5))
            out.append(S.path(f'M{x+154},124 L{x+154},221 L{x+184},221 L{x+184},124',fill='none',stroke=S.MUTED if absent else S.INK,stroke_width=1.6,stroke_dasharray='3 5' if absent else None))
            if not absent:out += S.hatch(x+154,145,30,65,step=10,stroke=S.GRID)
            else:out.append(S.path(f'M{x+151},163 L{x+163},169 L{x+174},157 L{x+187},163',fill='none',stroke=S.CONC,stroke_width=2))
            out += [S.line(x+10,223,x+350,223,stroke=S.INK2),t(x+169,259,'fim compartilhado' if not absent else 'o cumprimento ainda é possível',size=14,anchor='middle',family=S.SERIF),t(x+169,284,'sustenta a operação' if not absent else 'a utilidade comum se perdeu',size=14,anchor='middle',family=S.SERIF,fill=S.INK2)]
        return S.svg(820,308,'Metáfora da base: o vão permanece e o apoio comum desaparece',out),[]
    raise ValueError('Unknown mode: '+mode)
