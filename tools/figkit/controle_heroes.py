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


def apply(n):
    from inject import ROOT, element_span
    p = os.path.join(ROOT, 'courses', 'controle-de-constitucionalidade', f'aula-{n}.html')
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
