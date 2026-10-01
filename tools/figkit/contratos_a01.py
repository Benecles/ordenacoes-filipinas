"""Contratos Aula 01: classify legal facts, read the contract, and test its destination."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from figkit import Document, Field, Tally, statute, svg, t

STEPS1 = [
    'Fato jurídico em sentido estrito',
    'Ato-fato',
    'Ato jurídico em sentido estrito',
    'Negócio jurídico',
]
IDS1 = ['p-lad0', 'p-lad1', 'p-lad2', 'p-lad3']

STEPS2 = [
    'O acordo de vontades',
    'A operação econômica',
    'Operação econômica não é especulação',
    'O contrato no Direito',
]
IDS2 = ['p-est', 'p-sub', 'p-esp', 'p-nor']

STEPS3 = [
    'O bem termina no uso ou volta para o mercado?',
    'Três correntes',
    'Mesmo critério, resultados opostos',
]
IDS3 = ['p-dest', 'p-teo', 'p-cas']


def fact_field(k):
    """Classify the four legal-fact forms by human action and the will's role."""
    f = Field('tgc01-facts', x0=190, x1=540, y0=130, y1=430)
    f.axes(
        [(235, ('não', 'há ação humana')), (455, ('sim', 'há ação humana'))],
        [
            (150, ('vontade escolhe', 'conteúdo e efeitos')),
            (280, ('vontade age', 'a lei fixa os efeitos')),
            (410, ('vontade irrelevante', 'só importa o resultado')),
        ],
        xtitle='Ação humana',
        ytitle='Papel da vontade',
    )
    f.point(235, 410, 'Fato jurídico estrito', active=k == 0, tone='ink',
            dx=12, dy=-58, sub='natureza · nascimento · morte · tempo')
    f.point(455, 410, 'Ato-fato', active=k == 1, tone='ink',
            dx=-10, dy=-28, anchor='end', sub='caça · tomada de posse')
    f.point(455, 280, 'Ato jurídico em sentido estrito', active=k == 2, tone='ink',
            dx=-12, dy=-24, anchor='end', sub='domicílio · a lei define efeitos')
    f.point(510, 150, 'Negócio jurídico', active=k == 3, tone='ink',
            dx=-12, dy=-24, anchor='end', sub='contrato · vontade escolhe conteúdo')
    o = t(40, 60, 'QUATRO FORMAS DE FATO JURÍDICO', size=11, caps=True, weight=700,
          fill='var(--ink-2)')
    o += t(40, 82, 'Ação humana e papel da vontade organizam a classificação.',
           size=11, fill='var(--ink)')
    o += f.svg()
    o += t(40, 505, 'Do acontecimento natural à escolha de efeitos dentro dos limites legais.',
           size=10.5, fill='var(--ink-2)')
    return svg('24 44 552 484', o, cls='panel fig on' if k == 0 else 'panel fig',
               ident=IDS1[k], label=STEPS1[k])


def panels1():
    return [fact_field(k) for k in range(4)]


# The paper is a generic contract specimen: every entry is a term used in the lesson,
# with no invented parties, prices, dates, goods, or performance conditions.
CONTRACT_LINES = [
    ('title', 'Estrutura do contrato', 'title'),
    ('clause', ('Formação', 'proposta + aceitação'), 'formation'),
    ('clause', ('Natureza', 'bilateral quanto à formação'), 'nature'),
    ('clause', ('Operação', 'bens · serviços · crédito'), 'operation'),
    ('clause', ('Circulação', 'uso de coisas · riscos'), 'circulation'),
    ('clause', ('Função', 'fazer a riqueza circular'), 'wealth'),
    ('clause', ('Forma jurídica', 'dá força obrigatória à operação'), 'force'),
    ('clause', ('Ordenamento', 'interpreta · executa · limita'), 'law'),
]


