"""Aula 08: generate the deadline docket and contestation outline with figkit."""
from pathlib import Path
import re

from figkit import WARN, line, t, svg


def _family(markup, name):
    return markup.replace('<svg', f'<svg data-family="{name}"', 1)


def docket_hero():
    """The scaled dates on the 2017 exam docket, including each defendant's deadline."""
    o = t(28, 34, 'PROVA HALLOWEEN · 2017/2 · QUESTÃO 1', size=14, weight=700)
    o += line(28, 50, 572, 50, w=1)
    o += t(28, 82, 'ARIOVALDO · AÇÃO DISTRIBUÍDA EM 01/02/2018', size=12, weight=700)

    x0, x1, y = 46, 554, 151
    o += line(x0, y, x1, y, w=1.8)
    # The real exam dates span 71 calendar days from filing through the UFRGS deadline.
    dates = [
        (0, '01/02', 'AÇÃO', 'ink'),
        (28, '01/03', 'AUDIÊNCIA', 'ink'),
        (49, '22/03', 'ODRAUDE', 'dif'),
        (57, '30/03', 'FERIADO', 'conc'),
        (71, '13/04', 'UFRGS', 'dif'),
    ]
    for index, (day, date, label, tone) in enumerate(dates):
        x = x0 + day * (x1 - x0) / 71
        o += line(x, y - 8, x, y + 8, tone=tone, w=1.6)
        o += f'<circle cx="{x:.2f}" cy="{y}" r="5.5" style="fill:var(--paper);stroke:var(--{tone});stroke-width:2"/>'
        anchor = 'start' if index == 0 else ('end' if index == len(dates) - 1 else 'middle')
        label_anchor = {2: 'end', 3: 'start'}.get(index, anchor)
        o += t(x, y - 19, date, size=14, weight=700, anchor=anchor,
               fill='var(--conc)' if tone == 'conc' else 'var(--ink)')
        o += t(x, y + 27, label, size=11, weight=700 if tone == 'dif' else 600,
               anchor=label_anchor, fill='var(--conc)' if tone == 'conc' else 'var(--ink-2)')
    o += t(28, 222, 'ODRAUDE · 15 DIAS ÚTEIS', size=11, weight=700, fill='var(--dif)')
    o += t(572, 250, 'UFRGS · 30 DIAS ÚTEIS · ART. 183', size=11, weight=700,
           anchor='end', fill='var(--dif)')
    return _family(svg('0 0 600 270', o, cls='hero-fork fig', ident='pci-a08-docket-hero',
                       label='Docket da Prova Halloween de 2017: ação de Ariovaldo em primeiro de fevereiro, audiência em primeiro de março, prazo de Odraude até 22 de março e prazo da UFRGS até 13 de abril'),
                   'figure.calendar')


def hearing_panel():
    o = t(28, 36, 'PROVA HALLOWEEN · 2017/2 · QUESTÃO 1', size=13, weight=700)
    o += line(28, 52, 572, 52, w=1)
    o += t(28, 88, 'ARIOVALDO · ODRAUDE · UFRGS', size=12, weight=700)
    o += t(28, 118, 'PRAZOS CONTADOS DA AUDIÊNCIA SEM ACORDO', size=11, fill='var(--ink-2)', weight=600)

    x0, x1 = 62, 536
    y = 184
    o += line(x0, y, x1, y, w=1.8)
    # The axis spans 1 March to 13 April, 43 calendar days.
    marks = [
        (x0, '01/03', 'AUDIÊNCIA'),
        (x0 + 21 * (x1 - x0) / 43, '22/03', 'ODRAUDE'),
        (x0 + 29 * (x1 - x0) / 43, '30/03', 'FERIADO'),
        (x1, '13/04', 'UFRGS'),
    ]
    for i, (x, date, label) in enumerate(marks):
        tone = 'conc' if label == 'FERIADO' else ('dif' if label in {'ODRAUDE', 'UFRGS'} else 'ink')
        o += line(x, y - 7, x, y + 8, tone=tone, w=1.6)
        o += f'<circle cx="{x:.2f}" cy="{y}" r="5.5" style="fill:var(--paper);stroke:var(--{tone});stroke-width:2"/>'
        anchor = 'start' if i == 0 else ('end' if i == len(marks) - 1 else 'middle')
        o += t(x, y - 18, date, size=11, weight=700, anchor=anchor, fill='var(--conc)' if tone == 'conc' else 'var(--ink)')
        o += t(x, y + 27, label, size=11, weight=700 if tone == 'dif' else 600,
               anchor=anchor, fill='var(--conc)' if tone == 'conc' else 'var(--ink-2)')

    x15, x30 = marks[1][0], marks[3][0]
    o += t(62, 263, 'ODRAUDE', size=11, weight=700, fill='var(--dif)')
    o += line(62, 278, x15, 278, tone='dif', w=6)
    o += f'<circle cx="{x15:.2f}" cy="278" r="6" style="fill:var(--dif)"/>'
    o += t(62, 307, '15 DIAS ÚTEIS', size=11, weight=700)
    o += t(62, 353, 'UFRGS', size=11, weight=700, fill='var(--dif)')
    o += line(62, 368, x30, 368, tone='dif', w=6)
    o += f'<circle cx="{x30:.2f}" cy="368" r="6" style="fill:var(--dif)"/>'
    o += t(62, 397, '30 DIAS ÚTEIS · ART. 183', size=11, weight=700)
    o += t(62, 438, '30/03 · SEXTA-FEIRA DA PAIXÃO, EXCLUÍDA', size=11, weight=700, fill='var(--conc)')
    return _family(svg('0 0 600 460', o, cls='fig panel on', ident='pci-a08-term-hearing',
                       label='Calendário do exame de 2017: audiência em primeiro de março, prazo de Odraude até 22 de março e prazo em dobro da UFRGS até 13 de abril'),
                   'figure.timeline')


