"""Controle Aula 09 · controle preventivo. The law's-life axis from Aula 10 (controle_a10) opens the lesson, so
the two lessons share one instrument; the House and the President act on the projeto as stamps on paper; art.
60, § 4º is text; the reach of judicial preventive control is a ruler (rito | matéria | interna corporis).
Position, not colour, says preventive vs repressive. Blue = what the control reaches; orange = its limit.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a16 import say
from controle_a10 import axis, head


def stamp(cx, cy, s, tone, angle=-6):
    w = len(s) * 9.2 + 28
    return (f'<g transform="rotate({angle} {cx} {cy})"><rect x="{cx - w / 2}" y="{cy - 17}" width="{w}" height="32" rx="3" style="fill:none;stroke:{tone};stroke-width:2.2"/>'
            + t(cx, cy + 5, s, size=12.5, anchor='middle', weight=700, caps=True, ls='.1em', fill=tone) + '</g>')


def paper(x, y, w, h, title):
    o = f'<path d="M{x} {y}H{x + w - 14}L{x + w} {y + 14}V{y + h}H{x}Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    o += t(x + 14, y + 26, title, size=10.5, weight=700, caps=True)
    o += ''.join(f'<line x1="{x + 14}" y1="{y + 46 + i * 14}" x2="{x + w - 24 - (i % 3) * 40}" y2="{y + 46 + i * 14}" style="stroke:var(--ink-2);stroke-width:1"/>' for i in range(4))
    return o


def defs():
    o = head('Dois momentos, um marco') + axis()
    o += say(40, 300, 'Preventivo: sobre o projeto, durante a formação;')
    o += say(40, 324, 'por regra, Legislativo e Executivo.', 16, 'var(--ink-2)')
    o += say(40, 368, 'Repressivo: sobre a lei, depois da formação;')
    o += say(40, 392, 'por regra, o Judiciário.', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p9-defs',
               label='O eixo da vida da lei: à esquerda da publicação, o controle preventivo sobre o projeto; à direita, o repressivo sobre a lei')


def linha():
    o = head('A formação concluída separa as fases') + axis(emph=True, vacatio=True)
    o += say(40, 320, 'Em formação: projeto e controle preventivo.')
    o += say(40, 344, 'Formado o ato: controle repressivo, mesmo antes da vigência.', 15, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p9-linha',
               label='O mesmo eixo com o marco destacado: concluída a formação, o controle passa a ser repressivo, ainda que a vigência venha depois')


def leg():
    o = head('Pelo Legislativo · CCJ e Plenário')
    o += paper(40, 70, 300, 120, 'Projeto de lei')
    o += stamp(250, 160, 'CCJ: inconstitucional', 'var(--conc)')
    o += say(360, 100, 'Decisão terminativa:', 15) + say(360, 122, 'rejeição e arquivamento.', 15, 'var(--ink-2)')
    o += say(40, 250, 'Recurso ao Plenário da Casa; no Senado,')
    o += say(40, 274, 'ao menos um décimo dos membros.', 16, 'var(--ink-2)')
    o += t(40, 330, 'Fora da CCJ', size=10.5, weight=700, caps=True)
    o += say(40, 358, 'Medidas provisórias, resoluções de tribunais, decretos.', 15)
    o += say(40, 400, 'CCJs: art. 58 da CF.', 15, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p9-leg',
               label='Um projeto de lei carimbado pela CCJ como inconstitucional: decisão terminativa, com recurso ao Plenário da Casa')


def veto():
    o = head('Pelo Executivo · art. 66, § 1º')
    o += paper(40, 70, 300, 120, 'Projeto aprovado')
    o += stamp(200, 230, 'veto jurídico', 'var(--ink)', -4) + say(330, 236, 'inconstitucional', 15)
    o += stamp(200, 300, 'veto político', 'var(--ink)', -4) + say(330, 306, 'contrário ao interesse público', 15)
    o += say(40, 400, 'O Presidente veta no todo ou em parte.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p9-veto',
               label='O projeto aprovado com dois carimbos possíveis do Presidente: veto jurídico, por inconstitucionalidade, e veto político, por contrariedade ao interesse público')


def fund():
    o = head('CF · art. 60, § 4º')
    o += '<rect x="40" y="70" width="520" height="190" style="fill:var(--paper-2);stroke:none"/><rect x="40" y="70" width="3" height="190" style="fill:var(--dif)"/>'
    o += say(58, 100, 'Não será objeto de deliberação a proposta de', 15) + say(58, 120, 'emenda tendente a abolir:', 15)
    for i, s in enumerate(['I · a forma federativa de Estado', 'II · o voto direto, secreto, universal e periódico', 'III · a separação dos Poderes', 'IV · os direitos e garantias individuais']):
        o += say(70, 152 + i * 24, s, 14)
    o += stamp(300, 320, 'deliberação vedada', 'var(--conc)')
    o += say(40, 400, 'Votar uma PEC assim ofende o direito do parlamentar')
    o += say(40, 424, 'ao processo legislativo hígido.', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p9-fund',
               label='O texto do art. 60, parágrafo 4º, com as quatro cláusulas pétreas, e o carimbo deliberação vedada')


def ms():
    o = head('Mandado de segurança · só do parlamentar')
    o += paper(40, 70, 330, 150, 'MS · impetrante: parlamentar')
    o += say(56, 200, 'contra a Mesa da Câmara ou do Senado', 14, 'var(--ink-2)', True)
    o += stamp(450, 150, 'legitimidade exclusiva', 'var(--dif)', -8)
    o += say(40, 300, 'Via incidental, em defesa de direito próprio.')
    o += say(40, 340, 'MS 20.257/DF, Min. Moreira Alves (leading case);', 15, 'var(--ink-2)')
    o += say(40, 362, 'MS 20.452/DF, Min. Aldir Passarinho.', 15, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p9-ms',
               label='Um mandado de segurança impetrado por parlamentar contra a Mesa, carimbado legitimidade exclusiva; MS 20.257 e 20.452')


def ruler(y, label, reach, fence=False):
    o = t(40, y - 12, label, size=10.5, weight=700, caps=True)
    segs = [(40, 220, 'rito constitucional'), (220, 400, 'matéria'), (400, 560, 'interna corporis')]
    for a, b, s in segs:
        o += f'<rect x="{a}" y="{y}" width="{b - a}" height="30" style="fill:var(--paper);stroke:var(--ink);stroke-width:1"/>' + t((a + b) / 2, y + 20, s, size=10, anchor='middle', caps=True, fill='var(--ink-2)')
    o += f'<rect x="40" y="{y + 36}" width="{reach - 40}" height="8" style="fill:var(--dif)"/>'
    if fence:
        o += f'<line x1="400" y1="{y - 6}" x2="400" y2="{y + 50}" style="stroke:var(--conc);stroke-width:2.6"/>'
    return o


def alcance():
    o = head('O alcance · MS 32.033/DF')
    o += ruler(110, 'PEC', 400) + ruler(220, 'Projeto de lei', 220)
    o += say(40, 340, 'PEC: o art. 60, § 4º veda a deliberação; o controle')
    o += say(40, 364, 'alcança a matéria. Projeto de lei: só o rito.', 16)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p9-alcance',
               label='Duas réguas de alcance: sobre a PEC, o controle vai do rito à matéria; sobre o projeto de lei, só o rito')


def limites():
    o = head('O limite · interna corporis')
    o += ruler(110, 'Controle judicial preventivo', 220, fence=True)
    o += say(40, 230, 'Garante o procedimento conforme a Constituição.')
    o += say(40, 274, 'Questões políticas e atos internos ficam fora;', 16, 'var(--conc)')
    o += say(40, 298, 'ler o regimento é, por regra, vedado (ponto controverso).', 15, 'var(--conc)', True)
    o += say(40, 352, 'MS 24.356/DF: arquivamento de denúncia por quebra', 15, 'var(--ink-2)')
    o += say(40, 374, 'de decoro; o Plenário não conheceu do MS.', 15, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p9-limites',
               label='A régua com uma cerca antes dos atos internos: o controle judicial preventivo cobre o rito constitucional e para no interna corporis')


TEXT = [
    ('Nesta aula e na próxima, <em class="dif">azul</em> marca o controle <em class="dif">preventivo</em>, antes de a lei existir, e <em class="conc">vermelho</em> marca o controle <em class="conc">repressivo</em>, depois.',
     'Nesta aula e na próxima, o eixo tem dois lados: à esquerda, o controle <em>preventivo</em>, antes de a lei existir; à direita, o controle <em>repressivo</em>, depois.'),
    ('ainda pelo lado azul do eixo,', 'ainda à esquerda do eixo,'),
]


def panels():
    return [defs(), linha(), leg(), veto(), fund(), ms(), alcance(), limites()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    path = 'courses/controle-de-constitucionalidade/aula-09.html'
    n = inject(path, {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    p = os.path.join(os.path.dirname(__file__), '..', '..', path)
    h = open(p).read()
    for a, b in TEXT:
        if a not in h and b not in h:
            raise SystemExit(f'text not found: {a[:50]}')
        h = h.replace(a, b)
    open(p, 'w').write(h)
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
