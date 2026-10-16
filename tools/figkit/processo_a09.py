"""Aula 09 instruments: the 2018 record, art. 278 folio, and STJ docket."""

from html import escape

from figkit import line, svg, t


def _t(x, y, value, **kwargs):
    return t(x, y, escape(value, quote=False), **kwargs)


def _family(markup, family):
    return markup.replace("<svg", f'<svg data-family="{family}"', 1)


def _initial_diligence_panel():
    o = _t(34, 52, 'AUTOS · 2018/2 · P1 · QUESTÃO 4', size=14, weight=700)
    o += line(34, 69, 566, 69, w=1.3)
    o += line(68, 125, 68, 324, tone='muted', w=1.4)
    o += line(60, 153, 76, 153, w=2.6)
    o += _t(98, 157, 'PRIMEIRA DILIGÊNCIA', size=13, weight=700)
    o += _t(98, 181, 'Florinda não é localizada.', size=12.5, fill='var(--ink-2)')
    o += line(60, 259, 76, 259, tone='conc', w=2.6)
    o += _t(98, 263, 'HORA CERTA', size=13, fill='var(--conc)', weight=700)
    o += _t(98, 287, 'O oficial marca retorno para o dia seguinte.', size=12.5,
           fill='var(--ink-2)')
    return o


def _delivery_panel():
    o = _t(34, 52, 'AUTOS · 2018/2 · P1 · QUESTÃO 4', size=14, weight=700)
    o += line(34, 69, 566, 69, w=1.3)
    o += _t(34, 112, 'DIA SEGUINTE', size=13, fill='var(--conc)', weight=700)
    o += line(68, 132, 68, 322, tone='muted', w=1.4)
    o += line(60, 164, 76, 164, tone='dif', w=2.6)
    o += _t(98, 168, 'MANDADO DE HORA CERTA', size=13, weight=700)
    o += _t(98, 192, 'Entregue à vizinha Valquíria.', size=12.5, fill='var(--ink-2)')
    o += line(60, 260, 76, 260, tone='conc', w=2.6)
    o += _t(98, 264, 'RUMOR NO ENUNCIADO', size=13, fill='var(--conc)', weight=700)
    o += _t(98, 288, 'Valquíria espalha a notícia.', size=12.5, fill='var(--ink-2)')
    return o


def _date_pair_panel():
    o = _t(34, 52, 'AUTOS · 2018/2 · P1 · QUESTÃO 4', size=14, weight=700)
    o += line(34, 69, 566, 69, w=1.3)
    o += _t(34, 112, 'JUNTADA = COMPARECIMENTO DA ADVOGADA', size=11.5,
           fill='var(--ink-2)', weight=700)
    o += line(68, 135, 68, 322, tone='muted', w=1.4)
    o += line(60, 183, 76, 183, tone='dif', w=2.6)
    o += _t(98, 187, 'V1 · 5 SET.', size=14, fill='var(--dif)', weight=700)
    o += _t(98, 211, 'mandado juntado e comparecimento no mesmo dia', size=11.5,
           fill='var(--ink-2)')
    o += line(60, 276, 76, 276, tone='dif', w=2.6)
    o += _t(98, 280, 'V2 · 6 SET.', size=14, fill='var(--dif)', weight=700)
    o += _t(98, 304, 'mandado juntado e comparecimento no mesmo dia', size=11.5,
           fill='var(--ink-2)')
    return o


def case_record_panels():
    """Follow the Q4 record, then place each version's same-day date separately."""
    panels = (
        ('pci-a09-record-initial', _initial_diligence_panel(), True,
         'Questão 4: primeira diligência não localiza Florinda; o oficial marca hora certa para o dia seguinte.'),
        ('pci-a09-record-delivery', _delivery_panel(), False,
         'No dia seguinte, Valquíria recebe o mandado de hora certa e espalha a notícia narrada no enunciado.'),
        ('pci-a09-record-dates', _date_pair_panel(), False,
         'Questão 4: comparecimento da advogada na data da juntada, em V1 no dia 5 e em V2 no dia 6.'),
    )
    result = []
    for ident, inner, on, label in panels:
        classes = 'fig panel on' if on else 'fig panel'
        result.append(_family(svg('18 25 564 390', inner, cls=classes, ident=ident,
                                  label=escape(label, quote=True)), 'figure.autos'))
    return tuple(result)


