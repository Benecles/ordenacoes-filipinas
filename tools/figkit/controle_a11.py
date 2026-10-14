"""Controle Aula 11 · Figs. 3 and 4: one petition drawn twice. In the via principal the constitutional
question is the pedido; in the via incidental it moves up into the direito, as the premise of a claim
between A and B. The position of the bracket is the whole point; colour keeps its house meaning
(blue = what the decision does, orange = its limit), never the system's name.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import Document, WARN, svg, t


def sheet(uid, title, parties, fatos, direito, pedido):
    return Document(uid, x=40, y=70, w=440, font_size=14.5, meta_size=12.5, label_size=10.5, lines=[
        ('title', title, 'title'),
        ('party', parties[0], 'p0'),
        ('party', parties[1], 'p1'),
        ('clause', ('Dos fatos', fatos), 'fatos'),
        ('clause', ('Do direito', direito), 'direito'),
        ('clause', ('Dos pedidos', pedido), 'pedido'),
        ('sign', ('Local e data', 'Advogado'), 'sig'),
    ], lead=27, indent=100)


def panel(ident, head, doc, at, sub, effect, limit, label):
    inner = t(40, 40, head, size=11.5, weight=700, caps=True, ls='.12em')
    inner += doc.paper() + doc.highlight([at], tone='muted') + ''.join(doc.parts)
    inner += doc.bracket([at], 'right', 'A questão', sub=sub, tone='ink', gap=14)
    y = doc.y + doc.h + 64
    inner += t(40, y, 'Se procedente', size=10, weight=700, caps=True, fill='var(--ink-2)')
    inner += t(40, y + 26, effect, size=15, weight=700, caps=True, fill='var(--dif)')
    if limit:
        inner += t(40, y + 50, limit, size=13, fill='var(--conc)')
    return svg('0 0 600 600', inner, cls='panel fig on', ident=ident, label=label)


def panels():
    conc = sheet('a11-p-conc', 'Exmo. Sr. Ministro Presidente do STF',
                 [('Requerente', 'um legitimado do art. 103 da CF'), ('Requerido', 'não há réu')],
                 'a Lei X foi publicada e está em vigor.',
                 'a Lei X contraria o art. Z da Constituição.',
                 'a declaração de inconstitucionalidade da Lei X.')
    dif = sheet('a11-p-dif', 'Exmo. Sr. Juiz de Direito',
                [('Autor', 'A'), ('Réu', 'B')],
                'B exige de A o que a Lei X determina.',
                'a Lei X contraria o art. Z da Constituição; logo, não obriga A.',
                'que A seja dispensado de cumprir o que B exige.')
    return [
        panel('p-conc', 'Via principal · ação direta', conc, 'pedido', 'é o pedido',
              'Contra todos · ex tunc', 'salvo modulação dos efeitos',
              'Petição de ação direta ao STF: não há réu, e a inconstitucionalidade da lei é o próprio pedido; se procedente, vale contra todos e, salvo modulação, desde a origem'),
        panel('p-dif', 'Via incidental · ação entre A e B', dif, 'direito', 'é premissa',
              'Entre A e B · ex tunc', '',
              'Petição de uma ação comum entre A e B: a inconstitucionalidade aparece nos fundamentos, como premissa do pedido; se acolhida, vale entre as partes'),
    ]


# ── Fig. 1 · the bench: who may set the law aside ──────────────────────────────────────────────────────
COLS, ROWS, X0, Y0, DX, DY = 14, 6, 64, 196, 34, 30


def seats(active):
    o = ''
    for r in range(ROWS):
        for c in range(COLS):
            x, y = X0 + c * DX, Y0 + r * DY
            st = 'fill:var(--ink);stroke:none' if active else 'fill:none;stroke:var(--ink-2);stroke-width:1.2'
            o += f'<circle cx="{x}" cy="{y}" r="6.5" style="{st}"/>'
    return o


def court(active, label):
    st = 'fill:var(--ink);stroke:var(--ink)' if active else 'fill:none;stroke:var(--ink-2);stroke-dasharray:4 4'
    o = f'<rect x="190" y="96" width="220" height="54" rx="2" style="{st};stroke-width:1.5"/>'
    o += t(300, 129, label, size=12, anchor='middle', weight=700, caps=True, fill='var(--paper)' if active else 'var(--ink-2)')
    return o


def bench(ident, head, judges, court_on, court_label, says, theory, note, label):
    inner = t(40, 46, head, size=11.5, weight=700, caps=True, ls='.12em')
    inner += court(court_on, court_label) if court_label else ''
    inner += seats(judges)
    inner += t(X0 - 6, Y0 + ROWS * DY + 6, 'juízes e tribunais', size=10, fill='var(--ink-2)', caps=True)
    y = Y0 + ROWS * DY + 52
    inner += f'<text x="40" y="{y}" style="font-family:var(--serif,serif);font-size:19px;fill:var(--ink)">{says}</text>'
    inner += f'<text x="40" y="{y + 30}" style="font-family:var(--serif,serif);font-size:16px;font-style:italic;fill:var(--ink-2)">{theory}</text>'
    if note:
        inner += f'<text x="40" y="{y + 70}" style="font-family:var(--serif,serif);font-size:16px;fill:var(--ink)">{note}</text>'
    return svg('0 0 600 600', inner, cls='panel fig on', ident=ident, label=label)


def fig1():
    return [
        bench('p-eua', 'Estados Unidos · sistema difuso', True, False, 'Trib. Constitucional', 'Qualquer juiz afasta a lei, no caso.',
              'Teoria da nulidade: a lei incompatível é nula.', '',
              'Assentos de juízes e tribunais, todos preenchidos: no sistema difuso qualquer juiz pode afastar a lei no caso que julga'),
        bench('p-ale', 'Alemanha · sistema concentrado', False, True, 'Trib. Constitucional', 'Um só órgão julga a lei.',
              'Teoria da anulabilidade.', '',
              'Os assentos dos juízes ficam vazios e só o Tribunal Constitucional está preenchido: no sistema concentrado um órgão especial julga a constitucionalidade'),
        bench('p-tensao', 'Brasil · sistema misto', True, True, 'STF', 'Qualquer juiz, no caso; o STF, também por ação.',
              'As duas heranças no mesmo país.', 'A mesma lei pode ser afastada aqui e aplicada ali.',
              'Todos os assentos e também o STF preenchidos: o Brasil combina o difuso, pela via de defesa, com o concentrado, pela via das ações diretas'),
    ]


# ── Fig. 5 · one law across many cases, before and after the STF ─────────────────────────────────────────
def grid(x0, y0, pattern):
    o = ''
    for i, on in enumerate(pattern):
        x, y = x0 + (i % 6) * 34, y0 + (i // 6) * 34
        st = 'fill:var(--ink);stroke:var(--ink)' if on else 'fill:none;stroke:var(--ink)'
        o += f'<rect x="{x}" y="{y}" width="24" height="24" style="{st};stroke-width:1.3"/>'
    return o


def fig5():
    before = [1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0]   # illustrative: outcomes split
    inner = t(40, 46, 'A mesma lei em 24 processos', size=11.5, weight=700, caps=True, ls='.12em')
    inner += t(40, 96, 'Antes do STF', size=11, weight=700, caps=True)
    inner += t(330, 96, 'Depois · súmula vinculante', size=11, weight=700, caps=True, fill='var(--dif)')
    inner += grid(40, 116, before) + grid(330, 116, [1] * 24)
    inner += '<line x1="300" y1="80" x2="300" y2="270" style="stroke:var(--ink-2);stroke-width:1;stroke-dasharray:3 4"/>'
    inner += '<rect x="40" y="306" width="18" height="18" style="fill:var(--ink)"/>' + t(66, 320, 'lei afastada', size=11)
    inner += '<rect x="190" y="306" width="18" height="18" style="fill:none;stroke:var(--ink);stroke-width:1.3"/>' + t(216, 320, 'lei aplicada', size=11)
    serif = 'font-family:var(--serif,serif);font-size:17px;fill:var(--ink)'
    inner += f'<text x="40" y="384" style="{serif}">Antes, cada instância decide só o seu caso.</text>'
    inner += f'<text x="40" y="414" style="{serif}">Depois, a súmula vinculante alinha os demais.</text>'
    inner += f'<text x="40" y="468" style="{serif};font-style:italic;fill:var(--conc)">Sem ela, a decisão difusa do STF não vale,</text>'
    inner += f'<text x="40" y="492" style="{serif};font-style:italic;fill:var(--conc)">por si só, contra todos.</text>'
    return svg('0 0 600 600', inner, cls='panel fig on', ident='p-inst',
               label='Vinte e quatro processos sobre a mesma lei: antes do STF, uns a afastam e outros a aplicam; depois de uma súmula vinculante, todos seguem a mesma solução')


# ── Fig. 2 · two questions, two answers each; the usual pairs, linked but not the same ─────────────────────
def mini_bench(x, y, filled, court):
    o = ''
    for r in range(3):
        for c in range(6):
            st = 'fill:var(--ink)' if filled else 'fill:none;stroke:var(--ink-2);stroke-width:1.1'
            o += f'<circle cx="{x + c * 16}" cy="{y + 22 + r * 14}" r="4" style="{st}"/>'
    if court:
        o += f'<rect x="{x + 22}" y="{y - 6}" width="44" height="16" style="fill:var(--ink)"/>'
    return o


def mini_sheet(x, y, row):
    o = f'<path d="M{x} {y}H{x + 62}L{x + 74} {y + 12}V{y + 66}H{x}Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.3"/>'
    for i in range(4):
        yy = y + 16 + i * 13
        if i == row:
            o += f'<rect x="{x + 6}" y="{yy - 6}" width="60" height="11" style="fill:var(--paper-2)"/>'
        o += f'<line x1="{x + 10}" y1="{yy}" x2="{x + 62}" y2="{yy}" style="stroke:var(--ink);stroke-width:{2.2 if i == row else 1}"/>'
    return o


def fig2():
    serif = 'font-family:var(--serif,serif);font-size:17px;fill:var(--ink)'
    inner = t(40, 46, 'Sistema · quem controla', size=11.5, weight=700, caps=True, ls='.12em')
    inner += mini_bench(60, 70, True, False) + f'<text x="60" y="160" style="{serif}">qualquer juiz</text>' + t(60, 180, 'difuso', size=11, caps=True, fill='var(--ink-2)')
    inner += mini_bench(360, 70, False, True) + f'<text x="360" y="160" style="{serif}">um ou poucos órgãos</text>' + t(360, 180, 'concentrado', size=11, caps=True, fill='var(--ink-2)')
    inner += '<line x1="40" y1="222" x2="560" y2="222" style="stroke:var(--ink-2);stroke-width:1"/>'
    inner += t(40, 262, 'Técnica · onde está a questão', size=11.5, weight=700, caps=True, ls='.12em')
    inner += mini_sheet(60, 286, 1) + f'<text x="60" y="384" style="{serif}">na premissa do pedido</text>' + t(60, 404, 'em concreto · incidental', size=11, caps=True, fill='var(--ink-2)')
    inner += mini_sheet(360, 286, 3) + f'<text x="360" y="384" style="{serif}">no próprio pedido</text>' + t(360, 404, 'em abstrato · principal', size=11, caps=True, fill='var(--ink-2)')
    inner += f'<text x="40" y="470" style="{serif}">Os pares costumam andar juntos,</text>'
    inner += f'<text x="40" y="496" style="{serif}">mas respondem a perguntas diferentes.</text>'
    inner += f'<text x="40" y="540" style="{serif};font-style:italic;fill:var(--ink-2)">Misto: o Brasil tem os dois sistemas.</text>'
    return svg('0 0 600 600', inner, cls='panel fig on', ident='p-matriz',
               label='Duas perguntas: quem controla (qualquer juiz ou um órgão) e onde está a questão (na premissa ou no próprio pedido); os pares difuso-concreto e concentrado-abstrato costumam andar juntos')


def fig2_quem():
    return bench('p-quem', 'Quem controla', True, True, 'STF', 'Difuso: qualquer juiz ou tribunal.',
                 'Concentrado: um ou poucos órgãos.', 'No Brasil, as ações diretas vão ao STF.',
                 'Assentos de juízes preenchidos e o STF preenchido: no difuso qualquer juiz controla; no concentrado, um ou poucos órgãos, no Brasil o STF')


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    ps = panels() + fig1() + [fig5(), fig2(), fig2_quem()]
    n = inject('courses/controle-de-constitucionalidade/aula-11.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in ps})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
