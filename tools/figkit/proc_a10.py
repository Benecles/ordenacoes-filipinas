"""Aula 10 figures: Florianópolis docket and decision-form route selector."""
from figkit import Document, line, svg, t
import processo_threads


def hero():
    """A case-cover form assembled from the shared, source-tagged docket."""
    thread = processo_threads.DATA['threads']['florianopolis']
    events = thread['events']
    o = '<path d="M20 14H995L1018 37V215H20Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
    o += '<path d="M995 14V37H1018" style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1"/>'
    o += t(42, 46, thread['title'], size=19, fill='var(--ink)', weight=700)
    o += t(42, 69, thread['case_label'], size=13, fill='var(--ink-2)', weight=600)
    o += line(42, 82, 990, 82, w=1.2)
    fields = [
        ('COMPRA', events[0]['when'], 42, 'var(--ink)'),
        ('AÇÃO', events[1]['when'], 350, 'var(--ink)'),
        ('ITEM 15/16', 'impugnação · alegação e pedido', 640, 'var(--ink)'),
        ('RESULTADO', events[4]['heading'], 42, 'var(--dif)'),
    ]
    for label, value, x, color in fields:
        y = 112 if label != 'RESULTADO' else 174
        o += t(x, y, label, size=11.5, fill='var(--ink-2)', weight=700)
        o += t(x, y+21, value, size=14.5, fill=color, weight=700 if label == 'RESULTADO' else 500)
    o += t(990, 196, 'CPC/2015 · COMPARAÇÃO', size=12, fill='var(--ink)',
           anchor='end', weight=700)
    return svg('12 10 1014 215', o, cls='fig', ident='pci-a10-case-cover',
               label='Capa dos autos históricos de Florianópolis: compra, ajuizamento, item 15 e 16, e sentença que reconhece decadência; o CPC/2015 aparece como comparação separada').replace(
                   ' viewBox=', ' data-family="figure.form" viewBox=', 1)


def timeline_panel(specimen=False):
    """A vertical timeline growing from the shared position-13 record."""
    thread = processo_threads.DATA['threads']['florianopolis']
    events = [event for event in thread['events'] if event['from'] <= 15]
    steps = [step for step in thread['steps'] if step['position'] <= 15]
    o = t(34, 40, thread['title'], size=17, fill='var(--ink)', weight=700)
    o += t(34, 62, f"{thread['case_label']} · POSIÇÃO 15", size=11, fill='var(--ink-2)', weight=600)
    o += line(34, 74, 550, 74, w=1.2)
    o += line(51, 108, 51, 420, w=1.6)
    y = 112
    for index, event in enumerate(events):
        tone = 'var(--dif)' if event['heading'].startswith('Sentença') else 'var(--ink)'
        o += f'<circle cx="51" cy="{y-4}" r="5" style="fill:var(--paper);stroke:{tone};stroke-width:1.8"/>'
        o += t(70, y, event['heading'], size=13, fill=tone, weight=700)
        o += t(550, y, event['when'], size=10.5, fill='var(--ink-2)', anchor='end', weight=700)
        detail_rows = _wrap(event['detail'], 62)
        for row, detail in enumerate(detail_rows):
            o += t(70, y+18+row*13, detail, size=10.5, fill='var(--ink-2)')
        y += 62 + max(0, len(detail_rows)-1)*13
    divider = y - 5
    o += line(34, divider, 550, divider, tone='muted', w=1)
    o += t(34, divider+21, 'CAMADA ANALÍTICA · POSIÇÃO 13 → 15', size=11,
           fill='var(--ink-2)', weight=700)
    step_y = divider + 47
    for step in steps:
        color = 'var(--ink)'
        status = 'HIPÓTESE ·' if step['status'] == 'hypothesis' else 'REGISTRO ·'
        o += line(38, step_y-3, 56, step_y-3, tone='ink', w=2.2)
        o += t(68, step_y, status + ' ' + step['label'], size=11, fill=color, weight=700)
        detail = ('Peças, itens 15–16 e resultado por decadência.' if step['position'] == 13
                  else 'Comparação pelo CPC atual; a decisão de 2016 permanece histórica.')
        detail_rows = _wrap(detail, 62)
        for row, detail in enumerate(detail_rows):
            o += t(68, step_y+16+row*13, detail, size=10, fill='var(--ink-2)')
        step_y += 52 + max(0, len(detail_rows)-1)*13
    cls = 'fig on' if specimen else 'panel fig'
    drawing = svg('8 8 568 622', o, cls=cls, ident='pci-a10-docket',
                  label='Linha do tempo dos autos de Florianópolis, desde o registro da posição 13 até o resultado histórico e a comparação hipotética da posição 15')
    return drawing.replace(' viewBox=', ' data-family="figure.timeline" viewBox=', 1)


