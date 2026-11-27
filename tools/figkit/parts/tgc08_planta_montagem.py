"""Aula 08: a position as an assembly, a sorting pegboard and a tracing overlay.

Params: mode = planta | encaixes | pelicula. No case quantities are encoded.
planta has three focusable threads: direitos, deveres, exceções. Its cartridge
and fixed socket express global succession, not three independent assignments.
encaixes uses mating contacts, not labelled containers: an individual tooth,
another individual tooth, the complete comb and a second dependent comb.
pelicula has an initial outline and a superposed registered tracing, toggled by
the page's checkbox via [data-film]. Sources: Luis Renato pp.397–408;
Venosa pp.27,46–47; REsp356.383/SP as transcribed in Luis Renato pp.395–396.
"""
from . import svg as S


def build(p):
    mode = p.get('mode', 'planta')
    out = []

    def line(x, y, xx, yy, color=S.INK, width=1.5, **kw):
        out.append(S.line(x, y, xx, yy, stroke=color, stroke_width=width, **kw))

    def text(x, y, label, **kw):
        kw.setdefault('size', 13 if mode == 'planta' else 14)
        out.append(S.text(x, y, label, **kw))

    def path(d, color=S.INK, width=1.5, **kw):
        out.append(S.path(d, fill='none', stroke=color, stroke_width=width, **kw))

    def dot(x, y, r=5, color=S.INK):
        out.append(S.circle(x, y, r, fill=S.PAPER, stroke=color, stroke_width=1.5))

    if mode == 'planta':
        w, h = 1000, 355
        # An open socket stays fixed while the exploded cartridge converges on it.
        path('M630 83 H812 V298 H630 M630 83 V113 M630 268 V298', width=2)
        text(720, 57, 'o mesmo contrato', anchor='middle', size=14)
        text(910, 307, 'cedido', anchor='middle')
        line(910, 153, 910, 255)
        dot(910, 204, 8)
        # The cedente's carrier is empty after transfer. The three contacts
        # travel inside one rigid position, not as three separate assignments.
        path('M33 72 H196 V300 H33 Z', color=S.MUTED, stroke_dasharray='3 5')
        for yy in (90, 155, 220):
            path(f'M52 {yy} H138 L170 {yy+29} H84 Z', color=S.MUTED, width=1.2, stroke_dasharray='3 4')
            path(f'M170 {yy+15} H276', color=S.MUTED, width=1.2, stroke_dasharray='2 5')
        text(115, 335, 'cedente · sai', anchor='middle')
        text(384, 29, 'cessionário · entra', anchor='middle', size=14)
        text(384, 58, 'posição · unidade', anchor='middle', size=13, fill=S.DIF)
        path('M218 46 H551 M218 46 V58 M551 46 V58', color=S.MUTED)
        # A continuous frame and spine bind every contact into one object.
        path('M226 72 H548 V286 H226 Z', color=S.DIF, width=2.3)
        line(250, 88, 250, 270, S.DIF, 2.1)
        layers = [('direitos', 90, 146), ('deveres', 155, 204), ('exceções', 220, 262)]
        for i, (label, yy, contact) in enumerate(layers):
            out.append(f'<g data-thread="{label}" data-fio="{label}" tabindex="0" role="button" aria-label="Traçar {label}">')
            # Parallelogram laminae and their matched connector in the socket.
            path(f'M250 {yy} L451 {yy} L511 {yy+29} L250 {yy+29} Z', width=1.7)
            text(374, yy+20, label, anchor='middle', size=13)
            path(f'M511 {yy+15} L647 {contact} H683', stroke_dasharray='3 4')
            path(f'M683 {contact-9} H710 V{contact+9} H683 Z', width=1.8)
            line(710, contact, 910, contact)
            dot(910, contact)
            out.append('</g>')
        # The cedido's consent gate applies to the whole framed position.
        line(607, 116, 607, 286, S.CONC, 2.5)
        text(607, 316, 'anuência de quem permanece', anchor='middle', size=13, fill=S.CONC)
    elif mode == 'encaixes':
        w, h = 900, 466
        # The small regular holes establish a genuine pegboard surface.
        for x in range(288, 858, 25):
            for y in range(70, 391, 25):
                out.append(S.circle(x, y, 1.1, fill=S.GRID))
        labels = ['crédito', 'dívida', 'posição contratual']
        text(340, 26, 'direitos', anchor='middle')
        text(530, 26, 'deveres', anchor='middle')
        text(720, 26, 'exceções', anchor='middle')
        for row, label in enumerate(labels):
            y = 82 + row*91
            text(22, y+5, label, family=S.SANS, size=19)
            for x in (340, 530, 720):
                dot(x, y, 10, S.MUTED)
            if row < 2:
                x = (340, 530)[row]
                path(f'M{x-32} {y-24} H{x+32} V{y+24} H{x-32} Z', width=2)
                dot(x, y, 5)
            else:
                # One continuous plate encloses all three contacts. Its closed
                # geometry distinguishes the position from either isolated pole.
                path(f'M308 {y-27} H752 V{y+27} H308 Z', color=S.DIF, width=2.4)
                line(340, y, 720, y, S.DIF, 2.2)
        # A sub-contract is a second relation sharing one participant. The
        # dotted tie marks dependence; the base relation remains intact.
        y = 404
        text(22, y+5, 'subcontrato', family=S.SANS, size=19)
        path(f'M310 {y-18} H530 V{y+18} H310 Z', color=S.INK2, width=1.8)
        path(f'M530 {y-18} H750 V{y+18} H530 Z', color=S.MUTED, width=1.8)
        dot(310, y, 7); dot(530, y, 7); dot(750, y, 7)
        line(530, y+20, 530, y+42, S.CONC, 1.5, stroke_dasharray='3 4')
        text(420, y+42, 'base preservada', anchor='middle', size=13, fill=S.INK2)
        text(640, y+42, 'vínculo derivado', anchor='middle', size=13, fill=S.INK2)
    elif mode == 'pelicula':
        w, h = 900, 390
        # Fixed registration marks and coincident linework make the overlay an
        # actual act of superposition. The outgoing participant stays as a trace.
        for x, y in ((170, 56), (820, 56), (170, 312), (820, 312)):
            line(x-7, y, x+7, y, S.MUTED, 1)
            line(x, y-7, x, y+7, S.MUTED, 1)
        path('M155 43 H835 V327 H155 Z', color=S.MUTED, width=1)
        text(495, 25, 'REsp 356.383/SP · posição transmitida', anchor='middle', size=15)
        text(90, 182, 'arrendadora', anchor='middle', size=14)
        dot(205, 177, 9)
        # Three contacts of the one position: arrows are unnecessary because the
        # film registers precisely on the existing paths.
        for j, label in enumerate(('créditos', 'débitos', 'defesas')):
            y = 111 + j*66
            path(f'M205 177 H255 V{y} H731', color=S.MUTED)
            dot(731, y, 5, S.MUTED)
            text(480, y-12, label, anchor='middle')
        out.append('<g data-gone="true">')
        path('M707 84 H758 V269 H707', color=S.MUTED, stroke_dasharray='4 4')
        text(731, 302, 'arrendatária original', anchor='middle', size=13, fill=S.MUTED)
        out.append('</g>')
        out.append('<g data-film="true" data-dx="110">')
        path('M170 56 H820 V312 H170 Z', color=S.DIF, width=1)
        for y in (111, 177, 243):
            path(f'M205 177 H255 V{y} H731', color=S.DIF, width=2)
            dot(731, y, 6, S.DIF)
        path('M698 79 H767 V274 H698', color=S.DIF, width=2)
        text(186, 300, 'película da sucessora · cessionária', fill=S.DIF, size=14)
        out.append('</g>')
        text(220, 355, 'arrendadora · cedida', size=14)
    else:
        raise ValueError(f'unknown Aula 08 assembly mode: {mode}')
    label = S.esc(p.get('label', 'Cessão da posição contratual'))
    desktop = f'<svg data-assembly="full" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">' + ''.join(out) + '</svg>'
    # A separate setting of the same assembly keeps type legible on a phone.
    # It changes geometry, never facts, and shares the same thread/film hooks.
    out = []
    w, h = 340, 420
    if mode == 'planta':
        text(170, 24, 'cessionário · entra', anchor='middle', size=15)
        for i, word in enumerate(('direitos', 'deveres', 'exceções')):
            y = 53 + 51*i
            out.append(f'<g data-thread="{word}" data-fio="{word}" tabindex="0" role="button" aria-label="Traçar {word}">')
            path(f'M42 {y} H220 L268 {y+23} H90 Z', width=1.7)
            text(153, y+17, word, anchor='middle', size=13)
            x = 116 + 54*i
            path(f'M268 {y+12} H{290+i*14} V244 H{x} V278', stroke_dasharray='3 4')
            dot(x, 278)
            line(x, 284, x, 315)
            out.append('</g>')
        line(62, 260, 312, 260, S.CONC, 2)
        text(170, 238, 'anuência do cedido', anchor='middle', size=13, fill=S.CONC)
        path('M91 273 H249 V335 H91 Z', width=2)
        text(170, 357, 'o mesmo contrato', anchor='middle', size=14)
        path('M22 300 H72 V335 H22 Z', color=S.MUTED, stroke_dasharray='3 4')
        text(21, 382, 'cedente · sai', size=12)
        text(240, 382, 'cedido', size=12)
        line(249, 315, 285, 315)
        dot(285, 315)
    elif mode == 'encaixes':
        h = 500
        text(155, 22, 'direitos', size=12, anchor='middle')
        text(225, 22, 'deveres', size=12, anchor='middle')
        text(296, 22, 'defesas', size=12, anchor='middle')
        for row, name in enumerate(('crédito', 'dívida', 'posição')):
            y = 80 + row*94
            text(7, y+5, name, size=13, family=S.SANS)
            for x in (155, 225, 296):
                dot(x, y, 7, S.MUTED)
            if row < 2:
                x = (155, 225)[row]
                path(f'M{x-20} {y-19} H{x+20} V{y+19} H{x-20} Z', width=2)
            else:
                path(f'M136 {y-24} H316 V{y+24} H136 Z', color=S.DIF, width=2.2)
                line(155, y, 296, y, S.DIF, 2)
        y = 390
        text(5, y+5, 'subcontrato', size=13, family=S.SANS)
        path(f'M118 {y-16} H212 V{y+16} H118 Z', color=S.INK2, width=1.5)
        path(f'M212 {y-16} H314 V{y+16} H212 Z', color=S.MUTED, width=1.5)
        dot(118, y, 5); dot(212, y, 5); dot(314, y, 5)
        line(212, y+18, 212, y+43, S.CONC, 1.3, stroke_dasharray='3 4')
        text(165, y+47, 'base', anchor='middle', size=11, fill=S.INK2)
        text(263, y+47, 'derivado', anchor='middle', size=11, fill=S.INK2)
    else:
        h = 400
        path('M20 48 H320 V355 H20 Z', color=S.MUTED, width=1)
        text(170, 24, 'arrendadora · cedida', anchor='middle', size=14)
        dot(170, 68, 8)
        for j, word in enumerate(('créditos', 'débitos', 'defesas')):
            x = 71 + 99*j
            path(f'M170 68 V115 H{x} V257', color=S.MUTED)
            dot(x, 257, 5, S.MUTED)
            text(x, 149, word, anchor='middle', size=12)
        out.append('<g data-gone="true">')
        path('M48 236 H292 V279 H48 Z', color=S.MUTED, stroke_dasharray='3 4')
        text(170, 308, 'arrendatária original', anchor='middle', size=13, fill=S.MUTED)
        out.append('</g>')
        out.append('<g data-film="true" data-dx="28">')
        path('M30 58 H310 V345 H30 Z', color=S.DIF, width=1)
        for x in (71, 170, 269):
            path(f'M170 68 V115 H{x} V257', color=S.DIF, width=2)
            dot(x, 257, 6, S.DIF)
        path('M43 231 H297 V284 H43 Z', color=S.DIF, width=2)
        text(170, 335, 'sucessora · cessionária', anchor='middle', size=13, fill=S.DIF)
        out.append('</g>')
    compact = f'<svg data-assembly="compact" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">' + ''.join(out) + '</svg>'
    return desktop + compact, []
