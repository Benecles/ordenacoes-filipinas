"""Aula 20: the Florianópolis reasons and a qualitative sufficiency selector."""
from figkit import t, line, svg


def panel():
    """Grow Aula 19's located decision excerpt with the judge's valuation step."""
    o = '<rect x="12" y="12" width="376" height="468" rx="2" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
    o += t(30, 40, 'FLORIANÓPOLIS · TRECHOS DA DECISÃO', size=13, weight=700)
    o += line(30, 52, 370, 52, w=1.2)

    # These two source locations are the judge's own account of how each date was found.
    o += t(30, 82, 'CONTESTAÇÃO', size=11.5, fill='var(--ink-2)', weight=700)
    o += t(30, 108, 'compra do aparelho', size=14, weight=600, ls='.01em')
    o += t(370, 108, 'NOV. 2012', size=14, anchor='end', fill='var(--ink)', weight=700)
    o += line(30, 118, 370, 118, tone='ink', w=2)

    o += t(30, 150, 'ÚLTIMA PÁGINA DA INICIAL', size=11.5, fill='var(--ink-2)', weight=700)
    o += t(30, 176, 'ajuizamento da ação', size=14, weight=600, ls='.01em')
    o += t(370, 176, '18 AGO. 2015', size=14, anchor='end', fill='var(--ink)', weight=700)
    o += line(30, 186, 370, 186, tone='ink', w=2)

    # An ink bracket ties the two dates to the result the judgment actually states.
    o += '<path d="M22 118H17V186H22" style="fill:none;stroke:var(--ink);stroke-width:2.5"/>'
    o += line(200, 194, 200, 218, tone='ink', w=2)
    o += t(200, 242, 'DECADÊNCIA RECONHECIDA', size=14, anchor='middle', fill='var(--dif)', weight=700)
    o += t(200, 263, 'a razão exposta compara as datas', size=11.5, anchor='middle', fill='var(--ink-2)', ls='.01em')

    # The separate item-15 question remains a distinct annotation, as in Aula 19.
    o += line(30, 284, 370, 284, tone='muted', w=1, dash='3 4')
    o += t(30, 310, 'ITEM 15 · IMPUGNAÇÃO', size=11.5, fill='var(--ink)', weight=700)
    o += t(30, 336, 'tentativas amigáveis', size=14, weight=600, ls='.01em')
    o += t(30, 361, '“Mas, onde está a prova?”', size=13, italic=True, ls='0')
    o += t(30, 390, '“Ou onde isso foi alegado na inicial?”', size=13, italic=True, ls='0')
    o += t(30, 420, 'O item 15 pergunta pelas tentativas.', size=11, fill='var(--ink-2)', ls='.01em')
    o += t(30, 441, 'A razão ligada às datas leva à decadência.', size=11, fill='var(--ink-2)', ls='.01em')
    o += t(30, 463, 'Autos 0321861-32.2015.8.24.0023 · decisão de 15/01/2016',
           size=9.5, fill='var(--ink-2)', weight=600, ls='.01em')
    return svg('0 0 400 492', o, cls='fig', ident='pci-a16-timeline',
               label='Anotação da decisão de Florianópolis: a contestação situa a compra em novembro de 2012, a última página da inicial situa o ajuizamento em 18 de agosto de 2015, e a decisão reconhece decadência; item 15 fica em faixa separada')


def excerpt_panel():
    """Select a qualitative model before weighing; the slots are categories, not a scale."""
    o = '<rect x="12" y="12" width="376" height="548" rx="2" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
    o += t(30, 40, 'ENTRADA · FATOS E INTERESSES', size=12, weight=700)
    o += t(30, 64, 'Aula 20 · data de compra em disputa', size=12, fill='var(--ink-2)', ls='.01em')
    o += line(30, 78, 370, 78, tone='ink', w=1.2)

    # The same purchase-date issue stays patrimonial; it enters the ordinary slot.
    cards = [
        (98, '01 · PATRIMONIAL ORDINÁRIO', 'PREPONDERÂNCIA DE PROVAS',
         'Indenização por acidente de trânsito', 'Knijnik · p. 18', True),
        (207, '02 · CONTEXTO ESPECÍFICO', 'VEROSSIMILHANÇA SUFICIENTE',
         'Lesão pré-natal, conforme o direito material', 'Marinoni · pp. 261–262', False),
        (316, '03 · INTERESSE DE MAIOR PESO', 'PROVA CLARA E CONVINCENTE',
         'Perda do poder familiar; anulação de testamento', 'Knijnik · pp. 38–39', False),
    ]
    for y, head, model, example, source, selected in cards:
        stroke = 'var(--ink)' if selected else 'var(--ink-2)'
        weight = 2.5 if selected else 1.3
        o += f'<rect x="26" y="{y}" width="348" height="94" rx="2" style="fill:var(--paper-2);stroke:{stroke};stroke-width:{weight}"/>'
        o += t(38, y + 20, head, size=9.5, fill='var(--ink)', weight=700, ls='.035em')
        o += t(38, y + 43, model, size=12, fill='var(--ink)', weight=700, ls='.01em')
        o += t(38, y + 63, example, size=10.2, fill='var(--ink)', weight=500, ls='.005em')
        o += t(38, y + 81, source, size=9, fill='var(--ink-2)', weight=500, ls='.01em')
    o += t(370, 94, 'SELECIONADO', size=9.5, anchor='end', fill='var(--ink)', weight=700, ls='.04em')

    o += line(30, 427, 370, 427, tone='conc', w=1.5)
    o += t(30, 450, 'SE O MODELO EXIGIDO NÃO FOR ATINGIDO', size=10.5, fill='var(--conc)', weight=700, ls='.01em')
    o += t(30, 473, 'mantenha-o selecionado; avalie a suficiência', size=10.5, fill='var(--ink)', weight=600, ls='.005em')
    o += t(30, 490, 'e encaminhe a dúvida residual à Aula 21.', size=10.5, fill='var(--ink)', weight=600, ls='.005em')
    o += line(30, 507, 370, 507, tone='muted', w=1, dash='3 4')
    o += t(30, 530, 'CATEGORIAS, SEM PERCENTUAIS OU ESCALA', size=9.5, fill='var(--ink-2)', weight=700, ls='.025em')
    o += t(30, 547, 'Modelos abertos · Knijnik, p. 23', size=9.5, fill='var(--ink-2)', ls='.01em')
    return svg('0 0 400 572', o, cls='fig', ident='pci-a16-excerpt',
               label='Seletor qualitativo: preponderância para disputa patrimonial ordinária, verossimilhança quando o direito material permite, ou prova clara e convincente para interesse de maior peso; o modelo fica selecionado e a dúvida residual segue à Aula 21')


if __name__ == '__main__':
    print(panel())
