"""Aula 17: dated precedent and the rebuttable inference in REsp 70.170/SP.

Source: Carpes, *Ônus Dinâmico da Prova*, PDF p. 8 / printed p. 58,
note 189 (the STJ headnote). The case applied CC/1916 art. 943; the
separate course discussion of CPC/2015 art. 373 is not its legal basis.
These pure figure functions do not change a lesson or its generator.
"""

from datetime import date

from figkit import line, svg, t


def hero_balance():
    """Balance whose pans are semantic, keyboard-operable HTML buttons."""
    o = '<g class="a17-beam"><path d="M300 55 L106 105 L494 105"/><path d="M106 105 L80 168 M106 105 L132 168 M494 105 L468 168 M494 105 L520 168"/>'
    o += '<foreignObject x="48" y="164" width="116" height="48"><button xmlns="http://www.w3.org/1999/xhtml" type="button" class="a17-pan" data-side="claimant" aria-pressed="false">Quem pede</button></foreignObject>'
    o += '<foreignObject x="436" y="164" width="116" height="48"><button xmlns="http://www.w3.org/1999/xhtml" type="button" class="a17-pan" data-side="defendant" aria-pressed="false">Quem se defende</button></foreignObject>'
    o += '<g class="a17-doubt"><rect x="250" y="28" width="100" height="38" rx="3" style="fill:var(--paper);stroke:var(--ink-2);stroke-width:1.4"/>'
    o += t(300, 53, 'DÚVIDA', size=12, weight=700, anchor='middle') + '</g></g>'
    o += '<path d="M300 108 L270 218 L330 218 Z"/><path d="M252 222 H348"/>'
    return svg('0 0 600 250', o, cls='fig', ident='pci-a17-hero',
               label='Balança interativa com dois pratos que funcionam como botões e um bloco marcado dúvida.').replace('<svg ', '<svg data-family="figure.balance" ', 1)


def decision_timeline(publication=False):
    """Judgment to publication, with horizontal distance proportional to days."""
    judgment = date(2000, 4, 18)
    publication_date = date(2000, 6, 12)
    days = (publication_date - judgment).days
    x0, x1, y = 54, 546, 145
    o = t(54, 34, 'O TEMPO DO PRECEDENTE', size=15, weight=700)
    o += t(54, 58, 'STJ · 4ª TURMA · REsp 70.170/SP', size=11.5,
           fill='var(--ink-2)', weight=600)
    o += line(x0, y, x1, y, w=2)
    # One short tick per ten elapsed days; endpoints are the source dates.
    for day in range(10, days, 10):
        x = x0 + (x1 - x0) * day / days
        o += line(x, y - 5, x, y + 5, tone='muted', w=1)
    for x, top, bottom in (
        (x0, '18 ABR. 2000', 'JULGAMENTO'),
        (x1, '12 JUN. 2000', 'PUBLICAÇÃO'),
    ):
        anchor = 'start' if x == x0 else 'end'
        tone = 'ink'
        o += line(x, y - 17, x, y + 17, tone=tone, w=2.2)
        o += (f'<circle cx="{x}" cy="{y}" r="5" '
              f'style="fill:var(--paper);stroke:var(--{tone});stroke-width:2"/>')
        o += t(x, 111, top, size=12, anchor=anchor, weight=700)
        o += t(x, 180, bottom, size=11.5, anchor=anchor, fill='var(--ink)', weight=700)
    o += line(x0, 216, x1, 216, tone='dif' if publication else 'muted', w=1.5 if publication else 1, dash='3 5')
    o += t(300, 207, f'{days} DIAS', size=13, anchor='middle', weight=700)
    o += t(54, 251, 'O caso trata de cotas condominiais periódicas.', size=12, weight=600, ls='0')
    o += t(54, 276, 'Aplicou-se o art. 943 do CC/1916.', size=12, ls='0')
    ident = 'pci-a17-precedent-time-2' if publication else 'pci-a17-precedent-time'
    cls = 'fig panel' if publication else 'fig panel on'
    stage = ', com a publicação destacada' if publication else ''
    return svg('35 14 530 279', o, cls=cls, ident=ident,
               label=f'Linha do tempo em escala{stage}: julgamento do REsp 70.170/SP em 18 de abril de 2000, publicação em 12 de junho de 2000, intervalo de 55 dias. O caso das cotas condominiais aplicou o artigo 943 do Código Civil de 1916.').replace('<svg ', '<svg data-family="figure.timeline" ', 1)