def cancel_panel():
    o = t(28, 38, 'ART. 335, II · VARIAÇÃO DE UM FATO', size=12, weight=700)
    o += line(28, 54, 572, 54, w=1)
    o += t(300, 112, 'HIPÓTESE LEGAL DE CANCELAMENTO CONFIGURADA', size=11, anchor='middle', fill='var(--ink-2)', weight=600)
    o += f'<rect x="42" y="168" width="204" height="118" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
    o += t(144, 208, 'RÉU', size=11, anchor='middle', weight=700)
    o += t(144, 240, 'PROTOCOLA O PEDIDO', size=11, anchor='middle')
    o += line(247, 226, 352, 226, tone='dif', w=2.2)
    o += f'<path d="M352 226l-10-6v12z" style="fill:var(--dif)"/>'
    o += f'<rect x="354" y="168" width="204" height="118" style="fill:var(--paper-2);stroke:var(--dif);stroke-width:1.8"/>'
    o += t(456, 208, 'TERMO INICIAL', size=11, anchor='middle', weight=700, fill='var(--dif)')
    o += t(456, 240, 'NA DATA DO PROTOCOLO', size=11, anchor='middle')
    o += line(42, 330, 558, 330, tone='muted', w=1, dash='4 4')
    o += t(300, 372, 'SEM DATA ATRIBUÍDA AO PROCESSO', size=11, anchor='middle', weight=700, fill='var(--ink-2)')
    o += t(300, 407, 'NO LITISCONSÓRCIO, CADA PEDIDO TEM SEU PRÓPRIO MARCO', size=11, anchor='middle')
    return _family(svg('0 0 600 460', o, cls='fig panel', ident='pci-a08-term-cancel',
                       label='Variação do caso: quando a hipótese legal de cancelamento está configurada, o pedido protocolado pelo réu inicia o prazo'),
                   'figure.timeline')


def service_panel():
    o = t(28, 38, 'ART. 335, III · VARIAÇÃO DE UM FATO', size=12, weight=700)
    o += line(28, 54, 572, 54, w=1)
    o += t(300, 112, 'SEM AUDIÊNCIA DE CONCILIAÇÃO OU MEDIAÇÃO', size=11, anchor='middle', fill='var(--ink-2)', weight=600)
    o += f'<rect x="36" y="172" width="154" height="126" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
    o += t(113, 212, 'CITAÇÃO', size=12, anchor='middle', weight=700)
    o += line(66, 234, 160, 234, w=1)
    o += line(66, 250, 145, 250, tone='muted', w=1)
    o += line(66, 266, 153, 266, tone='muted', w=1)
    o += line(190, 235, 292, 235, tone='dif', w=2.2)
    o += f'<path d="M292 235l-10-6v12z" style="fill:var(--dif)"/>'
    o += f'<rect x="294" y="172" width="118" height="126" style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1.5"/>'
    o += t(353, 220, 'ART. 231', size=12, anchor='middle', weight=700)
    o += t(353, 252, 'MODO DE', size=11, anchor='middle')
    o += t(353, 270, 'CITAÇÃO', size=11, anchor='middle')
    o += line(412, 235, 462, 235, tone='dif', w=2.2)
    o += f'<path d="M462 235l-10-6v12z" style="fill:var(--dif)"/>'
    o += f'<rect x="464" y="172" width="100" height="126" style="fill:var(--paper);stroke:var(--dif);stroke-width:1.8"/>'
    o += t(514, 220, 'DATA', size=11, anchor='middle', weight=700, fill='var(--dif)')
    o += t(514, 250, 'INICIAL', size=11, anchor='middle')
    o += t(300, 368, 'O MARCO DEPENDE DO MEIO PELO QUAL A CITAÇÃO FOI FEITA', size=11,
           anchor='middle', weight=700, fill='var(--ink-2)')
    o += t(300, 405, 'NENHUMA DATA DO CASO É ALTERADA NESTA VARIAÇÃO', size=11, anchor='middle')
    return _family(svg('0 0 600 460', o, cls='fig panel', ident='pci-a08-term-service',
                       label='Variação do caso sem audiência: o modo de citação define a data inicial nos termos do artigo 231'),
                   'figure.timeline')


