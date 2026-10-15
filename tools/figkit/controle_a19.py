"""Controle Aula 19 · reação legislativa and institutional dialogue, as the score family (see controle_a03):
one column per institution, one row per move. The two ways Congress can answer, the tests each gets, the
vaquejada sequence as real rows (ADI 4.983, 2016 → EC 96, 2017), and the juriscentric drift as a score whose
rows all fall in the STF's column. Blue = what a court decided; orange = the limit / the risk.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t, wrap

XL, XR, COLW, Y0, ROW = 40, 332, 222, 140, 70


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def say(x, y, s, size=16, fill='var(--ink)', italic=False):
    return f'<text x="{x}" y="{y}" style="font-family:var(--serif,serif);font-size:{size}px;fill:{fill}{";font-style:italic" if italic else ""}">{s}</text>'


def score(rows, cur=None, rows_y0=Y0, height=None):
    """rows: list of (col 'L'|'R', mono tag, text, tone). cur: index set in a box."""
    o = t(XL, 100, 'STF', size=12, weight=700, caps=True) + t(XR, 100, 'Congresso Nacional', size=12, weight=700, caps=True)
    o += '<line x1="40" y1="112" x2="560" y2="112" style="stroke:var(--ink);stroke-width:1.5"/>'
    o += f'<line x1="300" y1="86" x2="300" y2="{height or rows_y0 + ROW * max(len(rows), 1)}" style="stroke:var(--ink-2);stroke-width:1"/>'
    for i, (col, tag, s, tone) in enumerate(rows):
        y = rows_y0 + i * ROW
        x = XL if col == 'L' else XR
        lines = wrap(s, COLW, ch=7.3)
        if i == cur:
            o += f'<rect x="{x - 8}" y="{y - 16}" width="{COLW + 14}" height="{len(lines) * 17 + 28}" style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1.3"/>'
        o += t(x, y, tag, size=10, caps=True, weight=700, fill=tone)
        o += ''.join(f'<text x="{x}" y="{y + 18 + k * 17}" style="font-family:var(--serif,serif);font-size:14px;fill:var(--ink)">{ln}</text>' for k, ln in enumerate(lines))
    return o


def reacao1():
    o = head('Da decisão à reação')
    o += score([('L', 'decide', 'Declara a lei inconstitucional.', 'var(--dif)')], cur=0)
    o += t(XR, Y0 + ROW, 'reage · duas vias', size=10, caps=True, weight=700)
    for k, (tag, s) in enumerate([('lei ordinária', 'Lei de conteúdo semelhante.'), ('emenda', 'Muda o parâmetro de controle.')]):
        y = Y0 + ROW + 22 + k * 64
        o += f'<rect x="{XR - 8}" y="{y}" width="{COLW + 14}" height="52" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>'
        o += t(XR + 2, y + 18, tag, size=10, caps=True, weight=700) + say(XR + 2, y + 38, s, 14)
    o += say(40, 470, 'A presunção de constitucionalidade é relativa;')
    o += say(40, 494, 'a interpretação segue aberta a novas respostas.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-reacao1',
               label='Partitura: o STF declara a lei inconstitucional; o Congresso pode reagir por lei ordinária ou por emenda que muda o parâmetro')


def reacao2():
    o = head('Dois testes')
    o += score([('R', 'lei ordinária', 'Contraria de frente o precedente.', 'var(--ink)'),
                ('L', 'reexame', 'Presunção de inconstitucionalidade; o legislador justifica a superação com novas premissas.', 'var(--conc)'),
                ('R', 'emenda', 'Altera o parâmetro.', 'var(--ink)'),
                ('L', 'reexame', 'Limites formais e materiais do poder de reforma (art. 60).', 'var(--dif)')], height=440)
    o += say(40, 500, 'Lei: ônus argumentativo e controle mais rigoroso.', 15)
    o += say(40, 524, 'Emenda: o controle mira o poder de reforma.', 15)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-reacao2',
               label='Partitura com dois caminhos: a lei ordinária contrária ao precedente enfrenta presunção de inconstitucionalidade; a emenda é controlada pelos limites do art. 60')


def dialogo1():
    o = head('Partitura do diálogo · vaquejada')
    o += score([('L', 'ADI 4.983 · 2016', 'A vaquejada é incompatível com a vedação à crueldade.', 'var(--dif)'),
                ('R', 'EC 96 · 2017', 'Acrescenta o § 7º ao art. 225: novo parâmetro.', 'var(--ink)'),
                ('L', 'e depois', 'Novo controle, sobre o novo texto.', 'var(--ink-2)')], cur=1, height=380)
    o += say(40, 450, 'A última palavra é de quem decide por último,')
    o += say(40, 474, 'e segue sujeita à resposta do outro Poder.', 16, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-dialogo1',
               label='Partitura real: em 2016 o STF julga a vaquejada na ADI 4.983; em 2017 o Congresso responde com a EC 96; o diálogo segue')


def dialogo2():
    o = head('A crítica juriscêntrica')
    o += score([('L', 'decide', 'Escolha política difícil.', 'var(--ink)'), ('L', 'decide', 'Outra.', 'var(--ink)'), ('L', 'decide', 'E outra.', 'var(--ink)')], height=360)
    o += t(XR, Y0 + 30, '“o tribunal arruma depois”', size=10, caps=True, fill='var(--ink-2)')
    o += say(40, 430, 'Quando as escolhas difíceis migram ao Judiciário,')
    o += say(40, 454, 'a coluna do Legislativo fica vazia.')
    o += say(40, 498, 'É uma hipótese sobre incentivos institucionais.', 15, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-dialogo2',
               label='Partitura em que todas as jogadas caem na coluna do STF e a do Congresso fica vazia: o risco de transferir escolhas políticas ao Judiciário')


def panels():
    return [reacao1(), reacao2(), dialogo1(), dialogo2()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-19.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