def _wrap(value, width):
    rows, row = [], []
    for word in value.split():
        if row and len(' '.join(row + [word])) > width:
            rows.append(' '.join(row))
            row = [word]
        else:
            row.append(word)
    if row:
        rows.append(' '.join(row))
    return rows or ['']


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
    """Decision form: read-only record fields feed five route outputs.

    The two states are the recorded decadence disposition and the CEO-approved, single
    timely-claim variation. Route cards are outputs, never controls.
    """
    ident = 'pci-a10-decision-variation' if variation else 'pci-a10-decision-record'
    title = ('Variação única · ajuizamento tempestivo' if variation
             else 'Registro histórico · 15 jan. 2016')
    o = '<path d="M18 12H558L582 36V660H18Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.6"/>'
    o += '<path d="M558 12V36H582" style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1"/>'
    o += t(36, 43, title.upper(), size=17, fill='var(--ink)', weight=700)
    o += line(36, 57, 564, 57, w=1.3)
    fields = [
        ('AUTOS', '0321861-32.2015.8.24.0023 · 2º JEC de Florianópolis'),
        ('TEMPO', 'compra · nov. 2012; ação · ' + ('tempestiva' if variation else '18 ago. 2015')),
        ('PEÇAS', 'inicial · contestação · impugnação'),
        ('ITEM 15', 'tentativas repetidas; juiz pergunta pela prova'),
        ('ITEM 16', 'pedido de rescisão contratual'),
    ]
    y = 82
    for label, value in fields:
        if variation and label == 'TEMPO':
            o += '<rect x="32" y="%s" width="536" height="27" style="fill:var(--paper-2);stroke:var(--ink-2);stroke-width:1"/>' % (y-19)
        o += t(38, y, label, size=12, fill='var(--ink-2)', weight=700)
        size = 11.5 if len(value) > 45 else 13
        o += t(116, y, value, size=size, fill='var(--ink)', ls='.015em')
        y += 29
    o += t(36, 232, 'SAÍDAS POSSÍVEIS · ARTIGOS 354–357', size=13,
           fill='var(--ink-2)', weight=700)
    o += line(36, 241, 564, 241, w=1)
    routes = [
        ('354 · sem mérito', 'Obstáculo processual impede examinar o pedido.'),
        ('354 · com mérito', 'Decadência/prescrição (art. 487, II) ou autocomposição (III).'),
        ('355 · pedido inteiro', 'I: prova dispensável. II: revelia + art. 344; sem exceção do art. 345, sem pedido do art. 349.'),
        ('356 · parcela do mérito', 'Pedido ou parte incontroversa ou pronta para julgamento imediato.'),
        ('357 · instrução', 'Fato material controvertido ainda depende de prova.'),
    ]
    selected = 1 if not variation else 4
    y = 258
    for i, (label, value) in enumerate(routes):
        if i == selected:
            o += f'<rect x="32" y="{y-17}" width="536" height="62" style="fill:var(--paper);stroke:var(--dif);stroke-width:1.5"/>'
        else:
            o += f'<rect x="32" y="{y-17}" width="536" height="62" style="fill:var(--paper-2);stroke:var(--grid-major);stroke-width:1"/>'
        color = 'var(--ink)'
        o += t(42, y, label.upper(), size=13, fill=color, weight=700)
        # Short two-line route summaries keep the text legible at the page's stage width.
        words = value.split()
        first, second = [], []
        for word in words:
            target = first if len(' '.join(first + [word])) <= 62 else second
            target.append(word)
        o += t(42, y+19, ' '.join(first), size=12.5, fill='var(--ink)')
        if second:
            o += t(42, y+35, ' '.join(second), size=12.5, fill='var(--ink)')
        y += 69
    o += t(36, 633, ('LIMITE · só muda a tempestividade.'
                     if variation else 'LIMITE · o CPC/2015 não foi fundamento do juiz em 2016.'),
           size=12.5, fill='var(--conc)', weight=700)
    cls = 'fig on' if specimen else 'panel fig'
    label = ('Variação única: ajuizamento tempestivo; demais fatos iguais; a necessidade da prova do item 15 conduz à rota do artigo 357.'
             if variation else
             'Registro histórico: fatos dos autos e decadência reconhecida; cinco saídas possíveis, com a comparação pelo artigo 354 selecionada.')
    drawing = svg('8 8 584 664', o, cls=cls, ident=ident, label=label)
    return drawing.replace(' viewBox=', ' data-family="figure.form" viewBox=', 1)


def decision_panels(specimen=False):
    return decision_panel(False, specimen), decision_panel(True, specimen)


def panels():
    return hero(), statute_panel()
