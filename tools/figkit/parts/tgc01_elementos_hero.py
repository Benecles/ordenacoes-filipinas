"""Aula01 companion (elementos): circuit schematic of art. 104's three requirements and what each failure does.

No params. Facts only from the companion's passages: CC art. 104 (agente capaz, objeto lícito possível determinado ou
determinável, forma prescrita ou não defesa), art. 497 (tutor), art. 426 (herança de pessoa viva), art. 107 and
Pereira p. 33 (forma essencial: o contrato não prevalece). Positions order the requirements; they measure nothing.
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

    o += [T(45, 25, 'Art. 104 · a validade requer', size=12, fill=S.INK2)]
    o += [S.circle(60, 170, 6, fill=S.PAPER, stroke=S.INK, stroke_width=1.8),
          S.line(66, 170, 194, 170, stroke=S.INK, stroke_width=1.8),
          S.rect(194, 164, 12, 12, fill=S.INK, stroke=S.INK),
          T(45, 148, 'Negócio', size=14, family=S.SANS, weight=600),
          T(45, 204, 'reconhecível', size=12, fill=S.INK2)]
    wire('agente', 'Rastrear o requisito do agente capaz', [
        line('M200,164 L200,70 L600,70'), arrow(600, 70), dot(612, 70, S.CONC),
        T(240, 58, 'I · agente capaz', size=13),
        T(240, 94, 'capacidade geral e legitimação para este negócio', size=12, fill=S.INK2),
        T(632, 76, 'venda ao tutor do bem tutelado', size=14, family=S.SANS, weight=600, fill=S.CONC),
        T(632, 98, 'art. 497, I: nulidade', size=12, fill=S.INK2)])
    wire('objeto', 'Rastrear o requisito do objeto lícito, possível e determinado', [
        line('M206,170 L600,170'), arrow(600, 170), dot(612, 170, S.CONC),
        T(240, 158, 'II · objeto lícito, possível, determinável', size=13),
        T(240, 194, 'a prestação e o bem precisam ser idôneos', size=12, fill=S.INK2),
        T(632, 176, 'herança de pessoa viva', size=14, family=S.SANS, weight=600, fill=S.CONC),
        T(632, 198, 'art. 426: contrato vedado', size=12, fill=S.INK2)])
    wire('forma', 'Rastrear o requisito da forma prescrita ou não defesa', [
        line('M200,176 L200,270 L600,270'), arrow(600, 270), dot(612, 270, S.CONC),
        T(240, 258, 'III · forma prescrita ou não defesa em lei', size=13),
        T(240, 294, 'regra: simples acordo; exceção: forma essencial', size=12, fill=S.INK2),
        T(632, 276, 'forma exigida e não observada', size=14, family=S.SANS, weight=600, fill=S.CONC),
        T(632, 298, 'art. 107: o contrato não prevalece', size=12, fill=S.INK2)])
    return S.svg(1080, 330, 'Circuito dos três requisitos de validade do art. 104 e da consequência de cada falha', o), []
