"""Processo Civil I Aula 01 · the initial petition as filed, built with Document."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from figkit import Document, line, svg, t


PETITION = [
    ('title', 'Petição inicial · art. 319', 'title'),
    ('place', ('', 'Excelentíssimo Senhor Juiz de Direito da __ Vara Cível.'), 'juizo'),
    ('party', ('', 'Autora: __________ · CPF: __________ · Endereço: __________.'), 'partes_a'),
    ('party', ('', 'Réu: __________ · CPF: __________ · Endereço: __________.'), 'partes_b'),
    ('clause', ('DOS FATOS', 'Empréstimo de R$ 12 mil. Vencimento sem pagamento.'), 'fatos'),
    ('clause', ('DO DIREITO', 'A relação jurídica que decorre dos fatos.'), 'direito'),
    ('clause', ('DOS PEDIDOS', 'Condenação ao pagamento.'), 'pedido'),
    ('clause', ('VALOR DA CAUSA', 'R$ 12 mil.'), 'valor'),
    ('clause', ('PROVAS', 'Provas pretendidas.'), 'provas'),
    ('clause', ('AUDIÊNCIA', 'Conciliação / mediação:   □   Sim     □   Não'), 'audiencia'),
]

INCISOS = [
    (['juizo'], 'I', 'dif'),
    (['partes_a', 'partes_b'], 'II', 'dif'),
    (['fatos', 'direito'], 'III', 'conc'),
    (['pedido'], 'IV', 'conc'),
    (['valor'], 'V', 'ink'),
    (['provas'], 'VI', 'ink'),
    (['audiencia'], 'VII', 'ink'),
]


def panel():
    # A facsimile rather than a row list: the call-outs land on the actual legal pleading.
    d = Document('pci-a01', 28, 28, 360, PETITION, lead=18, indent=0, foot=10)
    sheet_y = d.y + d.h - 25
    attachment_y = sheet_y + 20
    # The art. 320 attachment sits behind the final part of the actual pleading.
    back = (f'<path d="M190 {attachment_y}H510L526 {attachment_y + 16}V{attachment_y + 115}H190Z" '
            'style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1.4"/>'
            f'<path d="M510 {attachment_y}V{attachment_y + 16}H526" '
            'style="fill:var(--paper);stroke:var(--ink);stroke-width:1"/>'
            f'<path d="M371 {d.y + d.h - 32}l8 8m-2 -11l8 8" '
            'style="fill:none;stroke:var(--ink);stroke-width:1.4"/>'
            + t(210, attachment_y + 42, 'Doc. 1 · contrato de empréstimo', size=14, fill='var(--ink)')
            + t(210, attachment_y + 66, 'ART. 320', size=14, fill='var(--muted)', weight=700, caps=True))
    # Highlight the pleaded loan facts, not the repeated seven-item list.
    o = back + d.paper() + d.highlight(['fatos'], 'conc') + ''.join(d.parts)
    # Inciso marks and leaders are anchored in the page's own regions.
    for keys, inciso, tone in INCISOS:
        ys = [d.box[k][1] for k in keys] + [d.box[k][3] for k in keys]
        cy = (min(ys) + max(ys)) / 2
        o += line(d.x + d.w - 15, cy, 408, cy, tone=tone, w=1.3)
        o += t(417, cy + 5, inciso, size=18, fill=f'var(--{tone})', weight=700)
    # The § 2º note points to the still-empty CPF field; it is not another row in the form.
    qy = (d.box['partes_a'][1] + d.box['partes_a'][3]) / 2
    o += line(d.x + d.w - 36, qy + 4, 402, qy + 4, tone='dif', w=1.1, dash='3 3')
    o += t(417, qy - 2, '§ 2º', size=14, fill='var(--dif)', weight=700)
    o += t(417, qy + 15, 'ainda', size=14, fill='var(--ink-2)')
    o += t(417, qy + 30, 'citável', size=14, fill='var(--ink-2)')
    return svg(f'12 18 576 {d.h + 54}', o, cls='panel fig on', ident='p-pi0',
               label='Petição inicial em sua ordem real, com os incisos do art. 319 e contrato anexo do art. 320')


if __name__ == '__main__':
    print(panel())
