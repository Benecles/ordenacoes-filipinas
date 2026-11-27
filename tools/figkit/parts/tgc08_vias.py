"""Aula 08, chapters 2-3: two clickable instruments (data-opt / data-ans, wired by casa.js).
Params: mode = tres | momentos.
tres: the three ways to change a person in an obligation set on the same three places. Sai (left) and
  Entra (right) swap; Permanece (top) is the one who stays. The ledger between them has three rows
  (crédito com acessórios, dívida, deveres e exceções da posição): a blue line crosses from Sai to Entra
  when that row passes, an orange stub stays with Sai when it doesn't. The Permanece mark is a hollow
  circle (só notificado, art. 290) or a filled square (consent required). Sources: CC arts. 286-303;
  Luis Renato Ferreira da Silva pp. 3-7 (the page's own quotes and notes).
momentos: a time ruler for the cedido's consent. The cedente-cessionário ajuste is a dot; the cedido's
  consent is a square before it (prévio), on it (simultâneo) or after it (posterior, with the orange
  hatch for the stretch in which the negócio still depends on whoever stays). Sources: Luis Renato
  pp. 6-7; Orlando Gomes (p. 7).
"""
from . import svg as S

W = 1080


def _t(x, y, s, size=17, **kw):
    return S.text(x, y, s, size=size, family=S.SANS, **kw)


def _opts(choices, y, h=44, x0=30):
    n = len(choices)
    cw = (W - 2 * x0 - 12 * (n - 1)) / n
    o = []
    for i, (k, lab) in enumerate(choices):
        x = x0 + i * (cw + 12)
        o.append(f'<g data-opt="{k}" tabindex="0" role="button" aria-label="{S.esc(lab)}">')
        o.append(S.rect(x, y, cw, h, fill=S.PAPER, stroke=S.INK, stroke_width=1.6))
        o.append(S.text(x + cw / 2, y + 28, lab, size=17, family=S.SANS, weight='600', anchor='middle'))
        o.append('</g>')
    return o


def _panel(y, h, col, verdict, lines):
    o = [S.rect(30, y, W - 60, h, fill=S.PAPER, stroke=col, stroke_width=2),
         S.text(54, y + 36, verdict, size=22, family=S.SANS, weight='650', fill=col)]
    for i, (tag, line) in enumerate(lines):
        yy = y + 68 + i * 30
        o.append(S.text(54, yy, tag, size=14, family=S.MONO, fill=S.MUTED))
        o.append(S.text(190, yy, line, size=18, family=S.SERIF))
    return o


def _sq(x, y, r=11, col=S.INK):
    return S.rect(x - r, y - r, 2 * r, 2 * r, fill=col, stroke=col, stroke_width=1.5)


def _ring(x, y, r=10, col=S.INK):
    return S.circle(x, y, r, fill=S.PAPER, stroke=col, stroke_width=2.2)


# --- tres ---------------------------------------------------------------
CH3 = (('cred', 'Cessão de crédito'), ('div', 'Assunção de dívida'), ('pos', 'Cessão da posição contratual'))
ROWS3 = (('crédito e acessórios', 242), ('dívida', 302), ('deveres e exceções da posição', 362))
# per choice: roles (sai, entra, permanece), consent (True = consent required), rows passing, verdict, lines
T3 = {
    'cred': (('Cedente', 'Cessionário', 'Devedor'), False, (True, False, False), S.DIF,
             'Só o crédito circula; o devedor é notificado, não consulta',
             (('CONSENTE', 'Cedente e cessionário ajustam; ao devedor basta a notificação do art. 290.'),
              ('PASSA', 'O crédito com seus acessórios (art. 287); o resto da relação fica com o cedente.'),
              ('DEFESAS', 'O devedor opõe ao cessionário as suas exceções e as que tinha contra o cedente (art. 294).'))),
    'div': (('Devedor primitivo', 'Novo devedor', 'Credor'), True, (False, True, False), S.DIF,
            'A dívida muda de mãos se o credor consentir expressamente',
            (('CONSENTE', 'O credor, de modo expresso (art. 299); o silêncio, após o prazo assinado, vale como recusa.'),
             ('PASSA', 'O polo passivo, com a prestação preservada; o contrato segue entre as partes primitivas.'),
             ('DEFESAS', 'O novo devedor não opõe ao credor as exceções pessoais do primitivo (art. 302).'))),
    'pos': (('Cedente', 'Cessionário', 'Cedido'), True, (True, True, True), S.DIF,
            'A relação inteira passa, e o cedido precisa querer',
            (('CONSENTE', 'As três vontades: cedente, cessionário e cedido, antes, junto ou depois do ajuste.'),
             ('PASSA', 'A participação completa: direitos, deveres, ações, pretensões e exceções da relação.'),
             ('DEFESAS', 'O cedido segue com o contrato-base, agora com o novo titular no lugar do cedente.'))),
}
XS, XE, XP = 140, 940, 540


