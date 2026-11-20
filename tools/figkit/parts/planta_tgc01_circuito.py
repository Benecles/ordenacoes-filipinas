"""Planta cast for Aula 01: circuit schematic, not a time rail.

No params. Fixed facts: STJ local assigned reading p.4, REsp 1.176.019.
Four terminals include the taxi counterfactual, expressly not a fourth litigant.
Uses planta's drawing vocabulary/helpers: hollow terminals, square junctions,
notched flags, traceable conductors. Distances carry no financial quantities.
"""
from .planta import S


def build(p):
    o = []
    T = S.text
    def wire(key, label, body):
        o.append('<g data-thread="'+key+'" tabindex="0" role="button" aria-label="'+label+'">'+''.join(body)+'</g>')
    def line(d, col=S.INK, dash=None):
        return S.path(d, fill='none', stroke=col, stroke_width=1.8, stroke_dasharray=dash)
    def dot(x,y):
        return S.circle(x,y,6,fill=S.PAPER,stroke=S.INK,stroke_width=1.8)
    def arrow(x,y,direction=1,col=S.INK):
        return line(f'M{x-7*direction},{y-4} L{x},{y} L{x-7*direction},{y+4}',col)
    o += [T(45,25,'Seguro · REsp 1.176.019',size=12,fill=S.INK2),
          T(1030,25,'Quadro · operação, vínculo e proteção',size=12,anchor='end',fill=S.INK2)]
    wire('seguro','Rastrear a proteção adquirida pela transportadora',[
        line('M165,100 L165,59 L850,59 L850,100'),arrow(540,59),
        T(480,49,'contratação do seguro',size=13,anchor='middle'),
        line('M850,100 L850,143 L165,143 L165,100'),arrow(480,143,-1),
        T(500,167,'proteção da frota e danos a terceiros',size=13,anchor='middle'),
        dot(165,100),dot(850,100),T(185,106,'Transportadora',size=14,family=S.SANS,weight=600),
        T(830,106,'Seguradora',size=14,family=S.SANS,anchor='end',weight=600)])
    wire('indenizacao','Rastrear o pagamento ao proprietário prejudicado',[
        line('M165,106 L165,280 L380,280'),arrow(290,280),dot(380,280),
        T(183,230,'indenização paga',size=13),
        T(400,285,'Dono do caminhão particular',size=14,family=S.SANS),
        T(400,308,'prejudicado no caso julgado',size=12,fill=S.INK2)])
    wire('reembolso','Rastrear por que o reembolso foi negado',[
        line('M850,106 L1005,106 L1005,200 L600,200',S.CONC),
        line('M575,200 L120,200 L120,100 L159,100',S.CONC),
        line('M575,200 L598,186',S.CONC),dot(575,200),dot(600,200),
        T(730,225,'reembolso negado',size=13,fill=S.CONC,anchor='middle'),
        T(730,245,'categoria fora da cobertura',size=12,fill=S.CONC,anchor='middle')])
    wire('hipotese','Rastrear a hipótese de mudar somente a categoria para táxi',[
        line('M1005,200 L1005,340 L850,340 L850,290',S.INK2,'3 5'),dot(850,290),
        T(830,294,'Táxi',size=14,family=S.SANS,anchor='end'),
        T(830,316,'hipótese: categoria prevista',size=12,anchor='end',fill=S.INK2)])
    o += [S.path('M45,345 L310,345 L300,355 L310,365 L45,365 Z',fill='none',stroke=S.INK,stroke_width=1),
          T(57,359,'Consumidora; pedido improcedente',size=12,fill=S.DIF)]
    return S.svg(1080,385,'Circuito da proteção, da indenização e do reembolso no seguro da transportadora',o), []
