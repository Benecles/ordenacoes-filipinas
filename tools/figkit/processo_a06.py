"""Processo Civil I · Aula 06. Inline decision forms for the page's distinctions."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import svg, t, line


def _box(x, y, w, h, tone='ink'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" style="fill:var(--paper);stroke:var(--{tone});stroke-width:1.5"/>'


def hero():
    o = t(38, 31, 'PEDIDO ENTRE JUÍZOS · ESCOLHA DA VIA', size=13, weight=700, caps=True)
    o += line(38, 46, 1042, 46, w=1.2)
    o += t(38, 75, 'ATO SOLICITADO', size=10.5, weight=700, fill='var(--ink-2)', caps=True)
    o += t(210, 75, 'Cooperação jurisdicional', size=15, weight=600)
    o += _box(38, 92, 478, 58, 'ink') + _box(564, 92, 478, 58, 'ink')
    o += f'<rect x="54" y="109" width="20" height="20" style="fill:none;stroke:var(--ink);stroke-width:1.7"/>'
    o += f'<rect x="580" y="109" width="20" height="20" style="fill:none;stroke:var(--ink);stroke-width:1.7"/>'
    o += t(88, 116, 'VIA DIRETA', size=10.5, weight=700, fill='var(--ink)', caps=True)
    o += t(88, 137, 'prescinde de forma específica · art. 69', size=13)
    o += t(614, 116, 'CARTA', size=10.5, weight=700, fill='var(--ink)', caps=True)
    o += t(614, 137, 'regime próprio do CPC · art. 69, § 1º', size=13)
    result = svg('0 0 1080 170', o, cls='hero-fork', label='Formulário de escolha da via para pedido entre juízos: cooperação direta sem forma específica ou carta submetida ao regime do Código')
    return result.replace('<svg class="hero-fork figkit"', '<svg class="hero-fork figkit" data-family="figure.form"', 1)


def medium():
    o = t(32, 34, 'ARTS. 212, § 3º, E 213 · CORTE NO ÚLTIMO DIA', size=12, weight=700, caps=True)
    o += line(32, 48, 568, 48, w=1.2)
    o += _box(32, 64, 258, 158, 'ink') + _box(310, 64, 258, 158, 'ink')
    o += t(48, 90, 'PETIÇÃO EM AUTOS', size=11, weight=700, fill='var(--ink-2)', caps=True)
    o += t(48, 108, 'NÃO ELETRÔNICOS', size=11, weight=700, fill='var(--ink-2)', caps=True)
    o += t(48, 143, 'corte aplicável', size=11, weight=600, fill='var(--ink)')
    o += t(48, 169, 'expediente local', size=16, weight=700, fill='var(--conc)')
    o += t(48, 195, 'horário do fórum ou tribunal', size=11.5)
    o += t(326, 90, 'ATO PROCESSUAL', size=11, weight=700, fill='var(--ink-2)', caps=True)
    o += t(326, 108, 'ELETRÔNICO', size=11, weight=700, fill='var(--ink-2)', caps=True)
    o += t(326, 143, 'corte aplicável', size=11, weight=600, fill='var(--ink)')
    o += t(326, 169, 'até 24:00', size=16, weight=700, fill='var(--conc)')
    o += t(326, 195, 'no horário do juízo', size=11.5)
    return svg('0 0 600 245', o, cls='fig', ident='pci-a06-medium', label='Formulário de corte no último dia: petição em autos não eletrônicos segue o expediente local; ato eletrônico pode ser praticado até 24 horas no horário do juízo')


def letter():
    o = t(32, 40, 'ART. 267 · PRECATÓRIA OU ARBITRAL', size=13, weight=700, caps=True)
    o += _box(32, 58, 536, 43, 'dif')
    o += f'<rect x="48" y="70" width="18" height="18" style="fill:none;stroke:var(--dif);stroke-width:1.5"/>'
    o += t(80, 85, 'ÂMBITO DO DISPOSITIVO', size=11, weight=700, fill='var(--ink)', caps=True)
    o += t(556, 85, 'precatória ou arbitral', size=10.5, weight=600, anchor='end')
    items = [
        ('I', 'requisito legal ausente'),
        ('II', 'incompetência material ou hierárquica'),
        ('III', 'dúvida sobre autenticidade'),
    ]
    for i, (n, desc) in enumerate(items):
        y = 116 + i * 54
        o += _box(32, y, 536, 42, 'ink')
        o += t(50, y + 26, n, size=11, weight=700, fill='var(--ink)')
        o += t(82, y + 27, desc, size=13, fill='var(--conc)')
    o += _box(32, 292, 258, 64, 'conc') + _box(310, 292, 258, 64, 'dif')
    o += t(48, 316, 'FUNDAMENTO PRESENTE', size=9.5, weight=700, fill='var(--ink)', caps=True)
    o += t(48, 340, 'recusa motivada', size=14, weight=600)
    o += t(326, 316, 'SE HOUVER INCOMPETÊNCIA', size=9.5, weight=700, fill='var(--ink)', caps=True)
    o += t(326, 340, 'encaminhar ao competente', size=13.5, weight=600)
    o += t(32, 390, 'A RECUSA E O ENCAMINHAMENTO DEPENDEM DO FUNDAMENTO', size=9.5, weight=700, fill='var(--ink-2)', caps=True)
    return svg('0 0 600 410', o, cls='fig', ident='pci-a06-letter', label='Formulário de decisão limitado à carta precatória e arbitral: requisitos, competência material ou hierárquica e autenticidade; recusa motivada e possível encaminhamento')


if __name__ == '__main__':
    from inject import inject
    ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
    os.chdir(ROOT)
    replaced = inject('courses/processo-civil-i/aula-06.html', {
        'hero': hero(), 'pci-a06-medium': medium(), 'pci-a06-letter': letter(),
    })
    print(f'processo-civil-i/aula-06.html: {replaced} figures injected')
