"""Aula 04: consent as a signature field; nomination as a curtained threshold.
Symbolic paper objects, not reconstructions of the running case.
Pereira III pp.102–106; CC439–440,467–471. No written-form requirement
is inferred from the signature sketch. States show absence, refusal, consent.
"""
from . import svg as S


def build(p):
    mode = p.get('mode', 'consent')
    state = int(p.get('state', 0))
    out = []
    def line(x, y, a, b, col=S.INK, width=2, dash=None):
        out.append(S.line(x,y,a,b,stroke=col,stroke_width=width,stroke_dasharray=dash))
    def text(x,y,s,col=S.INK,anchor=None):
        out.append(S.text(x,y,s,size=18,family=S.SERIF,fill=col,anchor=anchor))
    def path(d,col=S.INK,width=2):
        out.append(S.path(d,fill='none',stroke=col,stroke_width=width))
    if mode == 'consent':
        # A sheet with one operative commitment, two separate signature fields.
        # Handwriting is a mark, not a fabricated name or quotation.
        out.append(S.rect(36,24,408,280,fill=S.PAPER,stroke=S.INK,stroke_width=1.5))
        for y, end in ((72,405),(88,378),(104,405)):
            line(66,y,end,y,S.GRID,1)
        text(66,145,'obter o compromisso')
        line(66,190,226,190)
        path('M78,180 q15,-27 20,-9 t19,-7 q-6,24 16,10 l34,-8')
        text(66,219,'promitente')
        line(262,252,410,252)
        text(262,282,'terceiro')
        if state == 1:
            # Refusal: the third signature field remains empty and is struck out.
            line(270,234,402,234,S.CONC,2)
            line(320,220,347,246,S.CONC,2)
        if state == 2:
            path('M272,242 q10,-34 19,-12 t18,-6 q-9,23 11,10 l47,-9',S.DIF,2.5)
            line(66,190,226,190,S.MUTED,1)
        label = ['compromisso ainda pendente','recusa: perdas e danos','anuência: terceiro obrigado'][state]
        text(240,337,label,S.CONC if state==1 else S.DIF if state==2 else S.INK,'middle')
        return S.svg(480,360,'A anuência muda quem deve ao credor',out), []
    if mode == 'nomination':
        # The same doorway admits one holder of the entire position.
        # The first holder is outside; a single new mark occupies the room.
        line(60,55,420,55,width=4)
        line(60,55,60,263,width=4)
        line(60,263,420,263,width=4)
        line(420,55,420,111,width=4)
        line(420,209,420,263,width=4)
        line(416,111,424,111)
        line(416,209,424,209)
        # Curtain drawn aside; the gap, not a second room, carries substitution.
        for i in range(5):
            path(f'M{420+i*4},112 q-10,16 0,30 t0,30',S.MUTED,1)
        out.append(S.circle(228,157,16,fill=S.PAPER,stroke=S.DIF,stroke_width=3))
        text(228,104,'posição inteira',anchor='middle')
        text(228,220,'direitos e obrigações',anchor='middle')
        text(228,190,'nomeada',S.DIF,'middle')
        out.append(S.circle(455,157,10,fill=S.PAPER,stroke=S.MUTED,stroke_width=1.5))
        line(443,145,467,169,S.MUTED,1.5)
        text(455,299,'originária',anchor='end')
        line(455,278,455,178,S.MUTED,1,'3 5')
        text(60,334,'efeitos desde a celebração',S.DIF)
        return S.svg(490,360,'Nomeação eficaz: uma pessoa assume a posição inteira',out), []
    raise ValueError(mode)