def presumption_panel():
    """A later payment supports a backward, rebuttable inference."""
    o = t(38, 37, 'O QUE A QUITAÇÃO POSTERIOR PERMITE INFERIR',
          size=14.5, weight=700)
    o += t(38, 63, 'REsp 70.170/SP · COTAS CONDOMINIAIS',
           size=11.5, fill='var(--ink-2)', weight=600)

    # The left band is an undetermined prior span, not a count of installments.
    o += line(58, 165, 285, 165, tone='ink', w=8)
    o += line(58, 151, 58, 179, tone='ink', w=1.7)
    o += line(285, 151, 285, 179, tone='ink', w=1.7)
    o += t(58, 196, 'COTAS ANTERIORES', size=12, weight=700)
    o += t(58, 215, 'quitação presumida', size=11.5, ls='0')

    # The receipt mark is the demonstrated later payment.
    o += '<circle cx="486" cy="165" r="31" style="fill:var(--paper);stroke:var(--dif);stroke-width:2.2"/>'
    o += '<path d="M472 165l10 10 19-22" style="fill:none;stroke:var(--dif);stroke-width:3;stroke-linecap:round;stroke-linejoin:round"/>'
    o += t(486, 215, 'PAGAMENTO POSTERIOR', size=12, anchor='middle', weight=700)
    o += t(486, 234, 'demonstrado pelo devedor', size=11.5,
           anchor='middle', ls='0')

    # Backward direction matters: the later receipt bears on earlier quotas.
    o += '<path d="M452 143C415 98 323 95 239 126" style="fill:none;stroke:var(--dif);stroke-width:2.4"/>'
    o += '<path d="M239 126l13-1-7-11" style="fill:none;stroke:var(--dif);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round"/>'
    o += t(347, 100, 'PRESUNÇÃO RELATIVA', size=11.5,
           anchor='middle', fill='var(--ink)', weight=700)

    # A separate opposing vector marks the creditor's burden to rebut.
    o += '<path d="M302 311C267 285 236 266 200 239" style="fill:none;stroke:var(--ink);stroke-width:2.2;stroke-dasharray:6 4"/>'
    o += '<path d="M200 239l14 2-7 11" style="fill:none;stroke:var(--ink);stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round"/>'
    o += t(305, 338, 'CREDOR: PROVA PARA AFASTAR A PRESUNÇÃO',
           size=11.5, anchor='middle', weight=700)

    # Two disconnected rails prevent the old case from appearing to apply the
    # current procedural article. The current lesson has its own instrument.
    o += line(38, 385, 275, 385, tone='ink', w=2)
    o += line(325, 385, 562, 385, tone='muted', w=2)
    o += t(38, 408, 'NESTE JULGADO', size=11, fill='var(--ink)', weight=700)
    o += t(38, 428, 'CC/1916 · art. 943', size=12, weight=600)
    o += t(325, 408, 'NA AULA', size=11, fill='var(--ink-2)', weight=700)
    o += t(325, 428, 'CPC/2015 · regra atual', size=12, weight=600)
    return svg('20 15 560 434', o, cls='fig', ident='pci-a17-presumption',
               label='No REsp 70.170/SP, o devedor demonstrou pagamento de cotas posteriores. Pelo artigo 943 do Código Civil de 1916, isso gerou presunção relativa de quitação das anteriores; coube ao credor produzir prova para afastá-la. A regra atual do CPC de 2015 é ensinada separadamente na aula.').replace('<svg ', '<svg data-family="figure.balance" ', 1)


def panels() -> tuple[str, str]:
    return decision_timeline(), presumption_panel()
