"""Aula 08-revelia: a filing form and a staged record of the 2015 case."""
from figkit import line, svg, t


def _family(markup, name):
    return markup.replace("<svg", f'<svg data-family="{name}"', 1)


def filing_form():
    """A reader classifies each function in Dalvo's response; orange marks the limit."""
    o = t(25, 44, 'RESPOSTA DE DALVO', size=15, weight=700)
    o += t(465, 44, 'CPC · ART. 343', size=13, anchor='end', weight=700, fill='var(--ink-2)')
    o += line(25, 56, 465, 56, w=1.2)
    o += t(25, 78, 'MARQUE A FUNÇÃO DE CADA ATO', size=13, weight=700, fill='var(--ink-2)')

    for y, filing, function in (
        (108, 'CONTESTAÇÃO', 'resiste à cobrança de Jesse'),
        (170, 'RECONVENÇÃO', 'formula pretensão própria de Dalvo'),
    ):
        o += f'<rect x="25" y="{y - 17}" width="20" height="20" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.6"/>'
        o += t(58, y, filing, size=15, weight=700)
        o += t(58, y + 23, function, size=14, fill='var(--ink-2)')
        o += line(58, y + 33, 465, y + 33, tone='muted', w=.75)

    o += line(25, 215, 465, 215, w=1.2)
    o += t(25, 239, 'LIMITE · CONEXÃO', size=12, weight=700, fill='var(--conc)').replace('<text ', '<text data-color-role="limit" ', 1)
    o += t(465, 239, 'ação principal ou fundamento da defesa', size=11.5, anchor='end', weight=600, fill='var(--conc)').replace('<text ', '<text data-color-role="limit" ', 1)
    return _family(svg('18 24 464 240', o, cls='fig hero-form', ident='pci-a08r-filing-form',
                       label='Formulário de resposta de Dalvo: a contestação resiste à cobrança de Jesse; a reconvenção formula pedido próprio; a conexão com a ação ou a defesa é o limite'),
                    'figure.form')


def _timeline_inner(ordinal=False, supplement=False, measure_interval=False):
    """The same scaled dates in each stage; first-week filing stays off the date axis."""
    o = t(50, 88, 'AVALIAÇÃO 2 · 2015 · REGISTRO DO CASO', size=18, weight=700)
    o += line(50, 102, 550, 102, w=1.2)

    if ordinal:
        o += t(50, 150, 'CONTESTAÇÃO · 1ª SEMANA DO PRAZO', size=18, weight=700)
        o += line(50, 165, 550, 165, tone='muted', w=.9, dash='3 4')

    x0, x1, y = 72, 528, 250
    o += line(x0, y, x1, y, w=1.8)
    step = (x1 - x0) / 12
    for day in range(13):
        x = x0 + day * step
        major = day in (0, 12)
        height = 16 if major else 8
        o += line(x, y - height / 2, x, y + height / 2, w=1.2 if major else .8)
    o += f'<circle cx="{x0}" cy="{y}" r="7" style="fill:var(--paper);stroke:var(--ink);stroke-width:2"/>'
    o += t(x0, 218, '01/04/2015', size=18, weight=700)
    o += t(x1, 218, '13/04/2015', size=18, weight=700, anchor='end')
    if measure_interval:
        # The dates sit 12 equal daily intervals apart; this measures elapsed time without
        # treating the first-week filing as a dated event or implying a deadline.
        measure_y = 185
        o += line(x0, measure_y, x1, measure_y, tone='conc', w=1.8)
        o += line(x0, measure_y - 5, x0, measure_y + 5, tone='conc', w=1.8)
        o += line(x1, measure_y - 5, x1, measure_y + 5, tone='conc', w=1.8)
        o += t((x0 + x1) / 2, measure_y - 8, 'INTERVALO · 12 DIAS', size=13, weight=700,
               anchor='middle', fill='var(--conc)').replace('<text ', '<text data-color-role="limit" ', 1)
    o += t(x0, 294, 'Audiência preliminar', size=18, weight=700)
    o += t(x0, 316, 'todas as partes · sem acordo', size=18, fill='var(--ink-2)')

    if supplement:
        o += f'<circle cx="{x1}" cy="{y}" r="7" style="fill:var(--paper);stroke:var(--ink);stroke-width:2"/>'
        o += t(x1, 340, 'Dalvo percebe os fatos', size=18, weight=700, anchor='end')
        o += t(x1, 362, 'complementa a defesa de pronto', size=18, fill='var(--ink-2)', anchor='end')
    return o


def case_timeline_panels():
    """Three views of the sourced chronology, with no invented date for the first-week filing."""
    panels = (
        ('pci-a08r-time-hearing', _timeline_inner(measure_interval=True), True,
         'Instrumento de medida: 12 dias decorridos entre 1º e 13 de abril de 2015; a faixa mede o intervalo sem datar a contestação da primeira semana.'),
        ('pci-a08r-time-contestation', _timeline_inner(ordinal=True), False,
         'O registro acrescenta a contestação de Dalvo na primeira semana, em faixa ordinal separada do eixo de dias.'),
        ('pci-a08r-time-supplement', _timeline_inner(ordinal=True, supplement=True), False,
         'O registro inclui a descoberta em 13 de abril e a complementação imediata da defesa de Dalvo.'),
    )
    result = []
    for ident, inner, on, label in panels:
        classes = 'fig panel on' if on else 'fig panel'
        result.append(_family(svg('30 55 540 340', inner, cls=classes, ident=ident, label=label),
                              'figure.timeline'))
    return tuple(result)


def figures():
    return filing_form(), case_timeline_panels()


def specimen_entry():
    form, panels = figures()
    timeline = panels[-1].replace('class="fig panel"', 'class="fig"', 1)
    return (
        '<section class="ref" id="specimen-pci-a08r"><header><span class="g">Instrumentos · resposta e registro</span>'
        '<span class="v">verbos · classificar / datar</span></header>'
        '<h2>Processo · Aula 08-revelia</h2>'
        '<p>O formulário separa os objetos dos dois atos; a linha do tempo marca as datas do caso sem converter a primeira semana em dia específico.</p>'
        '<p class="r">componentes · pci-a08r-filing-form / pci-a08r-time-hearing / pci-a08r-time-contestation / pci-a08r-time-supplement</p>'
        f'<div class="wide"><div class="s">{form}</div><div class="s" style="margin-top:16px">{timeline}</div></div></section>'
    )


if __name__ == '__main__':
    form, panels = figures()
    print(form)
    print('\n'.join(panels))
