"""Aula09 bespoke planta, strip chart. No params or quantitative series.
Three focusable threads compare prestação and market conditions qualitatively.
The band is álea normal, without numeric threshold. V68–70; CM145/148/150.
Blueprint §6 replaces the shared railway geometry; trace by focus or touch.
"""
from . import svg as S

def build(p):
    t=S.text
    out=[t(26,28,'PRESTAÇÃO E CONDIÇÕES DE MERCADO',size=12),t(26,53,'Comparação qualitativa ao longo do contrato',size=14,family=S.SERIF,fill=S.INK2)]
    for y in [208,280]:out.append(S.line(130,y,974,y,stroke=S.MUTED,stroke_width=1))
    for x in range(144,970,36):
        out += [S.line(x,208,x+6,202,stroke=S.GRID),S.line(x,280,x+6,286,stroke=S.GRID)]
    out += [S.line(130,244,974,244,stroke=S.INK2,stroke_dasharray='3 6'),t(26,249,'mercado',size=12,fill=S.INK2),t(956,311,'Álea normal: oscilações que o contrato distribui',size=12,anchor='end',fill=S.INK2),S.line(130,84,130,286,stroke=S.MUTED,stroke_dasharray='2 5'),S.line(130,330,974,330,stroke=S.INK),S.path('M966,325 L974,330 L966,335',fill='none',stroke=S.INK),t(130,351,'celebração',size=12,anchor='middle'),t(710,351,'execução',size=12,anchor='middle')]
    threads=[('ordinario','Oscilação ordinária','M130,244 C250,218 310,267 410,244 S590,222 710,248 S865,220 974,244',244,'risco contratado',S.INK),('posterior','Desequilíbrio superveniente','M130,244 L500,244 C570,244 600,180 680,162 L974,162',162,'mudança posterior',S.INK),('originario','Desequilíbrio originário','M130,106 L974,106',106,'defeito na celebração',S.CONC)]
    for key,name,path,y,label,ink in threads:
        out.append(f'<g data-thread="{key}" data-fio="{key}" tabindex="0" role="link" aria-label="{S.esc(name)}">')
        out += [S.path(path,fill='none',stroke=S.INK,stroke_width=18,opacity='0',pointer_events='stroke'),S.path(path,fill='none',stroke=ink,stroke_width=2),S.circle(130,244 if key=='posterior' else y,5,fill=S.PAPER,stroke=ink,stroke_width=1.7),S.rect(969,y-5,10,10,fill=S.PAPER,stroke=ink,stroke_width=1.5),t(956,y-15,label,size=12,anchor='end',fill=ink)]
        if key=='posterior':out += [S.circle(500,244,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.5),S.line(500,255,500,294,stroke=S.MUTED,stroke_dasharray='2 4'),t(500,311,'fato posterior',size=12,anchor='middle')]
        out.append('</g>')
    out += [t(26,383,'CC 157 · origem',size=12),t(365,383,'CC 317 / 478–480 · superveniência',size=12),t(974,383,'CDC 6º, V · sem imprevisibilidade',size=12,anchor='end')]
    return S.svg(1000,400,'Planta da revisão: origem, alteração posterior e álea normal, sem escala numérica',out),[]
