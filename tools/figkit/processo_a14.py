"""Aula 14 score: the statutory sequence in CPC arts. 369–371."""
from pathlib import Path
import sys
import re
sys.path.insert(0, str(Path(__file__).resolve().parent))
from figkit import t, line, svg

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / 'courses' / 'processo-civil-i' / 'aula-14.html'
HERO_START, HERO_END = '<!-- A14_42_HERO_START -->', '<!-- A14_42_HERO_END -->'
BET_START, BET_END = '<!-- A14_42_BET_START -->', '<!-- A14_42_BET_END -->'
STYLE_START, STYLE_END = '/* A14_42_START */', '/* A14_42_END */'


def opening_form():
    """Art. 370 decision form: initiative, necessity, and reasoned refusal."""
    o = ''
    o += t(42, 38, 'CPC · ART. 370', size=13, weight=700)
    o += t(558, 38, 'PROVA PARA JULGAR O MÉRITO', size=11, anchor='end', fill='var(--ink-2)', weight=600)
    o += line(42, 53, 558, 53, tone='ink', w=1.3)
    o += t(42, 91, 'INICIATIVA', size=11, fill='var(--ink-2)', weight=700)
    o += t(42, 119, 'a requerimento da parte', size=15, weight=600)
    o += t(42, 147, 'ou de ofício', size=15, weight=600)
    o += line(42, 169, 248, 169, tone='ink', w=1)
    o += t(42, 202, 'É necessária ao julgamento?', size=15, weight=700)
    o += line(300, 211, 300, 226, tone='ink', w=1.4)
    o += line(300, 226, 420, 226, tone='ink', w=1.4)
    o += line(420, 226, 420, 250, tone='ink', w=1.4)
    o += line(300, 226, 300, 250, tone='conc', w=1.4)
    o += t(300, 269, 'SIM', size=11, fill='var(--dif)', weight=700)
    o += t(420, 269, 'NÃO', size=11, fill='var(--conc)', weight=700)
    o += line(300, 278, 300, 294, tone='dif', w=1.5)
    o += line(420, 278, 420, 294, tone='conc', w=1.5)
    o += t(300, 317, 'DETERMINAR', size=12, fill='var(--dif)', weight=700)
    o += t(420, 317, 'INDEFERIR SE INÚTIL', size=11, fill='var(--conc)', weight=700)
    o += t(420, 336, 'OU PROTELATÓRIA', size=11, fill='var(--conc)', weight=700)
    o += t(42, 336, 'decisão fundamentada', size=11, fill='var(--ink-2)', weight=600)
    return svg('24 18 550 350', o, cls='hero-form', ident='pci-a14-opening-form',
               label='Formulário de decisão do art. 370: a prova pode ser determinada a pedido ou de ofício quando necessária ao julgamento; diligência inútil ou meramente protelatória é indeferida por decisão fundamentada').replace(
                   '<svg', '<svg data-family="figure.form"', 1)


def opening_bet():
    # Every factual/legal statement in this bet is grounded in CPC art. 370,
    # exact capture: work/pipeline/processo-civil-i/compendium/aula-14/30-supporting-003-cpc-lei-13105-capture-2026-09-28-Art.-370.txt.
    return '''<div class="bet" id="a14-opening-bet"><div><span class="bet-k">Antes de ler · art. 370 do CPC</span><p class="bet-q">O juiz pode determinar prova sem pedido da parte? E deve deferir toda diligência requerida?</p><div class="bet-opts"><button type="button" data-opt="0" aria-pressed="false">Pode agir de ofício, mas determina a prova necessária ao mérito; diligência inútil ou protelatória pode ser indeferida com fundamentação.</button><button type="button" data-opt="1" data-court aria-pressed="false">Só pode agir se a parte pedir, e deve deferir toda diligência para garantir o direito à prova.</button></div><div class="bet-reveal"><p>Art. 370 permite a iniciativa de ofício ou a requerimento, limitada às provas necessárias ao julgamento do mérito. O parágrafo único determina o indeferimento fundamentado das diligências inúteis ou meramente protelatórias.</p></div></div></div>'''


