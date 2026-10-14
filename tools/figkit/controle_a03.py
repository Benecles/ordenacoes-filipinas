"""Controle Aula 03 · Figs. 2–4: Kelsen × Schmitt as one score that grows round by round.
Two columns, one per voice; each round enters the column of whoever speaks; earlier rounds stay
on the page, the current one is set in a box. Position tells who speaks, so colour keeps its house
meaning (it used to be red = Kelsen, blue = Schmitt).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t, wrap

ROUNDS = [  # (speaker, the thesis in the lesson's words, short)
    ('K', 'Ninguém fiscaliza a si mesmo: o controle cabe a um órgão independente.'),
    ('S', 'Jurisdição não é isso: definir normas abertas é função política.'),
    ('K', 'Entre legislar e julgar há diferença de grau, não de natureza.'),
    ('S', 'Guarda da Constituição, sim, mas do chefe de Estado.'),
    ('S', 'Decisionismo: o tribunal decidiria sem controle o que vale.'),
    ('K', 'O chefe de Estado não é mais neutro que um tribunal.'),
    ('S', 'Juízes não eleitos: uma “aristocracia de toga”. Quem nomeia?'),
]
XK, XS, COLW, Y0, ROW = 40, 332, 222, 136, 63


def score(ident, upto, title, label, question=''):
    o = t(40, 46, title, size=11.5, weight=700, caps=True, ls='.12em')
    o += t(XK, 100, 'Hans Kelsen', size=12, weight=700, caps=True) + t(XS, 100, 'Carl Schmitt', size=12, weight=700, caps=True)
    o += f'<line x1="40" y1="112" x2="560" y2="112" style="stroke:var(--ink);stroke-width:1.5"/>'
    o += f'<line x1="300" y1="86" x2="300" y2="{Y0 + ROW * 7 if upto else 122}" style="stroke:var(--ink-2);stroke-width:1"/>'
    for i, (who, s) in enumerate(ROUNDS[:upto]):
        y = Y0 + i * ROW
        x = XK if who == 'K' else XS
        cur = i == upto - 1
        lines = wrap(s, COLW, ch=7.3)
        if cur:
            o += f'<rect x="{x - 8}" y="{y - 2}" width="{COLW + 14}" height="{len(lines) * 17 + 10}" style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1.3"/>'
        for k, ln in enumerate(lines):
            fill = 'var(--ink)' if cur else 'var(--ink-2)'
            o += f'<text x="{x}" y="{y + 15 + k * 17}" style="font-family:var(--serif,serif);font-size:14px;fill:{fill}">{ln}</text>'
        o += t(292, y + 16, f'{i + 1}', size=10, anchor='end', fill='var(--ink-2)') if who == 'K' else t(308, y + 16, f'{i + 1}', size=10, fill='var(--ink-2)')
    if question:
        o += f'<text x="40" y="230" style="font-family:var(--serif,serif);font-size:19px;fill:var(--ink)">{question}</text>'
    return svg('0 0 600 600', o, cls='panel fig on', ident=ident, label=label)


def panels():
    out = [
        score('p-anuncio', 0, 'O debate · século XX', 'Duas colunas vazias, Kelsen e Schmitt: a mesma pergunta, quem deve guardar a Constituição',
              'Quem deve ser o guarda da Constituição?'),
        score('p-confronto', 0, 'Tribunal constitucional?', 'Kelsen a favor de um tribunal constitucional, Schmitt contra',
              'Kelsen: um tribunal. Schmitt: não um tribunal.'),
    ]
    for k in range(1, 8):
        who = 'Kelsen' if ROUNDS[k - 1][0] == 'K' else 'Schmitt'
        out.append(score(f'p-r{k}', k, f'Rodada {k} · {who}', f'O debate até a rodada {k}: {who} diz que ' + ROUNDS[k - 1][1].lower()))
    return out


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    path = 'courses/controle-de-constitucionalidade/aula-03.html'
    n = inject(path, {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    p = os.path.join(os.path.dirname(__file__), '..', '..', path)
    h = open(p).read()
    old = 'No quadro comparativo, vermelho identifica Kelsen e azul identifica Schmitt.'
    if old in h:
        open(p, 'w').write(h.replace(old, 'No quadro, cada rodada entra na coluna de quem fala.'))
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
