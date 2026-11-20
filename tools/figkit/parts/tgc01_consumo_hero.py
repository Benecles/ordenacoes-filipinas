"""Aula01 companion (destinação final): circuit schematic of one professional buyer and where the use of the good leads.

No params. Facts only from the companion's own passages: the farmer's fertiliser (REsp 208.793/MT, finalist reading),
the services employed in commercial activity (REsp 2.020.811, 2.001.086; the card cases), and concrete fragility
proved (finalismo mitigado; art. 29 equiparação). Positions order routes; they measure nothing.
"""
from . import svg as S


def build(p):
    o = []
    T = S.text

    def wire(key, label, body):
        o.append('<g data-thread="' + key + '" tabindex="0" role="button" aria-label="' + label + '">' + ''.join(body) + '</g>')

    def line(d, col=S.INK, dash=None):
        return S.path(d, fill='none', stroke=col, stroke_width=1.8, stroke_dasharray=dash)

    def dot(x, y, col=S.INK):
        return S.circle(x, y, 6, fill=S.PAPER, stroke=col, stroke_width=1.8)

    def arrow(x, y, col=S.INK):
        return line(f'M{x-7},{y-4} L{x},{y} L{x-7},{y+4}', col)

    o += [T(45, 25, 'Quem adquire · o emprego do bem decide', size=12, fill=S.INK2)]
    o += [S.circle(60, 170, 6, fill=S.PAPER, stroke=S.INK, stroke_width=1.8),
          S.line(66, 170, 194, 170, stroke=S.INK, stroke_width=1.8),
          S.rect(194, 164, 12, 12, fill=S.INK, stroke=S.INK),
          T(45, 148, 'Adquirente', size=14, family=S.SANS, weight=600),
          T(45, 204, 'empresa ou profissional', size=12, fill=S.INK2)]
    wire('proprio', 'Rastrear o uso que esgota o bem na própria necessidade', [
        line('M200,164 L200,70 L600,70'), arrow(600, 70), dot(612, 70, S.DIF),
        T(240, 58, 'uso próprio, esgotado na lavoura', size=13),
        T(240, 94, 'adubo do agricultor · REsp 208.793/MT', size=12, fill=S.INK2),
        T(632, 76, 'destinatário final', size=14, family=S.SANS, weight=600, fill=S.DIF),
        T(632, 98, 'o CDC se aplica', size=12, fill=S.DIF)])
    wire('atividade', 'Rastrear o serviço empregado na atividade do adquirente', [
        line('M206,170 L600,170'), arrow(600, 170), dot(612, 170, S.CONC),
        T(240, 158, 'serviço empregado na atividade comercial', size=13),
        T(240, 194, 'ingressos · capital de giro · casa de tintas', size=12, fill=S.INK2),
        T(632, 176, 'insumo', size=14, family=S.SANS, weight=600, fill=S.CONC),
        T(632, 198, 'sem prova de vulnerabilidade, o CDC é afastado', size=12, fill=S.CONC)])
    wire('fragilidade', 'Rastrear a fragilidade concreta que justifica proteção excepcional', [
        line('M200,176 L200,270 L600,270', S.DIF, '5 5'), arrow(600, 270, S.DIF), dot(612, 270, S.DIF),
        T(240, 258, 'fragilidade concreta provada', size=13),
        T(240, 294, 'caminhoneiro com um só veículo · finalismo mitigado', size=12, fill=S.INK2),
        T(632, 276, 'proteção excepcional', size=14, family=S.SANS, weight=600, fill=S.DIF),
        T(632, 298, 'ou equiparação do art. 29', size=12, fill=S.INK2)])
    return S.svg(1080, 330, 'Circuito do adquirente profissional: uso próprio, atividade comercial e fragilidade provada', o), []