def pleading_outline():
    o = t(28, 40, 'CONTESTAÇÃO · ESTRUTURA DE TRABALHO', size=13, weight=700)
    o += line(28, 58, 732, 58, w=1)
    o += t(54, 92, 'IDENTIFICAÇÃO DO PROCESSO E DAS PARTES', size=11, fill='var(--ink-2)', weight=600)
    o += f'<rect x="42" y="112" width="500" height="450" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.6"/>'
    o += line(70, 148, 514, 148, w=1)
    o += t(70, 177, '01', size=13, weight=700, fill='var(--dif)')
    o += t(112, 177, 'PRELIMINARES', size=12, weight=700)
    o += t(112, 202, 'ANTES DA DISCUSSÃO DO MÉRITO', size=11, fill='var(--ink-2)')
    o += line(112, 226, 504, 226, tone='muted', w=1)
    o += line(112, 244, 468, 244, tone='muted', w=1)
    o += line(112, 262, 492, 262, tone='muted', w=1)
    o += line(70, 292, 514, 292, w=1)
    o += t(70, 328, '02', size=13, weight=700, fill='var(--dif)')
    o += t(112, 328, 'MÉRITO · ART. 336', size=12, weight=700)
    o += t(112, 353, 'FUNDAMENTOS DE FATO E DE DIREITO', size=11, fill='var(--ink-2)')
    o += line(112, 377, 488, 377, tone='muted', w=1)
    o += line(112, 395, 468, 395, tone='muted', w=1)
    o += t(112, 428, 'FATO A FATO · ART. 341', size=11, weight=700)
    o += line(112, 449, 492, 449, tone='muted', w=1)
    o += line(112, 467, 450, 467, tone='muted', w=1)
    o += line(70, 496, 514, 496, w=1)
    o += t(70, 532, '03', size=13, weight=700, fill='var(--dif)')
    o += t(112, 532, 'PROVAS PRETENDIDAS · ART. 336', size=11, weight=700)
    o += f'<path d="M576 142H676V270H576z" style="fill:var(--paper-2);stroke:var(--dif);stroke-width:1.5"/>'
    o += t(626, 178, 'ORDEM', size=11, anchor='middle', weight=700, fill='var(--dif)')
    o += t(626, 210, 'PRÉVIA', size=11, anchor='middle')
    o += line(626, 222, 626, 244, tone='dif', w=1.5)
    o += t(626, 264, 'MÉRITO', size=11, anchor='middle', weight=700)
    o += t(576, 316, 'A DEFESA PODE', size=11, weight=600, fill='var(--ink-2)')
    o += t(576, 337, 'APRESENTAR', size=11, weight=600, fill='var(--ink-2)')
    o += t(576, 358, 'ALTERNATIVAS', size=11, weight=700, fill='var(--ink-2)')
    o += line(576, 383, 692, 383, tone='muted', w=1)
    o += t(576, 418, 'SEM PREENCHER', size=11, weight=600, fill='var(--ink-2)')
    o += t(576, 439, 'FATOS DO CASO', size=11, weight=600, fill='var(--ink-2)')
    return _family(svg('0 0 760 600', o, cls='fig', ident='pci-a08-pleading-outline',
                       label='Esboço de contestação que situa preliminares antes do mérito e reserva espaços para fundamentos, impugnação de fatos e provas, sem preencher fatos de uma causa'),
                   'figure.form')


def figures():
    WARN.clear()
    return docket_hero(), hearing_panel(), cancel_panel(), service_panel(), pleading_outline()


def replace_block(page: str, start: str, end: str, value: str) -> str:
    pattern = re.compile(re.escape(start) + r'.*?' + re.escape(end), re.S)
    replacement = start + '\n' + value + '\n' + end
    page, count = pattern.subn(lambda _: replacement, page, count=1)
    if count != 1:
        raise ValueError(f'expected one figure marker pair: {start} / {end}')
    return page


def inject(path: Path | None = None) -> None:
    root = Path(__file__).resolve().parents[2]
    path = path or root / 'courses/processo-civil-i/aula-08.html'
    page = path.read_text(encoding='utf-8')
    hero, p1, p2, p3, p4 = figures()
    panel_html = '\n'.join((p1, p2, p3))
    hero_html = ('<figure class="a08-hero-figure">' + hero
                 + '<figcaption>Prova Halloween · Processo Civil I · 2017/2, questão 1.</figcaption></figure>')
    page = replace_block(page, '<!-- A08_HERO:BEGIN -->', '<!-- A08_HERO:END -->', hero_html)
    page = replace_block(page, '<!-- A08_F1:BEGIN -->', '<!-- A08_F1:END -->', panel_html)
    page = replace_block(page, '<!-- A08_F2:BEGIN -->', '<!-- A08_F2:END -->', p4)
    path.write_text(page, encoding='utf-8')
    if WARN:
        raise RuntimeError('\n'.join(WARN))


if __name__ == '__main__':
    inject()
