"""Controle Aula 22 · quem pode propor ADI. Doors for the legitimated parties (Brazil's nine, Germany's three),
measured dot fields for the flow and the stock (units printed, periods labelled as the lesson does), and the
signature block of a petition for capacidade postulatória: who signs, who needs a lawyer, why a governor's
missing signature makes the petition inepta. Ink; blue = the rule applied; orange = the limit.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a12 import dots, key

ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def say(x, y, s, size=16, fill='var(--ink)', italic=False):
    return f'<text x="{x}" y="{y}" style="font-family:var(--serif,serif);font-size:{size}px;fill:{fill}{";font-style:italic" if italic else ""}">{s}</text>'


def door(x, y, label, w=40, h=66):
    o = f'<path d="M{x} {y + h}V{y + 10}Q{x + w / 2} {y - 6} {x + w} {y + 10}V{y + h}" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    o += f'<circle cx="{x + w - 9}" cy="{y + h / 2 + 6}" r="2" style="fill:var(--ink)"/>'
    o += t(x + w / 2, y + h + 18, label, size=10, anchor='middle', fill='var(--ink-2)')
    return o


def rol():
    o = head('Quem pode provocar o controle abstrato')
    o += t(40, 92, 'Brasil · art. 103 da CF', size=11, weight=700, caps=True)
    o += ''.join(door(40 + i * 56, 110, ROMAN[i]) for i in range(9))
    o += t(40, 254, 'Alemanha · art. 93 (1), frase 2, da Lei Fundamental', size=11, weight=700, caps=True)
    for i, s in enumerate(['gov. federal', 'gov. estadual', '1/4 do Parlamento']):
        o += door(40 + i * 120, 272, '', w=56) + t(68 + i * 120, 362, s, size=10, anchor='middle', fill='var(--ink-2)')
    o += say(40, 430, 'Nove portas no Brasil; três na Alemanha.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-rol-comp',
               label='Nove portas numeradas de I a IX para os legitimados do art. 103 no Brasil; três portas na Alemanha: governo federal, governo estadual e um quarto do Parlamento')


def fluxo():
    o = head('Ações novas de controle abstrato')
    o += t(40, 92, 'STF · 1º semestre de 2025 · ≈150', size=11, weight=700, caps=True)
    o += dots(150, 46, 120, 25, step=20, r=5.6)
    o += t(40, 278, 'BVerfG · todo o ano de 2025 · 1', size=11, weight=700, caps=True)
    o += dots(1, 46, 304, 1, r=5.6)
    o += key(40, 360, 'um ponto = uma ação')
    o += say(40, 420, 'Seis meses no STF contra doze no BVerfG:')
    o += say(40, 444, 'uma diferença de ordem de grandeza.', 16, 'var(--ink-2)', True)
    o += say(40, 488, 'Classes e períodos diferem: um contraste aproximado.', 15, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-fluxo-anual',
               label='Cento e cinquenta pontos para as ações novas no STF no primeiro semestre de 2025; um ponto para o Tribunal Constitucional alemão em todo o ano')


def estoque():
    o = head('Estoque de ações')
    o += t(40, 92, 'STF · pendentes em jun/2025 · 1.001', size=11, weight=700, caps=True)
    o += dots(101, 46, 120, 25, step=20, r=5.6, partial=.1)      # 1.001 / 10
    o += t(40, 238, 'BVerfG · 1951 a 31/12/2025 · 194', size=11, weight=700, caps=True)
    o += dots(20, 46, 264, 25, step=20, r=5.6, partial=.4)       # 194 / 10
    o += key(40, 320, 'um ponto = dez ações')
    o += say(40, 384, 'Cerca de cinco para um.')
    o += say(40, 428, 'Períodos e critérios diferem: um contraste', 15, 'var(--conc)', True)
    o += say(40, 450, 'aproximado entre desenhos institucionais.', 15, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-estoque',
               label='Cento e um pontos para as 1.001 ações pendentes no STF; vinte para as 194 ações do Tribunal Constitucional alemão desde 1951; cada ponto, dez ações')


def signature(y, who, line_note, signed=True, lawyer=False, struck=False):
    o = f'<line x1="80" y1="{y}" x2="400" y2="{y}" style="stroke:var(--ink);stroke-width:1.2"/>'
    if signed:
        o += f'<path d="M96 {y - 6} q16 -22 30 -4 t28 -6 t26 4 t34 -10" style="fill:none;stroke:var(--ink);stroke-width:1.6"/>'
    o += t(80, y + 18, who, size=10.5, caps=True) + t(80, y + 33, line_note, size=10, fill='var(--ink-2)')
    if struck:
        o += f'<line x1="74" y1="{y + 14}" x2="406" y2="{y + 14}" style="stroke:var(--conc);stroke-width:2"/>'
    return o


def sheet_end(title):
    o = '<path d="M40 70H546L560 84V400H40Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    o += t(60, 100, title, size=11, weight=700, caps=True)
    o += ''.join(f'<line x1="60" y1="{124 + i * 16}" x2="{520 - (i % 3) * 60}" y2="{124 + i * 16}" style="stroke:var(--ink-2);stroke-width:1"/>' for i in range(5))
    return o


def especial():
    o = head('Capacidade postulatória especial · I a VII') + sheet_end('Petição inicial · ADI')
    o += signature(270, 'Governador do Estado', 'de próprio punho, sem advogado')
    o += say(40, 450, 'Presidente, Mesas, Governador, PGR, Conselho')
    o += say(40, 474, 'Federal da OAB: assinam a inicial.', 16, 'var(--dif)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-especial',
               label='O fim de uma petição de ADI assinada pelo próprio Governador: os legitimados dos incisos I a VII assinam sem advogado')


def sem_cap():
    o = head('Sem capacidade postulatória · VIII e IX') + sheet_end('Petição inicial · ADI')
    o += signature(250, 'Advogado · OAB', 'por procuração do partido ou da confederação')
    o += say(80, 330, 'Procuração com as normas impugnadas', 15)
    o += say(80, 352, '(ADI 2.552 e 2.187).', 15, 'var(--ink-2)')
    o += say(40, 450, 'Partido e confederação ou entidade de classe')
    o += say(40, 474, 'precisam de advogado.', 16, 'var(--conc)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-sem-cap',
               label='O fim da petição assinado por advogado, com procuração que indica as normas impugnadas: partidos e entidades dos incisos VIII e IX não assinam sozinhos')


def cargo():
    o = head('A capacidade é do cargo') + sheet_end('Petição inicial · ADI')
    o += signature(230, 'Governador do Estado', 'sem assinatura', signed=False)
    o += signature(310, 'Procurador-Geral do Estado', 'assina sozinho')
    o += '<g transform="rotate(-7 470 270)"><rect x="410" y="252" width="120" height="34" rx="3" style="fill:none;stroke:var(--conc);stroke-width:2.2"/>'
    o += t(470, 275, 'inepta', size=14, anchor='middle', weight=700, caps=True, ls='.16em', fill='var(--conc)') + '</g>'
    o += say(40, 450, 'Irrenunciável: o cargo assina, ou a inicial é inepta.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-cargo',
               label='A linha do Governador fica em branco e só o Procurador-Geral do Estado assina: o carimbo diz inepta, porque a capacidade é do cargo')


def panels():
    return [rol(), fluxo(), estoque(), especial(), sem_cap(), cargo()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-22.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
