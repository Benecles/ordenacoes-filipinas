"""Aula 08-revelia: one filing form and the sourced 2015 case timeline."""
from figkit import line, svg, t


def filing_form():
    """A reader marks both filing functions; orange marks the connection limit."""
    o = t(24, 39, 'FORMULÁRIO · RESPOSTA DE DALVO', size=14, weight=700)
    o += t(500, 39, 'CPC · ART. 343', size=10.5, anchor='end', weight=700, fill='var(--ink-2)')
    o += line(24, 52, 500, 52, w=1.25)
    o += t(24, 80, 'MARQUE AS FUNÇÕES PRESENTES', size=11.5, weight=700)

    # The reader can mark both independent acts on the same response form.
    for y, filing, target in (
        (127, 'contestação', 'pedido de Jesse'),
        (211, 'reconvenção', 'pedido próprio de Dalvo'),
    ):
        o += f'<rect x="30" y="{y - 15}" width="28" height="28" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.7"/>'
        o += t(76, y + 4, filing, size=13, weight=700)
        o += t(220, y + 4, 'resiste a' if filing == 'contestação' else 'formula', size=11, fill='var(--ink-2)')
        o += t(305, y + 4, target, size=12, weight=600)
        o += line(76, y + 23, 500, y + 23, tone='muted', w=.8)

    o += line(24, 278, 500, 278, tone='conc', w=2.3)
    o += t(24, 301, 'LIMITE · CONEXÃO', size=11, weight=700, fill='var(--conc)')
    o += t(24, 322, 'ação principal OU fundamento da defesa', size=12, weight=600, fill='var(--conc)')
    return svg('18 20 500 316', o, cls='fig', ident='pci-a08r-filing-form',
               label='Formulário com duas opções independentes: contestação que resiste à cobrança de Jesse e reconvenção que leva pedido próprio de Dalvo; a conexão com a ação ou com a defesa aparece como limite')


def case_timeline():
    """A scaled 1–13 April axis; only the two sourced dates are pinned."""
    o = t(24, 38, 'AVALIAÇÃO 2 · 2015 · REGISTRO', size=13, weight=700)
    o += line(24, 52, 500, 52, w=1.2)

    # Ordinal fact sits in a separate band; no position on the scale implies a date.
    o += t(24, 83, 'Contestação · 1ª semana do prazo', size=11.5, weight=700)
    o += line(24, 104, 500, 104, tone='muted', w=.9)

    x0, x1, y = 60, 475, 176
    o += line(x0, y, x1, y, w=1.8)
    step = (x1 - x0) / 12
    for day in range(13):
        x = x0 + day * step
        height = 15 if day in (0, 12) else 8
        o += line(x, y - height / 2, x, y + height / 2, w=1.1 if day in (0, 12) else .8)
    for x in (x0, x1):
        o += f'<circle cx="{x}" cy="{y}" r="7" style="fill:var(--paper);stroke:var(--ink);stroke-width:2"/>'
    o += t(x0, 145, '01/04/2015', size=12, weight=700)
    o += t(x1, 145, '13/04/2015', size=12, weight=700, anchor='end')
    o += t(x0, 216, 'Audiência preliminar', size=11.5, weight=700)
    o += t(x0, 235, 'todos comparecem;', size=10.5, fill='var(--ink-2)')
    o += t(x0, 250, 'sem acordo', size=10.5, fill='var(--ink-2)')
    o += t(x1, 216, 'Dalvo percebe os fatos', size=11.5, weight=700, anchor='end')
    o += t(x1, 235, 'complementa a defesa', size=10.5, fill='var(--ink-2)', anchor='end')
    o += t(x1, 250, 'de pronto', size=10.5, fill='var(--ink-2)', anchor='end')
    return svg('18 20 500 260', o, cls='fig', ident='pci-a08r-case-timeline',
               label='Linha do tempo em escala da audiência de 1 de abril de 2015 à ciência e complementação da defesa de Dalvo em 13 de abril; a contestação é indicada apenas como ocorrida na primeira semana do prazo')


def figures():
    return filing_form(), case_timeline()


def specimen_entry():
    a, b = figures()
    return (
        '<section class="ref" id="specimen-pci-a08r"><header><span class="g">Instrumentos · resposta e registro</span>'
        '<span class="v">verbos · classificar / datar</span></header>'
        '<h2>Processo · Aula 08-revelia</h2>'
        '<p>O formulário separa as funções da contestação e da reconvenção; a escala temporal prende apenas os dois dias indicados no caso de Jesse.</p>'
        '<p class="r">novos componentes · pci-a08r-filing-form / pci-a08r-case-timeline</p>'
        f'<div class="wide"><div class="s">{a}</div><div class="s" style="margin-top:16px">{b}</div></div></section>'
    )


if __name__ == '__main__':
    print('\n'.join(figures()))