def _replace_marked(source, start, end, content):
    pattern = re.compile(re.escape(start) + r'.*?' + re.escape(end), re.S)
    if source.count(start) == source.count(end) == 1:
        return pattern.sub(start + content + end, source, count=1)
    if source.count(start) or source.count(end):
        raise ValueError(f'partial or duplicate marker pair: {start}')
    return None


def install_opening():
    source = PAGE.read_text()
    hero = '<figure class="hero-art">' + opening_form() + '<figcaption>O art. 370 liga a iniciativa à necessidade e exige fundamentação para recusar diligências inúteis ou protelatórias.</figcaption></figure>'
    replaced = _replace_marked(source, HERO_START, HERO_END, hero)
    if replaced is not None:
        source = replaced
    else:
        anchor = '<div class="titleblock label"'
        if source.count(anchor) != 1:
            raise ValueError('Aula 14 hero titleblock anchor is absent or duplicated')
        source = source.replace(anchor, HERO_START + hero + HERO_END + anchor, 1)
    bet = _replace_marked(source, BET_START, BET_END, opening_bet())
    if bet is not None:
        source = bet
    else:
        anchor = '</header>\n<section class="chapter"'
        if source.count(anchor) != 1:
            raise ValueError('Aula 14 header close anchor is absent or duplicated')
        source = source.replace(anchor, '</header>\n' + BET_START + opening_bet() + BET_END + '\n<section class="chapter"', 1)
    style = '.hero-art{max-width:900px;margin:26px 0 0}.hero-art svg{display:block;width:min(100%,780px);height:auto}.hero-art figcaption{font:500 11px/1.5 var(--mono);color:var(--ink-2);margin:8px 0 0}'
    replaced = _replace_marked(source, STYLE_START, STYLE_END, style)
    if replaced is not None:
        source = replaced
    else:
        if source.count('</style>') != 1:
            raise ValueError('Aula 14 inline style close is absent or duplicated')
        source = source.replace('</style>', STYLE_START + style + STYLE_END + '</style>', 1)

    # Floor-driven polish: keep the existing distinctions, phrased as the reader's
    # analysis rather than as narration of information absent from a source.
    swaps = {
        'No enunciado, a existência de fatos sem impugnação expressa não informa que documento, testemunha ou outro meio os apoiaria.':
            'A impugnação dos fatos e a escolha de um meio que possa sustentá-los ocupam etapas distintas da análise.',
        'O enunciado de Jesse não identifica meio de prova específico.':
            'Para avaliar o caso de Jesse, importa localizar qual afirmação factual um meio de prova poderia sustentar.',
        'O enunciado fornece uma pergunta geral sobre a produção de prova a respeito de fatos “inverossímeis”; não informa a afirmação factual, o meio pretendido nem sua utilidade para o mérito.':
            'A questão 11 aborda, em termos gerais, a produção de prova sobre fatos “inverossímeis”; sua análise pede que se localizem a afirmação factual, o meio pretendido e a utilidade para o mérito.',
    }
    for old, new in swaps.items():
        if source.count(old) == 1:
            source = source.replace(old, new, 1)
        elif source.count(new) != 1:
            raise ValueError(f'Aula 14 polish anchor absent or duplicated: {old[:48]}')
    PAGE.write_text(source)
    print(f'updated {PAGE}')


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
    install_opening()
    print(panel())


def inject_thread_position(lesson_html):
    """Fill Aula 14's marked Jesse figure from the shared thread source."""
    from processo_threads import inject_single_page
    page = Path(__file__).resolve().parents[2] / 'courses' / 'processo-civil-i' / 'aula-14.html'
    return inject_single_page(18, page, lesson_html)
