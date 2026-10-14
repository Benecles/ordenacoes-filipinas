"""Controle Aula 16 · inconstitucionalidade progressiva e circunstancial, as strips through time.
Every panel uses the same instrument: a norm drawn as horizontal tracks (validade, aplicação) running left
to right in time. Progressive = one gauge that only moves one way; circumstantial = validity unbroken while
application is cut and resumed; the critique lays the three techniques' strips side by side.
Blue = what the STF decided; orange = the limit (temporary, excepted, carved out). Ink otherwise.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t

X0, X1 = 60, 540


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def say(x, y, s, size=16, fill='var(--ink)', italic=False, anchor='start'):
    a = '' if anchor == 'start' else f' text-anchor="{anchor}"'
    return f'<text x="{x}" y="{y}"{a} style="font-family:var(--serif,serif);font-size:{size}px;fill:{fill}{";font-style:italic" if italic else ""}">{s}</text>'


def track(y, segs, label, h=22):
    """segs: list of (x0, x1, kind) with kind in on | off | decided | limit | ghost."""
    o = t(X0, y - 10, label, size=10.5, caps=True, fill='var(--ink-2)')
    for a, b, k in segs:
        st = {'on': 'fill:var(--ink)', 'off': 'fill:none;stroke:var(--ink);stroke-width:1.2;stroke-dasharray:4 4',
              'decided': 'fill:var(--dif)', 'limit': 'fill:none;stroke:var(--conc);stroke-width:2',
              'ghost': 'fill:var(--paper-2);stroke:var(--ink-2);stroke-width:1'}[k]
        o += f'<rect x="{a}" y="{y}" width="{b - a}" height="{h}" style="{st}"/>'
    return o


def gauge(y, at, note=''):
    """the constitutionality spectrum: plena → imperfeita → total; the marker only moves right."""
    o = ''
    stops = [(X0, 'plena'), ((X0 + X1) / 2, 'imperfeita'), (X1, 'total')]
    o += f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" style="stroke:var(--ink);stroke-width:2"/>'
    for x, s in stops:
        o += f'<line x1="{x}" y1="{y - 8}" x2="{x}" y2="{y + 8}" style="stroke:var(--ink);stroke-width:1.5"/>'
        o += t(x, y + 28, s, size=10.5, caps=True, anchor='middle' if x not in (X0, X1) else ('start' if x == X0 else 'end'), fill='var(--ink-2)')
    o += f'<path d="M{X0} {y - 22} H{at}" style="stroke:var(--ink);stroke-width:1;stroke-dasharray:2 4"/>'
    o += f'<path d="M{at - 9} {y - 26} L{at + 9} {y - 26} L{at} {y - 10} Z" style="fill:var(--ink)"/>'
    o += f'<path d="M{at + 18} {y - 18} l14 0 m-5 -5 l5 5 l-5 5" style="fill:none;stroke:var(--conc);stroke-width:1.6"/>'
    if note:
        o += t(at, y - 38, note, size=10.5, caps=True, anchor='middle', weight=700)
    return o


def definicao():
    o = head('Inconstitucionalidade progressiva')
    o += gauge(170, 210, 'ainda constitucional')
    o += say(40, 280, 'Há indícios de inconstitucionalidade; os fatos de hoje')
    o += say(40, 304, 'ainda justificam a norma no ordenamento.')
    o += say(40, 352, 'Cabe ao legislador corrigi-la.', 16, 'var(--dif)')
    o += say(40, 400, 'O marcador só anda num sentido.', 15, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-definicao',
               label='Uma régua de plena constitucionalidade a total inconstitucionalidade; a norma ainda constitucional está perto do início, e o marcador só anda para a direita')


def espectro():
    o = head('O espectro não é binário')
    o += gauge(170, 410, 'o sentimento cresce')
    o += say(40, 280, '“O sentimento de inconstitucionalidade vai crescendo.”', 16, 'var(--ink)', True)
    o += say(40, 330, 'Uma trajetória num só sentido, sem prazo fixo')
    o += say(40, 354, 'para a passagem.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-espectro',
               label='O mesmo marcador avançou na régua, rumo à inconstitucionalidade, numa só direção e sem prazo fixo')


def paradoxo():
    o = head('Inconstitucionalidade circunstancial')
    o += t(X0, 96, 'Uma norma infraconstitucional X', size=11, caps=True)
    o += track(140, [(X0, X1, 'on')], 'validade · sempre')
    o += track(214, [(X0, 230, 'on'), (230, 370, 'off'), (370, X1, 'on')], 'aplicação · vai e volta')
    o += f'<path d="M230 244 V256 H370 V244" style="fill:none;stroke:var(--conc);stroke-width:1.6"/>' + t(300, 276, 'circunstância excepcional', size=10, anchor='middle', caps=True, fill='var(--conc)')
    o += say(40, 360, 'Como pode, sem mudar o texto, deixar de ser')
    o += say(40, 384, 'aplicada e depois voltar?')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-paradoxo',
               label='Duas faixas no tempo: a validade da norma corre inteira; a aplicação é interrompida durante uma circunstância excepcional e depois retomada')


def covid():
    o = head('ADI 6.357/DF · 13/05/2020')
    o += t(X0, 96, 'LRF e LDO 2020 · adequação e compensação', size=11, caps=True)
    o += track(140, [(X0, X1, 'on')], 'validade')
    o += track(214, [(X0, 230, 'on'), (230, 370, 'decided'), (370, X1, 'on')], 'exigência aplicada')
    o += '<line x1="230" y1="120" x2="230" y2="300" style="stroke:var(--dif);stroke-width:1.2"/>'
    o += t(230, 316, '13/05/2020', size=10.5, anchor='middle', caps=True, fill='var(--dif)')
    o += t(300, 268, 'suspensa pelo STF', size=10, anchor='middle', caps=True, fill='var(--dif)')
    o += t(455, 268, 'retomada', size=10, anchor='middle', caps=True, fill='var(--ink-2)')
    o += say(40, 380, 'Suspensa enquanto durasse a calamidade', 16, 'var(--conc)', True)
    o += say(40, 404, 'pública da pandemia; depois, de volta.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-covid',
               label='Na ADI 6.357, de 13 de maio de 2020, o STF suspendeu as exigências da LRF e da LDO enquanto durasse a calamidade; a validade das normas corre inteira')


def critica():
    o = head('Três técnicas, lado a lado')
    rows = [('Modulação', [(X0, 330, 'on'), (330, X1, 'ghost')], 'inválida · efeitos adiados'),
            ('Progressiva', [(X0, X1, 'ghost')], 'ainda constitucional · um só sentido'),
            ('“Circunstancial”', [(X0, 230, 'on'), (230, 370, 'off'), (370, X1, 'on')], 'válida · “inválida” · válida?')]
    for i, (name, segs, sub) in enumerate(rows):
        y = 110 + i * 92
        o += track(y, segs, name)
        o += t(X0, y + 42, sub, size=10.5, caps=True, fill='var(--ink-2)')
        if name == 'Progressiva':
            o += f'<path d="M{X0} {y + 11} H{X1 - 12} m-8 -7 l8 7 l-8 7" style="fill:none;stroke:var(--ink);stroke-width:2"/>'
    o += say(40, 420, 'Como algo seria inconstitucional num período')
    o += say(40, 444, 'e constitucional noutro?')
    o += say(40, 488, 'A crítica: é questão de vigência, não de validade.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-critica',
               label='Três faixas: modulação, uma norma inválida com efeitos adiados; progressiva, um único sentido; circunstancial, válida, inválida e válida de novo, o que a crítica recusa')


def alternativas():
    o = head('Duas saídas mais consistentes')
    o += t(X0, 96, 'Exceções implícitas · “a menos que”', size=11, caps=True)
    o += track(130, [(X0, X1, 'on')], 'validade')
    o += track(194, [(X0, 260, 'on'), (260, 340, 'limit'), (340, X1, 'on')], 'aplicação')
    o += t(300, 240, 'exceção', size=10, anchor='middle', caps=True, fill='var(--conc)')
    o += say(40, 280, 'Afasta a aplicação na situação anormal,', 15) + say(40, 300, 'sem declarar inconstitucionalidade.', 15)
    o += t(X0, 348, 'Declaração parcial sem redução de texto', size=11, caps=True)
    o += f'<rect x="{X0}" y="366" width="{X1 - X0}" height="70" style="fill:var(--ink)"/>'
    o += f'<rect x="330" y="366" width="110" height="70" style="fill:var(--paper);stroke:var(--conc);stroke-width:2"/>'
    o += t(385, 398, 'âmbito', size=10, anchor='middle', caps=True, fill='var(--conc)') + t(385, 412, 'não atingido', size=10, anchor='middle', caps=True, fill='var(--conc)')
    o += say(40, 470, 'Recorta um âmbito; preserva os demais, sem', 15) + say(40, 490, '“janelas temporais” entre válido e inválido.', 15)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-alternativas',
               label='Duas saídas: a exceção implícita corta a aplicação só na situação anormal; a declaração parcial sem redução de texto recorta um âmbito da norma e preserva o resto')


def panels():
    return [definicao(), espectro(), paradoxo(), covid(), critica(), alternativas()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-16.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
