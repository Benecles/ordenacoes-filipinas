"""Aula01 companion (destinação final), in the course hand: where the use of the good leads one professional buyer.

No params. Facts only from the companion's own passages: the farmer's fertiliser (REsp 208.793/MT, finalist reading),
the services employed in commercial activity (REsp 2.020.811, 2.001.086; the card cases), and concrete fragility
proved (finalismo mitigado; art. 29 equiparação). The consumo bond is the two-strand cord where the CDC applies; the
route that ends in insumo is cut by an orange limit. Positions order routes; they measure nothing. Nothing is boxed.
"""
from . import svg as S
from . import tgc01_hand as H


def build(p):
    xa, xj, xe = 110, 300, 650
    ys = (62, 138, 214)
    ym = ys[1]
    o = []
    o += [H.rule(f'M{xa + 8},{ym} H{xj}', S.INK, 2.0), H.mark(xa, ym, S.INK),
          H.name(xa, ym - 24, 'Adquirente', anchor='middle'),
          H.gloss(xa, ym + 34, 'empresa ou profissional', anchor='middle'),
          H.rule(f'M{xj},{ys[0]} V{ys[2]}', S.INK, 1.0), S.circle(xj, ym, 3.2, fill=S.INK, stroke=S.INK)]
    o.append(H.wire('proprio', 'Rastrear o uso que esgota o bem na própria necessidade', [
        H.cord(xj, xe - 8, ys[0]), H.mark(xe, ys[0], S.DIF),
        H.gloss(xj + 20, ys[0] - 20, 'uso próprio, esgotado na lavoura · REsp 208.793/MT'),
        H.name(xe + 20, ys[0] + 4, 'Destinatário final', S.DIF),
        H.gloss(xe + 20, ys[0] + 24, 'o CDC se aplica', S.DIF)]))
    o.append(H.wire('atividade', 'Rastrear o serviço empregado na atividade do adquirente', [
        H.rule(f'M{xj},{ym} H{xe - 8}', S.INK, 1.0), H.rule(f'M{xe - 86},{ym - 14} V{ym + 14}', S.CONC, 2.0),
        H.mark(xe, ym, S.CONC),
        H.gloss(xj + 20, ym - 20, 'serviço empregado na atividade comercial · ingressos, capital de giro'),
        H.name(xe + 20, ym + 4, 'Insumo', S.CONC),
        H.gloss(xe + 20, ym + 24, 'sem prova de vulnerabilidade, o CDC é afastado', S.CONC)]))
    o.append(H.wire('fragilidade', 'Rastrear a fragilidade concreta que justifica proteção excepcional', [
        H.rule(f'M{xj},{ys[2]} H{xe - 8}', S.DIF, 1.0, '3 5'), H.mark(xe, ys[2], S.DIF),
        H.gloss(xj + 20, ys[2] - 20, 'fragilidade concreta provada · caminhoneiro com um só veículo'),
        H.name(xe + 20, ys[2] + 4, 'Proteção excepcional', S.DIF),
        H.gloss(xe + 20, ys[2] + 24, 'finalismo mitigado · equiparação do art. 29')]))
    svg = S.svg(1080, 280, 'Percursos do adquirente profissional: uso próprio, atividade comercial e fragilidade provada', o)
    return svg.replace('viewBox="0 0 1080 280"', 'viewBox="0 24 1080 240"', 1), []
