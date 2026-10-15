"""Controle Aula 12 · Crítica à cumulação. Ten panels, three families the course already uses:
the bench from Aula 11 (who may set a law aside), measured dot fields (one dot = 100 people or
decisions, so the STF's load is seen, not told), and the ledger. Ink only; blue marks what a court
decides, orange the limit. Numbers are the lesson's own.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
import controle_a11 as a11

SERIF = 'font-family:var(--serif,serif);fill:var(--ink)'


def say(x, y, s, size=18, italic=False, fill='var(--ink)', anchor='start'):
    st = f'font-family:var(--serif,serif);font-size:{size}px;fill:{fill}' + (';font-style:italic' if italic else '')
    a = '' if anchor == 'start' else f' text-anchor="{anchor}"'
    return f'<text x="{x}" y="{y}"{a} style="{st}">{s}</text>'


def head(s):
    return t(40, 46, s, size=11.5, weight=700, caps=True, ls='.12em')


def dots(n, x0, y0, cols, step=15, r=4.2, filled=None, partial=0.0):
    """n dots, row-major; `filled` = how many from the start are solid (default all); `partial` = fraction of the last dot."""
    filled = n if filled is None else filled
    o = []
    for i in range(n):
        x, y = x0 + (i % cols) * step, y0 + (i // cols) * step
        if i == n - 1 and partial:
            o.append(f'<circle cx="{x}" cy="{y}" r="{r:.2f}" style="fill:none;stroke:var(--ink);stroke-width:1"/>'
                     f'<path d="M{x} {y - r:.2f} A{r} {r} 0 0 1 {x} {y + r:.2f} Z" style="fill:var(--ink)"/>')
            continue
        st = 'fill:var(--ink)' if i < filled else 'fill:none;stroke:var(--ink);stroke-width:1'
        o.append(f'<circle cx="{x}" cy="{y}" r="{r}" style="{st}"/>')
    return ''.join(o)


def key(x, y, s):
    return f'<circle cx="{x}" cy="{y - 4}" r="4.2" style="fill:var(--ink)"/>' + t(x + 12, y, s, size=10.5, fill='var(--ink-2)', caps=True)


# ── 1 · Separação × cumulação ────────────────────────────────────────────────────────────────────────────
def panorama():
    return a11.bench('p-panorama', 'Concentrado + difuso = confuso', True, True, 'STF', 'Os dois sistemas no mesmo país.',
                     'A herança das duas tradições, somada.', 'A mesma lei: afastada aqui, aplicada ali.',
                     'Assentos de juízes e o STF, todos preenchidos: o Brasil soma o difuso e o concentrado')


def piramide():
    o = head('Modelo alemão · separação')
    for r in range(5):                                   # the ordinary courts: a pyramid of seats that do not judge laws
        n = 3 + r * 3
        for c in range(n):
            x = 200 - (n - 1) * 9 + c * 18
            o += f'<circle cx="{x}" cy="{250 + r * 26}" r="5.5" style="fill:none;stroke:var(--ink-2);stroke-width:1.2"/>'
    o += t(200, 400, 'Justiça comum', size=10.5, anchor='middle', caps=True, fill='var(--ink-2)')
    o += '<rect x="400" y="236" width="150" height="70" style="fill:var(--ink)"/>'
    o += t(475, 268, 'Tribunal', size=12, anchor='middle', weight=700, caps=True, fill='var(--paper)')
    o += t(475, 288, 'Constitucional', size=12, anchor='middle', weight=700, caps=True, fill='var(--paper)')
    o += '<line x1="370" y1="200" x2="370" y2="410" style="stroke:var(--ink);stroke-width:1;stroke-dasharray:3 5"/>'
    o += say(40, 470, 'Dois níveis, dois corpos de juízes.') + say(40, 500, 'O Tribunal Constitucional Federal não integra', 16, True, 'var(--ink-2)')
    o += say(40, 522, 'a Justiça comum.', 16, True, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-piramide',
               label='Modelo alemão: a Justiça comum, de assentos vazios, e o Tribunal Constitucional separado dela por uma linha')


def triangulo():
    o = head('Modelo brasileiro · cumulação')
    for r in range(6):
        n = 1 + r * 3
        for c in range(n):
            x = 300 - (n - 1) * 9 + c * 18
            if r == 0:
                o += '<rect x="270" y="150" width="60" height="26" style="fill:var(--ink)"/>' + t(300, 168, 'STF', size=12, anchor='middle', weight=700, fill='var(--paper)')
            else:
                o += f'<circle cx="{x}" cy="{170 + r * 30}" r="5.5" style="fill:var(--ink)"/>'
    o += t(300, 360, 'Jurisdição ordinária e constitucional', size=10.5, anchor='middle', caps=True, fill='var(--ink-2)')
    o += say(40, 450, 'Um só triângulo, um só corpo de juízes.') + say(40, 480, 'Qualquer juiz comum também é juiz constitucional.', 16, True, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-triangulo',
               label='Modelo brasileiro: um só triângulo de juízes com o STF no topo, todos preenchidos; qualquer juiz comum também controla a constitucionalidade')


# ── 2 · A cumulação em números e em um caso real ─────────────────────────────────────────────────────────
def juizes():
    o = head('Poder Judiciário · 2025')
    o += t(40, 82, '19.094 juízes, desembargadores e ministros', size=11, caps=True)
    o += dots(191, 46, 112, 20, step=25, r=6.2, partial=.94)        # 19.094 / 100 = 190,94
    o += key(40, 400, 'um ponto = 100 magistrados')
    o += say(40, 450, 'Cada um pode, sozinho, afastar a lei no caso.')
    o += say(40, 490, '“Cada juiz é um tribunal constitucional.”', 17, True, 'var(--ink-2)')
    o += say(40, 530, 'E quando vários decidem de forma diferente?', 17, False, 'var(--conc)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-juizes',
               label='191 pontos, cada um cem magistrados: os 19.094 juízes do país, cada um capaz de afastar uma lei no caso concreto')


def whatsapp():
    o = head('Exemplo real · bloqueio do WhatsApp')
    rows = [('Comarca A', 'liberado'), ('Comarca B', 'bloqueado'), ('Comarca C', 'proibido'), ('Comarca D', 'liberado')]
    for i, (c, s) in enumerate(rows):
        y = 110 + i * 78
        o += f'<rect x="40" y="{y}" width="520" height="60" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.3"/>'
        o += t(60, y + 36, c, size=12, weight=700, caps=True)
        o += f'<g transform="rotate(-4 430 {y + 30})"><rect x="{430 - 72}" y="{y + 14}" width="144" height="32" rx="3" style="fill:none;stroke:var(--ink);stroke-width:2"/>'
        o += t(430, y + 36, s, size=14, anchor='middle', weight=700, caps=True, ls='.16em') + '</g>'
    o += say(40, 470, 'O mesmo aplicativo, quatro decisões,') + say(40, 498, 'ao mesmo tempo, no mesmo país.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-whatsapp',
               label='Quatro comarcas, quatro carimbos: o mesmo aplicativo liberado, bloqueado, proibido e liberado ao mesmo tempo')


# ── 3 · Constituição sintética e carga seletiva ─────────────────────────────────────────────────────────
def sintetica():
    o = head('Constituição americana · 1787')
    for i in range(7):
        o += f'<rect x="{40 + i * 30}" y="110" width="22" height="80" style="fill:var(--ink)"/>'
    o += t(40, 216, '7 artigos', size=11, caps=True)
    for i in range(27):
        x = 300 + (i % 9) * 28; y = 110 + (i // 9) * 28
        st = 'fill:var(--ink)' if i < 10 else 'fill:none;stroke:var(--ink);stroke-width:1.2'
        o += f'<rect x="{x}" y="{y}" width="18" height="18" style="{st}"/>'
    o += t(300, 216, '27 emendas · 10 = Bill of Rights', size=11, caps=True)
    o += say(40, 300, 'Curta, escrita e em vigor desde 1787.')
    o += say(40, 340, 'Pouco assunto constitucional no dia a dia forense:')
    o += say(40, 368, 'poucos casos difusos sobem.', 18, True, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-sintetica',
               label='Sete artigos e vinte e sete emendas, dez delas o Bill of Rights: uma Constituição curta, que gera poucos casos constitucionais')


def certiorari():
    o = head('Quantos casos cada corte decide')
    o += t(40, 92, 'Suprema Corte dos EUA · OT 2024 · 9 juízes', size=11, caps=True)
    o += dots(1, 46, 122, 1, r=6.2, partial=.8)
    o += say(70, 128, '~80 casos escolhidos entre +5.000 petições', 16)
    o += t(40, 186, 'Alemanha · BVerfG · 16 juízes', size=11, caps=True)
    o += dots(60, 46, 214, 20, step=25, r=6.2)
    o += say(40, 310, '~6.000 processos por ano', 16)
    o += key(40, 360, 'um ponto = 100 casos')
    o += say(40, 420, 'Mais juízes, mais processos;')
    o += say(40, 450, 'nenhum dos dois se compara ao STF.', 18, True, 'var(--conc)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-certiorari',
               label='Um ponto para cada cem casos: menos de um ponto para a Suprema Corte americana, sessenta para o Tribunal Constitucional alemão')


# ── 4 · O volume decisório do STF: the same field, growing a step ────────────────────────────────────────
def stf_field(ident, mono, label, lines):
    o = head('STF em 2025 · 11 ministros')
    n = 1162                                              # 116.170 / 100
    o += dots(n, 44, 92, 42, step=12.4, r=4.1, filled=mono if mono else n)
    o += key(40, 492, 'um ponto = 100 decisões')
    for i, (s, size, it, fill) in enumerate(lines):
        o += say(40, 528 + i * 28, s, size, it, fill)
    return svg('0 0 600 600', o, cls='panel fig on', ident=ident, label=label)


def stfnum():
    return stf_field('p-stfnum', None,
                     'Mil cento e sessenta e dois pontos: as 116.170 decisões do STF em 2025, contra 85.201 processos recebidos',
                     [('116.170 decisões; 85.201 entradas: 38% originárias, 62% recursais.', 15, False, 'var(--ink)')])


def monocratica():
    return stf_field('p-monocratica', 936,
                     'O mesmo campo de decisões do STF: 936 pontos cheios são as 93.559 decisões monocráticas, 80,5% do total',
                     [('Cheios: 93.559 decisões de um ministro sozinho (80,5%).', 15, False, 'var(--ink)'),
                      ('Vazios: as colegiadas (19,5%).', 15, True, 'var(--ink-2)')])


# ── 5 · O balanço: the ledger, in ink ─────────────────────────────────────────────────────────────────────
def sintese():
    o = head('Duas vias · um modelo misto')
    o += '<line x1="40" y1="120" x2="560" y2="120" style="stroke:var(--ink);stroke-width:1.5"/><line x1="300" y1="86" x2="300" y2="300" style="stroke:var(--ink);stroke-width:1"/>'
    o += t(40, 108, 'Concentrado', size=11, weight=700, caps=True) + t(320, 108, 'Difuso', size=11, weight=700, caps=True)
    o += say(40, 160, 'Um órgão rejeita a lei', 17) + say(320, 160, 'Cada juiz afasta a norma', 17)
    o += say(40, 190, 'para todos.', 17) + say(320, 190, 'no seu caso.', 17)
    o += '<line x1="40" y1="250" x2="560" y2="250" style="stroke:var(--ink);stroke-width:1"/>'
    o += t(40, 280, 'Saldo · segurança', size=11, caps=True, fill='var(--dif)') + t(320, 280, 'Saldo · incerteza', size=11, caps=True, fill='var(--conc)')
    o += '<line x1="40" y1="330" x2="560" y2="330" style="stroke:var(--ink);stroke-width:2.2"/>'
    o += t(40, 366, 'Cumulação', size=12, weight=700, caps=True)
    o += say(40, 400, 'Fragmentação e guerra de liminares.', 18)
    o += say(40, 460, 'A resposta: aproximar o difuso do concentrado.', 17, True, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-sintese',
               label='Livro-caixa das duas vias: o concentrado dá segurança, o difuso incerteza; a cumulação fragmenta, e a saída é aproximar o difuso do concentrado')


def panels():
    return [panorama(), piramide(), triangulo(), juizes(), whatsapp(), sintetica(), certiorari(), stfnum(), monocratica(), sintese()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-12.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
