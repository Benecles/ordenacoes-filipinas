"""Aula01, ch.1: a sieve of three meshes that sorts what the law does with human events.

No params. Items rest on the mesh that stops them; only the agreement of wills that shapes its own effects falls
through all three. Position is the sorting, not a scale. Facts: Venosa p. 2 (testamento, promessa de recompensa);
Pereira III p. 7 (negócio jurídico bilateral; acordo de vontades); the lesson's own ch.1 (nascimento, morte,
tomada de posse, domicílio, doação, seguro).
"""
from . import svg as S


def build(p):
    o = []
    T = S.text
    W, H = 870, 500
    ax = 130  # x of the aperture the contract falls through
    meshes = [(150, 'Há ato humano?'),
              (270, 'A vontade conforma os efeitos?'),
              (390, 'Duas vontades se encontram?')]
    # the three grains that fall through: compra e venda, seguro, doação
    for gx in (ax - 22, ax, ax + 22):
        o.append(S.circle(gx, 46, 6, fill=S.PAPER, stroke=S.DIF, stroke_width=2))
    o.append(T(ax + 52, 51, 'compra e venda, seguro, doação', size=14, family=S.SANS))
    o.append(S.line(ax, 58, ax, 450, stroke=S.DIF, stroke_width=2.4))
    for y, test in meshes:
        o.append(T(ax + 16, y - 30, test, size=14, family=S.SANS, weight='600'))
        # grating: a rail with teeth, open at the aperture
        for a, b in ((62, ax - 20), (ax + 20, 818)):
            o.append(S.line(a, y, b, y, stroke=S.INK, stroke_width=2))
            x = a + 6
            while x < b:
                o.append(S.line(x, y, x, y + 9, stroke=S.INK2, stroke_width=1))
                x += 11
        o.append(S.line(ax - 20, y - 5, ax - 20, y + 9, stroke=S.INK, stroke_width=2))
        o.append(S.line(ax + 20, y - 5, ax + 20, y + 9, stroke=S.INK, stroke_width=2))

    def item(x, y, head, l1, l2=None):
        o.append(S.circle(x, y - 9, 7, fill=S.PAPER, stroke=S.INK, stroke_width=2))
        o.append(T(x + 18, y - 8, head, size=14, family=S.SANS, weight='600'))
        o.append(T(x + 18, y + 24, l1, size=12.5, fill=S.INK2))
        if l2:
            o.append(T(x + 18, y + 41, l2, size=12.5, fill=S.INK2))

    item(300, 150, 'Nascimento, morte', 'fato natural: efeitos jurídicos', 'sem ato humano algum')
    item(300, 270, 'Tomada de posse', 'ato-fato: os efeitos', 'prescindem da conformação')
    item(590, 270, 'Domicílio', 'ato em sentido estrito:', 'a lei predetermina os efeitos')
    item(300, 390, 'Testamento', 'negócio unilateral: dispensa', 'o encontro de vontades')
    item(590, 390, 'Promessa de recompensa', 'vincula quem promete, sem', 'contrato com quem a lê')
    # the contract at the bottom
    o.append(S.circle(ax, 461, 8, fill=S.PAPER, stroke=S.DIF, stroke_width=2.4))
    o.append(T(ax + 28, 466, 'Contrato: acordo que conforma os próprios efeitos', size=14, family=S.SANS, weight='600', fill=S.INK))
    return S.svg(W, H, 'Peneira de três malhas: só o acordo de vontades que conforma seus efeitos passa por todas', o), []