def contract_document(k):
    d = Document(f'tgc01-doc-{k}', 82, 58, 436, CONTRACT_LINES, lead=25, foot=14)
    o = d.paper()
    if k == 0:
        o += d.highlight(['formation', 'nature'], 'dif')
    elif k == 1:
        o += d.highlight(['operation', 'circulation', 'wealth'], 'mix')
    elif k == 2:
        o += d.highlight(['operation', 'circulation'], 'dif')
    else:
        o += d.highlight(['force', 'law'], 'conc')
    o += ''.join(d.parts)

    if k == 0:
        o += t(40, 424, 'PROPOSTA + ACEITAÇÃO = ACORDO', size=10.5, caps=True,
               weight=700, fill='var(--dif)')
        o += t(40, 448, 'Bilateral na formação, mesmo quando só uma parte se obriga.',
               size=11, fill='var(--ink)')
    elif k == 1:
        o += t(40, 424, 'A OPERAÇÃO POR TRÁS DO ACORDO', size=10.5, caps=True,
               weight=700, fill='var(--mix)')
        o += t(40, 448, 'O contrato põe bens, serviços, crédito, uso de coisas e riscos em circulação.',
               size=10.5, fill='var(--ink)')
    elif k == 2:
        o += t(40, 424, 'EXEMPLOS CITADOS', size=10.5, caps=True, weight=700,
               fill='var(--dif)')
        o += t(40, 448, 'Uso próprio, seguro e serviço para uma atividade também são operações econômicas.',
               size=10.5, fill='var(--ink)')
    else:
        o += t(40, 424, 'LEI · FORÇA · INTERPRETAÇÃO · EXECUÇÃO · LIMITES',
               size=10.5, caps=True, weight=700, fill='var(--conc)')
        o += t(40, 448, 'Arts. 421 e 421-A articulam função social, paridade presumida e regimes especiais.',
               size=10.5, fill='var(--ink)')
    return svg('24 42 552 426', o, cls='panel fig on' if k == 0 else 'panel fig',
               ident=IDS2[k], label=STEPS2[k])


def economic_tally():
    tally = Tally('tgc01-econ', x0=40, x1=560, y0=160, columns=6, step=70, dot=6)
    tally.row('Categorias da operação', ['bens', 'serviços', 'crédito', 'uso de coisas', 'riscos'],
              tone='mix', sub='cada ponto corresponde a um item listado')
    tally.legend([('mix', 'um ponto por categoria nomeada; sem escala')], y=226)
    o = t(40, 58, 'A FUNÇÃO DO CONTRATO · CIRCULAÇÃO DE RIQUEZA',
          size=10.5, caps=True, weight=700, fill='var(--ink-2)') + tally.svg()
    for x, label in zip((210, 280, 350, 420, 490),
                        ('bens', 'serviços', 'crédito', 'uso de coisas', 'riscos')):
        o += t(x, 198, label, size=9.5, anchor='middle', fill='var(--ink-2)')
    o += t(40, 270, 'ACORDO E OPERAÇÃO', size=10.5, caps=True, weight=700,
           fill='var(--ink-2)')
    for x, label, detail in (
        (120, 'ACORDO', 'proposta + aceitação'),
        (300, 'OPERAÇÃO', 'bens e serviços em circulação'),
        (460, 'FUNÇÃO', 'circulação de riqueza'),
    ):
        o += t(x, 310, label, size=10.5, caps=True, anchor='middle', weight=700,
               fill='var(--mix)')
        o += t(x, 336, detail, size=9.5, anchor='middle', fill='var(--ink)')
    o += t(40, 386, 'O acordo é a roupagem; por trás dele há uma operação econômica.',
           size=10.5, fill='var(--ink)')
    o += t(40, 414, 'A função do contrato é fazer a riqueza circular.',
           size=10.5, weight=700, fill='var(--ink-2)')
    o += t(460, 386, 'OPERAÇÃO', size=9.5, caps=True, anchor='middle', weight=700,
           fill='var(--mix)')
    o += t(460, 412, 'ECONÔMICA', size=9.5, caps=True, anchor='middle', weight=700,
           fill='var(--mix)')
    return svg('24 42 503 392', o, cls='panel fig', ident=IDS2[1], label=STEPS2[1])


