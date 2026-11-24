"""Three states of paired strips: Venosa p.95; Caio Mário p.142.

The fold unwinds exchanged performances; a detached end preserves consumed use.
No numerical scale. Narrow enough for the reading-side panel and a phone.
"""
from . import svg as S


def build(p):
    state = p.get('state', 1)
    out = []
    def t(x, y, text, **kw):
        out.append(S.text(x, y, text, size=18, family=S.SERIF, **kw))
    if state in (1, 2):
        for y, label in [(88, 'Coisa recebida'), (182, 'Preço recebido')]:
            t(22, y-22, label)
            out.append(S.rect(22, y, 316, 30, fill=S.PAPER2, stroke=S.INK, stroke_width=1.5))
            if state == 2:
                out.append(S.path(f'M322,{y+15} C352,{y+15} 352,{y+61} 320,{y+61} H46 Q22,{y+61} 22,{y+38}', fill='none', stroke=S.DIF, stroke_width=2.5))
        t(22, 298, 'Troca recebida' if state == 1 else 'Restituir de ambos os lados', fill=S.INK if state == 1 else S.DIF)
    else:
        t(22, 66, 'Relação continuada')
        out.append(S.rect(22, 112, 183, 36, fill=S.PAPER2, stroke=S.INK, stroke_width=1.5))
        out += S.hatch(23, 113, 181, 34, step=12, stroke=S.GRID)
        out.append(S.rect(228, 132, 110, 36, fill='none', stroke=S.MUTED, stroke_dasharray='4 4'))
        out.append(S.line(216, 95, 216, 184, stroke=S.CONC, stroke_width=2))
        t(22, 218, 'Fruição passada preservada')
        t(22, 262, 'Futuro encerrado', fill=S.CONC)
    return S.svg(360, 330, 'Liquidação: estado ' + str(state), out), []
