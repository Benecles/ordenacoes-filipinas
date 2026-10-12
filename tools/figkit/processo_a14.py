"""Aula 14 score: the statutory sequence in CPC arts. 369–371."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from figkit import t, line, svg


def panel():
    # Four measured statutory operations share two staves; alignment is the comparison.
    x0, x1 = 205, 1050
    xs = [x0 + i * (x1 - x0) / 4 for i in range(5)]
    o = ''
    # Staff rules and measure bars are the score's information-bearing geometry.
    for y, tone in [(252, 'conc'), (423, 'dif')]:
        o += line(x0, y, x1, y, tone='ink', w=2.2)
        for x in xs:
            o += line(x, y - 18, x, y + 18, tone=tone, w=1.5)
    for i, x in enumerate(xs):
        o += line(x, 210, x, 465, tone='muted', w=1, dash='2 5')
    # Ordered measure heads: article and operative statutory term.
    heads = [('369', 'meios legítimos'), ('370', 'pedido / ofício'),
             ('370', 'necessidade / recusa'), ('371', 'avaliação / razões')]
    for i, (art, lab) in enumerate(heads):
        cx = (xs[i] + xs[i+1]) / 2
        o += t(cx, 190, 'ART. ' + art, size=13, fill='var(--ink)', anchor='middle', weight=700)
        o += t(cx, 211, lab.upper(), size=11, fill='var(--ink-2)', anchor='middle', weight=600)
    o += t(35, 258, 'DEMONSTRATIVO', size=12, fill='var(--conc)', weight=700)
    o += t(35, 429, 'ARGUMENTATIVO', size=12, fill='var(--dif)', weight=700)
    o += t(35, 447, '/ PERSUASIVO', size=11, fill='var(--dif)', weight=600)
    upper = ['qual afirmação', 'o que informa', 'qual lacuna', 'qual conclusão']
    lower = ['quem participa', 'quem provoca', 'qual razão', 'quais razões']
    for i, x in enumerate(xs[:-1]):
        cx = (x + xs[i+1]) / 2
        # Paired note-heads, joined by one continuous staff: two lenses, one law.
        o += f'<circle cx="{cx:g}" cy="252" r="8" style="fill:var(--conc-wash);stroke:var(--conc);stroke-width:2"/>'
        o += f'<circle cx="{cx:g}" cy="423" r="8" style="fill:var(--dif-wash);stroke:var(--dif);stroke-width:2"/>'
        o += t(cx, 294, upper[i], size=12, fill='var(--ink)', anchor='middle', weight=600, ls='.01em')
        o += t(cx, 315, 'sustentada?', size=12, fill='var(--ink-2)', anchor='middle', weight=500, ls='.01em')
        o += t(cx, 465, lower[i], size=12, fill='var(--ink)', anchor='middle', weight=600, ls='.01em')
        o += t(cx, 486, 'no processo?', size=12, fill='var(--ink-2)', anchor='middle', weight=500, ls='.01em')
    # Four beats survive removal of every label: order and vertical pairing remain visible.
    o += line(x0, 535, x1, 535, tone='ink', w=1.4)
    for i, x in enumerate(xs):
        o += f'<circle cx="{x:g}" cy="535" r="4" style="fill:var(--ink)"/>'
    o += t(x0, 565, 'MEIOS', size=11, fill='var(--ink-2)', weight=600)
    o += t(xs[1], 565, 'INICIATIVA', size=11, fill='var(--ink-2)', anchor='middle', weight=600)
    o += t(xs[2], 565, 'NECESSIDADE', size=11, fill='var(--conc)', anchor='middle', weight=700)
    o += t(xs[3], 565, 'AVALIAÇÃO', size=11, fill='var(--ink-2)', anchor='middle', weight=600)
    o += t(x1, 565, 'DECISÃO', size=11, fill='var(--ink-2)', anchor='end', weight=600)
    return svg('20 165 1045 415', o, cls='fig', ident='pci-a14-score',
               label='Partitura dos arts. 369 a 371: duas pautas mostram perguntas demonstrativas e argumentativas sobre os mesmos marcos legais')


def docket_panel():
    """The exam's case record: acts are located; absent detail stays unfilled."""
    o = ''
    o += t(46, 53, 'AUTOS · AVALIAÇÃO 2 / 2015', size=16, weight=700)
    o += t(46, 79, 'JESSE VALADÃO  ×  DALVO FRITZ E SEROTONINA DA SILVA',
           size=15, weight=600)
    o += line(46, 96, 954, 96, w=1.5)

    # A docket has an ordered margin and distinct entries, not prose in ruled cells.
    o += line(91, 127, 91, 455, w=2)
    entries = [
        (143, 'AÇÃO', 'Cobrança solidária de R$ 100.000',
         'Jesse demanda contra Dalvo e Serotonina', 'ink'),
        (231, '01/04/2015', 'Audiência preliminar',
         'Todas as partes comparecem · sem acordo', 'ink'),
        (320, '1ª SEMANA', 'Dalvo apresenta contestação',
         'Fatos da inicial sem impugnação expressa', 'conc'),
        (413, '13/04/2015', 'Dalvo protocola complemento',
         'Impugna os fatos antes esquecidos', 'dif'),
    ]
    for y, when, act, detail, tone in entries:
        o += line(78, y, 104, y, tone=tone, w=3)
        o += t(123, y - 8, when, size=12, fill=f'var(--{tone})', weight=700)
        o += t(300, y - 8, act, size=15, weight=700)
        o += t(300, y + 18, detail, size=12, fill='var(--ink-2)')
        o += line(123, y + 37, 954, y + 37, tone='muted', w=.8)

    # The unfiled defense is a visible open track, rather than a dated act.
    o += t(680, 301, 'SEROTONINA', size=11, fill='var(--dif)', weight=700)
    o += line(680, 312, 954, 312, tone='dif', w=1.5, dash='4 4')
    o += t(680, 334, 'sem defesa · sem advogado', size=11, fill='var(--ink-2)')

    # The source names neither the omitted allegations nor any evidence request.
    o += t(46, 493, 'CAMPOS QUE O ENUNCIADO NÃO PREENCHE', size=12,
           fill='var(--ink-2)', weight=700)
    o += line(46, 504, 954, 504, w=1.3)
    o += t(46, 532, 'FATOS NÃO IMPUGNADOS', size=11, fill='var(--conc)', weight=700)
    o += line(46, 551, 440, 551, tone='conc', w=1.1, dash='3 4')
    o += t(514, 532, 'MEIOS DE PROVA', size=11, fill='var(--dif)', weight=700)
    o += line(514, 551, 954, 551, tone='dif', w=1.1, dash='3 4')
    o += t(46, 590, 'ALEGADO  →  INFORMAÇÃO  →  CONCLUSÃO', size=12,
           fill='var(--ink-2)', weight=700)
    o += t(954, 590, 'Avaliação 2, 2015, Q1', size=11,
           fill='var(--ink-2)', anchor='end', weight=600)
    return svg('24 25 948 582', o, cls='fig', ident='pci-a14-docket',
               label='Autos do caso Jesse Valadão: sequência processual conhecida e campos não informados no enunciado da Avaliação 2 de 2015')


if __name__ == '__main__':
    print(panel())


def inject_thread_position(lesson_html):
    """Fill Aula 14's marked Jesse figure from the shared thread source."""
    from processo_threads import inject_single_page
    page = Path(__file__).resolve().parents[2] / 'courses' / 'processo-civil-i' / 'aula-14.html'
    return inject_single_page(18, page, lesson_html)