def speculation_tally():
    tally = Tally('tgc01-speculation', x0=40, x1=560, y0=150, columns=7, step=42, dot=6)
    tally.row('Operações sem aposta ou busca de lucro',
              ['compra para uso próprio', 'seguro de um bem', 'serviço para tocar uma atividade'],
              tone='dif', sub='exemplos de operações econômicas')
    tally.row('Contratos especulativos', ['derivativos'],
              tone='conc', sub='parte pequena do todo')
    tally.legend([('dif', 'operações sem aposta'), ('conc', 'especulativo')], y=290)
    o = t(40, 58, 'OPERAÇÃO ECONÔMICA NÃO EXIGE ESPECULAÇÃO', size=10.5, caps=True, weight=700,
          fill='var(--ink-2)') + tally.svg()
    o += t(40, 385, 'Uma marca por exemplo ou tipo citado; as marcas não medem frequência.',
           size=10.5, fill='var(--ink-2)')
    o += t(40, 412, 'Derivativos existem, mas são parte pequena do conjunto.',
           size=10.5, weight=700, fill='var(--conc)')
    return svg('24 42 552 426', o, cls='panel fig', ident=IDS2[2], label=STEPS2[2])


# Exact excerpts checked against the official Civil Code at Planalto:
# https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm
def statute_cut():
    o = t(40, 58, 'A FORMA JURÍDICA DÁ FORÇA E IMPÕE LIMITES',
          size=10.5, caps=True, weight=700, fill='var(--ink-2)')
    s1, h1 = statute(40, 86, 520, 'Código Civil · art. 421', [
        ('A liberdade contratual será exercida ', False),
        ('nos limites da função social do contrato.', True),
    ], tone='conc')
    s2, h2 = statute(40, 86 + h1 + 18, 520, 'Código Civil · art. 421-A', [
        ('Os contratos civis e empresariais presumem-se ', False),
        ('paritários e simétricos', True),
        (' até a presença de elementos concretos que justifiquem o afastamento dessa presunção, ', False),
        ('ressalvados os regimes jurídicos previstos em leis especiais', True),
        (', garantido também que: […]', False),
    ], tone='conc')
    o += s1 + s2
    y = 86 + h1 + 18 + h2 + 44
    o += t(40, y, 'A FORMA JURÍDICA', size=10.5, caps=True, weight=700,
           fill='var(--conc)')
    o += t(40, y + 24, 'dá força obrigatória e orienta interpretação, execução e limites da operação.',
           size=10.5, fill='var(--ink)')
    return svg('24 42 552 426', o, cls='panel fig', ident=IDS2[3], label=STEPS2[3])


def panels2():
    return [contract_document(0), economic_tally(), speculation_tally(), statute_cut()]


def destination_field():
    f = Field('tgc01-destination', x0=190, x1=540, y0=142, y1=450)
    f.axes(
        [(265, ('necessidade', 'própria')), (480, ('atividade', 'do adquirente'))],
        [(170, ('bem termina', 'no uso')), (410, ('bem entra', 'na atividade'))],
        xtitle='O que o adquirente faz?',
        ytitle='Destino do bem',
    )
    f.point(265, 170, 'Destinatário final', active=True, tone='dif',
            dx=12, dy=-20, sub='atende a necessidade própria')
    f.point(480, 410, 'Consumo intermediário', active=True, tone='conc',
            dx=-12, dy=-34, anchor='end', sub='insumo · ferramenta · peça · revenda')
    o = t(40, 62, 'DESTINAÇÃO DO BEM OU SERVIÇO', size=10.5, caps=True, weight=700,
          fill='var(--ink-2)')
    o += t(40, 84, 'Uso próprio ou integração na atividade do adquirente?',
           size=10.5, fill='var(--ink)')
    o += t(40, 112, 'CDC', size=10.5, caps=True, weight=700, fill='var(--dif)')
    o += t(78, 112, 'relação de consumo', size=10.5, fill='var(--ink-2)')
    o += t(275, 112, 'consumo intermediário', size=10.5, caps=True, weight=700, fill='var(--conc)')
    o += f.svg()
    o += t(300, 565, 'Conta a função econômica real, não o desgaste do bem.',
           size=10.5, anchor='middle', fill='var(--ink-2)')
    return svg('24 42 552 540', o, cls='panel fig on', ident=IDS3[0], label=STEPS3[0])


