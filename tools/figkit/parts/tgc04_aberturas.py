"""Aula 04 in the course's hand (DIRECTION.md, o vínculo): a floor plan drawn in hairlines, the two-strand cord
running through it. Params: mode = planta (default) | memoria | janela | talao.
Sources: CC417-420, 436-440, 462-471; Pereira III pp.73-106. Schematic, never a reconstruction of Ilha Plaza; no invented
dates, amounts or physical facts. Windows and doors encode consent. Focusable threads are alternatives, not a sequence.
"""
from . import svg as S
from .tgc01_hand import cord, rule, mark, name, gloss, hit

T = S.text


def thread(key, label, items):
    return (f'<g class="thread" data-thread="{key}" role="button" tabindex="0" aria-label="Traçar {S.esc(label)}" '
            f'aria-pressed="false">' + ''.join(items) + '</g>')


def zig(x, y0, y1, dx, n):
    """Torn edge: a zigzag hairline from y0 to y1 about x."""
    step = (y1 - y0) / n
    return ''.join(f' L{x + (dx if i % 2 == 0 else 0):.1f},{y0 + (i + 1) * step:.1f}' for i in range(n))


def build(p):
    mode = p.get('mode', 'planta')
    o = []
    if mode in ('planta', 'memoria'):
        full = mode == 'planta'
        dx = 0 if full else 170
        X = lambda v: v + dx
        W, H = 1084, 340
        INK = S.INK
        # Hairline walls: outer shell, the party wall with the preliminar, and (planta) the right wing.
        right = 1044 if full else 720
        walls = [f'M{X(40)},78 H{X(440)}', f'M{X(540)},78 H{X(right)} V300 H{X(40)} V78',
                 f'M{X(300)},78 V160', f'M{X(300)},220 V300']
        if full:
            walls += [f'M{X(720)},78 V110', f'M{X(720)},180 V230', f'M{X(720)},280 V300', f'M{X(720)},196 H{X(1044)}']
        o += [rule(d, INK, 1) for d in walls]
        # Door to the preliminar's room: leaf and swing.
        o += [rule(f'M{X(300)},220 H{X(240)}', INK, 1), rule(f'M{X(300)},160 A60,60 0 0 0 {X(240)},220', S.INK2, 1)]
        # Window onto the street: the sill is two hairlines; the beneficiary stands outside.
        o += [rule(f'M{X(440)},73 V83', INK, 1), rule(f'M{X(540)},73 V83', INK, 1), rule(f'M{X(440)},84 H{X(540)}', S.INK2, 1)]
        # The bond: two strands between the parties, tied at both ends.
        o += [cord(X(352), X(640), 190), mark(X(346), 190, S.DIF), mark(X(646), 190, S.DIF)]
        jx = X(495)
        o.append(S.circle(jx, 190, 5, fill=S.PAPER, stroke=S.DIF, stroke_width=1.8))
        # Beneficiário: the performance crosses the wall through the window; the third is no party.
        fav = [rule(f'M{jx},184 V34', S.DIF, 2), mark(jx, 27, S.DIF),
               name(jx + 16, 31, 'beneficiário' if full else 'benefício alheio', S.DIF),
               gloss(jx + 16, 58, 'direito próprio à prestação' if full else 'formação entre dois'),
               hit(jx - 14, 20, 200, 160)]
        o.append(thread('favor', 'estipulação em favor de terceiro', fav))
        # Preliminar: the bond reaches the door, then dashes on to a later contract.
        pre = [rule(f'M{X(339)},190 H{X(300)}', S.INK, 2), rule(f'M{X(300)},190 H{X(136)}', S.INK, 1.4, '3 5'),
               mark(X(130), 190), name(X(66), 130, 'preliminar' if full else 'contrato futuro'),
               gloss(X(66), 152, 'dever de celebrar o definitivo' if full else 'promessa já vinculante'),
               hit(X(48), 100, 296, 180)]
        o.append(thread('preliminar', 'contrato preliminar', pre))
        # Arras: the counterfoil torn in two on the junction.
        ay0, ay1 = 236, 274
        lh = f'M{jx - 6},{ay0} H{jx - 46} V{ay1} H{jx - 6}' + zig(jx - 6, ay1, ay0, 5, 6)
        rh = f'M{jx + 6},{ay0} H{jx + 46} V{ay1} H{jx + 6}' + zig(jx + 6, ay1, ay0, -5, 6)
        arr = [rule(f'M{jx},195 V{ay0 - 2}', S.INK, 2), rule(lh, S.INK, 1.2), rule(rh, S.INK, 1.2),
               gloss(jx, 292, 'arras: entrega do sinal' if full else 'sinal entregue: duas funções', anchor='middle'),
               hit(jx - 70, 200, 140, 100)]
        o.append(thread('arras', 'arras', arr))
        if full:
            # Pessoa a declarar: a curtain in the doorway; the named person takes the place from the celebration.
            cur = ''.join(rule(f'M{720 + k * 6},112 q-6,9 0,17 t0,17 t0,17 t0,17', S.INK2, 1) for k in range(2))
            pes = [rule('M646,190 H684 V145 H893', S.DIF, 2), mark(900, 145, S.DIF), cur,
                   name(752, 106, 'pessoa a declarar'), gloss(752, 176, 'assume desde a celebração'),
                   hit(724, 80, 316, 112)]
            o.append(thread('pessoa', 'pessoa a declarar', pes))
            # Fato de terceiro: a door the third holds from the far side; a refusal cuts the dashes.
            fat = [rule('M684,190 V255 H720', S.INK, 2), rule('M720,255 H874', S.INK, 1.4, '3 5'), mark(880, 255),
                   rule('M720,230 A50,50 0 0 1 770,280', S.INK2, 1), rule('M720,280 H770', S.INK, 1),
                   S.circle(763, 273, 2.6, fill=S.INK, stroke=S.INK),
                   rule('M806,244 V266', S.CONC, 2.4),
                   name(752, 224, 'fato de terceiro · anuência'), gloss(800, 290, 'recusa: responde quem prometeu', S.CONC),
                   hit(724, 200, 316, 100)]
            o.append(thread('fato', 'promessa de fato de terceiro', fat))
        return S.svg(W, H, 'Planta contratual: os limiares da formação e do cumprimento', o), []
    if mode == 'janela':
        W, H = 500, 250
        o += [rule('M40,40 H370 V105 M370,205 V235 H40 V40', S.INK, 1),
              rule('M364,105 H376', S.INK, 1), rule('M364,205 H376', S.INK, 1),
              rule('M365,105 V205', S.INK2, 1), rule('M375,105 V205', S.INK2, 1)]
        o += [cord(102, 242, 155, half=16, taper=22), mark(94, 155, S.DIF), mark(250, 155, S.DIF),
              name(94, 128, 'estipulante', anchor='middle'), name(250, 128, 'promitente', anchor='middle'),
              gloss(172, 192, 'acordo', anchor='middle'),
              rule('M257,155 H414', S.DIF, 2), mark(422, 155, S.DIF),
              gloss(318, 142, 'prestação', S.DIF, anchor='middle'),
              name(440, 196, 'beneficiário', anchor='middle')]
        return S.svg(W, H, 'A prestação atravessa a janela; a formação permanece entre dois', o), []
    if mode == 'talao':
        W, H = 800, 320
        n = 11
        # A counterfoil book: the spine, the stub, the torn half. Hairline paper, the words in the engraver's hand.
        stub = f'M72,48 H340 V268 H72' + ''
        o += [rule('M60,40 V276', S.INK, 2), rule('M72,48 H340', S.INK, 1.2), rule('M72,268 H340', S.INK, 1.2),
              rule('M340,48' + zig(340, 48, 268, 9, n), S.INK, 1.2),
              rule('M468,48 H736 V268 H468' + zig(468, 268, 48, -9, n), S.INK, 1.2)]
        for y in (110, 160, 210):
            o += [rule(f'M92,{y} H318', S.GRID, 1), rule(f'M492,{y} H714', S.GRID, 1)]
        o += [name(92, 80, 'canhoto'), name(492, 80, 'sinal entregue'),
              gloss(92, 104, 'quem deu'), gloss(492, 104, 'quem recebeu'),
              gloss(92, 152, 'contrato confirmado'), gloss(492, 152, 'imputação ou restituição'),
              gloss(92, 202, 'sem arrependimento'), gloss(492, 202, 'mínimo indenizatório', S.DIF),
              gloss(92, 252, 'com arrependimento'), gloss(492, 252, 'limite indenizatório', S.CONC),
              gloss(60, 304, 'A entrega ocorre agora; a função da quantia depende do que foi pactuado.')]
        return S.svg(W, H, 'Talão destacado: sinal transferido e função confirmatória ou penitencial', o), []
    raise ValueError(mode)
