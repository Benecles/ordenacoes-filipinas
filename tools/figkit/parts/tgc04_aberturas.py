"""Aula 04: architectural thresholds and the physical earnest-money counterfoil.
Params: mode = planta (default) | memoria | janela | talao.
Languages: LANGUAGES 7 floor plan; 16 architectural object; 8 document sheet.
Sources: CC417–420,436–440,462–471; Pereira III pp.73–106.
Geometry is schematic, never a reconstruction of Ilha Plaza. No invented dates,
amounts or physical facts. Windows/doors encode consent, not commercial premises.
The planta's focusable threads are alternatives, not a mandatory sequence.
"""
from . import svg as S

def build(p):
    mode=p.get('mode','planta'); o=[]
    def line(x,y,a,b,col=S.INK,w=1.5,dash=None):
        return S.line(x,y,a,b,stroke=col,stroke_width=w,stroke_dasharray=dash)
    def text(x,y,v,size=14,**kw):
        return S.text(x,y,v,size=size,family=S.SANS,**kw)
    def path(d,col=S.INK,w=1.5,dash=None):
        return S.path(d,fill='none',stroke=col,stroke_width=w,stroke_dasharray=dash)
    def dot(x,y,col=S.INK,r=6):
        return S.circle(x,y,r,fill=S.PAPER,stroke=col,stroke_width=2)
    def thread(key,label,items):
        return f'<g class="thread" data-thread="{key}" role="button" tabindex="0" aria-label="Traçar {S.esc(label)}" aria-pressed="false">'+''.join(items)+'</g>'
    if mode in ('planta','memoria'):
        W,H=1080,414
        # Outer walls and two open thresholds. Widened openings carry real topology.
        walls=[(48,100,48,178),(48,248,48,366),(48,366,1030,366),
               (48,100,450,100),(586,100,1030,100),(1030,100,1030,366),
               (310,100,310,178),(310,248,310,366),
               (730,100,730,150),(730,220,730,258),(730,328,730,366),
               (730,238,1030,238)]
        o.extend(line(*q,w=4) for q in walls)
        o += [line(48,248,116,248),path('M48,178 A70,70 0 0 1 118,248',w=1),
              line(310,248,378,248),path('M310,178 A70,70 0 0 1 380,248',w=1)]
        # Window: the performance may cross the wall, the beneficiary remains outside.
        o += [line(450,96,586,96,w=1),line(450,104,586,104,w=1),
              line(450,91,450,109),line(586,91,586,109),
              text(518,32,'beneficiário',anchor='middle'),dot(518,53),
              text(534,77,'direito próprio',size=13)]
        # The room behind a curtain: replacement is reserved, consent still needed.
        for i in range(8):
            x=730+(5 if i%2 else -5)
            o.append(line(x,152+i*8,x,160+i*8,w=1))
        # Door operated on the far side: autonomy of the third party.
        o += [line(730,328,795,328),path('M730,258 A70,70 0 0 1 800,328',w=1),
              S.circle(785,321,3,fill=S.INK,stroke=S.INK)]
        if mode=='planta':
            labels=[text(77,137,'Contrato preliminar',weight='600'),
                    text(77,159,'dever de celebrar o definitivo',size=13),
                    text(332,148,'Contrato formado',weight='600'),
                    text(332,171,'acordo entre as partes',size=13),
                    text(775,130,'Pessoa a declarar',weight='600'),
                    text(775,153,'reserva de substituição',size=13),
                    text(775,277,'Fato de terceiro',weight='600'),
                    text(812,314,'anuência',size=13),
                    text(437,345,'Arras: entrega do sinal',size=13)]
        else:
            labels=[text(77,137,'Contrato futuro',weight='600'),
                    text(77,159,'promessa já vinculante',size=13),
                    text(332,148,'Regime presente',weight='600'),
                    text(332,171,'direitos e obrigações',size=13),
                    text(775,130,'Benefício alheio',weight='600'),
                    text(775,153,'formação entre dois',size=13),
                    text(775,277,'Sinal entregue',weight='600'),
                    text(812,314,'duas funções',size=13),
                    text(437,345,'Do objeto à indenização',size=13)]
        o += labels
        # One agreement is the common junction; each path reaches the threshold it governs.
        cx,cy=518,220
        o += [dot(cx,cy,r=8),text(cx,cy+28,'acordo',size=13,anchor='middle')]
        o.append(thread('favor','estipulação em favor de terceiro',[
            path('M518,212 V53',S.DIF,2.4),dot(518,53,S.DIF),
            text(534,176,'prestação ao beneficiário',size=13)]))
        o.append(thread('preliminar','contrato preliminar',[
            path('M510,220 H180',w=2),dot(180,220),
            path('M180,220 H310',dash='3 5'),text(77,306,'contratar depois',size=13)]))
        o.append(thread('pessoa','pessoa a declarar',[
            path('M526,220 H670 V185 H852',w=2),dot(852,185),
            text(775,210,'assume desde a celebração',size=13)]))
        o.append(thread('fato','promessa de fato de terceiro',[
            path('M526,220 H650 V293 H721',w=2),
            path('M739,293 H790',dash='3 5'),dot(800,293),
            text(775,351,'recusa: responde quem prometeu',size=13,fill=S.CONC)]))
        # A pair of detached paper edges at a desk, no monetary quantity asserted.
        o.append(thread('arras','arras',[
            path('M518,228 V284',w=2),
            path('M465,282 H510 L506,290 L512,298 L506,306 L510,314 H465 Z'),
            path('M531,282 H576 V314 H531 L527,306 L533,298 L527,290 Z'),
            line(475,293,495,293),line(545,293,565,293)]))
        o += [text(48,401,'FORMAÇÃO · um vínculo já formado pode conservar uma abertura',size=13,fill=S.MUTED)]
        return S.svg(W,H,'Planta contratual: os limiares da formação e do cumprimento',o),[]
    if mode=='janela':
        W,H=500,348
        # Two hands of formation are dots on the inner sill. Third dot is outside.
        o += [line(50,50,50,297,w=4),line(50,50,450,50,w=4),
              line(50,297,450,297,w=4),line(450,50,450,116,w=4),
              line(450,224,450,297,w=4),
              line(445,116,445,224),line(455,116,455,224),
              line(437,116,463,116),line(437,224,463,224)]
        o += [line(100,160,300,160),dot(100,160),dot(300,160),
              text(100,135,'estipulante',size=14),text(275,135,'promitente',size=14),
              text(200,187,'acordo',size=14,anchor='middle'),
              path('M300,160 C350,160 365,252 420,252',S.DIF,2),
              path('M420,252 V170 H480',S.DIF,2),dot(480,170,S.DIF),
              text(290,276,'prestação',fill=S.DIF,size=14),
              text(480,330,'beneficiário',anchor='end',size=14),
              line(480,305,480,180,S.MUTED,1,'2 4')]
        return S.svg(W,H,'A prestação atravessa a janela; a formação permanece entre dois',o),[]
    if mode=='talao':
        W,H=800,330
        # Counterfoil bound at the left; matching zigzag edges attest actual detachment.
        o += [line(55,45,55,277,w=5),path('M65,45 H328 V277 H65 Z'),
              path('M338,45 H438 L430,58 L438,71 L430,84 L438,97 L430,110 L438,123 L430,136 L438,149 L430,162 L438,175 L430,188 L438,201 L430,214 L438,227 L430,240 L438,253 L430,266 L438,277 H338 Z'),
              path('M472,45 H735 V277 H472 L464,266 L472,253 L464,240 L472,227 L464,214 L472,201 L464,188 L472,175 L464,162 L472,149 L464,136 L472,123 L464,110 L472,97 L464,84 L472,71 L464,58 Z')]
        for y in (118,169,220):
            o += [line(90,y,306,y,S.GRID),line(496,y,710,y,S.GRID)]
        o += [text(90,84,'Canhoto',size=18,weight='600'),text(496,84,'Sinal entregue',size=18,weight='600'),
              text(90,110,'quem deu',size=16),text(496,110,'quem recebeu',size=16),
              text(90,157,'contrato confirmado',size=16),text(496,157,'imputação ou restituição',size=16),
              text(90,208,'sem arrependimento',size=16),text(496,208,'mínimo indenizatório',size=16,fill=S.DIF),
              text(90,254,'com arrependimento',size=16),text(496,254,'limite indenizatório',size=16,fill=S.CONC),
              text(55,314,'A entrega ocorre agora; a função da quantia depende do que foi pactuado.',size=16)]
        return S.svg(W,H,'Talão destacado: sinal transferido e função confirmatória ou penitencial',o),[]
    raise ValueError(mode)