def theory_field():
    f = Field('tgc01-theories', x0=190, x1=540, y0=140, y1=435)
    f.axes(
        [(230, ('não', 'basta ser destinatário de fato')),
         (470, ('sim', 'de fato e economicamente'))],
        [(165, ('sim', 'flexibiliza com vulnerabilidade')),
         (410, ('não', 'não flexibiliza'))],
        xtitle='Exige destinação econômica?',
        ytitle='Vulnerabilidade muda o resultado?',
    )
    f.point(230, 410, 'Maximalista', active=True, tone='ink',
            dx=12, dy=-50, sub='basta ser destinatário de fato')
    f.point(470, 410, 'Finalista', active=True, tone='ink',
            dx=-12, dy=-18, anchor='end', sub='retira de fato e economicamente')
    f.point(470, 165, 'Finalismo aprofundado', active=True, tone='dif',
            dx=-12, dy=-26, anchor='end', sub='finalista; cede com vulnerabilidade')
    o = t(40, 58, 'PESSOA JURÍDICA COMO DESTINATÁRIA FINAL?', size=10.5, caps=True,
          weight=700, fill='var(--ink-2)')
    o += f.svg()
    o += t(40, 500, 'O STJ parte do finalismo e o flexibiliza diante de vulnerabilidade provada.',
           size=10.5, fill='var(--ink)')
    o += t(40, 527, 'A especialidade do CDC depende da resposta à relação de consumo.',
           size=10.5, fill='var(--ink-2)')
    return svg('24 42 552 540', o, cls='panel fig', ident=IDS3[1], label=STEPS3[1])


def case_tally():
    left = Document('tgc01-case-aircraft', 40, 104, 245, [
        ('title', 'Aeronave', 'title'),
        ('clause', ('Adquirente', 'administradora de imóveis'), 'buyer'),
        ('clause', ('Destino', 'necessidade própria'), 'destination'),
        ('clause', ('Atividade', 'não integrava o serviço vendido'), 'activity'),
        ('clause', ('Resultado', 'STJ aplicou o CDC'), 'result'),
    ], lead=22, indent=70, foot=10)
    right = Document('tgc01-case-ticket', 315, 104, 245, [
        ('title', 'Intermediação', 'title'),
        ('clause', ('Adquirente', 'vendedora de ingressos'), 'buyer'),
        ('clause', ('Destino', 'serviço usado para operar o negócio'), 'destination'),
        ('clause', ('Prova', 'sem prova de vulnerabilidade'), 'proof'),
        ('clause', ('Resultado', 'STJ afastou o CDC'), 'result'),
    ], lead=22, indent=70, foot=10)
    o = t(40, 60, 'MESMO CRITÉRIO, RESULTADOS OPOSTOS', size=10.5, caps=True,
          weight=700, fill='var(--ink-2)')
    o += left.paper() + left.highlight(['result'], 'dif') + ''.join(left.parts)
    o += right.paper() + right.highlight(['result'], 'conc') + ''.join(right.parts)
    o += t(40, 557, 'A destinação e a prova de vulnerabilidade distinguem os casos descritos.',
           size=10.5, fill='var(--ink)')
    return svg('24 42 552 540', o, cls='panel fig', ident=IDS3[2], label=STEPS3[2])


def panels3():
    return [destination_field(), theory_field(), case_tally()]
