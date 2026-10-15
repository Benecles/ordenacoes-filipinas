"""Aula 13 instruments: the dated Juizado record, a 30-day ruler, and its conditional variation."""
from figkit import t, line, svg

PAGE = 'courses/processo-civil-i/aula-13.html'


def docket_panel():
    """A paper record with only the dates and filing details the judgment excerpt supplies."""
    o = ''
    # The open folio is the information-bearing object; no text sits in ruled cells.
    o += '<path d="M34 78L34 513L1044 513L1044 78L977 48L554 72L528 82L505 72L91 48Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:2"/>'
    o += '<path d="M527 83L527 511" style="fill:none;stroke:var(--grid-major);stroke-width:1.5"/>'
    o += '<path d="M48 93L507 76M548 76L1028 93" style="fill:none;stroke:var(--grid-major);stroke-width:1"/>'
    o += t(66, 119, '2º JUIZADO ESPECIAL CÍVEL · FLORIANÓPOLIS', size=13, weight=700)
    o += t(1015, 119, 'AUTOS 0321861-32.2015.8.24.0023', size=11, anchor='end', fill='var(--ink-2)', weight=600)
    o += line(67, 137, 1013, 137, tone='ink', w=1.2)
    # The decision locates the purchase month in the contestation and the filing date in the initial.
    o += t(77, 178, 'CONTESTAÇÃO', size=12, fill='var(--ink-2)', weight=700)
    o += t(77, 235, 'NOV/2012', size=24, fill='var(--ink)', weight=700, ls='.04em')
    o += t(77, 260, 'compra do aparelho', size=12, fill='var(--ink-2)', ls='.02em')
    o += line(78, 288, 465, 288, tone='muted', w=1)
    o += t(77, 322, 'INICIAL', size=12, fill='var(--ink-2)', weight=700)
    o += t(77, 362, '18/08/2015', size=20, fill='var(--ink)', weight=700, ls='.04em')
    o += t(77, 385, 'ajuizamento', size=12, fill='var(--ink-2)', ls='.02em')
    o += line(77, 410, 471, 410, tone='muted', w=1, dash='3 5')
    o += t(77, 445, 'DADO DE COMPRA LIDO NA DEFESA', size=11, fill='var(--ink-2)', weight=600)
    # Reply items appear on the right leaf as the judge records them.
    o += t(576, 178, 'IMPUGNAÇÃO · ITENS 15–16', size=12, fill='var(--ink-2)', weight=700)
    o += f'<path d="M580 205L580 339" style="stroke:var(--conc);stroke-width:3"/>'
    o += t(603, 226, '15', size=16, fill='var(--conc)', weight=700)
    o += t(645, 226, 'tentativas de solução', size=14, fill='var(--ink)', weight=600, ls='.02em')
    o += t(645, 251, 'o juiz diz que não estavam na inicial', size=11, fill='var(--ink-2)', ls='.01em')
    o += t(603, 303, '16', size=16, fill='var(--conc)', weight=700)
    o += t(645, 303, 'não quer manter o produto', size=14, fill='var(--ink)', weight=600, ls='.02em')
    o += t(645, 328, 'pede a rescisão do contrato', size=11, fill='var(--ink-2)', ls='.01em')
    o += line(576, 365, 998, 365, tone='muted', w=1)
    o += t(576, 410, '15/01/2016', size=20, fill='var(--dif)', weight=700, ls='.04em')
    o += t(576, 435, 'SENTENÇA · DECADÊNCIA', size=12, fill='var(--ink)', weight=700)
    o += t(576, 459, 'resultado registrado', size=11, fill='var(--ink-2)', ls='.02em')
    # Staple and folio marks make the material object legible without text.
    o += f'<path d="M497 101L516 101L516 123L497 123Z" style="fill:var(--paper-2);stroke:var(--ink-2);stroke-width:1"/>'
    o += t(66, 487, 'REGISTRO JUDICIAL', size=11, fill='var(--ink-2)', weight=700)
    return svg('18 32 1042 500', o, cls='fig figkit', ident='pci-a13-docket',
               label='Fólio dos autos 0321861-32.2015.8.24.0023: compra em novembro de 2012, ação em agosto de 2015, itens da impugnação e sentença de janeiro de 2016')


