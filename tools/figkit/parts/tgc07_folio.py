"""Aula 07: folio planta, dot tally and six-decision hemicycle.

params: mode = folio | atos | hemiciclo. All facts are fixed to this lesson's
assigned decisions; no invented votes, quantities or chronology. The folio's
clause is a spliced HTML source block over the empty document centre.
Desktop and phone versions use the same facts at legible native coordinates.
Folio extends the lesson planta's thread contract, replacing the railway form.
"""
from __future__ import annotations
from math import cos, sin, radians
from . import svg as S


def paired(large, small):
    return '<div class="tgc07-large">' + large + '</div><div class="tgc07-small">' + small + '</div>'


def folio(phone=False):
    if phone:
        w, h = 340, 510
        x, y, pw, ph = 10, 8, 320, 312
        o = [
            S.rect(x, y, pw, ph, fill=S.PAPER2, stroke=S.INK, stroke_width=1.2),
            S.rect(x, y, pw, 28, fill=S.INK, stroke=S.INK, stroke_width=1.2),
            S.text(x + 14, y + 18, 'CLÁUSULA TERCEIRA · TJSP', size=11.5, fill=S.PAPER, weight=600),
        ]
        specs = [('intencao', 'art. 112', 'intenção declarada'), ('conjunto', 'art. 113', 'conjunto e execução'), ('limite', 'art. 114', 'limite às liberalidades')]
        for i, (key, law, note) in enumerate(specs):
            gy = 365 + i * 53; gx = 28
            d = f'M{gx}, {gy-20} V{gy-31} H{310-i*14} V{324-i*12}'
            tone = S.CONC if i == 2 else S.DIF if i == 1 else S.INK
            o.append(f'<g data-thread="{key}" tabindex="0" role="link" aria-label="{S.esc(law+": "+note)}" data-fio="{key}">')
            o += [
                S.path(d, fill='none', stroke=tone, stroke_width=1.4),
                S.circle(gx, gy, 4, fill=S.PAPER, stroke=tone, stroke_width=1.4),
                S.text(gx + 12, gy + 4, law, size=12.5, fill=tone, weight=600),
                S.text(gx + 12, gy + 24, note, size=12.5, family=S.SERIF, fill=S.INK),
                S.rect(x - 3 if i < 2 else x + pw - 3, y + 72 + i * 80, 6, 6, fill=S.PAPER, stroke=tone, stroke_width=1.4),
            ]
            o.append('</g>')
        return S.svg(w, h, 'Planta da leitura: uma cláusula glosada pelos arts. 112 a 114', o)

    # Desktop architectural annotated folio instrument (preserving .folio-quote slot at left:27% top:17% width:46%)
    w, h = 1040, 386
    x, y, pw, ph = 264, 18, 510, 314
    o = [
        # Drop shadow & drafting folio sheet
        S.rect(x + 6, y + 6, pw, ph, fill='var(--grid-major)', stroke='none'),
        S.rect(x, y, pw, ph, fill=S.PAPER, stroke=S.INK, stroke_width=1.6),
        S.rect(x, y, pw, 28, fill=S.INK, stroke=S.INK, stroke_width=1.4),
        S.text(x + 16, y + 18, 'CLÁUSULA TERCEIRA · TJSP · AC 1000680', size=11.5, fill=S.PAPER, weight=600),
        S.text(x + pw - 16, y + 18, 'ARTS. 112–114 CC', size=11.5, anchor='end', fill=S.PAPER),
        S.line(x, y + 28, x, y + ph, stroke=S.DIF, stroke_width=3),
        # Lower structured interpretive strip inside the folio (well below the spliced HTML quote)
        S.line(x + 18, y + 228, x + pw - 18, y + 228, stroke=S.GRID, stroke_width=1, stroke_dasharray='3 3'),
        S.rect(x + 18, y + 238, 150, 62, fill='var(--dif-wash)', opacity='0.52', stroke=S.GRID, stroke_width=0.8),
        S.line(x + 18, y + 238, x + 18, y + 300, stroke=S.DIF, stroke_width=2.5),
        S.text(x + 28, y + 258, 'LETRA DA CLÁUSULA', size=11.5, fill=S.DIF, weight=600),
        S.text(x + 28, y + 278, 'condição de renovação', size=12, family=S.SERIF, fill=S.INK),

        S.rect(x + 180, y + 238, 150, 62, fill='var(--dif-wash)', opacity='0.52', stroke=S.GRID, stroke_width=0.8),
        S.line(x + 180, y + 238, x + 180, y + 300, stroke=S.DIF, stroke_width=2.5),
        S.text(x + 190, y + 258, 'EXECUÇÃO REAL', size=11.5, fill=S.DIF, weight=600),
        S.text(x + 190, y + 278, 'gestão e receitas', size=12, family=S.SERIF, fill=S.INK),

        S.rect(x + 342, y + 238, 150, 62, fill='var(--conc-wash)', opacity='0.54', stroke=S.GRID, stroke_width=0.8),
        S.line(x + 342, y + 238, x + 342, y + 300, stroke=S.CONC, stroke_width=2.5),
        S.text(x + 352, y + 258, 'SOLUÇÃO · TJSP', size=11.5, fill=S.CONC, weight=600),
        S.text(x + 352, y + 278, 'preço devido · art. 113', size=12, family=S.SERIF, fill=S.INK),
    ]

    # Marginal drafting-table gloss cards with orthogonal circuit wires
    specs = [
        ('intencao', 'art. 112 CC', 'intenção declarada', 'sentido comum das partes', 18, 66, 206, 80, S.DIF, 'var(--dif-wash)', True, y + 92),
        ('conjunto', 'art. 113 CC', 'conjunto e execução', 'boa-fé e usos do tráfego', 18, 186, 206, 80, S.DIF, 'var(--dif-wash)', True, y + 206),
        ('limite',   'art. 114 CC', 'limite às liberalidades', 'interpretação estrita', 816, 126, 206, 80, S.CONC, 'var(--conc-wash)', False, y + 166),
    ]
    for key, law, note, sub, cx, cy, cw, ch, tone, wash, left, anchor_y in specs:
        edge = x if left else x + pw
        sx = cx + cw if left else cx
        mid = edge - 20 if left else edge + 20
        d = f'M{sx},{cy + ch/2:.1f} H{mid} V{anchor_y} H{edge}'
        o.append(f'<g data-thread="{key}" tabindex="0" role="link" aria-label="{S.esc(law+": "+note)}" data-fio="{key}">')
        o += [
            S.path(d, fill='none', stroke=tone, stroke_width=1.6),
            S.rect(cx, cy, cw, ch, fill=wash, opacity='0.48', stroke=tone, stroke_width=1.4),
            S.line(cx if left else cx + cw, cy, cx if left else cx + cw, cy + ch, stroke=tone, stroke_width=3.2),
            S.text(cx + 14, cy + 24, law, size=12.5, fill=tone, weight=650),
            S.text(cx + 14, cy + 45, note, size=13, family=S.SERIF, fill=S.INK, weight=600),
            S.text(cx + 14, cy + 65, sub, size=11.5, fill=S.INK2),
            S.circle(sx, cy + ch / 2, 4, fill=S.PAPER, stroke=tone, stroke_width=1.5),
            S.rect(edge - 3.5, anchor_y - 3.5, 7, 7, fill=S.PAPER, stroke=tone, stroke_width=1.5),
        ]
        o.append('</g>')

    # Docked hermeneutic spine along the bottom
    ys = 348
    o += [
        S.rect(18, ys, 1004, 28, fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
        S.rect(18, ys, 206, 28, fill=S.INK, stroke=S.INK, stroke_width=1.4),
        S.text(121, ys + 18, 'CÓDIGO CIVIL · HERMENÊUTICA', size=11.5, anchor='middle', fill=S.PAPER, weight=600),
        S.line(486, ys, 486, ys + 28, stroke=S.INK, stroke_width=1.1),
        S.line(760, ys, 760, ys + 28, stroke=S.INK, stroke_width=1.1),
        S.text(355, ys + 18, 'art. 112 · intenção consubstanciada', size=11.5, anchor='middle', fill=S.DIF, weight=600),
        S.text(623, ys + 18, 'art. 113 · comportamento posterior', size=11.5, anchor='middle', fill=S.INK),
        S.text(891, ys + 18, 'art. 114 · interpretação estrita', size=11.5, anchor='middle', fill=S.CONC, weight=600),
    ]
    return S.svg(w, h, 'Planta da leitura: uma cláusula glosada pelos arts. 112 a 114', o)


def atos(phone=False):
    w,h=(340,290) if phone else (650,240)
    o=[S.text(12,25,'ATOS DE EXECUÇÃO',size=13),S.text(w-12,25,'4 registros',size=12,anchor='end')]
    names=['Administração assumida','Passivo assumido','Primeira parcela paga','Receitas recebidas']
    for i,name in enumerate(names):
        y=68+i*(56 if phone else 44)
        # Every dot denotes one kind of act, not frequency or strength of proof.
        o += [S.circle(25,y-5,5,fill=S.INK),S.text(45,y,name,size=15,family=S.SERIF),
              S.line(12,y+17,w-12,y+17,stroke=S.GRID,stroke_width=1)]
    return S.svg(w,h,'Quatro atos registrados no contrato de cessão de quotas',o)


def hemiciclo(phone=False):
    w,h=(340,420) if phone else (980,410)
    cx,cy=(170,200) if phone else (490,280)
    rx,ry=(135,160) if phone else (320,200)
    o=[]
    for factor in [1,.79]:
        o.append(S.path(f'M{cx-rx*factor},{cy} A{rx*factor},{ry*factor} 0 0 1 {cx+rx*factor},{cy}',fill='none',stroke=S.GRID,stroke_width=1))
    data=[('AR 7.296','letra mantida','intencao'),('REsp 1.013.976','nome insuficiente','intencao'),('REsp 1.938.997','liberalidade limitada','criterios'),('REsp 15.339','todo qualificado','qualificacao'),('AC 1000680','execução confirma','criterios'),('AREsp 1.679.541','prova preservada','criterios')]
    for i,(case,meaning,target) in enumerate(data):
        angle=180-i*36
        x=cx+rx*cos(radians(angle)); y=cy-ry*sin(radians(angle))
        o.append(f'<a tabindex="0" data-thread="caso-{i}" href="#{target}" aria-label="{S.esc(case+": "+meaning)}">')
        o += [S.circle(x,y,5,fill=S.PAPER,stroke=S.INK,stroke_width=1.5)]
        if not phone:
            if i in (1,4):
                # outside the whole arc's box, led by a rule from its dot, so no label straddles the figure's edge
                side=-1 if i==1 else 1
                tx=cx+side*(rx+14); ty=y-2
                o += [S.line(x+side*9,y,tx-side*4,y,stroke=S.MUTED,stroke_width=.8),S.text(tx,ty-24,case,size=13,anchor='end' if i==1 else 'start'),S.text(tx,ty-2,meaning,size=15,anchor='end' if i==1 else 'start',family=S.SERIF)]
            else:
                ty=335 if i in (0,5) else 36
                o += [S.line(x,y-9 if i in (2,3) else y+9,x,ty+32 if i in (2,3) else ty-21,stroke=S.MUTED,stroke_width=.8),S.text(x,ty,case,size=13,anchor='middle'),S.text(x,ty+22,meaning,size=15,anchor='middle',family=S.SERIF)]
        else:
            # Six numbered positions point to a readable key under the hemicycle.
            o.append(S.text(x,y-12,str(i+1),size=12,anchor='middle'))
        o.append('</a>')
    o += [S.text(cx,cy-45,'DECLARAÇÃO',size=13,anchor='middle'),S.text(cx,cy-23,'lida nas circunstâncias',size=14,anchor='middle',family=S.SERIF)]
    if phone:
        for i,(case,meaning,target) in enumerate(data):
            o.append(f'<a href="#{target}">')
            o.append(S.text(8,250+i*27,f'{i+1}  {case} · {meaning}',size=12,family=S.SERIF));o.append('</a>')
    return S.svg(w,h,'Seis julgados em torno da declaração: fundamentos distintos de leitura, sem contagem de votos',o)


def build(p: dict) -> tuple[str,list[dict]]:
    fn={'folio':folio,'atos':atos,'hemiciclo':hemiciclo}[p['mode']]
    return paired(fn(),fn(True)),[]
