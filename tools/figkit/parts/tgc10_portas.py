"""Two-key door instrument for CC474. No factual parameters.

Each door already has a fixed legal prerequisite (specific clause / definitive
breach). The reader turns the other key: creditor's declaration / constitutive
judgment. Buttons operate distinct locks; they never switch drawing versions.
Sources: Terra/Nanni pp.145–146,157–160; roteiro pp.20–22; CC474.
"""
from . import svg as S


def build(p):
    doors=[]
    for key,name,fixed,act,answer in [
        ('expressa','Expressa','Cláusula específica','Declarar a resolução','A declaração do credor produz a extinção sem sentença constitutiva.'),
        ('tacita','Tácita','Inadimplemento definitivo','Constituir em juízo','A sentença constitui o efeito extintivo fundado na cláusula tácita.'),
    ]:
        out=[S.text(20,25,name,size=18,family=S.SANS,weight='600'),
             S.rect(60,65,190,225,fill='none',stroke=S.INK,stroke_width=3),
             S.path('M70,76 L240,280 M240,76 L70,280',fill='none',stroke=S.GRID,stroke_width=1)]
        leaf=S.rect(67,72,176,211,fill=S.PAPER2,stroke=S.INK,stroke_width=1.5)
        leaf+=S.circle(219,178,5,fill=S.PAPER,stroke=S.INK,stroke_width=2)
        out.append('<g class="door-leaf">'+leaf+'</g>')
        # The fixed first key seats a bolt. The second is turned by the reader.
        out.append(S.line(22,116,104,116,stroke=S.INK,stroke_width=3))
        out.append(S.circle(22,116,9,fill=S.PAPER,stroke=S.INK,stroke_width=2))
        out.append(S.path('M84,116 v10 h8 v-10 M94,116 v7',fill='none',stroke=S.INK,stroke_width=3))
        out.append(S.text(20,52,fixed,size=14,family=S.SERIF))
        turning=S.circle(22,225,9,fill=S.PAPER,stroke=S.INK,stroke_width=2)
        turning+=S.path('M31,225 H100 v10 h-9 v-10 M80,225 v7',fill='none',stroke=S.INK,stroke_width=3)
        out.append('<g class="turning-key">'+turning+'</g>')
        doors.append(f'<div class="door-unit" data-door="{key}">'+S.svg(310,310,'Via '+name+' da resolução',out)+f'<button type="button" class="door-act" aria-pressed="false">{act}</button><p class="door-answer" aria-live="polite">{answer}</p></div>')
    return '<div class="tgc10-doors">'+''.join(doors)+'</div>',[]
