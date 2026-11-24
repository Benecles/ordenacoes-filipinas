"""Aula01, strata cutaway of one negócio, Venosa p.51; Pereira p.33.

No params. Three analytical planes, not three temporal steps. Dimensions
and hatch density have no quantitative meaning. One block is cut to reveal
the distinction between presence, validity and an effect pending a condition.
"""
from . import svg as S


def build(p):
    o=[]
    T=S.text
    def stroke(d,col=S.INK,dash=None):
        return S.path(d,fill='none',stroke=col,stroke_width=1.4,stroke_dasharray=dash)
    o += [stroke('M75,45 L485,45 L585,90 L175,90 Z'),
          stroke('M75,45 L75,215 L175,260 L585,260 L585,90'),
          stroke('M175,90 L175,260'),
          stroke('M75,100 L175,145 L585,145'),
          stroke('M75,155 L175,200 L585,200')]
    # Exposed material has a continuous top stratum, a fault in validity,
    # and an uncompleted/dashed seam for an effect awaiting a condition.
    for x in range(195,571,24):
        o.append(stroke(f'M{x},103 l-12,25',S.INK2))
    o += [stroke('M360,145 L348,161 L367,174 L351,190 L360,200',S.CONC),
          stroke('M175,229 L585,229',S.INK2,'4 6'),
          stroke('M585,117 L630,117'),T(645,111,'Existir',size=15,family=S.SANS,weight=600),
          T(645,134,'declarações convergentes',size=13,fill=S.INK2),
          stroke('M585,171 L630,171'),T(645,170,'Valer',size=15,family=S.SANS,weight=600),
          T(645,192,'requisitos do art. 104',size=13,fill=S.INK2),
          stroke('M585,235 L630,235'),T(645,234,'Produzir efeitos',size=15,family=S.SANS,weight=600),
          T(645,257,'condição pode adiá-los',size=13,fill=S.INK2),
          T(75,300,'Um negócio · três planos de análise, sem escala de duração',size=12,fill=S.INK2)]
    return S.svg(870,325,'Corte estratificado de um negócio jurídico: existência, validade e eficácia',o),[]