def objection_folio():
    o = _t(32, 48, 'FOLHA DE LEITURA · CPC · ART. 278', size=14, weight=700)
    o += line(32, 65, 568, 65, w=1.3)
    o += _t(32, 92, 'LOCALIZE O MOMENTO DA ARGUIÇÃO NA REGRA', size=11.5,
           fill='var(--ink-2)', weight=700)
    rows = (
        (144, 'PONTO DE PARTIDA', 'há um ato com vício a ser arguido', 'ink'),
        (235, 'REGRA DO CAPUT', 'na primeira oportunidade em que a parte falar nos autos', 'dif'),
        (326, 'CONSEQUÊNCIA', 'perde-se a ocasião se a parte deixa de alegar', 'conc'),
    )
    for y, head, detail, tone in rows:
        o += _t(42, y, head, size=13, fill=f'var(--{tone})', weight=700)
        o += _t(42, y + 24, detail, size=11.5, fill='var(--ink-2)')
        o += line(42, y + 39, 558, y + 39, tone=tone if tone != 'ink' else 'muted', w=1.4)
    o += _t(42, 398, 'PARÁGRAFO ÚNICO · OFÍCIO / LEGÍTIMO IMPEDIMENTO', size=10.5,
           fill='var(--ink-2)', weight=700)
    return _family(svg('18 25 564 415', o, cls='fig', ident='pci-a09-objection-folio',
                       label='Folha de leitura do art. 278: regra da primeira oportunidade e exceções do parágrafo único'),
                    'figure.instrument')


def stj_record():
    o = _t(32, 48, 'STJ · AgInt no REsp 2.075.558/SP', size=14, weight=700)
    o += line(32, 65, 568, 65, w=1.3)
    entries = (
        (119, 'FLS. 479 / 499', 'marco apontado na origem / primeiro laudo descrito pelo STJ', 'ink'),
        (205, 'FLS. 1083–1084', 'PGJ ouvida no segundo grau; sem prejuízo concreto indicado', 'ink'),
        (291, 'FLS. 1092–1098', 'origem alcança laudo e sentença; preserva manifestações das partes', 'conc'),
        (377, 'RESULTADO NO STJ', 'acórdão de origem anulado; novo julgamento, sem prejuízo presumido', 'dif'),
    )
    for y, head, detail, tone in entries:
        o += _t(42, y, head, size=12.5, fill=f'var(--{tone})', weight=700)
        o += _t(42, y + 21, detail, size=11.5, fill='var(--ink-2)')
        if y < 377:
            o += line(42, y + 39, 558, y + 39, tone='muted', w=.75)
    return _family(svg('18 25 564 415', o, cls='fig', ident='pci-a09-stj-record',
                       label='Registro do AgInt no REsp 2.075.558/SP: primeiro laudo, manifestação da PGJ, alcance da ordem de origem e resultado no STJ'),
                    'figure.autos')


def figures():
    return case_record_panels(), objection_folio(), stj_record()


def specimen_entry():
    cases, folio, record = figures()
    case = cases[0].replace('class="fig panel on"', 'class="fig"', 1)
    return (
        '<section class="ref" id="specimen-pci-a09"><header><span class="g">Autos · citação / nulidade / alcance</span>'
        '<span class="v">verbos · localizar / ordenar / delimitar</span></header>'
        '<h2>Processo · Aula 09 · nulidades</h2>'
        '<p>O registro de Florinda mantém as datas de cada versão; a folha do art. 278 localiza a primeira oportunidade; o processo do STJ mostra o alcance pedido e a decisão que o examinou.</p>'
        f'<div class="wide"><div class="s">{case}</div><div class="s">{folio}</div><div class="s">{record}</div></div></section>'
    )


if __name__ == '__main__':
    case, folio, record = figures()
    print('\n'.join((*case, folio, record)))
