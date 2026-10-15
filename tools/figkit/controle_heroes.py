"""Controle Aulas 30–36 · hero strips (1080 × 150) from the house families. 30 and 31 had hand-drawn heroes
that named categories by colour; 32–36 had none. Each strip answers the lesson's own question in one line
of drawing. Inserted after the deck when the page has no hero-fork; replaced in place otherwise.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, t

W, H = 1080, 150


def frame(inner, label):
    return (f'<svg class="hero-fork figkit" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">{inner}</svg>')


def sheet(x, y, w, h, title, dashed=False):
    st = 'fill:none;stroke:var(--ink-2);stroke-width:1.4;stroke-dasharray:6 5' if dashed else 'fill:var(--paper);stroke:var(--ink);stroke-width:1.4'
    o = f'<path d="M{x} {y}H{x + w - 12}L{x + w} {y + 12}V{y + h}H{x}Z" style="{st}"/>'
    o += t(x + 12, y + 22, title, size=11, weight=700, caps=True, fill='var(--ink-2)' if dashed else 'var(--ink)')
    if not dashed:
        o += ''.join(f'<line x1="{x + 12}" y1="{y + 38 + i * 11}" x2="{x + w - 20 - (i % 2) * 30}" y2="{y + 38 + i * 11}" style="stroke:var(--ink-2);stroke-width:1"/>' for i in range(max(0, (h - 46) // 11)))
    return o


def stamp(cx, cy, s, tone, size=12, angle=-5):
    w = len(s) * size * .74 + 22
    return (f'<g transform="rotate({angle} {cx} {cy})"><rect x="{cx - w / 2:.1f}" y="{cy - size - 3}" width="{w:.1f}" height="{size * 2 + 4}" rx="3" style="fill:none;stroke:{tone};stroke-width:2"/>'
            + t(cx, cy + size * .4, s, size=size, anchor='middle', weight=700, caps=True, ls='.1em', fill=tone) + '</g>')


def tick(x, y, on=True):
    o = f'<rect x="{x}" y="{y - 15}" width="20" height="20" style="fill:none;stroke:var(--ink);stroke-width:1.4"/>'
    return o + (f'<path d="M{x + 4} {y - 5} l5 6 l10 -14" style="fill:none;stroke:var(--ink);stroke-width:2.2"/>' if on else '')


def h30():
    o = sheet(20, 30, 200, 96, 'Lei federal')
    for i in range(6):
        x = 260 + i * 92
        o += sheet(x, 34, 80, 54, f'juízo {i + 1}')
        o += stamp(x + 40, 112, 'aplica' if i % 2 == 0 else 'afasta', 'var(--ink)', size=10, angle=-4 + (i % 3) * 3)
    o += stamp(950, 76, 'resposta única', 'var(--dif)', size=13)
    o += t(950, 120, 'ADC · alcance geral', size=10.5, anchor='middle', caps=True, fill='var(--dif)')
    return frame(o, 'Uma lei federal e seis juízos que a aplicam e a afastam alternadamente; a ADC no STF dá uma resposta única, com alcance geral')


def h31():
    o = sheet(20, 30, 220, 96, 'A norma que não veio', dashed=True)
    o += t(270, 58, 'ADO', size=13, weight=700, caps=True) + t(330, 58, 'a omissão frustra a Constituição, em abstrato', size=11.5)
    o += t(270, 108, 'MI', size=13, weight=700, caps=True) + t(330, 108, 'o direito de alguém está bloqueado, agora', size=11.5)
    o += '<path d="M244 52 H262 M244 102 H262" style="stroke:var(--ink);stroke-width:1.4"/>'
    o += t(900, 84, 'quem precisa da resposta?', size=11.5, anchor='middle', caps=True, fill='var(--ink-2)')
    return frame(o, 'Uma folha tracejada, a norma que não veio, abre dois caminhos: a ADO para a omissão em abstrato; o mandado de injunção para o direito bloqueado')


def h32():
    o = ''
    for i, s in enumerate(['ato do poder público', 'lesão a preceito fundamental', 'nenhum outro meio eficaz']):
        x = 20 + i * 300
        o += tick(x, 84) + t(x + 32, 84, s, size=12)
    o += stamp(990, 80, 'ADPF', 'var(--dif)', size=15)
    o += t(20, 130, 'subsidiariedade: falta qualquer caixa, a via é outra', size=10.5, caps=True, fill='var(--conc)')
    return frame(o, 'Três caixas marcadas, ato do poder público, lesão a preceito fundamental e nenhum outro meio eficaz, e o carimbo ADPF')


def h33():
    o = t(20, 40, 'STF', size=12, weight=700, caps=True) + t(560, 40, 'Presidente da República', size=12, weight=700, caps=True)
    o += '<line x1="540" y1="24" x2="540" y2="140" style="stroke:var(--ink-2);stroke-width:1"/>'
    o += sheet(20, 54, 220, 76, 'Representação · PGR')
    o += stamp(380, 92, 'violação constatada', 'var(--dif)', size=11)
    o += sheet(560, 54, 200, 76, 'Decreto')
    o += stamp(900, 92, 'medida mínima', 'var(--conc)', size=11)
    return frame(o, 'Duas colunas: no STF, a representação do PGR e a violação constatada; com o Presidente, o decreto e a medida mínima que restaura a normalidade')


def h34():
    o = t(20, 32, 'Lei X · art. 1º', size=11, weight=700, caps=True)
    cols = [('o texto', 'redução de texto'), ('um sentido', 'sem redução / conforme'), ('o tempo', 'modulação')]
    for i, (what, how) in enumerate(cols):
        x = 20 + i * 360
        o += f'<rect x="{x}" y="48" width="330" height="40" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>'
        o += t(x + 12, 73, 'Fica autorizada a licença L…', size=12)
        if i == 0:
            o += f'<line x1="{x + 140}" y1="69" x2="{x + 216}" y2="69" style="stroke:var(--dif);stroke-width:2.4"/>'
        elif i == 1:
            o += f'<rect x="{x + 230}" y="52" width="94" height="32" style="fill:none;stroke:var(--dif);stroke-width:1.8;stroke-dasharray:4 3"/>'
        else:
            o += f'<line x1="{x + 250}" y1="44" x2="{x + 250}" y2="94" style="stroke:var(--dif);stroke-width:2.4"/>'
        o += t(x, 118, f'muda {what}', size=11, weight=700, caps=True) + t(x, 136, how, size=10.5, fill='var(--ink-2)')
    return frame(o, 'O mesmo artigo três vezes: palavras riscadas, redução de texto; um sentido recortado, sem redução; uma marca no tempo, modulação')


def h35():
    o = sheet(20, 30, 260, 96, 'Constituição do Estado')
    o += '<path d="M290 78 H360" style="stroke:var(--ink);stroke-width:1.6"/><path d="M354 73 l7 5 l-7 5" style="fill:none;stroke:var(--ink);stroke-width:1.6"/>'
    o += sheet(372, 46, 180, 64, 'Tribunal de Justiça')
    o += t(372, 136, 'ADI estadual · parâmetro local', size=10.5, caps=True, fill='var(--ink-2)')
    o += sheet(600, 30, 270, 96, 'Reprodução obrigatória da CF')
    o += '<path d="M880 78 H920" style="stroke:var(--dif);stroke-width:1.6;stroke-dasharray:5 4"/><path d="M914 73 l7 5 l-7 5" style="fill:none;stroke:var(--dif);stroke-width:1.6"/>'
    o += stamp(990, 78, 'RE ao STF', 'var(--dif)', size=12)
    return frame(o, 'A Constituição do Estado leva ao Tribunal de Justiça; só quando o parâmetro reproduz obrigatoriamente a Constituição Federal cabe recurso extraordinário ao STF')


def h36():
    o = t(20, 34, 'Câmara · órgão fracionário', size=11, weight=700, caps=True)
    o += ''.join(f'<circle cx="{40 + i * 34}" cy="80" r="12" style="fill:none;stroke:var(--ink);stroke-width:1.5"/>' for i in range(3))
    o += t(20, 128, 'afasta a lei? não sozinha', size=10.5, caps=True, fill='var(--conc)')
    o += '<path d="M180 80 H300" style="stroke:var(--ink);stroke-width:1.4;stroke-dasharray:5 4"/>' + t(240, 70, 'incidente', size=10, anchor='middle', caps=True)
    o += t(320, 34, 'Plenário ou órgão especial · art. 97', size=11, weight=700, caps=True)
    o += ''.join(f'<circle cx="{334 + (i % 13) * 30}" cy="{68 + (i // 13) * 26}" r="10" style="fill:var(--ink)"/>' for i in range(25))
    o += t(320, 136, 'declara a inconstitucionalidade', size=10.5, caps=True, fill='var(--dif)')
    o += t(1060, 80, 'salvo decisão anterior', size=10.5, anchor='end', caps=True, fill='var(--ink-2)')
    o += t(1060, 98, 'do tribunal ou do STF', size=10.5, anchor='end', caps=True, fill='var(--ink-2)')
    return frame(o, 'Três assentos da câmara não afastam a lei sozinhos; pelo incidente, o plenário ou órgão especial, assentos cheios, declara a inconstitucionalidade, salvo decisão anterior')


HEROES = {30: h30, 31: h31, 32: h32, 33: h33, 34: h34, 35: h35, 36: h36}


def hero_n(n):
    def deco(f):
        HEROES[n] = f
        return f
    return deco


# ── 15/10 · Aulas 03–29: the hero previews the lesson's instrument (the old strips coded categories by colour) ──
def psheet(x, y, w, h, title, dashed=False):
    # plain paper for strips that write on the sheet (no filler lines through the labels)
    st = 'fill:none;stroke:var(--ink-2);stroke-width:1.4;stroke-dasharray:6 5' if dashed else 'fill:var(--paper);stroke:var(--ink);stroke-width:1.4'
    return f'<path d="M{x} {y}H{x + w - 12}L{x + w} {y + 12}V{y + h}H{x}Z" style="{st}"/>' + t(x + 12, y + 22, title, size=11, weight=700, caps=True)


INK, DIF, CONC, MUTED = 'var(--ink)', 'var(--dif)', 'var(--conc)', 'var(--ink-2)'


def m(x, y, s, fill=INK, size=11, anchor='start', bold=False):
    return t(x, y, s, size=size, caps=True, anchor=anchor, fill=fill, weight=700 if bold else 500)


def ser(x, y, s, size=14, fill=INK, anchor='start'):
    a = '' if anchor == 'start' else f' text-anchor="{anchor}"'
    return f'<text x="{x}" y="{y}"{a} style="font-family:var(--serif,serif);font-size:{size}px;fill:{fill}">{s}</text>'


def box(x, y, w, h, fill='var(--paper)', stroke=INK, dash=False):
    d = ';stroke-dasharray:5 4' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" style="fill:{fill};stroke:{stroke};stroke-width:1.3{d}"/>'


def arr(x1, x2, y, tone=INK, dash=False):
    d = ';stroke-dasharray:5 4' if dash else ''
    return f'<path d="M{x1} {y} H{x2 - 6}" style="stroke:{tone};stroke-width:1.5{d}"/><path d="M{x2 - 8} {y - 5} l7 5 l-7 5" style="fill:none;stroke:{tone};stroke-width:1.5"/>'


def track(x0, x1, y, segs, label=''):
    o = m(x0, y - 8, label, MUTED, 10) if label else ''
    for a, b, k in segs:
        st = {'on': f'fill:{INK}', 'off': 'fill:none;stroke:var(--ink);stroke-width:1.1;stroke-dasharray:4 4', 'dec': f'fill:{DIF}'}[k]
        o += f'<rect x="{a}" y="{y}" width="{b - a}" height="16" style="{st}"/>'
    return o


def law_axis(mark_right=False):
    o = f'<rect x="20" y="58" width="520" height="34" style="fill:var(--paper-2)"/>' + box(540, 58, 520, 34)
    o += '<line x1="20" y1="75" x2="1060" y2="75" style="stroke:var(--ink);stroke-width:1.4"/>'
    for x, s in ((80, 'projeto'), (240, 'votação'), (400, 'sanção')):
        o += f'<line x1="{x}" y1="69" x2="{x}" y2="81" style="stroke:var(--ink)"/>' + t(x, 112, s, size=10, anchor='middle', fill=MUTED)
    o += f'<line x1="540" y1="36" x2="540" y2="100" style="stroke:var(--ink);stroke-width:{4 if mark_right else 3}"/>' + m(540, 28, 'publicação', anchor='middle', bold=True)
    o += m(280, 50, 'preventivo', anchor='middle') + m(800, 50, 'repressivo', anchor='middle')
    return o


@hero_n(3)
def _():
    o = m(20, 28, 'quem guarda a Constituição?', bold=True)
    o += '<line x1="540" y1="40" x2="540" y2="140" style="stroke:var(--ink-2)"/>' + '<line x1="20" y1="58" x2="1060" y2="58" style="stroke:var(--ink);stroke-width:1.4"/>'
    o += m(20, 50, 'Hans Kelsen', size=12, bold=True) + m(560, 50, 'Carl Schmitt', size=12, bold=True)
    o += ser(20, 92, 'um tribunal constitucional independente', 16) + ser(560, 92, 'o chefe de Estado', 16)
    o += m(20, 132, 'sete rodadas, uma coluna por voz', MUTED, 10.5)
    return frame(o, 'Duas colunas: Kelsen, um tribunal constitucional; Schmitt, o chefe de Estado')


@hero_n(6)
def _():
    o = psheet(20, 18, 420, 118, 'Lei X')
    o += box(28, 46, 404, 22, 'none', CONC) + m(36, 61, 'iniciativa · votação · sanção', MUTED, 10)
    o += m(480, 62, 'formal · o caminho', bold=True) + m(480, 112, 'material · o conteúdo', bold=True)
    o += box(28, 80, 404, 48, 'none', CONC)
    o += arr(444, 474, 57, CONC) + arr(444, 474, 105, CONC)
    o += m(1060, 140, 'por ação · por omissão', MUTED, 10.5, 'end')
    return frame(o, 'A folha de uma lei com dois lugares do defeito: a faixa do caminho, vício formal; o corpo, vício material')


@hero_n(7)
def _():
    o = '<line x1="20" y1="80" x2="1060" y2="80" style="stroke:var(--ink-2)"/><line x1="540" y1="34" x2="540" y2="126" style="stroke:var(--ink);stroke-width:3"/>' + m(540, 26, 'CF/1988', anchor='middle', bold=True)
    o += m(280, 64, 'norma anterior', anchor='middle', bold=True) + ser(280, 104, 'recepção ou não recepção', 15, anchor='middle')
    o += m(800, 64, 'norma posterior', anchor='middle', bold=True) + ser(800, 104, 'constitucional ou não', 15, anchor='middle')
    return frame(o, 'O marco de 1988: normas anteriores são recebidas ou não; posteriores, constitucionais ou não')


@hero_n(9)
def _():
    o = law_axis() + m(20, 140, 'o projeto, antes de existir a lei: Legislativo e Executivo', MUTED, 10.5)
    return frame(o, 'O eixo da vida da lei: à esquerda da publicação, o controle preventivo sobre o projeto')


@hero_n(10)
def _():
    o = law_axis(True) + m(1060, 140, 'a lei existe: Judiciário (regra) · Legislativo, Justiça Eleitoral', MUTED, 10.5, 'end')
    return frame(o, 'O mesmo eixo: à direita da publicação, o controle repressivo sobre a lei que já existe')


@hero_n(11)
def _():
    for i, (title, at) in enumerate([('Via principal · STF', 2), ('Via incidental · A × B', 1)]):
        x = 20 + i * 400
        o = (o if i else '') + psheet(x, 14, 360, 124, title)
        for k, s in enumerate(['fatos', 'direito', 'pedidos']):
            y = 54 + k * 26
            o += m(x + 14, y + 4, s, MUTED, 10)
            if k == at:
                o += box(x + 8, y - 10, 344, 22, 'none', INK)
    o += m(1060, 70, 'onde está a questão', MUTED, 10.5, 'end') + m(1060, 92, 'constitucional?', MUTED, 10.5, 'end')
    return frame(o, 'Duas petições: na ação direta a questão está no pedido; na ação entre A e B, no direito')


@hero_n(12)
def _():
    o = m(20, 28, 'decisões em um ano · um ponto = 1.000', MUTED, 10.5)
    rows = [('STF · 2025 · 116.170', 116), ('BVerfG · ~6.000', 6), ('Suprema Corte dos EUA · ~80', 0)]
    for i, (lab, n) in enumerate(rows):
        y = 52 + i * 36
        o += m(20, y + 4, lab, size=10.5)
        o += ''.join(f'<circle cx="{300 + k * 6.6:.1f}" cy="{y}" r="2.5" style="fill:var(--ink)"/>' for k in range(n))
        if n == 0:
            o += f'<circle cx="300" cy="{y}" r="2.5" style="fill:none;stroke:var(--ink)"/>'
    return frame(o, 'Três fileiras de pontos, um ponto para cada mil decisões: o STF com 116, o tribunal alemão com 6, a Suprema Corte americana com menos de um')


@hero_n(13)
def _():
    X = lambda y: 60 + (y - 1995) * 34
    o = '<line x1="40" y1="80" x2="1060" y2="80" style="stroke:var(--ink);stroke-width:1.4"/>'
    for y, top, sub, tone, dash in [(1997, 'Colômbia', 'origem', INK, False), (2015.7, 'ADPF 347', 'prisional · 09/09/2015', DIF, False), (2022.4, 'ADPF 976', 'situação de rua', DIF, False)]:
        o += f'<circle cx="{X(y):.0f}" cy="80" r="6" style="fill:{tone}"/>' + m(X(y), 62, top, tone, 10.5, 'middle', True) + t(X(y), 104, sub, size=10, anchor='middle', fill=MUTED)
    o += m(1060, 140, 'três requisitos, todos ao mesmo tempo', MUTED, 10.5, 'end')
    return frame(o, 'Linha do tempo do estado de coisas inconstitucional: Colômbia, ADPF 347 em 2015, ADPF 976 em 2022')


@hero_n(14)
def _():
    o = psheet(20, 16, 330, 60, 'Lei X') + f'<line x1="30" y1="58" x2="340" y2="58" style="stroke:{DIF};stroke-width:2.4"/>'
    o += psheet(20, 86, 330, 56, 'Decreto Y') + f'<line x1="30" y1="122" x2="340" y2="122" style="stroke:{DIF};stroke-width:2.4;stroke-dasharray:7 5"/>'
    o += psheet(420, 86, 300, 56, 'Lei W · mesmo assunto')
    o += m(760, 52, 'declarada', DIF, 11) + m(760, 122, 'arrastado · fica', DIF, 11)
    return frame(o, 'A Lei X riscada; o Decreto Y, que depende dela, riscado com ela, tracejado; a Lei W, do mesmo assunto, fica')


@hero_n(15)
def _():
    o = box(20, 14, 1040, 34) + m(32, 36, 'texto · art. N', MUTED, 10.5)
    o += box(20, 62, 1040, 78, 'none', CONC) + m(28, 58, 'o sentido possível do texto', CONC, 9.5)
    for i, (h, s, struck) in enumerate([('leitura 1', 'compatível', False), ('leitura 2', 'compatível', False), ('leitura 3', 'colide', True)]):
        x = 60 + i * 330
        o += box(x, 80, 280, 44) + m(x + 10, 98, h, size=10, bold=True) + ser(x + 10, 116, s, 13)
        if struck:
            o += f'<line x1="{x - 4}" y1="102" x2="{x + 284}" y2="102" style="stroke:{DIF};stroke-width:2.4"/>'
    return frame(o, 'O texto, a moldura do sentido possível e três leituras: só a que colide é riscada')


@hero_n(16)
def _():
    o = '<line x1="60" y1="84" x2="1020" y2="84" style="stroke:var(--ink);stroke-width:2"/>'
    for x, s, a in ((60, 'plena', 'start'), (540, 'imperfeita', 'middle'), (1020, 'total', 'end')):
        o += f'<line x1="{x}" y1="76" x2="{x}" y2="92" style="stroke:var(--ink);stroke-width:1.5"/>' + t(x, 116, s, size=11, caps=True, anchor=a, fill=MUTED)
    o += '<path d="M300 58 L320 58 L310 74 Z" style="fill:var(--ink)"/>' + m(310, 46, 'ainda constitucional', anchor='middle', bold=True) + arr(334, 420, 66, CONC)
    o += m(1060, 146, 'circunstancial: validade inteira, aplicação suspensa', MUTED, 10.5, 'end')
    return frame(o, 'A régua de plena constitucionalidade a total inconstitucionalidade, com o marcador ainda constitucional que só anda num sentido')


@hero_n(17)
def _():
    o = '<circle cx="60" cy="96" r="10" style="fill:var(--ink)"/>' + box(900, 76, 140, 40, 'none', CONC) + m(970, 101, 'efeito vedado', CONC, 10.5, 'middle')
    o += '<path d="M72 96 H520" style="stroke:var(--ink);stroke-width:2"/><rect x="522" y="74" width="10" height="44" style="fill:var(--conc)"/>'
    o += '<path d="M66 86 C 260 10, 700 10, 898 90" style="fill:none;stroke:var(--ink);stroke-width:1.6;stroke-dasharray:6 5"/>' + box(430, 18, 120, 30) + m(490, 38, 'o ato', anchor='middle', bold=True)
    return frame(o, 'Duas rotas até o efeito vedado: a direta, bloqueada; a indireta, tracejada, pelo ato interposto')


@hero_n(18)
def _():
    o = box(20, 14, 1040, 34) + m(32, 36, 'texto constitucional · intocado', MUTED, 10.5)
    for i, s in enumerate(['1988', 'depois', 'hoje']):
        o += box(60 + i * 220, 66, 190, 40) + m(70 + i * 220, 90, f'leitura · {s}', size=10.5)
    o += m(760, 92, 'reação', size=10.5) + ''.join(f'<line x1="{840 + k * 9}" y1="78" x2="{840 + k * 9}" y2="104" style="stroke:var(--ink);stroke-width:2.4"/>' for k in range(4))
    o += m(1060, 140, 'muda o sentido, não o texto', MUTED, 10.5, 'end')
    return frame(o, 'O texto fixo e suas leituras em 1988, depois e hoje; ao lado, as marcas de uma reação social')


@hero_n(19)
def _():
    o = m(20, 26, 'STF', bold=True) + m(560, 26, 'Congresso Nacional', bold=True) + '<line x1="540" y1="14" x2="540" y2="146" style="stroke:var(--ink-2)"/>'
    o += box(20, 44, 300, 40) + m(32, 69, 'decide · a lei é inconstitucional', DIF, 10.5)
    o += box(560, 44, 240, 40) + m(572, 69, 'reage · lei ordinária', size=10.5) + box(820, 44, 240, 40) + m(832, 69, 'reage · emenda', size=10.5)
    o += box(20, 100, 300, 40, 'none', MUTED, True) + m(32, 125, 'novo controle', MUTED, 10.5)
    return frame(o, 'Partitura de duas colunas: o STF decide; o Congresso reage por lei ordinária ou emenda; segue novo controle')


@hero_n(20)
def _():
    o = ''
    for i, s in enumerate(['forma', 'espécie · art. 59', 'abstração']):
        o += tick(20 + i * 200, 70) + ser(50 + i * 200, 70, s, 15)
    o += '<path d="M640 30 V130 H820 V30" style="fill:none;stroke:var(--dif);stroke-width:2"/>' + m(650, 24, 'cabe ADI', DIF, 10.5, bold=True)
    o += '<path d="M860 30 V130 H1040 V30" style="fill:none;stroke:var(--conc);stroke-width:2"/>' + m(870, 24, 'não cabe', CONC, 10.5, bold=True)
    o += m(660, 120, 'leis · MP · EC', size=10) + m(880, 120, 'PEC · pré-CF', size=10)
    return frame(o, 'Três caixas do cabimento, forma, espécie e abstração, e duas bandejas: cabe ADI, não cabe')


@hero_n(21)
def _():
    o = psheet(20, 14, 600, 124, 'ADI · petição inicial')
    o += m(36, 64, 'pedido', MUTED, 10) + ser(150, 64, 'inconstitucionalidade da Lei X', 14) + m(560, 64, 'fechado', CONC, 10, 'end')
    o += m(36, 104, 'fundamento', MUTED, 10) + ser(150, 104, 'art. Z … ou art. Y', 14) + m(560, 104, 'aberto', DIF, 10, 'end')
    o += m(1060, 140, 'exceção: arrastamento', MUTED, 10.5, 'end')
    return frame(o, 'Uma petição de ADI: o pedido é fechado, o fundamento é aberto')


def doors(locks=(), x0=20, y=30):
    o = ''
    for i, r in enumerate(['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']):
        x = x0 + i * 56
        o += f'<path d="M{x} {y + 70}V{y + 10}Q{x + 20} {y - 6} {x + 40} {y + 10}V{y + 70}" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
        if i in locks:
            o += f'<rect x="{x + 13}" y="{y + 34}" width="14" height="11" style="fill:none;stroke:var(--conc);stroke-width:1.6"/>'
        o += t(x + 20, y + 88, r, size=10, anchor='middle', fill=MUTED)
    return o


@hero_n(22)
def _():
    o = doors() + m(560, 52, 'I–VII · assinam a inicial', DIF, 11) + m(560, 84, 'VIII–IX · precisam de advogado', CONC, 11)
    o += m(1060, 140, 'art. 103 · nove legitimados', MUTED, 10.5, 'end')
    return frame(o, 'Nove portas do art. 103: de I a VII assinam a inicial; VIII e IX precisam de advogado')


@hero_n(23)
def _():
    o = doors(locks=(3, 4, 8)) + m(560, 52, 'abertas · interesse presumido', size=11) + m(560, 84, 'com fechadura · provar pertinência', CONC, 11)
    return frame(o, 'Nove portas do art. 103: seis abertas, três com fechadura, a pertinência temática')


@hero_n(24)
def _():
    o = ''
    for i, s in enumerate(['ajuizamento', 'cautelar', 'mérito', 'julgamento']):
        o += box(20 + i * 150, 36, 136, 34, INK if s != 'cautelar' else 'var(--paper)') + m(30 + i * 150, 58, s, 'var(--paper)' if s != 'cautelar' else INK, 10)
    o += m(20, 100, 'rito ordinário', MUTED, 10.5)
    o += box(660, 36, 200, 34, 'none') + m(670, 58, '10 + 5 + 5 dias', size=10) + box(870, 30, 190, 46, DIF, DIF) + m(965, 58, 'cautelar + mérito', 'var(--paper)', 10, 'middle')
    o += m(660, 100, 'rito abreviado · art. 12', DIF, 10.5)
    return frame(o, 'O rito ordinário em quatro etapas e o abreviado: informações e manifestações em vinte dias, cautelar e mérito fundidos')


@hero_n(25)
def _():
    o = track(20, 1060, 64, [(20, 420, 'on'), (420, 760, 'dec'), (760, 1060, 'off')], 'a lei objeto da ADI')
    o += m(420, 110, 'cautelar · suspende', DIF, 10.5) + m(760, 110, 'mérito · retira', size=10.5)
    o += m(1060, 146, '8 presentes para a sessão · 6 votos para conceder', MUTED, 10.5, 'end')
    return frame(o, 'A faixa da lei: a cautelar a suspende, em azul; o mérito a retira; quóruns de oito e seis')


@hero_n(26)
def _():
    o = track(20, 1060, 44, [(20, 360, 'on'), (360, 700, 'off'), (700, 1060, 'dec')], 'Lei 1')
    o += track(20, 1060, 100, [(360, 700, 'on'), (700, 1060, 'off')], 'Lei 2')
    o += m(360, 140, 'Lei 2 revoga', size=10, anchor='middle') + m(700, 140, 'cautelar · Lei 1 volta', DIF, 10, 'middle')
    return frame(o, 'Duas faixas: a Lei 2 revoga a Lei 1; a cautelar contra a Lei 2 faz a Lei 1 voltar, efeito repristinatório')


@hero_n(27)
def _():
    days = [('sex', 'D1'), ('sáb', ''), ('dom', ''), ('seg', 'D2'), ('ter', 'D3'), ('qua', 'D4'), ('qui', 'D5'), ('sex', 'D6')]
    o = ''
    for i, (d, n) in enumerate(days):
        x = 20 + i * 110
        o += box(x, 40, 100, 50, 'var(--paper)' if n else 'var(--paper-2)') + m(x + 10, 60, d, MUTED, 10) + m(x + 10, 80, n, size=12, bold=True)
    o += m(20, 120, 'janela de 6 dias úteis · cada ministro vota no seu tempo', MUTED, 10.5)
    o += m(1060, 66, 'destaque', DIF, 11, 'end') + m(1060, 86, '→ presencial', DIF, 11, 'end')
    return frame(o, 'A janela da sessão virtual, de sexta a sexta, seis dias úteis; o destaque leva ao presencial')


@hero_n(28)
def _():
    def struck(y, cut, label):
        o = m(20, y - 8, label, MUTED, 10)
        if cut > 20:
            o += f'<rect x="20" y="{y}" width="{cut - 20}" height="16" style="fill:var(--ink)"/>'
        return o + box(cut, y, 760 - cut, 16) + f'<line x1="{cut}" y1="{y + 8}" x2="760" y2="{y + 8}" style="stroke:{DIF};stroke-width:3"/>'
    o = struck(40, 20, 'regra · ex tunc') + struck(96, 470, 'modulação · a partir do marco')
    o += m(1060, 66, 'art. 27 · 2/3', DIF, 11, 'end') + m(1060, 88, '8 de 11', DIF, 11, 'end')
    return frame(o, 'A faixa da lei apagada desde a origem, ex tunc, ou só a partir de um marco, com modulação por dois terços')


@hero_n(29)
def _():
    o = psheet(20, 12, 620, 128, 'ADI · acórdão')
    o += m(36, 60, 'fundamentos · ratio', MUTED, 10) + box(30, 92, 600, 30, 'none', DIF) + m(42, 112, 'dispositivo · eficácia contra todos', DIF, 10.5)
    o += m(1060, 66, 'efeito vinculante', size=11, anchor='end') + m(1060, 88, 'transcendência: teoria', CONC, 10.5, 'end')
    return frame(o, 'Um acórdão de ADI: os fundamentos e o dispositivo em azul, com eficácia contra todos')



def apply(n):
    from inject import ROOT, element_span
    p = os.path.join(ROOT, 'courses', 'controle-de-constitucionalidade', f'aula-{n:02d}.html')
    s = open(p).read()
    new = HEROES[n]()
    m = re.search(r'<svg\b[^>]*class="hero-fork[^"]*"', s)
    if m:
        a, b = element_span(s, m.start())
        s = s[:a] + new + s[b:]
    else:
        d = re.search(r'(?s)<p class="deck">.*?</p>', s)
        s = s[:d.end()] + '\n  ' + new + s[d.end():]
    open(p, 'w').write(s)


if __name__ == '__main__':
    for n in HEROES:
        apply(n)
    print(len(HEROES), 'heroes;', '\n'.join(WARN) or 'no text warnings')
