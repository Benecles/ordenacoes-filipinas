"""Processo Civil I Aula 01 · the initial petition as filed, built with Document."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from figkit import Document, line, svg, t

# The hidden body copy sets the Document's real paragraph positions; the drawing renders it as
# grey typeset lines and keeps only the short words needed to read the claim.
PETITION = [
    ('title', 'Petição inicial · art. 319', 'title'),
    ('place', 'Excelentíssimo Senhor Juiz de Direito da __ Vara Cível.', 'juizo'),
    ('party', 'Parte autora: [nome] · CPF [campo] · endereço: [endereço].', 'partes_a'),
    ('party', 'Parte ré: [nome] · CPF __________ · endereço: [endereço].', 'partes_b'),
    ('clause', 'DOS FATOS', 'fatos'),
    ('place', 'Empréstimo de R$ 12 mil.', 'fatos_a'),
    ('place', 'Vencimento sem pagamento.', 'fatos_b'),
    ('clause', 'DO DIREITO', 'direito'),
    ('place', 'Fato jurídico e relação jurídica.', 'direito_b'),
    ('clause', 'DOS PEDIDOS', 'pedido'),
    ('place', 'Condenação ao pagamento.', 'pedido_b'),
    ('clause', 'VALOR DA CAUSA', 'valor'),
    ('place', 'R$ __________.', 'valor_b'),
    ('clause', 'PROVAS', 'provas'),
    ('place', 'Provas pretendidas.', 'provas_b'),
    ('clause', 'AUDIÊNCIA', 'audiencia'),
    ('place', 'Conciliação ou mediação: [ ] sim · [ ] não.', 'audiencia_b'),
]

INCISOS = [
    (['juizo'], 'I · juízo', 'dif'),
    (['partes_a', 'partes_b'], 'II · partes', 'dif'),
    (['fatos', 'fatos_a', 'fatos_b', 'direito', 'direito_b'], 'III · fatos e fundamentos', 'conc'),
    (['pedido', 'pedido_b'], 'IV · pedido', 'conc'),
    (['valor', 'valor_b'], 'V · valor', 'ink'),
    (['provas', 'provas_b'], 'VI · provas', 'ink'),
    (['audiencia', 'audiencia_b'], 'VII · audiência', 'ink'),
]


def serif(x, y, text, size=16, fill='var(--ink-2)', weight=400):
    return (f'<text x="{x:g}" y="{y:g}" style="font-family:var(--serif,serif);font-size:{size}px;'
            f'font-weight:{weight};fill:{fill}">{text}</text>')


def panel():
    # A facsimile rather than a ruled list: incisos point to their real positions in the pleading.
    d = Document('pci-a01', 28, 28, 360, PETITION, lead=22, indent=0, foot=10)
    attachment_y = d.y + d.h - 58
    # Art. 320's sheet is physically behind the pleading and shows in the exposed lower corner.
    back = (f'<path d="M250 {attachment_y}H572L588 {attachment_y + 16}V{attachment_y + 115}H250Z" '
            'style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1.4"/>'
            f'<path d="M572 {attachment_y}V{attachment_y + 16}H588" '
            'style="fill:var(--paper);stroke:var(--ink);stroke-width:1"/>'
            f'<path d="M371 {d.y + d.h - 32}l8 8m-2 -11l8 8" '
            'style="fill:none;stroke:var(--ink);stroke-width:1.4"/>')
    o = back + d.paper()

    # The page itself carries the geometry: paper, folded corner, attachment, and section layout.

    # Title, conventional pleading headings, and only the words the incisos ask the student to read.
    o += t(d.x + d.w / 2, d.box['title'][1] + 13, 'PETIÇÃO INICIAL · ART. 319', size=18,
           fill='var(--ink)', anchor='middle', weight=700, caps=True)
    o += serif(d.x + 16, d.box['juizo'][1] + 12, 'Excelentíssimo Senhor Juiz de Direito', 16)
    o += serif(d.x + 16, d.box['juizo'][1] + 34, 'da __ Vara Cível', 14)
    for key, label in [('fatos', 'DOS FATOS'), ('direito', 'DO DIREITO'),
                       ('pedido', 'DOS PEDIDOS'), ('valor', 'VALOR DA CAUSA'),
                       ('provas', 'PROVAS'), ('audiencia', 'AUDIÊNCIA')]:
        o += t(d.x + 16, d.box[key][1] + 12, label, size=16, fill='var(--ink-2)', weight=700, caps=True)
    # Qualification remains a paragraph with blanks; no names or identifying facts are invented.
    for key, role in [('partes_a', 'Parte autora'), ('partes_b', 'Parte ré')]:
        yy = d.box[key][1] + 12
        cpf = 'CPF [campo]' if key == 'partes_a' else 'CPF __________'
        o += serif(d.x + 16, yy, f'{role}: [nome] · {cpf}', 15)
        o += serif(d.x + 16, yy + 22, 'endereço: [endereço]', 15)
    # The facts that turn “sou credor” into a pleaded cause are the tested mark.
    for key, phrase in [('fatos_a', 'Empréstimo de R$ 12 mil.'),
                        ('fatos_b', 'Vencimento sem pagamento.')]:
        o += serif(d.x + 16, d.box[key][1] + 12, phrase, 16, 'var(--conc)', 600)
    o += serif(d.x + 16, d.box['pedido_b'][1] + 12, 'Condenação ao pagamento.', 16, 'var(--ink)')
    o += serif(d.x + 16, d.box['valor_b'][1] + 12, 'Dá-se à causa o valor de R$ ________.', 14, 'var(--ink-2)')
    o += serif(d.x + 16, d.box['audiencia_b'][1] + 12, 'Conciliação ou mediação:', 14, 'var(--ink-2)')
    o += serif(d.x + 16, d.box['audiencia_b'][1] + 34, '[ ] sim   ·   [ ] não', 14, 'var(--ink-2)')
    # Stapled sheet label in the exposed edge, clear of the seven inciso leaders.
    o += t(397, attachment_y + 76, 'DOC. 1 · ART. 320', size=16, fill='var(--muted)', weight=700)
    o += serif(397, attachment_y + 98, 'contrato de empréstimo', 16, 'var(--ink)')

    for keys, label, tone in INCISOS:
        ys = [d.box[k][1] for k in keys] + [d.box[k][3] for k in keys]
        cy = (min(ys) + max(ys)) / 2
        if label != 'VII · audiência':
            o += line(d.x + d.w, cy, 408, cy, tone=tone, w=1.3)
        if label.startswith('III'):
            o += t(417, cy + 5, 'III · FATOS', size=17, fill='var(--conc)', weight=700)
            o += t(417, cy + 31, 'E FUNDAMENTOS', size=16, fill='var(--conc)', weight=600)
        else:
            offset = -6 if label == 'VII · audiência' else 5
            o += t(417, cy + offset, label, size=17, fill=f'var(--{tone})', weight=700)

    # The missing defendant CPF is an open field, attached to the § 2º note.
    qy = (d.box['partes_b'][1] + d.box['partes_b'][3]) / 2
    o += line(d.x + d.w - 30, qy + 4, 408, qy + 4, tone='dif', w=1.1, dash='3 3')
    o += t(417, qy + 25, '§ 2º · AINDA CITÁVEL', size=16, fill='var(--dif)', weight=700)

    return svg(f'12 18 576 {d.h + 75}', o, cls='panel fig on', ident='p-pi0',
               label='Petição inicial em sua ordem real, com os incisos do art. 319 e contrato anexo do art. 320')


if __name__ == '__main__':
    print(panel())