def _tres():
    o = [S.text(24, 26, 'três maneiras de trocar uma pessoa na obrigação', size=13, family=S.MONO)]
    o += _opts(CH3, 40)
    for k, lab in CH3:
        (sai, entra, perm), consent, rows, col, verdict, lines = T3[k]
        i = [c[0] for c in CH3].index(k)
        o.append(f'<g data-ans="{k}"' + ('' if i == 0 else ' display="none"') + '>')
        # the one who stays
        o.append(S.rect(XP - 100, 106, 200, 46, fill=S.PAPER, stroke=S.INK, stroke_width=1.8))
        o.append(_t(XP, 136, perm, 19, weight='600', anchor='middle'))
        o.append(S.line(XP, 152, XP, 214, stroke=S.INK, stroke_width=1.4, stroke_dasharray='2 5'))
        if consent:
            o.append(_sq(XP, 214, 12))
            o.append(_t(XP + 24, 220, 'consente', 16, fill=S.INK, anchor='start'))
        else:
            o.append(_ring(XP, 214, 10))
            o.append(_t(XP + 24, 220, 'só é notificado', 16, fill=S.INK2, anchor='start'))
        # leaving and entering
        for x, name, ent in ((XS, sai, False), (XE, entra, True)):
            o.append(S.rect(x - 110, 236, 220, 178, fill=S.PAPER, stroke=S.DIF if ent else S.CONC, stroke_width=1.8,
                            stroke_dasharray=None if ent else '5 4'))
            o.append(_t(x, 262, name, 18, weight='600', anchor='middle', fill=S.DIF if ent else S.CONC))
            o.append(_t(x, 282, 'entra' if ent else 'sai', 13, anchor='middle', fill=S.MUTED))
        for (name, y), moves in zip(ROWS3, rows):
            y = y + 20
            o.append(_t(XP, y - 12, name, 16, anchor='middle', fill=S.INK if moves else S.MUTED))
            if moves:
                o.append(S.line(XS + 110, y, XE - 110, y, stroke=S.DIF, stroke_width=3))
                o.append(S.path(f'M{XE-110} {y} l-12 -7 v14 z', fill=S.DIF, stroke=S.DIF, stroke_width=1))
                o.append(S.circle(XS + 110, y, 6, fill=S.DIF, stroke=S.DIF, stroke_width=1))
            else:
                o.append(S.line(XS + 110, y, XS + 250, y, stroke=S.CONC, stroke_width=3, stroke_dasharray='7 5'))
                o.append(_t(XS + 262, y + 5, 'fica', 15, fill=S.CONC, anchor='start'))
        o += _panel(434, 140, col, verdict, lines)
        o.append('</g>')
    return S.svg(W, 592, 'Cessão de crédito, assunção de dívida e cessão da posição sobre as mesmas três posições', o), []


