"""Aula 10: a measured case docket and an annotated cut of CPC art. 356.

The docket contains only dates and disposition in the Florianópolis record. The statute
sheet states a separate legal threshold; it makes no claim about that record.
"""
from figkit import Document, line, svg, t


def hero():
    """Calendar precision: the purchase occupies a month; the two court acts have days."""
    x0, x1, y = 48, 552, 158
    # The purchase occupies all of November; the dated filings use their day within the month.
    total_months = 38 + 14 / 31
    action = x0 + (33 + 17 / 31) / total_months * (x1 - x0)
    o = t(28, 38, 'AUTOS · JUIZADO ESPECIAL CÍVEL · FLORIANÓPOLIS',
          size=16, fill='var(--ink-2)', weight=700)
    o += line(28, 55, 572, 55, w=1.3)
    o += line(x0, y, x1, y, w=2.3)
    for month, name in [(2, '2013'), (14, '2014'), (26, '2015')]:
        x = x0 + month / total_months * (x1 - x0)
        o += line(x, y - 6, x, y + 6, tone='muted', w=1.2)
        o += t(x, 187, name, size=15, fill='var(--ink-2)', anchor='middle')
    # The purchase band is deliberately wider than a dated tick.
    o += f'<rect x="{x0:g}" y="{y - 16:g}" width="{(x1 - x0) / total_months:g}" height="32" style="fill:var(--dif-wash);stroke:var(--dif);stroke-width:1.4"/>'
    o += t(28, 101, 'COMPRA', size=17, fill='var(--dif)', weight=700)
    o += t(28, 128, 'NOV. 2012', size=19, fill='var(--ink)', weight=700)
    o += line(x0, 137, x0, y - 17, tone='dif', w=1.3)
    o += f'<circle cx="{action:g}" cy="{y:g}" r="6" style="fill:var(--dif)"/>'
    o += line(action, 115, action, y - 9, tone='dif', w=1.3)
    o += t(466, 100, 'AÇÃO', size=17, fill='var(--dif)', anchor='end', weight=700)
    o += t(466, 127, '18 AGO. 2015', size=19, anchor='end', weight=700)
    o += f'<circle cx="{x1:g}" cy="{y:g}" r="7" style="fill:var(--conc)"/>'
    o += line(x1, y + 10, x1, 229, tone='conc', w=1.4)
    o += t(572, 260, 'DECISÃO · 15 JAN. 2016', size=19,
           fill='var(--conc)', anchor='end', weight=700)
    o += line(28, 282, 572, 282, w=1)
    o += t(28, 315, 'DECADÊNCIA RECONHECIDA', size=20, fill='var(--conc)', weight=700)
    return svg('12 13 576 319', o, cls='fig on', ident='pci-a10-docket',
               label='Autos de Florianópolis: compra em novembro de 2012, ação em 18 de agosto de 2015 e decisão em 15 de janeiro de 2016 que reconhece decadência')