def ruler_panel():
    """Measure the statutory ceiling in thirty equal days, without inventing a calendar date."""
    o = ''
    x0, x1, y = 52, 1005, 264
    o += t(54, 82, 'CPC · ART. 352', size=14, weight=700)
    o += t(1005, 82, 'PRAZO FIXADO PELO JUIZ', size=12, anchor='end', fill='var(--ink-2)', weight=600)
    o += line(x0, y, x1, y, tone='ink', w=2.2)
    # Thirty equal intervals encode a maximum; the final tick is the cap.
    for i in range(31):
        x = x0 + i * (x1 - x0) / 30
        top = y - (26 if i in (0, 5, 10, 15, 20, 25, 30) else 13)
        bottom = y + (26 if i in (0, 5, 10, 15, 20, 25, 30) else 13)
        tone = 'conc' if i == 30 else ('muted' if i in (0, 5, 10, 15, 20, 25) else 'ink')
        o += line(x, top, x, bottom, tone=tone, w=2 if i == 30 else 1.2)
        if i in (0, 5, 10, 15, 20, 25, 30):
            o += t(x, 321, str(i), size=12, anchor='middle', fill='var(--conc)' if i == 30 else 'var(--ink-2)', weight=700)
    # The cap itself is a cut in the physical measure, with room for its limit label.
    xc = x1
    o += f'<path d="M{xc-9} 211L{xc} 198L{xc+9} 211" style="fill:none;stroke:var(--conc);stroke-width:2.2"/>'
    o += t(xc-8, 173, 'TETO', size=11, anchor='end', fill='var(--conc)', weight=700)
    o += t(xc, 388, '30 DIAS', size=18, anchor='end', fill='var(--conc)', weight=700, ls='.04em')
    o += t(54, 440, 'NUNCA SUPERIOR A', size=11, fill='var(--ink-2)', weight=600)
    o += t(1005, 440, 'MÁXIMO, NÃO ESPERA OBRIGATÓRIA', size=11, anchor='end', fill='var(--ink-2)', weight=600)
    # Empty track beyond the cap shows there is no further statutory interval.
    o += line(x1+20, y, 1033, y, tone='muted', w=1, dash='3 6')
    o += f'<path d="M1020 247L1038 281M1038 247L1020 281" style="stroke:var(--muted);stroke-width:1.5"/>'
    return svg('34 56 1010 410', o, cls='fig figkit', ident='pci-a13-ruler',
               label='Régua com trinta intervalos iguais e limite no trigésimo dia, medida do prazo máximo do art. 352')


def variation_panel():
    """Keep the recorded outcome separate from a conditional current-law variation."""
    o = ''
    # Two paper leaves preserve the historical object and mark only a changed fact.
    o += '<path d="M32 74L32 500L522 500L522 72L476 49L292 65L273 72L251 65L75 49Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.8"/>'
    o += '<path d="M556 72L556 500L1048 500L1048 74L1005 49L816 65L797 72L775 65L599 49Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.8"/>'
    o += t(54, 110, 'REGISTRO · 15/01/2016', size=11, fill='var(--ink-2)', weight=700)
    o += t(54, 161, 'NOV/2012', size=20, fill='var(--ink)', weight=700)
    o += t(54, 185, 'compra informada no processo', size=11, fill='var(--ink-2)', ls='.02em')
    o += line(54, 221, 486, 221, tone='muted', w=1)
    o += t(54, 269, 'DECADÊNCIA', size=18, fill='var(--ink)', weight=700, ls='.04em')
    o += t(54, 295, 'resultado que a sentença registra', size=11, fill='var(--ink-2)', ls='.02em')
    o += t(54, 368, 'JUIZADO ESPECIAL CÍVEL', size=11, fill='var(--ink-2)', weight=700)
    o += t(54, 423, 'data e resultado do próprio registro', size=11, fill='var(--ink-2)', ls='.01em')
    o += t(578, 110, 'HIPÓTESE · CPC ATUAL', size=11, fill='var(--conc)', weight=700)
    o += t(578, 161, 'DATA DA COMPRA', size=12, fill='var(--ink-2)', weight=700)
    # A pencil mark denotes a changed fact; the chart makes no finding about the event.
    o += f'<circle cx="607" cy="206" r="13" style="fill:none;stroke:var(--conc);stroke-width:2"/>'
    o += t(638, 212, 'controvertida', size=17, fill='var(--conc)', weight=700, ls='.02em')
    o += line(578, 250, 1016, 250, tone='muted', w=1)
    o += t(578, 291, 'MATERIAL PARA A DECISÃO?', size=12, fill='var(--ink)', weight=700)
    o += t(578, 323, 'AINDA EXIGE PROVA?', size=12, fill='var(--ink)', weight=700)
    o += t(578, 377, 'SEM PROVA NECESSÁRIA', size=11, fill='var(--dif)', weight=700)
    o += t(578, 401, 'julgamento possível', size=11, fill='var(--ink-2)', ls='.02em')
    o += t(824, 377, 'COM PROVA NECESSÁRIA', size=11, fill='var(--conc)', weight=700)
    o += t(824, 401, 'delimitar fato e meios', size=11, fill='var(--ink-2)', ls='.02em')
    o += line(778, 352, 778, 430, tone='muted', w=1, dash='3 4')
    o += t(578, 465, 'ART. 355, I', size=11, fill='var(--dif)', weight=700)
    o += t(1018, 465, 'ART. 357, II', size=11, anchor='end', fill='var(--conc)', weight=700)
    return svg('16 36 1048 468', o, cls='fig figkit', ident='pci-a13-variation',
               label='A sentença histórica de 2016 aparece separada de uma hipótese atual: uma data controvertida só leva à organização da prova se importar para a decisão e ainda exigir instrução')


def install():
    """Replace only Aula 13's three planned drawings in the target page."""
    import inject

    docket = docket_panel().replace('class="fig figkit"', 'class="hero-fork fig figkit"', 1)
    return inject.inject(PAGE, {
        'pci-a13-docket': docket,
        'pci-a13-ruler': ruler_panel(),
        'pci-a13-variation': variation_panel(),
    })


if __name__ == '__main__':
    print(f'{install()} Aula 13 figures installed')