# --- momentos ------------------------------------------------------------
CH4 = (('pre', 'Anuência prévia'), ('sim', 'Anuência simultânea'), ('pos', 'Anuência posterior'))
XB, XC, XD = 250, 600, 920
T4 = {
    'pre': (S.DIF, 'A autorização vem no contrato-base',
            (('QUANDO', 'Ao assinar o contrato que vier a ser cedido, com as exigências postas nele.'),
             ('EXEMPLO', 'Promessa de compra e venda com cláusula para escriturar a quem o promitente indicar.'),
             ('EFEITO', 'A transferência corre dentro das condições pactuadas; a adesão prévia hoje é admitida.'))),
    'sim': (S.DIF, 'O cedido comparece no instrumento de cessão',
            (('QUANDO', 'No mesmo ato em que cedente e cessionário ajustam; é o modo mais corriqueiro.'),
             ('QUEM', 'O interveniente-anuente, que aceita a substituição do cedente pelo cessionário.'),
             ('EFEITO', 'Ajuste e anuência completam o negócio juntos.'))),
    'pos': (S.CONC, 'O ajuste espera por quem permanece',
            (('QUANDO', 'Depois do ajuste; nesta modalidade é viável o consentimento tácito.'),
             ('ENQUANTO', 'O negócio ainda depende do cedido, e a substituição ajustada não o vincula.'),
             ('EFEITO', 'A anuência completa o negócio já ajustado entre cedente e cessionário.'))),
}


def _momentos():
    o = [S.text(24, 26, 'quando o cedido consente, em relação ao ajuste da cessão', size=13, family=S.MONO)]
    o += _opts(CH4, 40)
    o.append(_t(XB, 130, 'contrato-base', 15, anchor='middle', fill=S.INK2))
    o.append(_t(XC, 130, 'ajuste da cessão', 15, anchor='middle', fill=S.INK2))
    y = 190
    o.append(S.line(60, y, 1020, y, stroke=S.MUTED, stroke_width=1.2))
    o.append(S.circle(XB, y, 5, fill=S.INK, stroke=S.INK, stroke_width=1))
    o.append(S.line(XB, y + 10, XB, y + 56, stroke=S.GRID, stroke_width=1, stroke_dasharray='2 5'))
    o.append(S.line(XC, y + 10, XC, y + 56, stroke=S.GRID, stroke_width=1, stroke_dasharray='2 5'))
    o.append(S.circle(XC, y, 6, fill=S.INK, stroke=S.INK, stroke_width=1))
    o.append(_t(60, y - 12, 'tempo', 13, anchor='start', fill=S.MUTED))
    for k, lab in CH4:
        col, verdict, lines = T4[k]
        i = [c[0] for c in CH4].index(k)
        o.append(f'<g data-ans="{k}"' + ('' if i == 0 else ' display="none"') + '>')
        if k == 'pre':
            o.append(S.path(f'M{XB} {y-9} H{XC} V{y+9} H{XB} Z', fill='none', stroke=S.INK2, stroke_width=1.4))
            o.append(_sq(XB, y, 12))
            o.append(_t(XB, y + 48, 'cláusula do contrato-base', 16, anchor='middle', fill=S.INK2))
        elif k == 'sim':
            o.append(_sq(XC, y, 13, S.DIF))
            o.append(S.circle(XC, y, 5, fill=S.PAPER, stroke=S.PAPER, stroke_width=1))
            o.append(_t(XC, y + 48, 'interveniente-anuente', 16, anchor='middle', fill=S.INK2))
        else:
            for hl in S.hatch(XC, y - 9, XD - XC, 18, step=8, stroke=S.CONC, stroke_width=1.2):
                o.append(hl)
            o.append(S.path(f'M{XC} {y-9} H{XD} V{y+9} H{XC} Z', fill='none', stroke=S.CONC, stroke_width=1.4))
            o.append(_sq(XD, y, 12, S.CONC))
            o.append(_t((XC + XD) / 2, y + 48, 'ainda depende de quem permanece', 16, anchor='middle', fill=S.CONC))
        o += _panel(290, 140, col, verdict, lines)
        o.append('</g>')
    return S.svg(W, 448, 'Anuência do cedido antes, junto e depois do ajuste da cessão', o), []


def build(p):
    mode = p.get('mode', 'tres')
    fn = {'tres': _tres, 'momentos': _momentos}.get(mode)
    if fn is None:
        raise ValueError(f'unknown Aula 08 vias mode: {mode}')
    return fn()
