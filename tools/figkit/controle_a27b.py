"""Controle Aula 27 · plenário virtual, the panels around the clock (controle_a27 keeps the clock). The system
as four steps; its traits as a form; who may ask for a destaque as two records; virtual → presencial as
tracks; the ADI 6200 snapshot (11–18/09/2026) as the bench grouped by position; the 2024–2025 statistics as dot
fields (one dot = 10 judgments). Ink; blue = what is decided; orange = the limit.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a16 import say, track
from controle_a23 import form
from controle_a24 import step
from controle_a09 import stamp, paper
from controle_a12 import dots, key


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def sistema():
    o = head('Quatro peças do sistema')
    for i, (s, sub) in enumerate([('pauta', 'abre a janela'), ('voto', 'cada ministro'), ('vista', 'suspende a conclusão'), ('resultado', 'ao fechar')]):
        o += step(40 + i * 132, 120, 110, s, sub, fill=(s != 'vista'))
    o += say(40, 240, 'Um ambiente assíncrono e colegiado: decidem juntos,')
    o += say(40, 264, 'não ao mesmo tempo.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-sistema', label='Quatro etapas do plenário virtual: pauta, voto, vista e resultado')


def carac():
    return form('p-carac', 'Plenário virtual · características',
                [('Colegiado: votos inseridos na janela aberta', True), ('Assíncrono: cada ministro no seu tempo', True), ('Público: relatório, votos e placar no portal', True)],
                notes=[('Não é sessão por videoconferência:', 'var(--conc)'), ('não há reunião ao vivo, há um sistema.', 'var(--ink-2)')],
                label='Formulário com três caixas marcadas: colegiado, assíncrono, público; e a nota de que não é videoconferência')


def dest_quem():
    o = head('Destaque · quem pode pedir')
    o += paper(40, 70, 240, 120, 'Ministro · a qualquer hora')
    o += stamp(160, 168, 'retira do virtual', 'var(--dif)')
    o += paper(320, 70, 240, 120, 'Parte · até 48 h antes')
    o += stamp(440, 168, 'se o relator acolher', 'var(--conc)', -5)
    o += say(40, 260, 'O ministro destaca sem depender da Presidência.')
    o += say(40, 284, 'A parte só pede: indeferido, segue no virtual.', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-dest-quem',
               label='Dois pedidos de destaque: o do ministro, carimbado retira do virtual; o da parte, até 48 horas antes, carimbado se o relator acolher')


def dest_regra():
    o = head('Virtual → destaque → presencial')
    o += track(120, [(60, 260, 'on'), (260, 540, 'off')], 'votos no virtual')
    o += track(200, [(300, 540, 'on')], 'presencial · reinicia o caso')
    o += '<line x1="260" y1="100" x2="260" y2="240" style="stroke:var(--dif);stroke-width:1.6"/>' + t(260, 260, 'destaque', size=10, anchor='middle', caps=True, fill='var(--dif)')
    o += say(40, 320, 'Os votos virtuais não são o resultado: os ministros')
    o += say(40, 344, 'podem votar de novo no presencial.')
    o += say(40, 388, 'Exceção (QO na ADI 5.399): quem votou e deixou o', 15, 'var(--conc)', True)
    o += say(40, 410, 'cargo tem o voto preservado; o sucessor não vota.', 15, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-dest-regra',
               label='Duas faixas: os votos do virtual param no destaque; o presencial recomeça o caso; exceção do voto preservado de quem deixou o cargo')


def placar():
    o = head('ADI 6200 · sessão de 11 a 18/09/2026')
    groups = [('Relator', ['Alexandre de Moraes'], 'square'), ('Divergem', ['Gilmar Mendes', 'Rosa Weber'], 'fill'),
              ('Acompanham a divergência', ['Nunes Marques', 'Edson Fachin', 'Luiz Fux'], 'ring')]
    y = 90
    for title, names, mark in groups:
        o += t(40, y, title, size=10.5, weight=700, caps=True)
        for k, n in enumerate(names):
            yy = y + 26 + k * 28
            if mark == 'square':
                o += f'<rect x="44" y="{yy - 12}" width="16" height="16" style="fill:var(--ink)"/>'
            elif mark == 'fill':
                o += f'<circle cx="52" cy="{yy - 4}" r="8" style="fill:var(--ink)"/>'
            else:
                o += f'<circle cx="52" cy="{yy - 4}" r="8" style="fill:none;stroke:var(--ink);stroke-width:2"/><circle cx="52" cy="{yy - 4}" r="3" style="fill:var(--ink)"/>'
            o += say(72, yy, n, 15)
        y += 40 + len(names) * 28
    o += say(40, y + 10, 'Um retrato daquele momento: os votos aparecem', 15, 'var(--conc)', True)
    o += say(40, y + 32, 'à medida que liberados; o resultado vem ao fechar.', 15, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-adi6200-placar',
               label='O placar parcial da ADI 6200 agrupado por posição: o relator Alexandre de Moraes; Gilmar Mendes e Rosa Weber divergem; Nunes Marques, Edson Fachin e Luiz Fux acompanham a divergência')


def stats():
    o = head('Julgados do Plenário · virtual e presencial')
    o += t(40, 84, '2024 · 7.632 virtuais · 82 presenciais', size=10.5, caps=True)
    o += dots(764, 44, 104, 50, step=10, r=3.4, partial=.2)
    o += dots(8, 44, 272, 8, step=10, r=3.4, filled=0, partial=0)
    o += t(40, 318, '2025 · 6.116 virtuais · 61 presenciais', size=10.5, caps=True)
    o += dots(612, 44, 338, 50, step=10, r=3.4, partial=.6)
    o += dots(6, 44, 476, 8, step=10, r=3.4, filled=0)
    o += key(40, 520, 'cheio: 10 virtuais · vazio: 10 presenciais')
    o += say(40, 556, '98,9% e 99,0% virtuais (virtual = total − presenciais).', 14, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='fig', ident='p-fig-stats',
               label='Dois campos de pontos, um ponto para cada dez julgados: em 2024, 764 cheios para os virtuais e 8 vazios para os presenciais; em 2025, 612 e 6')


def stats_inline():
    # an inline figure, not a scrolly panel: keep the page's block sizing
    return stats().replace('class="fig figkit"', 'class="fig figkit" style="display:block;width:100%;height:auto"', 1)


def panels():
    return [sistema(), carac(), dest_quem(), dest_regra(), placar(), stats_inline()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-27.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
