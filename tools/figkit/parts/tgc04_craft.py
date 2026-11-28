"""Aula 04 in the course's hand: consent as a signature mark (passos, state 0-2); nomination as a curtained threshold.
Symbolic paper objects, not reconstructions of the running case. Pereira III pp.102-106; CC439-440,467-471."""
from . import svg as S
from .tgc01_hand import cord, rule, mark, name, gloss, bracket


def build(p):
    mode = p.get('mode', 'consent')
    state = int(p.get('state', 0))
    o = []
    if mode == 'consent':
        W, H = 480, 280
        o += [name(110, 70, 'promitente', anchor='middle'), name(370, 70, 'terceiro', anchor='middle'),
              mark(110, 100, S.DIF if state == 2 else S.INK), mark(370, 100, S.DIF if state == 2 else S.INK)]
        if state == 0:
            o.append(rule('M122,100 H358', S.INK, 1.4, '3 5'))
        elif state == 1:
            o += [rule('M122,100 H228', S.INK, 1.4, '3 5'), rule('M252,100 H358', S.INK, 1.4, '3 5'), rule('M240,86 V114', S.CONC, 2.4)]
        else:
            o.append(cord(118, 362, 100))
        o += [rule('M50,190 H190', S.INK, 1.2),
              rule('M62,180 q15,-27 20,-9 t19,-7 q-6,24 16,10 l34,-8', S.INK if state != 2 else S.MUTED, 2),
              gloss(50, 214, 'obter o compromisso'), rule('M290,190 H430', S.CONC if state == 1 else S.INK, 1.2)]
        if state == 1:
            o += [rule('M298,178 L322,202', S.CONC, 2), rule('M322,178 L298,202', S.CONC, 2)]
        if state == 2:
            o.append(rule('M300,180 q10,-34 19,-12 t18,-6 q-9,23 11,10 l47,-9', S.DIF, 2))
        lab = ['compromisso ainda pendente', 'recusa: perdas e danos', 'anuência: terceiro obrigado'][state]
        o.append(gloss(240, 258, lab, S.CONC if state == 1 else S.DIF if state == 2 else S.INK, anchor='middle', size=15))
        return S.svg(W, H, 'A anuência muda quem deve ao credor', o), []
    if mode == 'nomination':
        W, H = 490, 330
        # Hairline room, the curtain drawn aside in the doorway; the nominee holds the whole position.
        o += [rule('M60,70 H420 V120 M420,200 V260 H60 V70', S.INK, 1), rule('M414,120 H426 M414,200 H426', S.INK, 1)]
        o += [rule(f'M{420 + k * 6},121 q-8,13 0,26 t0,26 t0,27', S.INK2, 1) for k in range(2)]
        o += [bracket(120, 340, 100, True, S.DIF), name(230, 88, 'posição inteira', S.DIF, anchor='middle'),
              mark(230, 160, S.DIF, r=9), name(230, 192, 'nomeada', S.DIF, anchor='middle'),
              gloss(230, 238, 'direitos e obrigações', anchor='middle'),
              mark(456, 176, S.MUTED, r=7), rule('M450,170 L462,182', S.MUTED, 1.4),
              name(456, 300, 'originária', S.MUTED, anchor='end'), rule('M456,282 V190', S.MUTED, 1, '3 5'),
              gloss(60, 322, 'efeitos desde a celebração', S.DIF)]
        return S.svg(W, H, 'Nomeação eficaz: uma pessoa assume a posição inteira', o), []
    raise ValueError(mode)
