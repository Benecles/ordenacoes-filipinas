"""Controle Aula 23 · pertinência temática. The doors of art. 103 return from Aula 22: the universal ones open,
the special ones (IV, V, IX) carry a lock that only pertinência opens. The five conditions are a form; the
traditional and functional readings of 'classe' are the same form answered two ways; ADI 7.813 and 7.926 are
records with their stamps. Ink; blue = what the STF decided; orange = the limit (the lock, non-admission).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a20 import tick

ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
SPECIAL = {3, 4, 8}


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def say(x, y, s, size=16, fill='var(--ink)', italic=False):
    return f'<text x="{x}" y="{y}" style="font-family:var(--serif,serif);font-size:{size}px;fill:{fill}{";font-style:italic" if italic else ""}">{s}</text>'


def doors(y=100, focus=None):
    o = ''
    for i in range(9):
        x = 40 + i * 58; w, h = 42, 70
        dim = focus is not None and i not in focus
        st = f'fill:var(--paper);stroke:{"var(--ink-2)" if dim else "var(--ink)"};stroke-width:1.4'
        if i in SPECIAL:
            o += f'<path d="M{x} {y + h}V{y + 10}Q{x + w / 2} {y - 6} {x + w} {y + 10}V{y + h}" style="{st}"/>'
            o += f'<rect x="{x + w / 2 - 7}" y="{y + 32}" width="14" height="11" style="fill:none;stroke:var(--conc);stroke-width:1.6"/>'
            o += f'<path d="M{x + w / 2 - 4} {y + 32}v-4a4 4 0 0 1 8 0v4" style="fill:none;stroke:var(--conc);stroke-width:1.6"/>'
        else:   # open: the leaf swung inward
            o += f'<path d="M{x} {y + h}V{y + 10}Q{x + w / 2} {y - 6} {x + w} {y + 10}V{y + h}" style="fill:var(--ink);stroke:var(--ink);stroke-width:1.4;opacity:{".35" if dim else "1"}"/>'
            o += f'<path d="M{x} {y + h}L{x + 14} {y + h - 8}V{y + 14}L{x} {y + 10}" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>'
        o += t(x + w / 2, y + h + 18, ROMAN[i], size=10, anchor='middle', fill='var(--ink-2)' if dim else 'var(--ink)')
    return o


def neutros():
    o = head('Art. 103 · duas classes de portas') + doors()
    o += t(40, 226, 'abertas · legitimados universais', size=10.5, caps=True, weight=700)
    o += say(40, 256, 'Presidente, Mesas do Senado e da Câmara, PGR,', 15) + say(40, 278, 'Conselho Federal da OAB, partido no Congresso.', 15)
    o += say(40, 302, 'O interesse é presumido.', 15, 'var(--dif)')
    o += t(40, 352, 'com fechadura · legitimados especiais', size=10.5, caps=True, weight=700, fill='var(--conc)')
    o += say(40, 382, 'Mesa de Assembleia, Governador, confederação ou', 15) + say(40, 404, 'entidade de classe nacional: provam pertinência.', 15)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-neutros',
               label='Nove portas do art. 103: seis abertas, dos legitimados universais; três com fechadura, IV, V e IX, que precisam provar pertinência temática')


def especiais():
    o = head('A fechadura: pertinência temática') + doors(focus=SPECIAL)
    o += say(40, 250, 'Só o caso concreto diz se a porta abre:')
    o += say(40, 274, 'a finalidade institucional tem de casar com a norma.')
    o += say(40, 330, 'O STF quer evitar a banalização das ações diretas.', 15, 'var(--ink-2)', True)
    o += say(40, 374, 'Há quem no STF queira rever o requisito,', 15, 'var(--conc)', True)
    o += say(40, 396, 'sobretudo para governadores.', 15, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-especiais',
               label='As mesmas portas, com destaque para as três com fechadura: a pertinência temática se decide caso a caso')


def form(ident, title, rows, stamp=None, notes=(), label=''):
    o = head(title)
    h = 40 + len(rows) * 48
    o += f'<path d="M40 70H546L560 84V{70 + h}H40Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    for i, (s, on) in enumerate(rows):
        y = 112 + i * 48
        o += (tick(60, y) if on else f'<rect x="60" y="{y - 17}" width="22" height="22" style="fill:none;stroke:var(--ink);stroke-width:1.4"/>')
        o += say(96, y, s, 15)
    if stamp:
        s, tone, sy = stamp
        o += f'<g transform="rotate(-6 420 {sy})"><rect x="{420 - len(s) * 5.4 - 14}" y="{sy - 18}" width="{len(s) * 10.8 + 28}" height="32" rx="3" style="fill:none;stroke:{tone};stroke-width:2.2"/>'
        o += t(420, sy + 4, s, size=13, anchor='middle', weight=700, caps=True, ls='.12em', fill=tone) + '</g>'
    for i, (s, fill) in enumerate(notes):
        o += say(40, 110 + h + (90 if stamp else 40) + i * 24, s, 15, fill)
    return svg('0 0 600 600', o, cls='panel fig on', ident=ident, label=label)


def cond():
    rows = [('Homogeneidade entre os membros', True), ('Categoria econômica ou profissional', True), ('Associados em pelo menos nove estados', True),
            ('Pertinência entre objetivos e norma impugnada', True), ('Representatividade integral dos atingidos', True)]
    return form('p-cond', 'Entidade de classe nacional · cinco condições', rows,
                notes=[('Cinco caixas, todas exigidas, examinadas uma a uma.', 'var(--ink)')],
                label='Formulário com cinco caixas marcadas: homogeneidade, categoria econômica ou profissional, presença em nove estados, pertinência e representatividade integral')


def trad():
    rows = [('Homogeneidade entre os membros', True), ('Categoria econômica ou profissional', False), ('Associados em pelo menos nove estados', True)]
    return form('p-trad', 'Leitura tradicional · UNE · ADI 894', rows, stamp=('não conhecida', 'var(--conc)', 296),
                notes=[('“Classe” = categoria profissional. Estudantes', 'var(--ink)'), ('não são: a caixa fica vazia (ADI 894, 1995).', 'var(--ink-2)')],
                label='O mesmo formulário para a UNE: a caixa da categoria profissional fica vazia e o carimbo diz não conhecida, na leitura tradicional da ADI 894')


def func():
    o = head('Leitura funcional · grupos vulneráveis')
    rows = [('APIB · indígenas', 'ADPF 709'), ('CONAQ · quilombolas', 'ADPF 742'), ('FBASD · síndrome de Down', 'ADPF 936/DF'), ('Aliança LGBTI+', 'ADPF 1.151/1.153')]
    for i, (who, case) in enumerate(rows):
        y = 84 + i * 66
        o += f'<rect x="40" y="{y}" width="520" height="52" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>'
        o += say(58, y + 32, who, 16) + t(296, y + 31, case, size=11, caps=True, fill='var(--ink-2)')
        o += f'<rect x="452" y="{y + 12}" width="92" height="28" rx="3" style="fill:none;stroke:var(--dif);stroke-width:2"/>' + t(498, y + 31, 'admitida', size=10.5, anchor='middle', weight=700, caps=True, fill='var(--dif)')
    o += say(40, 400, '“Classe” lida pela função: entidades nacionais de')
    o += say(40, 424, 'direitos humanos, na defesa de grupos vulneráveis.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-func',
               label='Quatro registros carimbados como admitidos: APIB na ADPF 709, CONAQ na ADPF 742, FBASD na ADPF 936 e a Aliança LGBTI+ nas ADPFs 1.151 e 1.153')


def concl():
    o = head('Relativização, não superação')
    for i, (a, b) in enumerate([('O critério tradicional continua.', 'Representatividade nacional e pertinência.'),
                                ('“Classe” ganha leitura funcional.', 'Entidades de direitos humanos, grupos vulneráveis.'),
                                ('A formulação segura:', 'requisito preservado, leitura flexível.')]):
        y = 110 + i * 100
        o += t(40, y, f'{i + 1}', size=26, weight=800, fill='var(--ink-2)')
        o += say(80, y - 4, a, 18) + say(80, y + 22, b, 15, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-concl',
               label='Três conclusões: o critério tradicional continua; classe ganha leitura funcional; o requisito fica, com leitura flexível')


def record(ident, title, rows, stamp, tone, label):
    o = head(title)
    o += '<path d="M40 70H546L560 84V330H40Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    for i, (k, v) in enumerate(rows):
        y = 110 + i * 40
        o += t(60, y, k, size=10.5, caps=True, fill='var(--ink-2)') + say(220, y, v, 15)
    o += f'<g transform="rotate(-5 300 380)"><rect x="{300 - len(stamp) * 5.6 - 16}" y="362" width="{len(stamp) * 11.2 + 32}" height="36" rx="3" style="fill:none;stroke:{tone};stroke-width:2.4"/>'
    o += t(300, 386, stamp, size=14, anchor='middle', weight=700, caps=True, ls='.12em', fill=tone) + '</g>'
    return svg('0 0 600 600', o, cls='panel fig on', ident=ident, label=label)


def tend():
    o = head('Dois julgamentos, dois resultados')
    for i, (case, who, stamp, tone) in enumerate([('ADI 7.813 AgR · 2025', 'CNSaúde', 'agravo provido', 'var(--dif)'), ('ADI 7.926 · 2026', 'CNTI', 'não conhecida', 'var(--conc)')]):
        x = 40 + i * 270
        o += f'<path d="M{x} 80H{x + 236}L{x + 250} 94V300H{x}Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
        o += t(x + 16, 112, case, size=11, weight=700, caps=True) + say(x + 16, 146, who, 18)
        o += f'<g transform="rotate(-6 {x + 125} 230)"><rect x="{x + 30}" y="212" width="190" height="34" rx="3" style="fill:none;stroke:{tone};stroke-width:2.2"/>'
        o += t(x + 125, 235, stamp, size=13, anchor='middle', weight=700, caps=True, ls='.1em', fill=tone) + '</g>'
    o += say(40, 380, 'Processos distintos, resultados distintos;')
    o += say(40, 404, 'ambos decididos pela pertinência temática.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-tend',
               label='Dois autos lado a lado: ADI 7.813 AgR, de 2025, carimbada agravo provido; ADI 7.926, de 2026, carimbada não conhecida')


def a7813():
    return record('p-7813', 'ADI 7.813 AgR/DF · 2025',
                  [('legitimada', 'CNSaúde · especial'), ('objeto', 'normas tributárias de caráter geral'), ('relator p/ acórdão', 'Min. Gilmar Mendes'),
                   ('sessão virtual', '12 a 19.12.2025 · Plenário'), ('decisão', 'regular processamento da ADI')],
                  'pertinência reconhecida', 'var(--dif)',
                  'Registro da ADI 7.813 AgR: CNSaúde, normas tributárias de caráter geral, Plenário em dezembro de 2025; carimbo de pertinência reconhecida')


def a7926():
    return record('p-7926', 'ADI 7.926/SC · 2026',
                  [('legitimada', 'CNTI · especial'), ('objeto', 'cotas no ensino superior · SC'), ('relator', 'Min. Gilmar Mendes'),
                   ('sessão virtual', '10 a 17.4.2026 · Plenário'), ('decisão', 'ação não conhecida')],
                  'sem pertinência', 'var(--conc)',
                  'Registro da ADI 7.926: CNTI, cotas no ensino superior em Santa Catarina, Plenário em abril de 2026; carimbo sem pertinência')


def panels():
    return [neutros(), especiais(), cond(), trad(), func(), concl(), tend(), a7813(), a7926()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-23.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