def statute_panel():
    """A paper selection sheet: whole requests or a part, with either readiness mark."""
    d = Document('pci-a10-art356', 18, 18, 564,
                 [('title', 'Recorte do mérito', 'head')], foot=325)
    o = d.paper()
    o += t(42, 55, 'RECORTE DO MÉRITO', size=19,
           fill='var(--ink)', weight=700)
    o += line(42, 72, 558, 72, w=1.6)
    o += t(42, 107, 'ALCANCE POSSÍVEL', size=17,
           fill='var(--ink-2)', weight=700)
    # Paper strips are complete requests. Their count, rather than a sentence in a cell,
    # shows that a decision can cover one request or several.
    o += t(42, 141, 'UM PEDIDO', size=18, fill='var(--dif)', weight=700)
    o += f'<rect x="224" y="125" width="334" height="20" style="fill:var(--dif-wash);stroke:var(--dif);stroke-width:1.5"/>'
    o += t(42, 190, 'VÁRIOS PEDIDOS', size=18, fill='var(--dif)', weight=700)
    for y in (169, 184):
        o += f'<rect x="224" y="{y}" width="334" height="12" style="fill:var(--dif-wash);stroke:var(--dif);stroke-width:1.3"/>'
    # The uninked remainder remains on the same sheet; the jagged edge makes the
    # selectable parcel visible without assigning a real case or a numeric proportion.
    o += t(42, 256, 'PARTE DE UM PEDIDO', size=18, fill='var(--conc)', weight=700)
    o += f'<rect x="42" y="271" width="516" height="24" style="fill:var(--paper-2);stroke:var(--ink-2);stroke-width:1.2"/>'
    o += f'<path d="M42 271H247l-5 5 5 5-5 5 5 5-5 4H42Z" style="fill:var(--conc-wash);stroke:var(--conc);stroke-width:1.7;stroke-linejoin:round"/>'
    o += line(42, 312, 558, 312, tone='muted', w=1)
    o += t(42, 342, 'PARA DECIDIR O TRECHO SEPARADO', size=17,
           fill='var(--ink-2)', weight=700)
    # Unselected seals name alternative conditions; no case finding is asserted.
    for x in (62, 335):
        o += f'<circle cx="{x}" cy="375" r="11" style="fill:var(--paper);stroke:var(--ink);stroke-width:2"/>'
        o += f'<circle cx="{x}" cy="375" r="3" style="fill:var(--ink)"/>'
    o += t(84, 381, 'SEM DISPUTA', size=18, weight=700)
    o += t(273, 381, 'OU', size=17, anchor='middle', fill='var(--ink-2)', weight=700)
    o += t(357, 381, 'PRONTO A JULGAR', size=18, weight=700)
    return svg('8 8 584 410', o, cls='fig on', ident='pci-a10-art356',
               label='Folha de delimitação do mérito: a decisão pode abranger um pedido, vários pedidos ou parte de um pedido, desde que o trecho esteja sem disputa ou pronto para decisão imediata')


def decision_panel(variation=False, specimen=False):
    """The same Florianópolis file in its recorded state and one timely-claim variation.

    This is a document instrument: the reader reads the allegation and evidence state, then
    identifies the route the record supports. It changes no fact except claim timeliness.
    """
    ident = 'pci-a10-decision-variation' if variation else 'pci-a10-decision-record'
    title = ('Variação única · ajuizamento tempestivo' if variation
             else 'Registro histórico · 15 jan. 2016')
    route = ('Art. 357 · instruir o fato material' if variation
             else 'Decadência reconhecida · ação extinta')
    lines = [
        ('title', title, 'title'),
        ('clause', ('AUTOS', '0321861-32.2015.8.24.0023 · 2º JEC de Florianópolis'), 'autos'),
        ('clause', ('TEMPO', 'compra · nov. 2012; ajuizamento · ' +
                    ('tempestivo' if variation else '18 ago. 2015')), 'tempo'),
        ('clause', ('PEÇAS', 'inicial · contestação · impugnação'), 'pecas'),
        ('clause', ('ITEM 15', 'tentativas repetidas de solução amigável'), 'item15'),
        ('clause', ('PROVA', 'alegação na impugnação; juiz pergunta onde está a prova'), 'prova'),
        ('clause', ('ITEM 16', 'pedido de rescisão contratual'), 'item16'),
        ('clause', ('SAÍDA', route if variation else
                    'comparação atual · decadência: arts. 354 e 487, II'), 'route'),
    ]
    doc = Document(ident, 26, 20, 548, lines, lead=23, indent=82, foot=8,
                   font_size=15, meta_size=13.5, label_size=12)
    o = doc.paper()
    if variation:
        o += doc.highlight(['tempo'], tone='conc')
    o += doc.highlight(['route'], tone='dif')
    o += ''.join(doc.parts)
    cls = 'fig on' if specimen else 'panel fig'
    label = ('Variação única: ajuizamento tempestivo; o juiz pergunta pela prova da alegação do item 15.'
             if variation else
             'Registro histórico: compra, ajuizamento, contestação, impugnação e decadência reconhecida.')
    return svg('12 12 576 295', o, cls=cls, ident=ident, label=label)


def decision_panels(specimen=False):
    return decision_panel(False, specimen), decision_panel(True, specimen)


def panels():
    return hero(), statute_panel()
